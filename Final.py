import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QStackedWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
)
from PyQt6.QtGui import QIcon


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Proyecto - Estadística")
        self.setGeometry(100, 100, 800, 400)
        self.setWindowIcon(QIcon("./img/logo.png"))

        # Layout principal
        main_layout = QHBoxLayout()

        # Layout para los botones
        Botones_layout = QVBoxLayout()
        self.buttons = {
            "Boton_LectorArchivos": QPushButton("Inicio"),
            "Boton_TablaSencillas": QPushButton("Tabla Sencillas"),
            "Boton_TablasIntervalos": QPushButton("Tablas Intervalos"),
            "Boton_ResumenEstadictico": QPushButton("Resumen Estadístico"),
            "Boton_Graficos": QPushButton("Gráficos"),
            "Boton_MasFunciones": QPushButton("Más Funciones...")
        }

        for button in self.buttons.values():
            Botones_layout.addWidget(button)

        # Crear el QStackedWidget para cambiar entre los diferentes paneles
        self.stack = QStackedWidget()

        # Crear paneles vacíos
        self.Inicio = QLabel("Panel de Inicio")
        self.TablaSencilla = QLabel("Panel de Tabla Sencilla")
        self.Tablaintervalos = QLabel("Panel de Tablas por Intervalos")
        self.Resumen = QLabel("Panel de Resumen Estadístico")
        self.Graficos = QLabel("Panel de Gráficos")
        self.more = QLabel("Panel de Más Funciones")

        # Añadir los paneles al stack
        self.stack.addWidget(self.Inicio)
        self.stack.addWidget(self.TablaSencilla)
        self.stack.addWidget(self.Tablaintervalos)
        self.stack.addWidget(self.Resumen)
        self.stack.addWidget(self.Graficos)
        self.stack.addWidget(self.more)

        # Conectar los botones con los cambios de panel
        self.buttons["Boton_LectorArchivos"].clicked.connect(lambda: self.change_panel(0))
        self.buttons["Boton_TablaSencillas"].clicked.connect(lambda: self.change_panel(1))
        self.buttons["Boton_TablasIntervalos"].clicked.connect(lambda: self.change_panel(2))
        self.buttons["Boton_ResumenEstadictico"].clicked.connect(lambda: self.change_panel(3))
        self.buttons["Boton_Graficos"].clicked.connect(lambda: self.change_panel(4))
        self.buttons["Boton_MasFunciones"].clicked.connect(self.open_new_window)

        # Agregar los layouts al layout principal
        main_layout.addLayout(Botones_layout)
        main_layout.addWidget(self.stack)

        # Establecer el layout principal
        self.setLayout(main_layout)

    def change_panel(self, index):
        """Cambiar entre los diferentes paneles."""
        self.stack.setCurrentIndex(index)

    def open_new_window(self):
        """Abrir una nueva ventana y cerrar la actual."""
        self.new_window = SecondWindow(self)
        self.new_window.show()
        self.close()


class SecondWindow(QWidget):
    def __init__(self, previous_window):
        super().__init__()
        self.previous_window = previous_window
        self.setWindowTitle("Más Funciones")
        self.setGeometry(100, 100, 800, 400)
        self.setWindowIcon(QIcon("./img/logo.png"))

        # Layout principal
        main_layout = QHBoxLayout()

        # Layout para los botones
        Botones_layout = QVBoxLayout()
        self.buttons = {
            "Boton_Panel1": QPushButton("Panel 1"),
            "Boton_Panel2": QPushButton("Panel 2"),
            "Boton_Panel3": QPushButton("Panel 3"),
            "Boton_Regresar": QPushButton("Regresar")
        }

        for button in self.buttons.values():
            Botones_layout.addWidget(button)

        # Crear el QStackedWidget para cambiar entre los diferentes paneles
        self.stack = QStackedWidget()

        # Crear paneles vacíos para la segunda ventana
        self.Panel1 = QLabel("Panel 1 de la segunda ventana")
        self.Panel2 = QLabel("Panel 2 de la segunda ventana")
        self.Panel3 = QLabel("Panel 3 de la segunda ventana")

        # Añadir los paneles al stack
        self.stack.addWidget(self.Panel1)
        self.stack.addWidget(self.Panel2)
        self.stack.addWidget(self.Panel3)

        # Conectar los botones con los cambios de panel
        self.buttons["Boton_Panel1"].clicked.connect(lambda: self.change_panel(0))
        self.buttons["Boton_Panel2"].clicked.connect(lambda: self.change_panel(1))
        self.buttons["Boton_Panel3"].clicked.connect(lambda: self.change_panel(2))
        self.buttons["Boton_Regresar"].clicked.connect(self.regresar)

        # Agregar los layouts al layout principal
        main_layout.addLayout(Botones_layout)
        main_layout.addWidget(self.stack)

        # Establecer el layout principal
        self.setLayout(main_layout)

    def change_panel(self, index):
        self.stack.setCurrentIndex(index)

    def regresar(self):
        self.previous_window.show()
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec())