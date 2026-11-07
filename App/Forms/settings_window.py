# App/Pages/settings_page.py
from pathlib import Path

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QButtonGroup
)
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt, QSize

FLAGS_DIR = Path(__file__).resolve().parent.parent / "Images"

LANGUAGES = ["es", "en"]

class SettingsPage(QWidget):
    def __init__(self,translator):
        super().__init__()
        self.translator = translator

        main_layout = QVBoxLayout(self)

        self.title = QLabel()
        self.title.setObjectName("PageTitle")
        main_layout.addWidget(self.title)

        self.language_label = QLabel()

        main_layout.addWidget(self.language_label)

        # BOTONES DE IDIOMA
        flags_layout = QHBoxLayout()
        flags_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.group = QButtonGroup(self)
        self.group.setExclusive(True)
        self.lang_buttons = {}

        for code in LANGUAGES:
            button = QPushButton()
            button.setObjectName("FlagButton")
            button.setCheckable(True)
            button.setIcon(QIcon(str(FLAGS_DIR / f"{code}.png")))
            button.setIconSize(QSize(48, 32))
            button.setCursor(Qt.CursorShape.PointingHandCursor)

            button.clicked.connect(
                lambda checked=False, c=code: self.translator.set_language(c)
            )

            self.group.addButton(button)
            flags_layout.addWidget(button)
            self.lang_buttons[code] = button

        main_layout.addLayout(flags_layout)
        main_layout.addStretch()

        self.translator.language_changed.connect(self.retranslate)
        self.retranslate()
    
    def retranslate(self):
        t = self.translator.t
        self.title.setText(t("settings"))
        self.language_label.setText(t("language"))

        # Marca como seleccionado el idioma actual
        current = self.lang_buttons.get(self.translator.language)
        if current:
            current.setChecked(True)