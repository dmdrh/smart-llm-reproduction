import math
import re
import shutil
import subprocess
import time
import threading
import cv2
import numpy as np
from ai2thor.controller import Controller
from scipy.spatial import distance
from typing import Tuple
from collections import deque
import random
import os
from glob import glob

def closest_node(node, nodes, no_robot, clost_node_location):
    crps = []
    distances = distance.cdist([node], nodes)[0]
    dist_indices = np.argsort(np.array(distances))
    for i in range(no_robot):
        # 재시도 카운터(clost_node_location)가 누적되면 인덱스가 dist_indices 길이를
        # 초과할 수 있다. 마지막 유효 인덱스(len-1)로 clamp하여 IndexError를 방지한다.
        idx = (i * 5) + clost_node_location[i]
        idx = min(idx, len(dist_indices) - 1)
        pos_index = dist_indices[idx]
        crps.append (nodes[pos_index])
    return crps

def distance_pts(p1: Tuple[float, float, float], p2: Tuple[float, float, float]):
    return ((p1[0] - p2[0]) ** 2 + (p1[2] - p2[2]) ** 2) ** 0.5

def generate_video():
    frame_rate = 5
    # input_path, prefix, char_id=0, image_synthesis=['normal'], frame_rate=5
    # 이미지 전용 출력 폴더(output_images) 안만 훑는다. task_log_path는
    # execute_plan.py가 주입. 없으면 안전한 전용 하위 폴더로 폴백.
    try:
        base_path = task_log_path
    except NameError:
        base_path = os.getcwd()
    output_img_path = os.path.join(base_path, "output_images")
    cur_path = os.path.join(output_img_path, "*", "")
    for imgs_folder in glob(cur_path, recursive = False):
        view = os.path.basename(os.path.normpath(imgs_folder))
        if not os.path.isdir(imgs_folder):
            print("The input path: {} you specified does not exist.".format(imgs_folder))
        else:
            command_set = ['ffmpeg', '-i',
                                '{}/img_%05d.png'.format(imgs_folder),
                                '-framerate', str(frame_rate),
                                '-pix_fmt', 'yuv420p',
                                '{}/video_{}.mp4'.format(output_img_path, view)]
            subprocess.call(command_set)
        


