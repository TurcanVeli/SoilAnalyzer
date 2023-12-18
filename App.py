import matplotlib.pyplot as plt
import sys
from PyQt5.QtWidgets import QApplication, QTableWidget,QMainWindow ,QStackedWidget ,QTableWidgetItem, QVBoxLayout, QWidget, QDialog, QPushButton, QLabel, QGroupBox, QGridLayout, QLineEdit, QMessageBox
import numpy as np
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon,  QPalette, QColor
from SieveAnalysis import SoilAnalyzer
from ProctorTest import ProcotrTest



class App(QWidget):
    def __init__(self):
        super(App, self).__init__()
        self._initUi()
    
    def _initUi(self):
        self.setWindowTitle("Analysis")
        self.setGeometry(100, 100, 425, 320)
        self.Description_label = QLabel("Version 0.5.0")
        self.Producer_label = QLabel("Powered by Mustafa Mert Kayhan & Yusuf Aktan")
        self.SoilAnalyzer_button = QPushButton("Sieve Analysis Calculator", self)
        self.SoilAnalyzer_button.clicked.connect(self._changeScreenToSoilAnalyzer)
        self.WaterAnalyzer_button = QPushButton("Proctor Test", self)
        self.WaterAnalyzer_button.clicked.connect(self._changeScreenToWaterAnalyzer)
        self.SoilAnalyzer_button.setStyleSheet(
            "font: 10pt 'Helvetica Neue';"  
            "color: white;"  
            "background-color: #0071c5;"  
            "border: 2px solid #00538a;"  
            "border-radius: 10px;"  
            "padding: 5px;"  
        )
        self.WaterAnalyzer_button.setStyleSheet(
            "font: 10pt 'Helvetica Neue';"  
            "color: white;"  
            "background-color: #0071c5;"  
            "border: 2px solid #00538a;"  
            "border-radius: 10px;"  
            "padding: 5px;"  
        )
        
        
        self.grid_group_box = QGroupBox()
        self.main_layout = QGridLayout()
        self.main_layout.setColumnStretch(0, 0)
        self.main_layout.setColumnStretch(1, 0)
        self.main_layout.addWidget(self.Description_label,1,0,2,2,alignment=Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(self.SoilAnalyzer_button, 0, 0,1,1)
        self.main_layout.addWidget(self.WaterAnalyzer_button, 0, 1,1,1)
        self.main_layout.addWidget(self.Producer_label,2,0,2,2, Qt.AlignmentFlag.AlignRight)
        
        self.screen = SoilAnalyzer()
        self.WaterScreen = ProcotrTest()
        self.grid_group_box.setLayout(self.main_layout)

        window_layout = QVBoxLayout()
        window_layout.addWidget(self.grid_group_box)
        self.setLayout(window_layout)
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(255, 255, 255))  
        self.setPalette(palette)
    def mousePressEvent(self, event):

        if event.button() == 2: 
            self.show_warning_dialog("Developer Notu: Cebimde yoktu, yüreğimden verdim.")
    def show_warning_dialog(self, message):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setWindowTitle("Warning")
        msg_box.setText(message)
        msg_box.exec_()
    
    def _changeScreenToSoilAnalyzer(self):
        self.screen.show()
    
    def _changeScreenToWaterAnalyzer(self):
        self.WaterScreen.show()
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('Icon/analyzing.png'))
  
    
    window = App()
    window.show()
    sys.exit(app.exec_())


       

