import sys
from PyQt5.QtWidgets import QApplication
from soundpad import SoundpadApp
from database import SoundpadDatabase


def main():
    db = SoundpadDatabase("../resources/sounds.db")

    app = QApplication(sys.argv)
    main_window = SoundpadApp(db)
    main_window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
