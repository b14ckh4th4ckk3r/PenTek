from flask import Blueprint, jsonify, request
from web.backend.models import MongoDBHandler
from web.backend.socketio_instance import socketio
from database.mongodb_handler import db
import logging
import multiprocessing

from phases.recon import Recon
from phases.scanning import Scanning

api_routes = Blueprint('api_routes', __name__)

def run_scan_process(domain, scan_type):
    try:
        db_handler = MongoDBHandler(domain)
        db_handler.store_metadata()
        db_handler.update_scan_status("running")

        if scan_type == 'recon':
            Recon.recon_run(domain, db_handler, 'web')
        elif scan_type == 'scanning':
            Scanning.run_scanning(domain,db_handler, 'web')
        else:
            Recon.recon_run(domain, db_handler, 'web')
            Scanning.run_scanning(domain,db_handler, 'web')

        db_handler.update_scan_status("completed")
        socketio.emit('scan_completed', {'message': f'Scan for {domain} completed.'})
    except Exception as e:
        logging.error(f"Error running scan: {e}", exc_info=True)
        if db_handler:
            db_handler.update_scan_status("error")

@api_routes.route('/scan/start', methods=['POST'])
def start_scan():
    data = request.json
    domain = data.get('domain')
    scan_type = data.get('scan_type', 'full')

    try:
        process = multiprocessing.Process(target=run_scan_process, args=(domain, scan_type))
        process.start()

        return jsonify({"status": "Scan started", "domain": domain, "scan_type": scan_type})
    except Exception as e:
        logging.error(f"Error starting scan: {e}", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500

@api_routes.route('/scan/status', methods=['GET'])
def get_scan_status():
    # This endpoint can be improved to track multiple scans if needed
    return jsonify({"status": "Not implemented"})

@api_routes.route('/scan/results', methods=['GET'])
def get_scan_results():
    # This endpoint can be improved to fetch results for specific scans
    return jsonify({"results": []})

@api_routes.route('/scan/list', methods=['GET'])
def list_scans():
    try:
        scans = MongoDBHandler.list_scans()
        scan_entries = []
        for scan in scans:
            collection_name = scan.get('collection_name')
            domain = scan.get('domain')
            # Use the db object to get the collection by name
            collection = db[collection_name]
            for doc in collection.find({}, {"_id": 0}):
                entry = {
                    "collection_name": collection_name,
                    "domain": domain,
                    "scan_type": doc.get("scan_type"),
                    "module": doc.get("module"),
                    "name": doc.get("name"),
                    "status": doc.get("status"),
                    "timestamp": doc.get("timestamp"),
                    "output": doc.get("output"),
                }
                scan_entries.append(entry)
        return jsonify(scan_entries)
    except Exception as e:
        logging.error(f"Error listing scans: {e}", exc_info=True)
        return jsonify([]), 500

@api_routes.route('/scan/details/<collection_name>', methods=['GET'])
def scan_details(collection_name):
    try:
        collection = db[collection_name]
        docs = list(collection.find({}, {"_id": 0}))
        # Group docs by scan_type and module
        grouped = {}
        for doc in docs:
            scan_type = doc.get('scan_type', 'Unknown')
            module = doc.get('module', 'Unknown')
            if scan_type not in grouped:
                grouped[scan_type] = {}
            if module not in grouped[scan_type]:
                grouped[scan_type][module] = []
            grouped[scan_type][module].append(doc)
        return jsonify(grouped)
    except Exception as e:
        logging.error(f"Error fetching scan details for {collection_name}: {e}", exc_info=True)
        return jsonify({}), 500
