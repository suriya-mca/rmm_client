import requests
from datetime import datetime
from decouple import config

# Base URL for the API
API_BASE_URL = "http://localhost:8000/api/v1/"

# API key retrieved from environment variables or fallback to default
API_KEY = config('API_KEY', default='your-api-key-here')  # Replace with your actual API key

# Headers to include the API key for authentication
HEADERS = {
    "X-API-Key": API_KEY
}

def fetch_machine_status(machine_id):
    """
    Fetch the current status of a machine from the server.
    :param machine_id: The unique ID of the machine.
    :return: JSON response containing machine status.
    """
    response = requests.get(f"{API_BASE_URL}machines/{machine_id}/", headers=HEADERS)
    response.raise_for_status()  # Raise an error if the request fails
    return response.json()

def update_machine_status(machine_id, status):
    """
    Update the status of a machine on the server.
    :param machine_id: The unique ID of the machine.
    :param status: The new status to set for the machine.
    :return: JSON response after updating the status.
    """
    response = requests.post(
        f"{API_BASE_URL}machines/{machine_id}/status/",
        headers=HEADERS,
        json={"status": status}  # Send the new status in the request body
    )
    response.raise_for_status()  # Raise an error if the request fails
    return response.json()

def fetch_machine_logs(machine_id):
    """
    Fetch logs for a specific machine from the server.
    :param machine_id: The unique ID of the machine.
    :return: JSON response containing the logs.
    """
    response = requests.get(f"{API_BASE_URL}machines/{machine_id}/logs/", headers=HEADERS)
    response.raise_for_status()  # Raise an error if the request fails
    return response.json()

def send_local_logs(machine_id, logs):
    """
    Send local logs to the server for a specific machine.
    :param machine_id: The unique ID of the machine.
    :param logs: List of logs to send to the server.
    """
    for log in logs:
        response = requests.post(
            f"{API_BASE_URL}machines/{machine_id}/logs/",
            headers=HEADERS,
            json=log  # Send each log as JSON in the request body
        )
        response.raise_for_status()  # Raise an error if the request fails
