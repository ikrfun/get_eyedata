'''
video_editの仕様

def cut(video_file_path,use_frames=[(start,end),...]):
    動画を指定したフレームでカットして、保存する
    複数の箇所の指定が可能
    保存するファイル名は、f{video_name}_trim.mp4
    複数指定された場合は、f{video_name}_trim1.mp4, f{video_name}_trim2.mp4, ...
    
    return: None
    
    
def video_split(video_file_path,use_frames=[(start,end),...]):
    動画を指定したフレームで分割して、画像データとして保存する
    use_frames
    保存するフォルダは、f{video_name}_split1, f{video_name}_split2, ...
    保存するファイル名は、frame1.jpg, frame2.jpg, ...
    
    return:None

'''

from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import os
from moviepy.editor import VideoFileClip
import shutil

def cut(video_file_path, use_frames):
    video_name = os.path.splitext(os.path.basename(video_file_path))[0]
    directory = os.path.dirname(video_file_path)
    
    for i, (start, end) in enumerate(use_frames):
        output_file = os.path.join(directory, f"{video_name}_trim{i + 1}.mp4")
        ffmpeg_extract_subclip(video_file_path, start, end, targetname=output_file)
        

def video_split(video_file_path, use_frames):
    video_name = os.path.splitext(os.path.basename(video_file_path))[0]
    directory = os.path.dirname(video_file_path)
    video = VideoFileClip(video_file_path)
    
    for i, (start, end) in enumerate(use_frames):
        output_dir = os.path.join(directory, f"{video_name}_split{i + 1}")
        os.makedirs(output_dir, exist_ok=True)

        for j, frame in enumerate(range(start, end + 1)):
            frame_image = video.get_frame(frame / video.fps)
            frame_image.save_frame(os.path.join(output_dir, f"frame{j + 1}.jpg"))
            
    video.close()
