# GestureRecognition
This repository is contains solution for gesture recognition, outputing the number of raised fingers to the screen using OpenCV library.

## How to use
Create a conda enviroment
```
conda create --name gest_rec python
```
Activate your enviroment
```
conda activate gest_rec
```
Install the neccesery dependecies
``` python
pip3 install requirements.txt
```
To estimate the number of raised fingers, run
```
python3 gesture_recognition.py
```
If you want to see the thresholded image use, run (--thresh is 0 by default)
```
python3 gesture_recognition.py --thresh 1
```
