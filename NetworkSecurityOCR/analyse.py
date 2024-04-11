from paddleocr import PaddleOCR, draw_ocr
from getWebPic import getWebpic

# Paddleocr目前支持的多语言语种可以通过修改lang参数进行切换
# 例如`ch`, `en`, `fr`, `german`, `korean`, `japan`
detection_model_path = 'F:\Code\\ai_model\\ch_PP-OCRv4_det_server_infer'
ocr = PaddleOCR(use_angle_cls="true", lang="en",
                det_model_dir=detection_model_path)  # need to run only once to download and load model into memory


def analysePic(img_path):
    result = ocr.ocr(img_path, cls=True)
    res = result[0]
    if res is None:
        print("图片识别失败")
        return None
    print(res)
    t_res = res[0][1][0]
    print("识别结果：" + t_res)
    return t_res


if __name__ == '__main__':
    m_img_path = getWebpic()
    analysePic(m_img_path)
