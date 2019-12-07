# Software Carpentry Final Project
# Face Averager

This repository contains the code necessary to find an 'average' face given a set of images with faces in them.

## Getting started

Download or clone this repository to your machine.

You will also need the following libraries installed: ```Flask```, ```dlib```, ```opencv```, ```glob```, and ```numpy```. These can be installed by opening terminal and entering:
```
$ pip3 install "library name"
```
You will now have two separate directories. One named ```local_imp``` and one named ```gui_imp```. They correspond to different implementations of the program.

We will begin with ```local_imp```.

### ```local_imp```

Within ```local_imp``` there is an ```imagesfp``` subdirectory. You can place the images here to average. However, it is not necessary, as running the program in your terminal will prompt you to enter a filepath containing images you'd like to average. 
To execute the program, enter the following into the terminal:
```
$ python3 averager.py
```
You will then be asked to input the filename containing the images you'd like to average. For example
```
Please enter the name of a folder containing images: imagesfp
```
The program will then execute.

#### ```local_imp``` output

If the files within the directory you specify are valid, then you will see the following output along with the average face displayed:
```
Opening imagesfp and checking for faces...
Processing images...
Finding facial landmarks...
Scaling images to common space...
Triangulating points...
Averaging faces...
Success!
```
If the files within the directory you specified are invalid, you will be notified, and the program will exit.

Now we discuss ```gui_imp```.

### ```gui_imp```

Within ```gui_imp``` you will find the same set of python scripts with one exception. ```gui_imp``` contains ```site.py```. ```site.py``` is a website gui implementation of the above program. To run it, open your terminal and enter:
```
$ python3 site.py
```
Now, open any browser and navigate to ```localhost:5000```
You should be redirected to a homepage with further instructions.

## Authors

* **Lincoln Kartchner**

## Acknowledgments

* Dlib
* OpenCV
* https://www.learnopencv.com/average-face-opencv-c-python-tutorial/
* Flask
