from PySide6.QtWidgets import QMainWindow

from ui.composer_page import ComposerPage
from ui.generated.ui_main_window import Ui_MainWindow


class DesignerMainWindow(QMainWindow):
    """
    Temporary main window used while transitioning
    the application to Qt Designer.
    """

    def __init__(self) -> None:
        super().__init__()

        # Build the visual structure created in Qt Designer.
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Create the existing Composer page.
        self.composer_page = ComposerPage()

        # Add the existing Python page to the stacked page container.
        self.ui.contentStack.addWidget(
            self.composer_page
        )

        # Tell the stacked widget to display ComposerPage.
        self.ui.contentStack.setCurrentWidget(
            self.composer_page
        )

        # Connect File -> Exit to the window close method.
        self.ui.actionExit.triggered.connect(
            self.close
        )