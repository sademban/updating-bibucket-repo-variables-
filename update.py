import os
import requests
from requests.auth import HTTPBasicAuth
from time import sleep
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Bitbucket credentials
username = os.getenv('BITBUCKET_USERNAME')
app_password = os.getenv('BITBUCKET_APP_PASSWORD')

# Repository details
workspace = os.getenv('WORKSPACE_ID')
repo_slug = os.getenv('REPO_SLUG')

# API URLs
base_url = f'https://api.bitbucket.org/2.0/repositories/{workspace}'
variables_url = f'{base_url}/{repo_slug}/pipelines_config/variables/'

session = requests.Session()
session.auth = (username, app_password)

def get_variables():
    """Fetch all variables for the specified repository."""
    variables = []
    page = 1
    while True:
        params = {'page': page, 'pagelen': 100}
        response = session.get(variables_url, params=params)
        if response.status_code == 429:
            print("Hit the API rate limit. Sleeping for 10 sec...")
            sleep(10)
            continue
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()
        variables.extend(data.get('values', []))
        if not data.get('next'):
            break
        page += 1
    return variables

def update_or_create_variable(variable_name, new_value):
    """Update the variable if it exists, or create it if it does not."""
    variables = get_variables()
    variable = next((var for var in variables if var['key'] == variable_name), None)
    
    if variable:
        if variable['value'] != new_value:
            update_url = f'{variables_url}{variable["uuid"]}/'
            update_response = session.put(update_url, json={"value": new_value})
            if update_response.status_code == 200:
                print(f'Successfully updated {variable_name} to {new_value}')
            else:
                print(f'Failed to update {variable_name}. Status code: {update_response.status_code}')
        else:
            print(f'{variable_name} is up to date, no update needed.')
    else:
        # Create a new variable
        create_response = session.post(variables_url, json={"key": variable_name, "value": new_value})
        if create_response.status_code == 201:
            print(f'Successfully created {variable_name} with value {new_value}')
        else:
            print(f'Failed to create {variable_name}. Status code: {create_response.status_code}')

def main():
    for i in range(1, 11):
        variable_name = f'server{i}'  # Variable names are in lowercase
        new_value = os.getenv(f'SERVER{i}')  # Fetch the value from .env using uppercase

        if new_value:
            update_or_create_variable(variable_name, new_value)
        else:
            print(f'No value found for {variable_name} in .env file.')

if __name__ == '__main__':
    main()
