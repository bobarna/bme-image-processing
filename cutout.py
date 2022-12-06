'''
cutout.py inference

Cuts out all the labels contained in images/labels/*.txt from the
corresponding images/*.jpg files.

images/
|   |- image1.jpg
|   |- image2.jpg
|   ...
|   |_ imageN.jpg
|
|- labels/
    |- image1.txt
    |- image2.txt
    ...
    |_ imageN.txt

Results are written to inference/found-classes/*_0.jpg.
All found classes are written as different images *_0, *_1, etc.
E.g.:
images
|- image*.jpg
|- labels/
|_ found-classes
    |- image1_0.jpg
    |- image1_1.jpg
    |- image2_0.jpg
    ...
    |_ imageN_0.jpg
'''

from pathlib import Path
import sys
import cv2

inference_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('inference')

if not inference_dir.exists() or not inference_dir.is_dir():
    sys.exit("Inference dir {} does not exist or is not\
             a directory".format(inference_dir))

images_dir = inference_dir
if not images_dir.exists() or not images_dir.is_dir():
    sys.exit("Images dir {} does not exist or is not\
             a directory".format(images_dir))

labels_dir = inference_dir / "labels"
if not labels_dir.exists() or not labels_dir.is_dir():
    sys.exit("Labels dir {} does not exist or is not\
             a directory".format(labels_dir))

# Output dir
cutout_dir = Path(inference_dir / "cutouts")
# Create it, if necessary
cutout_dir.mkdir(parents=True, exist_ok=True)

# Loop through all images in images_dir
for img_path in images_dir.glob('*.jpg'):
    print("Processing {}".format(img_path))
    # Find corresponding label
    label_file_glob = list(labels_dir.glob("{}.txt".format(img_path.stem)))
    print("file glob")
    if len(label_file_glob) < 1:
        continue
    # Assume that there is at most 1 corresponding .txt file
    label_file_name = list(label_file_glob)[0]
    label_file = open(label_file_name, 'r')
    # Read each detected object in the label file
    print("reading in object detections")
    objects = []
    for l in label_file:
        # Each line has the format:
        # obj_id x_min y_min x_max y_max
        o = l.split()
        objects.append([
            int(o[1]), # x_min
            int(o[2]), # y_min
            int(o[3]), # x_max
            int(o[4])  # y_max
        ])
    label_file.close()

    # Load the original image
    print("loading the original image")
    img = cv2.imread(str(img_path))
    # Cut-out each detected object
    for i, o in enumerate(objects):
        x = (o[0], o[2])
        y = (o[1], o[3])
        crop_img = img[y[0]:y[1], x[0]:x[1]]

        # Optionally show each cut-out image
        # cv2.imshow('{}_{}'.format(img_path, o), crop_img)
        # cv2.waitKey(0)

        # Write out current cropped image
        crop_img_path = cutout_dir / "{}_{}.jpg".format(img_path.stem, i)
        cv2.imwrite(str(crop_img_path), crop_img)



