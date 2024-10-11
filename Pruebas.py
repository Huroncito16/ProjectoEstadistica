import sys
import numpy as np
import matplotlib.pyplot as plt
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton

class GraficaEstadisticas(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Gráfica de Estadísticas")
        self.setGeometry(100, 100, 800, 600)
        
        # Crear un widget central y un layout
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Crear un botón para generar la gráfica
        self.btn_graficar = QPushButton("Generar Gráfica", self)
        self.btn_graficar.clicked.connect(self.generar_grafica)

        # Añadir el botón al layout
        self.layout.addWidget(self.btn_graficar)

    def generar_grafica(self):
        # Datos de ejemplo
        datos = {
            'rango': 5,
            'media': 10,
            'mediana': 8,
            'moda': 7,
            'varianza': 2,
            'desviacion_estandar': 1.4,
            'curtosis': 0.5,
            'asimetria': -0.2,
            'error_tipico': 0.5,
            'suma': 50,
            'cuenta': 10
        }

        # Crear la gráfica
        nombres = list(datos.keys())
        valores = list(datos.values())

        plt.figure(figsize=(10, 6))
        plt.bar(nombres, valores, color='cyan', edgecolor='black')
        plt.plot(nombres, valores, marker='o', color='blue')  # Línea de conexión
        plt.title("Estadísticas Descriptivas")
        plt.xlabel("Estadísticas")
        plt.ylabel("Valores")
        plt.grid(axis='y')

        # Mostrar la gráfica
        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = GraficaEstadisticas()
    ventana.show()
    sys.exit(app.exec())