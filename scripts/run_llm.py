import copy
import glob
import json
import os
import argparse
from pathlib import Path
from datetime import datetime
import random
import subprocess
import re
import difflib

from openai import OpenAI
import ai2thor.controller

import sys
sys.path.append(".")

# 사용 가능한 로봇 액션 목록 (14종) 및 로봇 프로필(스킬, 질량) 정의 파일
import resources.actions as actions
import resources.robots as robots


# ============================================================
# [스킬명 정규화] normalize_skills - allocation 출력의 깨진 스킬명 교정
# 배경: LLM이 로봇 스킬 목록을 출력할 때(특히 마지막 로봇) 형식이 자주 깨진다.
#       공백 삽입('Pickup Object'), 대소문자('Pickupobject'),
#       글자 잘림('PickupObjec'), 글자 추가/환각('GoToObjective').
# 안전 원칙: 확실한 것만 결정론으로 고치고, 애매하면 원문을 그대로 둔다.
# ============================================================

# ── 정상 스킬 14종: resources/actions.py에서 파생 (하드코딩 중복/드리프트 방지) ──
#   actions.ai2thor_actions = "GoToObject <robot><object>, OpenObject <robot>..., PullObject ..."
#   ', '로 split 후 각 조각의 첫 토큰이 스킬명이다.
CANONICAL_SKILLS = [seg.strip().split()[0]
                    for seg in actions.ai2thor_actions.split(',')
                    if seg.strip()]

# 정규화 키(소문자) → 정상명
_SKILL_LOOKUP = {s.lower(): s for s in CANONICAL_SKILLS}


# CamelCase를 하위 단어로 분해해, '하위단어 사이 공백 허용 + 대소문자 무시' 패턴 생성
#   'PickupObject' → ['Pickup','Object'] → r'\bPickup\s*Object\b' (IGNORECASE)
def _skill_pattern(name):
    parts = re.findall(r'[A-Z][a-z]*', name)            # 'GoToObject'→['Go','To','Object']
    return re.compile(r'\b' + r'\s*'.join(parts) + r'\b', re.IGNORECASE)


# 긴 이름이 짧은 이름보다 먼저 매칭되도록 정렬
_SKILL_PATTERNS = sorted(((s, _skill_pattern(s)) for s in CANONICAL_SKILLS),
                         key=lambda p: -len(p[0]))

# 2차 후보: 길이 6+ 의 한 덩어리 알파벳 토큰만
_CAMEL_TOKEN = re.compile(r'\b[A-Za-z]{6,}\b')

# 2차(편집거리) 오교정 방지 파라미터
_FUZZY_THRESHOLD = 0.85    # 이 유사도 미만이면 손대지 않음
_FUZZY_MARGIN    = 0.07    # 1등-2등 유사도 차가 이보다 작으면(애매) 보류


def normalize_skills(text):
    """allocation 출력 텍스트의 깨진 스킬명을 정상 14종으로 교정한다.
    정상 스킬명/무관한 텍스트는 건드리지 않는다(안전 우선)."""
    if not text:
        return text

    # ── 1차: 공백 삽입 + 대소문자 깨짐 (결정론적, 오교정 0) ──
    # 글자 '구성'이 정상 스킬과 정확히 일치할 때만 치환된다.
    #   'Pickup Object', 'Pickupobject', 'PICKUPOBJECT' → 'PickupObject'
    # 전부 소문자인 매치는 평문(prose)일 가능성 → 건드리지 않는다.
    for canon, pat in _SKILL_PATTERNS:
        text = pat.sub(
            lambda m, c=canon: m.group(0) if m.group(0).islower() else c,
            text)

    # ── 2차: 글자 잘림/추가(환각) — 편집거리 기반, 임계값으로 오교정 차단 ──
    def _stage2(m):
        tok = m.group(0)
        key = tok.lower()

        # (a) 이미 정상 스킬이면 절대 손대지 않음
        if key in _SKILL_LOOKUP:
            return tok
        # (b) '스킬 시도' 형태만 후보: 대문자 2개 이상인 CamelCase 토큰만
        #     (일반 단어/문장 첫 단어/고유명사 대부분 제외)
        if sum(c.isupper() for c in tok) < 2:
            return tok

        scored = sorted(
            ((difflib.SequenceMatcher(None, key, c.lower()).ratio(), c)
             for c in CANONICAL_SKILLS),
            reverse=True)
        best_r, best_c = scored[0]
        second_r = scored[1][0]

        # (c) 임계값 미달 → 보류   (d) 1등-2등이 애매하면 → 보류
        if best_r < _FUZZY_THRESHOLD or best_r - second_r < _FUZZY_MARGIN:
            return tok
        return best_c

    return _CAMEL_TOKEN.sub(_stage2, text)


