from frame_utils import  get_corrd, save, sep, binarize
import os 
import cv2
from tqdm import tqdm
import numpy as np
import pandas as pd

CAM_HEIGHT = 1440

def check(file_path:str):
    if os.path.exists(file_path):
        return True
    else:
        print('FileNotFoundError')
        return False

def get_eye_coord(video_path:str):
    #動画の読み込み
    mov_file = os.path.normpath(video_path)
    cap = cv2.VideoCapture(mov_file)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    #中心座標を格納するリスト
    frame_ids = []
    eye_x = []
    eye_y = []
    image = []
    #メインループスタート
    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    for frame_id in tqdm(range(0,total_frames)):
        #フレームを取得
        ret, frame = cap.read()
        if ret:
            #get binarized iamge 
            real,eye = sep.sep_y(frame,corrd = CAM_HEIGHT)
            bin_image = binarize.binarize_image(frame)
            #get center of biggest object
            x,y = get_corrd.cog(bin_image.astype(np.uint8))
            eye_x.append(x)
            eye_y.append(y)
            frame_ids.append(frame_id)
            image_path = save.image(real,'frame'+str(frame_id))
            image.append(image_path)
        else:
            print(f'error occurd at frame{frame_id}')
            break
    
    cap.release()
    df = pd.DataFrame({'frame_ids':frame_ids,'x':eye_x,'y':eye_y,'image':image})
    save.csv(df,'eye_dataset')
    return df