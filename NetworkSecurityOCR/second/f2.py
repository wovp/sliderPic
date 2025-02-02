# 第二次攻击的 chrom 主体代码
import time
from datetime import datetime
import cv2
import ddddocr
import requests
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By

# 获取当前时间并格式化为字符串

url = "https://passport.kanxue.com/user-mobile-1.htm"


def sliding_code():
    for i in range(1):
        # 通过getSlicePic下载图片，传入ddddocr，获得res数组位置，然后移动鼠标.
        GECKODRIVER_PATH = r'./geckodriver.exe'
        browser = webdriver.Firefox(executable_path=GECKODRIVER_PATH)
        browser.maximize_window()
        browser.get(url)
        bg_pic_path, sl_pic_path = getSlicePic(browser)
        distance = preManage_pic(bg_pic_path, sl_pic_path)
        # 第二次修正轨迹
        move_mouse_new(mode_x_mouse(distance), browser)
        time.sleep(2)
        browser.close()
    return 0

# 第二次修正轨迹，通过多次实验，划分区间映射
def mode_x_mouse(X):
    print(f"修正前{X}")

    # 0 - 50
    if X < 50:
        X = X + 15
    # 50 - 100
    elif X < 100:
        X = X + 23
    # 100 - 125
    elif X < 125:
        X = X + 25
    # 125 - 140
    elif X < 140:
        X = X + 30
    # 140 - 150
    elif X < 150:
        X = X + 32
    # 150 - 175
    elif X < 175:
        X = X + 33
    # 175 - 200
    elif X < 200:
        X = X + 35
    # 200 - 225
    elif X < 225:
        X = X + 35
    # 225 - 250
    elif X < 250:
        X = X + 35
    # 250 - 275
    elif X < 275:
        X = X + 35
    # 275 - 290
    elif X < 290:
        X = X + 35
    # 290 - 300
    elif X <= 300:
        X = X + 35
    # 300 - 325
    elif X <= 325:
        X = X + 35
    # 325 - 340
    elif X <= 340:
        X = X + 35
    # 340 - 350
    elif X < 350:
        X = X + 35
    # 350 - 375
    elif X < 375:
        X = X + 35
    # 375 - 400
    elif X < 400:
        X = X + 35
    else:
        X = X + 35
    return X


# 旧的移动鼠标
def move_mouse(position, browser: webdriver):
    # 创建 ActionChains 对象
    actions = ActionChains(browser)

    # 在元素上执行点击并按住不放的操作
    # /html/body/div[2]/div[1]/div/div[2]/div/div[1]/form/div[2]/div/div/div[2]/div[2]
    element = browser.find_element(By.XPATH,
                                   "/html/body/div[2]/div[1]/div/div[2]/div/div[1]/form/div[2]/div/div/div[2]/div[2]")

    # 实时获得坐标信息
    slider_image_element = browser.find_element(By.XPATH,
                                                "/html/body/div[2]/div[1]/div/div[2]/div/div[1]/form/div["
                                                "2]/div/div/div[1]/div/div[1]/img[2]")
    actions.click_and_hold(element).perform()
    actions.move_by_offset(position, 0)
    # 这个是鼠标慢移动
    while 1:
        style = slider_image_element.get_attribute('style')
        left_index = style.find('left:')
        left_value = 0
        if left_index != -1:
            left_value_start = left_index + len("left:")  # left属性值的起始索引
            left_value_end = style.find("px", left_value_start)  # left属性值的结束索引
            left_value = style[left_value_start:left_value_end].strip()  # 提取left属性值
            print("left属性值:", left_value)
        else:
            print("未找到left属性值")
        left_value = float(left_value)
        if abs(left_value - position) < 1:
            break
        if left_value > position:
            actions.move_by_offset(-1, 0).perform()
            actions.pause(0.1).perform()  # 设置动作持续时间
        elif left_value < position:
            actions.move_by_offset(1, 0).perform()
            actions.pause(0.1).perform()  # 设置动作持续时间
    """
    首先，我们明确偏移量没问题
    就是在鼠标的偏移量出现了问题
    因为图片的像素是480长度
    但是在浏览器中是520长度
    你在480偏移的距离，要转换为520长度的距离
    """
    actions.pause(2).perform()  # 设置动作持续时间
    # 释放鼠标
    actions.release().perform()
    return 1


# 新的移动鼠标
def move_mouse_new(position, browser: webdriver):
    # 创建 ActionChains 对象
    actions = ActionChains(browser)

    # 在元素上执行点击并按住不放的操作
    # /html/body/div[2]/div[1]/div/div[2]/div/div[1]/form/div[2]/div/div/div[2]/div[2]
    element = browser.find_element(By.XPATH,
                                   "/html/body/div[2]/div[1]/div/div[2]/div/div[1]/form/div[2]/div/div/div[2]/div[2]")
    tracks = get_tracks(distance=position)
    actions.click_and_hold(element).perform()
    for track in tracks:
        actions.move_by_offset(xoffset=track, yoffset=0).perform()
        time.sleep(0.0001)

    time.sleep(0.5)
    # 释放鼠标
    actions.release().perform()
    return 1


