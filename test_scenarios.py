import json

import requests

BASE_URL = "http://localhost:8000/api/show_violation/"

# Sample payloads for different scenarios
payloads = [
    # Normal Scenario
    {
        "driver_id": "12345",
        "vehicle_id": "67890",
        "status": "driving",
        "location": "New York, NY",
        "notes": "Routine drive",
        "start_time": "2024-07-01T08:00:00Z",
        "end_time": "2024-07-01T10:00:00Z",
        "break_time": "00:30",
        "sleep_time": "08:00:00"
    },
    # Exceeding Driving Limit
    {
        "driver_id": "12382",
        "vehicle_id": "67897",
        "status": "driving",
        "location": "New York, NY",
        "notes": "Extended drive",
        "start_time": "2024-07-01T08:00:00Z",
        "end_time": "2024-07-01T18:00:00Z",
        "break_time": "00:30",
        "sleep_time": "08:00:00"
    },
    # Exceeding On-Duty Limit
    {
        "driver_id": "12389",
        "vehicle_id": "67892",
        "status": "on_duty_not_driving",
        "location": "New York, NY",
        "notes": "Overtime work",
        "start_time": "2023-01-02T08:00:00Z",
        "end_time": "2023-01-02T23:00:00Z",
        "break_time": "00:30",
        "sleep_time": "10:00:00"
    },
    # Failure to Meet Break Requirement
    {
        "driver_id": "12384",
        "vehicle_id": "67097",
        "status": "driving",
        "location": "Philadelphia, PA",
        "notes": "Skipped break",
        "start_time": "2024-07-01T08:00:00Z",
        "end_time": "2024-07-01T12:00:00Z",
        "break_time": "00:05",
        "sleep_time": "10:00:00"
    },
    # Failed Sleeper Berth Provision
    {
        "driver_id": "12384",
        "vehicle_id": "67097",
        "status": "driving",
        "location": "Philadelphia, PA",
        "notes": "Skipped break",
        "start_time": "2024-07-01T08:00:00Z",
        "end_time": "2024-07-01T12:00:00Z",
        "break_time": "00:30",
        "sleep_time": "00:30:00"
    },
    # Exceeding 60/70-Hour Limit
    {
        "driver_id": "12084",
        "vehicle_id": "67537",
        "status": "driving",
        "location": "Philadelphia, PA",
        "notes": "High total hours",
        "start_time": "2024-01-01T01:00:00Z",
        "end_time": "2024-07-01T07:00:00Z",
        "break_time": "00:30",
        "sleep_time": "08:00:00"
    },
    # Multiple Violations
    {
        "driver_id": "12834",
        "vehicle_id": "60567",
        "status": "driving",
        "location": "Washington, DC",
        "notes": "Multiple violations",
        "start_time": "2024-07-01T06:00:00Z",
        "end_time": "2024-07-01T20:00:00Z",
        "break_time": "00:00",
        "sleep_time": "00:30:00"
    }
]


# Function to send POST request and print response
def send_request(payload):
    response = requests.post(BASE_URL, json=payload)
    if response.status_code == 200:
        print("Response:", json.dumps(response.json(), indent=4))
    else:
        print("Failed to get response:", response.status_code, response.text)


# Send requests for each payload
for i, payload in enumerate(payloads):
    print(f"Sending request {i + 1}")
    send_request(payload)
    print("\n")
