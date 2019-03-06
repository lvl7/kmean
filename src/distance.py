import math


def euclidean(p1, p2):
    return math.sqrt(sum(
        map(lambda consecutive_points_coord: (consecutive_points_coord[0] - consecutive_points_coord[1]) ** 2,
            zip(p1.coords, p2.coords)
            )))
