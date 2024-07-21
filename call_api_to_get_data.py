import requests

def get_distance_and_duration(api_key, origin, destination):
    base_url = "https://maps.googleapis.com/maps/api/distancematrix/json"
    params = {
        "origins": origin,
        "destinations": destination,
        "key": api_key,
        "mode": "driving",  # You can change this to walking, bicycling, or transit
        "departure_time": "now"  # For live traffic conditions
    }

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        data = response.json()
        if data['rows'][0]['elements'][0]['status'] == 'OK':
            distance_text = data['rows'][0]['elements'][0]['distance']['text']
            duration_text = data['rows'][0]['elements'][0]['duration']['text']
            distance_value = data['rows'][0]['elements'][0]['distance']['value']
            duration_value = data['rows'][0]['elements'][0]['duration']['value']

            return distance_text, duration_text, distance_value, duration_value
        else:
            return "No route found", "No route found"
    else:
        return f"Error: {response.status_code}", f"Error: {response.status_code}"


