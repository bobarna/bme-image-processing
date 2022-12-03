# License Plate OCR
A license plate recognition application impleneted in python.
The project is based heavily on the tutorial and it's source code from [https://deepayan137.github.io/blog/markdown/2020/08/29/building-ocr.html](https://deepayan137.github.io/blog/markdown/2020/08/29/building-ocr.html)

## Setup
Navigate to root directory!
Install requirements from _requirements.txt_!
`pip install -r requirements.txt
`
## Train
`python train.py --path .\ --name licensePlateOCR --imgdir data\train --log_dir logs --save_dir saves
`
## Test trained model
`python test.py --path .\ --name licensePlateOCR --imgdir .\data\test
`
## Run character recognition
`python ocr.py --path .\ --name licensePlateOCR --imgdir .\data\cutouts
`

