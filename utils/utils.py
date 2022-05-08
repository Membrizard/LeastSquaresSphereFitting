import attr
import numpy
import typing


@attr.s(auto_attribs=True)
class Point:
    x: float = attr.ib(converter=float)
    y: float = attr.ib(converter=float)
    z: float = attr.ib(converter=float)


@attr.s(auto_attribs=True)
class Points:
    points: typing.List[Point]

    @classmethod
    def load(cls, path: str) -> 'Points':
        with open(path, 'r') as handle:
            points = []
            for line in handle:
                x, y, z = line.split(',')
                points.append(
                    Point(x, y, z)
                )
        return cls(points)

    @property
    def as_array(self) -> numpy.ndarray:
        return numpy.array([
            [point.x, point.y, point.z] for point in self.points
        ]).astype(numpy.float16)

    @property
    def size(self) -> int:
        return len(self.points)
