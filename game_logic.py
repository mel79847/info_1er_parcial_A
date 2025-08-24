import math
import arcade
from dataclasses import dataclass
from logging import getLogger

logger = getLogger(__name__)


@dataclass
class ImpulseVector:
    angle: float
    impulse: float


@dataclass
class Point2D:
    x: float = 0
    y: float = 0


def get_angle_radians(point_a: Point2D, point_b: Point2D) -> float:
    """angulo (en radianes) del vector A→B respecto al eje X positivo. donde A es el punto de inicio y B el final"""
    dx = point_b.x - point_a.x
    dy = point_b.y - point_a.y
    return math.atan2(dy, dx)


def get_distance(point_a: Point2D, point_b: Point2D) -> float:
    """distancia entre A y B"""
    dx = point_b.x - point_a.x
    dy = point_b.y - point_a.y
    return math.hypot(dx, dy)


def get_impulse_vector(start_point: Point2D, end_point: Point2D) -> ImpulseVector:
    """ vector de impulso desde start_point a end_point, es negativo para que salga en dirección contraria a la que se apunta"""
    angle = get_angle_radians(start_point, end_point)
    distance = get_distance(start_point, end_point)
    impulse = -distance  # negativo para que salga en dirección contraria a la que se apunta jiji
    return ImpulseVector(angle, impulse)
