from datetime import date
import sys
from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem, QLineEdit, QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFileDialog, QStackedWidget
from PyQt6.QtGui import QIcon, QPixmap, QGuiApplication
from readExcel import leerDatos
from procesarDatos import listas

class FileSelector(QWidget):
    def __init__(self):
        super().__init__()
        self.file_path = None

    def open_file_dialog(self):
        # Abrir diálogo de archivos solo para archivos Excel (.xlsx, .xls)
        file_dialog = QFileDialog(self)
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        file_dialog.setNameFilter("Archivos Excel (*.xlsx *.xls)")
        if file_dialog.exec():
            file_paths = file_dialog.selectedFiles()
            self.file_path = file_paths[0]
            return self.file_path
        return None




















class MenuWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Menú Principal")
        self.setGeometry(100, 100, 800, 500)
        self.setMinimumSize(800, 500)
        self.setMaximumSize(850, 550)
        self.setWindowIcon(QIcon("./img/logo.png"))
        self.center_window()

        layout = QVBoxLayout()
        image = QLabel(self)
        pixmap = QPixmap("./img/banner1.jpg")
        image.setPixmap(pixmap)     
        layout.addWidget(image)

        self.button_window1 = QPushButton("Ir a Ventana 1")
        self.button_window2 = QPushButton("Ir a Ventana 2")

        self.button_window1.clicked.connect(self.open_window1)
        self.button_window2.clicked.connect(self.open_window2)

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

    def center_window(self):
        screen = QGuiApplication.primaryScreen().geometry()
        window_geometry = self.frameGeometry()

        center_point = screen.center()
        window_geometry.moveCenter(center_point)

        self.move(window_geometry.topLeft())




























