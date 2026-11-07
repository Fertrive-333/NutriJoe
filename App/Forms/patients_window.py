# App/Pages/patients_page.py
from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton,
    QDialog, QLineEdit, QDialogButtonBox,
)

#Ventana flotante de añadir paciente
class AddPatientDialog(QDialog):
    def __init__(self, translator, parent=None):
        super().__init__(parent)
        self.setWindowTitle(translator.t("add_patients_name"))
        self.setModal(True)

        layout = QVBoxLayout(self)

        layout.addWidget(QLabel(translator.t("name"))) #Pone Widget de tipo Label

        self.name_input = QLineEdit() #Linea de edicion
        self.name_input.setPlaceholderText(translator.t("insert_name"))
        layout.addWidget(self.name_input) #La pone
        
        #Botones de OK y Cancel
        self.buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        layout.addWidget(self.buttons)

        # El botón OK solo se activa si hay nombre
        self.ok_button = self.buttons.button(QDialogButtonBox.Ok)
        self.ok_button.setEnabled(False) #Al inicio no se puede dar
        self.name_input.textChanged.connect(
            lambda text: self.ok_button.setEnabled(bool(text.strip()))
        )

    def patient_name(self):
        return self.name_input.text().strip()


class PatientsPage(QWidget):
    patient_added = Signal(str)  # emite el nombre del paciente nuevo

    def __init__(self, translator):
        super().__init__()
        self.translator = translator

        layout = QVBoxLayout(self)

        self.title = QLabel()
        self.title.setObjectName("PageTitle")
        layout.addWidget(self.title)

        #Botón de añadir paciente
        self.add_button = QPushButton() 
        self.add_button.clicked.connect(self.open_add_dialog)
        layout.addWidget(self.add_button)

        layout.addStretch()

        self.translator.language_changed.connect(self.retranslate_ui)
        self.retranslate_ui()

    def open_add_dialog(self): #Función al pulsar botón
        dialog = AddPatientDialog(self.translator, self) #Lanza ventana AddPatientDialog
        if dialog.exec() == QDialog.Accepted: #dialog.exec lanza la ventan, si das a aceptar hace lo de abajo que es mandar el nombre
            self.patient_added.emit(dialog.patient_name())

    def retranslate_ui(self):
        self.title.setText(self.translator.t("patients"))
        self.add_button.setText(self.translator.t("add_patients"))