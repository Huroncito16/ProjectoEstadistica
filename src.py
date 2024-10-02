import sys
from PyQt6.QtWidgets import (QHeaderView,QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QStackedWidget, QTableWidget, QTableWidgetItem, QFormLayout, QLineEdit, QFileDialog,QScrollArea, QSizePolicy)
    
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
        datos2 = [
                360, 372, 388, 404, 414, 428, 441, 452, 466, 483,
                360, 373, 389, 404, 415, 428, 441, 453, 467, 483,
                361, 374, 390, 404, 416, 429, 442, 455, 469, 485,
                361, 375, 390, 404, 416, 430, 443, 456, 469, 486,
                362, 376, 391, 405, 418, 432, 444, 456, 470, 486,
                363, 377, 392, 405, 419, 432, 444, 458, 471, 487,
                363, 378, 392, 405, 420, 433, 445, 458, 473, 487,
                364, 379, 393, 406, 420, 435, 446, 460, 473, 487,
                364, 380, 394, 406, 420, 435, 447, 460, 475, 488,
                365, 381, 395, 407, 421, 436, 447, 461, 475, 490,
                366, 382, 396, 407, 423, 436, 448, 462, 475, 491,
                367, 382, 398, 407, 423, 436, 448, 462, 478, 491,
                368, 382, 400, 408, 424, 436, 448, 463, 478, 492,
                369, 383, 401, 408, 424, 437, 449, 464, 479, 493,
                370, 384, 402, 409, 425, 438, 451, 464, 480, 493,
                370, 384, 402, 410, 426, 438, 451, 464, 480, 494,
                371, 385, 402, 412, 427, 439, 452, 465, 481, 495,
                372, 386, 403, 412, 428, 440, 452, 465, 482, 495]
        data = listas(datos)
        data2 = generar_tabla_por_intervalos(datos2)

        # Configurar el layout principal (horizontal)
        main_layout = QHBoxLayout()

        # Layout para los botones en el lado izquierdo
        button_layout = QVBoxLayout()
        self.buttons = {
            "Botón Lector": QPushButton("Lector de Archivos"),
            "Botón Tabla": QPushButton("Mostrar Tabla"),
            "Botón Tabla2": QPushButton("Mostrar Tabla Intervalos"),
            "Botón Formulario": QPushButton("Mostrar resumen"),
            "Botón Gráfico": QPushButton("Mostrar Gráfico de Barras")
        }

        for button in self.buttons.values():
            button_layout.addWidget(button)

        # Crear el panel derecho usando QStackedWidget para cambiar entre diferentes vistas
        self.stack = QStackedWidget()

        # Panel 2.2: Tabla
        self.table = QTableWidget(3, 3)  # Tabla con 3 filas y 3 columnas
        self.table.setRowCount(len(data['valores'])) 
        self.table.setColumnCount(14)
        headers = ["x", "f", "f%", "fa", "fa%", "fd", "fd%", "x", "d", "f|d|", "f*d", "fd^2", "fd^3", "fd^4"]
        self.table.setHorizontalHeaderLabels(headers)
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        
        cell_width = 60
        cell_height = 10
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        for i in range(14):
            self.table.setColumnWidth(i, cell_width)
            self.table.setFixedHeight(cell_height * len(datos))

        self.fill_table(data)

        #Panel 2.2: Tabla
        self.tablaIntervalos = QTableWidget(3, 3)  # Tabla con 3 filas y 3 columnas
        self.tablaIntervalos.setRowCount(len(data['valores'])) 
        self.tablaIntervalos.setColumnCount(15)
        headers = ["li", "ls", "xi", "frecuencia", "fr", "faPor", "fd", "fdPor", "dfPorXi", "d", "fPorAbsD", "fPorDD", "fPorDDD", "fPorDDDD"]
        self.tablaIntervalos.setHorizontalHeaderLabels(headers)
        self.tablaIntervalos.verticalHeader().setVisible(False)
        self.tablaIntervalos.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        
        
        self.tablaIntervalos.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        for i in range(14):
            self.tablaIntervalos.setColumnWidth(i, cell_width)
            self.tablaIntervalos.setFixedHeight(cell_height * len(datos2))

        self.fill_tableIntervalos(data2)
        

        # Panel 3: Resumen
        form_widget = QWidget()
        form_layout = QFormLayout()
        form_widget.setLayout(form_layout)

        # Panel 4: Gráfico de barras
        chart_view = self.create_bar_chart()

        # Panel 1: Lector de archivos
        self.file_selector = FileSelector()

        # Añadir los paneles al stack
        self.stack.addWidget(self.file_selector)
        self.stack.addWidget(self.scroll_area_table)  # Agregar tabla a la pila
        self.stack.addWidget(self.scrollIntervalos)  # Panel 1: Lector de archivos
        self.stack.addWidget(form_widget)  # Panel 3: Formulario
        self.stack.addWidget(chart_view)   # Panel 4: Gráfico de barras
        
        # Conectar los botones a las funciones para cambiar de panel
        self.buttons["Botón Lector"].clicked.connect(lambda: self.change_panel(0))
        self.buttons["Botón Tabla"].clicked.connect(lambda: self.change_panel(1))
        self.buttons["Botón Tabla2"].clicked.connect(lambda: self.change_panel(2))
        self.buttons["Botón Formulario"].clicked.connect(lambda: self.change_panel(3))
        self.buttons["Botón Gráfico"].clicked.connect(lambda: self.change_panel(4))
        

        # Añadir los layouts al layout principal
        main_layout.addLayout(button_layout)  # Añadir los botones al lado izquierdo
        main_layout.addWidget(self.stack)     # Añadir el área de visualización al lado derecho


        # Crear scroll areas para las tablas
        self.scroll_area_table = QScrollArea()
        self.scroll_area_table.setWidgetResizable(True)
        self.scroll_area_table.setWidget(self.table)

        self.scrollIntervalos = QScrollArea()
        self.scrollIntervalos.setWidgetResizable(True)
        self.scrollIntervalos.setWidget(self.tablaIntervalos)

        # Configurar el layout de la ventana
        self.setLayout(main_layout)
        self.setWindowTitle("Aplicación de Estadística")
        self.setGeometry(100, 100, 800, 600)

    def fill_table(self, data):
        valores = data['valores']

        for i, valor in enumerate(valores):
            self.table.setItem(i, 0, QTableWidgetItem(str(data['valores'][i])))
            self.table.setItem(i, 1, QTableWidgetItem(str(data['frecuencia_abs'][i])))
            self.table.setItem(i, 2, QTableWidgetItem(str(round(data['frecuencia_rel'][i], 2))))
            self.table.setItem(i, 3, QTableWidgetItem(str(data['frecuencia_acum'][i])))
            self.table.setItem(i, 4, QTableWidgetItem(str(round(data['frecuencia_acum_rel'][i], 2))))
            self.table.setItem(i, 5, QTableWidgetItem(str(data['frecuencia_desc'][i])))
            self.table.setItem(i, 6, QTableWidgetItem(str(round(data['frecuencia_desc_rel'][i], 2))))
            self.table.setItem(i, 7, QTableWidgetItem(str(round(data['frecuencia_abs_x'][i], 2))))
            self.table.setItem(i, 8, QTableWidgetItem(str(round(data['deltas'][i], 2))))
            self.table.setItem(i, 9, QTableWidgetItem(str(round(data['frecuencia_abs_delta_abs'][i], 2))))
            self.table.setItem(i, 10, QTableWidgetItem(str(round(data['frecuencia_abs_delta'][i], 2))))
            self.table.setItem(i, 11, QTableWidgetItem(str(round(data['frecuencia_abs_delta_cuadrado'][i], 2))))
            self.table.setItem(i, 12, QTableWidgetItem(str(round(data['frecuencia_abs_delta_cubo'][i], 2))))
            self.table.setItem(i, 13, QTableWidgetItem(str(round(data['frecuencia_abs_delta_cuarta'][i], 2))))
    
    def fill_tableIntervalos(self, data2):
       valores = data2['valores']

       for i, valor in enumerate(valores):
            self.tablaIntervalos.setItem(i, 0, QTableWidgetItem(str(data2['li'][i])))
            self.tablaIntervalos.setItem(i, 1, QTableWidgetItem(str(data2['ls'][i])))
            self.tablaIntervalos.setItem(i, 2, QTableWidgetItem(str(round(data2['xi'][i], 2))))
            self.tablaIntervalos.setItem(i, 3, QTableWidgetItem(str(data2['frecuencia'][i])))
            self.tablaIntervalos.setItem(i, 4, QTableWidgetItem(str(round(data2['fr'][i], 2))))
            self.tablaIntervalos.setItem(i, 5, QTableWidgetItem(str(data2['fa'][i])))
            self.tablaIntervalos.setItem(i, 6, QTableWidgetItem(str(round(data2['faPor'][i], 2))))
            self.tablaIntervalos.setItem(i, 7, QTableWidgetItem(str(round(data2['fd'][i], 2))))
            self.tablaIntervalos.setItem(i, 8, QTableWidgetItem(str(round(data2['fdPor'][i], 2))))
            self.tablaIntervalos.setItem(i, 9, QTableWidgetItem(str(round(data2['fPorXi'][i], 2))))
            self.tablaIntervalos.setItem(i, 10, QTableWidgetItem(str(round(data2['d'][i], 2))))
            self.tablaIntervalos.setItem(i, 11, QTableWidgetItem(str(round(data2['fPorAbsD'][i], 2))))
            self.tablaIntervalos.setItem(i, 12, QTableWidgetItem(str(round(data2['fPorDD'][i], 2))))
            self.tablaIntervalos.setItem(i, 13, QTableWidgetItem(str(round(data2['fPorDDD'][i], 2))))
            self.tablaIntervalos.setItem(i, 14, QTableWidgetItem(str(round(data2['fPorDDDD'][i], 2))))



    def change_panel(self, index):
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

        categories = ["x", "F", "Fa", "Fa%", "Fd", "Fd%","X","d", "f|d|", "f*d", "fd^2", "fd^3", "fd^4"]
        axisX = QBarCategoryAxis()
        axisX.append(categories)

        # Configurar el eje Y (valores numéricos)
        axisY = QValueAxis()
        axisY.setRange(0, 5)

        # Añadir los ejes al gráfico
        chart.addAxis(axisX, Qt.AlignmentFlag.AlignBottom)
        chart.addAxis(axisY, Qt.AlignmentFlag.AlignLeft)

        # Vincular la serie a los ejes
        series.attachAxis(axisX)
        series.attachAxis(axisY)

        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)

        return chart_view


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setWindowTitle("Estadística")
    window.setGeometry(100, 100, 800, 600)
    window.show()
    sys.exit(app.exec())