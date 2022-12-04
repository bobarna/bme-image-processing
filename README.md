![Pipeline Teaser](/docs/project-summary/figures/pipeline2_cut.png "")
# Automatic Number Plate Recognition
Group homework for the 7th semester class Image Processing at the Budapest
University of Technology and Economics.

- [project-summary.pdf](https://bobarna.github.io/bme-image-processing/project-summary.pdf)o

## Usage
- Put images in the `images` folder.
- Run YOLO object detection
    - `python detect.py --weights yolov7-number-plates/yolov7-number-plates-trained.pt --img-size 448 --source images --name number-plates-yolo --save-txt --save-conf --nosave --project inference --exist-ok` 
- Cut out detections
    - move detected `*.txt` labels into folder `images/labels`
        - `mv images/inference/recognition/labels images/labels`
    - `python cutout.py images`
    - Results are now in the `images/found-classes` folder
- Run OCR on detections
    - `python paddleOCR/main.py`
- `output.csv` contains the results (in the root folder)

## Individual Components
- License Plate Object Detection: [https://github.com/bobarna/yolov7-number-plates](https://github.com/bobarna/yolov7-number-plates)
- OCR: we implemented 2 different methods, and ended up using paddleOCR
    - paddleOCR: `paddleOCR` folder
    - custom OCR: `LicencePlateOCR` folder

## Building the Documents Locally with LaTeX
See `docs` folder.
