import sys

import random
from PyQt5 import uic, QtWidgets
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidget, QTableWidgetItem, QMessageBox

class ShiftHeadMenu(QMainWindow):
    def __init__(self):
        super(ShiftHeadMenu, self).__init__()
        self.ui = uic.loadUi("forms/shoft_head.ui", self)
        self.window().setWindowTitle("F")

class Builder:
    def __init__(self):
        self.gui = None

    def create_gui(self):
        self.gui=ShiftHeadMenu()
        return self.gui

if __name__ == '__main__':
    qapp = QtWidgets.QApplication(sys.argv)
    B = Builder()

    window = B.create_gui()
    window.show()
    qapp.exec()


