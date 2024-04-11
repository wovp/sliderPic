import math
import time

from PIL import Image
from selenium import webdriver

# from analyse import analysePic


def screan_pic(browser):
    browser.maximize_window()
    # 获取浏览器大小
    size_window = browser.get_window_size()
    time.sleep(1)
    # 获取截图
    browser.save_screenshot('login.png')
    login_img = Image.open('login.png')
    (login_width, login_height) = login_img.size
    print('截图的宽高：')
    print(login_width, login_height)
    # 计算浏览器与截图比例
    scale = size_window['width'] / login_width
    # 获取验证码
    code_loc = browser.find_element_by_xpath('//*[@id="img_valiCode"]').location
    code_size = browser.find_element_by_xpath('//*[@id="img_valiCode"]').size

    # 获取验证码位置
    # 此处的X和Y分别加了数字，因为前端的样式中，验证码标签img的margin-left为15，margin-top为5
    location_X = math.ceil(code_loc['x'] / scale) + 15
    location_Y = math.ceil(code_loc['y'] / scale) + 5
    location_height = math.ceil(code_size['height'] / scale)
    location_width = math.ceil(code_size['width'] / scale)

    code_img = login_img.crop((location_X, location_Y, location_X + location_width, location_Y + location_height))
    file_name = 'imgs/code_' + str(int(time.time())) + '.png'
    code_img.save(file_name)
    return file_name


def inpu_form():
    browser = webdriver.Firefox()
    browser.get('http://card.cqu.edu.cn/')
    user_inpu = browser.find_element_by_xpath('//*[@id="txt_sno"]')
    pass_inpu = browser.find_element_by_xpath('//*[@id="txt_pwd"]')
    verifyCode_inpu = browser.find_element_by_xpath('//*[@id="txtVal"]')
    user_inpu.send_keys("123456")
    pass_inpu.send_keys("654321")
    pic_ou = browser.find_element_by_xpath('//*[@id="img_valiCode"]')
    fi_name = screan_pic(browser)
    print("图片名：" + fi_name)
    # pic_code = analysePic(fi_name)
    # verifyCode_inpu.send_keys(pic_code)



if __name__ == '__main__':
    inpu_form()
