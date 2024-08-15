import sys
import os
import csv
import json
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QAction, QCheckBox
from PyQt5.QtCore import QTimer
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from datetime import datetime
from graphing import *
from settings import SettingsWindow
from edit_config import *
from reports import sendReport

class AllGraphWindow(QMainWindow):
    def __init__(self, parent=None):
        super(AllGraphWindow, self).__init__(parent)
        self.setWindowTitle("All Account Balances Over Time")
        self.setGeometry(150, 150, 800, 600)
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        self.layout = QVBoxLayout(self.central_widget)
        
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        self.layout.addWidget(self.canvas)
        
        graphAll(self)