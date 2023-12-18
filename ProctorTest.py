import matplotlib.pyplot as plt


import sys
from PyQt5.QtWidgets import QApplication, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QDialog, QPushButton, QLabel, QGroupBox, QGridLayout, QLineEdit, QMessageBox
import matplotlib.pyplot as plt
import numpy as np
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon,  QPalette, QColor

class StandartProctorTest():
    def __init__(self):
        pass
    
    def WaterContent(self,Mw,Md,Mc):
        return ((Mw - Md)/(Md - Mc)) * 100
    
    def Lambda(self,MassOfSoilAndMold, MassOfMold, VolumeOfMold):
        return ((MassOfSoilAndMold - MassOfMold)/ VolumeOfMold) * 9.81
        
    def ydry(self,Lambda,WaterContent):
        return Lambda / ( 1 + (WaterContent/100)) 
    
        



class ProcotrTest(QDialog):
    def __init__(self):
        super(ProcotrTest, self).__init__()
        self._initUI()
        self._proctorTest = StandartProctorTest()
        self._MaxYdry = 0
        self._OptimumWaterContent = 0
       
    
    def _initUI(self):
        self.setWindowTitle("Proctor Test")
        self.setGeometry(500, 100, 825, 520)
        
        self.table = QTableWidget(self)
        self.table.setColumnCount(6)
        self.table.setRowCount(5)
        headers = ["Mass of Soil and Mold (g)", "Mass of can and Wet Soil (g), Mw", "Mass of can and Dry Soil (g), Md", "Mass of can (g), Mc", "Water Content (%)  w", "Dry Unit Weight (KN/m^3)"]
        self.table.setHorizontalHeaderLabels(headers)
        self.table.setStyleSheet(
            "font: 8pt 'Helvetica Neue';"  
            "color: #333;"  
            "background-color: #f4f4f4;"  
            "border: 1px solid #ccc;"
        )
        self.addRows_button = QPushButton("Add Row", self)
        self.addRows_button.clicked.connect(self.add_row)
        self.calculate_button = QPushButton("Calculate Values", self)
        self.calculate_button.clicked.connect(self.calculate_values)
        self.remove_last_row_button = QPushButton('Delete Last Row', self)
        self.remove_last_row_button.clicked.connect(self.remove_last_row)
        self.calculate_button.setStyleSheet(
            "font: 10pt 'Helvetica Neue';"  
            "color: white;"  
            "background-color: #0071c5;"  
            "border: 2px solid #00538a;"  
            "border-radius: 10px;"  
            "padding: 5px;"  
        )
        self.addRows_button.setStyleSheet(
            "font: 10pt 'Helvetica Neue';"  
            "color: white;"  
            "background-color: #0071c5;"  
            "border: 2px solid #00538a;"  
            "border-radius: 10px;"  
            "padding: 5px;"  
        )
        self.remove_last_row_button.setStyleSheet(
            "font: 10pt 'Helvetica Neue';"  
            "color: white;"  
            "background-color: #0071c5;"  
            "border: 2px solid #00538a;"  
            "border-radius: 10px;"  
            "padding: 5px;"  
        )
        self.maximumDryUnitLabel = QLabel("Maximum Dry Unit Weight = ")
        self.optimumWaterContentLabel = QLabel("Optimum Water Content  = ")
        self.maximumDryUnitLabel.setStyleSheet(
            "font: 10pt 'Helvetica Neue';"  
            "color: #333;" 
            "background-color: #f4f4f4;"  
            "border: 1px solid #ccc;"  
            "border-radius: 10px;"  
            "padding: 10px;"  
        )
        self.optimumWaterContentLabel.setStyleSheet(
            "font: 10pt 'Helvetica Neue';"  
            "color: #333;"  
            "background-color: #f4f4f4;" 
            "border: 1px solid #ccc;"  
            "border-radius: 10px;"  
            "padding: 10px;"  
        )
        
        self.MassOfMold_input = QLineEdit(self)
        self.VolumeOfMold_input = QLineEdit(self)
        
        self.grid_group_box = QGroupBox()
        self.main_layout = QGridLayout()

        self.main_layout.setColumnStretch(0, 8)
        self.main_layout.setRowStretch(0,2)
        self.main_layout.setRowStretch(1,1)
        self.main_layout.setColumnStretch(1, 1)
        self.main_layout.setColumnStretch(2,1)
        self.main_layout.addWidget(self.table, 0, 0, 1,5)
        self.main_layout.addWidget(self.calculate_button, 6, 1, 1, 1, alignment=Qt.AlignmentFlag.AlignRight)
        self.main_layout.addWidget(self.addRows_button, 1, 2, 1, 1)
        self.main_layout.addWidget(self.remove_last_row_button, 2, 2, 1, 1)
        self.main_layout.addWidget(QLabel("Mass of Mold:"), 3, 1, 1, 1)
        self.main_layout.addWidget(self.MassOfMold_input, 3, 2, 1, 1)
        self.main_layout.addWidget(QLabel("Volume of Mold:"), 4, 1, 1, 1)
        self.main_layout.addWidget(self.VolumeOfMold_input, 4, 2, 1, 1)
        self.main_layout.addWidget(self.optimumWaterContentLabel, 4,0,1,1)
        self.main_layout.addWidget(self.maximumDryUnitLabel, 5,0,1,1)
        
        self.grid_group_box.setStyleSheet(  
            "background-color: #f1f1f1;"   
                   
        )
        
        self.grid_group_box.setLayout(self.main_layout)
        window_layout = QVBoxLayout()
        window_layout.addWidget(self.grid_group_box)
        self.setLayout(window_layout)
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(255, 255, 255))  
        self.setPalette(palette)
    
    def add_row(self):
        row_position = self.table.rowCount()
        self.table.insertRow(row_position)

    def remove_last_row(self):
        last_row_index = self.table.rowCount() - 1
        if last_row_index >= 0:
            self.table.removeRow(last_row_index)
    
    def calculate_values(self):
        Mw = self.get_column_values_as_float(self.table,1)
        Md = self.get_column_values_as_float(self.table,2)
        Mc = self.get_column_values_as_float(self.table,3)
        print(Md)
        if Mw == 0 or Md == 0 or Mc == 0 or len(Mw) == 0 or len(Md) == 0 or len(Mc) == 0:
            self.show_warning_dialog("Please enter all required values")
            return
        waterContent = list()

        try:
            for i in range(self.table.rowCount()):
                waterContent.append(self._proctorTest.WaterContent(Mw=Mw[i], Md=Md[i], Mc=Mc[i]))
            massOfSoilAndMold = self.get_column_values_as_float(self.table,0)
            print(massOfSoilAndMold)
           
            massOfMold = self.get_mold_value(self.MassOfMold_input)
            volumeOfMold = self.get_mold_value(self.VolumeOfMold_input)
            if volumeOfMold == None or massOfMold == None or massOfSoilAndMold == 0 or len(massOfSoilAndMold) == 0:
                self.show_warning_dialog("Please enter all required values")
                return
            lambda_values = list()
            for i in range(self.table.rowCount()):
                lambda_values.append(self._proctorTest.Lambda(MassOfSoilAndMold=massOfSoilAndMold[i], MassOfMold=massOfMold, VolumeOfMold= volumeOfMold))
            yDry = list()
            for i in range(self.table.rowCount()):
                yDry.append(self._proctorTest.ydry(Lambda=lambda_values[i], WaterContent=waterContent[i]))
        except IndexError:
            self.show_warning_dialog("delete empty rows :)")
            return
        
        self._MaxYdry = max(yDry)
        self.set_column_values(self.table, 4, waterContent )
        self.set_column_values(self.table, 5, yDry)
        self.compaction_curve(waterContent,yDry)
        
        self.maximumDryUnitLabel.setText(f"Maximum Dry Unit Weight = {self._MaxYdry} KN/m^3")
        self.optimumWaterContentLabel.setText(f"Optimum Water Content  = {self._OptimumWaterContent} %")
        self.maximumDryUnitLabel.setStyleSheet(
            "font: 10pt 'Helvetica Neue';"  
            "color: #ff0000;" 
            "background-color: #f4f4f4;"  
            "border: 1px solid #ccc;"  
            "border-radius: 10px;"  
            "padding: 10px;"  
        )
        self.optimumWaterContentLabel.setStyleSheet(
            "font: 10pt 'Helvetica Neue';"  
            "color: #ff0000;" 
            "background-color: #f4f4f4;"  
            "border: 1px solid #ccc;"  
            "border-radius: 10px;"  
            "padding: 10px;"  
        )
        
        
        
        
    
    
    def get_mold_value(self, mold_input):
        try:
            return float(mold_input.text())
        except ValueError:
            return None
        
    def get_column_values_as_float(self, table, column_index):
        values = []
        for row in range(table.rowCount()):
            item = table.item(row, column_index)
            if item is not None:
                try:
                    float_value = float(item.text())
                    values.append(float_value)
                except ValueError:
                    return 0
        return values

    def set_column_values(self, table, column_index, values):
        for row, value in enumerate(values):
            value = f"{value:.4f}"
            item = QTableWidgetItem(value)
            table.setItem(row, column_index, item)
            
    
    def show_warning_dialog(self, message):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setWindowTitle("Warning")
        msg_box.setText(message)
        msg_box.exec_()
    
    
    def compaction_curve(self,MoistureContent, DryUnitWeight):
        moisture_content = np.array(MoistureContent)
        dry_unit_weight = np.array(DryUnitWeight)

        sorted_indices = np.argsort(moisture_content)
        moisture_content_sorted = moisture_content[sorted_indices]
        dry_unit_weight_sorted = dry_unit_weight[sorted_indices]
        degree = 2
        coefficients = np.polyfit(moisture_content_sorted, dry_unit_weight_sorted, degree)
        polynomial = np.poly1d(coefficients)
        derivative = np.polyder(polynomial)
        critical_points = np.roots(derivative)
        vertex_x = critical_points[0]
        vertex_y = polynomial[vertex_x]
        print(vertex_y)

        self._OptimumWaterContent = vertex_x
        plt.plot(moisture_content_sorted, dry_unit_weight_sorted, marker='o', linestyle='dotted')

        x_fit = np.linspace(min(moisture_content_sorted), max(moisture_content_sorted), 100)
        y_fit = polynomial(x_fit)
        plt.plot(x_fit, y_fit)

        plt.xlabel('Moisture Content (%)')
        plt.ylabel('Dry Unit Weight (kN/m^3)')
        plt.title('Compaction Curve with Polynomial Fit')
        plt.legend()
        plt.grid(True)

        plt.show()


        
    