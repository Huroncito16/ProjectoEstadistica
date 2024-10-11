import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QStackedWidget, QTableWidget, QTableWidgetItem, QFormLayout, QLineEdit, QFileDialog, QHeaderView)
from PyQt6.QtCh import QChart, QChartView, QBarSeries, QBarSet, QBarCategoryAxis, QValueAxis
from PyQt6.QtGui import QPainter, QPixmap
from PyQt6.QtCore import Qt

from procesarDatos import listas 
from procesadorDatosIntervalos import generar_tabla_por_intervalos
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

        # datos = [360, 372, 388, 404, 414, 428, 441, 452, 466, 483]
        # datos2 = [360, 372, 388, 404, 414, 428, 441, 452, 466, 483]
        datos = [
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

        main_layout = QHBoxLayout()
# algo asi
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

        self.table = QTableWidget()
        self.setup_table(self.table, 14, data, headers=["x", "f", "f%", "fa", "fa%", "fd", "fd%", "x", "d", "f|d|", "f*d", "fd^2", "fd^3", "fd^4"])

        self.tablaIntervalos = QTableWidget()
        self.setup_table(self.tablaIntervalos, 15, data2, headers=["li", "ls", "xi", "frecuencia", "fr", "faPor", "fd", "fdPor", "dfPorXi", "d", "fPorAbsD", "fPorDD", "fPorDDD", "fPorDDDD"])

        form_widget = QWidget()
        form_layout = QFormLayout()
        form_widget.setLayout(form_layout)

        chart_view = self.create_bar_chart()

        self.file_selector = FileSelector()

        self.stack.addWidget(self.file_selector)
        self.stack.addWidget(self.table)
        self.stack.addWidget(self.tablaIntervalos)
        self.stack.addWidget(form_widget)
        self.stack.addWidget(chart_view)

        self.buttons["Botón Lector"].clicked.connect(lambda: self.change_panel(0))
        self.buttons["Botón Tabla"].clicked.connect(lambda: self.change_panel(1))
        self.buttons["Botón Tabla2"].clicked.connect(lambda: self.change_panel(2))
        self.buttons["Botón Formulario"].clicked.connect(lambda: self.change_panel(3))
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
        
        for i in range(len(data['valores'])):
            for j in range(column_count):
                table.setItem(i, j, QTableWidgetItem(str(data['valores'][i])))

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