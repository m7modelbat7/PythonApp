import sys

from PySide6.QtWidgets import QApplication

from ui.designer_window import DesignerMainWindow


def main() -> None:
    """
    Start the Python Composer desktop application.
    """

    app = QApplication(sys.argv)

    window = DesignerMainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()