# ============================================================
# [스킬 검증] validate_skills - decompose 단계의 필요 스킬을 검증
# 목적: 분해된 서브태스크가 요구하는 스킬을, (1) 14종(actions.py)에 정의된
#       스킬인지, (2) 해당 태스크에 배정된 로봇들이 실제로 보유하는지 검사한다.
#       환각/배정미스를 탐지해 경고만 남기며, 계획 생성은 차단하지 않는다.
# 배경: 2-2 실험에서 LLM이 없는 스킬을 환각(예: Paint)하거나, 정의는 됐지만
#       배정 로봇이 못 가진 스킬(예: CleanObject - 14종엔 있으나 보유 로봇 없음)을
#       요구하는 경우가 관찰됨.
# ============================================================

# decompose 출력의 'Skills Required: GoToObject, PickupObject)' 표기를 잡는 정규식.
# - 'Skills Required:' 이후, 닫는 괄호 ')' 또는 줄바꿈 직전까지를 캡처한다.
# - 이 표기는 'GENERAL TASK DECOMPOSITION' 불릿 라인에만 등장한다.
_SKILLS_REQUIRED_RE = re.compile(r'Skills Required:\s*([^)\n]+)')


def extract_required_skills(decomposed_text):
    """decompose 출력 텍스트에서 (서브태스크 라벨, [필요 스킬, ...]) 리스트를 추출한다."""
    results = []
    for line in decomposed_text.splitlines():
        m = _SKILLS_REQUIRED_RE.search(line)
        if not m:
            continue
        # 콤마로 분리 후 감싼 마크다운/구두점(`, *, ., ', ", 공백)을 벗긴다.
        #   예: '`GoToObject`'  -> 'GoToObject',  'PutObject.' -> 'PutObject'
        skills = [s.strip().strip('`*.\'" ') for s in m.group(1).split(',')]
        skills = [s for s in skills if s]   # 빈 토큰 제거
        results.append((line.strip(), skills))
    return results


def validate_skills(decomposed_text, task_robots):
    """필요 스킬을 두 단계로 검증하고 경고 문자열 리스트를 반환한다(차단하지 않음).
      - 14종(actions.py)에 아예 없는 스킬        → '[환각] 정의되지 않은 스킬: X'
      - 14종엔 있으나 배정 로봇이 미보유한 스킬   → '[배정미스] 로봇이 보유하지 않은 스킬: X'
    task_robots: 해당 태스크에 배정된 로봇 dict 리스트(각 dict는 'skills' 키 보유)."""
    canonical = set(CANONICAL_SKILLS)              # 14종 정의 스킬 (actions.py 파생)
    robot_skills = set()                           # 배정 로봇들의 스킬 합집합
    for r in task_robots:
        robot_skills.update(r.get('skills', []))

    warnings = []
    for label, skills in extract_required_skills(decomposed_text):
        for sk in skills:
            # 대소문자/공백 깨짐을 정상 14종명으로 보정 시도(없으면 원문 유지)
            sk_norm = _SKILL_LOOKUP.get(sk.lower(), sk)
            if sk_norm not in canonical:
                warnings.append(f"[환각] 정의되지 않은 스킬: {sk}  ({label})")
            elif sk_norm not in robot_skills:
                warnings.append(f"[배정미스] 로봇이 보유하지 않은 스킬: {sk_norm}  ({label})")
    return warnings


# ============================================================
# [핵심 함수 1] LM - LLM(GPT) API 호출 래퍼  (openai>=1.0 신 SDK)
# 역할: GPT 계열 모델에 프롬프트를 보내고 텍스트 응답을 반환한다.
# 변경: openai.ChatCompletion.create → client.chat.completions.create
#       구버전 Completion API 분기(text-davinci 등 퇴역 모델)는 제거.
# 인자: client - OpenAI() 클라이언트 객체 (set_api_key가 반환)
#       prompt - messages 리스트 [{"role": ..., "content": ...}] 형태
# 반환값: (전체 response 객체, 생성된 텍스트 문자열) 튜플
#         (호출부는 모두 _, text 로 받아 text만 사용하므로 첫 값은 호환용 유지)
# ============================================================
def LM(client, prompt, gpt_version, max_tokens=128, temperature=0, stop=None, frequency_penalty=0):

    # ── 신 SDK: 모든 gpt-4o / gpt-4 계열은 Chat Completions 단일 경로 ──
    # 응답 파싱이 딕셔너리 첨자(response["choices"]...)에서 객체 속성 접근으로 바뀜.
    response = client.chat.completions.create(model=gpt_version,
                                              messages=prompt,
                                              max_tokens=max_tokens,
                                              temperature=temperature,
                                              stop=stop,
                                              frequency_penalty=frequency_penalty)

    return response, response.choices[0].message.content.strip()


# ============================================================
# [핵심 함수 2] set_api_key - OpenAI 클라이언트 생성  (openai>=1.0 신 SDK)
# 역할: api_key.txt 파일에서 키를 읽어 OpenAI 클라이언트 객체를 만들어 반환한다.
# 변경: 전역 openai.api_key 할당 방식 → OpenAI(api_key=...) 클라이언트 객체 반환.
#       .strip()으로 파일 끝 개행/공백을 제거 (개행 포함 시 인증 실패 방지).
# ============================================================
def set_api_key(openai_api_key):
    api_key = Path(openai_api_key + '.txt').read_text().strip()
    return OpenAI(api_key=api_key)


