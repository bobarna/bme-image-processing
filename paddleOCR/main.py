import os
import csv

from PIL import Image
from paddleocr import PaddleOCR, draw_ocr
# Paddleocr supports Chinese, English, French, German, Korean and Japanese.
# You can set the parameter `lang` as `ch`, `en`, `fr`, `german`, `korean`, `japan`
# to switch the language model in order.


ocr = PaddleOCR(use_angle_cls=True, lang='en', use_gpu=False, det=False) # need to run only once to download and load model into memory


def main():
    img_dir_path = 'D:/PythonProjects/paddleOCR/data/cutouts/'

    with open(file='output.csv', mode='w', newline='') as output:
        writer = csv.writer(output, delimiter=';')
        for image_name in os.listdir(img_dir_path):
            result = ocr.ocr(img_dir_path + '/' + image_name)
            txts = [line[1][0] for line in result[0]]
            scores = [line[1][1] for line in result[0]]
            row = [image_name]
            for txt in txts:
                txt = txts[0]
                txt = txt.replace('.', '-')
                txt = txt.replace('_', '-')
                delimiter = txt.find('-')
                txt_len = len(txt)
                if (txt_len > 7):
                    a = 0
                    if delimiter > 3:
                        txt = txt[delimiter - 3: txt_len:]
                    txt_len = len(txt)
                    delimiter = txt.find('-')
                    if txt_len - delimiter - 1 > 3:
                        txt = txt[0: - txt_len - (txt_len - delimiter)]
                row.extend([txt])
            writer.writerow(row)


if __name__ == '__main__':
    main()
