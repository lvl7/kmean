import random


def uniform(boundaries, mouse_pos, **kwargs):
    return (random.randint(boundaries[0], boundaries[1]),
            random.randint(boundaries[1], boundaries[2]))


def triangular(bounardies, mouse_pos, **kwargs):
    return (round(random.triangular(bounardies[0], bounardies[1], mouse_pos[0])),
            round(random.triangular(bounardies[2], bounardies[3], mouse_pos[1])))


def normal(boundaries, mouse_pos, modifier=40, **kwargs):
    if modifier is None:
        modifier = 40

    def coord(lowest, highest, center):
        while True:
            coord = round(random.normalvariate(center, modifier))
            if lowest <= coord <= highest:
                return coord

    return (coord(boundaries[0], boundaries[1], mouse_pos[0]),
            coord(boundaries[2], boundaries[3], mouse_pos[1]))
