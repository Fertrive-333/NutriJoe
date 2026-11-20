import ctypes
import sys

from pathlib import Path
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QSettings

from App.Forms.main_window import MainWindow
from App.Translations.translator import Translator
from App.database import init_db
from PySide6.QtGui import QIcon

ICON_PATH = Path(__file__).resolve().parent / "App" / "Images" / "icon.ico"
def main():


    if sys.platform == "win32":
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("nutrijoe.app")
    
    app = QApplication(sys.argv) #Inicia grafica
    app.setWindowIcon(QIcon(str(ICON_PATH)))
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
    saved = QSettings("NutriJoe", "NutriJoe").value("language", "es")
    translator = Translator(saved)
    init_db()
    window = MainWindow(translator)
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
