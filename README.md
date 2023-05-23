# Outburst Analysis

<sub>_Authored by Timothy Johnson & Sumari Faul_</sub>

This script processes outburst data into a list of outbursts, a list of upper limits of the outbursts, a list of lower limits of the outbursts, and the time between the outbursts' peak magnitudes.

## Preparing the data

The data should be in CSV format. The first column should be time, the second column should be magnitude, and the third column should be error. See example below:

```
57303.453887,18.819,0.240
57303.475996,18.027,0.103
57303.483013,17.975,0.098
```

## Running the script

To run the script, simply run:

```
$ python main.py
```

To use the result of the script, you will have to modify the script.

## Testing

There are rudimentary tests for the utils functions in the OutburstAnalysis package.

You can run the tests with:

```
$ python test.py
```
