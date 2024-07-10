import requests
import json

# Configuration
home_assistant_url = "http://<home-assistent>:8123/api/states"
home_assistant_token = "<your HA token>"

# URL and headers for the initial API request
url = "https://portaal.eplucon.nl/api/v2/econtrol/modules/<your moduleID>/get_realtime_info"
headers = {
    "Accept": "application/json",
    "Authorization": "Bearer <your api token>"
}

# Get the data
response = requests.get(url, headers=headers)

if response.status_code == 200:
    data = response.json()
    print(json.dumps(data, indent=4, sort_keys=True))
    
    # Extract the 'common' data
    common_data = data.get("data", {}).get("common", {})
    
    # Prepare headers for Home Assistant API
    ha_headers = {
        "Authorization": f"Bearer {home_assistant_token}",
        "Content-Type": "application/json",
    }
    
    # Update entities in Home Assistant
    for key, value in common_data.items():
        entity_id = f"sensor.{key}"
        entity_data = {
            "state": value,
            "attributes": {
                "friendly_name": key.replace('_', ' ').title(),
                "unit_of_measurement": ""  # Add appropriate units if needed
            }
        }
        
        ha_response = requests.post(f"{home_assistant_url}/{entity_id}", headers=ha_headers, data=json.dumps(entity_data))
        
        if ha_response.status_code in (200, 201):
            print(f"Successfully updated {entity_id}")
        else:
            print(f"Failed to update {entity_id}. Status code: {ha_response.status_code}")
else:
    print(f"Request failed with status code {response.status_code}")
