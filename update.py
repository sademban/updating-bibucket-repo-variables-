import os
import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Bitbucket credentials
username = os.getenv('BITBUCKET_USERNAME')
app_password = os.getenv('BITBUCKET_APP_PASSWORD')

# Repository details
workspace = os.getenv('WORKSPACE_ID')
repo_slug = os.getenv('REPO_SLUG')

# Variable details
variable_name = os.getenv('VARIABLE_NAME')
new_value = os.getenv('NEW_VALUE')

# API URL for repository variables
url = f'https://api.bitbucket.org/2.0/repositories/{workspace}/{repo_slug}/pipelines_config/variables/'

# Fetch all repository variables
response = requests.get(url, auth=HTTPBasicAuth(username, app_password))

# Check if the request was successful
if response.status_code == 200:
    variables = response.json()['values']

    # Find the variable you want to update
    variable = next((var for var in variables if var['key'] == variable_name), None)

    if variable:
        # Update the variable
        update_url = f'{url}{variable["uuid"]}/'
        update_response = requests.put(update_url, json={"value": new_value}, auth=HTTPBasicAuth(username, app_password))

        if update_response.status_code == 200:
            print(f'Successfully updated {variable_name} to {new_value}')
        else:
            print(f'Failed to update variable. Status code: {update_response.status_code}')
    else:
        print(f'Variable {variable_name} not found')
else:
    print(f'Failed to fetch variables. Status code: {response.status_code}')
