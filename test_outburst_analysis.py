from outburst_analysis import Analysis, Observation, calculate_difference


class TestClassUtils:
    def test_calculate_difference(self):
        assert calculate_difference(10, 5) == 5
        assert calculate_difference(5, 10) == 5


class TestClassAnalysis:
    def test_analysis_has_data(self):
        test_data = [Observation(22, 33, 44, "f"), Observation(55, 66, 77, "g")]
        analysis = Analysis(test_data)

        assert analysis.data == test_data
