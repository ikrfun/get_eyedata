import os
from tqdm import tqdm
from moviepy.editor import VideoFileClip, concatenate_videoclips

def crop_video(video_path: str, save_dir: str):
    # ファイル名と拡張子を取得
    file_name, extension = os.path.splitext(os.path.basename(video_path))

    # 上下に分割した動画の保存パスを作成
    top_save_path = os.path.join(save_dir, f'{file_name}_top{extension}')
    bottom_save_path = os.path.join(save_dir, f'{file_name}_bottom{extension}')

    # VideoFileClipを使用して元の動画を読み込み
    video_clip = VideoFileClip(video_path)

    # 動画を上下に分割してトリミング
    top_clip = video_clip.crop(y1=0, y2=video_clip.h // 2)
    bottom_clip = video_clip.crop(y1=video_clip.h // 2, y2=video_clip.h)

    # 分割した動画を保存
    top_clip.write_videofile(top_save_path, codec="libx264")
    bottom_clip.write_videofile(bottom_save_path, codec="libx264")

    # リソースを解放
    video_clip.close()

import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--video_path', '-f', type=str, required=True)
    parser.add_argument('--save_dir', '-s', type=str, default='data/video')
    args = parser.parse_args()
    crop_video(args.video_path, args.save_dir)
