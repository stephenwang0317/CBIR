
import tkinter as tk
from tkinter import END, filedialog
from PIL import Image, ImageTk

from DataBase import DataBase
from Search import Search
from Property import * 

default_seaImg="193003.jpg"
default_dataset="data/myData"
default_method=1

class MainWindow:
    def __init__(self,mw) -> None:
        self.mainWindow=mw
        self.mainWindow.title("CBIR System")
        self.mainWindow.geometry("800x500")
        self.seaImg=None
        self.resImgs=[]

    def createUI(self):
        openFileButton=tk.Button(self.mainWindow,text="Select File",command=lambda: selectFile())
        openFileButton.grid(row=0, column=0, padx=5, pady=5)
        dataPathButton=tk.Button(self.mainWindow,text="Select DatasetPath",command=lambda: selectDataSetPath())
        dataPathButton.grid(row=0, column=1, padx=5, pady=5)
        searchButton=tk.Button(self.mainWindow,text="Start to Search",command=lambda: search())
        searchButton.grid(row=0, column=2, padx=5, pady=5)

        methodInt = tk.IntVar()
        methodInt.set(default_method)
        methodLabel=tk.Label(self.mainWindow,text="Search Method:")
        methodLabel.grid(row=1, column=0, padx=5, pady=5)

        for i,name in enumerate(methodNames):
            tk.Radiobutton(self.mainWindow,text=name,value=i+1,variable=methodInt).grid(row=1, column=i+1, padx=5, pady=5)


        seaImgPathLabel=tk.Label(self.mainWindow,text="Image Path:")
        seaImgPathLabel.grid(row=2, column=0, padx=5, pady=5)
        dataSetPathLabel=tk.Label(self.mainWindow,text="Dataset Path:")
        dataSetPathLabel.grid(row=3, column=0, padx=5, pady=5)
        seaImgPathEntry=tk.Entry(self.mainWindow)
        seaImgPathEntry.grid(row=2, column=1, padx=5, pady=5)
        seaImgPathEntry.insert( 0,  default_seaImg)
        dataSetPathEntry=tk.Entry(self.mainWindow)
        dataSetPathEntry.grid(row=3, column=1, padx=5, pady=5)
        dataSetPathEntry.insert( 0,  default_dataset)


        def selectFile():
            path = filedialog.askopenfilename()
            seaImgPathEntry.delete(0, END)
            seaImgPathEntry.insert(0, path)
            openImg=Image.open(path)
            self.seaImg = ImageTk.PhotoImage(openImg)
            tk.Label(self.mainWindow, text="Search Picture:").grid(row=4, column=0, padx=5, pady=5)
            tk.Label(self.mainWindow, image = self.seaImg).grid(row=4, column=1, padx=5, pady=5)
                        
        def selectDataSetPath():
            path = filedialog.askdirectory()
            dataSetPathEntry.delete(0, END)
            dataSetPathEntry.insert(0, path)

        def search():
            self.resImgs.clear()
            imgPath=seaImgPathEntry.get()
            dataPath=dataSetPathEntry.get()
            csvPath=DataBase(methodInt.get()).getDatasetCsv(dataPath)
            resPaths=Search(methodInt.get()).searchImgMostCloestPath(imgPath,csvPath)
            tk.Label(self.mainWindow, text="Result Picture:").grid(row=5, column=0, padx=5, pady=5)
            for i,resPath in enumerate(resPaths):
                openImg=Image.open(resPath)
                self.resImgs.append(ImageTk.PhotoImage(openImg))
                tk.Label(self.mainWindow, image = self.resImgs[i]).grid(row=int(5+i/5), column=int(1+i%5))   
