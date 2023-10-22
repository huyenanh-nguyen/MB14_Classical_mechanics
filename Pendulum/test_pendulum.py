import pytest
from pathlib import Path, PurePath
from pendulum import Pendulum


def test_turning_point_stats():

    excelpath = PurePath(str(Path.cwd()) + "/F3_Fadenpendel.xlsx")
    test = Pendulum(excelpath)
    results = test.turningpoint_period_stats()
    assert results[0] == pytest.approx(1.994, 1)