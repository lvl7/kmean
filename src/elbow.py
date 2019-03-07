from functools import reduce
from typing import TYPE_CHECKING

from matplotlib import pyplot

if TYPE_CHECKING:
    from typing import List
    from src.points import Centroid


class MeanVisualizer:
    def __init__(self, clusters):
        self.clusters = clusters  # type: List[Centroid]
        self.k_errors = {}

        self.figure = 123

    def show_means(self, distance_function):
        sum_error = reduce(lambda error, cluster: error + cluster.calculate_error(distance_function),
                           self.clusters,
                           0)

        self.k_errors[len(self.clusters)] = sum_error

        fig = pyplot.figure(self.figure)
        pyplot.clf()
        pyplot.plot(self.k_errors.keys(), self.k_errors.values(), "-x")
        pyplot.draw()
        pyplot.pause(0.001)

    def clean_errors(self):
        self.k_errors = {}
