from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QByteArray
from PyQt5.QtCore import Qt

from io import BytesIO
import requests
import sys
from PIL import Image

from map_app import Ui_MainWindow as MainUi


class Main(QMainWindow, MainUi):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.static_map_request = 'https://static-maps.yandex.ru/1.x/'
        self.static_map_x = 37.617218
        self.static_map_y = 55.751694
        self.static_map_params = {"ll": f'{self.static_map_x},{self.static_map_y}',
                                  "z": '10',
                                  "size": '650,450',
                                  "l": "map"}
        self.update_image()

    def update_image(self):
        response = requests.get(self.static_map_request, params=self.static_map_params)
        self.image = QPixmap()
        self.image.loadFromData(QByteArray(response.content), "PNG")
        self.map_label.setPixmap(self.image)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageDown:
            z = int(self.static_map_params["z"])
            if z - 1 >= 0:
                z -= 1
            self.static_map_params["z"] = str(z)

        if event.key() == Qt.Key_PageUp:
            z = int(self.static_map_params["z"])
            if z + 1 <= 17:
                z += 1
            self.static_map_params["z"] = str(z)
        self.update_image()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Main()
    ex.show()
    sys.exit(app.exec())
