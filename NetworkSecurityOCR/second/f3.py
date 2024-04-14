# 第二次攻击的 chrom 主体代码
import io
import time
from datetime import datetime
import cv2
import requests
from PIL import Image
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By

# 获取当前时间并格式化为字符串

url = "https://passport.kanxue.com/user-mobile-1.htm"


def sliding_code():
    GECKODRIVER_PATH = r'./geckodriver.exe'
    for i in range(1):
        # 通过getSlicePic下载图片，传入ddddocr，获得res数组位置，然后移动鼠标.
        browser = webdriver.Firefox(executable_path=GECKODRIVER_PATH)
        browser.maximize_window()
        browser.get(url)
        time.sleep(5)
        bg_image_element = browser.find_element(By.XPATH,
                                                "/html/body/div[2]/div[1]/div/div[2]/div/div[1]/form/div[2]/div/div/div[1]/div/div[1]/img[1]")
        slider_image_element = browser.find_element(By.XPATH,
                                                    "/html/body/div[2]/div[1]/div/div[2]/div/div[1]/form/div["
                                                    "2]/div/div/div[1]/div/div[1]/img[2]")
        bg_pic_path, sl_pic_path = getSlicePic(bg_image_element, slider_image_element)
        actions = ActionChains(browser)
        element = browser.find_element(By.XPATH,
                                       "/html/body/div[2]/div[1]/div/div[2]/div/div[1]/form/div[2]/div/div/div[2]/div[2]")
        # 将鼠标移动到元素上
        actions.move_to_element(element).perform()
        bg_image_size = bg_image_element.size
        # 使用 Selenium 的 get_attribute 方法获取元素的宽度属性
        bg_image_width = bg_image_element.get_attribute("width")
        # 使用 int() 函数将宽度转换为整数
        bg_image_width = int(bg_image_width)
        print(f"网页背景图片大小高度为: {bg_image_size['height']}, 宽度为:{bg_image_size['width']}")
        print(f"网页背景图片宽度为:{bg_image_width}")
        # distance = preManage_pic(bg_pic_path, sl_pic_path)
        #
        # # move_mouse(distance, browser)
        # move_mouse_new(distance, browser)
        time.sleep(2)
        browser.close()
    return 0


def move_mouse_new(position, browser: webdriver):
    # 创建 ActionChains 对象
    actions = ActionChains(browser)

    # 在元素上执行点击并按住不放的操作
    # /html/body/div[2]/div[1]/div/div[2]/div/div[1]/form/div[2]/div/div/div[2]/div[2]
    element = browser.find_element(By.XPATH,
                                   "/html/body/div[2]/div[1]/div/div[2]/div/div[1]/form/div[2]/div/div/div[2]/div[2]")
    tracks = get_tracks(distance=position)
    actions.click_and_hold(element).perform()
    for track in tracks['forward_tracks']:
        actions.move_by_offset(xoffset=track, yoffset=0).perform()
    time.sleep(0.5)
    for back_tracks in tracks['back_tracks']:
        actions.move_by_offset(xoffset=back_tracks, yoffset=0).perform()

    time.sleep(0.5)
    # 释放鼠标
    actions.release().perform()
    return 1


# 通过url 获得有缺口的图片和滑块图片
def getSlicePic(bg_image_element, slider_image_element):
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    # 背景图片xpath
    # /html/body/div[2]/div[1]/div/div[2]/div/div[1]/form/div[2]/div/div/div[1]/div/div[1]/img[1]

    # 滑块xpath
    # /html/body/div[2]/div[1]/div/div[2]/div/div[1]/form/div[2]/div/div/div[1]/div/div[1]/img[2]

    # /html/body/div[2]/div[1]/div/div[2]/div/div[1]/form/div[2]/div/div/div[1]/div/div[1]/img[1]



    # 获取背景图片和滑块图片的URL
    bg_image_url = bg_image_element.get_attribute("src")
    slider_image_url = slider_image_element.get_attribute("src")



    # 下载背景图片和滑块图片
    bg_image = requests.get(bg_image_url).content
    slider_image = requests.get(slider_image_url).content
    width = height = 0
    with Image.open(io.BytesIO(bg_image)) as img:
        width, height = img.size
    # 构造文件名
    bg_image_name = f"./imgs/bg_img_{current_time}.jpg"
    sl_image_name = f"./imgs/sl_img_{current_time}.jpg"
    # 保存图片到本地
    with open(bg_image_name, "wb") as bg_file:
        bg_file.write(bg_image)
        bg_file.flush()  # 刷新到磁盘

    with open(sl_image_name, "wb") as slider_file:
        slider_file.write(slider_image)
        slider_file.flush()  # 刷新到磁盘

    print(f"真实背景图片高度为: {height}, 宽度为: {width}")
    return bg_image_name, sl_image_name


def preManage_pic(bg_name, slider_name):
    # 读取背景图和滑块图
    bg_image = cv2.imread(bg_name)
    slider_image = cv2.imread(slider_name)

    # 将图片转换为灰度图
    gray_bg = cv2.cvtColor(bg_image, cv2.COLOR_BGR2GRAY)
    gray_slider = cv2.cvtColor(slider_image, cv2.COLOR_BGR2GRAY)

    # 使用Canny边缘检测算法
    edges_bg = cv2.Canny(gray_bg, 100, 200)
    edges_slider = cv2.Canny(gray_slider, 100, 200)

    bg_pic = cv2.cvtColor(edges_bg, cv2.COLOR_GRAY2RGB)
    tp_pic = cv2.cvtColor(edges_slider, cv2.COLOR_GRAY2RGB)

    res = cv2.matchTemplate(bg_pic, tp_pic, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)  # 寻找最优匹配

    X = max_loc[0]
    print("原始缺口的X轴坐标,", X)
    th, tw = tp_pic.shape[:2]
    tl = max_loc  # 左上角点的坐标
    br = (tl[0] + tw, tl[1] + th)  # 右下角点的坐标
    cv2.rectangle(bg_image, tl, br, (0, 0, 255), 2)  # 绘制矩形

    out_name = "./imgs " + "out" + str(X) + bg_name.split('/')[2]

    cv2.imwrite(out_name, bg_image)

    return X


def get_tracks(distance):
    v = 0
    t = 0.2
    forward_tracks = []
    current = 0
    mid = distance * 4 / 5  # 减速阀值
    while current < distance:
        if current < mid:
            a = 2  # 加速度为+2
        else:
            a = -3  # 加速度-3
        v0 = v
        v = v0 + a * t
        s = v0 * t + 0.5 * a * (t ** 2)
        current += s
        forward_tracks.append(round(s))
    return forward_tracks


if __name__ == "__main__":
    sliding_code()
