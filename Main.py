
import sys

from pathlib import Path
from PySide6.QtWidgets import QApplication

from App.Forms.main_window import MainWindow
from App.Translations.translator import Translator


def main():

    app = QApplication(sys.argv) #Inicia grafica

    app.setApplicationName("NutriJoe") 

    # Path a estilos
    stylesheet_path = (
        Path(__file__).parent
        / "App"
        / "Resources"
        / "Styles"
        / "nutri_styles.qss"
    )

    #Carga los estilos
    app.setStyleSheet(stylesheet_path.read_text(encoding="utf-8"))

    # Abrir ventana
    translator = Translator("es")
    window = MainWindow(translator)
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
