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

    def move_map(self, move_x, move_y):
        z = int(self.static_map_params["z"])
        dx = 360 / 2 ** z
        dy = 180 / 2 ** z
        self.static_map_x += dx * move_x
        self.static_map_y += dy * move_y
        self.static_map_x = (self.static_map_x + 180) % 360 - 180
        self.static_map_y = min(self.static_map_y, 90)
        self.static_map_y = max(self.static_map_y, -90)
        self.static_map_params["ll"] = f'{self.static_map_x},{self.static_map_y}'

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

        if event.key() == Qt.Key_A:
            self.move_map(-1, 0)

        if event.key() == Qt.Key_W:
            self.move_map(0, 1)

        if event.key() == Qt.Key_D:
            self.move_map(1, 0)

        if event.key() == Qt.Key_S:
            self.move_map(0, -1)

        self.update_image()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Main()
    ex.show()
    sys.exit(app.exec())
