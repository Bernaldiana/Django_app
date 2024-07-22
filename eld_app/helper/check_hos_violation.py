from datetime import datetime, timedelta

from django.utils.dateparse import parse_datetime

from eld_app.helper.hours_of_service_rules import HOURS_OF_SERVICE_RULES
from eld_app.models import ELD, Driver, Vehicle


# Function to check if the driving time exceeds the allowed limit
def check_driving_limit(total_driving_time, rules):
    if total_driving_time > timedelta(hours=rules['driving_limit']):
        return f"Exceeded {rules['driving_limit']}-hour driving limit."
    return None


# Function to check if the total on-duty time exceeds the allowed limit
def check_on_duty_limit(total_on_duty_hours, rules):
    if total_on_duty_hours > timedelta(hours=rules['on_duty_limit']):
        return f"Exceeded {rules['on_duty_limit']}-hour on-duty limit."
    return None


# Function to check if the break requirement is met
def check_break_requirement(break_time, rules):
    min_break_required = timedelta(minutes=rules['break_duration'])
    if break_time != min_break_required:
        return f"Failed to take {rules['break_duration']}-minute break."
    return None


# Function to check if the 60/70-hour limit is violated
def check_60_70_hour_limit(total_on_duty_hours, days_to_check):
    hours_limit = 60 if days_to_check == 7 else 70
    if total_on_duty_hours > timedelta(hours=hours_limit):
        return f"HOS violation: Exceeded {hours_limit}-hour limit."
    return None


# Function to check if the sleeper berth provision is violated
def check_sleeper_berth_provision(sleep_time, rules):
    min_off_duty_required = timedelta(hours=rules['sleeper_berth']['min_hours'])
    if sleep_time != min_off_duty_required:
        return f"Failed to meet sleeper berth provision of {rules['sleeper_berth']['min_hours']} hours."
    return None


def create_eld_data(data):
    # Extract data from the request
    driver_id = data.get('driver_id')
    vehicle_id = data.get('vehicle_id')
    status = data.get('status')
    location = data.get('location')
    notes = data.get('notes')
    start_time = parse_datetime(data.get('start_time'))
    end_time = parse_datetime(data.get('end_time'))
    break_time_str = data.get('break_time')
    sleep_time_str = data.get('sleep_time')

    # Convert break_time and sleep_time to timedelta
    break_time = timedelta(hours=int(break_time_str.split(':')[0]), minutes=int(break_time_str.split(':')[1]))
    sleep_time = timedelta(hours=int(sleep_time_str.split(':')[0]), minutes=int(sleep_time_str.split(':')[1]),
                           seconds=int(sleep_time_str.split(':')[2]))

    # Calculate the duration of the new record in seconds
    new_duration = int((end_time - start_time).total_seconds())

    # Get the Driver object
    try:
        driver = Driver.objects.get(driver_id=driver_id)
    except Driver.DoesNotExist:
        return {"error": "Driver not found"}

    # Get the Vehicle object
    try:
        vehicle = Vehicle.objects.get(vehicle_id=vehicle_id)
    except Vehicle.DoesNotExist:
        return {"error": "Vehicle not found"}

    driver_type = driver.driver_type
    days_to_check = 7 if driver_type == 'property' else 8
    now = datetime.now()
    start_period = now - timedelta(days=days_to_check)
    eld_records = ELD.objects.filter(driver=driver, timestamp__gte=start_period).exclude(status='off_duty')

    total_on_duty_hours = timedelta()
    total_driving_time = timedelta()
    rules = HOURS_OF_SERVICE_RULES[driver_type]
    record_violations = []

    # Process each ELD record to compute total on-duty and driving time
    for record in eld_records:
        total_on_duty_hours += timedelta(seconds=record.duration)
        if record.status == 'driving':
            total_driving_time += timedelta(seconds=record.duration)

    # Calculate record's duration for 1 day
    total_on_duty_hours += timedelta(seconds=new_duration)
    total_driving_time += timedelta(seconds=new_duration) if status == 'driving' else timedelta()
    # Check for various types of violations
    violation_message = check_60_70_hour_limit(total_driving_time, days_to_check)
    if violation_message:
        return {"error": violation_message}

    if status == "driving":
        violation_message = check_driving_limit(total_driving_time, rules)
        if violation_message:
            record_violations.append(violation_message)

    violation_message = check_on_duty_limit(total_on_duty_hours, rules)
    if violation_message:
        record_violations.append(violation_message)

    violation_message = check_break_requirement(break_time, rules)
    if violation_message:
        record_violations.append(violation_message)

    violation_message = check_sleeper_berth_provision(sleep_time, rules)
    if violation_message:
        record_violations.append(violation_message)

    # Determine if there are any violations
    record_violation = bool(record_violations)

    # Prepare the ELD data dictionary
    eld_data = {
        "driver_id": driver.driver_id,
        "vehicle_id": vehicle.vehicle_id,
        "timestamp": start_time,
        "status": status,
        "location": location,
        "notes": notes,
        "start_time": start_time,
        "end_time": end_time,
        "duration": new_duration
    }

    # If there are violations, return them along with the ELD data
    if record_violation:
        return {
            "eld_data": eld_data,
            "violation": record_violation,
            "violations_details": record_violations
        }

    # Save the new ELD record to the database
    new_eld_record = ELD(
        driver=driver,
        vehicle=vehicle,
        timestamp=start_time,
        status=status,
        location=location,
        notes=notes,
        start_time=start_time,
        end_time=end_time,
        duration=new_duration
    )
    new_eld_record.save()

    # Return the ELD data along with information about any violations
    return {
        "eld_data": eld_data,
        "violation": record_violation,
        "violations_details": record_violations
    }
