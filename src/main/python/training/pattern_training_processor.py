from enum import Enum

from src.main.python.tools.geometry import DEG_2_RAD, Point3D, format_angle


class PatternStep(Enum):
    CROSSWIND = 0
    DOWNWIND = 1
    BASE = 2
    FINAL = 3


class Runway:
    def __init__(self, _th1: Point3D, _th2: Point3D) -> None:
        self.th1 = _th1
        self.th2 = _th2
        self.qfu = self.th2.relevement(self.th1) / DEG_2_RAD  # in rad


class Pattern:
    def __init__(
        self,
        _runway: Runway,
        _is_left_hand: bool,
        _final_offset: int,
        _downwind_offset: int,
        _altitude_offset: int,
    ):
        self.runway = _runway
        self.is_left_hand = _is_left_hand
        self.final_offset = _final_offset
        self.downwind_offset = _downwind_offset
        self.altitude_offset = _altitude_offset


def compute_init_position(pattern: Pattern, step: PatternStep, is_qfu: bool) -> Point3D:
    """Computes the initial position of the plane in the pattern

    Args:
        pattern (Pattern): the pattern
        step (PatternStep): the step in the pattern
        is_qfu (bool): if the preferential qfu is used or not

    Returns:
        Point3D: the initial position
    """
    match step:
        case PatternStep.DOWNWIND:
            if is_qfu:
                res_pt = Point3D(
                    pattern.runway.th2.lon,
                    pattern.runway.th2.lat,
                    pattern.runway.th2.altitude + pattern.altitude_offset,
                )
            else:
                res_pt = Point3D(
                    pattern.runway.th1.lon,
                    pattern.runway.th1.lat,
                    pattern.runway.th1.altitude + pattern.altitude_offset,
                )
            if pattern.is_left_hand:
                res_pt.add_distance(pattern.downwind_offset, pattern.runway.qfu - 90)
            else:
                res_pt.add_distance(pattern.downwind_offset, pattern.runway.qfu + 90)
        case PatternStep.BASE:
            if is_qfu:
                res_pt = Point3D(
                    pattern.runway.th1.lon,
                    pattern.runway.th1.lat,
                    pattern.runway.th1.altitude + pattern.altitude_offset,
                )
                res_pt.add_distance(pattern.final_offset, pattern.runway.qfu - 180)
            else:
                res_pt = Point3D(
                    pattern.runway.th2.lon,
                    pattern.runway.th2.lat,
                    pattern.runway.th2.altitude + pattern.altitude_offset,
                )
                res_pt.add_distance(pattern.final_offset, pattern.runway.qfu)
            if pattern.is_left_hand:
                res_pt.add_distance(pattern.downwind_offset, pattern.runway.qfu - 90)
            else:
                res_pt.add_distance(pattern.downwind_offset, pattern.runway.qfu + 90)
        case PatternStep.FINAL:
            if is_qfu:
                res_pt = Point3D(
                    pattern.runway.th1.lon,
                    pattern.runway.th1.lat,
                    pattern.runway.th1.altitude + pattern.altitude_offset,
                )
                res_pt.add_distance(pattern.final_offset, pattern.runway.qfu - 180)
            else:
                res_pt = Point3D(
                    pattern.runway.th2.lon,
                    pattern.runway.th2.lat,
                    pattern.runway.th2.altitude + pattern.altitude_offset,
                )
                res_pt.add_distance(pattern.final_offset, pattern.runway.qfu)
    return res_pt

def compute_init_direction(pattern: Pattern, step: PatternStep, is_qfu: bool) -> float:
    """Computes the initial direction in degrees of the plane in the pattern

    Args:
        pattern (Pattern): the pattern
        step (PatternStep): the step in the pattern
        is_qfu (bool): if the preferential qfu is used or not

    Returns:
        Point3D: the initial direction (in degrees)
    """
    match step:
        case PatternStep.DOWNWIND:
            if is_qfu:
                res_dir = pattern.runway.qfu+180
            else:
                res_dir = pattern.runway.qfu
        case PatternStep.BASE:
            if is_qfu:
                if pattern.is_left_hand:
                    res_dir = pattern.runway.qfu + 90
                else:
                    res_dir = pattern.runway.qfu - 90
            else:
                if pattern.is_left_hand:
                    res_dir = pattern.runway.qfu - 90
                else:
                    res_dir = pattern.runway.qfu + 90
        case PatternStep.FINAL:
            if is_qfu:
                res_dir = pattern.runway.qfu
            else:
                res_dir = pattern.runway.qfu+180
    return format_angle(res_dir)