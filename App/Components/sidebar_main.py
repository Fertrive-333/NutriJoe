
from pathlib import Path

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QFrame
)

from PySide6.QtGui import QPixmap
from PySide6.QtCore import Signal, Qt

from App.Translations.translator import Translator


BASE_DIR = Path(__file__).resolve().parent
path_logo = BASE_DIR / "Images" / "logo_joe.png"


class Sidebar(QWidget):

    section_changed = Signal(str)

    def __init__(self, translator=None):
        super().__init__()

        self.translator = translator or Translator("en")

        self.setObjectName("Sidebar")
        self.setFixedWidth(250)

        self.buttons = {}
        self.section_labels = {}

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(6)

        # HEADER
        self.create_header()

        # SEPARADOR
        separator = QFrame()
        separator.setObjectName("SidebarSeparator")
        separator.setFrameShape(QFrame.Shape.HLine)

        self.layout.addWidget(separator)
        self.layout.addSpacing(15)

        # MENU PRINCIPAL
        self.add_section_title("menu_main")

        self.add_menu_button("patients", "patients", "♙")
        self.add_menu_button("foods", "foods", "◈")
        self.add_menu_button("diets", "diets", "▤")
        self.add_menu_button("plans", "plans", "▦")

        self.layout.addSpacing(20)

        # GESTION
        self.add_section_title("menu_management")

        self.add_menu_button("reports", "reports", "▧")

        self.layout.addStretch()

        # CONFIGURACION
        self.add_menu_button("settings", "settings", "⚙")

        self.retranslate()

    # ---------------------------------
    # HEADER
    # ---------------------------------

    def create_header(self):

        header = QWidget()
        header.setObjectName("SidebarHeader")

        header_layout = QVBoxLayout(header)
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(0)

        self.logo = QLabel()
        self.logo.setObjectName("SidebarLogo")
        self.logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.logo.setFixedSize(250, 100)

        pixmap = QPixmap(str(path_logo))

        self.logo.setPixmap(
            pixmap.scaled(
                250,
                100,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
        )

        self.name = QLabel()
        self.name.setObjectName("SidebarBrand")

        self.subtitle = QLabel()
        self.subtitle.setObjectName("SidebarSubtitle")

        header_layout.addWidget(
            self.logo,
            alignment=Qt.AlignmentFlag.AlignLeft
        )

        header_layout.addSpacing(5)
        header_layout.addWidget(self.name)
        header_layout.addWidget(self.subtitle)

        self.layout.addWidget(header)

    # ---------------------------------
    # TITULOS DE SECCION
    # ---------------------------------

    def add_section_title(self, key):

        label = QLabel()
        label.setObjectName("SidebarSectionTitle")

        self.layout.addWidget(label)

        self.section_labels[key] = label

    # ---------------------------------
    # BOTONES
    # ---------------------------------

    def add_menu_button(self, text_key, identifier, icon):

        button = QPushButton()
        button.setObjectName("SidebarButton")
        button.setCheckable(True)
        button.setCursor(Qt.CursorShape.PointingHandCursor)

        button.clicked.connect(
            lambda checked=False, section=identifier:
            self.select_button(section)
        )

        self.layout.addWidget(button)

        self.buttons[identifier] = {
            "button": button,
            "text_key": text_key,
            "icon": icon
        }

    # ---------------------------------
    # TRADUCCIONES
    # ---------------------------------

    def retranslate(self):

        tr = self.translator.tr

        # HEADER
        self.name.setText(tr("brand_name"))
        self.subtitle.setText(tr("brand_subtitle"))

        # TITULOS
        for key, label in self.section_labels.items():
            label.setText(tr(key))

        # BOTONES
        for identifier, data in self.buttons.items():

            text = tr(data["text_key"])
            icon = data["icon"]

            data["button"].setText(f"{icon}    {text}")

    def change_language(self, language):

        self.translator.load_language(language)
        self.retranslate()

    # ---------------------------------
    # SELECCION DE SECCION
    # ---------------------------------

    def select_button(self, identifier):

        if identifier not in self.buttons:
            return

        for data in self.buttons.values():
            data["button"].setChecked(False)

        self.buttons[identifier]["button"].setChecked(True)

        self.section_changed.emit(identifier)
