
from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QStackedWidget,
    QLabel,
    QVBoxLayout
)

from PySide6.QtCore import Qt

from App.Components.sidebar_main import Sidebar


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("NutriJoe")

        # CONTENEDOR PRINCIPAL
        central = QWidget()
        main_layout = QHBoxLayout(central)

        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # SIDEBAR
        self.sidebar = Sidebar()

        # CONTENIDO
        self.pages = QStackedWidget()
        self.pages.setObjectName("MainContent")

        # Crear páginas provisionales
        self.sections = [
            "dashboard",
            "patients",
            "foods",
            "diets",
            "plans",
            "reports",
            "settings"
        ]

        for section in self.sections:

            page = QWidget()
            page_layout = QVBoxLayout(page)

            title = QLabel(section.replace("_", " ").title())

            title.setStyleSheet("""
                font-size: 30px;
                font-weight: bold;
            """)

            page_layout.addWidget(title)
            page_layout.addStretch()

            self.pages.addWidget(page)

        # Conectar navegación
        self.sidebar.section_changed.connect(
            self.change_page
        )

        # Añadir elementos
        main_layout.addWidget(self.sidebar)
        main_layout.addWidget(self.pages)

        self.setCentralWidget(central)

        self.showMaximized()

    def change_page(self, section):

        if section in self.sections:

            index = self.sections.index(section)

            self.pages.setCurrentIndex(index)