# ============================================================
# [핵심 함수 3] convert_to_dict_objprop - 객체 목록을 딕셔너리 형태로 변환
# 역할: AI2-THOR에서 가져온 raw 객체 이름/질량 리스트를
#        [{'name': 'Apple', 'mass': 0.3}, ...] 형태로 구조화한다.
# 이 형식이 프롬프트 내 objects= [...] 로 LLM에게 주입된다.
# ============================================================
def convert_to_dict_objprop(objs, obj_mass):
    objs_dict = []
    for i, obj in enumerate(objs):
        obj_dict = {'name': obj , 'mass' : obj_mass[i]}
        # obj_dict = {'name': obj , 'mass' : 1.0}  # 디버그용: 질량을 1.0으로 고정할 때 사용
        objs_dict.append(obj_dict)
    return objs_dict


# ============================================================
# [핵심 함수 4] get_ai2_thor_objects - AI2-THOR 씬에서 객체 목록 조회
# 역할: 지정된 플로어플랜(방 번호)을 AI2-THOR 시뮬레이터에서 실행하여
#        해당 씬에 실제로 존재하는 객체 이름과 질량 정보를 가져온다.
# 반환값: [{'name': 'Apple', 'mass': 0.3}, {'name': 'Knife', 'mass': 0.5}, ...] 형태
# 주의: 매 호출마다 Controller 인스턴스를 새로 생성하고 종료한다. (→ 개선 포인트)
# ============================================================
def get_ai2_thor_objects(floor_plan_id):
    # AI2-THOR 시뮬레이터에 접속하여 해당 플로어플랜의 씬을 로드
    controller = ai2thor.controller.Controller(scene="FloorPlan"+str(floor_plan_id))
    # 씬 내 모든 오브젝트의 타입 이름 추출 (예: 'Apple', 'Knife', 'Fridge' ...)
    obj = list([obj["objectType"] for obj in controller.last_event.metadata["objects"]])
    # 씬 내 모든 오브젝트의 물리적 질량(kg) 추출 → 로봇 mass_capacity 제약에 사용됨
    obj_mass = list([obj["mass"] for obj in controller.last_event.metadata["objects"]])
    controller.stop()  # 객체 조회 후 즉시 시뮬레이터 종료
    obj = convert_to_dict_objprop(obj, obj_mass)
    return obj


