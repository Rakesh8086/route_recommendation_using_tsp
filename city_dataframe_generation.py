import pandas as pd
import itertools


def generate_city_permutations(cities):
    # Generate all permutations of the cities, including pairs with the same source and destination
    permutations = list(itertools.product(cities, repeat=2))

    # Initialize lists to store the data for the DataFrame
    sources = []
    destinations = []
    duration_numbers = []
    distance_numbers = []
    duration_texts = []
    distance_texts = []
    city_ids = []

    city_id_map = {city: idx for idx, city in enumerate(cities)}

    # Populate the lists with the permutation data
    for source, destination in permutations:
        sources.append(source)
        destinations.append(destination)
        # For demonstration, we'll use placeholder values for duration and distance
        duration_numbers.append(0)  # Placeholder
        distance_numbers.append(0)  # Placeholder
        duration_texts.append("0 mins")  # Placeholder
        distance_texts.append("0 km")  # Placeholder
        city_ids.append(city_id_map[source])

    # Create the DataFrame
    df = pd.DataFrame({
        'source': sources,
        'destination': destinations,
        'duration_number': duration_numbers,
        'distance_number': distance_numbers,
        'duration_text': duration_texts,
        'distance_text': distance_texts,
        'city_id': city_ids
    })

    return df


