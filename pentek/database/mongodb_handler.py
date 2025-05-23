import uuid
from datetime import datetime
from pymongo import MongoClient


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

    def initialize_function(self, name, scan_type, module, scan_subtype=None):
        """Initialize a function’s status inside the scan collection."""
        doc = {
            "name": name,
            "scan_type": scan_type,
            "module": module,
            "status": "running",
            "timestamp": datetime.now(),
            "output": ""
        }
        if scan_subtype:
            doc["scan_subtype"] = scan_subtype
        self.collection.insert_one(doc)

    # def store_scan_result(self, name, full_output, scan_subtype=None):
    #     """Store scan results as full_output only and mark as completed."""
    #     query = {"name": name}
    #     if scan_subtype:
    #         query["scan_subtype"] = scan_subtype
    #     output = full_output
    #     self.collection.update_one(
    #     query,
    #     {"$set": {
    #         "status": "completed",
    #         "output": {"$concat": ["$output", "\n", full_output]} if "output" in query else full_output
    #     }}
    # )

    def store_scan_result(self, name, full_output, scan_subtype=None):
        """Store or append scan results as full_output and mark as completed."""
        query = {"name": name}
        if scan_subtype:
            query["scan_subtype"] = scan_subtype
        
        # Fetch the current document to append the output
        current_doc = self.collection.find_one(query)
        
        if current_doc and "output" in current_doc:
            # Append the new output to the existing output
            new_output = current_doc["output"] + "\n" + full_output
        else:
            # If no previous output, just store the new output
            new_output = full_output
        
        # Update the document with the new appended output
        self.collection.update_one(
            query,
            {"$set": {
                "status": "completed",
                "output": new_output
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
