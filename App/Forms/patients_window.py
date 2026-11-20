# App/Pages/patients_page.py
from PySide6.QtCore import Signal, QDate, Qt
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton,
    QDialog, QLineEdit, QDialogButtonBox, QComboBox,
    QDateEdit, QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView
)
import App.database as db


# Ventana flotante de añadir paciente
class AddPatientDialog(QDialog):
    def __init__(self, translator, parent=None):
        super().__init__(parent)
        self.setWindowTitle(translator.t("add_patients_name"))
        self.setModal(True)

        layout = QVBoxLayout(self)

        # Name
        layout.addWidget(QLabel(translator.t("name")))  # Pone Widget de tipo Label
        self.name_input = QLineEdit()  # Linea de edicion
        self.name_input.setPlaceholderText(translator.t("insert_name"))
        layout.addWidget(self.name_input)  # La pone

        # Tlf
        layout.addWidget(QLabel(translator.t("tlf")))
        self.tlf_input = QLineEdit()
        layout.addWidget(self.tlf_input)

        # Gender
        layout.addWidget(QLabel(translator.t("gender")))
        self.gender_input = QComboBox()
        self.gender_input.addItem(translator.t("gender_m"), "M")
        self.gender_input.addItem(translator.t("gender_f"), "F")
        layout.addWidget(self.gender_input)

        # Birthday
        layout.addWidget(QLabel(translator.t("birthday")))
        self.birthday_input = QDateEdit()
        self.birthday_input.setCalendarPopup(True)  # calendario desplegable
        self.birthday_input.setDisplayFormat("dd/MM/yyyy")
        self.birthday_input.setMaximumDate(QDate.currentDate())  # no permite fechas futuras
        self.birthday_input.setDate(QDate(2000, 1, 1))  # fecha inicial
        layout.addWidget(self.birthday_input)

        # Botones de OK y Cancel
        self.buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        layout.addWidget(self.buttons)

        # El botón OK solo se activa si hay nombre
        self.ok_button = self.buttons.button(QDialogButtonBox.Ok)
        self.ok_button.setEnabled(False)  # Al inicio no se puede dar
        self.name_input.textChanged.connect(
            lambda text: self.ok_button.setEnabled(bool(text.strip()))
        )

    def patient_name(self):
        return self.name_input.text().strip()

    def patient_tlf(self):
        return self.tlf_input.text().strip()

    def patient_gender(self):
        return self.gender_input.currentData()  # "M", "F"

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

        # Botón de añadir paciente
        self.add_button = QPushButton()
        self.add_button.clicked.connect(self.open_add_dialog)
        layout.addWidget(self.add_button)

        self.search_patient = QLineEdit()
        self.search_patient.setObjectName("SearchPatient")
        self.search_patient.setClearButtonEnabled(True)
        self.search_patient.setMinimumHeight(36)
        # self.search_patient.textChanged.connect(self._refresh_food_list)
        layout.addWidget(self.search_patient)

        self.patient_table = QTableWidget(0, 4)   # 0 filas, 4 columnas
        self.patient_table.setObjectName("PatientTable")
        self.patient_table.verticalHeader().setVisible(False)   # oculta los números de fila
        self.patient_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # columnas reparten el ancho
        self.patient_table.setEditTriggers(QAbstractItemView.NoEditTriggers)  # no se edita al hacer doble clic
        self.patient_table.setSelectionBehavior(QAbstractItemView.SelectRows)  # selecciona la fila entera
        layout.addWidget(self.patient_table, stretch=1)

        self.refresh_list()  # 1ª llamada: carga los pacientes al abrir la página
        self.translator.language_changed.connect(self.retranslate_ui)
        self.retranslate_ui()

    def open_add_dialog(self):  # Función al pulsar botón
        dialog = AddPatientDialog(self.translator, self)  # Lanza ventana AddPatientDialog
        if dialog.exec() == QDialog.Accepted:  # exec() la muestra; si das a OK entra aquí

            nombre = dialog.patient_name()
            telefono = dialog.patient_tlf()
            genero = dialog.patient_gender()
            birth_date = dialog.patient_birthday()

            db.add_patient(nombre, telefono, genero, birth_date)  # Guarda en SQLite
            self.refresh_list()  # 2ª llamada: repinta la lista con el paciente nuevo

    def retranslate_ui(self):
        self.title.setText(self.translator.t("patients"))
        self.add_button.setText(self.translator.t("add_patients"))
        self.patient_table.setHorizontalHeaderLabels([
            self.translator.t("name"),
            self.translator.t("tlf"),
            self.translator.t("gender"),
            self.translator.t("birthday"),
        ])

    def refresh_list(self):
        pacientes = db.get_patients()
        self.patient_table.setRowCount(len(pacientes))   # tantas filas como pacientes
        for fila, (id_paciente, nombre, tlf, gender, birthday) in enumerate(pacientes):
            item_nombre = QTableWidgetItem(nombre)
            item_nombre.setData(Qt.UserRole, id_paciente)   # id escondido en la 1ª columna
            self.patient_table.setItem(fila, 0, item_nombre)
            self.patient_table.setItem(fila, 1, QTableWidgetItem(tlf or ""))
            self.patient_table.setItem(fila, 2, QTableWidgetItem(gender or ""))
            self.patient_table.setItem(fila, 3, QTableWidgetItem(birthday or ""))