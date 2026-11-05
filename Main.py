import sys

from PySide6.QtWidgets import QApplication
from App.Forms.main_window import MainWindow


def main():
    app = QApplication(sys.argv) #Inicia motor gráfico

    app.setApplicationName("NutriJoe")  #Da nombre

    window = MainWindow() #Crea Main Windows
    window.show() #Muestra la ventana main

    sys.exit(app.exec())


if __name__ == "__main__":
    main()