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

def sep_x(image,corrd:tuple = None):
    pass
def crop(image,corrd):
    pass
