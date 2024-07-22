# point 4
from datetime import timedelta


def plan_driving_schedule(pickup_time, dropoff_time, current_status):
    """
    Plans the driving schedule based on pickup and dropoff times, considering HOS regulations.

    :param pickup_time: datetime object indicating the pickup time
    :param dropoff_time: datetime object indicating the dropoff time
    :param current_status: list of dictionaries containing current duty status logs
    :return: list of dictionaries representing the planned schedule
    """
    # Constants
    MAX_DRIVING_HOURS = 11
    MAX_ON_DUTY_HOURS = 14
    SLEEPER_BERTH_MIN_HOURS = 7
    MIN_BREAK_HOURS = 0.5
    TOTAL_OFF_DUTY_HOURS = 10

    # Placeholder for the planned schedule
    schedule = []

    # Calculate remaining driving and on-duty hours for the day
    total_driving_time = sum([entry['duration'] for entry in current_status if entry['status'] == 'driving'])
    total_on_duty_time = sum([entry['duration'] for entry in current_status if entry['status'] != 'off_duty'])

    remaining_driving_hours = MAX_DRIVING_HOURS - (total_driving_time / 3600)
    remaining_on_duty_hours = MAX_ON_DUTY_HOURS - (total_on_duty_time / 3600)

    # Plan the schedule
    current_time = pickup_time

    while current_time < dropoff_time and remaining_driving_hours > 0 and remaining_on_duty_hours > 0:
        driving_period = min(remaining_driving_hours, 8)  # Max 8 hours driving before break
        driving_duration = timedelta(hours=driving_period)
        next_time = current_time + driving_duration

        # Append driving period to the schedule
        schedule.append({
            "status": "driving",
            "start_time": current_time,
            "end_time": next_time,
            "duration": int(driving_duration.total_seconds())
        })

        # Update current time and remaining hours
        current_time = next_time
        remaining_driving_hours -= driving_period
        remaining_on_duty_hours -= driving_period

        # Check if a break is needed
        if remaining_driving_hours > 0 and remaining_on_duty_hours > 0:
            break_duration = timedelta(hours=MIN_BREAK_HOURS)
            next_time = current_time + break_duration

            # Append break period to the schedule
            schedule.append({
                "status": "off_duty",
                "start_time": current_time,
                "end_time": next_time,
                "duration": int(break_duration.total_seconds())
            })

            # Update current time
            current_time = next_time

    # Ensure at least 7 hours in sleeper berth if close to 14-hour limit
    if remaining_on_duty_hours < SLEEPER_BERTH_MIN_HOURS:
        sleeper_berth_duration = timedelta(hours=SLEEPER_BERTH_MIN_HOURS)
        next_time = current_time + sleeper_berth_duration

        # Append sleeper berth period to the schedule
        schedule.append({
            "status": "sleeper_berth",
            "start_time": current_time,
            "end_time": next_time,
            "duration": int(sleeper_berth_duration.total_seconds())
        })

        # Update current time
        current_time = next_time

    # Return the planned schedule
    return schedule

# Example usage:
# pickup_time = datetime(2024, 6, 28, 8, 0, 0)
# dropoff_time = datetime(2024, 6, 28, 20, 0, 0)
# current_status = [
#     {"status": "off_duty", "duration": 3600},
#     {"status": "driving", "duration": 14400},
#     {"status": "off_duty", "duration": 1800}
# ]
#
# planned_schedule = plan_driving_schedule(pickup_time, dropoff_time, current_status)
# for entry in planned_schedule:
#     print(entry)
