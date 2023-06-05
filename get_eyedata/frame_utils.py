import cv2
import numpy as np

#1と0で表現されたバイナリイメージに書き換える関数
def binarize_image(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    binary_array = np.where(binary == 0, 0, 1)
    return binary_array

def cog(binary_img):
    '''
    Center of Gravity
    重心を座標として出力する（左下を0,0とする座標系）
    '''
    # ラベリング処理
    nlabels, labels, stats, center = cv2.connectedComponentsWithStats(binary_img)
    
    # 背景のオブジェクト情報の削除
    nlabels = nlabels - 1
    stats = np.delete(stats, 0, 0)
    center = np.delete(center, 0, 0)
    
    # 面積が最大のオブジェクトのラベル番号を取得
    try:
        max_index = np.argmax(stats[:, 4])
        center_x = int(center[max_index][0])
        center_y = binary_img.shape[0] - int(center[max_index][1])  # y座標を変更
    except ValueError:
        center_x = np.nan
        center_y = np.nan
    
    return center_x, center_y


def sep_y(image,corrd:int = None):
    '''
    frameを回しているfor文の中での利用を前提とする
    '''
    if corrd:
        # 動画を上下で半分に分割
        top_half = image[:corrd, :]
        bottom_half = image[corrd:, :]
    else:
        # 動画を上下で半分に分割
        top_half = image[:2160 // 2, :]
        bottom_half = image[2160 // 2:, :]
    
    return top_half,bottom_half
