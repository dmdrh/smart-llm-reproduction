import os
import re
from pathlib import Path
import subprocess
import argparse

def sanitize_plan(text):
    """
    LLM이 생성한 code_plan.py에서 마크다운/산문을 제거하고 순수 파이썬 코드만 남긴다.

    (A) 코드펜스 우선: ```python ... ``` (또는 ``` ... ```) 블록이 있으면
        그 안의 내용만 모아서 반환한다. 블록이 여러 개면 순서대로 이어붙인다.
    (B) 펜스가 없으면: 줄 단위로 필터링하여 마크다운 산문을 제거하고
        실제 파이썬 코드로 보이는 줄만 보존한다.

    안전 원칙: 확실히 코드인 줄(import/def/주석/들여쓰기/함수호출 등)은 절대 제거하지 않는다.
    애매하면 보존한다.
    """
    # ── (A) 코드펜스 추출 ──
    # ```python ... ``` 또는 ``` ... ``` 블록 내부만 캡처 (대소문자 무시, 여러 개 허용)
    fence_pattern = re.compile(r"```(?:python|py)?\s*\n(.*?)```", re.DOTALL | re.IGNORECASE)
    blocks = fence_pattern.findall(text)
    if blocks:
        # 추출된 블록들을 빈 줄 하나로 이어붙임
        return "\n\n".join(block.strip("\n") for block in blocks).strip() + "\n"

    # ── (B) 펜스가 없으면 줄 단위 필터링 ──
    kept_lines = []
    for line in text.split("\n"):
        stripped = line.strip()

        # 1) 빈 줄은 보존 (코드 구조/가독성 유지)
        if stripped == "":
            kept_lines.append(line)
            continue

        # 2) 들여쓰기된 줄은 코드 본문일 가능성이 매우 높음 → 무조건 보존
        #    (함수 내부 액션 호출, 블록 등. 산문은 보통 들여쓰기가 없음)
        if line[0] in (" ", "\t"):
            kept_lines.append(line)
            continue

        # 3) 마크다운 라인 제거 대상
        #    - 코드펜스 잔재: ```
        #    - 헤더: ## / ### 형태 (마크다운 헤더)
        #    - 불릿/설명: -, *, +, 숫자목록, "**" 강조
        #    - 표/인용: |, >
        if stripped.startswith("```"):
            continue
        if re.match(r"^#{2,}\s", stripped):          # "## ", "### " 등 마크다운 헤더
            continue
        if re.match(r"^[-*+]\s", stripped):           # "- ", "* ", "+ " 불릿
            continue
        if re.match(r"^\d+\.\s", stripped):           # "1. " 번호 목록
            continue
        if stripped.startswith("**"):                 # "**Robot Selection**" 강조
            continue
        if stripped.startswith(("|", ">")):           # 표/인용
            continue

        # 4) 확실한 파이썬 코드 줄은 보존
        #    - 주석(#): 위 ## 헤더는 이미 걸러졌으므로 "# 1: ..." 같은 코드 주석만 남음
        #    - import / from / def / class / 제어문
        #    - 함수 호출 패턴: name(...) 으로 시작하는 줄
        #    - 대입문 (=) 포함
        if stripped.startswith("#"):
            kept_lines.append(line)
            continue
        if re.match(r"^(import|from|def|class|if|elif|else|for|while|try|except|finally|with|return|global|threading|time)\b", stripped):
            kept_lines.append(line)
            continue
        if re.match(r"^[A-Za-z_][\w\.]*\s*\(", stripped):   # 함수/메서드 호출
            kept_lines.append(line)
            continue
        if "=" in stripped and not stripped.startswith("="): # 대입문
            kept_lines.append(line)
            continue
        if stripped.endswith((")", ":", "]", "}", "\\")):    # 코드 연속/블록으로 보이는 줄
            kept_lines.append(line)
            continue

        # 5) 위 어디에도 안 걸리면 산문일 가능성 높음 → 제거
        #    (예: "Here is the solution:", "Robot1 will perform...")
        continue

    return "\n".join(kept_lines).strip() + "\n"

def append_trans_ctr(allocated_plan):
    brk_ctr = 0
    code_segs = allocated_plan.split("\n\n")
    fn_calls = []
    for cd in code_segs:
        if "def" not in cd and "threading.Thread" not in cd and "join" not in cd and cd[-1] == ")":
            # fn_calls.append(cd)
            brk_ctr += 1
    print ("No Breaks: ", brk_ctr)
    return brk_ctr

def compile_aithor_exec_file(expt_name):
    log_path = os.getcwd() + "/logs/" + expt_name
    executable_plan = ""
    
    # append the imports to the file
    import_file = Path(os.getcwd() + "/data/aithor_connect/imports_aux_fn.py").read_text()
    executable_plan += (import_file + "\n")
    
    # append the list of robots and floor plan number
    log_file = open(log_path + "/log.txt")
    log_data = log_file.readlines()
    # append the robot list
    executable_plan += (log_data[8] + "\n")
    # append the floor number
    flr_no = log_data[4][12:]
    gt = log_data[9]
    executable_plan += ("floor_no = " + flr_no + "\n\n")
    executable_plan += (gt)
    trans = log_data[10][8:]
    executable_plan += ("no_trans_gt = " + trans)
    max_trans = log_data[11][12:]
    executable_plan += ("max_trans = " + max_trans + "\n")
    
    # 이미지 출력 폴더 기준 경로를 실행 파일에 주입 (루트 오삭제 방지)
    executable_plan += (f'task_log_path = r"{log_path}"\n\n')

    # append the ai thoe connector and helper fns
    connector_file = Path(os.getcwd() + "/data/aithor_connect/aithor_connect.py").read_text()
    executable_plan += (connector_file + "\n")
    
    # append the allocated plan
    allocated_plan = Path(log_path + "/code_plan.py").read_text()
    allocated_plan = sanitize_plan(allocated_plan)
    brks = append_trans_ctr(allocated_plan)
    executable_plan += (allocated_plan + "\n")
    executable_plan += ("no_trans = " + str(brks) + "\n")

    # append the task thread termination
    terminate_plan = Path(os.getcwd() + "/data/aithor_connect/end_thread.py").read_text()
    executable_plan += (terminate_plan + "\n")

    with open(f"{log_path}/executable_plan.py", 'w') as d:
        d.write(executable_plan)
        
    return (f"{log_path}/executable_plan.py")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--command", type=str, required=True)
    args = parser.parse_args()

    expt_name = args.command
    print (expt_name)
    ai_exec_file = compile_aithor_exec_file(expt_name)

    subprocess.run(["python", ai_exec_file])