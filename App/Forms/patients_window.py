# App/Pages/patients_page.py
from PySide6.QtCore import QDate, Qt
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QDialog, QLineEdit, QDialogButtonBox, QComboBox,
    QDateEdit, QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView
)
import App.database as db

#Ventana flotante de añadir paciente
class AddPatientDialog(QDialog):
    def __init__(self, translator, parent=None):
        super().__init__(parent)
        self.setObjectName("AddPatientDialog")  # para que le apliquen los estilos
        self.setWindowTitle(translator.t("add_patients_name"))
        self.setModal(True)
        self.setMinimumWidth(380)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(8)

        # Título del diálogo
        title = QLabel(translator.t("add_patients_name"))
        title.setObjectName("DialogTitle")
        layout.addWidget(title)

        # Name
        layout.addWidget(QLabel(translator.t("name")))
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText(translator.t("insert_name"))
        layout.addWidget(self.name_input)

        # Tlf
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
        self.birthday_input.setCalendarPopup(True)
        self.birthday_input.setDisplayFormat("dd/MM/yyyy")
        self.birthday_input.setMaximumDate(QDate.currentDate())
        self.birthday_input.setDate(QDate(2000, 1, 1))
        layout.addWidget(self.birthday_input)

        layout.addSpacing(8)

        # Botones de OK y Cancel
        self.buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        layout.addWidget(self.buttons)

        # Estilos de los botones (los mismos que en foods)
        self.ok_button = self.buttons.button(QDialogButtonBox.Ok)
        self.ok_button.setObjectName("PrimaryDialogButton")
        self.ok_button.setCursor(Qt.PointingHandCursor)

        self.cancel_button = self.buttons.button(QDialogButtonBox.Cancel)
        self.cancel_button.setObjectName("SecondaryDialogButton")
        self.cancel_button.setCursor(Qt.PointingHandCursor)

        # El botón OK solo se activa si hay nombre
        self.ok_button.setEnabled(False)
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
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(12)

        self.title = QLabel()
        self.title.setObjectName("PageTitle")
        layout.addWidget(self.title)

        # Botón de añadir paciente (arriba a la izquierda, sin estirarse)
        top_bar = QHBoxLayout()
        self.add_button = QPushButton()
        self.add_button.setObjectName("PrimaryButton")
        self.add_button.setCursor(Qt.PointingHandCursor)
        self.add_button.clicked.connect(self.open_add_dialog)
        top_bar.addWidget(self.add_button)
        top_bar.addStretch()
        layout.addLayout(top_bar)

        # Buscador
        self.search_patient = QLineEdit()
        self.search_patient.setObjectName("SearchInput")
        self.search_patient.setClearButtonEnabled(True)
        self.search_patient.setMinimumHeight(36)
        # self.search_patient.textChanged.connect(...)
        layout.addWidget(self.search_patient)

        # Tabla
        self.patient_table = QTableWidget(0, 4)
        self.patient_table.setObjectName("PatientTable")
        self.patient_table.verticalHeader().setVisible(False)
        self.patient_table.verticalHeader().setDefaultSectionSize(44)  # filas más altas
        self.patient_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.patient_table.horizontalHeader().setHighlightSections(False)
        self.patient_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.patient_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.patient_table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.patient_table.setShowGrid(False)
        self.patient_table.setFocusPolicy(Qt.NoFocus)  # sin recuadro de foco punteado
        layout.addWidget(self.patient_table, stretch=1)

        self.refresh_list()  # 1ª llamada: carga los pacientes al abrir la página
        self.translator.language_changed.connect(self.retranslate_ui)
        self.retranslate_ui()

    def open_add_dialog(self):
        dialog = AddPatientDialog(self.translator, self)
        if dialog.exec() == QDialog.Accepted:
            db.add_patient(
                dialog.patient_name(),
                dialog.patient_tlf(),
                dialog.patient_gender(),
                dialog.patient_birthday(),
            )
            self.refresh_list()  # 2ª llamada: repinta con el paciente nuevo

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
        self.patient_table.setRowCount(len(pacientes))
        for fila, (id_paciente, nombre, tlf, gender, birthday) in enumerate(pacientes):
            valores = [nombre, tlf or "", gender or "", birthday or ""]
            for columna, texto in enumerate(valores):
                item = QTableWidgetItem(texto)
                item.setTextAlignment(Qt.AlignCenter)   # centra horizontal y verticalmente
                if columna == 0:
                    item.setData(Qt.UserRole, id_paciente)   # id escondido en la 1ª columna
                self.patient_table.setItem(fila, columna, item)
