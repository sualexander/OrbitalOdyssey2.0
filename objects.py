import pygame

class Actor:
    def __init__(self, image, location):
        self.image = pygame.image.load(image)
        self.location = location
        self.radius = [self.image.get_size()[0] / 2, self.image.get_size()[1] / 2]
        self.center = self.get_center()
        self.rect = pygame.Rect(self.location[0], self.location[1], self.radius[0]*2, self.radius[1]*2)

    def get_center(self):
        center = [self.radius[0] + self.location[0], self.radius[1] + self.location[1]]
        return center

class Obstacle(Actor):
    def __init__(self, image, location, is_target):
        Actor.__init__(self, image, location)
        self.is_target = is_target

class Player(Actor):
    def __init__(self, image, location):
        Actor.__init__(self, image, location)
        self.velocity = [2,0]

class Portal(Obstacle):
    def __init__(self, image, location, is_target, location2):
        Obstacle.__init__(self, image, location, is_target)
        self.image2 = pygame.image.load("ART/portal.png")
        self.location2 = location2
        self.rect2 = pygame.Rect(self.location2[0], self.location2[1], self.radius[0]*2, self.radius[1]*2)
        self.is_portal = True

def make_target(location):
    return Obstacle("ART/blueplanet.png", location, True)


def make_astroids(location):
    return Obstacle("ART/asteroids.png", location, False)


def make_redplanet(location):
    return Obstacle("ART/redplanet.png", location, False)


def make_blueplanet(location):
    return Obstacle("ART/blueplanet.png", location, False)


def make_portal(location, location2: []):
    return Portal("ART/portal.png", location, False, location2)