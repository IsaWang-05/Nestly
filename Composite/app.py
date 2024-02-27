from fastapi import FastAPI, Request, HTTPException
from composites import Composite
from fastapi.responses import JSONResponse, HTMLResponse
import mysql.connector
from typing import Optional
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
import logging
import random
import time
import aiohttp
import asyncio

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
composite = Composite()

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# API Endpoints

@app.get("/")
async def root():
    return FileResponse('static/index.html')

# sync and async aggregators for sprint 2
@app.get("/sync-aggregator")
async def sync_aggregator():
    result = composite.fetch_sync()
    return JSONResponse(content={"result": result})

@app.get("/async-aggregator")
async def async_aggregator():
    result = await composite.fetch_async()
    return JSONResponse(content={"result": result})

@app.get("/clientType")
async def clientType():
    return RedirectResponse(url="https://nestly6156.s3.us-east-2.amazonaws.com/composite/clienttype.html")

@app.get("/host")
async def host():
    return RedirectResponse(url="https://nestly6156.s3.us-east-2.amazonaws.com/bookings_static/host.html")

@app.get("/user")
async def user():
    return RedirectResponse(url="https://nestly6156.s3.us-east-2.amazonaws.com/property_static/user.html")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8012)
