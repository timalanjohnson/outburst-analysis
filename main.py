from outburst_analysis import utils

from outburst_analysis.data import DataFromCSV
from outburst_analysis.analysis import (
    ColourAnalysis,
    SuperOutburstAnalysis,
    OutburstAnalysis,
)


data = DataFromCSV("./data/CV_output.csv").meerlicht()


SuperOutburstAnalysis(data, so_boundary=15.42, q_boundary=17.34)
OutburstAnalysis(data, l_boundary=15.5, o_boundary=17, q_boundary=22)
ColourAnalysis(data)


data2 = DataFromCSV("./data/copy.csv").atlas_and_meerlicht()
SuperOutburstAnalysis(data2, so_boundary=15.42, q_boundary=17.34)
OutburstAnalysis(data2, l_boundary=15.5, o_boundary=17, q_boundary=22)
