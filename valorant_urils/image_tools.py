import cv2
import numpy as np
'''
便利ツール群
バイナリイメージ関係
'''
#1と0で表現されたバイナリイメージに書き換える関数
def binarize_image(image, plot = True):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    binary_array = np.where(binary == 0, 0, 1)
    
    if plot:
        plt.imshow(binary_array, cmap='gray')
        plt.show()
    return binary_array

#バイナリimageから最も１が多いマスを取得する
def find_most_ones(image, grid_size,plot = False):
    h, w = image.shape
    grid_h, grid_w = h // grid_size, w // grid_size
    grids = np.zeros((grid_h, grid_w))

    for i in range(grid_h):
        for j in range(grid_w):
            grid = image[i*grid_size:(i+1)*grid_size, j*grid_size:(j+1)*grid_size]
            grids[i][j] = np.sum(grid)

    max_i, max_j = np.unravel_index(np.argmax(grids), grids.shape)
    image = np.zeros((h, w))
    image[max_i*grid_size:(max_i+1)*grid_size, max_j*grid_size:(max_j+1)*grid_size] = 1
    
    if plot:
        plt.imshow(image, cmap='gray')
        plt.show()
    return (max_i, max_j)

def np2int(frame):
    frame.looking_grid = tuple(int(x) for x in frame.grid_60)
    return frame

def sep(frame):
    
    '''
    frameを回しているfor文の中での利用を前提とする
    '''
    # 動画を上下で半分に分割
    top_half = frame[:2160 // 2, :]
    bottom_half = frame[2160 // 2:, :]

    return top_half,bottom_half

