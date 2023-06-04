from .frame_utils import cog, sep_y, binarize_image
import os 
import cv2
from tqdm import tqdm
import numpy as np
import pandas as pd
from dataclasses import dataclass


@dataclass
class Area:
    name:str
    top_x:int
    top_y:int
    bottom_x:int
    bottom_y:int

minimap = Area('minimap',15,40,435,460)
left_team = Area('left_team',440,0,870,100)
right_team = Area('right_team',1050,0,1480,100)
timer = Area('timer',870,0,1050,100)
kill_log = Area('kill_log',1490,60,1920,300)
hp = Area('hp',520,980,685,1080)
skill = Area('skill',745,980,1175,1080)
amo = Area('amo',1235,980,1400,1080)
center = ('center',960,540,125)

def get_roi(x, y):
    if ((x - center[1])**2 + (y - center[2])**2) <= center[3]**2:
        return center[0]
    elif left_team.top_x <= x <= left_team.bottom_x and left_team.top_y <= y <= left_team.bottom_y:
        return left_team.name
    elif right_team.top_x <= x <= right_team.bottom_x and right_team.top_y <= y <= right_team.bottom_y:
        return right_team.name
    elif timer.top_x <= x <= timer.bottom_x and timer.top_y <= y <= timer.bottom_y:
        return timer.name
    elif kill_log.top_x <= x <= kill_log.bottom_x and kill_log.top_y <= y <= kill_log.bottom_y:
        return kill_log.name
    elif hp.top_x <= x <= hp.bottom_x and hp.top_y <= y <= hp.bottom_y:
        return hp.name
    elif skill.top_x <= x <= skill.bottom_x and skill.top_y <= y <= skill.bottom_y:
        return skill.name
    elif amo.top_x <= x <= amo.bottom_x and amo.top_y <= y <= amo.bottom_y:
        return amo.name
    elif minimap.top_x <= x <= minimap.bottom_x and minimap.top_y <= y <= minimap.bottom_y:
        return minimap.name
    else:
        return 'other'

def check(file_path:str):
    if os.path.exists(file_path):
        return True
    else:
        print('FileNotFoundError')
        return False

def make_dataset(video_path:str):
    #動画の読み込み
    mov_file = os.path.normpath(video_path)
    check(mov_file)
    cap = cv2.VideoCapture(mov_file)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print(f'total_frames:{total_frames}')
    #中心座標を格納するリスト
    frame_ids = []
    eye_x = []
    eye_y = []
    rois = []
    images = []
    #メインループスタート
    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    for frame_id in tqdm(range(0,total_frames)):
        #フレームを取得
        ret, frame = cap.read()
        if ret:
            #get binarized iamge 
            if frame.shape[0] != 1080:
                game,eye = sep_y(frame)
            else:
                eye = frame
            bin_image = binarize_image(eye)
            #get center of biggest object
            x,y = cog(bin_image.astype(np.uint8))
            roi = get_roi(x,y)
            eye_x.append(x)
            eye_y.append(y)
            rois.append(roi)
            frame_ids.append(frame_id)
        else:
            print(f'error occurd at frame{frame_id}')
            break   
    cap.release()
    df = pd.DataFrame({'frame_ids':frame_ids,'x':eye_x,'y':eye_y,'roi':rois})
    return df

if __name__ == "__main__":
    df = make_dataset('test_bottom.mp4')
    print(df)