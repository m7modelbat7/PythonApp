from pathlib import Path

from PySide6.QtWidgets import (
    QInputDialog,
    QMainWindow,
    QMessageBox,
)

from projects.project_manager import ProjectManager
from ui.composer_page import ComposerPage
from ui.generated.ui_main_window import Ui_MainWindow


class DesignerMainWindow(QMainWindow):
    """
    Main window used while transitioning the application
    from a manually created interface to Qt Designer.
    """

    def __init__(self) -> None:
        super().__init__()

        # Build the visual structure created in Qt Designer.
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)


        # Display an initial message in the Output panel.
        self.ui.outputConsole.setPlainText(
            "Python Composer started successfully.\n"
            "Output and execution logs will appear here."
        )

        # No project is open when the application starts.
        self.current_project_directory: Path | None = None

        # ProjectManager contains the backend logic responsible
        # for creating project folders and project.json.
        self.project_manager = ProjectManager(
            self.get_workspace_directory()
        )

        # Create the existing Composer page.
        self.composer_page = ComposerPage()

        # Add ComposerPage to the stacked page container.
        self.ui.contentStack.addWidget(
            self.composer_page
        )

        # Display ComposerPage.
        self.ui.contentStack.setCurrentWidget(
            self.composer_page
        )

        # Prepare the initial Project Explorer content.
        self.initialize_project_explorer()

        # Connect Designer actions to Python methods.
        self.connect_actions()

    def get_workspace_directory(self) -> Path:
        """
        Return the workspace directory located in the project root.

        designer_window.py is located at:

            app/ui/designer_window.py

        Therefore, parent.parent.parent reaches the project root.
        """

        project_root = (
            Path(__file__).resolve().parent.parent.parent
        )

        return project_root / "workspace"

    def initialize_project_explorer(self) -> None:
        """
        Display the initial Project Explorer message.
        """

        self.ui.projectExplorerList.clear()

        self.ui.projectExplorerList.addItem(
            "No project is currently open"
        )

    def connect_actions(self) -> None:
        """
        Connect objects created in Designer to Python behavior.
        """

        self.ui.actionNewProject.triggered.connect(
            self.create_new_project
        )

        self.ui.actionSave.triggered.connect(
            self.composer_page.save_service
        )
        
        self.ui.actionExit.triggered.connect(
            self.close
        )

    def create_new_project(self) -> None:
        """
        Ask for a project name and create the project.
        """

        project_name, accepted = QInputDialog.getText(
            self,
            "New Project",
            "Enter project name:",
        )

        if not accepted:
            return

        try:
            project_directory = (
                self.project_manager.create_project(
                    project_name
                )
            )

        except ValueError as error:
            QMessageBox.warning(
                self,
                "Invalid Project Name",
                str(error),
            )
            return

        except FileExistsError as error:
            QMessageBox.warning(
                self,
                "Project Already Exists",
                str(error),
            )
            return

        except OSError as error:
            QMessageBox.critical(
                self,
                "Project Creation Failed",
                (
                    "The project could not be created.\n\n"
                    f"Reason: {error}"
                ),
            )
            return

        self.current_project_directory = project_directory

        self.load_project_into_explorer(
            project_directory
        )

        # Add the successful operation to the Output panel.
        self.ui.outputConsole.appendPlainText("")

        self.ui.outputConsole.appendPlainText(
            f"Project created: {project_directory}"
        )


        self.ui.statusbar.showMessage(
            f"Project: {project_directory.name}"
        )

        QMessageBox.information(
            self,
            "Project Created",
            (
                f"Project '{project_directory.name}' "
                "was created successfully."
            ),
        )

    def load_project_into_explorer(
        self,
        project_directory: Path,
    ) -> None:
        """
        Display the current project in Project Explorer.
        """

        self.ui.projectExplorerList.clear()

        self.ui.projectExplorerList.addItem(
            project_directory.name
        )

        self.ui.projectExplorerList.addItem(
            "    Services"
        )

        self.ui.projectExplorerList.addItem(
            "    Dashboards"
        )

        self.ui.projectExplorerList.addItem(
            "    Assets"
        )

        self.ui.projectExplorerList.addItem(
            "    Resources"
        )