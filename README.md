# GestureRecognition
This repository contains solution for gesture recognition, outputing the number of raised fingers to the screen using OpenCV library.

## How to use
Create a conda environment
```
conda create --name gest_rec python
```
Activate your environment
```
conda activate gest_rec
```
Install the necessary dependecies
``` python
pip3 install requirements.txt
```
To estimate the number of raised fingers, run
```
python3 gesture_recognition.py
```
or
```
python3 gesture_recognition.py --thresh 0
```

![img_1](/images/img_1.png)

If you want to see image threshold, run
```
python3 gesture_recognition.py --thresh 1
```
![img_3](/images/img_3.png)

While runnig the program you can press ```r``` to refresh the backgound image. This should be used if you have changed your location during the code's execution or if there is too mush noise in the thresholded image.

To stop the program press ```q```.

## Limitaions
This method should be used in a room with good lightning. Dim lighting and having bracelets can lead to incorrect results. The angle between two fingers shouldn't be greater than 80° or othrewise the results will be incorrect as shown in the image.

![img_4](/images/img_4.png)
