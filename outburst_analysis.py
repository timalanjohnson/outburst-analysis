import numpy as np

class Observation:
    def __init__(self, time: float, magnitude: float, error: float, filter: str):
        self.time = time
        self.magnitude = magnitude
        self.error = error
        self.filter = filter
        self.absolute_magnitude = magnitude + 5 - (5 * np.log10(663.482))


class Star:
    def __init__(
        self,
        distance,
        q_magnitude,
        q_magnitude_error,
        u_magnitude,
        u_magnitude_error,
        i_magnitude,
        i_magnitude_error,
        parallax_angle,
    ):
        self.distance = distance
        self.q_magnitude = q_magnitude
        self.q_magnitude_error = q_magnitude_error
        self.u_magnitude = u_magnitude
        self.u_magnitude_error = u_magnitude_error
        self.i_magnitude = i_magnitude
        self.i_magnitude_error = i_magnitude_error
        self.parallax_angle = parallax_angle
        self.absolute_magnitude = q_magnitude + 5 - (5 * np.log10(distance))
        self.uq = None if u_magnitude is None else u_magnitude - q_magnitude
        self.qi = None if i_magnitude is None else q_magnitude - i_magnitude


class StarAnalysis:
    def __init__(self, data: list[Star]):
        self.data = data

        self.run()

    def run(self):
        self.result = [star for star in self.data if star.parallax_angle < 0.2]


