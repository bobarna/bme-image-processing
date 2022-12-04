#!/bin/bash

# Run YOLO object detection
python3 yolov7-number-plates/detect.py --weights yolov7-number-plates/yolov7-number-plates-trained.pt --img-size 448 --source images --name number-plates-yolo --save-txt --save-conf --nosave --project images --exist-ok
# Cut out detection
## move detected `*.txt` labels into folder `images/labels`
mv images/number-plates-yolo/labels images/labels
python3 cutout.py images
#  Results are now in the `images/cutouts` folder
# Run OCR on detections
python3 paddleOCR/main.py
# `output.csv` contains the results (in the root folder)
