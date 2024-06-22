from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QSlider, QPushButton
from PyQt5.QtCore import Qt

class SettingsWindow(QDialog):
    def __init__(self, db, main_window):
        super().__init__()
        self.db = db
        self.main_window = main_window
        self.initUI()
        self.load_settings()
        self.setGeometry(main_window.geometry())

    def initUI(self):
        self.setWindowTitle("Настройки")

        self.layout = QVBoxLayout()

        self.volume_label = QLabel("Громкость")
        self.layout.addWidget(self.volume_label)

        self.volume_slider = QSlider(Qt.Horizontal)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.valueChanged.connect(self.update_volume_label)
        self.layout.addWidget(self.volume_slider)

        self.speed_label = QLabel("Скорость воспроизведения")
        self.layout.addWidget(self.speed_label)

        self.speed_slider = QSlider(Qt.Horizontal)
        self.speed_slider.setRange(50, 150)
        self.speed_slider.valueChanged.connect(self.update_speed_label)
        self.layout.addWidget(self.speed_slider)

        self.save_button = QPushButton("Сохранить")
        self.save_button.clicked.connect(self.save_settings)
        self.layout.addWidget(self.save_button)

        self.setLayout(self.layout)

    def load_settings(self):
        volume, playback_speed = self.db.get_settings()
        self.volume_slider.setValue(int(volume * 100))
        self.speed_slider.setValue(int(playback_speed * 100))

    def update_volume_label(self, value):
        self.volume_label.setText(f"Громкость: {value}%")

    def update_speed_label(self, value):
        self.speed_label.setText(f"Скорость воспроизведения: {value}%")

    def save_settings(self):
        volume = self.volume_slider.value() / 100
        playback_speed = self.speed_slider.value() / 100
        self.db.update_settings(volume, playback_speed)
        self.main_window.setGeometry(self.geometry())
        self.main_window.show()
        self.close()
