
def create_distance_matrix(df, distance_dictionary):
    distance_matrix = []
    for source in df.source.unique().tolist():
        distance_from_each_place_to_other = []
        for destination in df.destination.unique().tolist():
            distance_from_each_place_to_other.append(distance_dictionary[source, destination])
        distance_matrix.append(distance_from_each_place_to_other)

    return distance_matrix