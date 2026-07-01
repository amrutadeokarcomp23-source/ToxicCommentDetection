import requests
import json

# Define the URL of the Flask server (ensure you include the correct endpoint)
url = "http://127.0.0.1:5000/predict"  # Updated URL to the /predict endpoint

# Create the data payload with the comment text you want to classify
data = {
    "text": "You freaking suck!"  # Replace with any text you want to test
}

# Send the POST request
response = requests.post(url, json=data)

# Check the status code first
if response.status_code == 200:
    try:
        print(response.json())  # Print the JSON response from the server
    except json.decoder.JSONDecodeError:
        print("Error parsing JSON: Response body is not in valid JSON format")
else:
    print(f"Error: {response.status_code}, {response.text}")
