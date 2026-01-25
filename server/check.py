from pymongo import MongoClient
import certifi, os
from dotenv import load_dotenv

load_dotenv()

client = MongoClient(
    os.getenv("MONGO_URI"),
    tls=True,
    tlsCAFile=certifi.where()
)

print(client.admin.command("ping"))