# ============================================================
# 메인 실행 블록: 전체 4단계 파이프라인(분해 → 연합 → 할당 → 저장)을 순서대로 실행
# ============================================================
if __name__ == "__main__":

    # ── 커맨드라인 인자 파싱 ──
    parser = argparse.ArgumentParser()
    parser.add_argument("--floor-plan", type=int, required=True)          # 테스트할 방 번호 (필수)
    parser.add_argument("--openai-api-key-file", type=str, default="api_key")  # API 키 파일 이름
    parser.add_argument("--gpt-version", type=str, default="gpt-4o-mini",
                        choices=['gpt-4o-mini', 'gpt-4o', 'gpt-4'])  # 사용할 GPT 모델

    # Few-shot 프롬프트 파일 이름 (현재 단일 선택지만 존재)
    parser.add_argument("--prompt-decompse-set", type=str, default="train_task_decompose",
                        choices=['train_task_decompose'])

    parser.add_argument("--prompt-allocation-set", type=str, default="train_task_allocation",
                        choices=['train_task_allocation'])

    parser.add_argument("--test-set", type=str, default="final_test",
                        choices=['final_test'])

    parser.add_argument("--log-results", type=bool, default=True)  # 결과를 logs/ 폴더에 저장할지 여부

    args = parser.parse_args()

    # OpenAI 클라이언트 객체 생성 (이후 모든 LM 호출에 명시적으로 전달)
    client = set_api_key(args.openai_api_key_file)

    # logs/ 폴더가 없으면 생성
    if not os.path.isdir(f"./logs/"):
        os.makedirs(f"./logs/")

    # ── 테스트 데이터 로드 ──
    # data/final_test/FloorPlan{번호}.json 파일에서 태스크/로봇/정답 정보를 읽는다.
    # JSON 각 줄의 구조: {"task": "...", "robot list": [...], "object_states": [...], "trans": 0, "max_trans": 0}
    test_tasks = []          # 자연어 태스크 설명 목록 (예: "Slice the tomato")
    robots_test_tasks = []   # 각 태스크에 사용할 로봇 ID 목록 (예: [2, 3, 4])
    gt_test_tasks = []       # 정답(ground truth) 상태 목록 → 실행 후 성공 여부 평가에 사용
    trans_cnt_tasks = []     # 실제 전환(transition) 횟수
    max_trans_cnt_tasks = [] # 최대 허용 전환 횟수
    with open (f"./data/{args.test_set}/FloorPlan{args.floor_plan}.json", "r") as f:
        for line in f.readlines():
            # values()의 순서가 JSON 필드 순서에 의존한다. (→ 개선 포인트: 키 직접 접근)
            test_tasks.append(list(json.loads(line).values())[0])
            robots_test_tasks.append(list(json.loads(line).values())[1])
            gt_test_tasks.append(list(json.loads(line).values())[2])
            trans_cnt_tasks.append(list(json.loads(line).values())[3])
            max_trans_cnt_tasks.append(list(json.loads(line).values())[4])

    print(f"\n----Test set tasks----\n{test_tasks}\nTotal: {len(test_tasks)} tasks\n")

    # ── 로봇 객체 준비 ──
    # robots_test_tasks의 ID를 resources/robots.py의 로봇 프로필로 변환하고 이름을 재지정한다.
    # 예: ID=2 → robot2 프로필 → 이름을 'robot1'로 재지정 (태스크별 순번)
    available_robots = []
    for robots_list in robots_test_tasks:
        task_robots = []
        for i, r_id in enumerate(robots_list):
            rob = robots.robots [r_id-1]  # ID는 1-based, 리스트는 0-based
            # 같은 로봇 타입이라도 태스크마다 robot1, robot2... 로 순번 재지정
            rob['name'] = 'robot' + str(i+1)
            task_robots.append(rob)
        available_robots.append(task_robots)


    # ============================================================
    # [1단계] Task Decomposition (작업 분해)
    # 목표: 자연어 태스크를 로봇이 실행 가능한 Python 서브태스크 함수들로 분해한다.
    # 방법: Few-shot 프롬프팅 — LLM에게 예시 입출력 쌍을 보여주고 패턴을 학습시킨다.
    # 출력: decomposed_plan (list[str]) — 각 태스크에 대한 Python 코드 문자열
    # ============================================================

    # ── [1-A] 프롬프트 헤더 구성 (레이어 1: 환경 컨텍스트) ──
    # 역할: LLM이 사용할 수 있는 도구(스킬)와 씬 환경을 명시한다.
    # "from skills import ..."는 LLM의 출력을 이 14개 함수로만 제한하는 핵심 제약이다.
    prompt = f"from skills import " + actions.ai2thor_actions
    # threading 모듈: 병렬 서브태스크 실행을 위해 필요
    prompt += f"\nimport time"
    prompt += f"\nimport threading"
    # AI2-THOR 씬에서 실제 존재하는 객체 목록을 실시간으로 가져와 주입한다.
    # 이 정보가 LLM의 객체 환각(존재하지 않는 객체 참조)을 억제하는 역할을 한다.
    objects_ai = f"\n\nobjects = {get_ai2_thor_objects(args.floor_plan)}"
    prompt += objects_ai

    # ── [1-B] Few-shot 예시 주입 (레이어 2: 출력 형식 패턴 학습) ──
    # data/pythonic_plans/train_task_decompose.py 에는 4개의 예시 태스크가 들어있다.
    # 각 예시는 "# Task Description: ..." → "# SubTask N: ..." → "def subtask(): ..." → threading 코드
    # 순서로 이루어져 있으며, LLM이 이 패턴을 보고 새 태스크에 동일한 형식으로 응답한다.
    decompose_prompt_file = open(os.getcwd() + "/data/pythonic_plans/" + args.prompt_decompse_set + ".py", "r")
    decompose_prompt = decompose_prompt_file.read()
    decompose_prompt_file.close()

    # 최종 공유 프롬프트 = 헤더(스킬+객체목록) + 4개 Few-shot 예시
    # 이 prompt는 모든 태스크에 공통으로 재사용되므로, 루프 밖에서 한 번만 조립된다.
    prompt += "\n\n" + decompose_prompt

    print ("Generating Decompsed Plans...")

    # ── [1-C] 각 태스크에 대해 LLM 호출 및 분해 결과 수집 ──
    # decomposed_plan: list[str]
    #   인덱스 i → 태스크 i에 대한 Python 코드 문자열
    #   예) "def slice_tomato():\n    GoToObject('Knife')\n    ..."
    decomposed_plan = []
    for task in test_tasks:
        # ── [1-C-i] 태스크별 프롬프트 완성 (레이어 3: 실제 쿼리 주입) ──
        # "# Task Description:" 태그가 LLM에게 "여기서부터가 실제 문제" 임을 알려주는 유일한 구분자다.
        # 자연어 태스크(예: "Slice the tomato")가 이 지점에서 최초로 프롬프트에 삽입된다.
        curr_prompt =  f"{prompt}\n\n# Task Description: {task}"

        if "gpt" not in args.gpt_version:
            # ── 구버전 GPT: Completion API 사용
            # stop=["def"]: 다음 함수 정의 전에 출력 중단 (구버전 특성)
            # frequency_penalty=0.15: 반복 표현을 약하게 억제
            _, text = LM(client, curr_prompt, args.gpt_version, max_tokens=1000, stop=["def"], frequency_penalty=0.15)
        else:
            # ── 신버전 GPT (gpt-3.5-turbo, gpt-4): ChatCompletion API 사용
            # system message 없음 — 제약은 오직 few-shot 패턴만으로 전달된다.
            # (3단계 Allocation과의 차이점: Allocation은 system message로 역할을 명시)
            # temperature=0 (기본값): 결정론적 출력 → 재현 가능성 확보
            # frequency_penalty=0.0: 반복 억제 없음 (반복 서브태스크 구조를 해치지 않기 위해)
            # max_tokens=1300: 복잡한 태스크의 긴 코드를 수용하기 위한 여유 크기
            messages = [{"role": "user", "content": curr_prompt}]
            _, text = LM(client, messages, args.gpt_version, max_tokens=1300, frequency_penalty=0.0)

        # LLM이 생성한 Python 코드 문자열을 결과 리스트에 추가
        # 이 text는 다음 단계(2단계 Coalition Formation)의 프롬프트 입력으로 그대로 연결된다.
        decomposed_plan.append(text)

    print ("Generating Allocation Solution...")

    # ============================================================
    # [2단계] Coalition Formation (연합 구성)
    # 목표: 1단계에서 분해된 각 서브태스크에 대해, 어떤 로봇(들)이 수행할지 결정한다.
    #       단일 로봇으로 불가능한 경우 로봇 팀(Coalition)을 구성한다.
    # 방법: Few-shot 프롬프팅 + System Message (GPT-4)
    # 출력: allocated_plan (list[str]) — 로봇 배정 근거를 서술한 자연어 추론 텍스트
    #       이 텍스트는 코드가 아니며, 3단계(Code Generation)의 추론 근거로 전달된다.
    #
    # 핵심 판단 로직 (LLM이 수행):
    #   - 모든 로봇의 스킬이 동일하면 → 질량(mass) 기반 할당
    #   - 로봇마다 스킬이 다르면    → 스킬(skill) 기반 할당
    #   - 단일 로봇으로 부족하면   → Coalition: 스킬 합집합 or 질량 합산
    # ============================================================

    ######## Train Task Allocation - SOLUTION ########

    # ── [2-A] 2단계 공유 프롬프트 헤더 구성 ──
    # 1단계와 동일한 스킬/모듈 선언으로 시작한다.
    # (LLM이 1단계 코드를 이어서 읽을 때 동일한 컨텍스트를 유지하기 위함)
    prompt = f"from skills import " + actions.ai2thor_actions
    prompt += f"\nimport time"
    prompt += f"\nimport threading"

    # ── [2-B] Few-shot 예시 로드 ──
    # train_task_allocation_solution.py에는 3가지 시나리오 예시가 들어있다:
    #   EXAMPLE 1: 로봇 스킬이 달라서 스킬 기반 할당 → 단일 로봇 배정 (직렬화)
    #   EXAMPLE 2: 어떤 로봇도 필요 스킬을 혼자 못 가짐 → Coalition 팀 구성
    #   EXAMPLE 3: 스킬은 같지만 질량 초과 → 질량 합산 팀 구성
    # 이 3가지가 LLM에게 모든 분기 경우를 학습시키는 핵심 Few-shot이다.
    prompt_file = os.getcwd() + "/data/pythonic_plans/" + args.prompt_allocation_set + "_solution.py"
    allocated_prompt_file = open(prompt_file, "r")
    allocated_prompt = allocated_prompt_file.read()
    allocated_prompt_file.close()

    # 공유 프롬프트 = 헤더 + 3개 Few-shot 예시
    # 이 prompt는 모든 태스크에 재사용되며 루프 밖에서 한 번만 조립된다.
    prompt += "\n\n" + allocated_prompt + "\n\n"

    # ── [2-C] 태스크별 LLM 호출 및 Coalition 추론 결과 수집 ──
    # allocated_plan: list[str]
    #   인덱스 i → 태스크 i에 대한 로봇 배정 추론 텍스트
    #   (예: "Robot1+Robot3 팀이 필요. Robot1은 SliceObject, Robot3은 PickupObject 보유...")
    allocated_plan = []
    for i, plan in enumerate(decomposed_plan):

        # ── [2-C-i] 1단계 출력(decomposed_plan[i])을 프롬프트에 직접 이어붙임 ──
        # 별도 파싱 없이 Python 코드 문자열 그대로 연결된다.
        # 1단계가 생성한 "# Skills Required: ..." 주석이 여기서 로봇 스킬 매칭의 근거가 된다.
        no_robot = len(available_robots[i])  # 이 태스크에 투입 가능한 로봇 수
        curr_prompt = prompt + plan           # Few-shot + 1단계 코드 출력 연결

        # ── [2-C-ii] 2단계 질의 블록 추가 ──
        # "# TASK ALLOCATION" 태그가 1단계 코드 영역의 끝과 2단계 시작을 구분한다.
        curr_prompt += f"\n# TASK ALLOCATION"

        # 태스크별 로봇 수와 할당 원칙을 자연어로 명시 (Few-shot과 같은 포맷 유지)
        # "minimum number of robots" 원칙 → 불필요한 로봇 낭비 방지
        curr_prompt += f"\n# Scenario: There are {no_robot} robots available, The task should be performed using the minimum number of robots necessary. Robots should be assigned to subtasks that match its skills and mass capacity. Using your reasoning come up with a solution to satisfy all contraints."

        # ── [2-C-iii] 로봇 스펙 주입 ──
        # resources/robots.py에서 읽어온 실제 로봇 딕셔너리를 Python 리터럴로 변환하여 삽입.
        # 각 로봇의 {'name', 'skills', 'mass_capacity'} 필드가 LLM의 스킬/질량 매칭 근거가 된다.
        # 주의: Few-shot 예시에는 'no_skills' 필드가 있지만 실제 주입값에는 없다.
        #       LLM이 스킬 개수를 직접 세도록 유도하는 Gap이 존재한다. (→ 개선 포인트)
        curr_prompt += f"\n\nrobots = {available_robots[i]}"

        # ── [2-C-iv] 씬 객체 목록 재주입 ──
        # 1단계에서 이미 주입된 objects_ai를 2단계에서도 다시 삽입한다.
        # 이유: 질량 기반 할당 시 객체 mass 값이 필요하므로 LLM이 참조할 수 있어야 한다.
        curr_prompt += f"\n{objects_ai}"

        # ── [2-C-v] 최종 지시문 + SOLUTION 태그 ──
        # "# IMPORTANT" 지시가 LLM에게 두 가지 핵심 조건을 재확인시킨다:
        #   1) 로봇 스킬이 태스크 요구 스킬을 충족하는지 반드시 검증할 것
        #   2) 병렬/순차 실행 여부를 판단하고 가용성에 기반해 배정할 것
        # "# SOLUTION" 태그가 LLM의 응답 시작점을 지정한다 (Few-shot 패턴 유지)
        curr_prompt += f"\n\n# IMPORTANT: The AI should ensure that the robots assigned to the tasks have all the necessary skills to perform the tasks. IMPORTANT: Determine whether the subtasks must be performed sequentially or in parallel, or a combination of both and allocate robots based on availablitiy. "
        curr_prompt += f"\n# SOLUTION  \n"

        # ── [2-D] 모델별 LLM 호출 ──
        if "gpt" not in args.gpt_version:
            # ── 구버전 GPT (Completion API): frequency_penalty=0.65로 강하게 억제
            # 2단계는 1단계(0.15)보다 penalty가 훨씬 높다.
            # 이유: 추론 텍스트에서 같은 결론이 반복 서술되는 것을 방지
            _, text = LM(client, curr_prompt, args.gpt_version, max_tokens=1000, stop=["def"], frequency_penalty=0.65)

        elif "gpt-3.5" in args.gpt_version:
            # ── GPT-3.5 계열: system message 없이 user message만 사용
            # frequency_penalty=0.35 (구버전보다 낮음 — 3.5는 반복 경향이 덜함)
            # max_tokens=1500: 3.5는 추론 능력이 낮아 더 길게 써야 도달하는 경향
            messages = [{"role": "user", "content": curr_prompt}]
            _, text = LM(client, messages, args.gpt_version, max_tokens=1500, frequency_penalty=0.35)

        else:
            # ── GPT-4: system message 2개 + user message 구조 (1단계와 가장 큰 차이점)
            #
            # [System Message 1 - 상세 역할 + 추론 규칙 명시]
            # "스킬 기반 할당": 필요 스킬 집합 ⊆ 로봇(팀) 스킬 집합 인지 검증
            # "질량 기반 할당": 로봇(팀) mass_capacity ≥ 객체 mass 인지 검증
            # "다중 후보 시": 최선의 선택을 reasoning으로 결정
            # → 이 규칙들이 코드가 아닌 자연어 추론(Chain-of-Thought)을 통해 강제된다.
            #
            # [System Message 2 - 역할 재강조]
            # "You are a Robot Task Allocation Expert"를 한 번 더 반복하는 이유:
            # GPT-4가 첫 번째 system message의 긴 내용 처리 후 역할 페르소나를 유지하도록 보강
            #
            # max_tokens=400: 추론 결과는 짧은 주석 형태이므로 충분
            # frequency_penalty=0.69: 2단계에서 가장 높은 값 — 반복 추론 패턴 강력 억제
            messages = [
                {"role": "system", "content": "You are a Robot Task Allocation Expert. Determine whether the subtasks must be performed sequentially or in parallel, or a combination of both based on your reasoning. In the case of Task Allocation based on Robot Skills alone - First check if robot teams are required. Then Ensure that robot skills or robot team skills match the required skills for the subtask when allocating. Make sure that condition is met. In the case of Task Allocation based on Mass alone - First check if robot teams are required. Then Ensure that robot mass capacity or robot team combined mass capacity is greater than or equal to the mass for the object when allocating. Make sure that condition is met. In both the Task Task Allocation based on Mass alone and Task Allocation based on Skill alone, if there are multiple options for allocation, pick the best available option by reasoning to the best of your ability."},
                {"role": "system", "content": "You are a Robot Task Allocation Expert"},
                {"role": "user",   "content": curr_prompt}
            ]
            _, text = LM(client, messages, args.gpt_version, max_tokens=400, frequency_penalty=0.69)

        # LLM이 생성한 추론 텍스트를 수집
        # 이 text는 3단계(Code Generation) 프롬프트에 그대로 이어붙여진다.
        # 즉, "왜 이 로봇 조합인가"의 근거가 3단계 코드 생성의 컨텍스트가 된다.
        # 수집 전에 깨진 스킬명(공백/대소문자/잘림/환각)을 정상 14종으로 교정한다.
        text = normalize_skills(text)
        allocated_plan.append(text)

    print ("Generating Allocated Code...")

    # ============================================================
    # [3단계] Task Allocation - CODE Solution (코드화된 작업 할당)
    # 목표: 2단계의 자연어 추론 결과를 실제 실행 가능한 Python 코드로 변환한다.
    #       핵심 변환은 두 가지다:
    #         변환 1: 함수 시그니처에 robot_list 인자 추가
    #                 def slice_potato()  →  def slice_potato(robot_list)
    #         변환 2: 모든 스킬 호출 첫 번째 인자에 로봇 삽입 + 실제 robot 인덱스로 호출
    #                 GoToObject('Knife') →  GoToObject(robot_list[0], 'Knife')
    #                 slice_potato()      →  slice_potato([robots[0], robots[2]])
    #
    # 입력: decomposed_plan[i] (1단계 코드) + allocated_plan[i] (2단계 추론 텍스트)
    # 출력: code_plan (list[str]) — robot 인자를 포함한 최종 실행 Python 코드
    # ============================================================

    ######## Train Task Allocation - CODE Solution ########

    # ── [3-A] 3단계 공유 프롬프트 헤더 구성 ──
    # 1·2단계와 동일한 스킬/모듈 선언으로 시작.
    # 차이점: objects_ai를 헤더에 포함한다.
    # (2단계는 루프 내에서 curr_prompt에 추가했지만, 3단계는 공유 프롬프트에 고정 포함)
    prompt = f"from skills import " + actions.ai2thor_actions
    prompt += f"\nimport time"
    prompt += f"\nimport threading"
    prompt += objects_ai   # ← 2단계와 달리 공유 프롬프트에 포함 (루프 밖)

    # ── [3-B] Few-shot 4개 예시 로드 ──
    # train_task_allocation_code.py에는 4가지 코드 변환 패턴 예시가 있다:
    #   EXAMPLE 1: 단일 로봇 (robot_list[0] 인덱스 방식) → wash_fork([robots[1]])
    #   EXAMPLE 2: 단일 로봇 (robot_list 전체 방식)      → put_tomato_in_fridge([robots[0]])
    #   EXAMPLE 3: Coalition 팀, 역할 분리               → slice_potato([robots[0], robots[2]])
    #              robot_list[0]은 SliceObject, robot_list[1]은 GoToObject/PickupObject 담당
    #   EXAMPLE 4: 순차 서브태스크, 서브태스크별 다른 팀 → pick_up_fork([robots[0],robots[1]])
    #                                                        throw_fork_in_trash([robots[0],robots[2]])
    # 주의: EX1(robot_list[0])과 EX2(robot_list)의 인자 방식이 달라 LLM이 혼용할 수 있다.
    code_plan = []
    prompt_file1 = os.getcwd() + "/data/pythonic_plans/" + args.prompt_allocation_set + "_code.py"
    code_prompt_file = open(prompt_file1, "r")
    code_prompt = code_prompt_file.read()
    code_prompt_file.close()

    # 공유 프롬프트 = 헤더(스킬+객체) + 4개 Few-shot 예시
    prompt += "\n\n" + code_prompt + "\n\n"

    # ── [3-C] 태스크별 LLM 호출 및 최종 코드 생성 ──
    # zip(decomposed_plan, allocated_plan): 1단계·2단계 출력을 인덱스 동기화하여 순회
    # code_plan: list[str] — 각 인덱스가 로봇 인자 포함 Python 코드 문자열
    for i, (plan, solution) in enumerate(zip(decomposed_plan, allocated_plan)):

        # ── [3-C-i] 1단계 출력 이어붙임 (robot 없는 분해 코드) ──
        # 3단계 LLM은 이 코드를 보고 함수 구조를 파악한 뒤 robot 인자를 삽입한다.
        curr_prompt = prompt + plan   # Few-shot + 1단계 코드(로봇 없음)

        # ── [3-C-ii] 로봇 스펙 재주입 ──
        # 2단계와 동일하게 실제 로봇 딕셔너리를 Python 리터럴로 삽입.
        # LLM이 robots[0], robots[1], robots[2] 인덱스와 로봇 이름을 매핑하는 데 사용된다.
        curr_prompt += f"\n# TASK ALLOCATION"
        curr_prompt += f"\n\nrobots = {available_robots[i]}"

        # ── [3-C-iii] 2단계 추론 결과(자연어) 이어붙임 ──
        # 이것이 3단계의 핵심 입력이다: "왜 robot1+robot3인가"의 추론 근거가
        # robots = [...] 바로 뒤에 위치하여, LLM이 올바른 인덱스를 선택하는 context가 된다.
        # 예: "# The 'Slice the Potato' subtask is assigned to team of Robots 1 and 3."
        #   → LLM은 이 문장을 보고 [robots[0], robots[2]] 로 호출하는 코드를 생성한다.
        curr_prompt += solution

        # ── [3-C-iv] 응답 시작 마커 삽입 ──
        # "# CODE Solution" 태그가 Few-shot 예시의 응답 시작 형식과 일치해야
        # LLM이 이 지점 이후에 Python 코드를 생성한다.
        # 2단계의 "# SOLUTION" 태그와 대응되는 3단계 전용 마커다.
        curr_prompt += f"\n# CODE Solution  \n"

        # ── [3-D] 모델별 LLM 호출 ──
        if "gpt" not in args.gpt_version:
            # ── 구버전 GPT: frequency_penalty=0.30
            # 1단계(0.15), 2단계(0.65) 사이의 중간값.
            # 코드에는 어느 정도 반복이 허용되지만(robot_list 반복 참조),
            # 너무 낮으면 같은 액션 패턴이 반복될 위험이 있다.
            _, text = LM(client, curr_prompt, args.gpt_version, max_tokens=1000, stop=["def"], frequency_penalty=0.30)
        else:
            # ── GPT-4/3.5: system message 1개 (2단계의 2개보다 단순)
            # system message가 1개인 이유:
            #   - "왜 이 로봇을 선택했는가"의 추론은 이미 allocated_plan에 담겨 있다.
            #   - 3단계는 추론이 아닌 코드 번역만 하면 되므로 역할 선언 1개로 충분하다.
            # max_tokens=1400: 3단계가 전 단계 중 가장 큼.
            #   - 함수 정의 + 내부 액션 × n개 + threading 배선 코드까지 포함해야 하기 때문
            # frequency_penalty=0.4:
            #   - 2단계(0.69)보다 낮음 — robot_list[0]이 여러 번 등장하는 것이 올바른 코드이므로
            #     과도한 반복 억제는 오히려 코드를 망친다.
            messages = [
                {"role": "system", "content": "You are a Robot Task Allocation Expert"},
                {"role": "user",   "content": curr_prompt}
            ]
            _, text = LM(client, messages, args.gpt_version, max_tokens=1400, frequency_penalty=0.4)

        # 생성된 코드를 수집.
        # 이 text가 execute_plan.py에서 aithor_connect.py와 합쳐져 최종 executable_plan.py가 된다.
        code_plan.append(text)

    # save generated plan
    exec_folders = []
    if args.log_results:
        line = {}
        now = datetime.now() # current date and time
        date_time = now.strftime("%m-%d-%Y-%H-%M-%S")

        for idx, task in enumerate(test_tasks):
            task_name = "{fxn}".format(fxn = '_'.join(task.split(' ')))
            task_name = task_name.replace('\n','')
            folder_name = f"{task_name}_plans_{date_time}"
            exec_folders.append(folder_name)

            os.mkdir("./logs/"+folder_name)

            with open(f"./logs/{folder_name}/log.txt", 'w') as f:
                f.write(task)
                f.write(f"\n\nGPT Version: {args.gpt_version}")
                f.write(f"\n\nFloor Plan: {args.floor_plan}")
                f.write(f"\n{objects_ai}")
                f.write(f"\nrobots = {available_robots[idx]}")
                f.write(f"\nground_truth = {gt_test_tasks[idx]}")
                f.write(f"\ntrans = {trans_cnt_tasks[idx]}")
                f.write(f"\nmax_trans = {max_trans_cnt_tasks[idx]}")

            # ── 스킬 검증: 배정 로봇이 필요 스킬을 보유하는지 확인 (경고만, 차단 X) ──
            skill_warnings = validate_skills(decomposed_plan[idx], available_robots[idx])
            if skill_warnings:
                print(f"\n[스킬 검증] {task}")
                for w in skill_warnings:
                    print("  " + w)
                with open(f"./logs/{folder_name}/log.txt", 'a') as f:
                    f.write("\n\n# ===== Skill Validation Warnings =====\n")
                    f.write("\n".join(skill_warnings))

            with open(f"./logs/{folder_name}/decomposed_plan.py", 'w') as d:
                d.write(decomposed_plan[idx])

            with open(f"./logs/{folder_name}/allocated_plan.py", 'w') as a:
                a.write(allocated_plan[idx])

            with open(f"./logs/{folder_name}/code_plan.py", 'w') as x:
                x.write(code_plan[idx])
