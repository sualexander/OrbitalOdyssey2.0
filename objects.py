import pygame

class Actor:
    def __init__(self, image, location):
        self.image = pygame.image.load(image)
        self.location = location
        self.radius = [self.image.get_size()[0] / 2, self.image.get_size()[1] / 2]
        self.center = self.get_center()
        self.rect = pygame.Rect(self.location[0]+5, self.location[1]+5, (self.radius[0]-10)*2, (self.radius[1]-10)*2)

    def get_center(self):
        center = [self.radius[0] + self.location[0], self.radius[1] + self.location[1]]
        return center

class Obstacle(Actor):
    def __init__(self, image, location, is_target, has_gravity, can_move):
        Actor.__init__(self, image, location)
        self.is_target = is_target
        self.has_gravity = has_gravity
        self.can_move = can_move
        self.original_size = self.image.get_size()

class Player(Actor):
    def __init__(self, image, location, frames):
        Actor.__init__(self, image, location)
        self.frames = frames
        self.animation = self.load_images()
        self.velocity = [2,0]

    def load_images(self):
        animation = []
        for frame in self.frames:
            animation.append(pygame.image.load(frame))
        return animation

class Portal(Obstacle):
    def __init__(self, image, location, is_target, has_gravity, can_move, location2):
        Obstacle.__init__(self, image, location, is_target, has_gravity, can_move)
        self.image2 = pygame.image.load("ART/portal.png")
        self.location2 = location2
        self.rect2 = pygame.Rect(self.location2[0], self.location2[1], self.radius[0]*2, self.radius[1]*2)
        self.is_portal = True

class Text:
    def __init__(self, surface, location):
        self.image = surface
        self.location = location

def make_target(location):
    return Obstacle("ART/blueplanet.png", location, True, True, False)


def make_astroids(location):
    return Obstacle("ART/asteroids.png", location, False, False, False)


def make_redplanet(location):
    return Obstacle("ART/redplanet.png", location, False, False, True)


def make_blueplanet(location):
    return Obstacle("ART/blueplanet.png", location, False, False, True)


def make_portal(location, location2: []):
    return Portal("ART/portal.png", location, False, False, False, location2)
