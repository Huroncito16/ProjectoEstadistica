import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QLineEdit, QPushButton, QComboBox
from PyQt6.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from math import factorial as fac
import networkx as nx
import matplotlib.patches as patches

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

# Clase para crear una gráfica de árbol de combinaciones
class Grafica(FigureCanvas):
    def __init__(self, parent=None):
        fig, self.ax = Figure(figsize=(5, 4), dpi=100), None
        super().__init__(fig)
        self.setParent(parent)
        self.ax = fig.add_subplot(111)
        self.ax.set_title('Árbol de Combinaciones')

    def plot_tree(self, n, r):
        self.ax.clear()
        self.ax.set_title('Árbol de Combinaciones')

        # Crear el grafo con NetworkX
        G = nx.DiGraph()

        # Nodo raíz (inicial)
        root = f"Combinación (n={n}, r={r})"
        G.add_node(root)

        # Añadir nodos y conexiones (nodos hijos)
        for i in range(n):
            parent = f"C{i+1}"
            G.add_node(parent)
            G.add_edge(root, parent)

            # Añadir ramas adicionales
            for j in range(r):
                child = f"C{i+1},R{j+1}"
                G.add_node(child)
                G.add_edge(parent, child)

        # Generar el layout para el árbol
        pos = nx.spring_layout(G, seed=42)

        # Dibujar nodos y bordes
        nx.draw(G, pos, with_labels=True, ax=self.ax, node_size=2000, node_color="lightblue", font_size=10)

        # Dibujar nodos personalizados (óvalo y rectángulos)
        for node, (x, y) in pos.items():
            if node == root:
                # Nodo raíz como óvalo
                oval = patches.Ellipse((x, y), 0.2, 0.1, edgecolor='black', facecolor='none', lw=2)
                self.ax.add_patch(oval)
            else:
                # Otros nodos como rectángulos
                rect = patches.Rectangle((x-0.05, y-0.025), 0.1, 0.05, edgecolor='black', facecolor='none', lw=2)
                self.ax.add_patch(rect)

        # Refrescar el canvas
        self.ax.figure.canvas.draw()

# Aplicación PyQt6
class CombPermApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Configuración de la ventana
        self.setWindowTitle("Cálculo de Combinaciones y Permutaciones")
        self.setGeometry(100, 100, 600, 500)

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

        # Widget de la gráfica en forma de árbol
        self.grafica = Grafica(self)

        # Añadir widgets al layout
        layout.addWidget(self.combo)
        layout.addWidget(self.label_n)
        layout.addWidget(self.input_n)
        layout.addWidget(self.label_r)
        layout.addWidget(self.input_r)
        layout.addWidget(self.btn_calcular)
        layout.addWidget(self.resultado)
        layout.addWidget(self.grafica)

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
            self.resultado.setText(f"Resultado: {res:.2f}")

            # Generar el árbol de combinaciones
            self.grafica.plot_tree(n, r)
        except ValueError:
            self.resultado.setText("Por favor, ingresa valores válidos para n y r.")
        except ZeroDivisionError:
            self.resultado.setText("Error: No se puede dividir por cero.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ventana = CombPermApp()
    ventana.show()
    sys.exit(app.exec())