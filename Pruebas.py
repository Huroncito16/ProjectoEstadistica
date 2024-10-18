import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
from PyQt6.QtCore  import Qt
from PyQt6.QtWidgets import QApplication,QWidget,QVBoxLayout,QLabel,QLineEdit,QSlider

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class NormalDistributionPlot(QWidget):
    def __init__(self):
        super().__init__()

        # Create the figure and axes
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)

        # Create a vertical layout and add the canvas
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)

        # Add elements for modifying values
        self.mean_label = QLabel("Media:")
        self.mean_edit = QLineEdit("0")
        self.std_dev_label = QLabel("Desviación estándar:")
        self.std_dev_edit = QLineEdit("1")

        layout.addWidget(self.mean_label)
        layout.addWidget(self.mean_edit)
        layout.addWidget(self.std_dev_label)
        layout.addWidget(self.std_dev_edit)

        # Connect the elements with the update function
        self.mean_edit.textChanged.connect(self.update_plot)
        self.std_dev_edit.textChanged.connect(self.update_plot)

        self.setLayout(layout)

        # Get the axes
        self.ax = self.figure.add_subplot(111)

        # Initialize the plot
        self.update_plot()

    def update_plot(self):
        # Get the values from the elements
        try:
            mean = float(self.mean_edit.text())
            std_dev = float(self.std_dev_edit.text())
        except ValueError:
            # Handle invalid input (optional)
            print("Invalid input. Please enter numerical values.")
            return

        # Clear the axes
        self.ax.clear()

        # Create the data for the graph
        x = np.linspace(-4, 4, 1000)
        y = norm.pdf(x, mean, std_dev)

        # Plot the normal curve
        self.ax.plot(x, y)

        # Personalize the graph
        self.ax.set_title('Distribución Normal')
        self.ax.set_xlabel('Valores')
        self.ax.set_ylabel('Densidad de Probabilidad')

        # Update the graph
        self.canvas.draw()


if __name__ == '__main__':
    app = QApplication([])
    window = NormalDistributionPlot()
    window.show()
    app.exec()