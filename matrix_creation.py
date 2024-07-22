
def create_distance_matrix(dataframe, distance_dictionary):
    distance_matrix = []
    for source in dataframe.source.unique().tolist():
        distance_from_each_place_to_other = []
        for destination in dataframe.destination.unique().tolist():
            distance_from_each_place_to_other.append(distance_dictionary[source, destination])
        distance_matrix.append(distance_from_each_place_to_other)

    return distance_matrix

def create_duration_matrix(dataframe, duration_dictionary):
    duration_matrix = []
    for source in dataframe.source.unique().tolist():
        duration_1d = []
        for destination in dataframe.destination.unique().tolist():
            duration_1d.append(duration_dictionary[source, destination])
        duration_matrix.append(duration_1d)

    return duration_matrix