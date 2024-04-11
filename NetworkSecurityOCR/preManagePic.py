import cv2
import numpy as np


def m_pre_pic(img_path):
    yzm = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)


    # 二值化
    thresh, yzm = cv2.threshold(yzm, 160, 255, cv2.THRESH_BINARY)
    # yzm:表示需要操作的数组
    # 160:表示阈值
    # 255 表示最大值

    cv2.imwrite('new_img.png', yzm)


if __name__ == '__main__':
    m_pre_pic("captcha_1711104387.png")