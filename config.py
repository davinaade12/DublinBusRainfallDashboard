import os
from dotenv import load_dotenv

load_dotenv()

class Config:

    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")

    NTA_API_KEY = os.getenv("e87f6e6b164a4b99a42c229ef0b6c7b8")

    NTA_GTFS_URL = os.getenv("https://api.nationaltransport.ie/gtfsr/v2/gtfsr?format=protobuf")
    MET_FORECAST_URL = os.getenv("http://openaccess.pf.api.met.ie/metno-wdb2ts/locationforecast?lat=53.3498;long=-6.2603")