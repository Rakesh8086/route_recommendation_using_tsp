
def replace_spaces_with_underscores_in_city_names(route):
    # Create a new list with spaces replaced by underscores
    updated_route = [city.replace(' ', '_') for city in route]
    return updated_route