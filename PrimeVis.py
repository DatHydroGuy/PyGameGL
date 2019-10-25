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


def r(n):
    if n == 1:
        return 1
    s = sin(pi / n)
    return s / (s + 1)


INCREASE = pygame.USEREVENT + 1


class Disc:
    def __init__(self, window_width, window_height, widget_num, num_widgets, radius, factors):
        self.window_width = window_width
        self.window_height = window_height
        self.angle = 0.0
        self.offset = 0
        self.id_num = widget_num
        self.radius = radius * 2
        self.size = radius * 4
        self.factors = factors
        self.num_widgets = num_widgets
        self.center_x = 0
        self.center_y = 0
        self.colour = (255, 0, 0)

    def position_widget(self, center_x, center_y, inscribed_circle_radius, angle):
        if self.num_widgets == 1:
            self.center_x = center_x
            self.center_y = center_y
            return
        self.offset = inscribed_circle_radius - self.radius   # Additional radius required to touch circle edge
        self.angle = angle + 2.0 * self.id_num * pi / self.num_widgets
        radius = round(inscribed_circle_radius + self.offset + 0.5)
        self.center_x = center_x + int(radius * sin(self.angle))
        self.center_y = center_y + int(radius * cos(self.angle))
        self.colour = self.generate_global_colour()

    def generate_global_colour(self):
        x_off = self.center_x - self.window_width / 2
        y_off = self.center_y - self.window_height / 2
        master_angle = atan2(y_off, x_off)
        master_radius = sqrt(x_off * x_off + y_off * y_off)
        hue = master_angle / (2 * pi)
        hue = hue if 0 <= hue <= 1 else hue + 1
        temp = hsv_to_rgb(hue, 0.5 + master_radius / self.window_height, 1)
        return tuple([int(t * 255) for t in temp])


class PygView(object):
    def __init__(self, width=640, height=400, fps=60):
        """Initialize pygame, window, background, font,..."""
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        pygame.init()
        pygame.display.set_caption("Press ESC to quit")
        pygame.time.set_timer(INCREASE, 1000)
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.DOUBLEBUF)
        self.background = pygame.Surface(self.screen.get_size()).convert()
        self.clock = pygame.time.Clock()
        self.fps = fps
        self.radius = min(width / 4, height / 4)

    def run(self):
        """The main loop"""
        value = 1
        factors = list(reversed(fours(value)))

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                elif event.type == INCREASE:
                    value += 1
                    factors = list(reversed(fours(value)))

            self.background.fill((0, 0, 0))
            self.clock.tick(self.fps)

            self.draw_factors(factors, self.width / 2, self.height / 2, self.radius, 0, False)

            pygame.display.flip()
            self.screen.blit(self.background, (0, 0))

        pygame.quit()

    def draw_factors(self, factors, center_x, center_y, radius, angle, adjusted):
        if not factors:
            return

        n = factors[0]
        if n == 4 and adjusted is False:
            angle -= pi / 4
            adjusted = True  # First time we hit a 4, adjust rotation, but no adjustments after that!
        new_radius = radius * r(n)
        for i in range(1, n + 1):
            disc = Disc(self.width, self.height, i, n, new_radius, factors)
            disc.position_widget(center_x, center_y, radius, angle)
            if len(factors) == 1:
                pygame.draw.circle(self.background, disc.colour, (int(disc.center_x), int(disc.center_y)),
                                   int(disc.radius))
            self.draw_factors(factors[1:], disc.center_x, disc.center_y, new_radius, disc.angle, adjusted)


if __name__ == '__main__':
    # call with width of window and fps
    PygView(1000, 1000).run()
