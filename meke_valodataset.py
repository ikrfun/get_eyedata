from frame_utils import  get_corrd, save, sep, binarize
from valorant_urils import game_info
import os 
import cv2
from tqdm import tqdm
import numpy as np
import pandas as pd

def check(file_path:str):
    if os.path.exists(file_path):
        return True
    else:
        print('FileNotFoundError')
        return False

def make_dataset(video_path:str) -> list:
    #動画の読み込み
    mov_file = os.path.normpath(video_path)
    cap = cv2.VideoCapture(mov_file)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
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
            game,eye = sep.sep_y(frame)
            bin_image = binarize.binarize_image(eye)
            #get center of biggest object
            x,y = get_corrd.cog(bin_image.astype(np.uint8))
            roi = game_info.roi(x,y)
            eye_x.append(x)
            eye_y.append(y)
            rois.append(roi)
            frame_ids.append(frame_id)
            image_path = save.image(game,'frame'+str(frame_id))
            images.append(image_path)
        else:
            print(f'error occurd at frame{frame_id}')
            break   
    cap.release()
    df = pd.DataFrame({'frame_ids':frame_ids,'x':eye_x,'y':eye_y,'roi':rois,'images':images})

    


import argparse
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='welcome to Aeye-Tracler')
    parser.add_argument('-f', '--file', type=str, help='video file path',required=True)
    args = parser.parse_args()
    if check(args.file):

        make_dataset(args.file)
