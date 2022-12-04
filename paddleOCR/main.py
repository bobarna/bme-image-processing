import os
import csv
from pathlib import Path

from src.clear_photo import *
from tqdm import tqdm

from PIL import Image
from paddleocr import PaddleOCR, draw_ocr
# Paddleocr supports Chinese, English, French, German, Korean and Japanese.
# You can set the parameter `lang` as `ch`, `en`, `fr`, `german`, `korean`, `japan`
# to switch the language model in order.


ocr = PaddleOCR(use_angle_cls=True, lang='en', use_gpu=False, det=False) # need to run only once to download and load model into memory


def preprocess(img_dir_path, cleared_path):
    print('Preprocessing cutouts before OCR:')
    dir_list = os.listdir(img_dir_path)
    for file in tqdm(dir_list):
        img = cv2.imread(img_dir_path + file, cv2.IMREAD_COLOR)
        img2 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img_cleared = clear(img)
        cv2.imwrite(str(cleared_path / file), img_cleared)


def main():
    img_dir_path = './images/cutouts/'
    cleared_path = Path('./images/cleared/')
    # Create it cleared path, if necessary
    cleared_path.mkdir(parents=True, exist_ok=True)

    preprocess(img_dir_path, cleared_path)

    with open(file='output.csv', mode='w', newline='') as output:
        writer = csv.writer(output, delimiter=';')
        for image_name in os.listdir(cleared_path):
            result = ocr.ocr(str(cleared_path / image_name))
            txts = [line[1][0] for line in result[0]]
            scores = [line[1][1] for line in result[0]]
            original_img_name = image_name.split('_')[1:-1]
            row = [str(''.join(original_img_name) + '.jpg')]
            processed_txts = ['']   # Adding empty string to filter out empty predictions
            for txt in txts:        # Multiple predictions are available
                txt = txts[0]
                txt = txt.replace('.', '-')     # Account for incorrectly recognised delimiter character
                txt = txt.replace('_', '-')
                delimiter = txt.find('-')
                txt_len = len(txt)
                if txt_len > 7:           # If too many characters were recognised
                    a = 0
                    if delimiter > 3:
                        txt = txt[delimiter - 3: txt_len:]
                    txt_len = len(txt)
                    delimiter = txt.find('-')
                    if txt_len - delimiter - 1 > 3:
                        txt = txt[0: - txt_len - (txt_len - delimiter)]
                if txt not in processed_txts:     # Not allowing duplicate predictions
                    processed_txts.extend(txt)
                    row.extend([txt])
            writer.writerow(row)


if __name__ == '__main__':
    main()
