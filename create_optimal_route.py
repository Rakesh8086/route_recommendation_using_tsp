
def optimal_route_creation(city_id_dictionary, permutation):
    route = []
    for i in permutation:
        route.append(city_id_dictionary[i])
    route.append(city_id_dictionary[0])
    return route