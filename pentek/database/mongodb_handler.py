import pymongo
import uuid
from datetime import datetime
from pymongo import MongoClient

# ✅ Global MongoDB Connection (Avoid Reconnecting)
client = MongoClient("mongodb://localhost:27017/")
db = client["pentesting_db"]
metadata_collection = db["scans_metadata"]

class MongoDBHandler:
    """Handles MongoDB operations for pentesting scans."""
    
    def __init__(self, domain):
        """Initialize scan with domain and unique collection name."""
        self.domain = domain.replace(".","_")
        self.uuid = str(uuid.uuid4())[:8]  # Generate short UUID
        self.collection_name = f"Scan_for_{self.domain}_{self.uuid}"
        self.collection = db[self.collection_name]
        
        self.store_metadata()

    def store_metadata(self):
        """Store scan metadata (Called Once Per Scan)."""
        metadata_collection.insert_one({
            "collection_name": self.collection_name,
            "domain": self.domain,
            "uuid": self.uuid,
            "timestamp": datetime.now(),
            "status": "not initiated"  # Initial scan status
        })

    def update_scan_status(self, status):
        """Update the overall scan status in metadata."""
        metadata_collection.update_one(
            {"collection_name": self.collection_name},
            {"$set": {"status": status}}
        )

    def initialize_function(self,name, scan_type):
        """Initialize a function’s status inside the scan collection."""
        self.collection.insert_one({
            "name": name,
            "scan_type": scan_type,
            "status": "",
            "timestamp": datetime.now(),
            "output": []
        })

    def update_function_status(self, name, status):
        """Update the status of a specific function within the scan."""
        self.collection.update_one(
            {"name": name},
            {"$set": {"status": status}}
        )

    def store_scan_result(self, name, output):
        """Store scan results and mark as completed."""
        self.collection.update_one(
            {"name": name},
            {"$set": {
                "status": "completed",
                "output": output
            }}
        )

    @staticmethod
    def delete_scan(collection_name):
        """Delete a scan collection and its metadata."""
        db.drop_collection(collection_name)
        metadata_collection.delete_one({"collection_name": collection_name})

    @staticmethod
    def list_scans():
        """List all stored scans from metadata."""
        return list(metadata_collection.find({}, {"_id": 0}))
