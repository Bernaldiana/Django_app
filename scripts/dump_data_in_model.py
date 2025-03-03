from datetime import timedelta

from eld_app.models import Driver, Vehicle, ELD
from django.utils.dateparse import parse_datetime

eld_data = [
    {
        "driver_id": {
            "driver_id": "12345",
            "name": "xyz",
            "status": "off_duty",
            "driver_type": "passenger"
        },
        "vehicle_id": {
            "vehicle_id": "67890",
            "status": "off_duty",
            "location": "New York, NY"
        },
        "status": "off_duty",
        "timestamp": "2024-06-26T08:00:00Z",
        "location": "New York, NY",
        "duration": 3600,
        "start_time": "2023-01-01T08:00:00Z",
        "end_time": "2023-01-01T16:00:00Z",
        "notes": "abc"
    },
    {
        "driver_id": {
            "driver_id": "12389",
            "name": "upc",
            "status": "on_duty_not_driving",
            "driver_type": "property"
        },
        "vehicle_id": {
            "vehicle_id": "67892",
            "status": "on_duty_not_driving",
            "location": "New York, NY"
        },
        "status": "on_duty_not_driving",
        "timestamp": "2024-06-28T09:00:00Z",
        "location": "New York, NY",
        "duration": 1800,
        "start_time": "2024-06-28T08:00:00Z",
        "end_time": "2024-06-28T16:00:00Z",
        "notes": "abc"
    },
    {
        "driver_id": {
            "driver_id": "12382",
            "name": "ijk",
            "status": "driving",
            "driver_type": "passenger"
        },
        "vehicle_id": {
            "vehicle_id": "67897",
            "status": "driving",
            "location": "New York, NY"
        },
        "status": "driving",
        "timestamp": "2024-07-21T09:30:00Z",
        "location": "New York, NY",
        "duration": 14400,
        "start_time": "2024-07-21T08:00:00Z",
        "end_time": "2024-07-22T16:00:00Z",
        "notes": "abc"
    },
    {
        "driver_id": {
            "driver_id": "12384",
            "name": "pqr",
            "status": "on_duty_not_driving",
            "driver_type": "property"
        },
        "vehicle_id": {
            "vehicle_id": "67097",
            "status": "on_duty_not_driving",
            "location": "Philadelphia, PA"
        },
        "status": "on_duty_not_driving",
        "timestamp": "2024-06-23T13:30:00Z",
        "location": "Philadelphia, PA",
        "duration": 1800,
        "start_time": "2024-06-23T08:00:00Z",
        "end_time": "2024-06-23T16:00:00Z",
        "notes": "abc"
    },
    {
        "driver_id": {
            "driver_id": "12084",
            "name": "omg",
            "status": "driving",
            "driver_type": "passenger"
        },
        "vehicle_id": {
            "vehicle_id": "67537",
            "status": "driving",
            "location": "Philadelphia, PA"
        },
        "status": "driving",
        "timestamp": "2024-06-26T14:00:00Z",
        "location": "Philadelphia, PA",
        "duration": 10800,
        "start_time": "2024-06-25T08:00:00Z",
        "end_time": "2024-06-26T16:00:00Z",
        "notes": "abc"
    },
    {
        "driver_id": {
            "driver_id": "12884",
            "name": "a-one",
            "status": "off_duty",
            "driver_type": "property"
        },
        "vehicle_id": {
            "vehicle_id": "60537",
            "status": "off_duty",
            "location": "Washington, DC"
        },
        "status": "off_duty",
        "timestamp": "2024-06-26T17:00:00Z",
        "location": "Washington, DC",
        "duration": 43200,
        "start_time": "2024-06-26T08:00:00Z",
        "end_time": "2024-06-26T16:00:00Z",
        "notes": "abc"
    },
    {
        "driver_id": {
            "driver_id": "12834",
            "name": "b-one",
            "status": "driving",
            "driver_type": "property"
        },
        "vehicle_id": {
            "vehicle_id": "60567",
            "status": "driving",
            "location": "Washington, DC"
        },
        "status": "driving",
        "timestamp": "2024-06-27T05:00:00Z",
        "location": "Washington, DC",
        "duration": 18000,
        "start_time": "2024-06-27T08:00:00Z",
        "end_time": "2024-06-01T22:00:00Z",
        "notes": "abc"
    }
]


def main():
    for data in eld_data:
        driver = data.pop("driver_id")
        vehicle = data.pop("vehicle_id")

        data["driver"] = Driver.objects.create(**driver)
        data["vehicle"] = Vehicle.objects.create(**vehicle)
        data["timestamp"] = parse_datetime(data["timestamp"])
        data["start_time"] = parse_datetime(data["start_time"])
        data["end_time"] = parse_datetime(data["end_time"])
        ELD.objects.create(**data)
