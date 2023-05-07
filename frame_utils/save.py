import cv2
import os 

def image(image,save_name,save_dir = None, ):
    if save_dir == None:
        save_dir = 'images'
    #savedirがないときは作成する
    if save_dir:
        os.makedirs(save_dir, exist_ok=True)

    save_path = os.path.join(save_dir,save_name)

    cv2.imwrite(save_path, image)
    return save_path

def csv(df,save_name,save_dir = None):
    if save_dir == None:
        save_dir = os.mkdir('csvs')
    save_path = os.path.join(save_dir,save_name)
    df.to_csv(save_path)