from fastapi import FastAPI,APIRouter
from helpers.config import get_settings
import os
base_router=APIRouter()

@base_router.get("/")
def welcome():
    sett=get_settings()
    app_name=sett.APP_NAME
    return {"message":"helloo",
            "APP-NAME":{app_name}}