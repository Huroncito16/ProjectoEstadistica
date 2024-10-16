from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QComboBox, QPushButton, QDialog
)
import sys

# Ventana que calcula cuartiles, deciles y percentiles
class VentanaCalculos(QDialog):
    def __init__(self):
        super().__init__()

        # Configuración de la ventana
        self.setWindowTitle('Cálculo de Cuartiles, Deciles y Percentiles')
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

        # Sección para calcular Cuartiles
        cuartil_layout = QHBoxLayout()
        cuartil_label = QLabel('Cuartil:')
        self.cuartil_combo = QComboBox()
        self.cuartil_combo.addItems(['Seleccionar Cuartil', '1', '2', '3', '4'])
        cuartil_button = QPushButton('Calcular')
        cuartil_button.clicked.connect(self.calcular_cuartil)
        self.cuartil_resultado = QLabel('El resultado es:')
        cuartil_layout.addWidget(cuartil_label)
        cuartil_layout.addWidget(self.cuartil_combo)
        cuartil_layout.addWidget(cuartil_button)

        # Sección para calcular Deciles
        decil_layout = QHBoxLayout()
        decil_label = QLabel('Decil:')
        self.decil_combo = QComboBox()
        self.decil_combo.addItems(['Seleccionar Decil', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10'])
        decil_button = QPushButton('Calcular')
        decil_button.clicked.connect(self.calcular_decil)
        self.decil_resultado = QLabel('El resultado es:')
        decil_layout.addWidget(decil_label)
        decil_layout.addWidget(self.decil_combo)
        decil_layout.addWidget(decil_button)

        # Sección para calcular Percentiles
        percentil_layout = QHBoxLayout()
        percentil_label = QLabel('Percentil:')
        self.percentil_combo = QComboBox()
        self.percentil_combo.addItems([f'{i}' for i in range(1, 101)])
        percentil_button = QPushButton('Calcular')
        percentil_button.clicked.connect(self.calcular_percentil)
        self.percentil_resultado = QLabel('El resultado es:')
        percentil_layout.addWidget(percentil_label)
        percentil_layout.addWidget(self.percentil_combo)
        percentil_layout.addWidget(percentil_button)

        # Agregar layouts a la ventana principal
        layout.addLayout(cuartil_layout)
        layout.addWidget(self.cuartil_resultado)
        layout.addLayout(decil_layout)
        layout.addWidget(self.decil_resultado)
        layout.addLayout(percentil_layout)
        layout.addWidget(self.percentil_resultado)

        self.setLayout(layout)

    def calcular_cuartil(self):
        cuartil = self.cuartil_combo.currentText()
        if cuartil != 'Seleccionar Cuartil':
            resultado = f'Cuartil {cuartil} calculado'
            self.cuartil_resultado.setText(f'El resultado es: {resultado}')

    def calcular_decil(self):
        decil = self.decil_combo.currentText()
        if decil != 'Seleccionar Decil':
            resultado = f'Decil {decil} calculado'
            self.decil_resultado.setText(f'El resultado es: {resultado}')

    def calcular_percentil(self):
        percentil = self.percentil_combo.currentText()
        resultado = f'Percentil {percentil} calculado'
        self.percentil_resultado.setText(f'El resultado es: {resultado}')


# Ventana principal que tiene un botón para abrir la ventana de cálculos
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Configuración de la ventana principal
        self.setWindowTitle('Ventana Principal')
        self.setGeometry(100, 100, 400, 200)

        # Layout principal
        layout = QVBoxLayout()

        # Etiqueta de instrucción
        label = QLabel("Haz clic en el botón para calcular cuartiles, deciles y percentiles")

        # Botón para abrir la ventana de cálculos
        abrir_ventana_button = QPushButton('Abrir ventana de cálculos')
        abrir_ventana_button.clicked.connect(self.abrir_ventana_calculos)

        # Agregar widgets al layout
        layout.addWidget(label)
        layout.addWidget(abrir_ventana_button)

        # Configuración del contenedor principal
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def abrir_ventana_calculos(self):
        # Crear y mostrar la ventana de cálculos
        ventana_calculos = VentanaCalculos()
        ventana_calculos.exec()

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Crear la ventana principal
    main_window = MainWindow()
    main_window.show()

    sys.exit(app.exec())