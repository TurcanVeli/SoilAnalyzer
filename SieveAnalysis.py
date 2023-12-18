import matplotlib.pyplot as plt


import sys
from PyQt5.QtWidgets import QApplication, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QDialog, QPushButton, QLabel, QGroupBox, QGridLayout, QLineEdit, QMessageBox
import matplotlib.pyplot as plt
import numpy as np
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon,  QPalette, QColor

class SoilAnalyzer(QWidget):
    def __init__(self):
        super(SoilAnalyzer, self).__init__()
        self.result_text = ""
        self.group_symbol = ""
        self.setWindowTitle("Soil Analyzer")
        self.setGeometry(500, 100, 825, 720)

        self.cu = 0
        self.cc = 0

        self.table = QTableWidget(self)
        self.table.setColumnCount(6)
        self.table.setRowCount(9)
        headers = ["Sieve Number", "Particle Size", "Mass Retained", "Percent Retained", "Cum % Retained", "Percent Passing"]
        sieve_numbers = ["4", "8", "16", "30", "40", "50", "100", "200", "0"]
        particle_sizes = ["4.750", "2.360", "1.180", "0.600", "0.425", "0.300", "0.150", "0.075", "0"]
        self.table.setHorizontalHeaderLabels(headers)

        
        for row in range(len(sieve_numbers)):
            self.table.setItem(row, 0, QTableWidgetItem(sieve_numbers[row]))
            self.table.setItem(row, 1, QTableWidgetItem(particle_sizes[row]))


        for row in range(9):
            item = QTableWidgetItem("?")
            self.table.setItem(row, 2, item)

        self.table.setStyleSheet(
            "font: 8pt 'Helvetica Neue';"  
            "color: #333;"  
            "background-color: #f4f4f4;"  
            "border: 1px solid #ccc;"  
        )




        self.calculate_button = QPushButton("Calculate Values", self)
        self.calculate_button.clicked.connect(self.calculate_values)

        self.result_button = QPushButton("calculate soil properties", self)
        self.result_button.clicked.connect(self.calculate_soil_properties)

        self.graph_button = QPushButton("plot particle size distribution", self)
        self.graph_button.clicked.connect(self.plot_particle_size_distribution)
        
        self.addRows_button = QPushButton("Add Row", self)
        self.addRows_button.clicked.connect(self.add_row)

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
        self.result_button.setStyleSheet(
            "font: 10pt 'Helvetica Neue';" 
            "color: white;" 
            "background-color: #0071c5;" 
            "border: 2px solid #00538a;" 
            "border-radius: 10px;"  
            "padding: 5px;"  
        )
        self.graph_button.setStyleSheet(
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
        
        

        self.sand_percentage_label = QLabel("Sand Percentage: ")
        self.gravel_percentage_label = QLabel("Gravel Percentage: ")
        self.sand_percentage_label.setStyleSheet(
            "font: 10pt 'Helvetica Neue';"  
            "color: #333;" 
            "background-color: #f4f4f4;"  
            "border: 1px solid #ccc;"  
            "border-radius: 10px;"  
            "padding: 10px;"  
        )
        self.gravel_percentage_label.setStyleSheet(
            "font: 10pt 'Helvetica Neue';"  
            "color: #333;"  
            "background-color: #f4f4f4;" 
            "border: 1px solid #ccc;"  
            "border-radius: 10px;"  
            "padding: 10px;"  
        )
    
        self.liquid_limit_input = QLineEdit(self)
        self.plastic_limit_input = QLineEdit(self)

        
        self.grid_group_box = QGroupBox()
        self.main_layout = QGridLayout()

        self.main_layout.setColumnStretch(0, 8)
        self.main_layout.setColumnStretch(1, 1)
        self.main_layout.setColumnStretch(2, 1)
        self.main_layout.setColumnStretch(3, 1)
        self.main_layout.addWidget(self.table, 0, 0, 4, 5)
        self.main_layout.addWidget(self.sand_percentage_label, 4, 0, 1, 1,alignment=Qt.AlignmentFlag.AlignLeft)
        self.main_layout.addWidget(self.gravel_percentage_label, 4, 1, 1, 1)
        self.main_layout.addWidget(self.calculate_button, 6, 0, 1, 1, alignment=Qt.AlignmentFlag.AlignLeft)
        self.main_layout.addWidget(self.graph_button, 7, 0, 1, 1, alignment=Qt.AlignmentFlag.AlignLeft)
        self.main_layout.addWidget(self.addRows_button, 8, 1, 1, 1)
        self.main_layout.addWidget(self.remove_last_row_button, 9,1,1,1)
        self.main_layout.addWidget(self.result_button, 8, 0, 1, 1, alignment=Qt.AlignmentFlag.AlignLeft)
        self.main_layout.addWidget(QLabel("Liquid Limit:"), 6, 1, 1, 1)
        self.main_layout.addWidget(self.liquid_limit_input, 6, 2, 1, 1)
        self.main_layout.addWidget(QLabel("Plastic Limit:"), 7, 1, 1, 1)
        self.main_layout.addWidget(self.plastic_limit_input, 7, 2, 1, 1)

        self.grid_group_box.setLayout(self.main_layout)
        self.grid_group_box.setStyleSheet(  
            "background-color: #f1f1f1;"   
                   
        )
        window_layout = QVBoxLayout()
        window_layout.addWidget(self.grid_group_box)
        self.setLayout(window_layout)
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(255, 255, 255))  
        self.setPalette(palette)

    def calculate_soil_properties(self):
        if self.Gravel == 0 or self.Sand == 0:
            self.show_warning_dialog("First calculate all values")
            return

        value_of_200 = self.get_column_values_as_float(self.table, 2)[-1]

        if self.Gravel > self.Sand:
            if value_of_200 < 5:
                self.process_gravel_properties(4, 1, 3, "GW", "Well-graded gravel", "Well-graded gravel with sand")
            elif 5 <= value_of_200 <= 12:
                self.process_gravel_properties(4, 1, 3, "GW-GM", "Well-graded gravel with silt", "Well-graded gravel with silt and sand")
            elif value_of_200 > 12:
                self.process_gravel_properties(0, 0, 0, "GM", "Silty gravel", "Silty gravel with sand")
        else:
            if value_of_200 < 5:
                self.process_sand_properties(6, 1, 3, "SW", "Well graded sand", "Well graded sand with gravel")
            elif 5 <= value_of_200 <= 12:
                self.process_sand_properties(6, 1, 3, "SW-SM", "Well-graded Sand with silt", "Well-graded sand with silt and gravel")
            elif value_of_200 > 12:
               self.process_sand_properties(0, 0, 0, "SM", "Silty sand", "Silty sand with gravel")

        self.show_result_dialog(self.GroupSymbol, self.resultText)
    
    def process_gravel_properties(self, cu_threshold, cc_lower, cc_upper, group_symbol, result_text_low, result_text_high):
        if self.CU >= cu_threshold:
            if cc_lower <= self.CC <= cc_upper:
                self.GroupSymbol = group_symbol
                self.resultText = result_text_low if self.Sand < 15 else result_text_high
            else:
                self.GroupSymbol = "GP"
                self.resultText = result_text_low if self.Sand < 15 else result_text_high
        else:
            self.GroupSymbol = "GP"
            self.resultText = result_text_low if self.Sand < 15 else result_text_high

    def process_sand_properties(self, cu_threshold, cc_lower, cc_upper, group_symbol, result_text_low, result_text_high):
        if self.CU > cu_threshold:
            if cc_lower <= self.CC <= cc_upper:
                self.GroupSymbol = group_symbol
                self.resultText = result_text_low if self.Gravel < 15 else result_text_high
            else:
                self.GroupSymbol = "SP"
                self.resultText = result_text_low if self.Gravel < 15 else result_text_high
        else:
            self.GroupSymbol = "SP"
            self.resultText = result_text_low if self.Gravel < 15 else result_text_high


    def add_row(self):
        row_position = self.table.rowCount()
        self.table.insertRow(row_position)
    
    def remove_last_row(self):
        last_row_index = self.table.rowCount() - 1
        if last_row_index >= 0:
            self.table.removeRow(last_row_index)
    
    def show_result_dialog(self,Symbol, resultText):
        if Symbol == "" or resultText == "":
            exit(1)
        custom_dialog = QDialog()
        custom_dialog.setWindowTitle("Result")

        layout = QVBoxLayout()
        labelSymbol = QLabel(Symbol)
        labelResult = QLabel(resultText)
        layout.addWidget(labelResult)
        layout.addWidget(labelSymbol)

        ok_button = QPushButton("ok")
        ok_button.clicked.connect(custom_dialog.accept)
        layout.addWidget(ok_button)

        custom_dialog.setLayout(layout)

        custom_dialog.exec_()

    def show_warning_dialog(self, message):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setWindowTitle("Warning")
        msg_box.setText(message)
        msg_box.exec_()
        
    def calculate_values(self):
        liquid_limit = self.get_limit_value(self.liquid_limit_input)
        plastic_limit = self.get_limit_value(self.plastic_limit_input)
        mass_retained = self.get_column_values_as_float(self.table, 2)
        if liquid_limit == None or plastic_limit == None or mass_retained == 0:
            self.show_warning_dialog("Please enter all required values")
            return
        self.symbol = self.find_symbol_for_point(liquid_limit, plastic_limit)
     
        percentage_retained = [x * 100 / sum(mass_retained) for x in mass_retained]
        cumulative_retained = [sum(percentage_retained[:y + 1]) for y, x in enumerate(percentage_retained)]
        finer = [100 - x for x in cumulative_retained]
        self.set_column_values(self.table, 3, percentage_retained)
        self.set_column_values(self.table, 4, cumulative_retained)
        self.set_column_values(self.table, 5, finer)
        
        sieveNumber = self.get_column_values_as_float(self.table, 0)
        four  = -1
        twoHundred = -1
        for j,i in enumerate(sieveNumber):
            if int(i) == 4:
                four =j
            if int(i) == 200:
                twoHundred = j
         
        if four == -1 or twoHundred == -1:
            self.show_warning_dialog("There are wrong values at Sieve Numbers (Where is #4 or #200)")
         
        self.Sand = finer[four] - finer[twoHundred]
        self.Gravel = 100 - finer[four]
        self.sand_percentage_label.setText(f"Sand Percentage: {self.Sand:.3f}%")
        self.gravel_percentage_label.setText(f"Gravel Percentage: {self.Gravel:.3f}%")

    def get_limit_value(self, limit_input):
        try:
            print(limit_input.text())
            return float(limit_input.text())
        except ValueError:
            return None

    def find_symbol_for_point(self, liquid_limit, plastic_limit):
        Plasttic_Index = liquid_limit - plastic_limit
        l = np.linspace(0, liquid_limit , 1000)
        for liquid_limit in l:
            AL = 0.73 * (liquid_limit - 20)
            UL = 0.90 * (liquid_limit - 8)
        
        if ((Plasttic_Index>=4 and Plasttic_Index <=7) and liquid_limit <= 35) and (Plasttic_Index < UL and Plasttic_Index >AL) :
            return "CL-ML"
        
        elif (Plasttic_Index <=4 and liquid_limit <= 35) and (Plasttic_Index < AL ) :
            return "ML"

        elif (Plasttic_Index >=7 and liquid_limit <= 35) and (Plasttic_Index < UL and Plasttic_Index >AL) :    
            return "CL"
        elif (liquid_limit > 35 and liquid_limit <= 50) and (Plasttic_Index < AL) :
            return "ML"
        elif (liquid_limit > 35 and liquid_limit <= 50) and (Plasttic_Index > AL and Plasttic_Index < UL) :  
            return "CL"
        elif (liquid_limit > 50 ) and (Plasttic_Index < AL) :
            return "MH"
        elif (liquid_limit > 50) and (Plasttic_Index > AL and Plasttic_Index < UL) :
            return "CH"
        else:
            return ""

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
            value = f"{value:.2f}"
            item = QTableWidgetItem(value)
            table.setItem(row, column_index, item)

    def plot_particle_size_distribution(self):
        particle_size = self.get_column_values_as_float(self.table, 1)
        finer = self.get_column_values_as_float(self.table, 5)

        plt.plot(particle_size, finer, marker='o', linestyle='-', color='b')
        plt.xlabel("Grain Size (mm)")
        plt.ylabel("% Finer")
        plt.title("Particle Size Distribution")
        plt.xlim(0.01, 100) 
        plt.ylim(0, 100)     
        plt.grid(True)  

        self.plot_reference_lines(finer)

        x60 = np.interp(60, np.flip(finer), np.flip(particle_size))
        x30 = np.interp(30, np.flip(finer), np.flip(particle_size))
        x10 = np.interp(10, np.flip(finer), np.flip(particle_size))

        self.plot_vertical_lines(x60, x30, x10)

        self.CU = (x60 / x10)
        self.CC = (x30 ** 2) / (x10 * x60)

        plt.show()

    def plot_reference_lines(self, finer):
        plt.axhline(y=60, color='r', linestyle='--')
        plt.axhline(y=30, color='g', linestyle='--')
        plt.axhline(y=10, color='b', linestyle='--')

    def plot_vertical_lines(self, x60, x30, x10):
        plt.axvline(x=x60, color='r', linestyle='--')
        plt.axvline(x=x30, color='g', linestyle='--')
        plt.axvline(x=x10, color='b', linestyle='--')


    



       

