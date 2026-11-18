# App/Pages/patients_page.py
from PySide6.QtCore import Signal, QDate
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton,
    QDialog, QLineEdit, QDialogButtonBox,QComboBox,
    QDateEdit,
)
import App.database as db

#Ventana flotante de añadir paciente
class AddPatientDialog(QDialog):
    def __init__(self, translator, parent=None):
        super().__init__(parent)
        self.setWindowTitle(translator.t("add_patients_name"))
        self.setModal(True)

        layout = QVBoxLayout(self)

        #Name
        layout.addWidget(QLabel(translator.t("name"))) #Pone Widget de tipo Label
        self.name_input = QLineEdit() #Linea de edicion
        self.name_input.setPlaceholderText(translator.t("insert_name"))
        layout.addWidget(self.name_input) #La pone
        
        #Tlf
        layout.addWidget(QLabel(translator.t("tlf")))
        self.tlf_input = QLineEdit()
        layout.addWidget(self.tlf_input)

        #Gender
        layout.addWidget(QLabel(translator.t("gender")))
        self.gender_input = QComboBox()
        self.gender_input.addItem(translator.t("gender_m"), "M")
        self.gender_input.addItem(translator.t("gender_f"), "F")
        layout.addWidget(self.gender_input)

        #Birthday
        layout.addWidget(QLabel(translator.t("birthday")))
        self.birthday_input = QDateEdit()
        self.birthday_input.setCalendarPopup(True)          # calendario desplegable
        self.birthday_input.setDisplayFormat("dd/MM/yyyy")
        self.birthday_input.setMaximumDate(QDate.currentDate())  # no permite fechas futuras
        self.birthday_input.setDate(QDate(2000, 1, 1))      # fecha inicial
        layout.addWidget(self.birthday_input)

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
    
    def patient_tlf(self):
        return self.tlf_input.text().strip()

    def patient_gender(self):
        return self.gender_input.currentData()   # "M", "F"

    def patient_birthday(self):
        return self.birthday_input.date().toString("yyyy-MM-dd")


class PatientsPage(QWidget):

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
            
            nombre = dialog.patient_name()
            telefono = dialog.patient_tlf()
            genero = dialog.patient_gender()
            birth_date = dialog.patient_birthday()

            db.add_patient(nombre,telefono,genero,birth_date)   #Funcion de añadir persona a database

    def retranslate_ui(self):
        self.title.setText(self.translator.t("patients"))
        self.add_button.setText(self.translator.t("add_patients"))