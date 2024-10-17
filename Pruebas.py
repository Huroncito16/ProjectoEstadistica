from PyQt6.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

class ImageWidget(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        self.image_label = QLabel(self)

        # Cargar la imagen
        pixmap = QPixmap("./img/banner3.jpg")

        # Escalar la imagen al tamaño del QLabel manteniendo proporciones
        scaled_pixmap = pixmap.scaled(self.image_label.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)

        # Asignar la imagen escalada al QLabel
        self.image_label.setPixmap(scaled_pixmap)

        layout.addWidget(self.image_label)
        self.setLayout(layout)

        # Conectar un evento para ajustar la imagen cuando cambie el tamaño
        self.image_label.resizeEvent = self.resize_image

    def resize_image(self, event):
        # Escalar la imagen cuando cambie el tamaño del QLabel
        pixmap = QPixmap("./img/banner3.jpg")
        scaled_pixmap = pixmap.scaled(self.image_label.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self.image_label.setPixmap(scaled_pixmap)

if __name__ == "__main__":
    app = QApplication([])
    window = ImageWidget()
    window.show()
    app.exec()