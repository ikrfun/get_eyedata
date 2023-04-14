import image_tools
import cv2
from tqdm import tqdm
import numpy as np
from dataclasses import dataclass, field
from collections import defaultdict
from dataclasses import dataclass, asdict, field
import json
from typing import List



@dataclass
class Frame:
    grid_60:tuple
    looking_at:str
    frame_id : int
    
class FrameMaker:
    def __init__(self,mov_path,coord_json):
        self.mov = cv2.VideoCapture(mov_path)
        self.frame_list = []
        self.json_path = coord_json
        
    def get_frames(self):
        self.mov.set(cv2.CAP_PROP_POS_FRAMES, 0)
        height = int(self.mov.get(cv2.CAP_PROP_FRAME_HEIGHT))
        frame_count = int(self.mov.get(cv2.CAP_PROP_FRAME_COUNT))
        for frame_id in tqdm(range(frame_count)):
            ret,frame = self.mov.read()
            if not ret:
                print(f'{frame_id}フレームでエラー')
                break
            if height == 2160:
                _,eye = image_tools.sep(frame)
            binary_eye = image_tools.binarize_image(eye,plot=False)
            coord = image_tools.find_most_ones(binary_eye,grid_size = 60, plot = False)
            looking_at = self.where_looking(coord)
            self.frame_list.append(Frame(coord,looking_at,frame_id))
        return self.frame_list
    
    def default_json(self,obj):
        if isinstance(obj, np.int64):
            return int(obj)
        raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")

    def save_json(self) -> None:
        frames_dict_list = [asdict(image_tools.np2int(frame)) for frame in self.frame_list]
        with open(self.frames_json_path, 'w') as f:
            json.dump(frames_dict_list, f, indent=4, default=self.default_json)
        print('save done')
        
    def save_csv(self,file_name:str) -> None:
        if not file_name.endswith('.csv'):
            file_name = file_name+'.csv'
        to_csv(self.frame_list,file_name)
        
        print(f'save as {file_name}')


    #どこを見ているかを文字列で返す
    def where_looking(self,coord):
        with open(self.json_path, 'r') as f:
            data = json.load(f)

        for feature, coordinates in data.items():
            if list(coord) in coordinates:
                return feature

        return None
    
import csv

def to_csv(frames: List[Frame], file_name: str):
    with open(file_name, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['x', 'y', 'looking_at', 'frame_id'])
        for frame in frames:
            x, y = frame.grid_60
            writer.writerow([x, y, frame.looking_at, frame.frame_id])