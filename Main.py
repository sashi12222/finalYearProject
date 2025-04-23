from tkinter import messagebox
from tkinter import *
from tkinter import simpledialog
import tkinter
import matplotlib.pyplot as plt
from tkinter import ttk
from tkinter import filedialog
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
import pickle
import os
import numpy as np
import torch
import cv2
import os
import socket
import pickle
import pathlib
from pathlib import Path
pathlib.PosixPath = pathlib.WindowsPath

main = Tk()
main.title("Remote Sensing Image Analysis using Deep Learning")
main.geometry("1300x1200")

global filename, model
CONFIDENCE_THRESHOLD = 0.3
GREEN = (0, 255, 0)

#fucntion to upload dataset
def uploadDataset():
    global X, Y, boundings
    text.delete('1.0', END)
    filename = filedialog.askdirectory(initialdir=".") #upload dataset file
    text.insert(END,filename+" loaded\n\n")
    
def preprocess():
    text.delete('1.0', END)
    text.insert(END,"Dataset Processing Completed")

def runYolo():
    global  model
    text.delete('1.0', END)
    model = torch.hub.load('yolov5', 'custom', path='model/best.pt', force_reload=True,source='local')
    text.insert(END,"Yolo Remote Sensing Object Detection Model Loaded")

def predict():
    global model
    filename = filedialog.askopenfilename(initialdir="testImages") #upload dataset file
    img = cv2.imread(filename)
    img = cv2.resize(img, (512, 512))
    results = model(img)
    results.xyxy[0]  # im predictions (tensor)
    out = results.pandas().xyxy[0]  # im predictions (pandas)
    print(out)
    if len(out) > 0:
        for i in range(len(out)):
            xmin = int(out['xmin'].ravel()[i])
            ymin = int(out['ymin'].ravel()[i])
            xmax = int(out['xmax'].ravel()[i])
            ymax = int(out['ymax'].ravel()[i])
            name = out['name'].ravel()[i]
            confidence = float(out['confidence'].ravel()[i])
            if confidence > 0.80:
                cv2.rectangle(img, (xmin, ymin), (xmax, ymax), (255, 0, 0), 2)
                cv2.putText(img, name, (xmin, ymin-20), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 255, 0), 2)
    cv2.imshow("Original Image", img)
    cv2.waitKey(0)    

def graph():
    grp = cv2.imread('model/results.png')
    grp = cv2.resize(grp, (800, 600))
    cv2.imshow("Yolo Performance Graph", grp)
    cv2.waitKey(0)

font = ('times', 16, 'bold')
title = Label(main, text='Remote Sensing Image Analysis using Deep Learning')
title.config(bg='gold2', fg='thistle1')  
title.config(font=font)           
title.config(height=3, width=120)       
title.place(x=0,y=5)

font1 = ('times', 13, 'bold')
ff = ('times', 12, 'bold')

uploadButton = Button(main, text="Upload Remote Sensing Dataset", command=uploadDataset)
uploadButton.place(x=20,y=550)
uploadButton.config(font=ff)


processButton = Button(main, text="Preprocess Dataset", command=preprocess)
processButton.place(x=300,y=550)
processButton.config(font=ff)

cnnButton = Button(main, text="Generate & Load Yolo Model", command=runYolo)
cnnButton.place(x=510,y=550)
cnnButton.config(font=ff)

graphButton = Button(main, text="Object Detection from Test Image", command=predict)
graphButton.place(x=850,y=550)
graphButton.config(font=ff)

predictButton = Button(main, text="Yolo Performance Graph", command=graph)
predictButton.place(x=20,y=600)
predictButton.config(font=ff)

font1 = ('times', 12, 'bold')
text=Text(main,height=22,width=150)
scroll=Scrollbar(text)
text.configure(yscrollcommand=scroll.set)
text.place(x=10,y=100)
text.config(font=font1)

main.config(bg='DarkSlateGray1')
main.mainloop()
