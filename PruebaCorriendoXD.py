import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QStackedWidget, QTableWidget, QTableWidgetItem, QFormLayout, QLineEdit, QFileDialog, QHeaderView)
from PyQt6.QtCharts import QChart, QChartView, QBarSeries, QBarSet, QBarCategoryAxis, QValueAxis
from PyQt6.QtGui import QPainter, QPixmap
from PyQt6.QtCore import Qt

from procesarDatos import listas 
from procesadorDatosIntervalos import generar_tabla_por_intervalos
import subprocess
import json

    
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        datos = [360, 372, 388, 404, 414, 428, 441, 452, 466, 483]
        datos2 = [360, 372, 388, 404, 414, 428, 441, 452, 466, 483]
        

        main_layout = QHBoxLayout()

        button_layout = QVBoxLayout()
        self.buttons = {
            "Botón Lector": QPushButton("Lector de Archivos"),
            "Botón Tabla": QPushButton("Mostrar Tabla"),
            "Botón Tabla2": QPushButton("Mostrar Tabla Intervalos"),
            "Botón Formulario": QPushButton("Mostrar Resumen"),
            "Botón Gráfico": QPushButton("Mostrar Gráfico de Barras")
        }

        for button in self.buttons.values():
            button_layout.addWidget(button)

        self.stack = QStackedWidget()

        
        form_widget = QWidget()
        form_layout = QFormLayout()
        form_widget.setLayout(form_layout)

               

        self.stack.addWidget(QLabel("hola"))
        self.stack.addWidget(QLabel("hola"))
        self.stack.addWidget(QLabel("hola"))
        self.stack.addWidget(QLabel("hola"))
        self.stack.addWidget(self.create_bar_chart)

        self.buttons["Botón Lector"].clicked.connect(lambda: self.change_panel(0))
        self.buttons["Botón Tabla"].clicked.connect(lambda: self.change_panel(1))
        self.buttons["Botón Tabla2"].clicked.connect(lambda: self.change_panel(2))
        self.buttons["Botón Formulario"].clicked.connect(lambda: self.change_panel(3))
        self.buttons["Botón Gráfico"].clicked.connect(lambda: self.change_panel(4))

        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.stack)

        self.setLayout(main_layout)

    

    def create_bar_chart(self):
        series = QBarSeries()
        bar_set = QBarSet("Datos")
        bar_set.append([1, 2, 3, 4, 5])
        series.append(bar_set)

        chart = QChart()

        
        chart.addSeries(series)
        chart.setTitle("Gráfico de Barras")
        chart.setAnimationOptions(QChart.AnimationOption.SeriesAnimations)

        axisX = QBarCategoryAxis()
        axisX.append(["A", "B", "C", "D", "E"])
        chart.addAxis(axisX, Qt.AlignmentFlag.AlignBottom)
        series.attachAxis(axisX)

        axisY = QValueAxis()
        axisY.setRange(0, 10)
        chart.addAxis(axisY, Qt.AlignmentFlag.AlignLeft)
        series.attachAxis(axisY)

        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)

        return chart_view

    def change_panel(self, index):
        self.stack.setCurrentIndex(index)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())