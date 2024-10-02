import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFileDialog, QLineEdit, QTableWidget, QTableWidgetItem, QGridLayout
)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
import subprocess
import json


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.ubicacion = None  # Variable para almacenar la ubicación del archivo
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Ventana Principal")
        self.setGeometry(100, 100, 800, 500)
        self.move(QApplication.primaryScreen().geometry().center() - self.rect().center())
        self.setFixedSize(self.size())

        # Layout principal
        main_layout = QHBoxLayout()

    
        # Sección derecha
        right_layout = QVBoxLayout()

        # Imagen del banner
        banner_label = QLabel(self)
        pixmap = QPixmap("./img/banner.jpg")  # Cambia esta ruta a la ubicación de tu imagen
        banner_label.setPixmap(pixmap)
        banner_label.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        right_layout.addWidget(banner_label)

        # Reducir espacio entre el banner y el explorador de archivos
        right_layout.addSpacing(10)

        # Explorador de archivos
        file_layout = QHBoxLayout()
        self.file_input = QLineEdit(self)
        self.file_input.setPlaceholderText("src")
        browse_button = QPushButton(self)
        browse_button.setText("📂")
        browse_button.clicked.connect(self.open_file_dialog)
        file_layout.addWidget(QLabel("src: "))
        file_layout.addWidget(self.file_input)
        file_layout.addWidget(browse_button)
        right_layout.addLayout(file_layout)

        # Botón para guardar la ubicación del archivo
        next_window_button = QPushButton("Guardar Dirección del Archivo")
        next_window_button.clicked.connect(self.save_file_location)
        right_layout.addWidget(next_window_button)

        # Añadir layouts al layout principal
        main_layout.addLayout(right_layout)

        self.setLayout(main_layout)

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
            
            # Abrir la ventana de análisis de datos con los datos procesados
            self.data_analysis_window = DataAnalysisWindow(self.ubicacion, data)
            self.data_analysis_window.show()
        else:
            print("No se ha seleccionado ningún archivo.")

    def open_data_analysis_window(self):
        if self.ubicacion:
            # Ejecutar el script readExcel.py pasando la ruta del archivo
            result = subprocess.run(['python', 'readExcel.py', self.ubicacion], capture_output=True, text=True)
            
            # Obtener los datos procesados del script readExcel.py
            data = json.loads(result.stdout.strip())
            print(f"Datos procesados: {data}")
            
            # Abrir la ventana de análisis de datos con los datos procesados
            self.data_analysis_window = DataAnalysisWindow(self.ubicacion, data)
            self.data_analysis_window.show()
        else:
            print("No se ha seleccionado ningún archivo.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec())
