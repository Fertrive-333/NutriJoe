
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QFrame
)

from PySide6.QtCore import Signal, Qt


class Sidebar(QWidget):

    # Señal que comunica la sección seleccionada
    section_changed = Signal(str)

    def __init__(self):
        super().__init__()

        self.setObjectName("Sidebar")
        self.setFixedWidth(250)

        self.buttons = {}

        # Layout principal
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(12, 20, 12, 20)
        self.layout.setSpacing(6)

        # LOGOTIPO Y NOMBRE
        self.create_header()

        # Separador
        separator = QFrame()
        separator.setObjectName("SidebarSeparator")
        separator.setFrameShape(QFrame.Shape.HLine)

        self.layout.addWidget(separator)
        self.layout.addSpacing(15)

        # MENÚ PRINCIPAL
        self.add_section_title("MENÚ PRINCIPAL")

        self.add_menu_button("Dashboard", "dashboard", "⌂")
        self.add_menu_button("Pacientes", "patients", "♙")
        self.add_menu_button("Alimentos", "foods", "◈")
        self.add_menu_button("Dietas", "diets", "▤")
        self.add_menu_button("Planes nutricionales", "plans", "▦")

        self.layout.addSpacing(20)

        # GESTIÓN
        self.add_section_title("GESTIÓN")

        self.add_menu_button("Informes", "reports", "▧")

        self.layout.addStretch()

        # CONFIGURACIÓN
        self.add_menu_button("Configuración", "settings", "⚙")

        # Seleccionar Dashboard inicialmente
        self.select_button("dashboard")

    def create_header(self):

        header = QWidget()
        header.setObjectName("SidebarHeader")

        header_layout = QVBoxLayout(header)
        header_layout.setContentsMargins(12, 10, 12, 20)
        header_layout.setSpacing(4)

        logo = QLabel("N")
        logo.setObjectName("SidebarLogo")
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo.setFixedSize(42, 42)

        name = QLabel("NutriJoe")
        name.setObjectName("SidebarBrand")

        subtitle = QLabel("NUTRITION MANAGEMENT")
        subtitle.setObjectName("SidebarSubtitle")

        header_layout.addWidget(logo, alignment=Qt.AlignmentFlag.AlignLeft)
        header_layout.addSpacing(5)
        header_layout.addWidget(name)
        header_layout.addWidget(subtitle)

        self.layout.addWidget(header)

    def add_section_title(self, title):

        label = QLabel(title)
        label.setObjectName("SidebarSectionTitle")

        self.layout.addWidget(label)

    def add_menu_button(self, text, identifier, icon):

        button = QPushButton(f"{icon}    {text}")

        button.setObjectName("SidebarButton")
        button.setCheckable(True)
        button.setCursor(Qt.CursorShape.PointingHandCursor)

        button.clicked.connect(
            lambda checked=False, section=identifier:
            self.select_button(section)
        )

        self.layout.addWidget(button)

        self.buttons[identifier] = button

    def select_button(self, identifier):

        if identifier not in self.buttons:
            return

        # Desmarcar todos los botones
        for button in self.buttons.values():
            button.setChecked(False)

        # Marcar el seleccionado
        self.buttons[identifier].setChecked(True)

        # Avisar a la ventana principal
        self.section_changed.emit(identifier)
