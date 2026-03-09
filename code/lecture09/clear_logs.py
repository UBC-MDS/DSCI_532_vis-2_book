"""Pre-class cleanup: delete all documents from form_log and query_log collections.

Run once before each lecture session:
    python clear_logs.py

Requires MONGODB_URI in environment or .env file.
"""

from dotenv import load_dotenv
from pymongo import MongoClient
import os

load_dotenv()

client = MongoClient(os.environ["MONGODB_URI"])
db = client["dsci532"]

for collection_name in ["form_log", "query_log"]:
    result = db[collection_name].delete_many({})
    print(f"  {collection_name}: deleted {result.deleted_count} documents")

print("Done — logs cleared.")
