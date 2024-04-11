import requests
from PIL import Image
from io import BytesIO
import time


def getWebpic():
    # 获取当前时间戳
    current_time = str(int(time.time()))

    # 构造请求URL
    url = "http://card.cqu.edu.cn/Login/GetValidateCode?time=" + current_time
    print(current_time)
    # 发送请求
    response = requests.get(url)

    # 检查请求是否成功
    if response.status_code == 200:
        # 读取图像内容
        image = Image.open(BytesIO(response.content))

        # 构造文件名
        filename = "./imgs/captcha_" + current_time + ".png"

        # 保存图像到本地
        image.save(filename)
        print("验证码已保存为" + filename)
        return filename
    else:
        print("无法获取验证码")
    return None


# 通过url 获得有缺口的图片和滑块图片
def getSlicePic(url: str):
    pass


if __name__ == '__main__':
    getWebpic()
