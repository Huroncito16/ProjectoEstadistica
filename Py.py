import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QStackedWidget, QTableWidget, QTableWidgetItem, QFormLayout, QLineEdit, QFileDialog, QHeaderView, QSizePolicy)
from PyQt6.QtCharts import QChart, QChartView, QBarSeries, QBarSet, QBarCategoryAxis, QValueAxis
from PyQt6.QtGui import QPainter
from PyQt6.QtCore import Qt
import numpy as np
from scipy import stats
from datos import listas
from TablasIntervalos import generar_tabla_por_intervalos
import subprocess
import json

class FileSelector(QWidget):
    def __init__(self):
        super().__init__()
        self.ubicacion = None
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.file_input = QLineEdit(self)
        self.file_input.setPlaceholderText("src")
        layout.addWidget(self.file_input)

        browse_button = QPushButton("📂", self)
        browse_button.clicked.connect(self.open_file_dialog)
        layout.addWidget(browse_button)

        save_button = QPushButton("Guardar Dirección del Archivo", self)
        save_button.clicked.connect(self.save_file_location)
        layout.addWidget(save_button)

        self.setLayout(layout)

    def open_file_dialog(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Seleccionar Archivo", "", "Todos los Archivos (*.*)")
        if file_name:
            self.file_input.setText(file_name)
            self.ubicacion = file_name

    def save_file_location(self):
        if self.ubicacion:
            result = subprocess.run(['python', 'readExcel.py', self.ubicacion], capture_output=True, text=True)
            data = json.loads(result.stdout.strip())
            print(f"Datos procesados: {data}")
        else:
            print("No se ha seleccionado ningún archivo.")

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

    def create_summary_form(self):
        # Crear etiquetas y campos para el resumen estadístico
        self.media_label = QLabel("Media:")
        self.media_field = QLineEdit()
        self.media_field.setReadOnly(True)

        self.mediana_label = QLabel("Mediana:")
        self.mediana_field = QLineEdit()
        self.mediana_field.setReadOnly(True)

        self.moda_label = QLabel("Moda:")
        self.moda_field = QLineEdit()
        self.moda_field.setReadOnly(True)

        self.varianza_label = QLabel("Varianza:")
        self.varianza_field = QLineEdit()
        self.varianza_field.setReadOnly(True)

        self.desviacion_label = QLabel("Desviación Estándar:")
        self.desviacion_field = QLineEdit()
        self.desviacion_field.setReadOnly(True)

        self.curtosis_label = QLabel("Curtosis:")
        self.curtosis_field = QLineEdit()
        self.curtosis_field.setReadOnly(True)

        self.asimetria_label = QLabel("Asimetría:")
        self.asimetria_field = QLineEdit()
        self.asimetria_field.setReadOnly(True)

        # Agregar los elementos al layout
        self.form_layout.addRow(self.media_label, self.media_field)
        self.form_layout.addRow(self.mediana_label, self.mediana_field)
        self.form_layout.addRow(self.moda_label, self.moda_field)
        self.form_layout.addRow(self.varianza_label, self.varianza_field)
        self.form_layout.addRow(self.desviacion_label, self.desviacion_field)
        self.form_layout.addRow(self.curtosis_label, self.curtosis_field)
        self.form_layout.addRow(self.asimetria_label, self.asimetria_field)

    def show_summary(self):
        # Mostrar valores en el formulario de resumen
        self.media_field.setText(f"{self.data['media']:.2f}")
        self.mediana_field.setText(f"{self.data['mediana']:.2f}")
        self.moda_field.setText(", ".join(map(str, self.data['moda'])))
        self.varianza_field.setText(f"{self.data['varianza']:.2f}")
        self.desviacion_field.setText(f"{self.data['desviacion_estandar']:.2f}")
        self.curtosis_field.setText(f"{self.data['curtosis']:.2f}")
        self.asimetria_field.setText(f"{self.data['asimetria']:.2f}")

    def change_panel(self, index):
        self.stack.setCurrentIndex(index)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setWindowTitle("Estadística")
    window.setGeometry(100, 100, 800, 600)
    window.show()
    sys.exit(app.exec())