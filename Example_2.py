import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
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

# Example 1: Importing Data from an Excel file, Processing it and Uploading to Genomcore
def import_process_upload():
    """
    This function demonstrates how to import data from an Excel file, process it
    and then upload the processed data to Genomcore.
    Note: This is a conceptual example and not meant to be executed by consultants.
    """

    # Import data from Excel file
    input_excel = "Test-datasets/Sample_data.xlsx"
    df = pd.read_excel(input_excel, sheet_name='Sheet1')

    # Process the data (e.g. filter and add a new column)
    filtered_df = df[df['measurement_value'] > 50]  # Filter
    filtered_df['new_metric'] = filtered_df['value'] * 1.1  # Add new column

    # Convert the DataFrame to a list of dictionaries with the required format
    data_list = []
    for _, row in filtered_df.iterrows():
        data_list.append({
            "code": f"Patient_{row['patient_id']}",
            "data": {
                "User_Information": {
                    "patient_id": row['patient_id'],
                    "patient_name": row['patient_name'],
                    "age": row['age']
                },
                "Metrics": {
                    "measurement_value": row['measurement_value'],
                    "adjusted_value": row['adjusted_value'],
                    "measurement_date": row['measurement_date']
                }
            }
        })

    # Create the final body with the required structure
    body = {"items": data_list}

    # Upload the processed data to the Genomcore platform
    responses = api.records.create_records(template = "processed_data", body = body)

    # Print the responses from the API for review
    print(responses)


# Example 2: Retrieving Time Series Data, Performing Analysis and Visualizing
def retrieve_analyze_visualize():
    """
    This function demonstrates how to retrieve time series data from Genomcore,
    perform statistical analysis and visualize the data.
    Note: This is a conceptual example and not meant to be executed by consultants.
    """

    # Retrieve time series data from Genomcore (conceptual example)
    response = api.time_series.query_time_series(pageSize = 100)

    # Extract the data points from the response
    data_points = response['items']

    # Convert the data points to a DataFrame
    df = pd.DataFrame([{
        'userId': point['meta']['userId'],
        'source': point['meta']['source'],
        'metric': point['meta']['metric'],
        'externalId': point['meta']['externalId'],
        'batch': point['meta']['batch'],
        'start': point['point']['start'],
        'end': point['point']['end'],
        'value': point['point']['val']
    } for point in data_points])

    # Perform basic statistical analysis
    mean_value = df['value'].mean()
    median_value = df['value'].median()
    std_dev = df['value'].std()

    # Print the statistical results
    print(f"Mean Value: {mean_value}")
    print(f"Median Value: {median_value}")
    print(f"Standard Deviation: {std_dev}")

    # Visualize the time series data
    plt.figure(figsize=(10, 6))
    sns.lineplot(data=df, x='start', y='value')
    plt.title('Hemodynamic Time Series Data')
    plt.xlabel('Time')
    plt.ylabel('Value')
    plt.show()


## These functions are defined for conceptual understanding only. They are not meant to be executed.
##--------------------------------------------------------------------------------------------------