# 通过url 获得有缺口的图片和滑块图片
def getSlicePic(browser: webdriver):
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    # 背景图片xpath
    # /html/body/div[2]/div[1]/div/div[2]/div/div[1]/form/div[2]/div/div/div[1]/div/div[1]/img[1]

    # 滑块xpath
    # /html/body/div[2]/div[1]/div/div[2]/div/div[1]/form/div[2]/div/div/div[1]/div/div[1]/img[2]

    # /html/body/div[2]/div[1]/div/div[2]/div/div[1]/form/div[2]/div/div/div[1]/div/div[1]/img[1]

    # 找到背景图片和滑块图片的元素
    # 等待5秒钟
    time.sleep(5)
    bg_image_element = browser.find_element(By.XPATH,
                                            "/html/body/div[2]/div[1]/div/div[2]/div/div[1]/form/div[2]/div/div/div[1]/div/div[1]/img[1]")
    slider_image_element = browser.find_element(By.XPATH,
                                                "/html/body/div[2]/div[1]/div/div[2]/div/div[1]/form/div["
                                                "2]/div/div/div[1]/div/div[1]/img[2]")

    # 获取背景图片和滑块图片的URL
    bg_image_url = bg_image_element.get_attribute("src")
    slider_image_url = slider_image_element.get_attribute("src")

    # 下载背景图片和滑块图片
    bg_image = requests.get(bg_image_url).content
    slider_image = requests.get(slider_image_url).content

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

    return bg_image_name, sl_image_name


def generate_distance(bg_image_name, sl_image_name):
    # bg_image_name = "./imgs/bg_img_20240411_135439.jpg"
    # sl_image_name = "./imgs/sl_img_20240411_135439.jpg"
    with open(bg_image_name, 'rb') as f:
        bg_image = f.read()
    with open(sl_image_name, 'rb') as f:
        target_bytes = f.read()

    slide = ddddocr.DdddOcr(det=False, ocr=False, show_ad=False)
    result = slide.slide_match(target_bytes, bg_image)
    print(result)
    return result['target'][0]


def generate_distance_by_matchTemplate(bg_name, slider_name):
    # 读取背景图和滑块图
    bg_image = cv2.imread(bg_name)
    slider_image = cv2.imread(slider_name)

    # 将图片转换为灰度图
    gray_bg = cv2.cvtColor(bg_image, cv2.COLOR_BGR2GRAY)
    gray_slider = cv2.cvtColor(slider_image, cv2.COLOR_BGR2GRAY)

    # 使用模板匹配查找滑块在背景图中的位置
    result = cv2.matchTemplate(gray_bg, gray_slider, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    # 计算滑块需要移动的距离
    distance = max_loc[0] - slider_image.shape[1] // 2

    print("滑块需要移动的距离：", distance)
    return distance


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

    # 第一次修正轨迹
    X = mode_X_new(X)

    # 下面是验证缺口的位置
    th, tw = tp_pic.shape[:2]
    tl = max_loc  # 左上角点的坐标
    br = (tl[0] + tw, tl[1] + th)  # 右下角点的坐标
    cv2.rectangle(bg_image, tl, br, (0, 0, 255), 2)  # 绘制矩形

    out_name = "./imgs " + "out" + str(X) + bg_name.split('/')[2]

    cv2.imwrite(out_name, bg_image)

    return X

# 模拟轨迹
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


def mode_X(X: float):
    if X < 50:
        X = X * 1.08 - 15
    # 50 - 100
    elif X < 100:
        X = X * 1.08 - 15
    # 100 - 125
    elif X < 125:
        X = X * 1.08 - 35
    # 125 - 140
    elif X < 140:
        X = X * 1.08 - 47
    # 140 - 150
    elif X < 150:
        X = X * 1.08 - 53
    # 150 - 175
    elif X < 175:
        X = X * 1.08 - 58
    # 175 - 200
    elif X < 200:
        X = X * 1.08 - 60
    # 200 - 225
    elif X < 225:
        X = X * 1.08 - 64
    # 225 - 250
    elif X < 250:
        X = X * 1.08 - 66
    # 250 - 275
    elif X < 275:
        X = X * 1.08 - 75
    # 275 - 290
    elif X < 290:
        X = X * 1.08 - 80
    # 290 - 300
    elif X <= 300:
        X = X * 1.08 - 79
    # 300 - 325
    elif X <= 325:
        X = X * 1.08 - 86
    # 325 - 340
    elif X <= 340:
        X = X * 1.08 - 90
    # 340 - 350
    elif X < 350:
        X = X * 1.08 - 97
    # 350 - 375
    elif X < 375:
        X = X * 1.08 - 100
    # 375 - 400
    elif X < 400:
        X = X * 1.08 - 102
    else:
        X = X * 1.08 - 120
    return X

# 第一次修正轨迹，通过缩放的方式
def mode_X_new(X: float):
    X = (X - 20) / 480 * 412.5
    return X


if __name__ == "__main__":
    sliding_code()
