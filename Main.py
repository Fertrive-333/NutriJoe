import sys
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout

# Crear la aplicación
app = QApplication(sys.argv)

# Crear la ventana
ventana = QWidget()
ventana.setWindowTitle("Mi primera aplicación")
ventana.resize(600, 400)

# Crear el texto
texto = QLabel("¡Hola Joe!")

# Centrar el texto
texto.setStyleSheet("font-size: 30px;")
texto.setAlignment(__import__("PySide6.QtCore", fromlist=["Qt"]).Qt.AlignmentFlag.AlignCenter)

# Colocar el texto en la ventana
layout = QVBoxLayout()
layout.addWidget(texto)
ventana.setLayout(layout)

# Mostrar ventana
ventana.show()

# Mantener la aplicación abierta
sys.exit(app.exec())
