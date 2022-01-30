from array import array
import os
import uvicorn
from distutils.log import error
from importlib.resources import path
import fastapi
from typing import Optional
from pydantic import BaseModel
import time
import final_tile_error
import tile_error
import tile_error_recognition
import numpy as np
app=fastapi.FastAPI()

tiles={}

@app.get("/get-grade")
async def get_grade(tile_id:str):
    tile_geo = tile_error_recognition.Tile_Geo(tiles[tile_id], [987, 1076, 1131, 1148, 1186])
    return tile_geo.get_grade()

@app.post("/post_tile")
async def create_tile(tile_id:str, tile_array:list):
    tiles[tile_id]= tile_array
    return tiles



if __name__ == "__main__":
    script_name =os.path.basename(__file__).replace('.py','')
    uvicorn.run("fastapi_req:app", host="0.0.0.0", port=5000, log_level="info")

