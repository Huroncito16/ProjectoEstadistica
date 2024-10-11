from PyQt6.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget
from PyQt6.QtCharts import QChartView, QChart, QBarSet, QBarSeries, QBarCategoryAxis, QValueAxis
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter

class MiVentana(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Actualizar Gráfico de Barras")

        # Ruta de archivo guardada (dummy para el ejemplo)
        self.saved_file_path = 'ruta/del/archivo.csv'

        # Layout principal
        self.layout = QVBoxLayout()
        self.central_widget = QWidget()
        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)

        # Botón para actualizar el gráfico
        self.update_button = QPushButton("Actualizar Gráfico")
        self.update_button.clicked.connect(self.actualizar_grafico)
        self.layout.addWidget(self.update_button)

        # Crear el gráfico inicial
        self.chart_view = self.crear_Grafico()
        self.layout.addWidget(self.chart_view)

    def leerDatos(self, file_path):
        # Aquí iría la lógica de leer el archivo y devolver los datos
        # Para el ejemplo, devolveremos datos dummy
        return [1, 2, 3, 4, 5]

    def listas(self, datos):
        # Aquí iría la lógica de procesar los datos
        # Para el ejemplo, devolveremos valores estadísticos dummy
        return {
            'rango': 10,
            'media': 20,
            'mediana': 15,
            'moda': 5,
            'varianza': 25,
            'desviacion_estandar': 8,
            'curtosis': 1,
            'asimetria': -0.5,
            'error_tipico': 2.5,
            'suma': 100,
            'cuenta': 50
        }

    def crear_Grafico(self):
        if self.saved_file_path:
            datos = self.leerDatos(self.saved_file_path)
            data = self.listas(datos)
            series = QBarSeries()
            bar_set = QBarSet("Datos Estadísticos")

            # Valores estadísticos
            bar_values = [
                data['rango'], 
                data['media'], 
                data['mediana'], 
                data['moda'], 
                data['varianza'], 
                data['desviacion_estandar'], 
                data['curtosis'], 
                data['asimetria'], 
                data['error_tipico'], 
                data['suma'], 
                data['cuenta']
            ]
            bar_set.append(bar_values)
            series.append(bar_set)

            # Crear el gráfico
            chart = QChart()
            chart.addSeries(series)
            chart.setTitle("Gráfico de Barras - Valores Estadísticos")
            chart.setAnimationOptions(QChart.AnimationOption.SeriesAnimations)

            # Eje X (categorías)
            axisX = QBarCategoryAxis()
            axisX.append(['Rango', 'Media', 'Mediana', 'Moda', 'Varianza', 'Desviación Est.', 'Curtosis', 'Asimetría', 'Error Típico', 'Suma', 'Cuenta'])
            chart.addAxis(axisX, Qt.AlignmentFlag.AlignBottom)
            series.attachAxis(axisX)

            # Eje Y (valores numéricos)
            axisY = QValueAxis()
            axisY.setRange(0, max(bar_values) + 10)  # Ajusta el rango en función de los valores
            chart.addAxis(axisY, Qt.AlignmentFlag.AlignLeft)
            series.attachAxis(axisY)

            # Configurar la vista del gráfico
            chart_view = QChartView(chart)
            chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)

            return chart_view

    def actualizar_grafico(self):
        # Elimina la gráfica anterior del layout
        self.layout.removeWidget(self.chart_view)
        self.chart_view.deleteLater()

        # Crea una nueva gráfica y la añade al layout
        self.chart_view = self.crear_Grafico()
        self.layout.addWidget(self.chart_view)