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