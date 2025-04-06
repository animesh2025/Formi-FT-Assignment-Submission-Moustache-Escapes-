from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import List, Union
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import uvicorn

app = FastAPI(title="Moustache Escapes Nearest Property API")
geolocator = Nominatim(user_agent="moustache_locator")

# Sample property data
properties = [
    {"id": "PROP001", "name": "Moustache Jaipur", "latitude": 26.9124, "longitude": 75.7873, "address": "Jaipur, Rajasthan"},
    {"id": "PROP002", "name": "Moustache Agra", "latitude": 27.1767, "longitude": 78.0081, "address": "Agra, Uttar Pradesh"},
    {"id": "PROP003", "name": "Moustache Rishikesh", "latitude": 30.0869, "longitude": 78.2676, "address": "Rishikesh, Uttarakhand"},
    {"id": "PROP004", "name": "Moustache Manali", "latitude": 32.2396, "longitude": 77.1887, "address": "Manali, Himachal Pradesh"},
    # Add more properties as needed
]

class LocationQuery(BaseModel):
    query: str

class PropertyResponse(BaseModel):
    name: str
    address: str
    distance_km: float

@app.post("/nearest-properties", response_model=Union[List[PropertyResponse], dict])
def get_nearest_properties(location: LocationQuery):
    try:
        location_obj = geolocator.geocode(location.query)
        if not location_obj:
            raise HTTPException(status_code=404, detail="Location not found")

        user_coords = (location_obj.latitude, location_obj.longitude)
        results = []

        for prop in properties:
            prop_coords = (prop["latitude"], prop["longitude"])
            distance = geodesic(user_coords, prop_coords).kilometers
            if distance <= 50:
                results.append({
                    "name": prop["name"],
                    "address": prop["address"],
                    "distance_km": round(distance, 2)
                })

        if not results:
            return {"message": "No properties available within 50 km."}

        return sorted(results, key=lambda x: x["distance_km"])

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# To run the app: uvicorn filename:app --reload
if __name__ == "__main__":
    uvicorn.run("nearest_properties_api:app", host="0.0.0.0", port=8000, reload=True)