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
current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
url = "https://passport.kanxue.com/user-mobile-1.htm"


def sliding_code():
    for i in range(6):
        # 通过getSlicePic下载图片，传入ddddocr，获得res数组位置，然后移动鼠标.
        GECKODRIVER_PATH = r'./geckodriver.exe'
        browser = webdriver.Firefox(executable_path=GECKODRIVER_PATH)
        browser.get(url)
        bg_pic_path, sl_pic_path = getSlicePic(browser)

        distance1 = generate_distance(bg_pic_path, sl_pic_path) - 30
        distance2 = generate_distance_by_matchTemplate(bg_pic_path, sl_pic_path)
        distance = distance1
        if distance1 <= 0:
            distance = distance2
        # print(distance)
        move_mouse(distance, browser)
    return 0

# 移动鼠标
def move_mouse(position, browser: webdriver):
    # 创建 ActionChains 对象
    actions = ActionChains(browser)

    # 在元素上执行点击并按住不放的操作
    # /html/body/div[2]/div[1]/div/div[2]/div/div[1]/form/div[2]/div/div/div[2]/div[2]
    element = browser.find_element(By.XPATH, "/html/body/div[2]/div[1]/div/div[2]/div/div[1]/form/div[2]/div/div/div[2]/div[2]")
    actions.click_and_hold(element).perform()
    speed = 10
    # 计算步长
    step = int(position / speed)

    # 分解移动操作，并控制速度
    for i in range(1, abs(position), step):
        if position > 0:
            actions.move_by_offset(step, 0).perform()
        else:
            actions.move_by_offset(-step, 0).perform()
        actions.pause(0.1).perform()  # 设置动作持续时间

    # 最后的微调，确保移动到指定位置
    actions.move_by_offset(position % step, 0).perform()
    # 移动鼠标到指定的偏移位置，设置持续时间
    # actions.move_to_element_with_offset(element, position, 0).perform()
    actions.pause(1).perform()  # 设置动作持续时间
    # 释放鼠标
    actions.release().perform()
    return 1


# 通过url 获得有缺口的图片和滑块图片
def getSlicePic(browser: webdriver):
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

    with open(sl_image_name, "wb") as slider_file:
        slider_file.write(slider_image)

    return bg_image_name, sl_image_name


def generate_distance(bg_image_name, sl_image_name):
    # bg_image_name = "./imgs/bg_img_20240411_135439.jpg"
    # sl_image_name = "./imgs/sl_img_20240411_135439.jpg"
    with open(bg_image_name, 'rb') as f:
        bg_image = f.read()
    with open(sl_image_name, 'rb') as f:
        target_bytes = f.read()

    slide = ddddocr.DdddOcr(det=False, ocr=False, show_ad=False)
    result = slide.slide_match(target_bytes, bg_image, simple_target=True)
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


if __name__ == "__main__":
    sliding_code()
    # generate_distance("0", "0")
    # generate_distance_by_matchTemplate("./imgs/bg_img_20240411_134909.jpg", "./imgs/sl_img_20240411_134909.jpg")
