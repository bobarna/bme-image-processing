![Pipeline Teaser](/docs/project-summary/figures/pipeline2_cut.png "")
# Automatic Number Plate Recognition
Group homework for the 7th semester class Image Processing at the Budapest
University of Technology and Economics.

- [project-summary.pdf](https://bobarna.github.io/bme-image-processing/project-summary.pdf)

## Dependencies
Install [Python](https://www.python.org/) packages with
[pip](https://pip.pypa.io/en/stable/): 
```
pip install -r requirements.txt
```

## TLDR Usage
- Put images in the `images` folder.
- `./detect.sh`
- `output_original.csv` contains the results (in the root folder)
- `output.csv` contains the results of each cutout 
    - good for debugging purposes, and matching these against the detections in
        `images/cutouts/`

## Usage
- Put images in the `images` folder.
- Run YOLO object detection
    - `python yolov7-number-plates/detect.py --weights yolov7-number-plates/yolov7-number-plates-trained.pt --img-size 448 --source images --name number-plates-yolo --save-txt --save-conf --nosave --project images --exist-ok` 
- Cut out detections
    - move detected `*.txt` labels into folder `images/labels`
        - `mv images/number-plates-yolo/labels images/labels`
    - `python cutout.py images`
    - Results are now in the `images/cutouts` folder
- Run OCR on detections
    - `python paddleOCR/main.py`
- `output.csv` contains the results (in the root folder)
- Run `python fix_csv.py` to merge detections from the same image to the same
    line, with the original file names
- The final results are in `output_original.csv`

## Individual Components
- License Plate Object Detection: [https://github.com/bobarna/yolov7-number-plates](https://github.com/bobarna/yolov7-number-plates)
- OCR: we implemented 2 different methods, and ended up using paddleOCR
    - paddleOCR: `paddleOCR` folder
    - custom OCR: `LicensePlateOCR` folder

## Building the Documents Locally with LaTeX
See `docs` folder.
