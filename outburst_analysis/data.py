import numpy as np

class DataPoint:
    def __init__(self, time: float, magnitude: float, error: float, filter: str):
        self.time = time
        self.magnitude = magnitude
        self.error = error
        self.filter = filter
        self.absolute_magnitude = magnitude + 5 - (5 * np.log10(663.482))


class Outburst:
    def __init__(
        self,
        data: list[DataPoint],
        peak_magnitude: list[DataPoint],
        upper_limit: float,
        lower_limit: float,
    ):
        self.data = data
        self.peak_magnitude = peak_magnitude
        self.upper_limit = upper_limit
        self.lower_limit = lower_limit


class OutburstAnalysisResult:
    def __init__(
        self,
        outbursts: list[Outburst],
        upper_limits: list[float],
        lower_limits: list[float],
        time_between_peak_magnitudes: list[float],
    ):
        self.outbursts = outbursts
        self.upper_limits = upper_limits
        self.lower_limits = lower_limits
        self.time_between_peak_magnitudes = time_between_peak_magnitudes


class UQ:
    def __init__(self, u: DataPoint, q: DataPoint):
        self.u = u
        self.q = q
        self.uq = None if u is None else u.magnitude - q.magnitude
        self.average_time = (u.time + q.time) / 2


class QI:
    def __init__(self, q: DataPoint, i: DataPoint):
        self.q = q
        self.i = i
        self.qi = None if i is None else q.magnitude - i.magnitude


class ColourAnalysisResult:
    def __init__(self, uq_points: list[UQ], qi_points: list[QI]):
        self.uq_points = uq_points
        self.qi_points = qi_points


class DataFromCSV:
    def __init__(self, path_to_csv: str):
        self.path_to_csv = path_to_csv

    def atlas_and_meerlicht(self):
        data: list[DataPoint] = []

        with open(self.path_to_csv, "r") as file:
            for line in file:
                columns = line.split(",")

                time = columns[0]
                magnitude = columns[1]
                error = columns[2]

                data.append(DataPoint(float(time), float(magnitude), float(error), ""))

        return data

    def meerlicht(self):
        data: list[DataPoint] = []

        with open(self.path_to_csv, "r") as file:
            for line in file:
                columns = line.split(",")

                time = columns[6]
                magnitude = columns[17]
                error = columns[18]
                filter = columns[8]

                data.append(
                    DataPoint(
                        float(time),
                        float(magnitude),
                        float(error),
                        filter,
                    )
                )

        return data
