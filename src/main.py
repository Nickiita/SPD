import sys
from PyQt5.QtWidgets import QApplication
from soundpad import SoundpadApp
from database import SoundpadDatabase
import keyboard


def main():
    db = SoundpadDatabase("../resources/sounds.db")

    app = QApplication(sys.argv)
    main_window = SoundpadApp(db)
    main_window.show()

    # Инициализация глобального прослушивателя горячих клавиш
    hotkeys = db.get_hotkeys()
    for sound_name, hotkey in hotkeys:
        sound_path = db.get_sound_path_by_name(sound_name)
        keyboard.add_hotkey(hotkey, lambda path=sound_path: main_window.play_sound_by_path(sound_path))

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
