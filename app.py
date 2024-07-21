from flask import Flask, request, render_template
from city_dataframe_generation import generate_city_permutations
from config import api_key
from call_api_to_get_data import get_distance_and_duration
from matrix_creation import create_distance_matrix

app = Flask(__name__)

@app.route('/')
def webpage():
    return render_template('webpage.html')

@app.route('/submit', methods=['POST', 'GET'])
def submit():
    num_stops = request.form.get('numStops')
    cities = [request.form.get(f'location{i + 1}') for i in range(int(num_stops))]  # Get the list of cities from the form

    # Check if cities list is not empty
    if not cities:
        return "No cities provided", 400

    city_dataframe = generate_city_permutations(cities)

    # Your Google Maps API key
    google_maps_api_key = api_key

    # Iterate over each row in the DataFrame and update it with distance and duration
    for index, row in city_dataframe.iterrows():
        if row['source'] == row['destination']:
            city_dataframe.at[index, 'distance_text'] = 0
            city_dataframe.at[index, 'duration_text'] = 0
            city_dataframe.at[index, 'distance_number'] = 0
            city_dataframe.at[index, 'duration_number'] = 0
        else:
            origin = row['source']
            destination = row['destination']
            distance_text, duration_text, distance_value, duration_value = get_distance_and_duration(google_maps_api_key, origin,
                                                                                                     destination)
            city_dataframe.at[index, 'distance_text'] = distance_text
            city_dataframe.at[index, 'duration_text'] = duration_text
            city_dataframe.at[index, 'distance_number'] = distance_value
            city_dataframe.at[index, 'duration_number'] = duration_value

    print(city_dataframe)

    return 'Data received and processed.'

if __name__ == '__main__':
    app.run(debug=True)