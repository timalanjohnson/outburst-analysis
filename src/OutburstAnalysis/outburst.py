import sys

from OutburstAnalysis import utils


L_BOUNDARY = 15.5
O_BOUNDARY = 17
Q_BOUNDARY = 22


# Take input file and append data points
data_points = []
input = sys.argv[1]
with open(input, "r") as f:
    for line in f:
        columns = line.split(",")

        time = columns[0]
        magnitude = columns[1]
        error = columns[2]

        data_points.append(
            {
                "time": float(time),
                "magnitude": float(magnitude),
                "error": float(error),
            }
        )

# Filter out transitionary data points
filtered_data_points = utils.filter_data_points_outburst(
    data_points, lower_limit=L_BOUNDARY, upper_limit=Q_BOUNDARY
)


# Find outbursts
outbursts = []
new_outburst_data = []
for index, point in enumerate(filtered_data_points):
    prev = filtered_data_points[index - 1] if index > 0 else point
    next = utils.get_next_or_last(filtered_data_points, index)

    is_outburst = point["magnitude"] >= L_BOUNDARY and point["magnitude"] <= O_BOUNDARY
    is_first_outburst = is_outburst and prev["magnitude"] >= O_BOUNDARY
    is_last_outburst = is_outburst and next["magnitude"] >= O_BOUNDARY

    if is_first_outburst:
        new_outburst_data.append(prev)

    if is_outburst:
        new_outburst_data.append(point)

    if is_last_outburst:
        new_outburst_data.append(next)

        new_outburst = {
            "data_points": new_outburst_data,
            "peak_magnitude": utils.get_peak_magnitude(new_outburst_data),
            "upper_limit": utils.calc_upper_limit(new_outburst_data),
            "lower_limit": utils.calc_lower_limit(new_outburst_data),
        }

        outbursts.append(new_outburst)
        new_outburst_data = []


upper_limits = []
for outburst in outbursts:
    upper_limits.append(outburst["upper_limit"])


lower_limits = []
for outburst in outbursts:
    lower_limits.append(outburst["lower_limit"])


time_between_peak_magnitudes = []
for index, outburst in enumerate(outbursts):
    next = utils.get_next_or_last(outbursts, index)

    time = next["peak_magnitude"]["time"] - outburst["peak_magnitude"]["time"]
    time_between_peak_magnitudes.append(time)


result = {
    "outbursts": outbursts,
    "upper_limits": upper_limits,
    "lower_limits": lower_limits,
    "time_between_peak_magnitudes": time_between_peak_magnitudes,
}

print("OK")