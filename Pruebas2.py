import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton
import matplotlib.pyplot as plt
import networkx as nx

class DecisionTreeApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Árbol de Decisión Binario")
        self.setGeometry(100, 100, 800, 600)
        
        # Crear el widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Crear un layout
        layout = QVBoxLayout()
        self.plot_button = QPushButton("Generar y Visualizar Árbol")
        self.plot_button.clicked.connect(self.visualize_tree)
        
        layout.addWidget(self.plot_button)
        central_widget.setLayout(layout)

    def generate_tree(self, depth=3, current_depth=0, current_node='A'):
        if current_depth < depth:
            left_child = self.generate_tree(depth, current_depth + 1, 'A')
            right_child = self.generate_tree(depth, current_depth + 1, 'B')
            return (current_node, left_child, right_child)
        return current_node

    def plot_tree(self, tree, pos=None, level=0, x=0, y=0, layer_width=2):
        if pos is None:
            pos = {tree[0]: (x, y)}
        else:
            pos[tree[0]] = (x, y)

        # Calcula la posición para los nodos hijos
        if isinstance(tree[1], tuple):
            pos = self.plot_tree(tree[1], pos, level + 1, x - layer_width / (2 ** (level + 1)), y - 1, layer_width)
        if isinstance(tree[2], tuple):
            pos = self.plot_tree(tree[2], pos, level + 1, x + layer_width / (2 ** (level + 1)), y - 1, layer_width)

        return pos

    def visualize_tree(self):
        tree = self.generate_tree()
        pos = self.plot_tree(tree)
        
        # Crear un grafo
        G = nx.DiGraph()
        for node, (x, y) in pos.items():
            G.add_node(node, pos=(x, y))
            if isinstance(tree[1], tuple):
                G.add_edge(node, tree[1][0])
            if isinstance(tree[2], tuple):
                G.add_edge(node, tree[2][0])

        # Dibujar el árbol
        nx.draw(G, pos, with_labels=True, arrows=True, node_size=2000, node_color="lightblue", font_size=12, font_weight='bold')
        plt.title("Árbol de Decisión Binario")
        plt.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DecisionTreeApp()
    window.show()
    sys.exit(app.exec())