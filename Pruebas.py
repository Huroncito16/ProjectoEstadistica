import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QLineEdit, QPushButton, QComboBox
from math import factorial as fac

# Funciones de combinaciones y permutaciones
def combSinRep(n, r):
    return fac(n) / (fac(r) * fac(n - r))

def combConRep(n, r):
    return fac(n + r - 1) / (fac(r) * fac(n - 1))

def perSinRep(n, r):
    return fac(n) / fac(n - r)

def perConRep(n, r):
    return n ** r

def perSinRepAll(n):
    return fac(n)

def perCir(n):
    return fac(n - 1)

# Aplicación PyQt6
class CombPermApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Configuración de la ventana
        self.setWindowTitle("Cálculo de Combinaciones y Permutaciones")
        self.setGeometry(100, 100, 400, 200)

        # Layout principal
        layout = QVBoxLayout()

        # Menú desplegable (ComboBox)
        self.combo = QComboBox(self)
        self.combo.addItem("Combinaciones sin repetición")
        self.combo.addItem("Combinaciones con repetición")
        self.combo.addItem("Permutaciones sin repetición")
        self.combo.addItem("Permutaciones con repetición")
        self.combo.addItem("Permutaciones sin repetición (n!)")
        self.combo.addItem("Permutaciones circulares")

        # Campo de texto para n
        self.label_n = QLabel("Valor de n:")
        self.input_n = QLineEdit(self)

        # Campo de texto para r
        self.label_r = QLabel("Valor de r:")
        self.input_r = QLineEdit(self)

        # Botón para calcular
        self.btn_calcular = QPushButton("Calcular", self)
        self.btn_calcular.clicked.connect(self.calcular)

        # Label para mostrar el resultado
        self.resultado = QLabel("Resultado: ")

        # Añadir widgets al layout
        layout.addWidget(self.combo)
        layout.addWidget(self.label_n)
        layout.addWidget(self.input_n)
        layout.addWidget(self.label_r)
        layout.addWidget(self.input_r)
        layout.addWidget(self.btn_calcular)
        layout.addWidget(self.resultado)

        # Establecer el layout
        self.setLayout(layout)

    def calcular(self):
        try:
            n = int(self.input_n.text())
            r = int(self.input_r.text())

            # Selección según el tipo de cálculo elegido
            tipo = self.combo.currentText()
            if tipo == "Combinaciones sin repetición":
                res = combSinRep(n, r)
            elif tipo == "Combinaciones con repetición":
                res = combConRep(n, r)
            elif tipo == "Permutaciones sin repetición":
                res = perSinRep(n, r)
            elif tipo == "Permutaciones con repetición":
                res = perConRep(n, r)
            elif tipo == "Permutaciones sin repetición (n!)":
                res = perSinRepAll(n)
            elif tipo == "Permutaciones circulares":
                res = perCir(n)

            # Mostrar el resultado
            self.resultado.setText(f"Resultado: {res}")
        except ValueError:
            self.resultado.setText("Por favor, ingresa valores válidos para n y r.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ventana = CombPermApp()
    ventana.show()
    sys.exit(app.exec())