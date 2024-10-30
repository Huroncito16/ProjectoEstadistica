from datetime import date
import sys
from PyQt6.QtWidgets import QDialog, QComboBox, QScrollArea, QSizePolicy, QTableWidget, QTableWidgetItem, QLineEdit, QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFileDialog, QStackedWidget
from PyQt6.QtCharts import QLineSeries, QChart, QChartView, QBarSeries, QBarSet, QBarCategoryAxis, QValueAxis
from PyQt6.QtGui import QPainter, QIcon, QPixmap, QGuiApplication, QBrush, QColor, QFont
from PyQt6.QtCore import Qt, QFile, QIODevice, QTextStream


import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm, poisson, binom
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from readExcel import leerDatos
from procesarDatos import listas
from procesadorDatosIntervalos import generar_tabla_por_intervalos
from distriBinomialPoisson import distriBinomial, distriPoison, distriNormal
from analiCombi import combConRep, combSinRep, perCir, perConRep, perSinRep, perSinRepAll

class FileSelector(QWidget):
    def __init__(self):
        super().__init__()
        self.file_path = None

    def open_file_dialog(self):
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

        pixmap = QPixmap("./img/banner3.jpg")
        self.image_label = QLabel(self)
        scaled_pixmap = pixmap.scaled(self.image_label.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self.image_label.setPixmap(scaled_pixmap)
        layout = QVBoxLayout()

        self.button_window1 = QPushButton("Analisis Estadisticos")
        self.button_window2 = QPushButton("Combinaciones y Distrubuciones")
        self.button_cerrar = QPushButton("salir")

        self.button_window1.clicked.connect(self.open_window1)
        self.button_window2.clicked.connect(self.open_window2)
        self.button_cerrar.clicked.connect(self.close)

        layout.addWidget(self.image_label)
        layout.addWidget(self.button_window1)
        layout.addWidget(self.button_window2)
        layout.addWidget(self.button_cerrar)

        self.setLayout(layout)

        self.apply_stylesheet()
    
        self.image_label.resizeEvent = self.resize_image

    def resize_image(self, event):
        pixmap = QPixmap("./img/banner3.jpg")
        scaled_pixmap = pixmap.scaled(self.image_label.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self.image_label.setPixmap(scaled_pixmap)

    def open_window1(self):
        try:
            self.window1 = Window1(self)
            self.window1.show()
            self.close()
        except Exception as e:
            print(f"Ocurrió un error: {e}")

    def open_window2(self):
        try:
            self.window2 = Window2(self)
            self.window2.show()
            self.close()
        except Exception as e:
            print(f"Ocurrió un error: {e}")

    def close(self):
        return super().close()

    def center_window(self):
        screen = QGuiApplication.primaryScreen().geometry()
        window_geometry = self.frameGeometry()

        center_point = screen.center()
        window_geometry.moveCenter(center_point)

        self.move(window_geometry.topLeft())

    def apply_stylesheet(self):
        qss_file = QFile("style.qss")
        if qss_file.open(QIODevice.OpenModeFlag.ReadOnly | QIODevice.OpenModeFlag.Text):
            stream = QTextStream(qss_file)
            self.setStyleSheet(stream.readAll())
    
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

       
        self.file_textfield = QLineEdit()
        file_dialog_panel = QWidget()
        file_dialog_layout = QVBoxLayout()

        banner_layout = QHBoxLayout()
        banner = QLabel()
        pixmap = QPixmap("./img/banner2.jpg")
        banner.setPixmap(pixmap.scaled(800, 600))
        banner_layout.addWidget(banner)

        file_dialog_button = QPushButton("Seleccionar Archivo")
        file_dialog_button.clicked.connect(self.open_and_display_file)

        guardar_button = QPushButton("Guardar")
        guardar_button.clicked.connect(self.guardar_direccion)

        file_dialog_layout.addLayout(banner_layout)
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
        self.stack.addWidget(self.crear_Grafico())

        self.buttons["Boton_LectorArchivos"].clicked.connect(lambda: self.change_panel(0))
        self.buttons["Boton_TablaSencillas"].clicked.connect(lambda: self.change_panel(1))
        self.buttons["Boton_TablasIntervalos"].clicked.connect(lambda: self.change_panel(2))
        self.buttons["Boton_ResumenEstadictico"].clicked.connect(lambda: self.change_panel(3))
        self.buttons["Boton_Graficos"].clicked.connect(lambda: self.change_panel(4))
        self.buttons["Boton_Regresar"].clicked.connect(self.regresar)

        self.apply_stylesheet()

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
            print("leido parcero XD")

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
        abrir_ventana_button = QPushButton('Calcular Cuartiles, Deciles y Percentiles')
        abrir_ventana_button.clicked.connect(self.abrir_ventana_calculos)
             
        tabla_layout.addWidget(self.table_widget)
        tabla_layout.addWidget(self.table_resul)
        tabla_layout.addWidget(actualizar_button)
        tabla_layout.addWidget(abrir_ventana_button)
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
        abrir_ventana_button = QPushButton('Calcular Cuartiles, Deciles y Percentiles')
        abrir_ventana_button.clicked.connect(self.abrir_ventana_calculos)
        
                
        Layout_inter.addWidget(self.table_Inter)
        Layout_inter.addWidget(self.table_resul_inter)
        Layout_inter.addWidget(abrir_ventana_button)
        Layout_inter.addWidget(actualizar_button)
        intervalos.setLayout(Layout_inter)

        return intervalos
    
    def abrir_ventana_calculos(self):
        datos_inter = self.table_Inter
        ventana_calculos = VentanaCalculos(datos_inter)
        ventana_calculos.exec()

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

        panel_label_col1 = QVBoxLayout()
        panel_text_col1 = QVBoxLayout()
        panel_label_col2 = QVBoxLayout()
        panel_text_col2 = QVBoxLayout()

        img = QVBoxLayout()
        image = QLabel(self)
        pixmap = QPixmap("./img/banner_delgado.jpg")
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

        # Distribuye los labels y QLineEdits en dos columnas
        for i, (label_text, field_value) in enumerate(self.field_data):
            label = QLabel(label_text)
            text_field = QLineEdit()
            text_field.setText(str(field_value))
            self.text_fields.append(text_field)

            if i < len(self.field_data) // 2:
                panel_label_col1.addWidget(label)
                panel_text_col1.addWidget(text_field)
            else:
                panel_label_col2.addWidget(label)
                panel_text_col2.addWidget(text_field)

        self.update_button = QPushButton("Actualizar")
        self.update_button.clicked.connect(self.actualizar_valores)

        # Agrega los layouts de columnas al layout horizontal
        layout_Horizontal.addLayout(panel_label_col1)
        layout_Horizontal.addLayout(panel_text_col1)
        layout_Horizontal.addLayout(panel_label_col2)
        layout_Horizontal.addLayout(panel_text_col2)

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
        
    def crear_Grafico(self):
        rango = 0
        media = 0
        mediana = 0
        moda = 0
        varianza = 0
        desviacion_estandar = 0
        curtosis = 0
        asimetria = 0
        error_tipico = 0
        cuenta = 0

        panel = QWidget()
        layout = QVBoxLayout()

        self.series = QBarSeries()
        self.bar_set = QBarSet("Pato")
        self.bar_set.setBrush(QBrush(QColor("#2b0063"))) 
        self.bar_set.append([rango, media, mediana, moda, varianza, desviacion_estandar, curtosis, asimetria, error_tipico, cuenta])
        self.series.append(self.bar_set)

        chart = QChart()
        chart.addSeries(self.series)
        chart.setTitle("Gráfico de Barras con Línea Conectada")
        chart.setBackgroundBrush(QBrush(QColor("#1b1b1b"))) 
        chart.setTitleFont(QFont("Arial", 16, QFont.Weight.Bold))
        chart.setTitleBrush(QBrush(QColor("#fff")))

        axisX = QBarCategoryAxis()
        axisX.append(["Rango", "Media", "Mediana", "Moda", "Varianza", "Desviación Est.", "Curtosis", "Asimetría", "Error Típico", "Cuenta"])
        axisX.setLabelsFont(QFont("Arial", 8, QFont.Weight.Bold))
        axisX.setLabelsBrush(QBrush(QColor("#ffffff")))
        chart.addAxis(axisX, Qt.AlignmentFlag.AlignBottom)
        self.series.attachAxis(axisX)

        axisY = QValueAxis()
        axisY.setRange(0, 1600)
        axisY.setLabelsFont(QFont("Arial", 8, QFont.Weight.Bold))
        axisY.setLabelsBrush(QBrush(QColor("#ffffff")))
        chart.addAxis(axisY, Qt.AlignmentFlag.AlignLeft)
        self.series.attachAxis(axisY)

        self.line_series = QLineSeries()
        self.line_series.setColor(QColor("#6100e0"))
        for i, value in enumerate([rango, media, mediana, moda, varianza, desviacion_estandar, curtosis, asimetria, error_tipico, cuenta]):
            self.line_series.append(i, value)
        chart.addSeries(self.line_series)
        self.line_series.attachAxis(axisX)
        self.line_series.attachAxis(axisY)

        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)

        actualizar_btn = QPushButton("Actualizar Tabla")
        actualizar_btn.clicked.connect(self.actualizar_Grafica)

        layout.addWidget(chart_view)
        layout.addWidget(actualizar_btn)
        panel.setLayout(layout)

        return panel
       
    def actualizar_Grafica(self):
        if self.saved_file_path:
            datos = leerDatos(self.saved_file_path)
            dat = listas(datos)

            rango = dat.get('rango', 0)
            media = dat.get('media', 0)
            mediana = dat.get('mediana', 0)
            moda = dat.get('moda', [0])
            if isinstance(moda, list):
                moda = moda[0]
            varianza = dat.get('varianza', 0)
            desviacion_estandar = dat.get('desviacion_estandar', 0)
            curtosis = dat.get('curtosis', 0)
            asimetria = dat.get('asimetria', 0)
            error_tipico = dat.get('error_tipico', 0)
            cuenta = dat.get('cuenta', 0)

            nuevos_valores = [rango, media, mediana, moda, varianza,
                            desviacion_estandar, curtosis, asimetria,
                            error_tipico, cuenta]

            for index, valor in enumerate(nuevos_valores):
                if isinstance(valor, (int, float)):
                    self.bar_set.replace(index, valor)
                else:
                    print(f"Advertencia: Valor no numérico en la posición {index}: {valor}")

            self.line_series.clear()
            for index, valor in enumerate(nuevos_valores):
                if isinstance(valor, (int, float)):
                    self.line_series.append(index, valor)

            self.series.chart().update()
         
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

    def apply_stylesheet(self):
        qss_file = QFile("style.qss")
        if qss_file.open(QIODevice.OpenModeFlag.ReadOnly | QIODevice.OpenModeFlag.Text):
            stream = QTextStream(qss_file)
            self.setStyleSheet(stream.readAll())

class VentanaCalculos(QDialog):
    def __init__(self, datos_inter):
        super().__init__()

        self.setWindowTitle('Cálculo de Cuartiles, Deciles y Percentiles')
        self.setGeometry(100, 100, 400, 300)
        self.center_window()

        layout = QVBoxLayout()

        self.datos_inter = datos_inter
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

        boton_regresar = QPushButton("Cerrar")
        boton_regresar.clicked.connect(self.close)

        layout.addLayout(cuartil_layout)
        layout.addWidget(self.cuartil_resultado)
        layout.addLayout(decil_layout)
        layout.addWidget(self.decil_resultado)
        layout.addLayout(percentil_layout)
        layout.addWidget(self.percentil_resultado)
        layout.addWidget(boton_regresar)

        self.setLayout(layout)

        self.apply_stylesheet()

    def calcular_cuartil(self):
        cuartil = self.cuartil_combo.currentText()
        if cuartil != 'Seleccionar Cuartil':
            try:
                k = int(cuartil)
                N = sum([float(self.datos_inter.item(i, 3).text()) for i in range(self.datos_inter.rowCount())])

                if N == 0:  # Comprobar si no hay datos
                    raise ValueError("No hay datos disponibles para calcular el cuartil.")

                posicion = k * N / 4
                frecuencia_acumulada = 0
                for i in range(self.datos_inter.rowCount()):
                    frecuencia_acumulada += float(self.datos_inter.item(i, 3).text())
                    if frecuencia_acumulada >= posicion:
                        li = float(self.datos_inter.item(i, 1).text())
                        fa = frecuencia_acumulada - float(self.datos_inter.item(i, 3).text())
                        f = float(self.datos_inter.item(i, 3).text()) 
                        i_width = float(self.datos_inter.item(i, 2).text()) - li 
                        
                        cuartil_value = li + ((posicion - fa) * i_width) / f
                        self.cuartil_resultado.setText(f'El resultado del Cuartil {cuartil} es: {cuartil_value:.2f}')
                        break  # Termina el ciclo aquí
            except Exception as e:
                self.cuartil_resultado.setText("No hay datos para procesar")

    def calcular_decil(self):
        decil = self.decil_combo.currentText()
        if decil != 'Seleccionar Decil':
            try:
                k = int(decil)
                N = sum([float(self.datos_inter.item(i, 3).text()) for i in range(self.datos_inter.rowCount())])

                if N == 0:  # Comprobar si no hay datos
                    raise ValueError("No hay datos disponibles para calcular el decil.")

                posicion = k * N / 10
                frecuencia_acumulada = 0
                for i in range(self.datos_inter.rowCount()):
                    frecuencia_acumulada += float(self.datos_inter.item(i, 3).text())
                    if frecuencia_acumulada >= posicion:
                        li = float(self.datos_inter.item(i, 1).text())
                        fa = frecuencia_acumulada - float(self.datos_inter.item(i, 3).text())
                        f = float(self.datos_inter.item(i, 3).text()) 
                        i_width = float(self.datos_inter.item(i, 2).text()) - li
                        
                        decil_value = li + ((posicion - fa) * i_width) / f
                        self.decil_resultado.setText(f'El resultado del Decil {decil} es: {decil_value:.2f}')
                        break
            except Exception as e:
                self.decil_resultado.setText("No hay datos para procesar")

    def calcular_percentil(self):
        percentil = self.percentil_combo.currentText()
        if percentil:
            try:
                k = int(percentil)
                N = sum([float(self.datos_inter.item(i, 3).text()) for i in range(self.datos_inter.rowCount())])

                if N == 0:  # Comprobar si no hay datos
                    raise ValueError("No hay datos disponibles para calcular el percentil.")

                posicion = k * N / 100
                frecuencia_acumulada = 0
                for i in range(self.datos_inter.rowCount()):
                    frecuencia_acumulada += float(self.datos_inter.item(i, 3).text())
                    if frecuencia_acumulada >= posicion:
                        li = float(self.datos_inter.item(i, 1).text())
                        fa = frecuencia_acumulada - float(self.datos_inter.item(i, 3).text())
                        f = float(self.datos_inter.item(i, 3).text()) 
                        i_width = float(self.datos_inter.item(i, 2).text()) - li
                        
                        percentil_value = li + ((posicion - fa) * i_width) / f
                        self.percentil_resultado.setText(f'El resultado del Percentil {percentil} es: {percentil_value:.2f}')
                        break
            except Exception as e:
                self.percentil_resultado.setText("No hay datos para procesar")
    
    def center_window(self):
        screen = QGuiApplication.primaryScreen().geometry()
        window_geometry = self.frameGeometry()

        center_point = screen.center()
        window_geometry.moveCenter(center_point)

        self.move(window_geometry.topLeft())
    
    def apply_stylesheet(self):
        qss_file = QFile("ventanas.qss")
        if qss_file.open(QIODevice.OpenModeFlag.ReadOnly | QIODevice.OpenModeFlag.Text):
            stream = QTextStream(qss_file)
            self.setStyleSheet(stream.readAll())

class Window2(QWidget):
    def __init__(self, previous_window):
        super().__init__()
        self.previous_window = previous_window
        self.setWindowTitle("Ventana 2")
        self.setMaximumSize(1000, 600)
        self.setMinimumSize(950, 500)
        self.setGeometry(100, 100, 800, 400)
        self.setWindowIcon(QIcon("./img/logo.png"))

        main_layout = QHBoxLayout()
        self.center_window()

        Botones_layout = QVBoxLayout()
        self.buttons = {
            "Boton_Panel1": QPushButton("combinaciones"),
            "Boton_Panel2": QPushButton("Distri Normal int"),
            "Boton_Panel3": QPushButton("Distribucion Normal"),
            "Boton_Panel4": QPushButton("Distribucion Binomial"),
            "Boton_Panel5": QPushButton("Distribucion Poisson"),
            "Boton_Regresar": QPushButton("Regresar")
        }

        for button in self.buttons.values():
            Botones_layout.addWidget(button)

        self.stack = QStackedWidget()
        self.stack.addWidget(self.combinaciones())
        self.stack.addWidget(self.normalInv())
        self.stack.addWidget(self.normal())
        self.stack.addWidget(self.binomial())
        self.stack.addWidget(self.poisson_panel())

        self.buttons["Boton_Panel1"].clicked.connect(lambda: self.change_panel(0))
        self.buttons["Boton_Panel2"].clicked.connect(lambda: self.change_panel(1))
        self.buttons["Boton_Panel3"].clicked.connect(lambda: self.change_panel(2))
        self.buttons["Boton_Panel4"].clicked.connect(lambda: self.change_panel(3))
        self.buttons["Boton_Panel5"].clicked.connect(lambda: self.change_panel(4))
        self.buttons["Boton_Regresar"].clicked.connect(self.regresar)

        main_layout.addLayout(Botones_layout)
        main_layout.addWidget(self.stack)
        self.setLayout(main_layout)

        self.apply_stylesheet()

    def combinaciones(self):
        panel = QWidget()
        main_layout = QVBoxLayout()

        banner_layout = QHBoxLayout()
        banner = QLabel()
        pixmap = QPixmap("./img/banner4.jpg")
        banner.setPixmap(pixmap.scaled(800, 250))
        banner_layout.addWidget(banner)

        main_layout.addLayout(banner_layout)

        content_layout = QHBoxLayout()
        
        layout1 = QVBoxLayout()
        combo1 = QComboBox()
        combo1.addItem("Combinaciones sin repetición")
        combo1.addItem("Combinaciones con repetición")
        label_n1 = QLabel("Valor de n:")
        n_input1 = QLineEdit()
        label_r1 = QLabel("Valor de r:")
        r_input1 = QLineEdit()
        boton_calcular1 = QPushButton("Calcular")
        boton_limpiar1 = QPushButton("Limpiar")
        label_resultado1 = QLabel("Resultado: ")
        title2 = QLabel("Conbinaciones")

        title2.setFont(QFont("Arial",8))

        layout1.addWidget(title2)
        layout1.addWidget(label_resultado1)
        n1 = QHBoxLayout()
        n1.addWidget(label_n1)
        n1.addWidget(n_input1)
        layout1.addLayout(n1)
        r1 = QHBoxLayout()
        r1.addWidget(label_r1)
        r1.addWidget(r_input1)
        layout1.addLayout(r1)
        layout1.addWidget(combo1)
        layout1.addWidget(boton_calcular1)
        layout1.addWidget(boton_limpiar1)
        
        boton_calcular1.clicked.connect(lambda: self.calcular_combinaciones(n_input1, r_input1, label_resultado1, combo1))
        boton_limpiar1.clicked.connect(lambda: self.limpiar_Combinacion(n_input1, r_input1, label_resultado1))

        layout2 = QVBoxLayout()
        combo2 = QComboBox()
        combo2.addItem("Permutaciones sin repetición")
        combo2.addItem("Permutaciones con repetición")
        label_n2 = QLabel("Valor de n:")
        n_input2 = QLineEdit()
        label_r2 = QLabel("Valor de r:")
        r_input2 = QLineEdit()
        boton_calcular2 = QPushButton("Calcular")
        boton_limpiar2 = QPushButton("Limpiar")
        label_resultado2 = QLabel("Resultado: ")
        title2 = QLabel("Permutaciones")

        layout2.addWidget(title2)
        layout2.addWidget(label_resultado2)
        n2 = QHBoxLayout()
        n2.addWidget(label_n2)
        n2.addWidget(n_input2)
        layout2.addLayout(n2)
        r2 = QHBoxLayout()
        r2.addWidget(label_r2)
        r2.addWidget(r_input2)
        layout2.addLayout(r2)
        layout2.addWidget(combo2)
        layout2.addWidget(boton_calcular2)
        layout2.addWidget(boton_limpiar2)
        
        boton_calcular2.clicked.connect(lambda: self.calcular_combinaciones(n_input2, r_input2, label_resultado2, combo2))
        boton_limpiar2.clicked.connect(lambda: self.limpiar_Combinacion(n_input2, r_input2, label_resultado2))

        layout3 = QVBoxLayout()
        combo3 = QComboBox()
        combo3.addItem("Permutaciones sin repetición (n!)")
        combo3.addItem("Permutaciones circulares")
        label_n3 = QLabel("Valor de n:")
        n_input3 = QLineEdit()
        boton_calcular3 = QPushButton("Calcular")
        boton_limpiar3 = QPushButton("Limpiar")
        label_resultado3 = QLabel("Resultado: ")
        title3 = QLabel("Otras permutaciones")

        layout3.addWidget(title3)
        layout3.addWidget(label_resultado3)
        n3 = QHBoxLayout()
        n3.addWidget(label_n3)
        n3.addWidget(n_input3)
        layout3.addLayout(n3)
        layout3.addWidget(combo3)
        layout3.addWidget(boton_calcular3)
        layout3.addWidget(boton_limpiar3)
        
        boton_calcular3.clicked.connect(lambda: self.calcular_combinaciones(n_input3, None, label_resultado3, combo3))
        boton_limpiar3.clicked.connect(lambda: self.limpiar_Combinacion(n_input3, None, label_resultado3))

        content_layout.addLayout(layout1)
        content_layout.addLayout(layout2)
        content_layout.addLayout(layout3)

        main_layout.addLayout(content_layout)
        panel.setLayout(main_layout)
        
        return panel

    def calcular_combinaciones(self, n_input, r_input, label_resultado, combo):
        try:
            n = int(n_input.text())
            r = int(r_input.text()) if r_input else None

            tipo = combo.currentText()
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

            label_resultado.setText(f"Resultado: {round(res, 4)}")
        except ValueError:
            label_resultado.setText("Por favor, ingresa valores válidos para n y r.")

    def limpiar_Combinacion(self, n_input, r_input, label_resultado):
        n_input.clear()
        if r_input:
            r_input.clear()
        label_resultado.setText("Resultado: ")

    def normalInv(self):
        panel = QWidget()
        layout = QVBoxLayout()
        labels = QHBoxLayout()
        text = QHBoxLayout()
        inputs = QVBoxLayout()
        botones = QHBoxLayout()

        self.canvas = FigureCanvas(plt.Figure())
        layout.addWidget(self.canvas)

        labelMedia = QLabel("Media (μ):")
        self.textMedia = QLineEdit(" ")
        labelDesviacion = QLabel("Desviación Estándar (σ):")
        self.textDesviacion = QLineEdit(" ")
        labelRango = QLabel("Rango (± alrededor de μ):")
        self.textRango = QLineEdit(" ")
        
        self.label_resultado = QLabel("Probabilidad dentro del rango: ")
        layout.addWidget(self.label_resultado)
        
        boton_calcular = QPushButton("Calcular")
        boton_calcular.clicked.connect(self.calcular_Inv)
        
        boton_limpiar = QPushButton("Limpiar")
        boton_limpiar.clicked.connect(self.limpiar_campos)

        labels.addWidget(labelMedia)
        labels.addWidget(labelDesviacion)
        labels.addWidget(labelRango)
        text.addWidget(self.textMedia)
        text.addWidget(self.textDesviacion)
        text.addWidget(self.textRango)
        inputs.addLayout(labels)
        inputs.addLayout(text)
        
        layout.addLayout(inputs)
        botones.addWidget(boton_calcular)
        botones.addWidget(boton_limpiar)
        layout.addLayout(botones)
        
        panel.setLayout(layout)
        return panel

    def calcular_Inv(self):
        try:
            media = float(self.textMedia.text())
            desviacion = float(self.textDesviacion.text())
            rango = float(self.textRango.text())
            lim_inferior = media - rango
            lim_superior = media + rango

            probabilidad = norm.cdf(lim_superior, loc=media, scale=desviacion) - norm.cdf(lim_inferior, loc=media, scale=desviacion)
            self.label_resultado.setText(f"Probabilidad dentro del rango: {probabilidad:.4f}")

            self.graficar_Norm_Inv(media, desviacion, lim_inferior, lim_superior)

        except ValueError:
            self.label_resultado.setText("Ingrese valores válidos")

    def graficar_Norm_Inv(self, media, desviacion, lim_inferior, lim_superior):
        ax = self.canvas.figure.add_subplot(111)
        ax.clear()

        x = np.linspace(media - 4 * desviacion, media + 4 * desviacion, 1000)
        y = norm.pdf(x, loc=media, scale=desviacion)

        ax.plot(x, y, label="Distribución Normal")
        x_fill = np.linspace(lim_inferior, lim_superior, 1000)
        y_fill = norm.pdf(x_fill, loc=media, scale=desviacion)
        ax.fill_between(x_fill, y_fill, color="skyblue", alpha=0.4)

        ax.axvline(lim_inferior, color='orange', linestyle='--', label="Límite Inferior")
        ax.axvline(lim_superior, color='orange', linestyle='--', label="Límite Superior")

        ax.set_title('Distribución Normal')
        ax.set_xlabel('Valor')
        ax.set_ylabel('Densidad')
        ax.legend()
        ax.grid()

        self.canvas.draw()

    def limpiar_campos(self):
        self.textMedia.setText(" ")
        self.textDesviacion.setText(" ")
        self.textRango.setText(" ")
        self.label_resultado.setText("Probabilidad dentro del rango: ")
        self.canvas.figure.clear()
        self.canvas.draw()

    def normal(self):
        panel = QWidget()
        layout = QVBoxLayout(panel)
        self.figura = Figure()
        self.canvas = FigureCanvas(self.figura)
        layout.addWidget(self.canvas)

        layoutH = QVBoxLayout()
        self.resultado_normal = QLabel("")
        layout.addWidget(self.resultado_normal)
        
        label_layout = QHBoxLayout()
        label_layout.addWidget(QLabel("Valor (x):"))
        label_layout.addWidget(QLabel("Media (μ):"))
        label_layout.addWidget(QLabel("Desviación estándar (σ):"))
        label_layout.addWidget(QLabel("Tipo de distribución:"))
        
        textfield_layout = QHBoxLayout()
        self.x_input_normal = QLineEdit()
        self.mu_input_normal = QLineEdit()
        self.sigma_input_normal = QLineEdit()
        textfield_layout.addWidget(self.x_input_normal)
        textfield_layout.addWidget(self.mu_input_normal)
        textfield_layout.addWidget(self.sigma_input_normal)
        
        self.combo_acumulado_normal = QComboBox()
        self.combo_acumulado_normal.addItems(["Elija una opción", "Acumulativa", "No acumulativa"])
        textfield_layout.addWidget(self.combo_acumulado_normal)
        
        layoutH.addLayout(label_layout)
        layoutH.addLayout(textfield_layout)
        layoutBotones = QHBoxLayout()
        boton_calcular_normal = QPushButton("Calcular Normal")
        boton_calcular_normal.clicked.connect(self.calcular_normal)
        layoutBotones.addWidget(boton_calcular_normal)
        
        boton_limpiar_normal = QPushButton("Limpiar")
        boton_limpiar_normal.clicked.connect(self.limpiar_normal)
        layoutBotones.addWidget(boton_limpiar_normal)
        
        layout.addLayout(layoutH)
        layout.addLayout(layoutBotones)
        
        return panel

    def graficar_normal(self, mu, sigma, acumulado=False):
        self.figura.clear()
        x = np.linspace(mu - 4 * sigma, mu + 4 * sigma, 1000)
        ax = self.figura.add_subplot(111)

        if acumulado:
            y = norm.cdf(x, mu, sigma)
            ax.set_title('Función de Distribución Acumulativa (CDF)')
            ax.fill_between(x, y, color='skyblue', alpha=0.5)
        else:
            y = norm.pdf(x, mu, sigma)
            ax.set_title('Función de Densidad de Probabilidad (PDF)')
            ax.fill_between(x, y, color='skyblue', alpha=0.5)

        ax.plot(x, y, color='blue', label='Distribución normal')
        ax.axvline(mu, color='r', linestyle='--', label='Media (μ)')
        ax.axvline(mu + sigma, color='g', linestyle='--', label='σ')
        ax.axvline(mu - sigma, color='g', linestyle='--')

        ax.set_xlabel('Valor (x)')
        ax.set_ylabel('Probabilidad')
        ax.legend()
        ax.grid()

        self.canvas.draw()

    def calcular_normal(self):
        try:
            x = float(self.x_input_normal.text())
            mu = float(self.mu_input_normal.text())
            sigma = float(self.sigma_input_normal.text())

            if sigma <= 0:
                self.resultado_normal.setText("Por favor, ingrese un valor positivo para la desviación estándar.")
                return
        except ValueError:
            self.resultado_normal.setText("Por favor, ingrese valores válidos para proseguir.")
            return

        acumulado = self.combo_acumulado_normal.currentText() == "Acumulativa"

        if self.combo_acumulado_normal.currentText() == "Elija una opción":
            self.resultado_normal.setText("Por favor seleccione una opción acumulativa o no acumulativa para continuar.")
            return

        try:
            if acumulado:
                resultado = norm.cdf(x, mu, sigma)
                self.resultado_normal.setText(f"Probabilidad acumulada (CDF): {resultado:.4f}")
            else:
                resultado = norm.pdf(x, mu, sigma)
                self.resultado_normal.setText(f"Densidad normal (PDF): {resultado:.4f}")

            self.graficar_normal(mu, sigma, acumulado)

        except ValueError as e:
            self.resultado_normal.setText(str(e))

    def limpiar_normal(self):
        self.x_input_normal.clear()
        self.mu_input_normal.clear()
        self.sigma_input_normal.clear()
        self.combo_acumulado_normal.setCurrentIndex(0)
        self.resultado_normal.clear()
        self.figura.clear()
        self.canvas.draw()

    def poisson_panel(self):
        panel = QWidget()
        layout = QVBoxLayout()
        layoutV = QVBoxLayout()
        label_layout = QHBoxLayout()
        textfield_layout = QHBoxLayout()

        self.grafica_widget = QWidget()
        self.grafica_layout = QVBoxLayout(self.grafica_widget)
        layout.addWidget(self.grafica_widget)

        combo_acumulado = QComboBox()
        combo_acumulado.addItems(["Elija una opción", "Acumulativa", "No acumulativa"])
        label_layout.addWidget(QLabel("Tipo de distribución: "))
        textfield_layout.addWidget(combo_acumulado)

        label_x = QLabel("Número de éxitos (x): ")
        x_input = QLineEdit()
        label_media = QLabel("Media (λ): ")
        media_input = QLineEdit()

        label_resultado = QLabel("Resultado Poisson:")
        layout.addWidget(label_resultado)

        label_layout.addWidget(label_x)
        label_layout.addWidget(label_media)
        textfield_layout.addWidget(x_input)
        textfield_layout.addWidget(media_input)

        layoutV.addLayout(label_layout)
        layoutV.addLayout(textfield_layout)

        botones_layout = QHBoxLayout()
        boton_actualizar = QPushButton("Actualizar")
        boton_limpiar = QPushButton("Limpiar")

        botones_layout.addWidget(boton_actualizar)
        botones_layout.addWidget(boton_limpiar)

        boton_actualizar.clicked.connect(lambda: self.actualizar_poisson(x_input, media_input, label_resultado, combo_acumulado))
        boton_limpiar.clicked.connect(lambda: self.limpiar_poisson(x_input, media_input, label_resultado, combo_acumulado))

        layout.addLayout(layoutV)
        layout.addLayout(botones_layout)

        panel.setLayout(layout)
        return panel

    def graficar_poisson(self, media):
        for i in reversed(range(self.grafica_layout.count())):
            widget = self.grafica_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()
        
        figura = Figure()
        canvas = FigureCanvas(figura)
        self.grafica_layout.addWidget(canvas)

        x = np.arange(0, int(media) + 4 * int(media), 1)
        y = [poisson.pmf(k, media) for k in x]

        ax = figura.add_subplot(111)
        ax.bar(x, y, color='skyblue', alpha=0.5)

        ax.set_title('Función de Densidad de Probabilidad (PMF) de Poisson')
        ax.set_xlabel('Número de Éxitos (x)')
        ax.set_ylabel('Probabilidad')
        ax.grid()

        canvas.draw()

    def actualizar_poisson(self, x_input, media_input, label_resultado, combo_acumulado):
        try:
            x = int(x_input.text())
            media = float(media_input.text())
            seleccion = combo_acumulado.currentText()

            if seleccion == "Elija una opción":
                label_resultado.setText("Seleccione una opción: acumulativa o no acumulativa.")
                return  
            acumulado = seleccion == "Acumulativa"
            if x < 0 or media <= 0:
                raise ValueError("Los valores deben ser positivos")

            resultado = distriPoison(x, media, acumulado)
            resultado = round(resultado, 4)
            label_resultado.setText(f"Resultado Poisson: {resultado}")

            self.graficar_poisson(media)

        except ValueError as e:
            label_resultado.setText(f"Error: {str(e)}")

    def limpiar_poisson(self, x_input, media_input, label_resultado, combo_acumulado):
        x_input.clear()
        media_input.clear()
        combo_acumulado.setCurrentIndex(0)
        label_resultado.setText("")
        for i in reversed(range(self.grafica_layout.count())):
            widget = self.grafica_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()
        
    def binomial(self):
        panel = QWidget()
        layout = QVBoxLayout()

        layoutV = QVBoxLayout()
        label_layout = QHBoxLayout()
        textfiel_layout = QHBoxLayout()

        figura = Figure()
        canvas = FigureCanvas(figura)
        layout.addWidget(canvas)

        combo_acumulado = QComboBox()
        combo_acumulado.addItems(["Elija una opción", "Acumulativa", "No acumulativa"])

        label_resultado = QLabel("Resultado Binomial: ")
        label_n = QLabel("Número de ensayos (n): ")
        n_input = QLineEdit()
        label_k = QLabel("Número de éxitos (K): ")
        k_input = QLineEdit()
        label_p = QLabel("Probabilidad de éxito (P): ")
        p_input = QLineEdit()

        label_layout.addWidget(label_n)
        label_layout.addWidget(label_k)
        label_layout.addWidget(label_p)
        label_layout.addWidget(QLabel("Tipo de distribución: "))
        textfiel_layout.addWidget(n_input)
        textfiel_layout.addWidget(k_input)
        textfiel_layout.addWidget(p_input)
        textfiel_layout.addWidget(combo_acumulado)

        layoutV.addLayout(label_layout)
        layoutV.addLayout(textfiel_layout)

        Botones_layout = QHBoxLayout()
        boton_actualizar = QPushButton("Actualizar")
        boton_limpiar = QPushButton("Limpiar")

        Botones_layout.addWidget(boton_actualizar)
        Botones_layout.addWidget(boton_limpiar)

        boton_actualizar.clicked.connect(lambda: self.actualizar_binomial(n_input, k_input, p_input, label_resultado, combo_acumulado, canvas))
        boton_limpiar.clicked.connect(lambda: self.limpiar_binomial(n_input, k_input, p_input, label_resultado, combo_acumulado, canvas))

        layout.addWidget(label_resultado)
        layout.addLayout(layoutV)
        layout.addLayout(Botones_layout)

        panel.setLayout(layout)
        return panel

    def actualizar_binomial(self, n_input, k_input, p_input, label_resultado, combo_acumulado, canvas):
        try:
            n = int(n_input.text())
            k = int(k_input.text())
            p = float(p_input.text())

            seleccion = combo_acumulado.currentText()
            if seleccion == "Elija una opción":
                label_resultado.setText("Selecciona un valor acumulativo o no acumulativo.")
                return
            
            acumulado = seleccion == "Acumulativa"
            if n < 0 or k < 0 or not (0 <= p <= 1):
                raise ValueError("Los valores deben ser positivos y 0 <= p <= 1")

            resultado = distriBinomial(k, n, p, acumulado)
            resultado = round(resultado, 4)
            label_resultado.setText(f"Resultado Binomial: {resultado}")
            
            self.graficar_en_canvas(n, p, acumulado, canvas)

        except ValueError as e:
            label_resultado.setText(f"Error: {str(e)}")

    def graficar_en_canvas(self, n, p, acumulado, canvas):
        canvas.figure.clf()

        if n > 0:
            x = range(n + 1)
            ax = canvas.figure.add_subplot(111)

            y = [binom.pmf(k, n, p) for k in x]
            ax.set_title('Función de Densidad de Probabilidad (PDF)')
            ax.bar(x, y, color='skyblue', alpha=0.5)

            ax.set_xlabel('Número de éxitos (k)')
            ax.set_ylabel('Probabilidad')
            ax.axhline(0, color='black', lw=1)
            ax.grid()
        else:
            ax = canvas.figure.add_subplot(111)
            ax.set_title('No hay datos para graficar')
            ax.text(0.5, 0.5, 'n debe ser mayor que 0', horizontalalignment='center', verticalalignment='center')
            ax.axis('off')

        canvas.draw()

    def limpiar_binomial(self, n_input, k_input, p_input, label_resultado, combo_acumulado, canvas):
        n_input.clear()
        k_input.clear()
        p_input.clear()
        combo_acumulado.setCurrentIndex(0)
        label_resultado.setText("")

        canvas.figure.clf()
        canvas.draw()

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

    def apply_stylesheet(self):
        qss_file = QFile("style.qss")
        if qss_file.open(QIODevice.OpenModeFlag.ReadOnly | QIODevice.OpenModeFlag.Text):
            stream = QTextStream(qss_file)
            self.setStyleSheet(stream.readAll())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    menu = MenuWindow()
    menu.show()
    sys.exit(app.exec())