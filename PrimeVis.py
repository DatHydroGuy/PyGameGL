import os
import pygame
from math import sin, cos, pi, atan2, sqrt
from colorsys import hsv_to_rgb


def prime_factors(n):
    i = 2
    factors = []
    while i * i <= n:
        if n % i:
            i += 1
        else:
            n //= i
            factors.append(i)
    if n > 1:
        factors.append(n)
    return factors


def fours(n):
    if n == 1:
        return[1]

    factors = []
    while n % 4 == 0:
        factors.append(4)
        n //= 4

    return factors + prime_factors(n)


def inscribed_radius(n):
    if n == 1:
        return 1
    s = sin(pi / n)
    return s / (s + 1)


INCREASE = pygame.USEREVENT + 1
RECIP_TWO_PI = 1.0 / (2.0 * pi)


class Disc:
    def __init__(self, window_width, window_height, widget_num, num_widgets, radius, factors):
        self.window_width = window_width
        self.window_height = window_height
        self.angle = 0.0
        self.offset = 0
        self.id_num = widget_num
        self.radius = radius * 2
        self.abs_radius = 0
        self.size = radius * 4
        self.factors = factors
        self.num_widgets = num_widgets
        self.x = 0
        self.y = 0
        self.colour = (255, 0, 0)

    def position_widget(self, center_x, center_y, inscribed_circle_radius, angle):
        if self.num_widgets == 1:
            self.x = center_x
            self.y = center_y
        else:
            self.offset = inscribed_circle_radius - self.radius   # Additional radius required to touch circle edge
            self.angle = angle + 2.0 * self.id_num * pi / self.num_widgets
            radius = round(inscribed_circle_radius + self.offset + 0.5)
            self.x = center_x + int(radius * sin(self.angle))
            self.y = center_y + int(radius * cos(self.angle))
            self.colour = PygView.pixel_colours[int(self.y)][int(self.x)]
        return self.x, self.y, self.radius, self.colour


class PygView(object):
    pixel_colours = list()

    def __init__(self, width=640, height=400, fps=60, update=1000.0):
        """Initialize pygame, window, background, font,..."""
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.DOUBLEBUF)
        self.background = pygame.Surface(self.screen.get_size()).convert()
        self.clock = pygame.time.Clock()
        self.fps = fps
        self.radius = min(width * 0.25, height * 0.25)
        self.circles = []
        self.old_circles = []
        self.generate_pixel_colours(width, height)
        pygame.time.set_timer(INCREASE, int(1000 * update))

    @classmethod
    def generate_pixel_colours(cls, width, height):
        cls.pixel_colours = list()
        for y in range(height + 10):
            cls.pixel_colours.append([])
            for x in range(width + 10):
                x_off = x - width * 0.5
                y_off = y - height * 0.5
                master_angle = atan2(y_off, x_off)
                master_radius = sqrt(x_off * x_off + y_off * y_off)
                hue = master_angle * RECIP_TWO_PI
                hue = hue if 0 <= hue <= 1 else hue + 1
                cls.pixel_colours[y].append([int(255 * t) for t in hsv_to_rgb(hue, 0.5 + master_radius / height, 1)])

    def run(self):
        """The main loop"""
        value = 1#0000
        factors = self.draw_screen(value)

        running = True
        while running:
            # if value > 10010:
            #     running = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                elif event.type == INCREASE:
                    self.old_circles = self.circles[:]
                    value += 1
                    self.circles = []
                    factors = self.draw_screen(value)

            self.clock.tick(self.fps)

            pygame.display.flip()
            self.screen.blit(self.background, (0, 0))
            pygame.display.set_caption(f'{value} = {factors}')

        pygame.quit()

    def draw_screen(self, value):
        factors = list(reversed(fours(value)))
        self.background.fill((0, 0, 0))
        self.draw_factors(factors, self.width * 0.5, self.height * 0.5, self.radius, 0, False)
        return factors

    def draw_factors(self, factors, center_x, center_y, radius, angle, adjusted):
        if not factors:
            return

        n = factors[0]
        if n == 4 and adjusted is False:
            angle -= pi * 0.25
            adjusted = True  # First time we hit a 4, adjust rotation, but no adjustments after that!
        new_radius = radius * inscribed_radius(n)
        for i in range(1, n + 1):
            disc = Disc(self.width, self.height, i, n, new_radius, factors)
            x, y, r, c = disc.position_widget(center_x, center_y, radius, angle)
            if len(factors) == 1:
                self.circles.append([x, y, r, c])
                pygame.draw.circle(self.background, disc.colour, (int(disc.x), int(disc.y)),
                                   int(disc.radius))
            self.draw_factors(factors[1:], disc.x, disc.y, new_radius, disc.angle, adjusted)


if __name__ == '__main__':
    PygView(1000, 1000, 60, 1).run()
