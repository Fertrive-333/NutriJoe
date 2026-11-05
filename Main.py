
import sys

from pathlib import Path
from PySide6.QtWidgets import QApplication

from App.Forms.main_window import MainWindow


def main():

    app = QApplication(sys.argv)

    app.setApplicationName("NutriJoe")

    # Cargar stylesheet
    stylesheet_path = (
        Path(__file__).parent
        / "App"
        / "Resources"
        / "Styles"
        / "nutri_styles.qss"
    )

    with open(stylesheet_path, "r", encoding="utf-8") as file:
        app.setStyleSheet(file.read())

    # Abrir ventana
    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
