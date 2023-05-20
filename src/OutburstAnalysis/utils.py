def get_next_or_last(list, index=0):
    """
    return the next element in a list or last element if at the end of a list
    """
    return list[index + 1] if index < len(list) - 1 else list[index]


def calc_upper_limit(data_points):
    """
    return the timer difference between the last and first data points of a super outburst
    """
    end_index = len(data_points) - 1

    start_time = data_points[0]["time"]
    end_time = data_points[end_index]["time"]

    return end_time - start_time


def calc_lower_limit(data_points):
    """
    return the time difference between normal the data points around a super outburst
    """
    if len(data_points) <= 3:
        return 0

    end_index = len(data_points) - 2

    start_time = data_points[1]["time"]
    end_time = data_points[end_index]["time"]

    return end_time - start_time


def get_peak_magnitude(data_points):
    """
    return the data point of the peak magnitude
    """
    peak_magnitude = data_points[0]["magnitude"]
    peak_magnitude_index = 0

    for index, point in enumerate(data_points):
        if point["magnitude"] < peak_magnitude:
            peak_magnitude = point["magnitude"]
            peak_magnitude_index = index

    return data_points[peak_magnitude_index]


def filter_data_points_super_outburst(data_points, lower_limit, upper_limit):
    """
    filter out the data points where the magnitude falls between the lower and upper limits

    returns a list of data points
    """
    filtered_data_points = []
    for point in data_points:
        if point["magnitude"] <= lower_limit or point["magnitude"] >= upper_limit:
            filtered_data_points.append(point)

    return filtered_data_points


def filter_data_points_outburst(data_points, lower_limit, upper_limit):
    filtered_data_points = []
    for point in data_points:
        if point["magnitude"] >= lower_limit and point["magnitude"] <= upper_limit:
            filtered_data_points.append(point)

    return filtered_data_points