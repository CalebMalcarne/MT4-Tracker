import sys
import os
import time
import csv
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtCore import QTimer
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from datetime import datetime

def graphDay(main):
    bal = []
    time = []
    
    date = datetime.now().strftime("%m%d%y")
    fName = f"{date}.csv"
    
    with open(f"Sheets/{fName}", "r") as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=",")
        for row in csv_reader:
            time.append(row[0])
            bal.append(float(row[1]))
   
    main.ax.clear()
    main.ax.plot(time, bal, color="blue", marker='o', linestyle='-')  # Adding markers for clarity
    main.ax.set_xlabel('Time')
    main.ax.set_ylabel('Balance')
    main.ax.set_title('Account Balance Over Time')
    main.ax.grid(True)  # Add a grid for better readability
    main.canvas.draw()
    print("Graphing")
            
def graphWeek(main):
    pass

def graphMonth(main):
    pass
    
def graphAll(main):
    bal = []
    time_points = []
    
    file_names = os.listdir("Sheets")
    file_names.sort()  
    
    for file in file_names:
        with open(f"Sheets/{file}", "r") as csvfile:
            csv_reader = csv.reader(csvfile, delimiter=",")
            day_bal = []
            day_time_points = []
            
            for row in csv_reader:
                day_time_points.append(f"{file[:6]} {row[0]}")  
                day_bal.append(float(row[1]))  
            
            time_points.extend(day_time_points)
            bal.extend(day_bal)
            

            main.ax.plot(day_time_points, day_bal, marker='o', linestyle='-', label=file[:6])

    main.ax.clear()
    main.ax.plot(time_points, bal, color="blue", marker='o', linestyle='-')
    main.ax.set_xlabel('Time')
    main.ax.set_ylabel('Balance')
    main.ax.set_title('Account Balance Over Time')
    main.ax.grid(True)  
    main.ax.legend(title="Days")  
    main.ax.tick_params(axis='x', rotation=45)  
    main.canvas.draw()
    print("Graphing") 