class Outburst:
    def __init__(
        self,
        data: list[Observation],
        peak_magnitude: list[Observation],
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


class UQPair:
    def __init__(self, u: Observation, q: Observation):
        self.u = u
        self.q = q
        self.uq = None if u is None else u.magnitude - q.magnitude
        self.average_time = (u.time + q.time) / 2


class QIPair:
    def __init__(self, q: Observation, i: Observation):
        self.q = q
        self.i = i
        self.qi = None if i is None else q.magnitude - i.magnitude
        self.average_time = (i.time + q.time) / 2


class ColourAnalysisResult:
    def __init__(self, uq_points: list[UQPair], qi_points: list[QIPair]):
        self.uq_points = uq_points
        self.qi_points = qi_points


class DataFromCSV:
    def __init__(self, path_to_csv: str):
        self.path_to_csv = path_to_csv

    def atlas_and_meerlicht(self):
        data: list[Observation] = []

        with open(self.path_to_csv, "r") as file:
            next(file)
            for line in file:
                columns = line.split(",")

                time = columns[0]
                magnitude = columns[1]
                error = columns[2]

                data.append(
                    Observation(float(time), float(magnitude), float(error), "")
                )

        return data

    def meerlicht(self):
        data: list[Observation] = []

        with open(self.path_to_csv, "r") as file:
            next(file)
            for line in file:
                columns = line.split(",")

                time = columns[6]
                magnitude = columns[17]
                error = columns[18]
                filter = columns[8]

                data.append(
                    Observation(
                        float(time),
                        float(magnitude),
                        float(error),
                        filter,
                    )
                )

        return data

    def meerlicht_catalogue(self):
        data: list[Star] = []

        with open(self.path_to_csv, "r") as file:
            next(file)
            for line in file:
                columns = line.split(",")

                distance = columns[28]
                q_magnitude = columns[10]
                q_magnitude_error = columns[11]
                u_magnitude = columns[2]
                u_magnitude_error = columns[3]
                i_magnitude = columns[8]
                i_magnitude_error = columns[9]
                parallax_angle = columns[32]

                data.append(
                    Star(
                        distance=float(distance),
                        q_magnitude=float(q_magnitude),
                        q_magnitude_error=float(q_magnitude_error),
                        u_magnitude=float(u_magnitude),
                        u_magnitude_error=float(u_magnitude_error),
                        i_magnitude=float(i_magnitude),
                        i_magnitude_error=float(i_magnitude_error),
                        parallax_angle=float(parallax_angle),
                    )
                )

        return data


class Analysis:
    def __init__(self, data: list[Observation]):
        self.data = data

    def _start(self):
        print("Starting {}".format(self.__class__.__name__))

    def _done(self):
        print("{} Completed.".format(self.__class__.__name__))


class ColourAnalysis(Analysis):
    def __init__(self, data: list[Observation]):
        super().__init__(data)
        self._setup()
        self.run()

    def _setup(self):
        self.result: ColourAnalysisResult = None
        self.uq_points: list[UQPair] = []
        self.qi_points: list[QIPair] = []

    def _find_nearest_point(self, index, target_filter, time):
        index_offset = 10
        time_offset = 0.0083
        search_index = index - index_offset if index > index_offset else 0
        time_start = time - time_offset
        time_end = time + time_offset
        nearest_point = None
        nearest_difference = None

        for i, point in enumerate(self.data[search_index:]):
            if point.time < time_start:
                continue
            if point.time > time_end:
                break

            if point.filter == target_filter:
                difference = Utils.calculate_difference(index_offset, i)
                if nearest_difference is None or difference < nearest_difference:
                    nearest_difference = difference
                    nearest_point = point

        return nearest_point

    def _analyze(self):
        for index, point in enumerate(self.data):
            if point.filter == "q":
                q = point

                u = self._find_nearest_point(index, "u", q.time)
                if u is not None:
                    self.uq_points.append(UQPair(u, q))

                i = self._find_nearest_point(index, "i", q.time)
                if i is not None:
                    self.qi_points.append(QIPair(q, i))

    def run(self):
        self._start()
        self._analyze()
        self.result = ColourAnalysisResult(self.uq_points, self.qi_points)
        print("Number of data points", len(self.data))
        print("Number of UQ points", len(self.uq_points))
        print("Number of QI points", len(self.qi_points))
        self._done()


class OutburstAnalysis(Analysis):
    def __init__(self, data, l_boundary, o_boundary, q_boundary):
        super().__init__(data)
        self.l_boundary = l_boundary
        self.o_boundary = o_boundary
        self.q_boundary = q_boundary
        self._setup()
        self.run()

    def _setup(self):
        self.filtered_data: list[Observation] = []
        self.outbursts: list[Outburst] = []
        self.upper_limits = []
        self.lower_limits = []
        self.time_between_peak_magnitudes = []
        self.result: OutburstAnalysisResult = None

    def _append_outburst(self, new_outburst_data):
        self.outbursts.append(
            Outburst(
                new_outburst_data,
                Utils.get_peak_magnitude(new_outburst_data),
                Utils.calc_upper_limit(new_outburst_data),
                Utils.calc_lower_limit(new_outburst_data),
            )
        )

    def _find_upper_limits(self):
        for outburst in self.outbursts:
            self.upper_limits.append(outburst.upper_limit)

    def _find_lower_limits(self):
        for outburst in self.outbursts:
            self.lower_limits.append(outburst.lower_limit)

    def _find_time_between_peak_magnitudes(self):
        for i, outburst in enumerate(self.outbursts):
            next_outburst: Outburst = Utils.get_next_or_last(self.outbursts, i)
            time = next_outburst.peak_magnitude.time - outburst.peak_magnitude.time
            self.time_between_peak_magnitudes.append(time)

    def _filter_data(self):
        for point in self.data:
            if (
                point.magnitude >= self.l_boundary
                and point.magnitude <= self.q_boundary
            ):
                self.filtered_data.append(point)

    def _find_outbursts(self):
        new_outburst_data: list[Observation] = []

        for i, current_point in enumerate(self.filtered_data):
            previous_point: Observation = Utils.get_previous_or_first(
                self.filtered_data, i
            )
            next_point: Observation = Utils.get_next_or_last(self.filtered_data, i)

            is_outburst = (
                current_point.magnitude >= self.l_boundary
                and current_point.magnitude <= self.o_boundary
            )
            is_first_outburst = (
                is_outburst and previous_point.magnitude >= self.o_boundary
            )
            is_last_outburst = is_outburst and next_point.magnitude >= self.o_boundary

            if is_first_outburst:
                new_outburst_data.append(previous_point)
            if is_outburst:
                new_outburst_data.append(current_point)
            if is_last_outburst:
                new_outburst_data.append(next_point)
                self._append_outburst(new_outburst_data)
                new_outburst_data = []

    def _done_(self):
        print("Number of data points:", len(self.data))
        print("Number of filtered data points:", len(self.filtered_data))
        print("Number of outbursts:", len(self.outbursts))
        print("{} Completed.".format(self.__class__.__name__))

    def run(self):
        self._start()
        self._filter_data()
        self._find_outbursts()
        self._find_upper_limits()
        self._find_lower_limits()
        self._find_time_between_peak_magnitudes()
        self.result = OutburstAnalysisResult(
            self.outbursts,
            self.upper_limits,
            self.lower_limits,
            self.time_between_peak_magnitudes,
        )
        print(len(self.outbursts))
        self._done()


class SuperOutburstAnalysis(OutburstAnalysis):
    def __init__(self, data, so_boundary, q_boundary):
        self.data = data
        self.so_boundary = so_boundary
        self.q_boundary = q_boundary
        self._setup()
        self.run()

    def _filter_data(self):
        for point in self.data:
            if (
                point.magnitude <= self.so_boundary
                or point.magnitude >= self.q_boundary
            ):
                self.filtered_data.append(point)

    def _find_outbursts(self):
        new_outburst_data: list[Observation] = []

        for i, current_point in enumerate(self.filtered_data):
            previous_point: Observation = Utils.get_previous_or_first(
                self.filtered_data, i
            )
            next_point: Observation = Utils.get_next_or_last(self.filtered_data, i)

            is_outburst = current_point.magnitude <= self.so_boundary
            is_first_outburst = (
                is_outburst and previous_point.magnitude >= self.so_boundary
            )
            is_last_outburst = is_outburst and next_point.magnitude >= self.so_boundary

            if is_first_outburst:
                new_outburst_data.append(previous_point)
            if is_outburst:
                new_outburst_data.append(current_point)
            if is_last_outburst:
                new_outburst_data.append(next_point)
                self._append_outburst(new_outburst_data)
                new_outburst_data = []


class Utils:
    def get_next_or_last(list: list, index=0):
        """
        return the next element in a list or last element if at the end of a list
        """
        return list[index + 1] if index < len(list) - 1 else list[index]

    def get_previous_or_first(list: list, index=0):
        return list[index - 1] if index > 0 else list[index]

    def calc_upper_limit(data_points):
        """
        return the timer difference between the last and first data points of a super outburst
        """
        end_index = len(data_points) - 1

        start_time = data_points[0].time
        end_time = data_points[end_index].time

        return end_time - start_time

    def calc_lower_limit(data_points):
        """
        return the time difference between normal the data points around a super outburst
        """
        if len(data_points) <= 3:
            return 0

        end_index = len(data_points) - 2

        start_time = data_points[1].time
        end_time = data_points[end_index].time

        return end_time - start_time

    def get_peak_magnitude(data_points: list[Observation]):
        """
        return the data point of the peak magnitude
        """
        peak_magnitude = data_points[0].magnitude
        peak_magnitude_index = 0

        for index, point in enumerate(data_points):
            if point.magnitude < peak_magnitude:
                peak_magnitude = point.magnitude
                peak_magnitude_index = index

        return data_points[peak_magnitude_index]

    def calculate_difference(a, b):
        difference = 0

        if a > b:
            difference = a - b
        else:
            difference = b - a

        return difference
