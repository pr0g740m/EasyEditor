#create the Easy Editor photo editor here!
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QListWidget, QFileDialog
)
from PyQt5.QtGui import QPixmap
import os
from PIL import Image, ImageFilter, ImageEnhance

App = QApplication([])
win = QWidget()
win.resize(700, 500)
win.setWindowTitle("Easy Editor")

button_folder = QPushButton("Folder")
button_left = QPushButton("Left")
button_right = QPushButton("Right")
button_mirror = QPushButton("Mirror")
button_sharpness = QPushButton("Sharpness")
button_BW = QPushButton("B&W")

list_image = QListWidget()

image = QLabel()

main_line = QHBoxLayout()
col_1 = QVBoxLayout()
col_1.addWidget(button_folder)
col_1.addWidget(list_image)

row_1 = QHBoxLayout()
row_1.addWidget(button_left)
row_1.addWidget(button_right)
row_1.addWidget(button_mirror)
row_1.addWidget(button_sharpness)
row_1.addWidget(button_BW)

col_2 = QVBoxLayout()
col_2.addWidget(image)
col_2.addLayout(row_1)

main_line.addLayout(col_1, 20)
main_line.addLayout(col_2,80)

win.setLayout(main_line)

win.show()

workdir = ''
def filter(files, extensions):
    filename = []
    for names in files:
        for extension in extensions:
            if names.endswith(extension):
                filename.append(names)
    return filename

def chooseWorkdir():
    global workdir
    workdir = QFileDialog.getExistingDirectory()

def showFileNameList():
    extensions = [".jpg", ".jpeg", ".png", ".gif", ".bmp"]
    chooseWorkdir()
    filenames = filter(os.listdir(workdir), extensions)
    list_image.clear()
    for name in filenames:
        list_image.addItem(name)
        
button_folder.clicked.connect(showFileNameList)

class imageProcessor():
    def __init__(self):
        self.image = None
        self.filename = None
        self.savefile = "edit/"
    def loadImage(self, filename):
        self.filename = filename
        file_path = os.path.join(workdir, filename)
        self.image = Image.open(file_path)
    def showImage(self, path):
        image.hide()
        pixmapImg = QPixmap(path)
        w, h = image.width(), image.height()
        pixmapImg = pixmapImg.scaled(w, h, Qt.KeepAspectRatio)
        image.setPixmap(pixmapImg)
        image.show()
    def saveImage(self):
        path = os.path.join(workdir, self.savefile)
        if not(os.path.exists(path) or os.path.isdir(path)):
            os.mkdir(path)
        file_path = os.path.join(path, self.filename)
        self.image.save(file_path)      
    def makeBW(self):
        self.image  = self.image.convert("L")
        self.saveImage()
        path = os.path.join(workdir, self.savefile, self.filename)
        self.showImage(path)
    def doFlip(self):
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.saveImage()
        path = os.path.join(workdir, self.savefile, self.filename)
        self.showImage(path)
    def turnLeft(self):
        self.image = self.image.transpose(Image.ROTATE_90)
        self.saveImage()
        path = os.path.join(workdir, self.savefile, self.filename)
        self.showImage(path)
    def turnRight(self):
        self.image = self.image.transpose(Image.ROTATE_270)
        self.saveImage()
        path = os.path.join(workdir, self.savefile, self.filename)
        self.showImage(path)
    def sharpen(self):
        self.image = self.image.filter(ImageFilter.EDGE_ENHANCE)
        self.saveImage()
        path = os.path.join(workdir, self.savefile, self.filename)
        self.showImage(path)
    

def showChosenImage():
    if list_image.currentRow() >= 0:
        file_name = list_image.currentItem().text()
        workimage.loadImage(file_name)
        file_path = os.path.join(workdir, workimage.filename)
        workimage.showImage(file_path)
workimage = imageProcessor()

list_image.currentRowChanged.connect(showChosenImage)
button_BW.clicked.connect(workimage.makeBW)
button_mirror.clicked.connect(workimage.doFlip)
button_left.clicked.connect(workimage.turnLeft)
button_right.clicked.connect(workimage.turnRight)
button_sharpness.clicked.connect(workimage.sharpen)
App.exec()

