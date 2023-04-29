import cv2
import os 
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd 
from tqdm import tqdm
from coords.get_roi import get_roi
import image_tools
 

def get_center(binary_img):
    #ラベリング処理
    nlabels, labels, stats, center = cv2.connectedComponentsWithStats(binary_img)
    #背景のオブジェクト情報の削除
    nlabels = nlabels - 1
    stats = np.delete(stats, 0, 0)
    center = np.delete(center, 0, 0)
    #面積が最大のオブジェクトのラベル番号を取得
    max_index = np.argmax(stats[:,4])
    center_x = int(center[max_index][0])
    center_y = int(center[max_index][1])

    return center_x, center_y


def get_eye_coord(video_path:str) -> list:
    #動画の読み込み
    mov_file = os.path.normpath(video_path)
    cap = cv2.VideoCapture(mov_file)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    #中心座標を格納するリスト
    frame_ids = []
    eye_x = []
    eye_y = []
    rois = []
    #メインループスタート
    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    for frame_id in tqdm(range(0,total_frames+1)):
        #フレームを取得
        ret, frame = cap.read()
        if ret:
            #get binarized iamge 
            _,eye = image_tools.sep(frame)
            bin_image = image_tools.binarize_image(frame,plot = False)
            #get center of biggest object
            x,y = get_center(bin_image.astype(np.uint8))
            roi = get_roi(x,y)
            eye_x.append(x)
            eye_y.append(y)
            rois.append(roi)
            frame_ids.append(frame_id)
        else:
            print(f'error occurd at frame{frame_id}')
            break   

    cap.release()

    return frame_ids, eye_x, eye_y, rois

def save_csv(frame_ids, eye_x, eye_y, rois):
    data = {
    'frame_ids': frame_ids,
    'x': eye_x,
    'y': eye_y,
    'roi': rois
    }
    # create a pandas DataFrame from the dictionary
    df = pd.DataFrame(data)
    # set the index to 'frame_ids' and select the desired columns
    df = df.set_index('frame_ids')[['x', 'y', 'roi']]
    return df

import argparse
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--video_path', type=str, default='figuzation/valo.mp4')
    parser.add_argument('--save_path', type=str, default='eye.csv')
    args = parser.parse_args()


    frame_ids, eye_x, eye_y, rois = get_eye_coord(args.video_path)
    df = save_csv(frame_ids, eye_x, eye_y, rois)
    df.to_csv(args.save_path)
    print('done')