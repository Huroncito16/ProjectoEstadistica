from datetime import date
import sys
from PyQt6.QtWidgets import QScrollArea, QSizePolicy, QTableWidget, QTableWidgetItem, QLineEdit, QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFileDialog, QStackedWidget
from PyQt6.QtGui import QIcon, QPixmap, QGuiApplication
from PyQt6.QtCore import Qt
from readExcel import leerDatos
from procesarDatos import listas
from procesadorDatosIntervalos import generar_tabla_por_intervalos

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
        try:
            self.window1 = Window1(self)
            self.window1.show()
            self.close()
        except Exception as e:
            print(f"Ocurrió un error: {e}")

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
        self.setMaximumSize(900, 600)
        self.setMinimumSize(900, 600)
        self.setWindowIcon(QIcon("./img/logo.png"))
        self.center_window()

        self.saved_file_path = None 

        layout = QHBoxLayout()

        self.file_selector = FileSelector()

        self.file_label = QLabel("Selecciona un archivo para leer")
        self.file_textfield = QLineEdit()
        file_dialog_panel = QWidget()
        file_dialog_layout = QVBoxLayout()

        file_dialog_button = QPushButton("Seleccionar Archivo")
        file_dialog_button.clicked.connect(self.open_and_display_file)

        guardar_button = QPushButton("Guardar")
        guardar_button.clicked.connect(self.guardar_direccion)

        file_dialog_layout.addWidget(self.file_label)
        file_dialog_layout.addWidget(self.file_textfield)
        file_dialog_layout.addWidget(file_dialog_button)
        file_dialog_layout.addWidget(guardar_button)
        file_dialog_panel.setLayout(file_dialog_layout)

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

        self.stack = QStackedWidget()
        self.stack.addWidget(file_dialog_panel)
        self.stack.addWidget(self.crear_tabla_sencilla())
        self.stack.addWidget(self.crear_Intervalos())
        self.stack.addWidget(self.Resumen())
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
        self.table_resul = QTableWidget() 

        self.table_widget.verticalHeader().setVisible(False)
        self.table_resul.verticalHeader().setVisible(False)
        self.table_widget.setColumnCount(13)
        self.table_widget.setRowCount(1)
        self.table_widget.setHorizontalHeaderLabels([
            "x", "f", "fr%", "Fa", "Fa%", "Fd", "Fd%", 
            "f*x", "d", "f*|d|", "f*d^2", "f*d^3", "f*d^4"
        ])
        
        actualizar_button = QPushButton("Actualizar Tabla")
        actualizar_button.clicked.connect(self.actualizar_tabla_sencilla)
             
        tabla_layout.addWidget(self.table_widget)
        tabla_layout.addWidget(self.table_resul)
        tabla_layout.addWidget(actualizar_button)
        tabla_panel.setLayout(tabla_layout)

        return tabla_panel

    def actualizar_tabla_sencilla(self):
        if self.saved_file_path:
            datos = leerDatos(self.saved_file_path)
            data = listas(datos)
            valores = data['valores']

            self.table_widget.setRowCount(len(valores))

            for col in range(14):
                if col < 7:
                    self.table_widget.setColumnWidth(col, 40)
                else:
                    self.table_widget.setColumnWidth(col, 70)

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

            total_f = sum(data['frecuencia_abs'])
            total_f_rel = sum(data['frecuencia_rel'])
            total_abs_delta = sum(data['frecuencia_abs_delta_abs'])
            total_delta = sum(data['deltas'])
            total_delta_cuadrado = sum(data['frecuencia_abs_delta_cuadrado'])
            total_delta_cubo = sum(data['frecuencia_abs_delta_cubo'])
            total_delta_cuarta = sum(data['frecuencia_abs_delta_cuarta'])

            self.table_resul.setRowCount(1)
            self.table_resul.setColumnCount(13)
            self.table_resul.verticalHeader().hide()
            self.table_resul.horizontalHeader().hide()
            self.table_resul.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
            self.table_resul.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

            
            self.table_resul.setFixedHeight(self.table_resul.verticalHeader().defaultSectionSize())

            for col in range(12):
                if col < 7:
                    self.table_resul.setColumnWidth(col, 40)
                else:
                    self.table_resul.setColumnWidth(col, 70)
                if col == 13:
                    self.table_resul.setColumnWidth(col, 80)

            self.table_resul.setItem(0, 0, QTableWidgetItem("Totales"))
            self.table_resul.setItem(0, 1, QTableWidgetItem(str(total_f)))
            self.table_resul.setItem(0, 2, QTableWidgetItem(str(round(total_f_rel, 2))))
            self.table_resul.setItem(0, 3, QTableWidgetItem(" "))
            self.table_resul.setItem(0, 4, QTableWidgetItem(" "))
            self.table_resul.setItem(0, 5, QTableWidgetItem(" "))
            self.table_resul.setItem(0, 6, QTableWidgetItem(" "))
            self.table_resul.setItem(0, 7, QTableWidgetItem(" "))
            self.table_resul.setItem(0, 8, QTableWidgetItem(str(round(total_delta, 2))))
            self.table_resul.setItem(0, 9, QTableWidgetItem(str(round(total_abs_delta, 2))))
            self.table_resul.setItem(0, 10, QTableWidgetItem(str(round(total_delta_cuadrado, 2))))
            self.table_resul.setItem(0, 11, QTableWidgetItem(str(round(total_delta_cubo, 2))))
            self.table_resul.setItem(0, 12, QTableWidgetItem(str(round(total_delta_cuarta, 2))))

    def crear_Intervalos(self):
        intervalos = QWidget()
        Layout_inter = QVBoxLayout()

        self.table_resul_inter = QTableWidget()
        self.table_Inter = QTableWidget()  
       
        self.table_Inter.verticalHeader().setVisible(False)
        self.table_Inter.setColumnCount(14)
        self.table_Inter.setRowCount(1)
        self.table_Inter.setHorizontalHeaderLabels([
            "li","ls","xi","Frecuencia","Fr","Fa","Fa%","Fd","Fd%", 
            "f*Xi","d","f*|d|","f*d^2","f*d^3","f*d^4"
        ])
      
       
        actualizar_button = QPushButton("Actualizar Tabla")
        actualizar_button.clicked.connect(self.actualizar_intervalo)
        
                
        Layout_inter.addWidget(self.table_Inter)
        Layout_inter.addWidget(self.table_resul_inter)
        Layout_inter.addWidget(actualizar_button)
        intervalos.setLayout(Layout_inter)

        return intervalos

    def actualizar_intervalo(self):
        if self.saved_file_path:
            datos = leerDatos(self.saved_file_path)
            data = generar_tabla_por_intervalos(datos)
            valor = data['valor']

            self.table_Inter.setRowCount(len(valor))

            for col in range(15):
                if col < 7:
                    self.table_Inter.setColumnWidth(col, 60)
                else:
                    self.table_Inter.setColumnWidth(col, 80)

            for i, valor in enumerate(valor):
                self.table_Inter.setItem(i, 0, QTableWidgetItem(str(data['valor'][i])))
                self.table_Inter.setItem(i, 1, QTableWidgetItem(str(data['li'][i])))
                self.table_Inter.setItem(i, 2, QTableWidgetItem(str(round(data['ls'][i], 2))))
                self.table_Inter.setItem(i, 3, QTableWidgetItem(str(data['xi'][i])))
                self.table_Inter.setItem(i, 4, QTableWidgetItem(str(round(data['frecuencia'][i], 2))))
                self.table_Inter.setItem(i, 5, QTableWidgetItem(str(data['fr'][i])))
                self.table_Inter.setItem(i, 6, QTableWidgetItem(str(round(data['fa'][i], 2))))
                self.table_Inter.setItem(i, 7, QTableWidgetItem(str(round(data['faPor'][i], 2))))
                self.table_Inter.setItem(i, 8, QTableWidgetItem(str(round(data['fd'][i], 2))))
                self.table_Inter.setItem(i, 9, QTableWidgetItem(str(round(data['fdPor'][i], 2))))
                self.table_Inter.setItem(i, 10, QTableWidgetItem(str(round(data['fPorXi'][i], 2))))
                self.table_Inter.setItem(i, 11, QTableWidgetItem(str(round(data['d'][i], 2))))
                self.table_Inter.setItem(i, 12, QTableWidgetItem(str(round(data['fPorAbsD'][i], 2))))
                self.table_Inter.setItem(i, 13, QTableWidgetItem(str(round(data['fPorDD'][i], 2))))
                self.table_Inter.setItem(i, 13, QTableWidgetItem(str(round(data['fPorDDD'][i], 2))))
                self.table_Inter.setItem(i, 13, QTableWidgetItem(str(round(data['fPorDDDD'][i], 2))))

                
                total_frecuencia = sum(data['frecuencia'])
                total_fr = sum(data['fr'])
                total_fPorAbsD = sum(data['fPorAbsD'])
                total_fPorDD = sum(data['fPorDD'])
                total_fPorDDD = sum(data['fPorDDD'])
                total_fPorDDDD = sum(data['fPorDDDD'])

                self.table_resul_inter.setRowCount(1)
                self.table_resul_inter.setColumnCount(7)
                self.table_resul_inter.setHorizontalHeaderLabels([
                    " ","Frecuencia","Fr","f*|d|","f*d^2","f*d^3","f*d^4"
                ])
                self.table_resul_inter.verticalHeader().hide()
                self.table_resul_inter.horizontalHeader().show()
                self.table_resul_inter.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

                self.table_resul_inter.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
                self.table_resul_inter.setMaximumSize(800, 70)
                

                for col in range(7):
                    self.table_resul_inter.setColumnWidth(col, 80)
                                                                    
                self.table_resul_inter.setItem(0, 0, QTableWidgetItem("Totales"))
                self.table_resul_inter.setItem(0, 1, QTableWidgetItem(str(total_frecuencia)))
                self.table_resul_inter.setItem(0, 2, QTableWidgetItem(str(total_fr)))
                self.table_resul_inter.setItem(0, 3, QTableWidgetItem(str(total_fPorAbsD)))
                self.table_resul_inter.setItem(0, 4, QTableWidgetItem(str(total_fPorDD)))
                self.table_resul_inter.setItem(0, 5, QTableWidgetItem(str(total_fPorDDD)))
                self.table_resul_inter.setItem(0, 6, QTableWidgetItem(str(total_fPorDDDD)))
                
    def Resumen(self):
        panel_resul = QWidget()
        layout = QVBoxLayout()
        layout_Horizontal = QHBoxLayout()
        panel_label_1 = QVBoxLayout()
        panel_label = QVBoxLayout()

        img = QVBoxLayout()
        image = QLabel(self)
        pixmap = QPixmap("./img/Banner_resumen.jpg")
        image.setPixmap(pixmap)
        img.addWidget(image)

        if self.saved_file_path:
            datos = leerDatos(self.saved_file_path)
            resultados = listas(datos)
        else:
            resultados = {
                'valor_minimo': 0,
                'valor_maximo': 0,
                'rango': 0,
                'media': 0,
                'mediana': 0,
                'moda': 0,
                'varianza': 0,
                'desviacion_estandar': 0,
                'curtosis': 0,
                'asimetria': 0,
                'error_tipico': 0,
                'suma': 0,
                'cuenta': 0
            }

        self.field_data = [
            ("Valor mínimo:", resultados['valor_minimo']),
            ("Valor máximo:", resultados['valor_maximo']),
            ("Rango:", resultados['rango']),
            ("Media:", resultados['media']),
            ("Mediana:", resultados['mediana']),
            ("Moda:", resultados['moda']),
            ("Varianza:", resultados['varianza']),
            ("Desviación estándar:", resultados['desviacion_estandar']),
            ("Curtosis:", resultados['curtosis']),
            ("Asimetría:", resultados['asimetria']),
            ("Error típico:", resultados['error_tipico']),
            ("Suma:", resultados['suma']),
            ("Cuenta:", resultados['cuenta'])
        ]

        self.text_fields = []

        for label_text, _ in self.field_data:
            label = QLabel(label_text)
            panel_label_1.addWidget(label)

        for _, field_value in self.field_data:
            text_field = QLineEdit()
            text_field.setText(str(field_value))
            self.text_fields.append(text_field)
            panel_label.addWidget(text_field)

        self.update_button = QPushButton("Actualizar")
        self.update_button.clicked.connect(lambda: self.actualizar_valores())

        layout_Horizontal.addLayout(panel_label_1)
        layout_Horizontal.addLayout(panel_label)

        layout.addLayout(img)
        layout.addLayout(layout_Horizontal)
        layout.addWidget(self.update_button)

        panel_resul.setLayout(layout)

        return panel_resul

    def actualizar_valores(self):
        if self.saved_file_path:
            datos = leerDatos(self.saved_file_path)
            resultados = listas(datos)
            
            nuevos_valores = [
                resultados['valor_minimo'], resultados['valor_maximo'], resultados['rango'], 
                resultados['media'], resultados['mediana'], resultados['moda'], resultados['varianza'], 
                resultados['desviacion_estandar'], resultados['curtosis'], resultados['asimetria'], 
                resultados['error_tipico'], resultados['suma'], resultados['cuenta']
            ]
            
            for i, new_value in enumerate(nuevos_valores):
                self.text_fields[i].setText(str(new_value))
        
    
        
    
    

        
        

    
        
     













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