# Automatic Number Plate Recognition
Group homework for the 7th semester class Image Processing at the Budapest
University of Technology and Economics.

- [project_summary.pdf](https://bobarna.github.io/bme-image-processing/project_summary.pdf)
- [proposal.pdf](https://bobarna.github.io/bme-image-processing/proposal.pdf)

## Licence Plate Object Detection
See: [https://github.com/bobarna/yolov7-number-plates](https://github.com/bobarna/yolov7-number-plates)

## Building the Proposal Locally
### Requirements
#### Ubuntu
```shell
sudo apt install texlive-full
# it's also enough to install only a subset of texlive-full (smaller in size):
sudo apt install texlive texlive-publishers texlive-science cm-super
```
#### Mac
``` shell
brew install texlive
# or 
brew install mactex
```

### Building proposal.pdf
``` shell
# Go to docs folder
cd docs
# Makefile commands tldr:
# Build docs/build/proposal.pdf + clean build files
make 
# Build docs/proposal.pdf without cleaning up
make proposal.pdf 
# Delete build files
make clean 
```
