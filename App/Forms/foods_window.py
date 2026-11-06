# App/Pages/patients_page.py
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel


class FoodsPage(QWidget):
    def __init__(self,translator):
        super().__init__()
        self.translator = translator

        layout = QVBoxLayout(self)

        self.title = QLabel()
        self.title.setObjectName("PageTitle")
        layout.addWidget(self.title)
        layout.addStretch()

        self.translator.language_changed.connect(self.retranslate_ui)
        self.retranslate_ui()
    
    def retranslate_ui(self):
        self.title.setText(self.translator.t("foods"))