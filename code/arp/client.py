import logging
import os
import time

import requests

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- Configuration ---
SERVER   = os.environ.get("SERVER_NAME")
PORT     = os.environ.get("SERVER_PORT")
USERNAME = os.environ.get("USERNAME")
PASSWORD = os.environ.get("PASSWORD")


def authenticate():
    # Step 1: POST credentials → receive JWT access token
    response = requests.post(
        f"http://{SERVER}:{PORT}/token",
        data={"username": USERNAME, "password": PASSWORD},
    )
    token = response.json()["access_token"]
    logger.info(f"Token: {token}")

    # Step 2: GET protected resource → send JWT as Bearer token
    protected = requests.get(
        f"http://{SERVER}:{PORT}/protected",
        headers={"Authorization": f"Bearer {token}"},
    )
    logger.info(f"Protected: {protected.json()}")


if __name__ == "__main__":
    # Authenticate every 30 seconds
    while True:
        authenticate()
        time.sleep(30)