class Window1(QWidget):
    def __init__(self, previous_window):
        super().__init__()
        self.previous_window = previous_window
        self.setWindowTitle("Ventana 1")
        self.setGeometry(100, 100, 800, 500)
        self.setMaximumSize(1000, 500)
        self.setMinimumSize(800, 500)
        self.setWindowIcon(QIcon("./img/logo.png"))
        self.center_window()

        self.saved_file_path = None  # Inicializar aquí para evitar el error

        layout = QHBoxLayout()

        self.file_selector = FileSelector()

        self.file_label = QLabel("Selecciona un archivo para leer")
        self.file_textfield = QLineEdit()  # Campo de texto para mostrar la dirección del archivo
        file_dialog_panel = QWidget()
        file_dialog_layout = QVBoxLayout()

        file_dialog_button = QPushButton("Seleccionar Archivo")
        file_dialog_button.clicked.connect(self.open_and_display_file)

        guardar_button = QPushButton("Guardar")  # Botón para guardar la dirección
        guardar_button.clicked.connect(self.guardar_direccion)

        file_dialog_layout.addWidget(self.file_label)
        file_dialog_layout.addWidget(self.file_textfield)
        file_dialog_layout.addWidget(file_dialog_button)
        file_dialog_layout.addWidget(guardar_button)
        file_dialog_panel.setLayout(file_dialog_layout)

        # Botones para los paneles en Ventana 
        Botones_layout = QVBoxLayout()
        self.buttons = {
            "Boton_LectorArchivos": QPushButton("Inicio"),
            "Boton_TablaSencillas": QPushButton("Tabla Sencillas"),
            "Boton_TablasIntervalos": QPushButton("Tablas Intervalos"),
            "Boton_ResumenEstadictico": QPushButton("Resumen Estadístico"),
            "Boton_Graficos": QPushButton("Gráficos"),
            "Boton_Regresar": QPushButton("Regresar")
        }

        for button in self.buttons.values():
            Botones_layout.addWidget(button)

        # Crear el QStackedWidget para los paneles
        self.stack = QStackedWidget()
        self.stack.addWidget(file_dialog_panel)
        self.stack.addWidget(self.crear_tabla_sencilla())
        self.stack.addWidget(QLabel("Panel de Tablas por Intervalos"))
        self.stack.addWidget(QLabel("Panel de Resumen Estadístico"))
        self.stack.addWidget(QLabel("Panel de Gráficos"))


        self.buttons["Boton_LectorArchivos"].clicked.connect(lambda: self.change_panel(0))
        self.buttons["Boton_TablaSencillas"].clicked.connect(lambda: self.change_panel(1))
        self.buttons["Boton_TablasIntervalos"].clicked.connect(lambda: self.change_panel(2))
        self.buttons["Boton_ResumenEstadictico"].clicked.connect(lambda: self.change_panel(3))
        self.buttons["Boton_Graficos"].clicked.connect(lambda: self.change_panel(4))
        self.buttons["Boton_Regresar"].clicked.connect(self.regresar)

        layout.addLayout(Botones_layout)
        layout.addWidget(self.stack)
        self.setLayout(layout)


    def open_and_display_file(self):
        file_path = self.file_selector.open_file_dialog()
        if file_path:
            self.file_textfield.setText(file_path)

    def guardar_direccion(self):
        self.saved_file_path = self.file_textfield.text()
        print(f"Dirección guardada: {self.saved_file_path}")
        
        if self.saved_file_path:
            datos = leerDatos(self.saved_file_path)
            print("leido perce XD")

    def crear_tabla_sencilla(self):
        tabla_panel = QWidget()
        tabla_layout = QVBoxLayout()

        self.table_widget = QTableWidget()  
        self.table_widget.setColumnCount(13)
        self.table_widget.setRowCount(1)

        

        self.table_widget.setHorizontalHeaderLabels([
            "x", "f", "fr%", "Fa", "Fa%", "Fd", "Fd%", 
            "f*x", "d", "f*|d|", "f*d^2", "f*d^3", "f*d^4"
        ])

        actualizar_button = QPushButton("Actualizar Tabla")
        actualizar_button.clicked.connect(self.actualizar_tabla_sencilla)
        
        self.totales_label = QLabel("Totales: ") 
        tabla_layout.addWidget(self.totales_label)
        
        tabla_layout.addWidget(self.table_widget)
        tabla_layout.addWidget(actualizar_button)
        tabla_panel.setLayout(tabla_layout)

        return tabla_panel

    def actualizar_tabla_sencilla(self):
        if self.saved_file_path:
            datos = leerDatos(self.saved_file_path)
            data = listas(datos)
            valores = data['valores']

            self.table_widget.setRowCount(len(valores))

            self.table_widget.setColumnWidth(0, 20)
            self.table_widget.setColumnWidth(1, 20)
            self.table_widget.setColumnWidth(2, 20)
            self.table_widget.setColumnWidth(3, 20)
            self.table_widget.setColumnWidth(4, 20)
            self.table_widget.setColumnWidth(5, 20)
            self.table_widget.setColumnWidth(6, 20)
            self.table_widget.setColumnWidth(7, 30)
            self.table_widget.setColumnWidth(8, 30)
            self.table_widget.setColumnWidth(9, 40)
            self.table_widget.setColumnWidth(10, 60)
            self.table_widget.setColumnWidth(11, 60)
            self.table_widget.setColumnWidth(12, 70)
            self.table_widget.setColumnWidth(13, 70)

            for i, valor in enumerate(valores):
                self.table_widget.setItem(i, 0, QTableWidgetItem(str(data['valores'][i])))
                self.table_widget.setItem(i, 1, QTableWidgetItem(str(data['frecuencia_abs'][i])))
                self.table_widget.setItem(i, 2, QTableWidgetItem(str(round(data['frecuencia_rel'][i], 2))))
                self.table_widget.setItem(i, 3, QTableWidgetItem(str(data['frecuencia_acum'][i])))
                self.table_widget.setItem(i, 4, QTableWidgetItem(str(round(data['frecuencia_acum_rel'][i], 2))))
                self.table_widget.setItem(i, 5, QTableWidgetItem(str(data['frecuencia_desc'][i])))
                self.table_widget.setItem(i, 6, QTableWidgetItem(str(round(data['frecuencia_desc_rel'][i], 2))))
                self.table_widget.setItem(i, 7, QTableWidgetItem(str(round(data['frecuencia_abs_x'][i], 2))))
                self.table_widget.setItem(i, 8, QTableWidgetItem(str(round(data['deltas'][i], 2))))
                self.table_widget.setItem(i, 9, QTableWidgetItem(str(round(data['frecuencia_abs_delta_abs'][i], 2))))
                self.table_widget.setItem(i, 10, QTableWidgetItem(str(round(data['frecuencia_abs_delta'][i], 2))))
                self.table_widget.setItem(i, 11, QTableWidgetItem(str(round(data['frecuencia_abs_delta_cuadrado'][i], 2))))
                self.table_widget.setItem(i, 12, QTableWidgetItem(str(round(data['frecuencia_abs_delta_cubo'][i], 2))))
                self.table_widget.setItem(i, 13, QTableWidgetItem(str(round(data['frecuencia_abs_delta_cuarta'][i], 2))))

            # Calcular los totales
            total_f = sum(data['frecuencia_abs'])
            total_f_rel = sum(data['frecuencia_rel'])
            total_abs_delta = sum(data['frecuencia_abs_delta_abs'])
            total_delta = sum(data['deltas'])
            total_delta_cuadrado = sum(data['frecuencia_abs_delta_cuadrado'])
            total_delta_cubo = sum(data['frecuencia_abs_delta_cubo'])
            total_delta_cuarta = sum(data['frecuencia_abs_delta_cuarta'])

            # Mostrar los totales en el QLabel
            self.totales_label.setText(
                f"Total: {total_f}   f_rel:  {total_f_rel},      abs_delta={total_abs_delta}, "
                f"delta={total_delta}, delta_cuadrado={total_delta_cuadrado}, "
                f"delta_cubo={total_delta_cubo}, delta_cuarta={total_delta_cuarta}"
            )


    def change_panel(self, index):
        self.stack.setCurrentIndex(index)

    def regresar(self):
        self.previous_window.show()
        self.close()

    def center_window(self):
        screen = QGuiApplication.primaryScreen().geometry()
        window_geometry = self.frameGeometry()

        center_point = screen.center()
        window_geometry.moveCenter(center_point)

        self.move(window_geometry.topLeft())















































class Window2(QWidget):
    def __init__(self, previous_window):
        super().__init__()
        self.previous_window = previous_window
        self.setWindowTitle("Ventana 2")
        self.setMaximumSize(1000, 600)
        self.setMinimumSize(800, 400)
        self.setGeometry(100, 100, 800, 400)
        self.setWindowIcon(QIcon("./img/logo.png"))

        # Layout principal
        main_layout = QHBoxLayout()

        self.center_window()

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
    
    def center_window(self):
        screen = QGuiApplication.primaryScreen().geometry()
        window_geometry = self.frameGeometry()

        center_point = screen.center()
        window_geometry.moveCenter(center_point)

        self.move(window_geometry.topLeft())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    menu = MenuWindow()
    menu.show()
    sys.exit(app.exec())