from hspls import get_z_coordinate, fit_sphere
from utils import Points

if __name__ == '__main__':
    points = Points.load('input.txt')

    center, radius = fit_sphere(points)
    r2 = 1 - sum(
            (point.z - get_z_coordinate(center, radius, point.x, point.y)) ** 2
            for point in points.points
    ) / sum(
        (point.z - points.as_array[:, 2].mean()) ** 2
        for point in points.points
    )

    output = ('\n'
              '    Center:\n'
              '        x: {}\n'
              '        y: {}\n'
              '        z: {}\n'
              '        r: {}\n'
              '        R2: {}\n'
              '    ').format(center.x, center.y, center.z, radius, r2)
    print(output)
