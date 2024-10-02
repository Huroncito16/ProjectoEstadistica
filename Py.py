import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QStackedWidget, QTableWidget, QTableWidgetItem, QFormLayout, QLineEdit, QFileDialog)
    
from PyQt6.QtCharts import QChart, QChartView, QBarSeries, QBarSet, QBarCategoryAxis, QValueAxis
from PyQt6.QtGui import QPainter
from PyQt6.QtCore import Qt

from datos import listas 
from TablasIntervalos import generar_tabla_por_intervalos
import subprocess
import json

class FileSelector(QWidget):
    def __init__(self):
        super().__init__()
        self.ubicacion = None  # Variable para almacenar la ubicación del archivo
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Campo de texto para mostrar la ubicación del archivo
        self.file_input = QLineEdit(self)
        self.file_input.setPlaceholderText("src")
        layout.addWidget(self.file_input)

        # Botón para abrir el diálogo de selección de archivo
        browse_button = QPushButton("📂", self)
        browse_button.clicked.connect(self.open_file_dialog)
        layout.addWidget(browse_button)

        # Botón para guardar la ubicación del archivo
        save_button = QPushButton("Guardar Dirección del Archivo", self)
        save_button.clicked.connect(self.save_file_location)
        layout.addWidget(save_button)

        self.setLayout(layout)

    def open_file_dialog(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Seleccionar Archivo", "", "Todos los Archivos (*.*)")
        if file_name:
            self.file_input.setText(file_name)
            self.ubicacion = file_name  # Guardar la ubicación del archivo en una variable


    def save_file_location(self):
        if self.ubicacion:
            # Ejecutar el script readExcel.py pasando la ruta del archivo
            result = subprocess.run(['python', 'readExcel.py', self.ubicacion], capture_output=True, text=True)
            
            # Obtener los datos procesados del script readExcel.py
            data = json.loads(result.stdout.strip())
            print(f"Datos procesados: {data}")
            
            # Aquí podrías hacer algo con los datos procesados si es necesario
        else:
            print("No se ha seleccionado ningún archivo.")


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        datos = [11, 9, 8, 7, 11, 6, 11, 11, 11, 8, 6, 9, 7, 10, 11, 5, 9, 7, 8, 6, 5, 9, 7, 5, 5, 6, 8, 8, 8, 9, 11, 8, 8, 8, 10, 10, 8, 9, 7, 9, 6, 7, 9, 9, 11, 10, 7, 10, 8, 11, 10, 5, 5, 5, 6, 10, 6, 6, 10, 7, 9, 9, 10, 8, 7, 6, 10, 7, 9, 7]
        data = listas(datos)
        data2 = generar_tabla_por_intervalos(datos)

        # Configurar el layout principal (horizontal)
        main_layout = QHBoxLayout()

        # Layout para los botones en el lado izquierdo
        button_layout = QVBoxLayout()
        self.buttons = {
            "Botón Lector": QPushButton("Lector de Archivos"),
            "Botón Tabla": QPushButton("Mostrar Tabla"),
            "Botón Formulario": QPushButton("Mostrar resumen"),
            "Botón Gráfico": QPushButton("Mostrar Gráfico de Barras")
        }

        for button in self.buttons.values():
            button_layout.addWidget(button)

        # Crear el panel derecho usando QStackedWidget para cambiar entre diferentes vistas
        self.stack = QStackedWidget()

        # Panel 2: Tabla
        self.tablaIntervalos = QTableWidget(3, 3)  # Tabla con 3 filas y 3 columnas
        self.tablaIntervalos.setRowCount(len(data['valores'])) 
        self.tablaIntervalos.setColumnCount(14)
        headers = ["x", "f", "f%", "fa", "fa%", "fd", "fd%", "x", "d", "f|d|", "f*d", "fd^2", "fd^3", "fd^4"]
        self.tablaIntervalos.setHorizontalHeaderLabels(headers)
        self.tablaIntervalos.verticalHeader().setVisible(False)
        self.tablaIntervalos.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        
        cell_width = 60
        cell_height = 10
        for i in range(14):
            self.tablaIntervalos.setColumnWidth(i, cell_width)
        self.tablaIntervalos.setFixedHeight(cell_height * len(datos))

        self.fill_table(data)

        # Panel 3: Resumen
        form_widget = QWidget()
        form_layout = QFormLayout()
        form_widget.setLayout(form_layout)

        # Panel 4: Gráfico de barras
        chart_view = self.create_bar_chart()

        # Panel 1: Lector de archivos
        self.file_selector = FileSelector()

        # Añadir los paneles al stack
        self.stack.addWidget(self.file_selector)  # Panel 1: Lector de archivos
        self.stack.addWidget(self.tablaIntervalos)        # Panel 2: Tabla
        self.stack.addWidget(form_widget)  # Panel 3: Formulario
        self.stack.addWidget(chart_view)   # Panel 4: Gráfico de barras
        
        # Conectar los botones a las funciones para cambiar de panel
        self.buttons["Botón Lector"].clicked.connect(lambda: self.change_panel(0))
        self.buttons["Botón Tabla"].clicked.connect(lambda: self.change_panel(1))
        self.buttons["Botón Formulario"].clicked.connect(lambda: self.change_panel(2))
        self.buttons["Botón Gráfico"].clicked.connect(lambda: self.change_panel(3))
        

        # Añadir los layouts al layout principal
        main_layout.addLayout(button_layout)  # Añadir los botones al lado izquierdo
        main_layout.addWidget(self.stack)     # Añadir el área de visualización al lado derecho

        # Configurar el layout de la ventana
        self.setLayout(main_layout)

    def fill_table(self, data):
        valores = data['valores']

        for i, valor in enumerate(valores):
            self.tablaIntervalos.setItem(i, 0, QTableWidgetItem(str(data['valores'][i])))
            self.tablaIntervalos.setItem(i, 1, QTableWidgetItem(str(data['frecuencia_abs'][i])))
            self.tablaIntervalos.setItem(i, 2, QTableWidgetItem(str(round(data['frecuencia_rel'][i], 2))))
            self.tablaIntervalos.setItem(i, 3, QTableWidgetItem(str(data['frecuencia_acum'][i])))
            self.tablaIntervalos.setItem(i, 4, QTableWidgetItem(str(round(data['frecuencia_acum_rel'][i], 2))))
            self.tablaIntervalos.setItem(i, 5, QTableWidgetItem(str(data['frecuencia_desc'][i])))
            self.tablaIntervalos.setItem(i, 6, QTableWidgetItem(str(round(data['frecuencia_desc_rel'][i], 2))))
            self.tablaIntervalos.setItem(i, 7, QTableWidgetItem(str(round(data['frecuencia_abs_x'][i], 2))))
            self.tablaIntervalos.setItem(i, 8, QTableWidgetItem(str(round(data['deltas'][i], 2))))
            self.tablaIntervalos.setItem(i, 9, QTableWidgetItem(str(round(data['frecuencia_abs_delta_abs'][i], 2))))
            self.tablaIntervalos.setItem(i, 10, QTableWidgetItem(str(round(data['frecuencia_abs_delta'][i], 2))))
            self.tablaIntervalos.setItem(i, 11, QTableWidgetItem(str(round(data['frecuencia_abs_delta_cuadrado'][i], 2))))
            self.tablaIntervalos.setItem(i, 12, QTableWidgetItem(str(round(data['frecuencia_abs_delta_cubo'][i], 2))))
            self.tablaIntervalos.setItem(i, 13, QTableWidgetItem(str(round(data['frecuencia_abs_delta_cuarta'][i], 2))))

    def change_panel(self, index):
        # Cambiar el panel visible en el stack
        self.stack.setCurrentIndex(index)

    def create_bar_chart(self):
         # Crear un gráfico de barras con datos de ejemplo
        set0 = QBarSet("2023")
        set0.append([1, 5, 3, 4, 5, 3,2, 3, 3, 4, 5, 3,5])

        series = QBarSeries()
        series.append(set0)

        chart = QChart()
        chart.addSeries(series)
        chart.setTitle("Gráfico de Barras de Ejemplo")
        chart.setAnimationOptions(QChart.AnimationOption.SeriesAnimations)

        categories = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]
        axisX = QBarCategoryAxis()
        axisX.append(categories)
        chart.addAxis(axisX, Qt.AlignmentFlag.AlignBottom)
        series.attachAxis(axisX)

        axisY = QValueAxis()
        axisY.setRange(0, 10)
        chart.addAxis(axisY, Qt.AlignmentFlag.AlignLeft)
        series.attachAxis(axisY)

        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignmentFlag.AlignBottom)

        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)

        return chart_view


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())