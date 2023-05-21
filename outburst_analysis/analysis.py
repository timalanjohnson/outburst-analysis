from .data import (
    QI,
    UQ,
    ColourAnalysisResult,
    DataPoint,
    Outburst,
    OutburstAnalysisResult,
)
from . import utils


class Analysis:
    def __init__(self, data: list[DataPoint]):
        self.data = data

    def _start(self):
        print("Starting {}".format(self.__class__.__name__))

    def _done(self):
        print("{} Completed.".format(self.__class__.__name__))


class ColourAnalysis(Analysis):
    def __init__(self, data: list[DataPoint]):
        super().__init__(data)
        self._setup()
        self.run()

    def _setup(self):
        self.result: ColourAnalysisResult = None
        self.uq_points: list[UQ] = []
        self.qi_points: list[QI] = []

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
                difference = utils.calculate_difference(index_offset, i)
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
                    self.uq_points.append(UQ(u, q))

                i = self._find_nearest_point(index, "i", q.time)
                if i is not None:
                    self.qi_points.append(QI(q, i))

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
        self.filtered_data: list[DataPoint] = []
        self.outbursts: list[Outburst] = []
        self.upper_limits = []
        self.lower_limits = []
        self.time_between_peak_magnitudes = []
        self.result: OutburstAnalysisResult = None

    def _append_outburst(self, new_outburst_data):
        self.outbursts.append(
            Outburst(
                new_outburst_data,
                utils.get_peak_magnitude(new_outburst_data),
                utils.calc_upper_limit(new_outburst_data),
                utils.calc_lower_limit(new_outburst_data),
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
            next_outburst: Outburst = utils.get_next_or_last(self.outbursts, i)
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
        new_outburst_data: list[DataPoint] = []

        for i, current_point in enumerate(self.filtered_data):
            previous_point: DataPoint = utils.get_previous_or_first(
                self.filtered_data, i
            )
            next_point: DataPoint = utils.get_next_or_last(self.filtered_data, i)

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
        new_outburst_data: list[DataPoint] = []

        for i, current_point in enumerate(self.filtered_data):
            previous_point: DataPoint = utils.get_previous_or_first(
                self.filtered_data, i
            )
            next_point: DataPoint = utils.get_next_or_last(self.filtered_data, i)

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
