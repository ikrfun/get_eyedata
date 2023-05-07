import cv2
import numpy as np
from . import binarize

def cog(binary_img):
    '''
    Center of Gravity
    重心を座標として出力する
    '''
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

def top(binary_image_now,binaru_image_1farame_ago):
    '''
    進行方向の一番先頭にあるピクセルの座標
    '''
    pass


import argparse
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='get_eye_xy')
    parser.add_argument('-f', '--file', type=str, help='image file path',required=True)
    args = parser.parse_args()
    
    image = cv2.imread(args.file)
    binary_image = binarize.binarize_image(image)
    x,y = cog(binary_image)
    print(x,y)