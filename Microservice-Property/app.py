from fastapi import FastAPI, Request, HTTPException
import mysql.connector
from properties import PropertiesService
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from fastapi import HTTPException
from address_veri_api import is_address_valid

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# setting up db connection
def db_connection(host, user, pwd, db, port):
    try:
        conn = mysql.connector.connect(
            host=host,
            user=user,
            passwd=pwd,
            database=db,
            port=port)
        print("Database connected successfully!")
    except mysql.connector.Error as err:
        print(f"Error: '{err}'")
        raise HTTPException(status_code=500, detail="Database connection failed")
    return conn

# initializing db connection and PropertiesService
conn = db_connection("database-1.cjcvwqrysug2.us-east-2.rds.amazonaws.com", "admin", "dbuserdbuser", "property", 3306)
properties_service = PropertiesService(conn)

# api endpoints
@app.get("/")  ## use this as the static page of this app
async def root():
    return RedirectResponse(url="https://nestly6156.s3.us-east-2.amazonaws.com/property_static/index.html")

@app.get("/search")
async def search():
    return RedirectResponse(url="https://nestly6156.s3.us-east-2.amazonaws.com/property_static/search.html")

@app.get("/host_property_management/{host_id}")
async def host_property_management(host_id: str):
    return RedirectResponse(url=f"https://nestly6156.s3.us-east-2.amazonaws.com/property_static/host_property_management.html?host_id={host_id}")

@app.get("/properties")
async def get_properties(property_id: Optional[str] = None, first_name: Optional[str] = None,
                         last_name: Optional[str] = None, property_address: Optional[str] = None,
                         house_type: Optional[str] = None, house_size: Optional[int] = None,
                         size_gt: Optional[int] = None,
                         size_lt: Optional[int] = None,
                         price: Optional[int] = None,
                         price_gt: Optional[int] = None,
                         price_lt: Optional[int] = None, availability: Optional[bool] = None, 
                         host_id: Optional[str] = None, limit: Optional[int] = None, 
                         offset: Optional[int] = None):
    filters = {
        "property_id": property_id,
        "first_name": first_name,
        "last_name": last_name,
        "property_address": property_address,
        "house_type": house_type,
        "house_size":house_size,
        "size_gt": size_gt,
        "size_lt": size_lt,
        "price":price,
        "price_gt": price_gt,
        "price_lt": price_lt,
        "availability": availability,
        "host_id": host_id
    }
    filters = {k: v for k, v in filters.items() if v}     ##simple search
    return properties_service.get_properties(filters, limit, offset)

@app.post("/properties")         ## create properties function
async def create_property(request: Request):
    property_data = await request.json()
    if not is_address_valid(property_data.get("property_address")):
        raise HTTPException(status_code=400, detail="Invalid address")
    return properties_service.create_property(property_data)

@app.put("/properties/{property_id}")        ## update properties function
async def update_property(property_id: str, request: Request):
    property_data = await request.json()
    if 'property_address' in property_data and property_data['property_address']:
        if not is_address_valid(property_data['property_address']):
            raise HTTPException(status_code=400, detail="Invalid address")
    return properties_service.update_property(property_id, property_data)

@app.delete("/properties/{property_id}")        ## delete properties function
async def delete_property(property_id: str):
    return properties_service.delete_property(property_id)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8013)
