import random
from itertools import permutations

import pygame
import pygame.freetype

from src import coords_generators, averagers, distance
from src.points import Points, Centroid, Point

random.seed(1)

EVENT_ITERATE = pygame.USEREVENT + 1

DISPLAY = (800, 600)
BACKGROUND = (0, 0, 0)
UNASSIGNED_POINTS_COLOR = (255, 255, 255)


def color_generator():
    for color in sorted(permutations((32, 255, 192, 64), 3), key=lambda c: sum(c)):
        yield color

    while True:
        yield (random.randint(64, 255),
               random.randint(64, 255),
               random.randint(64, 255))


def handle_events(world, events):
    for event in events:
        if event.type == pygame.QUIT:
            return False
        elif event.type == pygame.KEYDOWN:
            ukey = event.unicode
            try:
                num = int(ukey)
                world.add_number_modifier(num)
            except ValueError:
                if ukey == 'r':
                    world.add_points(pygame.mouse.get_pos())
                elif ukey == 'p':
                    world.add_point(pygame.mouse.get_pos())
                elif ukey == 'c':
                    world.add_centroid(pygame.mouse.get_pos())
                elif ukey == 's':
                    world.siblings()
                elif ukey == 'm':
                    world.move_centroids()
                elif ukey == 'n':
                    world.new()
                elif ukey == 'i':
                    world.iterate()
                elif ukey == 'l':
                    world.toggle_lines()
                elif event.key == pygame.K_ESCAPE:
                    world.cancel()
        elif event.type == EVENT_ITERATE:
            world.iterate()

    return True


class World:
    def __init__(self,
                 distance_function=distance.euclidean,
                 centorid_move_function=averagers.mean,
                 points_random_function=coords_generators.normal):
        self.points = None
        self.centroids = []

        self.distance_function = distance_function
        self.centroid_move_function = centorid_move_function
        self.points_random_function = points_random_function

        self.color_picker = color_generator()
        self.show_lines = False

        self.number_modifier = None

        self.new()

    def add_points(self, mouse_pos):
        world.points.add_points(100, (0, DISPLAY[0], 0, DISPLAY[1]), mouse_pos,
                                modifier=self.number_modifier)

    def add_point(self, coords):
        world.points.points.append(Point(coords, UNASSIGNED_POINTS_COLOR))

    def add_number_modifier(self, number):
        if self.number_modifier is None:
            self.number_modifier = number
        else:
            self.number_modifier = self.number_modifier * 10 + number

    def add_centroid(self, coords):
        self.centroids.append(
            Centroid(coords=coords,
                     move_function=self.centroid_move_function,
                     color=next(self.color_picker))
        )

    def new(self):
        self.points = Points(color=UNASSIGNED_POINTS_COLOR,
                             coords_generator_function=self.points_random_function)
        self.centroids = []

    def cancel(self):
        self.number_modifier = None
        pygame.time.set_timer(EVENT_ITERATE, 0)

    def iterate(self):
        self.siblings()
        self.move_centroids()

        if self.number_modifier:
            pygame.time.set_timer(EVENT_ITERATE, self.number_modifier)

    def siblings(self):
        if not self.centroids:
            return

        for centroid in self.centroids:
            centroid.clear_points()

        for point in self.points.points:
            centroid_iter = iter(self.centroids)
            closest_centroid = next(centroid_iter)  # type: Centroid
            closest_distance = self.distance_function(point, closest_centroid)

            for centroid in centroid_iter:
                distance = self.distance_function(point, centroid)
                if distance < closest_distance:
                    closest_distance = distance
                    closest_centroid = centroid

            closest_centroid.add_point(point)

    def move_centroids(self):
        for centroid in self.centroids:
            centroid.move()

    def toggle_lines(self):
        self.show_lines = not self.show_lines

    def draw(self, screen, font):
        for point in self.points.points:
            point.draw(screen)

        for centroid in self.centroids:  # type: Centroid
            centroid.draw(screen, show_lines=self.show_lines)

        if self.number_modifier is not None:
            font.render_to(screen, (2, 2), str(self.number_modifier), (255, 255, 255))


def draw_world(screen, world, font):
    screen.fill(BACKGROUND)
    world.draw(screen, font)
    pygame.display.flip()


if __name__ == '__main__':
    # TODO move pygame related to class - remove globals
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode(DISPLAY)
    clock = pygame.time.Clock()

    font = pygame.freetype.Font('../OpenSans-Light.ttf', 15)

    world = World(
    )

    while handle_events(
            world=world,
            events=pygame.event.get()):
        draw_world(screen, world, font)

        clock.tick(30)
