from outburst_analysis import utils

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
ColourAnalysis(meerlicht)
