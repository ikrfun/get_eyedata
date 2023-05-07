import cv2
import numpy as np


#1と0で表現されたバイナリイメージに書き換える関数
def binarize_image(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    binary_array = np.where(binary == 0, 0, 1)
    return binary_array

import argparse
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='get_binary_image')
    parser.add_argument('-f', '--file', type=str, help='image file path',required=True)
    args = parser.parse_args()
    binary_image = binarize_image(cv2.imread(args.file))
    print(binary_image)
