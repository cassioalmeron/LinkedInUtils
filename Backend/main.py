#!/usr/bin/env python3
"""
Crowler Service Script with Hourly Logging
This script runs the crowler service with automatic hourly logging
"""

import os
import sys
import time
import threading
import uvicorn
from datetime import datetime
from service_manager import manage_service
from api import app
from logger import logger

service_name = os.getenv('SERVICE_NAME')

def install_service():
    """Install the crowler service using service_manager"""
    app_path = os.path.abspath(__file__)
    manage_service(service_name, "install", app_path)
    
def start_service():
    """Start the crowler service using service_manager"""
    manage_service(service_name, "start")
    
def stop_service():
    """Stop the crowler service using service_manager"""
    manage_service(service_name, "stop")
    
def uninstall_service():
    """Uninstall the crowler service using service_manager"""
    manage_service(service_name, "uninstall")
    
def main():
    """Main function to run the FastAPI backend service"""
    logger.info("LinkedIn Utils Backend service started")
    
    api_port = int(os.getenv("API_PORT"))
    uvicorn.run(app, host="0.0.0.0", port=api_port)

if __name__ == "__main__":
    if len(sys.argv) == 1:
        main()
    else:
        action = sys.argv[1]
        if action == "install":
            install_service()
        elif action == "start":
            start_service()
        elif action == "stop":
            stop_service()
        elif action == "uninstall":
            uninstall_service()
        else:
            print("Invalid action. Available actions: install, start, stop, uninstall")
            print("Usage:")
            print("  python3 main.py          # Run as service")
            print("  python3 main.py install  # Install service")
            print("  python3 main.py start    # Start service")
            print("  python3 main.py stop     # Stop service")
            print("  python3 main.py uninstall # Uninstall service")
            sys.exit(1)
