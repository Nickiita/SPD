from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QListWidget,
                             QComboBox, QMessageBox, QInputDialog, QFileDialog)
from PyQt5.QtGui import QGuiApplication
from sound_player import SoundPlayer
from settings import SettingsWindow
import os

class SoundpadApp(QMainWindow):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.current_player = None
        self.initUI()
        self.load_categories()
        self.load_hotkeys()
        self.center_x = None
        self.center_y = None

    def initUI(self):
        self.setWindowTitle("Soundpad")
        self.setGeometry(100, 100, 500, 500)

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

        self.button_layout = QHBoxLayout()  # Создаем горизонтальный макет для кнопок

        self.play_button = QPushButton("Воспроизвести")
        self.play_button.clicked.connect(self.play_sound)
        self.button_layout.addWidget(self.play_button)

        self.settings_button = QPushButton("Настройки")
        self.settings_button.clicked.connect(self.open_settings)
        self.button_layout.addWidget(self.settings_button)

        self.add_hotkey_button = QPushButton("Добавить горячую клавишу")
        self.add_hotkey_button.clicked.connect(self.add_hotkey)
        self.button_layout.addWidget(self.add_hotkey_button)

        self.stop_button = QPushButton("Остановить звук")
        self.stop_button.clicked.connect(self.stop_sound)
        self.button_layout.addWidget(self.stop_button)

        self.add_sound_button = QPushButton("Добавить звук")
        self.add_sound_button.clicked.connect(self.add_sound)
        self.button_layout.addWidget(self.add_sound_button)

        self.remove_sound_button = QPushButton("Удалить звук")
        self.remove_sound_button.clicked.connect(self.remove_sound)
        self.button_layout.addWidget(self.remove_sound_button)

        self.layout.addLayout(self.button_layout)  # Добавляем горизонтальный макет в основной вертикальный макет

    def showEvent(self, event):
        super().showEvent(event)
        if self.center_x is None or self.center_y is None:
            self.center()
        else:
            self.move(self.center_x, self.center_y)

    def center(self):
        screen_geometry = QGuiApplication.primaryScreen().availableGeometry()
        window_geometry = self.geometry()
        self.center_x = (screen_geometry.width() - window_geometry.width()) // 2
        self.center_y = (screen_geometry.height() - window_geometry.height()) // 2
        self.move(self.center_x, self.center_y)

    def load_categories(self):
        categories = self.db.get_categories()
        self.category_combo.addItems(categories)
        self.update_sound_list()

    def update_sound_list(self):
        self.sound_list.clear()
        category = self.category_combo.currentText()
        sounds = self.db.get_sounds_by_category(category)
        for sound in sounds:
            self.sound_list.addItem(sound[1])
        self.load_hotkeys()

    def load_hotkeys(self):
        hotkeys = self.db.get_hotkeys()
        for i in range(self.sound_list.count()):
            item = self.sound_list.item(i)
            sound_name = item.text()
            hotkey = next((hk[1] for hk in hotkeys if hk[0] == sound_name), None)
            if hotkey:
                item.setText(f"{sound_name} ({hotkey})")

    def play_sound(self):
        selected_item = self.sound_list.currentItem()
        if not selected_item:
            QMessageBox.critical(self, "Ошибка", "Пожалуйста, выберите звук для воспроизведения")
            return

        sound_name = selected_item.text().split(' (')[0]
        category = self.category_combo.currentText()
        sounds = self.db.get_sounds_by_category(category)

        sound_path = next((sound[2] for sound in sounds if sound[1] == sound_name), None)
        volume, playback_speed = self.db.get_settings()

        if sound_path:
            try:
                if self.current_player and self.current_player.is_playing():
                    self.current_player.stop()

                self.current_player = SoundPlayer(sound_path, volume, playback_speed)
                self.current_player.play_async()
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Не удалось воспроизвести звук: {e}")
        else:
            QMessageBox.critical(self, "Ошибка", "Не удалось найти файл звука")

    def stop_sound(self):
        if self.current_player and self.current_player.is_playing():
            self.current_player.stop()

    def open_settings(self):
        self.center_x = self.pos().x()
        self.center_y = self.pos().y()
        settings_window = SettingsWindow(self.db, self)
        settings_window.exec_()

    def add_hotkey(self):
        selected_item = self.sound_list.currentItem()
        if not selected_item:
            QMessageBox.critical(self, "Ошибка", "Пожалуйста, выберите звук для добавления горячей клавиши")
            return

        sound_name = selected_item.text().split(' (')[0]
        category = self.category_combo.currentText()
        sounds = self.db.get_sounds_by_category(category)

        sound_id = next((sound[0] for sound in sounds if sound[1] == sound_name), None)

        if sound_id:
            hotkey, ok = QInputDialog.getText(self, "Горячая клавиша", "Введите комбинацию клавиш:")
            if ok and hotkey:
                self.db.add_hotkey(sound_id, hotkey)
                self.update_sound_list()
        else:
            QMessageBox.critical(self, "Ошибка", "Не удалось найти звук для добавления горячей клавиши")

    def add_sound(self):
        category = self.category_combo.currentText()
        if not category:
            QMessageBox.critical(self, "Ошибка", "Пожалуйста, выберите категорию для добавления звука")
            return

        file_name, _ = QFileDialog.getOpenFileName(self, "Выберите звуковой файл", "", "Audio Files (*.wav *.mp3)")
        if not file_name:
            return

        name, ok = QInputDialog.getText(self, "Название звука", "Введите название звука:")
        if ok and name:
            self.db.add_sound(category, name, file_name)
            self.update_sound_list()
        else:
            QMessageBox.critical(self, "Ошибка", "Не удалось добавить звук")

    def remove_sound(self):
        selected_item = self.sound_list.currentItem()
        if not selected_item:
            QMessageBox.critical(self, "Ошибка", "Пожалуйста, выберите звук для удаления")
            return

        sound_name = selected_item.text().split(' (')[0]
        category = self.category_combo.currentText()
        sounds = self.db.get_sounds_by_category(category)

        sound_id = next((sound[0] for sound in sounds if sound[1] == sound_name), None)

        if sound_id:
            self.db.remove_sound(sound_id)
            self.update_sound_list()
        else:
            QMessageBox.critical(self, "Ошибка", "Не удалось найти звук для удаления")
