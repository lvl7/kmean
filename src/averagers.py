def mean(points):
    return list(map(
        lambda consecutive_points_coord: sum(consecutive_points_coord) / len(consecutive_points_coord),
        zip(*[p.coords for p in points])
    ))
