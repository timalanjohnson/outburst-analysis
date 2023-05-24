import time

from outburst_analysis import (
    FormatData,
    ColourAnalysis,
    StarAnalysis,
    SuperOutburstAnalysis,
    OutburstAnalysis,
)


atlas_and_meerlicht = FormatData.atlas_and_meerlicht("./data/copy.csv")
SuperOutburstAnalysis(atlas_and_meerlicht, so_boundary=15.42, q_boundary=17.34)
OutburstAnalysis(atlas_and_meerlicht, l_boundary=15.5, o_boundary=17, q_boundary=22)


meerlicht = FormatData.meerlicht("./data/CV_output.csv")
super_outburst_analysis = SuperOutburstAnalysis(
    meerlicht, so_boundary=15.42, q_boundary=17.34
)
outburst_analysis = OutburstAnalysis(
    meerlicht, l_boundary=15.5, o_boundary=17, q_boundary=22
)
colour_analysis = ColourAnalysis(meerlicht)


print("Reading uqriq_ml_catalogue.csv ...")
read_start = time.time()
stars = FormatData.meerlicht_catalogue("./data/uqriq_ml_catalogue.csv")
read_end = time.time()
read_duration = read_end - read_start
print("Read completed in {}".format(read_duration))

print("Starting star analysis ...")
start = time.time()
star_analysis = StarAnalysis(stars)
end = time.time()
duration = end - start
print("Star analysis completed in {}".format(duration))
