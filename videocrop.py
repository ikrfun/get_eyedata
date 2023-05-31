import cv2
from frame_utils import sep
import os 
from tqdm import tqdm

def crop_video(video_path:str, save_dir:str):
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    #拡張子より前の名前を取得
    input_name = video_path.split(os.sep)[-1].split('.')[0]

    #output_name = file_name + botom/top + .mp4
    top_save_path = os.path.join(save_dir,f'{input_name}_top.mp4')
    bottom_save_path = os.path.join(save_dir,f'{input_name}_bottom.mp4')

    #save_pathがなかったら作る
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')

    top_out = cv2.VideoWriter(top_save_path, fourcc, fps, (width, height//2))
    bottom_out = cv2.VideoWriter(bottom_save_path, fourcc, fps, (width, height//2))

    for frame_id in tqdm(range(frame_count)):
        ret, frame = cap.read()
        try:
            top,bottom = sep.sep_y(frame)
            top_out.write(top)
            bottom_out.write(bottom)
        except:
            print(f'frame_id:{frame_id} is error')
            continue
    cap.release()
    top_out.release()
    bottom_out.release()

import argparse
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--video_path','-f', type=str, required=True)
    parser.add_argument('--save_dir','-s', type=str, default='data/video')
    args = parser.parse_args()
    crop_video(args.video_path, args.save_dir)