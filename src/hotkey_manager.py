from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton
from PyQt5.QtGui import QKeySequence


class HotkeyManager(QDialog):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.new_hotkey = None
        self.setWindowTitle("Назначение горячей клавиши")
        self.layout = QVBoxLayout(self)

        self.label = QLabel("Нажмите новую комбинацию клавиш:")
        self.layout.addWidget(self.label)

        self.line_edit = QLineEdit()
        self.line_edit.setReadOnly(True)
        self.layout.addWidget(self.line_edit)

        self.save_button = QPushButton("Сохранить")
        self.save_button.setEnabled(False)
        self.save_button.clicked.connect(self.accept)
        self.layout.addWidget(self.save_button)

    def keyPressEvent(self, event):
        key = event.key()
        modifiers = event.modifiers()
        key_sequence = QKeySequence(modifiers | key).toString(QKeySequence.NativeText)
        self.line_edit.setText(key_sequence)
        self.new_hotkey = key_sequence
        self.save_button.setEnabled(True)

    def assign_hotkey(self, sound_id):
        if self.exec_() == QDialog.Accepted and self.new_hotkey:
            self.db.add_hotkey(sound_id, self.new_hotkey)
            return self.new_hotkey
        return None

    def remove_hotkey(self, sound_id):
        self.db.remove_hotkey(sound_id)
