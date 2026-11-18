# App/Pages/foods_page.py
from PySide6.QtCore import Signal, Qt
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton,
    QDialog, QLineEdit, QDialogButtonBox, QFormLayout, QDoubleSpinBox,
    QListWidget
)


class AddFoodDialog(QDialog):
    def __init__(self, translator, parent=None):
        super().__init__(parent)
        self.translator = translator
        self.setObjectName("AddFoodDialog")
        self.setWindowTitle(translator.t("add_food_title"))
        self.setModal(True)
        self.setMinimumWidth(420)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        self.form_title = QLabel(translator.t("add_food_title"))
        self.form_title.setObjectName("DialogTitle")
        layout.addWidget(self.form_title)

        form = QFormLayout()
        form.setSpacing(12)
        form.setLabelAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        form.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.AllNonFixedFieldsGrow)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText(translator.t("insert_food_name"))
        self.name_input.setMinimumHeight(36)
        form.addRow(translator.t("name"), self.name_input)

        self.calories = QDoubleSpinBox()
        self.calories.setRange(0, 10000)
        self.calories.setDecimals(1)
        self.calories.setSuffix(" kcal")
        self.calories.setMinimumHeight(36)
        form.addRow(translator.t("calories"), self.calories)

        self.protein = QDoubleSpinBox()
        self.protein.setRange(0, 1000)
        self.protein.setDecimals(1)
        self.protein.setSuffix(" g")
        self.protein.setMinimumHeight(36)
        form.addRow(translator.t("protein"), self.protein)

        self.carbs = QDoubleSpinBox()
        self.carbs.setRange(0, 1000)
        self.carbs.setDecimals(1)
        self.carbs.setSuffix(" g")
        self.carbs.setMinimumHeight(36)
        form.addRow(translator.t("carbs"), self.carbs)

        self.fat = QDoubleSpinBox()
        self.fat.setRange(0, 1000)
        self.fat.setDecimals(1)
        self.fat.setSuffix(" g")
        self.fat.setMinimumHeight(36)
        form.addRow(translator.t("fat"), self.fat)

        layout.addLayout(form)

        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        layout.addWidget(self.buttons)

        self.ok_button = self.buttons.button(QDialogButtonBox.Ok)
        self.cancel_button = self.buttons.button(QDialogButtonBox.Cancel)
        if self.ok_button:
            self.ok_button.setObjectName("PrimaryDialogButton")
            self.ok_button.setCursor(Qt.CursorShape.PointingHandCursor)
            self.ok_button.setDefault(True)
        if self.cancel_button:
            self.cancel_button.setObjectName("SecondaryDialogButton")
            self.cancel_button.setCursor(Qt.CursorShape.PointingHandCursor)

        self.ok_button.setEnabled(False)
        self.name_input.textChanged.connect(
            lambda text: self.ok_button.setEnabled(bool(text.strip()))
        )

    def food_data(self):
        return {
            "name": self.name_input.text().strip(),
            "calories": self.calories.value(),
            "protein": self.protein.value(),
            "carbs": self.carbs.value(),
            "fat": self.fat.value(),
        }


class FoodsPage(QWidget):
    food_added = Signal(dict)

    def __init__(self, translator):
        super().__init__()
        self.translator = translator
        self.foods = []

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(14)

        self.title = QLabel()
        self.title.setObjectName("PageTitle")
        layout.addWidget(self.title)

        self.add_button = QPushButton()
        self.add_button.setObjectName("PrimaryButton")
        self.add_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.add_button.clicked.connect(self.open_add_dialog)
        layout.addWidget(self.add_button, alignment=Qt.AlignmentFlag.AlignLeft)

        self.search_input = QLineEdit()
        self.search_input.setObjectName("SearchInput")
        self.search_input.setClearButtonEnabled(True)
        self.search_input.setMinimumHeight(36)
        self.search_input.textChanged.connect(self._refresh_food_list)
        layout.addWidget(self.search_input)

        self.food_list = QListWidget()
        self.food_list.setObjectName("FoodList")
        self.food_list.setSpacing(4)
        layout.addWidget(self.food_list)

        self.translator.language_changed.connect(self.retranslate_ui)
        self.retranslate_ui()

    def open_add_dialog(self):
        dialog = AddFoodDialog(self.translator, self)
        if dialog.exec() == QDialog.Accepted:
            data = dialog.food_data()
            self.foods.append(data)
            self.food_added.emit(data)
            self._refresh_food_list()

    def _add_food_item(self, data):
        text = (
            f"{data['name']}  •  {data['calories']:.1f} kcal  "
            f"(P: {data['protein']:.1f} g  |  C: {data['carbs']:.1f} g  |  G: {data['fat']:.1f} g)"
        )
        self.food_list.addItem(text)

    def _refresh_food_list(self):
        query = self.search_input.text().strip().lower()
        self.food_list.clear()
        for food in self.foods:
            if not query or query in food["name"].lower():
                self._add_food_item(food)

    def retranslate_ui(self):
        self.title.setText(self.translator.t("foods"))
        self.add_button.setText(self.translator.t("add_food_manual"))
        self.search_input.setPlaceholderText(self.translator.t("search_food"))