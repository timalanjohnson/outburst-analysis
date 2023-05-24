import time

from outburst_analysis import (
    DataFromCSV,
    ColourAnalysis,
    StarAnalysis,
    SuperOutburstAnalysis,
    OutburstAnalysis,
)


# atlas_and_meerlicht = DataFromCSV("./data/copy.csv").atlas_and_meerlicht()
# SuperOutburstAnalysis(atlas_and_meerlicht, so_boundary=15.42, q_boundary=17.34)
# OutburstAnalysis(atlas_and_meerlicht, l_boundary=15.5, o_boundary=17, q_boundary=22)


# meerlicht = DataFromCSV("./data/CV_output.csv").meerlicht()
# super_outburst_analysis = SuperOutburstAnalysis(
#     meerlicht, so_boundary=15.42, q_boundary=17.34
# )
# outburst_analysis = OutburstAnalysis(
#     meerlicht, l_boundary=15.5, o_boundary=17, q_boundary=22
# )
# colour_analysis = ColourAnalysis(meerlicht)

# uq_points = colour_analysis.result.uq_points

# list_of_q_minus_u_magnitudes = [i.uq for i in uq_points]
# list_of_q_magnitudes = [i.q.magnitude for i in uq_points]
# list_of_q_times = [i.q.time for i in uq_points]
# list_of_u_times = [i.u.time for i in uq_points]
# list_of_average_time_times = [i.average_time for i in uq_points]
# list_of_absolute_q_magnitudes = [i.q.absolute_magnitude for i in uq_points]


# def plot(x_axis: list, y_axis: list):
#     pass


# plot(list_of_q_minus_u_magnitudes, list_of_absolute_q_magnitudes)

print("Reading uqriq_ml_catalogue.csv ...")
read_start = time.time()
stars = DataFromCSV("./data/uqriq_ml_catalogue.csv").meerlicht_catalogue()
read_end = time.time()
read_duration = read_end - read_start
print("Read completed in {}".format(read_duration))

print("Starting star analysis ...")
start = time.time()
star_analysis = StarAnalysis(stars)
end = time.time()
duration = end - start
print("Star analysis completed in {}".format(duration))
