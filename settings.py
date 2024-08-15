"""
Copyright © 2023 Malcarne Contracting Inc. All rights reserved.
"""
from edit_config import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class SettingsWindow(QDialog):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setWindowTitle("Settings")
        self.config = getConfigData()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # MT4 Files directory setting
        self.directory_label = QLabel("MT4 Files Directory:")
        layout.addWidget(self.directory_label)

        self.directory_edit = QLineEdit()
        self.directory_edit.setText(self.config.get("mt4_files_directory", ""))
        layout.addWidget(self.directory_edit)

        # Report time setting
        self.report_time_label = QLabel("Report Time:")
        layout.addWidget(self.report_time_label)

        self.report_time_edit = QTimeEdit()
        report_time = QTime.fromString(self.config.get("report_time", "00:00"), "HH:mm")
        self.report_time_edit.setTime(report_time)
        layout.addWidget(self.report_time_edit)
        
        self.update_delay_label = QLabel("Update Delay (s)")
        layout.addWidget(self.update_delay_label)
        
        self.update_delay = QLineEdit()
        self.update_delay.setText(self.config.get("update_delay", ""))
        layout.addWidget(self.update_delay)

        self.account_label = QLabel("Account:")
        layout.addWidget(self.account_label)
        
        self.account = QLineEdit()
        self.account.setText(self.config.get("account", ""))
        layout.addWidget(self.account)
        

        # Save button
        self.save_button = QPushButton("Save")
        layout.addWidget(self.save_button)
        self.save_button.clicked.connect(self.applyChanges)

        self.setLayout(layout)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.applyChanges()
        else:
            super().keyPressEvent(event)

    def applyChanges(self):
        mt4_directory = self.directory_edit.text()
        self.config["mt4_files_directory"] = mt4_directory

        report_time = self.report_time_edit.time().toString("HH:mm")
        self.config["report_time"] = report_time
        
        update_delay = self.update_delay.text()
        self.config["update_delay"] = update_delay

        account = self.account.text()
        self.config["account"] = account
        
        self.saveConfig()

        self.accept()

    def saveConfig(self):
        writeConfigData(self.config)
