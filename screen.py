import pygame
import math
import random


SCREEN_DIM = (800, 600)


def draw_points(points, display):
    for p in points:
        p.draw_self(display)

def draw_help(curve_number):
    gameDisplay.fill((50, 50, 50))
    font1 = pygame.font.SysFont("courier", 24)
    font2 = pygame.font.SysFont("serif", 24)
    data = []
    data.append(["F1", "Show Help"])
    data.append(["D", "Delete Point"])
    data.append(["R", "Restart"])
    data.append(["P", "Pause/Play"])
    data.append(["Num+", "More points"])
    data.append(["Num-", "Less points"])
    data.append(["[", "Previous curve"])
    data.append(["]", "Next curve"])
    data.append(["", ""])
    data.append([str(steps), "Current support points"])
    data.append([str(curve_number), "Selected curve"])

    pygame.draw.lines(gameDisplay, (255, 50, 50, 255), True, [
        (0, 0), (800, 0), (800, 600), (0, 600)], 5)
    for i, text in enumerate(data):
        gameDisplay.blit(font1.render(
            text[0], True, (128, 128, 255)), (100, 100 + 30 * i))
        gameDisplay.blit(font2.render(
            text[1], True, (128, 128, 255)), (200, 100 + 30 * i))

# =======================================================================================
# Class represents a vector in two dimensional space
# =======================================================================================
class Vec2d:
    def __init__(self, x, y):
        self.x = math.ceil(x)
        self.y = math.ceil(y)

    def __sub__(self, vec):
        """"return difference of two vectors"""
        return Vec2d(self.x - vec.x, self.y - vec.y)


    def __add__(self, vec):
        """return sum of two vectors"""
        return Vec2d(self.x + vec.x, self.y + vec.y)


    def __len__(self):
        """return length of the vector"""
        x = self.x
        y = self.y
        return math.sqrt(x * x + y * y)


    def __mul__(self, k):
        """return multiplication of the vector and the number"""
        return Vec2d(self.x * k, self.y * k)

    def __str__(self):
        return str((self.x, self.y))


    def int_pair(self):
        """return the coordinates of the vector"""
        return (self.x, self. y)

    def draw_self(self, gameDisplay, width=3, color=(255, 255, 255)):
        pygame.draw.circle(gameDisplay, color,
                            (self.x, self.y) , width)


# =======================================================================================
# Class represents a closed curve in two dimensional space
# =======================================================================================
class Polyline:
    def __init__(self, points):
        self.points = points
        self.speeds = self._add_speeds()

    def _add_speeds(self):
        speeds = []
        for _ in range(len(self.points)):
            speeds.append(Vec2d(random.random() * 2, random.random() * 2))
        return speeds

    def add_point(self, point):
        self.points.append(point)
        self.speeds.append(Vec2d(random.random() * 2, random.random() * 2))

    def set_points(self, points, speeds, SCREEN_DIM):
        """recalculate coorditanes of supporting points"""
        for p in range(len(points)):
            points[p] = points[p] + speeds[p]
            if points[p].x > SCREEN_DIM[0] or points[p].x < 0:
                speeds[p] = Vec2d(- speeds[p].x, speeds[p].y)
            if points[p].y > SCREEN_DIM[1] or points[p].y < 0:
                speeds[p] = Vec2d(speeds[p].x, -speeds[p].y)

    def draw_points(self, points, gameDisplay, width=3, color=(255, 255, 255)):
        """draw closed curve"""
        for p_n in range(-1, len(points) - 1):
            pygame.draw.line(gameDisplay, color,
                            (int(points[p_n].x), int(points[p_n].y)),
                            (int(points[p_n + 1].x), int(points[p_n + 1].y)), width)


#import pygame
#from polyline import Polyline


# =======================================================================================
# Class represents a knot in two dimensional space
# =======================================================================================
class Knot(Polyline):
    def __init__(self, points, steps):
        super().__init__(points)
        self.steps = steps
        self.knot = self.get_knot(points, steps)

    def set_points(self, points, speeds, SCREEN_DIM):
        super().set_points(points, speeds, SCREEN_DIM)
        self.knot = self.get_knot(self.points, self.steps)

    def add_point(self):
        pass

    def get_point(self, points, alpha, deg=None):
        if deg is None:
            deg = len(points) - 1
        if deg == 0:
            return points[0]
        return (points[deg] * alpha) + (self.get_point(points, alpha, deg - 1) * (1 - alpha))

    def get_points(self, base_points, count):
        alpha = 1 / count
        res = []
        for i in range(count):
            res.append(self.get_point(base_points, i * alpha))
        return res

    def get_knot(self, points, count):
        if len(points) < 3:
            return []
        res = []
        for i in range(-2, len(points) - 2):
            ptn = []
            ptn.append((points[i] + points[i + 1]) * 0.5)
            ptn.append(points[i + 1])
            ptn.append((points[i + 1] + points[i + 2]) * 0.5)

            res.extend(self.get_points(ptn, count))
        return res


if __name__ == "__main__":
    pygame.init()
    gameDisplay = pygame.display.set_mode(SCREEN_DIM)
    pygame.display.set_caption("MyScreenSaver")

    steps = 35
    working = True
    curves = [Knot([], steps)]
    curves_points = [[]]
    curves_speeds = [[]]
    curve_ptn = 0
    show_help = False
    pause = True

    hue = 0
    color = pygame.Color(0)

    while working:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                working = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    working = False
                if event.key == pygame.K_r:
                    curves = [Knot([], steps)]
                    curves_points = [[]]
                    curves_speeds = [[]]
                    curve_ptn = 0
                if event.key == pygame.K_p:
                    pause = not pause
                if event.key == pygame.K_KP_PLUS:
                    steps += 1
                if event.key == pygame.K_F1:
                    show_help = not show_help
                if event.key == pygame.K_KP_MINUS:
                    steps -= 1 if steps > 1 else 0
                if event.key == pygame.K_LEFTBRACKET:
                    if curve_ptn - 1 >= 0:
                        curve_ptn -= 1
                if event.key == pygame.K_RIGHTBRACKET:
                    curve_ptn += 1
                    try:
                        a = curves[curve_ptn]
                    except IndexError:
                        curves.append(Knot([], steps))
                        curves_points.append([])
                        curves_speeds.append([])

                if event.key == pygame.K_d:
                    try:
                        del curves_points[curve_ptn][0]
                        del curves_speeds[curve_ptn][0]
                    except IndexError:
                        pass

            if event.type == pygame.MOUSEBUTTONDOWN:
                curves_points[curve_ptn].append(Vec2d(event.pos[0], event.pos[1]))
                curves_speeds[curve_ptn].append(Vec2d(random.random() * 2, random.random() * 2))

        gameDisplay.fill((0, 0, 0))
        hue = (hue + 1) % 360
        color.hsla = (hue, 100, 50, 100)
        for i in range(len(curves)):
            draw_points(curves_points[i], gameDisplay)
            curves[i] = Knot(curves_points[i], steps)
            curves[i].draw_points(curves[i].knot, gameDisplay, color=color)

        if not pause:
            for i in range(len(curves)):
                curves[i].set_points(curves_points[i], curves_speeds[i], SCREEN_DIM)
        if show_help:
            draw_help(curve_ptn)

        pygame.display.flip()

    pygame.display.quit()
    pygame.quit()
    exit(0)
