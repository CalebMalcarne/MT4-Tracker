import sys
import os
import csv
import json
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QAction, QCheckBox
from PyQt5.QtCore import QTimer, Qt
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from datetime import datetime
from graphing import *
from settings import SettingsWindow
from edit_config import *
from reports import *
from graphWindows import *




class AccountBalanceGraph(QMainWindow):
    def __init__(self, parent=None):
        super(AccountBalanceGraph, self).__init__(parent)
        
        self.setWindowTitle("Account Balance Graph")
        self.setGeometry(100, 100, 800, 600)
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        self.layout = QVBoxLayout(self.central_widget)
        
        self.data = []
        self.config = getConfigData() 
        
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        self.layout.addWidget(self.canvas)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(int(self.config.get("update_delay", "")) * 1000)  # Update every 10 seconds

        self.create_menu()

        self.display_all_checkbox = QCheckBox("Display All", self)
        self.display_all_checkbox.stateChanged.connect(self.toggle_display_all)
        self.layout.addWidget(self.display_all_checkbox)

        self.display_week_checkbox = QCheckBox("Display Week", self)
        self.display_week_checkbox.stateChanged.connect(self.toggle_display_week)
        self.layout.addWidget(self.display_week_checkbox)

        
        # Create a placeholder for the All Graph window
        self.all_graph_window = None
        self.week_graph_window = None

    def create_menu(self):
        settings_action = QAction("Settings", self)
        settings_action.triggered.connect(self.open_settings)
        
        export_action = QAction("Export Graph", self)
        export_action.triggered.connect(self.export_graph)

        report_action = QAction("Send Day Report", self)
        report_action.triggered.connect(self.send_day_report)

        report_weel_action = QAction("Send Week Report", self)
        report_weel_action.triggered.connect(self.send_week_report)

        menubar = self.menuBar()
        file_menu = menubar.addMenu("File")
        file_menu.addAction(settings_action)
        file_menu.addAction(export_action)
        file_menu.addAction(report_action)
        file_menu.addAction(report_weel_action)

    def open_settings(self):
        settings_window = SettingsWindow(self)
        settings_window.exec_()

    def toggle_display_week(self, state):
        if state == Qt.Checked:
            self.open_week_graph_window()
        else:
            self.close_week_graph_window()

    def toggle_display_all(self, state):
        if state == Qt.Checked:
            self.open_all_graph_window()
        else:
            self.close_all_graph_window()


    def open_week_graph_window(self):
        if self.week_graph_window is None:
            self.week_graph_window = WeekGraphWindow(self)
            self.week_graph_window.show()

    def close_week_graph_window(self):
        if self.week_graph_window is not None:
            self.week_graph_window.close()
            self.week_graph_window = None

    def open_all_graph_window(self):
        if self.all_graph_window is None:
            self.all_graph_window = AllGraphWindow(self)
            self.all_graph_window.show()

    def close_all_graph_window(self):
        if self.all_graph_window is not None:
            self.all_graph_window.close()
            self.all_graph_window = None

    def newSheet(self):
        now = datetime.now()
        date = now.strftime("%m%d%y")
        
        fileName = f"{date}.csv"
        path = f"Sheets/{fileName}"
        
        with open(path, 'w') as file:
            file.close()
        print(f"New file {fileName} created successfully")

    def dateCheck(self):
        now = datetime.now()
        date = now.strftime("%m%d%y")
        
        file_names = os.listdir("Sheets")
        
        if len(file_names) == 0:
            return True
        
        lastSheet = file_names[-1]
        lastSheetDate = lastSheet[:6]
        
        if datetime.strptime(date, "%m%d%y") > datetime.strptime(lastSheetDate, "%m%d%y"):
            return True
        else:
            return False
          
    def addVal(self, balance):
        now = datetime.now()
        date = now.strftime("%m%d%y")
        HM = now.strftime("%H:%M")
        fname = f"{date}.csv"
        
        with open(f"Sheets/{fname}", 'a', newline = '') as csvfile:
            csv_writer = csv.writer(csvfile, delimiter=',')
            csv_writer.writerow([HM, balance])

    def addToSheet(self, balance):
        bals = []
        new = False
        
        if self.dateCheck():
            self.newSheet()
    
        now = datetime.now()
        date = now.strftime("%m%d%y")
        fname = f"{date}.csv"
                
        with open(f"Sheets/{fname}", mode = 'r') as csvfile:
            csv_reader = csv.reader(csvfile, delimiter=",")
            rows = list(csv_reader)
            if len(rows) > 0:
                for row in rows:
                    bals.append(float(row[1]))
            else:
                new = True
        
        if new:
            bals.append(balance)
            self.addVal(balance)
            print(f"Added {balance} to sheet")
        else:        
            if float(balance) != bals[-1]:
                print(f"{balance}, {bals[-1]}")
                bals.append(balance)
                self.addVal(balance)
                print(f"Added {balance} to sheet")
        

    def export_graph(self, type):
        date_str = datetime.now().strftime("%m%d%y")
        if type == 0:
            filename = f"BalGraphDay-{date_str}.png"
            filepath = (f"img/{filename}")
            self.figure.savefig(filepath)
            print(f"Graph saved as {filename}")
        elif type == 1:
            filename = f"BalGraphWeek-{date_str}.png"
            filepath = (f"img/{filename}")
            if self.week_graph_window is not None:

                self.week_graph_window.figure.savefig(filepath)
                print(f"Graph saved as {filename}")
            else:
                print("Week graph window not open")

    def send_day_report(self):
        self.export_graph(0)
        sendDayReport()
    
    def send_week_report(self):
        self.export_graph(1)
        sendWeekReport()


    def get_account_balance(self):
        config = getConfigData()
        path = config["mt4_files_directory"]
        file_name = f"{path}/AccountBalance.txt"
        if os.path.exists(file_name):
            try:
                with open(file_name, 'r') as file:
                    try:
                        balance = float(file.readline().strip())
                        return balance
                    except ValueError:
                        print("Error reading balance from file")
                        return None
            except OSError:
                print ("Error Reading file")
        else:
            return None
        
    def update(self):
        balance = self.get_account_balance()
        if balance is not None:
            self.addToSheet(balance)
        graphDay(self)

        if self.all_graph_window is not None:
            graphAll(self.all_graph_window)
        if self.week_graph_window is not None:
            graphWeek(self.week_graph_window)
            
def main():
    app = QApplication(sys.argv)
    main_win = AccountBalanceGraph()
    main_win.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
