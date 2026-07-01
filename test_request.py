import requests
import json

url = "http://127.0.0.1:5000/predict"  # Updated URL to the /predict endpoint

data = {
    "text": "You freaking suck!"  # Replace with any text you want to test
}

response = requests.post(url, json=data)

if response.status_code == 200:
    try:
        print(response.json())  # Print the JSON response from the server
    except json.decoder.JSONDecodeError:
        print("Error parsing JSON: Response body is not in valid JSON format")
else:
    print(f"Error: {response.status_code}, {response.text}")
