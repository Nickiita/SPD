import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QCheckBox, QSpinBox, QLabel, QListWidget
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt


class KFC(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(800, 400, 400, 550)
        self.setWindowTitle('Soundpad')

        button = QPushButton('Заказать', self)
        button.move(50, 200)

        for i, (name, cost, img) in enumerate(self.data):
            label_name = QLabel(name, self)
            label_name.move(80, i * 50 + 10)

            label_cost = QLabel(f"{cost}руб", self)
            label_cost.move(210, i * 50 + 10)

            check = QCheckBox(self)
            check.move(50, i * 50 + 10)

            spin_box = QSpinBox(self)
            spin_box.resize(35, 20)
            spin_box.move(160, i * 50 + 10)
            spin_box.setRange(0, 10)
            spin_box.setValue(0)
            spin_box.setEnabled(False)

            pixmap = QPixmap(img)
            image = QLabel(self)
            image.setAlignment(Qt.AlignCenter)
            image.move(260, i * 50)
            pixmap = pixmap.scaled(40, 40)
            image.setPixmap(pixmap)

            self.dict_checkbox_spinbox[check] = spin_box
            self.dict_checkbox_name[check] = name

            check.clicked.connect(self.check_state)
            button.clicked.connect(self.pushed)

        self.list_widget = QListWidget(self)
        self.list_widget.move(50, 250)
        self.list_widget.resize(300, 230)

    def check_state(self):
        btn: QCheckBox = self.sender()  # btn - local
        if btn.isChecked():
            self.dict_checkbox_spinbox[btn].setEnabled(True)
            self.dict_checkbox_spinbox[btn].setValue(1)
        else:
            self.dict_checkbox_spinbox[btn].setEnabled(False)
            self.dict_checkbox_spinbox[btn].setValue(0)

    def pushed(self):
        total_cost = 0
        order = "Ваш заказ\n\n"

        self.list_widget.clear()

        for checkbox, name in self.dict_checkbox_name.items():
            if checkbox.isChecked():
                quantity = self.dict_checkbox_spinbox[checkbox].value()
                cost = next(item[1] for item in self.data if item[0] == name)
                subtotal = cost * quantity
                total_cost += subtotal
                order += f"{name}-----{quantity}-----{subtotal}руб\n\n"

        order += f"Итого: {total_cost}руб"
        self.list_widget.addItem(order)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    data = [('Гамбургер', 150, 'img1.png'),
            ('Картошка', 110, 'img2.jpg'),
            ('Кока-кола', 90, 'img3.png'),
            ('Наггетсы', 20, 'img4.png')]
    ex = KFC(data)
    ex.show()
    sys.exit(app.exec_())
