import numpy as np
from flask import Flask, render_template, request, redirect, url_for
from city_dataframe_generation import generate_city_permutations
from config import api_key
from call_api_to_get_data import get_distance_and_duration
from matrix_creation import create_distance_matrix
from matrix_creation import create_duration_matrix
from python_tsp.exact import solve_tsp_dynamic_programming
from create_optimal_route import optimal_route_creation
from clean_city_names_for_google_maps import replace_spaces_with_underscores_in_city_names
from create_web_url import generate_google_maps_url

app = Flask(__name__)

@app.route('/')
def webpage():
    return render_template('webpage.html')

@app.route('/submit', methods=['POST'])
def submit():
    num_stops = request.form.get('numStops')
    num_stops = int(num_stops)
    cities = [request.form.get(f'location{i + 1}') for i in range(int(num_stops))]  # Get the list of cities from the form
    route_chosen = request.form.get('routeType')

    '''variables = []
    for i in range(len(cities)):
        variables.append(f'city_{i + 1}')
        
    for i in range(len(cities)):
        variables[i] = cities[i]'''

    # formatted_cities = {f'city_{i + 1}': city for i, city in enumerate(cities)}

    # Check if cities list is not empty
    if not cities:
        return "No cities provided", 400
    if not route_chosen:
        return "No route type provided", 400

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

    optimal_route = []
    if route_chosen == "shortest":
        distance_dictionary = city_dataframe.set_index(['source', 'destination'])['distance_number'].to_dict()
        distance_matrix = create_distance_matrix(city_dataframe, distance_dictionary)
        distance_matrix = np.array(distance_matrix)
        optimal_route_order, total_distance = solve_tsp_dynamic_programming(distance_matrix)
        city_id_dictionary = city_dataframe[['city_id', 'source']].drop_duplicates().set_index(['city_id'])['source'].to_dict()
        optimal_route = optimal_route_creation(city_id_dictionary, optimal_route_order)

    elif route_chosen == "fastest":
        duration_dictionary = city_dataframe.set_index(['source', 'destination'])['duration_number'].to_dict()
        duration_matrix = create_duration_matrix(city_dataframe, duration_dictionary)
        duration_matrix = np.array(duration_matrix)
        optimal_route_order, total_duration = solve_tsp_dynamic_programming(duration_matrix)
        city_id_dictionary = city_dataframe[['city_id', 'source']].drop_duplicates().set_index(['city_id'])['source'].to_dict()
        optimal_route = optimal_route_creation(city_id_dictionary, optimal_route_order)

    optimal_route = replace_spaces_with_underscores_in_city_names(optimal_route)
    google_maps_url = generate_google_maps_url(optimal_route)

    '''template_vars = {
        'url': google_maps_url,
        'num_stops': num_stops,
        'route_type': route_chosen
    }
    template_vars.update(formatted_cities)

    print(template_vars)'''

    return render_template('webpage.html', url=google_maps_url,num_stops=num_stops, locations=cities, route_type=route_chosen)

if __name__ == '__main__':
    app.run(debug=True)