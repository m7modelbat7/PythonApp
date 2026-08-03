from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QDockWidget,
    QInputDialog,
    QLabel,
    QListWidget,
    QMainWindow,
    QMessageBox,
    QPlainTextEdit,
    QStatusBar,
    QToolBar,
)

from projects.project_manager import ProjectManager
from ui.composer_page import ComposerPage


class MainWindow(QMainWindow):
    """
    Main desktop window for the Python Composer application.
    """

    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("Python Composer")
        self.resize(1400, 850)

        self.current_project_directory: Path | None = None

        self.project_manager = ProjectManager(
            self.get_workspace_directory()
        )

        self.create_actions()
        self.create_menu_bar()
        self.create_toolbar()
        self.create_project_explorer()
        self.create_output_panel()
        self.create_composer_page()
        self.create_status_bar()

    def get_workspace_directory(self) -> Path:
        """
        Return the root workspace directory.

        The application file is located at:

        app/ui/main_window.py

        Therefore, parent.parent.parent reaches
        the project root.
        """

        project_root = Path(__file__).resolve().parent.parent.parent

        return project_root / "workspace"

    def create_actions(self) -> None:
        self.new_project_action = QAction(
            "New Project",
            self,
        )

        self.open_project_action = QAction(
            "Open Project",
            self,
        )

        self.save_action = QAction(
            "Save",
            self,
        )

        self.exit_action = QAction(
            "Exit",
            self,
        )

        self.run_action = QAction(
            "Run Service",
            self,
        )

        self.new_project_action.triggered.connect(
            self.create_new_project
        )

        self.exit_action.triggered.connect(
            self.close
        )

    def create_menu_bar(self) -> None:
        menu_bar = self.menuBar()

        file_menu = menu_bar.addMenu("File")
        file_menu.addAction(self.new_project_action)
        file_menu.addAction(self.open_project_action)
        file_menu.addAction(self.save_action)
        file_menu.addSeparator()
        file_menu.addAction(self.exit_action)

        menu_bar.addMenu("Edit")
        menu_bar.addMenu("View")
        menu_bar.addMenu("Project")

        run_menu = menu_bar.addMenu("Run")
        run_menu.addAction(self.run_action)

        menu_bar.addMenu("Help")

    def create_toolbar(self) -> None:
        toolbar = QToolBar("Main Toolbar")
        toolbar.setMovable(False)

        toolbar.addAction(self.new_project_action)
        toolbar.addAction(self.open_project_action)
        toolbar.addAction(self.save_action)
        toolbar.addSeparator()
        toolbar.addAction(self.run_action)

        self.addToolBar(toolbar)

    def create_project_explorer(self) -> None:
        project_dock = QDockWidget(
            "Project Explorer",
            self,
        )

        project_dock.setAllowedAreas(
            Qt.DockWidgetArea.LeftDockWidgetArea
            | Qt.DockWidgetArea.RightDockWidgetArea
        )

        self.project_explorer = QListWidget()

        self.project_explorer.addItem(
            "No project is currently open"
        )

        project_dock.setWidget(
            self.project_explorer
        )

        self.addDockWidget(
            Qt.DockWidgetArea.LeftDockWidgetArea,
            project_dock,
        )

    def create_output_panel(self) -> None:
        output_dock = QDockWidget(
            "Output",
            self,
        )

        output_dock.setAllowedAreas(
            Qt.DockWidgetArea.BottomDockWidgetArea
            | Qt.DockWidgetArea.TopDockWidgetArea
        )

        self.output_console = QPlainTextEdit()
        self.output_console.setReadOnly(True)

        self.output_console.setPlainText(
            "Python Composer started successfully.\n"
            "Output and execution logs will appear here."
        )

        output_dock.setWidget(
            self.output_console
        )

        self.addDockWidget(
            Qt.DockWidgetArea.BottomDockWidgetArea,
            output_dock,
        )

    def create_composer_page(self) -> None:
        self.composer_page = ComposerPage()

        self.setCentralWidget(
            self.composer_page
        )

    def create_status_bar(self) -> None:
        self.status_label = QLabel("Ready")

        status_bar = QStatusBar()
        status_bar.addWidget(
            self.status_label
        )

        self.setStatusBar(
            status_bar
        )

    def create_new_project(self) -> None:
        """
        Ask the user for a project name and create the project.
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

        self.current_project_directory = (
            project_directory
        )

        self.load_project_into_explorer(
            project_directory
        )

        self.output_console.appendPlainText(
            ""
        )

        self.output_console.appendPlainText(
            f"Project created: {project_directory}"
        )

        self.status_label.setText(
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
        Display the current project inside Project Explorer.
        """

        self.project_explorer.clear()

        self.project_explorer.addItem(
            project_directory.name
        )

        self.project_explorer.addItem(
            "    Services"
        )

        self.project_explorer.addItem(
            "    Dashboards"
        )

        self.project_explorer.addItem(
            "    Assets"
        )

        self.project_explorer.addItem(
            "    Resources"
        )