import webbrowser

def generate_google_maps_url(optimal_route):
    base_url = "https://www.google.com/maps/dir/?api=1"
    origin = optimal_route[0]
    destination = optimal_route[-1]
    waypoints = optimal_route[1:-1]  # Exclude origin and destination

    # Create waypoints string
    waypoints_str = "|".join(waypoints)

    # Generate URL
    maps_url = f"{base_url}&origin={origin}&destination={destination}&waypoints={waypoints_str}"

    return maps_url
