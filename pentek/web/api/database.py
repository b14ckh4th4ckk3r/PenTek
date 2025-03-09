from fastapi import FastAPI


# import sys
# import os
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from database.mongodb_handler import MongoDBHandler

app = FastAPI()

@app.get("/scans")
def get_scans():
    """Get all scans from metadata collection."""
    return MongoDBHandler.list_scans()

@app.delete("/delete_scan/{collection_name}")
def delete_scan(collection_name: str):
    """Delete a scan collection by name."""
    MongoDBHandler.delete_scan(collection_name)
    return {"message": f"Scan {collection_name} deleted successfully"}
