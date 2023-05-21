from outburst_analysis import utils


class Colors:
    PASSED = "\033[92m"
    FAILED = "\033[93m"
    ERRORED = "\033[91m"
    END = "\033[0m"


def test_decorator(function):
    def wrapper():
        try:
            function()
            print(function.__name__, Colors.PASSED, "PASSED", Colors.END)
        except AssertionError:
            print(function.__name__, Colors.FAILED, "FAILED", Colors.END)
        except:
            print(function.__name__, Colors.ERRORED, "UNKNOWN ERROR", Colors.END)

    return wrapper


@test_decorator
def test_get_next_or_last():
    list = ["a", "b", "c", "d"]

    assert utils.get_next_or_last(list, 0) == "b"
    assert utils.get_next_or_last(list, 1) == "c"
    assert utils.get_next_or_last(list, 3) == "d"


@test_decorator
def test_get_peak_magnitude():
    data_points = [{"magnitude": 5}, {"magnitude": 4}, {"magnitude": 6}]

    assert utils.get_peak_magnitude(data_points) == {"magnitude": 4}


@test_decorator
def test_calc_upper_limit():
    data_points = [{"time": 10}, {"time": 11}, {"time": 12}, {"time": 13}, {"time": 14}]

    assert utils.calc_upper_limit(data_points) == 14 - 10


@test_decorator
def test_calc_lower_limit():
    data_points = [{"time": 10}, {"time": 11}, {"time": 12}]

    assert utils.calc_lower_limit(data_points) == 0

    data_points = [{"time": 10}, {"time": 11}, {"time": 12}, {"time": 13}, {"time": 14}]

    assert utils.calc_lower_limit(data_points) == 13 - 11


test_get_next_or_last()
test_get_peak_magnitude()
test_calc_upper_limit()
test_calc_lower_limit()
