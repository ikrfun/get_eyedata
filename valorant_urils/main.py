import valo_60
import argparse
import os 

if __name__ == "__main__":
    # ArgumentParserオブジェクトを作成
    parser = argparse.ArgumentParser(description='welcome to Aeye-Tracler')
    # 引数を定義
    parser.add_argument('-f', '--file', type=str, help='video file path',required=True)
    parser.add_argument('-o', '--output', type=str, help='output file path',default='output')
    parser.add_argument('-t', '--type', type=str, help='Type of file to save (csv or json)', choices=['csv', 'json'])
    # 引数をパース
    args = parser.parse_args()
    frame_maker = valo_60.FrameMaker(os.path.normpath(args.file),os.path.normpath('coords/coord_data.json'))
    frame_maker.get_frames()
    frame_maker.save_csv(args.output)
