import cv2
import os 

BASE_DIR = os.path.normpath('data')

def image(image, save_name, save_dir=None):
    if save_dir is None:
        save_dir = 'images'

    # dataディレクトリがない場合は作成する
    os.makedirs(BASE_DIR, exist_ok=True)

    # 保存先のディレクトリがない場合は作成する
    os.makedirs(os.path.join(BASE_DIR, save_dir), exist_ok=True)

    save_path = os.path.join(BASE_DIR, save_dir, save_name + '.jpg')

    cv2.imwrite(save_path, image, [cv2.IMWRITE_JPEG_QUALITY, 100])
    return save_path



def csv(df,save_name):
    save_dir = BASE_DIR
    os.makedirs(save_dir, exist_ok=True)

    save_path = os.path.join(save_dir, save_name + '.csv')
    df.to_csv(save_path, index=False)