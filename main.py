import math

import pygame
pygame.init()


window = (1920, 1080)
black = 0, 0, 0

screen = pygame.display.set_mode(window)
pygame.display.set_caption("Orbital Odyssey")


FPS = 20
GRAV_CONST = 1
VEL = 10

class Actor:
    def __init__(self, image, location):
        self.image = pygame.image.load(image)
        self.location = location
        self.radius = [self.image.get_size()[0] / 2, self.image.get_size()[1] / 2]
        self.center = self.get_center()

    def get_center(self):
        center = [self.radius[0] + self.location[0], self.radius[1] + self.location[1]]
        return center

class Planet(Actor):
    pass

class Player(Actor):
    def __init__(self, image, location):
        Actor.__init__(self, image, location)
        self.velocity = [1,0]



def update_gravity(rocket, actors):
    force_x = 0
    force_y = 0
    for actor in actors:
        y = actor.get_center()[1] - rocket.get_center()[1]
        x = actor.get_center()[0] - rocket.get_center()[0]
        distance_squared = (x ** 2) + (y ** 2)
        gravity = GRAV_CONST / distance_squared
        force_x = gravity * x
        force_y = gravity * y
    rocket.velocity[0] += force_x
    rocket.velocity[1] += force_y
    print(force_x,force_y)

def update_window(objects):
    for object in objects:
        screen.blit(object.image, object.location)

        screen.fill((200, 200, 200), (object.center[0], object.center[1], 20, 20))
    pygame.display.flip()

def check_collision(rocket, actors):
    rocket_rect = pygame.Rect(rocket.location[0], rocket.location[1], rocket.radius[0]*2, rocket.radius[1]*2)
    for actor in actors:
        actor_rect = pygame.Rect(actor.location[0], actor.location[1], actor.radius[0]*2, actor.radius[1]*2)
        if rocket_rect.colliderect(actor_rect):
            return True

def main():
    running = True
    #speed of while loop
    clock = pygame.time.Clock()
    clock.tick(FPS)

    #init images
    background = Actor("ART/spacebackground.jpg", [0,0])
    earth = Planet("ART/earth.png", [1000,500])
    rocket = Player("ART/rocket.png", [500,0])

    actors = [earth]
    objects = [background] + actors + [rocket]

    playing = True

    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if playing:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_a]:
                rocket.velocity[0] -= VEL
            if keys[pygame.K_d]:
                rocket.velocity[0] += VEL
            if keys[pygame.K_w]:
                rocket.velocity[1] -= VEL
            if keys[pygame.K_s]:
                rocket.velocity[1] += VEL

            update_gravity(rocket, actors)

            rocket.location[0] += rocket.velocity[0]
            rocket.location[1] += rocket.velocity[1]

            if check_collision(rocket, actors):
                objects.remove(rocket)
                playing = False


        update_window(objects)


    pygame.quit()



if __name__ == "__main__":
    main()


