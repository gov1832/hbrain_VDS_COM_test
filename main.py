import sys
import os

from PyQt5.uic          import loadUi
from PyQt5.QtGui        import QPixmap
from PyQt5.QtGui        import QIcon
from PyQt5.QtWidgets    import *

from main_function import main_function

import cv2

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.ui = loadUi(self.resource_path('main.ui'), self)
        self.ui.hbrain_icon.setPixmap(QPixmap("resources/icon/hbrain_logo.png"))
        self.setWindowIcon(QIcon("resources/icon/hbrain.png"))
        self.mf = main_function(self.ui)

    def resource_path(self, relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        # try:
        #     # PyInstaller creates a temp folder and stores path in _MEIPASS
        #     base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        #     print("base_path:", base_path)
        # except Exception:
        base_path = os.path.abspath(".")

        # return os.path.join(base_path, './', relative_path)
        return os.path.join(base_path, relative_path)

if __name__ == '__main__':
    # cap = cv2.VideoCapture('testImg.jg')
    # cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    # cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
    # _, img = cap.read()
    #
    # print(str(type(img)))
    # if str(type(img)) == "<class 'NoneType'>":
    #     print('asljdhfgoasdjhh')
    #
    # if type(img) == None:
    #     print(type(img))
    # else:
    #     cv2.imshow('img', img)
    #     cv2.waitKey(0)
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    app.exec_()
