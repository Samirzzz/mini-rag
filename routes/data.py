from fastapi import FastAPI,APIRouter,UploadFile,Depends
from fastapi import status
from fastapi.responses import JSONResponse
import os 
from helpers.config import get_settings,Settings
from controllers import DataController,ProjectController,ProcessController
import aiofiles
from .schemas.data import ProcessRequest
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

@data_router.post("/process/{project_id}")
async def process_endpoint(project_id:str,process_request:ProcessRequest):
    file_id=process_request.file_id
    chunk_size=process_request.chunk_size
    overlap_size=process_request.overlap
    process_controller=ProcessController(project_id=project_id)
    file_content=process_controller.get_file_content(file_id=file_id)
    file_chunks=process_controller.process_file_content(file_content=file_content,file_id=file_id,chunk_size=chunk_size,overlap_size=overlap_size)
    if file_chunks is None or len(file_chunks)==0:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "message":"processing failed"
            }
        )
    return file_chunks

    