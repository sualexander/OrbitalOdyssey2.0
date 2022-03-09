import pygame

class Actor:
    def __init__(self, image, location):
        self.image = pygame.image.load(image)
        self.location = location
        self.radius = [self.image.get_size()[0] / 2, self.image.get_size()[1] / 2]
        self.center = self.get_center()

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

def make_target(location):
    return Obstacle("ART/blueplanet.png", location, True)

def make_astroids(location):
    return Obstacle("ART/asteroids.png", location, False)

def make_redplanet(location):
    return Obstacle("ART/redplanet.png", location, False)

def make_blueplanet(location):
    return Obstacle("ART/blueplanet.png", location, False)