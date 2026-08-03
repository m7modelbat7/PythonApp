from PySide6.QtWidgets import QMainWindow

from ui.generated.ui_main_window import Ui_MainWindow


class DesignerMainWindow(QMainWindow):
    """
    Temporary main window used while transitioning
    the application to Qt Designer.
    """

    def __init__(self) -> None:
        super().__init__()

        # Create the interface generated from main_window.ui.
        self.ui = Ui_MainWindow()

        # Place the generated interface inside this real QMainWindow.
        self.ui.setupUi(self)

        # Connect the Designer Exit action to QMainWindow.close().
        self.ui.actionExit.triggered.connect(
            self.close
        )