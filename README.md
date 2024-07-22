# Federal Motor Carrier Safety Administration

## Description

This project involves the following tasks:

1. **Setup Django version 3.2.23**
2. **Build an API to pull sample truck ELD data**
   - Request API test environment access through DMs
3. **Build a function to detect FMCSA HOS violations**
   - Refer to [FMCSA HOS regulations](https://www.fmcsa.dot.gov/regulations/hours-service/summary-hours-service-regulations)
4. **Build a function to plan out a driver's driving schedule based on pickup and dropoff times and conditions**
   - Make this function as optimal as possible to leave the maximum future flexibility on HOS
   - "Sleeper Berth Provision" needs to be built into this function
   - "Adverse Driving Conditions" and "Short-Haul Exception" do not need to be built into this function
5. **Build a function that:**
   - Takes Pickup and Dropoff conditions along with Duty Status and times as inputs
     - Refer to [FMCSA ELD usage](https://www.fmcsa.dot.gov/hours-service/elds/using-elds)
   - Returns:
     - Whether inputs constitute an HOS violation
     - If so, how the HOS could have been entered instead while maintaining pickup and dropoff requirements to not result in an HOS violation

## Setup and Installation


### 1. Create and Activate a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate
```

### 2. Install Requirements

```bash
pip install -r  requirements.txt
```

### 3. Run Script to Populate Database

```bash
python manage.py shell
from scripts.dump_data_in_model import main
main()
```

### 4. Run Project
Run this command and then you will access project at this url "http://127.0.0.1:8000/".

```bash
python manage.py runserver
```

### 5. Test the use case
python test_scenarios.py