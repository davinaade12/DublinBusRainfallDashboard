from dotenv import load_dotenv
import os

load_dotenv()

print("KEY:", os.getenv("NTA_API_KEY"))
print("URL:", os.getenv("NTA_GTFS_URL"))