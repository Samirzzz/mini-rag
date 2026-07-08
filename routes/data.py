from fastapi import FastAPI,APIRouter,UploadFile,Depends
from fastapi import status
from fastapi.responses import JSONResponse
import os 
from helpers.config import get_settings,Settings
from controllers import DataController,ProjectController
import aiofiles
data_router=APIRouter()

@data_router.post("/upload/{project_id}")
async def upload_data(project_id:str,file:UploadFile,
                      app_settings:Settings=Depends(get_settings)):
    is_valid=DataController().validate_uploaded_file(file=file)
    if not is_valid:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message":"invalid file"}
        )
    
    project_dir_path=ProjectController().get_project_path(project_id=project_id)
    file_path=os.path.join(project_dir_path,file.filename)
    async with aiofiles.open(file_path,"wb")as f:
        while chunk := await file.read(app_settings.FILE_DEFAULT_CHUNK_SIZE):
            await f.write(chunk)
    return  JSONResponse(
            content={"message":"File uploaded"}
        )
