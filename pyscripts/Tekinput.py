# Copyright 2020 by Chua Teck Lee.
# All rights reserved.

import tkinter as tk
from tkinter import *

from tkinter import ttk
from tkinter.ttk import *
from PIL import ImageTk,Image

import copy

import json
import Utility
import os
import pathlib
import math

########################VARIABLES###############################

class InputButton:
    def __init__(self, parent, imageFilename, thumbnailImage, inputCallback, x, y):
        self.imageFilename = imageFilename

        self.button = ttk.Button(
            parent,
            text = self.imageFilename,
            image = thumbnailImage,
            command = lambda: inputCallback(self.imageFilename),
            style = 'InputButton.TButton'
        )
        
        self.button.grid(
            row = y,
            column = x,
            padx = 3,
            pady = 10
        )

class MainWindow:
    savePath = r"images"

    inputBuffer = []
    inputButtons = []

    data = {}
    previewImages = {}
    originalImages = {}
    thumbnailImages = {}

    previewSize = 32
    padding = 16

    root = 0
    charSelect = 0
    gameSelect = 0
    comboCanvas = 0
    comboPreview = 0
    inputFrame = 0

    def __init__(self):
        #TK GUI
        self.root = Tk()
        self.root.title("Tekinput Generator")
        Utility.CentraliseWindow(self.root)

        #ttk style
        style = ttk.Style()

        #Various GUI Frames
        displayFrame = ttk.Frame(self.root)
        displayFrame.pack(pady = 10)

        self.inputFrame = ttk.LabelFrame(self.root, text = "Inputs", padding = 10)
        self.inputFrame.pack(pady = 10)

        selectFrame = ttk.Frame(self.root, padding = 10)
        selectFrame.pack()

        buttonsFrame = ttk.Frame(self.root, padding = 10)
        buttonsFrame.pack()

        self.data = self.loadData()
        
        #Tekinput Graphic Image Label
        photo = Utility.MakeTKImage(r'images/Logo/TKIG.png',160,90)
        label = ttk.Label(displayFrame, image = photo)
        label.grid(row = 0, column = 0)

        comboPreviewFrame = Labelframe(displayFrame, text = "Combo preview", width = 1000, height = 40)
        comboPreviewFrame.grid(row = 0, column = 1)
        comboPreviewFrame.grid_propagate(0)

        self.comboCanvas=Canvas(comboPreviewFrame, width = 1000, height = 40)
        comboFrame=Frame(self.comboCanvas)

        comboPreviewScrollbar=Scrollbar(comboPreviewFrame, orient = "horizontal", command=self.comboCanvas.xview)

        self.comboCanvas.configure(xscrollcommand = comboPreviewScrollbar.set)
        comboPreviewScrollbar.pack(side="bottom",fill="x")
        self.comboCanvas.pack(side="bottom")

        self.comboCanvas.create_window((0,0),window=comboFrame,anchor='nw')
        comboFrame.bind("<Configure>",self.scrollCanvas)

        #combo Preview label
        style.configure('comboPreviewLabel.TLabel', width = 100, height = 50)
        self.comboPreview = ttk.Label(comboFrame, style = 'comboPreviewLabel.TLabel')
        self.comboPreview.grid(row = 0, column = 1)

        #UI
        style.configure('InputButton.TButton', background = 'black', borderwidth = 10)

        # Game Selection widgets and functions
        gameSelectLabel = ttk.Label(selectFrame, text = "Choose game")
        gameSelectLabel.grid(row = 1, column = 1, padx = 10)
        self.gameSelect = ttk.Combobox(selectFrame, value = list(self.data['games'].keys()))
        self.gameSelect.bind("<<ComboboxSelected>>", self.updateSelection)
        self.gameSelect.grid(row = 2, column = 1, padx = 10)
        initialGame = next(iter(self.data['games'].keys()))
        self.gameSelect.set(initialGame)
    
        # Character Selection widgets and functions
        charSelectLabel = ttk.Label(selectFrame, text = "Choose character")
        charSelectLabel.grid(row = 1, column = 2)
        self.charSelect = ttk.Combobox(selectFrame, value = list(self.data['games'][initialGame]['characters'].keys()))
        self.charSelect.bind("<<ComboboxSelected>>", self.updateSelection)
        self.charSelect.grid(row = 2, column = 2)

        self.updateGame()

        #GENERATE, CLEAR, ERASE Buttons
        generatePhoto = Utility.MakeTKImage(r'images/Logo/Generate.png',162,50)
        clearPhoto    = Utility.MakeTKImage(r'images/Logo/Clear.png',125,50)
        erasePhoto    = Utility.MakeTKImage(r'images/Logo/Erase.png',125,50)

        generateBtn = ttk.Button(buttonsFrame, text = "Generate", command = self.generateImage, image = generatePhoto)
        clearBtn    = ttk.Button(buttonsFrame, text = "Clear", command = self.clear, image = clearPhoto)
        eraseBtn    = ttk.Button(buttonsFrame, text = "Erase", command = self.erase, image = erasePhoto)

        generateBtn.grid(row = 0, column = 0, padx = 0)
        clearBtn.grid(row = 0, column = 1, padx = 100)
        eraseBtn.grid(row = 0, column = 2, padx = 0)

        self.root.mainloop()

    def loadData(self):
        with open("data.json" ,'r') as datafile:
            data = json.load(datafile)
        return data

    #FUNCTIONS
    def generateImage(self):
        if (len(self.inputBuffer) == 0):
            return
    
        totalLength = 0

        for i in range(0, len(self.inputBuffer), 1):
            totalLength += self.originalImages[self.inputBuffer[i]].size[0] + self.padding

        #creates a new empty image, RGB mode, and size
        img = Utility.NewImage('RGBA', totalLength, self.originalImages[self.inputBuffer[0]].size[1])
        
        currentLength = 0
        for i in range(0, len(self.inputBuffer), 1):
            img.paste(self.originalImages[self.inputBuffer[i]], (currentLength, 0))
            currentLength += self.originalImages[self.inputBuffer[i]].size[0] + self.padding

        #saves the image onto the selected path
        img.save(os.path.join(self.savePath, self.gameSelect.get()+"-output", self.generateFilename() + '.png'))

        # img.show()

    def generateFilename(self):
        text = ""
        for input in self.inputBuffer:
            text += pathlib.Path(input).stem

        return text

    def generatePreview(self):
        if (len(self.inputBuffer) == 0):
            self.comboPreview.configure(image = None)
            self.comboPreview.image = None
            return

        totalLength = 0

        for imageFilename in self.inputBuffer:
            # print(self.previewImages[imageFilename].size[0])
            totalLength += self.previewImages[imageFilename].size[0]

        #creates a new empty image, RGB mode, and size
        new_im = Utility.NewImage('RGBA', totalLength, self.previewSize)
        
        currentLength = 0
        for imageFilename in self.inputBuffer:
            new_im.paste(self.previewImages[imageFilename], (currentLength, 0))
            currentLength += self.previewImages[imageFilename].size[0]
        
        photo = Utility.MakeTKImageWithImage(new_im)
        self.comboPreview.configure(image = photo)
        self.comboPreview.image = photo

    def addInput(self, input):
        self.inputBuffer.append(input)
        self.generatePreview()

    def clear(self):
        if (len(self.inputBuffer) == 0): 
            return None

        self.inputBuffer.clear()
        self.generatePreview()

    def erase(self):
        if (len(self.inputBuffer) == 0): 
            return None

        self.inputBuffer.pop()
        self.generatePreview()


    def getInputColumnWidth(self):
        # width = int(self.root.geometry().split('+')[0].split('x')[0])
        # # how many input columns can we fit *approximately
        # numInputColumns = math.floor(width / 200+10)
        # return numInputColumns
        # fuck it
        return 12

    def loadImage(self, imageFilename):
        filepath = os.path.join("images", self.gameSelect.get()+"-inputs", imageFilename)
        fullsize_img = Image.open(filepath)
        self.originalImages[imageFilename] = fullsize_img
        preview_img = copy.deepcopy(fullsize_img)
        y = preview_img.size[1] / self.previewSize
        x = preview_img.size[0] / y
        self.previewImages[imageFilename] = preview_img.resize((int(x),self.previewSize))
        preview_img.thumbnail((x,self.previewSize))
        self.thumbnailImages[imageFilename] = ImageTk.PhotoImage(preview_img)


    def updateGame(self):
        currentGame = self.gameSelect.get()

        for inButton in self.inputButtons:
            inButton.button.destroy()
        self.inputButtons = []
        
        numInputColumns = self.getInputColumnWidth()
        for i, imageFilename in enumerate(self.data['games'][currentGame]['inputs']):
            self.loadImage(imageFilename)
            # print(i % numInputColumns, i//numInputColumns)
            self.inputButtons.append(InputButton(self.inputFrame, imageFilename, self.thumbnailImages[imageFilename], self.addInput, i % numInputColumns, i//numInputColumns))
        
        self.charSelect.set("")
        self.charSelect.config(values=list(self.data['games'][currentGame]['characters'].keys()))


    def updateCharacter(self):
        newCharacter = self.charSelect.get()
        currentGame = self.gameSelect.get()
        characterInputs = self.data['games'][currentGame]['characters'][newCharacter]['inputs']
        numOtherInputs = len(self.data['games'][currentGame]['inputs'])

        numInputColumns = self.getInputColumnWidth()
        for inButton in self.inputButtons:
            if (not inButton.imageFilename in self.data['games'][currentGame]['inputs']):
                inButton.button.destroy()
                self.inputButtons.remove(inButton)
        
        for i, imageFilename in enumerate(characterInputs):
            self.loadImage(imageFilename)
            # print((numOtherInputs+i) % numInputColumns, (numOtherInputs+i)//numInputColumns)
            self.inputButtons.append(InputButton(self.inputFrame, imageFilename, self.thumbnailImages[imageFilename], self.addInput, (numOtherInputs+i) % numInputColumns, (numOtherInputs+i)//numInputColumns))

    def updateSelection(self, event):
        if (event.widget == self.gameSelect):
            self.updateGame()
        else:
            self.updateCharacter()

    def scrollCanvas(self, event):
        self.comboCanvas.configure(scrollregion=self.comboCanvas.bbox("all"), width=1000, height=40)

def main():
    a = MainWindow()

if __name__ == "__main__":
    main()