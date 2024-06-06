from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QListWidget, QComboBox, QMessageBox
from sound_player import SoundPlayer
import os


class SoundpadApp(QMainWindow):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.initUI()
        self.load_categories()

    def initUI(self):
        self.setWindowTitle("Soundpad")
        self.setGeometry(100, 100, 400, 300)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        self.category_label = QLabel("Выберите категорию:")
        self.layout.addWidget(self.category_label)

        self.category_combo = QComboBox()
        self.category_combo.currentIndexChanged.connect(self.update_sound_list)
        self.layout.addWidget(self.category_combo)

        self.sound_list = QListWidget()
        self.layout.addWidget(self.sound_list)

        self.play_button = QPushButton("Воспроизвести")
        self.play_button.clicked.connect(self.play_sound)
        self.layout.addWidget(self.play_button)

    def load_categories(self):
        categories = self.db.get_categories()
        self.category_combo.addItems(categories)
        self.update_sound_list()

    def update_sound_list(self):
        self.sound_list.clear()
        category = self.category_combo.currentText()
        sounds = self.db.get_sounds_by_category(category)
        for sound in sounds:
            self.sound_list.addItem(sound[0])

    def play_sound(self):
        selected_item = self.sound_list.currentItem()
        if not selected_item:
            QMessageBox.critical(self, "Ошибка", "Пожалуйста, выберите звук для воспроизведения")
            return

        sound_name = selected_item.text()
        category = self.category_combo.currentText()
        sounds = self.db.get_sounds_by_category(category)

        sound_path = next((sound[1] for sound in sounds if sound[0] == sound_name), None)

        if sound_path:
            try:
                sound_player = SoundPlayer(sound_path)
                sound_player.play()
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Не удалось воспроизвести звук: {e}")
        else:
            QMessageBox.critical(self, "Ошибка", "Не удалось найти файл звука")
