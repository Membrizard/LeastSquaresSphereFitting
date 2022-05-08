import numpy

from scipy.linalg import norm, inv

from utils import Point, Points


def get_z_coordinate(center: Point, r: float, x: float, y: float) -> float:
    z = numpy.sqrt(
        abs(r ** 2 - (x - center.x) ** 2 - (y - center.y) ** 2)
    ) + center.z
    return z


def fit_sphere(points: Points):
    a = (2 / points.size) * numpy.matmul(
        points.as_array.T, (points.as_array - points.as_array.mean(axis=0))
    )
    b = numpy.matmul(
        numpy.expand_dims(norm(points.as_array, axis=1), axis=0),
        (points.as_array - points.as_array.mean(axis=0))
    ) / points.size
    c = numpy.matmul(
        inv(numpy.matmul(a.T, a)),
        numpy.matmul(a.T, b.T)
    )
    c = numpy.squeeze(c, axis=1)
    r = numpy.sqrt(numpy.power(norm(points.as_array - c, axis=1), 2).sum() / points.size)

    return Point(c[0], c[1], c[2]), r
