import pygame


class Point:
    def __init__(self, coords, color):
        super().__init__()
        self.coords = coords

        self.color = color

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.coords[0], self.coords[1]), 2)


class Points:
    def __init__(self, color, coords_generator_function):
        self.points = []
        self.color = color

        self.coords_generator = coords_generator_function

    def add_points(self, quantity, boundaries, mouse_pos, **kwargs):
        self.points.extend([
            Point(coords=self.coords_generator(boundaries, mouse_pos, **kwargs),
                  color=self.color)
            for p in range(quantity)])


class Centroid(Point):
    def __init__(self, coords, move_function, color):
        super().__init__(coords, color)

        self.move_function = move_function
        self.color = color
        self._points = []

    def draw(self, screen, **kwargs):
        for point in self._points:
            point.draw(screen)

            if kwargs.get('show_lines'):
                pygame.draw.line(screen,
                                 self.color,
                                 self.coords,
                                 point.coords,
                                 1)

        pygame.draw.rect(screen,
                         self.color,
                         (self.coords[0] - 3, self.coords[1] - 3, 6, 6),
                         3)

    def clear_points(self):
        self._points = []

    def add_point(self, p):
        p.color = self.color
        self._points.append(p)

    def move(self):
        if self._points:
            self.coords = self.move_function(self._points)
