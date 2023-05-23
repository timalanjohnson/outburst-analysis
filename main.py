from outburst_analysis.data import DataFromCSV
from outburst_analysis.analysis import (
    ColourAnalysis,
    SuperOutburstAnalysis,
    OutburstAnalysis,
)


atlas_and_meerlicht = DataFromCSV("./data/copy.csv").atlas_and_meerlicht()
SuperOutburstAnalysis(atlas_and_meerlicht, so_boundary=15.42, q_boundary=17.34)
OutburstAnalysis(atlas_and_meerlicht, l_boundary=15.5, o_boundary=17, q_boundary=22)


meerlicht = DataFromCSV("./data/CV_output.csv").meerlicht()
SuperOutburstAnalysis(meerlicht, so_boundary=15.42, q_boundary=17.34)
OutburstAnalysis(meerlicht, l_boundary=15.5, o_boundary=17, q_boundary=22)

colour_analysis = ColourAnalysis(meerlicht)

uq_points = colour_analysis.result.uq_points


list_of_q_minus_u_magnitudes = []
list_of_absolute_q_magnitudes = []
for uq_point in uq_points:
    list_of_q_minus_u_magnitudes.append(uq_point.uq)
    list_of_absolute_q_magnitudes.append(uq_point.q.absolute_magnitude)
    uq_point.q.magnitude
    uq_point.q.time
    uq_point.u.time
    uq_point.average_time
    uq_point.q.absolute_magnitude

def plot(x_axis: list, y_axis: list):
    pass

plot(list_of_q_minus_u_magnitudes, list_of_absolute_q_magnitudes)