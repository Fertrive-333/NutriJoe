
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
from App.Forms.dashboard_window import DashboardPage
from App.Forms.patients_window import PatientsPage
from App.Forms.foods_window import FoodsPage
from App.Forms.settings_window import SettingsPage


class MainWindow(QMainWindow):

    def __init__(self,translator):
        super().__init__()
        self.setWindowTitle("NutriJoe") #Nombre de la app que sale arriba en la ventana de google

        self.translator = translator
        self.sidebar = Sidebar(translator)
        # CONTENEDOR PRINCIPAL
        central = QWidget()
        main_layout = QHBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0) #margenes de lo de la izq respecto a la sidebar
        main_layout.setSpacing(0)

        # CONTENIDO
        self.pages = QStackedWidget()
        self.pages.setObjectName("MainContent")

        # Crear páginas provisionales
        self.page_map = {
            "dashboard": DashboardPage(translator),
            "patients": PatientsPage(translator),
            "foods": FoodsPage(translator),
            "settings": SettingsPage(translator)
        }

        for page in self.page_map.values():
            self.pages.addWidget(page) #Crea las paginas

        # Conectar navegación
        self.sidebar.section_changed.connect(
            self.change_page
        )

        # Añadir elementos en la main_layout
        main_layout.addWidget(self.sidebar) #Sidebar a la izq
        main_layout.addWidget(self.pages) #Pagina a la derecha
        self.setCentralWidget(central)
        self.showMaximized()

    def change_page(self, section: str):
        page = self.page_map.get(section)
        if page:
            self.pages.setCurrentWidget(page)
