from .BaseController import BaseController
from fastapi import UploadFile,status
from fastapi.responses import JSONResponse
import os
class ProjectController(BaseController):
    def __init__(self):
        super().__init__()

    def get_project_path(self, project_id: str):
        project_directory = os.path.join(self.file_dir, project_id)
        os.makedirs(project_directory, exist_ok=True)
        return project_directory



