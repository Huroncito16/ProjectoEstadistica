import sys
import math
import matplotlib.pyplot as plt
from PyQt6.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
    QStackedWidget, QGridLayout
)
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class Window2(QWidget):
    def __init__(self, previous_window):
        super().__init__()
        self.previous_window = previous_window
        self.setWindowTitle("Ventana 2")
        self.setMaximumSize(1000, 600)
        self.setMinimumSize(800, 400)
        self.setGeometry(100, 100, 800, 400)
        self.setWindowIcon(QIcon("./img/logo.png"))

        main_layout = QHBoxLayout()

        self.center_window()

        # Botones para los paneles
        botones_layout = QVBoxLayout()
        self.buttons = {
            "Boton_Panel1": QPushButton("Panel 1"),
            "Boton_Panel2": QPushButton("Panel 2"),
            "Boton_Panel3": QPushButton("Distribución Binomial"),
            "Boton_Panel4": QPushButton("Distribución de Poisson"),
            "Boton_Regresar": QPushButton("Regresar")
        }

        for button in self.buttons.values():
            botones_layout.addWidget(button)

        # Crear el QStackedWidget
        self.stack = QStackedWidget()
        self.stack.addWidget(QLabel("Contenido del Panel 1", alignment=Qt.AlignmentFlag.AlignCenter))
        self.stack.addWidget(QLabel("Contenido del Panel 2", alignment=Qt.AlignmentFlag.AlignCenter))

        # Panel 3: Distribución Binomial
        binomial_layout, self.binomial_input_fields, self.binomial_result_label, self.binomial_canvas = self.create_binomial_panel()
        panel_binomial = QWidget()
        panel_binomial.setLayout(binomial_layout)
        self.stack.addWidget(panel_binomial)

        # Panel 4: Distribución de Poisson
        poisson_layout, self.poisson_input_fields, self.poisson_result_label, self.poisson_canvas = self.create_poisson_panel()
        panel_poisson = QWidget()
        panel_poisson.setLayout(poisson_layout)
        self.stack.addWidget(panel_poisson)

        # Conectar los botones para cambiar entre paneles
        self.buttons["Boton_Panel1"].clicked.connect(lambda: self.change_panel(0))
        self.buttons["Boton_Panel2"].clicked.connect(lambda: self.change_panel(1))
        self.buttons["Boton_Panel3"].clicked.connect(lambda: self.change_panel(2))
        self.buttons["Boton_Panel4"].clicked.connect(lambda: self.change_panel(3))
        self.buttons["Boton_Regresar"].clicked.connect(self.regresar)

        # Agregar los layouts
        main_layout.addLayout(botones_layout)
        main_layout.addWidget(self.stack)
        self.setLayout(main_layout)

    def create_binomial_panel(self):
        layout = QGridLayout()

        # Etiquetas y campos de entrada
        layout.addWidget(QLabel("Ensayos (n):"), 0, 0)
        n_input = QLineEdit()
        layout.addWidget(n_input, 0, 1)

        layout.addWidget(QLabel("Éxitos (k):"), 1, 0)
        k_input = QLineEdit()
        layout.addWidget(k_input, 1, 1)

        layout.addWidget(QLabel("Probabilidad de éxito (p):"), 2, 0)
        p_input = QLineEdit()
        layout.addWidget(p_input, 2, 1)

        # Botón para calcular y limpiar
        calcular_btn = QPushButton("Calcular Binomial")
        layout.addWidget(calcular_btn, 3, 0, 1, 2)

        limpiar_btn = QPushButton("Limpiar")
        layout.addWidget(limpiar_btn, 4, 0, 1, 2)

        # Canvas para el gráfico
        canvas = FigureCanvas(plt.figure())
        layout.addWidget(canvas, 5, 0, 1, 2)

        # Etiqueta para mostrar resultados
        result_label = QLabel("")
        layout.addWidget(result_label, 6, 0, 1, 2)

        # Conectar el botón de calcular
        calcular_btn.clicked.connect(lambda: self.calcular_binomial(n_input, k_input, p_input, canvas, result_label))

        # Conectar el botón de limpiar
        limpiar_btn.clicked.connect(lambda: self.limpiar_campos([n_input, k_input, p_input], canvas, result_label))

        return layout, [n_input, k_input, p_input], result_label, canvas

    def create_poisson_panel(self):
        layout = QGridLayout()

        # Etiquetas y campos de entrada
        layout.addWidget(QLabel("Eventos (x):"), 0, 0)
        x_input = QLineEdit()
        layout.addWidget(x_input, 0, 1)

        layout.addWidget(QLabel("Media (λ):"), 1, 0)
        lambda_input = QLineEdit()
        layout.addWidget(lambda_input, 1, 1)

        # Botón para calcular y limpiar
        calcular_btn = QPushButton("Calcular Poisson")
        layout.addWidget(calcular_btn, 2, 0, 1, 2)

        limpiar_btn = QPushButton("Limpiar")
        layout.addWidget(limpiar_btn, 3, 0, 1, 2)

        # Canvas para el gráfico
        canvas = FigureCanvas(plt.figure())
        layout.addWidget(canvas, 4, 0, 1, 2)

        # Etiqueta para mostrar resultados
        result_label = QLabel("")
        layout.addWidget(result_label, 5, 0, 1, 2)

        # Conectar el botón de calcular
        calcular_btn.clicked.connect(lambda: self.calcular_poisson(x_input, lambda_input, canvas, result_label))

        # Conectar el botón de limpiar
        limpiar_btn.clicked.connect(lambda: self.limpiar_campos([x_input, lambda_input], canvas, result_label))

        return layout, [x_input, lambda_input], result_label, canvas

    def change_panel(self, index):
        self.stack.setCurrentIndex(index)

    def regresar(self):
        self.previous_window.show()
        self.close()

    def center_window(self):
        screen = QApplication.primaryScreen().geometry()
        window_geometry = self.frameGeometry()
        window_geometry.moveCenter(screen.center())
        self.move(window_geometry.topLeft())

    def calcular_binomial(self, n_input, k_input, p_input, canvas, result_label):
        try:
            n = int(n_input.text())
            k = int(k_input.text())
            p = float(p_input.text())

            if n < 0 or k < 0 or not (0 <= p <= 1):
                raise ValueError("Los valores deben ser positivos y 0 <= p <= 1")

            # Calcular el resultado
            result = self.distriBinomial(k, n, p, False)
            result_label.setText(f"Resultado Binomial: {result:.4f}")

            # Plotear el gráfico
            self.plot_binomial(n, k, p, canvas)

        except ValueError as ve:
            result_label.setText(str(ve))

    def calcular_poisson(self, x_input, lambda_input, canvas, result_label):
        try:
            x = int(x_input.text())
            lmbda = float(lambda_input.text())

            if x < 0 or lmbda < 0:
                raise ValueError("Los valores deben ser positivos")

            # Calcular el resultado
            result = self.distriPoisson(x, lmbda, False)
            result_label.setText(f"Resultado Poisson: {result:.4f}")

            # Plotear el gráfico
            self.plot_poisson(x, lmbda, canvas)

        except ValueError as ve:
            result_label.setText(str(ve))

    def distriBinomial(self, k, n, p, acumulado):
        comb = math.comb(n, k)
        pk = p ** k
        qN_K = (1 - p) ** (n - k)
        return comb * pk * qN_K

    def distriPoisson(self, x, media, acumulado):
        return (media ** x) * math.exp(-media) / math.factorial(x)

    def plot_binomial(self, n, k, p, canvas):
        plt.cla()
        x = range(0, n + 1)
        y = [self.distriBinomial(i, n, p, False) for i in x]
        plt.bar(x, y, color='blue')
        plt.title("Distribución Binomial")
        plt.xlabel("Número de Éxitos (k)")
        plt.ylabel("Probabilidad")
        canvas.draw()

    def plot_poisson(self, x, lmbda, canvas):
        plt.cla()
        x_values = range(0, x + 5)
        y_values = [self.distriPoisson(i, lmbda, False) for i in x_values]
        plt.bar(x_values, y_values, color='orange')
        plt.title("Distribución de Poisson")
        plt.xlabel("Eventos (x)")
        plt.ylabel("Probabilidad")
        canvas.draw()

    def limpiar_campos(self, inputs, canvas, result_label):
        for input_field in inputs:
            input_field.clear()
        result_label.clear()
        plt.cla()
        canvas.draw()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window2(previous_window=None)  # Cambia esto según tu implementación anterior
    window.show()
    sys.exit(app.exec())