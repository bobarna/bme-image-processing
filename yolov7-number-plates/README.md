# Transfer Learning for Number Plate Recognition
We trained a YOLOv7 model for number plate recognition. This folder contains the
end results of the learning. For more details, and reproducing the teaching, see
[https://github.com/bobarna/bme-image-processing](https://github.com/bobarna/bme-image-processing).

## Usage for cutting out all deteted number plates
1. Download some dataset of cars into the `number-plates-hun/images` folder.
    - [Mirror 1](https://barnabasborcsok.com/number-plates-hun.zip)
    - [Mirror 2](https://drive.google.com/file/d/1Hgds3pXZP2sX2EB0GeYWaFLiA96h4JlW/view?usp=share_link)
    - or get any other data source of some cars
2. Download yolov7 weights trained for number plate recognition:
    -  [yolov7-number-plates-trained.pt](https://github.com/bobarna/yolov7-number-plates/releases/download/Trained%2BData/yolov7-number-plates-trained.pt)
3. Run inference with trained yolov7 weights:
``
python detect.py --weights yolov7-number-plates-trained.pt --img-size 448 --source number-plates-hun/images --name number-plates-recognition --save-txt --save-conf --nosave --project inference --exist-ok
``
4. Move detected `*.txt` labels into folder `inference/labels`:
``mv number-plates-hun/number-plates/recognition/labels
number-plates-hun/labels``
5. Cut out all detected objects:
``python cutout.py number-plates-hun``
6. Results are in the `number-plates-hun/found-classes` folder.

## Running inference (detecting licence plates)
```
python detect.py --weights weights-number-plates.pt --img-size 448 --source number-plates-hun/ --name test-number-plates --save-txt --save-conf
```

- `--weights`: pretrained weights (result of the transfer learning)
- `--img-size`: size used for the inference
- `--source`: folder containing the images
- `--name`: name for this inference
- `--save-txt`: also saves the labels as `*.txt` files 
- `--save-conf`: also saves the confidence in the `*.txt` files

(`detect.py` could also take in single images instead of a whole directory.)

Each line of a detection (`image_name.txt`) takes the following form:

```
object_id x_min x_max y_min y_max confidence
```

- `object_id`: describes which object is detected (in our case, this is always
0 for the number plate class)
- `x_min`, `x_max`, `y_min`, `y_max`: describe the dimension of the bounding box
- `confidence`: 0..1 value for the confidence of the given detection.

(We modified `detect.py` to output detections in image-space, instead of the
original relative dimensions.)

## Run transfer learning (for reproducibility)
```
python3 train.py --workers 8 --device 0 --batch-size 8 --data data/number-plates.yaml --img 420 --cfg cfg/training/yolov7-number-plates.yaml --weights yolov7_training.pt --name yolov7-custom --hyp data/hyp.scratch.custom.yaml
```

# Forked from the official YOLOv7 implementation
For more details, see: 
- [original implementation](https://github.com/WongKinYiu/yolov7) 
- [paper](https://arxiv.org/abs/2207.02696)

