import json
import re
from datetime import datetime
from pathlib import Path

from projects.project_structure import PROJECT_FOLDERS


class ProjectManager:
    """
    Responsible for creating and managing Composer projects.
    """

    def __init__(self, workspace_directory: Path) -> None:
        self.workspace_directory = workspace_directory
        self.projects_directory = workspace_directory / "projects"

        self.projects_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

    def create_project(self, project_name: str) -> Path:
        """
        Create a new project and return its directory path.

        Raises:
            ValueError: If the project name is invalid.
            FileExistsError: If the project already exists.
        """

        clean_project_name = project_name.strip()

        self._validate_project_name(clean_project_name)

        project_directory = (
            self.projects_directory / clean_project_name
        )

        if project_directory.exists():
            raise FileExistsError(
                f"Project '{clean_project_name}' already exists."
            )

        project_directory.mkdir(
            parents=True,
            exist_ok=False,
        )

        for folder_name in PROJECT_FOLDERS:
            folder_path = project_directory / folder_name
            folder_path.mkdir()

        project_information = {
            "name": clean_project_name,
            "version": "1.0.0",
            "description": "",
            "created_at": datetime.now().isoformat(
                timespec="seconds"
            ),
        }

        project_file = project_directory / "project.json"

        with project_file.open(
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(
                project_information,
                file,
                indent=4,
            )

        return project_directory

    def open_project(
    self,
    project_directory: Path,
) -> Path:
        """
        Validate an existing Composer project and return its path.

        A valid project must:
        - Exist
        - Be a directory
        - Contain a project.json file
        - Contain a valid project name in project.json
        """

        project_directory = Path(
            project_directory
        ).resolve()

        if not project_directory.exists():
            raise FileNotFoundError(
                f"Project directory does not exist: "
                f"{project_directory}"
            )

        if not project_directory.is_dir():
            raise ValueError(
                "The selected path is not a directory."
            )

        project_file = (
            project_directory / "project.json"
        )

        if not project_file.exists():
            raise ValueError(
                "The selected folder is not a valid "
                "Python Composer project because "
                "project.json was not found."
            )

        try:
            with project_file.open(
                "r",
                encoding="utf-8",
            ) as file:
                project_information = json.load(file)

        except json.JSONDecodeError as error:
            raise ValueError(
                "The project's project.json file "
                "contains invalid JSON."
            ) from error

        project_name = project_information.get(
            "name"
        )

        if (
            not isinstance(project_name, str)
            or not project_name.strip()
        ):
            raise ValueError(
                "The project's project.json file "
                "does not contain a valid project name."
            )

        return project_directory
        

    def _validate_project_name(
        self,
        project_name: str,
    ) -> None:
        """
        Validate the project name before creating folders.
        """

        if not project_name:
            raise ValueError(
                "Project name cannot be empty."
            )

        valid_name_pattern = r"^[A-Za-z0-9_-]+$"

        if not re.match(
            valid_name_pattern,
            project_name,
        ):
            raise ValueError(
                "Project name can only contain letters, "
                "numbers, underscores, and hyphens."
            )