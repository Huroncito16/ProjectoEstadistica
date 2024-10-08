import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QStackedWidget
from PyQt6.QtGui import QIcon


class MenuWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Menú Principal")
        self.setGeometry(100, 100, 800, 400)
        self.setWindowIcon(QIcon("./img/logo.png"))

        # Layout principal
        layout = QVBoxLayout()

        # Botones para acceder a las otras ventanas
        self.button_window1 = QPushButton("Ir a Ventana 1")
        self.button_window2 = QPushButton("Ir a Ventana 2")

        # Conectar los botones con las funciones para abrir ventanas
        self.button_window1.clicked.connect(self.open_window1)
        self.button_window2.clicked.connect(self.open_window2)

        # Agregar los botones al layout
        layout.addWidget(self.button_window1)
        layout.addWidget(self.button_window2)

        self.setLayout(layout)

    def open_window1(self):
        self.window1 = Window1(self)
        self.window1.show()
        self.close()

    def open_window2(self):
        self.window2 = Window2(self)
        self.window2.show()
        self.close()


class Window1(QWidget):
    def __init__(self, previous_window):
        super().__init__()
        self.previous_window = previous_window
        self.setWindowTitle("Ventana 1")
        self.setGeometry(100, 100, 800, 400)
        self.setWindowIcon(QIcon("./img/logo.png"))

        # Layout principal
        layout = QHBoxLayout()

        # Botones para los paneles en Ventana 1
        Botones_layout = QVBoxLayout()
        self.buttons = {
            "Boton_LectorArchivos": QPushButton("Inicio"),
            "Boton_TablaSencillas": QPushButton("Tabla Sencillas"),
            "Boton_TablasIntervalos": QPushButton("Tablas Intervalos"),
            "Boton_ResumenEstadictico": QPushButton("Resumen Estadístico"),
            "Boton_Graficos": QPushButton("Gráficos"),
            "Boton_Regresar": QPushButton("Regresar")  # Botón para regresar al menú
        }

        for button in self.buttons.values():
            Botones_layout.addWidget(button)

        # Crear el QStackedWidget para los paneles
        self.stack = QStackedWidget()
        self.stack.addWidget(QLabel("Panel de Inicio"))
        self.stack.addWidget(QLabel("Panel de Tabla Sencilla"))
        self.stack.addWidget(QLabel("Panel de Tablas por Intervalos"))
        self.stack.addWidget(QLabel("Panel de Resumen Estadístico"))
        self.stack.addWidget(QLabel("Panel de Gráficos"))

        # Conectar botones para cambiar de panel
        self.buttons["Boton_LectorArchivos"].clicked.connect(lambda: self.change_panel(0))
        self.buttons["Boton_TablaSencillas"].clicked.connect(lambda: self.change_panel(1))
        self.buttons["Boton_TablasIntervalos"].clicked.connect(lambda: self.change_panel(2))
        self.buttons["Boton_ResumenEstadictico"].clicked.connect(lambda: self.change_panel(3))
        self.buttons["Boton_Graficos"].clicked.connect(lambda: self.change_panel(4))
        self.buttons["Boton_Regresar"].clicked.connect(self.regresar)

        # Agregar los layouts
        layout.addLayout(Botones_layout)
        layout.addWidget(self.stack)
        self.setLayout(layout)

    def change_panel(self, index):
        self.stack.setCurrentIndex(index)

    def regresar(self):
        self.previous_window.show()
        self.close()


class Window2(QWidget):
    def __init__(self, previous_window):
        super().__init__()
        self.previous_window = previous_window
        self.setWindowTitle("Ventana 2")
        self.setGeometry(100, 100, 800, 400)
        self.setWindowIcon(QIcon("./img/logo.png"))

        # Layout principal
        main_layout = QHBoxLayout()

        # Botones para los paneles de la segunda ventana
        Botones_layout = QVBoxLayout()
        self.buttons = {
            "Boton_Panel1": QPushButton("Panel 1"),
            "Boton_Panel2": QPushButton("Panel 2"),
            "Boton_Panel3": QPushButton("Panel 3"),
            "Boton_Regresar": QPushButton("Regresar")  # Botón para regresar al menú
        }

        for button in self.buttons.values():
            Botones_layout.addWidget(button)

        # Crear el QStackedWidget para los paneles de la segunda ventana
        self.stack = QStackedWidget()
        self.stack.addWidget(QLabel("Panel 1 de la segunda ventana"))
        self.stack.addWidget(QLabel("Panel 2 de la segunda ventana"))
        self.stack.addWidget(QLabel("Panel 3 de la segunda ventana"))

        # Conectar los botones para cambiar entre paneles
        self.buttons["Boton_Panel1"].clicked.connect(lambda: self.change_panel(0))
        self.buttons["Boton_Panel2"].clicked.connect(lambda: self.change_panel(1))
        self.buttons["Boton_Panel3"].clicked.connect(lambda: self.change_panel(2))
        self.buttons["Boton_Regresar"].clicked.connect(self.regresar)

        # Agregar los layouts
        main_layout.addLayout(Botones_layout)
        main_layout.addWidget(self.stack)
        self.setLayout(main_layout)

    def change_panel(self, index):
        self.stack.setCurrentIndex(index)

    def regresar(self):
        self.previous_window.show()
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    menu = MenuWindow()
    menu.show()
    sys.exit(app.exec())