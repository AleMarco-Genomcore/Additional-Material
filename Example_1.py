# Example 1: Uploading Hemodynamic Time Series Data

import logging
import os
import csv
import dotenv
from genomcore.client import Genomcore

# Set up logging to provide informative output during script execution
logging.basicConfig(
    level="INFO",
    format="[%(asctime)s][%(levelname)s][%(name)s] -- %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# Load environment variables from .env file
dotenv.load_dotenv()

# Specify the path to the input CSV file
input_csv = "Test-datasets/50000.csv"

# Read the CSV file and prepare the data for uploading
with open(input_csv) as csv_file:
    csv_reader = csv.DictReader(csv_file)
    data_list = []
    for row in csv_reader:

        data_list.append({
            'meta': {
                'userId': int(row['meta.userId']),
                'source': row['meta.source'],
                'metric': row['meta.metric'],
                'externalId': row['meta.externalId'],
                'batch': row['meta.batch'],
            },
            'point': {
                'start': row['point.start'],
                'end': row['point.end'],
                'value': int(row['point.value']),
            }
        })

# Initialize the Genomcore-sdk-python client with authentication tokens and environment settings
api = Genomcore(
    token=os.getenv("TOKEN"),
    refresh_token=os.getenv("REFRESH_TOKEN"),
    env=os.getenv("ENV"),
)

# Upload the hemodynamic time series data to the Genomcore platform
responses = api.time_series.create_time_series(
    body = data_list,
    chunksize = 1000, # Upload data in chunks of 1000 datapoints at a time
    max_retries = 3,  # Retry up to 3 times in case of failures
    timer = True      # Enable timing of the operation for performance analysis
)

# Print the responses from the API for review
print(responses)

#------------------------------------------------
# Example 2: Creating Patient Records

import logging
import os
import json
import dotenv
from genomcore.client import Genomcore

# Set up logging to provide informative output during script execution
logging.basicConfig(
    level="INFO",
    format="[%(asctime)s][%(levelname)s][%(name)s] -- %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# Load environment variables from .env file
dotenv.load_dotenv()

# Load the JSON file for creating patient records
with open("Test-datasets/Patient_records.json") as f:
    patients = json.load(f)

# Create the patient records using the data from the JSON file
response_patients = api.records.create_records(template = "Patients_test", body = patients)

# Print the response from the API for review
print(response_patients)

#------------------------------------------------
# Example 3: Deleting Patient Records
import logging
import os
import dotenv
from genomcore.client import Genomcore

# Set up logging to provide informative output during script execution
logging.basicConfig(
    level="INFO",
    format="[%(asctime)s][%(levelname)s][%(name)s] -- %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# Load environment variables from .env file
dotenv.load_dotenv()

# Initialize the Genomcore SDK client with authentication tokens and environment settings
api = Genomcore(
    token=os.getenv("TOKEN"),
    refresh_token=os.getenv("REFRESH_TOKEN"),
    env=os.getenv("ENV"),
)

# Define the body for deleting patient records
body_delete = {
    "records": [
        {"id": "PatientRecord_id1"},
        {"id": "PatientRecord_id2"},
        {"id": "PatientRecord_id3"}
    ]
}

# Delete the patient records
response_delete = api.records.delete_records(body = body_delete)

# Print the response from the API for review
print(response_delete)

#------------------------------------------------
# Example 4: Creating Terminologies

import logging
import os
import json
import dotenv
from genomcore.client import Genomcore

# Set up logging to provide informative output during script execution
logging.basicConfig(
    level="INFO",
    format="[%(asctime)s][%(levelname)s][%(name)s] -- %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# Load environment variables from .env file
dotenv.load_dotenv()

# Initialize the Genomcore SDK client with authentication tokens and environment settings
api = Genomcore(
    token=os.getenv("TOKEN"),
    refresh_token=os.getenv("REFRESH_TOKEN"),
    env=os.getenv("ENV"),
)

# Load the JSON file for creating terminologies
with open("Test-datasets/Terminology_records.json") as f:
    terminologies = json.load(f)

# Create the terminology
response_terminologies = api.records.create_records(template = "Terms_test", body = terminologies)

# Print the response from the API for review
print(response_terminologies)