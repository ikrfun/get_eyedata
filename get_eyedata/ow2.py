from .frame_utils import cog, sep_y, binarize_image, make_displayonly_video
import cv2
import numpy as np
import pandas as pd
from dataclasses import dataclass
from queue import Queue
from threading import Thread
from concurrent.futures import ProcessPoolExecutor, as_completed
from tqdm import tqdm
import os

@dataclass
class Area:
    name: str
    top_x: int
    top_y: int
    bottom_x: int
    bottom_y: int
    
areas = [
    Area('hp', 50, 50, 500, 250),
    Area('chat', 50, 330, 500, 500),
    Area('ult', 880, 50, 1040, 220),
    Area('my_status', 1450, 50, 1900, 280),
    Area('match_status', 650, 880, 1300, 1080),
    Area('kill_log', 1450, 880, 1920, 1080)
]

def get_roi(x, y):
    if ((x - 960)**2 + (y - 540)**2) <= 125**2:
        return 'center'
    else:
        for area in areas:
            if area.top_x <= x <= area.bottom_x and area.top_y <= y <= area.bottom_y:
                return area.name
    return 'other'

def check(file_path:str):
    if os.path.exists(file_path):
        return True
    else:
        print('FileNotFoundError')
        return False

#フレームの読み込みと画像処理の並列化
def frame_reader(cap, queue):
    while True:
        ret, frame = cap.read()
        if not ret:
            print('ret is False')
            break
        queue.put(frame)
    queue.put(None)  # signal that all frames have been read

def make_dataset(video_path:str, save:bool = True, get_display:bool = True):
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
    if save:
        # Get the base name of the video file and use it to create csv filename
        base_name = os.path.basename(video_path)
        file_name, _ = os.path.splitext(base_name)
        df.to_csv(f'{file_name}.csv',index=False)
    if get_display:
        make_displayonly_video(video_path)
    return df

def make_dataset_from_folder(folder_path:str, max_workers:int = 4, save:bool = True, get_display:bool = True):
    # Get a list of all video files in the folder
    video_files = [f for f in os.listdir(folder_path) if f.endswith('.mp4') or f.endswith('.mkv')]

    video_files = [os.path.join(folder_path, f) for f in video_files]

    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        # Create a list to hold the Future objects
        futures = [executor.submit(make_dataset, video_file, save, get_display) for video_file in video_files]

        # Use tqdm for progress bar
        for future in tqdm(as_completed(futures), total=len(futures)):
            # Results are ready only when processing is complete, so we don't need to do anything here
            pass
if __name__ == "__main__":
    df = make_dataset('F:\git-repo\get_eyedata\data\test.mkv')
    print(df)