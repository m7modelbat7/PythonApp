from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QComboBox,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QSplitter,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)


class ComposerPage(QWidget):
    """
    The central page used to create and edit Python services.

    This page does not create the complete application window.
    It will be placed inside MainWindow.
    """

    def __init__(self) -> None:
        super().__init__()

        self.build_ui()

    def build_ui(self) -> None:
        """
        Create all controls used by the service Composer.
        """

        main_layout = QVBoxLayout(self)

        title = QLabel("Python Service Composer")
        title.setStyleSheet(
            """
            QLabel {
                font-size: 24px;
                font-weight: bold;
            }
            """
        )
        main_layout.addWidget(title)

        self.service_name_input = QLineEdit()
        self.service_name_input.setPlaceholderText(
            "Enter service name"
        )

        main_layout.addWidget(QLabel("Service Name"))
        main_layout.addWidget(self.service_name_input)

        splitter = QSplitter(Qt.Orientation.Horizontal)

        self.code_editor = QTextEdit()
        self.code_editor.setPlaceholderText(
            "Write your Python service here...\n\n"
            "def run(inputs):\n"
            "    return {'message': 'Hello'}"
        )

        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)

        form_layout = QFormLayout()

        self.input_name_input = QLineEdit()
        self.input_name_input.setPlaceholderText(
            "Example: temperature"
        )

        self.input_type_combo = QComboBox()
        self.input_type_combo.addItems(
            [
                "String",
                "Integer",
                "Number",
                "Boolean",
                "JSON",
            ]
        )

        self.output_type_combo = QComboBox()
        self.output_type_combo.addItems(
            [
                "None",
                "String",
                "Integer",
                "Number",
                "Boolean",
                "JSON",
                "List",
            ]
        )

        form_layout.addRow(
            "Input Name",
            self.input_name_input,
        )

        form_layout.addRow(
            "Input Type",
            self.input_type_combo,
        )

        form_layout.addRow(
            "Output Type",
            self.output_type_combo,
        )

        right_layout.addLayout(form_layout)

        self.save_button = QPushButton("Save Service")
        self.execute_button = QPushButton("Execute Service")

        self.save_button.clicked.connect(self.save_service)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.execute_button)

        right_layout.addLayout(button_layout)
        right_layout.addStretch()

        splitter.addWidget(self.code_editor)
        splitter.addWidget(right_panel)

        splitter.setSizes([800, 400])

        main_layout.addWidget(splitter)

    def save_service(self) -> None:
        """
        Collect the service information entered by the developer.

        The service is not saved permanently yet.
        For now, the values are printed in the terminal.
        """

        service_name = self.service_name_input.text().strip()
        code = self.code_editor.toPlainText().strip()

        if not service_name:
            QMessageBox.warning(
                self,
                "Missing Service Name",
                "Please enter a service name.",
            )
            return

        if not code:
            QMessageBox.warning(
                self,
                "Missing Python Code",
                "Please enter Python code for the service.",
            )
            return

        input_name = self.input_name_input.text().strip()
        input_type = self.input_type_combo.currentText()
        output_type = self.output_type_combo.currentText()

        print("=" * 60)
        print("Save Service button clicked")
        print(f"Service Name: {service_name}")
        print(f"Input Name: {input_name}")
        print(f"Input Type: {input_type}")
        print(f"Output Type: {output_type}")
        print("Python Code:")
        print(code)
        print("=" * 60)

        QMessageBox.information(
            self,
            "Service Collected",
            (
                f"Service '{service_name}' was collected successfully.\n\n"
                "Permanent saving will be added in a later step."
            ),
        )