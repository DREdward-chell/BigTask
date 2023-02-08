from PyQt5 import QtGui, QtWidgets, QtCore
import requests
import sys
import os


SCREEN_SIZE = (500, 500)


class Application(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.getImage()
        self.initUI()

    def getImage(self, spn: float = 0.002):
        params = {
            "ll": "37.530887,55.703118",
            "l": "map",
            "spn": f"{spn},{spn}"
        }
        map_request = "http://static-maps.yandex.ru/1.x/"
        response = requests.get(map_request, params)

        if not response:
            print("Ошибка выполнения запроса:")
            print(map_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)

        self.map_file = "map.png"
        with open(self.map_file, "wb") as file:
            file.write(response.content)

    def initUI(self):
        global SCREEN_SIZE
        self.setGeometry(100, 100, *SCREEN_SIZE)
        self.setWindowTitle('Отображение карты')

        # Изображение
        self.pixmap = QtGui.QPixmap(self.map_file)
        self.image = QtWidgets.QLabel(self)
        self.image.move(0, 0)
        self.image.resize(*SCREEN_SIZE)
        self.image.setPixmap(self.pixmap)

    def closeEvent(self, event):
        """При закрытии формы подчищаем за собой"""
        os.remove(self.map_file)


def main():
    if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)
    app = QtWidgets.QApplication(sys.argv)
    exe = Application()
    exe.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
