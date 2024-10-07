import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QStackedWidget, QTableWidget, QTableWidgetItem, QFormLayout, QLineEdit, QFileDialog, QHeaderView, QSizePolicy)
from PyQt6.QtCharts import QChart, QChartView, QBarSeries, QBarSet, QBarCategoryAxis, QValueAxis
from PyQt6.QtGui import QPainter
from PyQt6.QtCore import Qt
import numpy as np
from scipy import stats
from procesarDatos import listas
from procesadorDatosIntervalos import generar_tabla_por_intervalos
import subprocess
import json



class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        datos = [360, 372, 388, 404, 414, 428, 441, 452, 466, 483]
        datos2 = [360, 372, 388, 404, 414, 428, 441, 452, 466, 483]
        self.data = listas(datos)  # Guardar data como atributo de la clase
        self.data2 = generar_tabla_por_intervalos(datos2)

        main_layout = QHBoxLayout()

        button_layout = QVBoxLayout()
        self.buttons = {
            "Botón Lector": QPushButton("Lector de Archivos"),
            "Botón Tabla": QPushButton("Mostrar Tabla"),
            "Botón Tabla2": QPushButton("Mostrar Tabla Intervalos"),
            "Botón Formulario": QPushButton("Mostrar Resumen"),
            "Botón Gráfico": QPushButton("Mostrar Gráfico de Barras")
        }

        # Configurar los botones para que se redimensionen automáticamente
        for button in self.buttons.values():
            button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            button_layout.addWidget(button)

        self.stack = QStackedWidget()

        self.table = QTableWidget()
        self.setup_table(self.table, 14, self.data, headers=["x", "f", "f%", "fa", "fa%", "fd", "fd%", "x", "d", "f|d|", "f*d", "fd^2", "fd^3", "fd^4"])

        self.tablaIntervalos = QTableWidget()
        self.setup_table(self.tablaIntervalos, 15, self.data2, headers=["li", "ls", "xi", "frecuencia", "fr", "faPor", "fd", "fdPor", "dfPorXi", "d", "fPorAbsD", "fPorDD", "fPorDDD", "fPorDDDD"])

        self.form_widget = QWidget()
        self.form_layout = QFormLayout()
        self.create_summary_form()  # Crear el formulario de resumen estadístico
        self.form_widget.setLayout(self.form_layout)

        chart_view = self.create_bar_chart()

        self.file_selector = FileSelector()

        self.stack.addWidget(self.file_selector)
        self.stack.addWidget(self.table)
        self.stack.addWidget(self.tablaIntervalos)
        self.stack.addWidget(self.form_widget)
        self.stack.addWidget(chart_view)

        # Conectar los botones a los diferentes paneles
        self.buttons["Botón Lector"].clicked.connect(lambda: self.change_panel(0))
        self.buttons["Botón Tabla"].clicked.connect(lambda: self.change_panel(1))
        self.buttons["Botón Tabla2"].clicked.connect(lambda: self.change_panel(2))
        self.buttons["Botón Formulario"].clicked.connect(self.show_summary)
        self.buttons["Botón Gráfico"].clicked.connect(lambda: self.change_panel(4))

        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.stack)

        self.setLayout(main_layout)

    def setup_table(self, table, column_count, data, headers):
        table.setRowCount(len(data['valores']))
        table.setColumnCount(column_count)
        table.setHorizontalHeaderLabels(headers)
        table.verticalHeader().setVisible(False)
        table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        table.setFixedHeight(400)  # Limitar la altura de la tabla
        table.setFixedWidth(600)   # Limitar el ancho de la tabla
        
        valores = data['valores']
        for i, valores in enumerate(valores):
            table.setItem(i, 0, QTableWidgetItem(str(data['valores'][i])))
            table.setItem(i, 1, QTableWidgetItem(str(data['frecuencia_abs'][i])))
            table.setItem(i, 2, QTableWidgetItem(str(round(data['frecuencia_rel'][i], 2))))
            table.setItem(i, 3, QTableWidgetItem(str(data['frecuencia_acum'][i])))
            table.setItem(i, 4, QTableWidgetItem(str(round(data['frecuencia_acum_rel'][i], 2))))
            table.setItem(i, 5, QTableWidgetItem(str(data['frecuencia_desc'][i])))
            table.setItem(i, 6, QTableWidgetItem(str(round(data['frecuencia_desc_rel'][i], 2))))
            table.setItem(i, 7, QTableWidgetItem(str(round(data['frecuencia_abs_x'][i], 2))))
            table.setItem(i, 8, QTableWidgetItem(str(round(data['deltas'][i], 2))))
            table.setItem(i, 9, QTableWidgetItem(str(round(data['frecuencia_abs_delta_abs'][i], 2))))
            table.setItem(i, 10, QTableWidgetItem(str(round(data['frecuencia_abs_delta'][i], 2))))
            table.setItem(i, 11, QTableWidgetItem(str(round(data['frecuencia_abs_delta_cuadrado'][i], 2))))
            table.setItem(i, 12, QTableWidgetItem(str(round(data['frecuencia_abs_delta_cubo'][i], 2))))
            table.setItem(i, 13, QTableWidgetItem(str(round(data['frecuencia_abs_delta_cuarta'][i], 2))))
        

    
        

    def change_panel(self, index):
        self.stack.setCurrentIndex(index)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setWindowTitle("Estadística")
    window.setGeometry(100, 100, 800, 600)
    window.show()
    sys.exit(app.exec())