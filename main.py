import io
import requests
import uvicorn
from fastapi import FastAPI
from typing import Dict,List,Any,Union
from AmariSubtitles import AmariSubtitles
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


amarisub = AmariSubtitles()

@app.get('/')# GET # allow all origins all methods.
async def index():
    return "Welcome to Amari Subtitle"

@app.get("/api/fetchsubtitle")
async def fetchsubtitle(imdb_id:str,season:int,episode:int):
    try:
        filename,link = amarisub.search_and_get_url(imdb_id,season,episode)
        return {"filename":filename,"link":link}
    except Exception as ex:
        return {"error":str(ex),"errortype":str(type(ex))}
@app.get("/api/fetchsubtitlemovie")
async def fetchsubtitlemovie(imdb_id:str):
    try:
        filename,link = amarisub.search_and_get_url_movie(imdb_id)
        return {"filename":filename,"link":link}
    except Exception as ex:
        return {"error":str(ex),"errortype":str(type(ex))}

@app.get("/api/searchsubtitles")
async def searchsubtitles(query:str):
    try:
        search_results = amarisub.fetch_subs(query,search=1)
        return {"search_results":search_results}
    except Exception as ex:
        return {"error":str(ex),"errortype":str(type(ex))}

@app.get("/api/getavailablesubtitles")
async def available_subtitles(imdb_id:str):
    try:
        num_available = amarisub.get_available_episodes(imdb_id)
        return {"num_available":num_available}
    except Exception as ex:
        return {"error":str(ex),"errortype":str(type(ex))}
@app.get("/api/queryavailablesubtitles")
async def available_subtitles(query:str):
    try:
        num_available = amarisub.get_available_episodes(query,search=1)
        return {"num_available":num_available}
    except Exception as ex:
        return {"error":str(ex),"errortype":str(type(ex))}




if __name__ == "__main__":
    uvicorn.run("main:app",port=8080,log_level="info")
