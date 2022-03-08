import pygame
import json
pygame.init()


window = (1920, 1080)
black = 0, 0, 0

screen = pygame.display.set_mode(window)
pygame.display.set_caption("Orbital Odyssey")


FPS = 20
GRAV_CONST = 10
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

class Obstacle(Actor):
    def __init__(self, image, location, is_target):
        Actor.__init__(self, image, location)
        self.is_target = is_target

class Player(Actor):
    def __init__(self, image, location):
        Actor.__init__(self, image, location)
        self.velocity = [2,0]

def update_gravity(rocket, actors):
    force_x = 0
    force_y = 0
    for actor in actors:
        y = actor.get_center()[1] - rocket.get_center()[1]
        x = actor.get_center()[0] - rocket.get_center()[0]
        distance_squared = (x ** 2) + (y ** 2)
        gravity = GRAV_CONST / distance_squared
        force_x += gravity * x
        force_y += gravity * y
    rocket.velocity[0] += force_x
    rocket.velocity[1] += force_y

def update_window(objects):
    for object in objects:
        screen.blit(object.image, object.location)
    pygame.display.flip()

def check_collision(rocket, actors):
    rocket_rect = pygame.Rect(rocket.location[0], rocket.location[1], rocket.radius[0]*2, rocket.radius[1]*2)
    for actor in actors:
        actor_rect = pygame.Rect(actor.location[0], actor.location[1], actor.radius[0]*2, actor.radius[1]*2)
        if rocket_rect.colliderect(actor_rect):
            if actor.is_target:
                return 2
            else:
                return 1
    return 0

def make_earth(location):
    return Obstacle("ART/earth.png", location, False)

def make_target(location):
    return Obstacle("ART/earth.png", location, True)

def start_menu():
    start_screen = Actor("ART/startmenu.png", [0, 0])
    start_button = Actor("ART/startbutton.png", [400,600])
    objects = [start_screen, start_button]
    starting = True
    while starting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.image.get_rect(topleft=start_button.location).collidepoint(pygame.mouse.get_pos()):
                    starting = False
        update_window(objects)

def make_level(actors, background):
    rocket = Player("ART/rocket.png", [0, 0])
    objects = [background] + actors + [rocket]

    launching = False
    designing = True
    has_selected = False
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                click_pos = pygame.mouse.get_pos()
                has_selected = True
            elif event.type == pygame.MOUSEBUTTONUP:
                has_selected = False
            if event.type == pygame.MOUSEMOTION and designing:
                mouse_pos = pygame.mouse.get_pos()

        if designing:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                rocket.location[1] -= VEL
            elif keys[pygame.K_s]:
                rocket.location[1] += VEL
            if keys[pygame.K_SPACE]:
                designing = False
                launching = True

            if has_selected:
                for actor in actors:
                    if actor.image.get_rect(topleft=actor.location).collidepoint(click_pos):
                        selected = actor
                        selected.location = (mouse_pos[0] - selected.radius[0], mouse_pos[1] - selected.radius[1])

        if launching:
            update_gravity(rocket, actors)
            rocket.location[0] += rocket.velocity[0]
            rocket.location[1] += rocket.velocity[1]

            check = check_collision(rocket, actors)

            if check != 0:
                launching = False
                if check == 1:
                    objects.remove(rocket)
                elif check == 2:
                    print("SUCCESS!")
                    running = False

        update_window(objects)

def main():
    running = True
    while running:
        #speed of while loop
        clock = pygame.time.Clock()
        clock.tick(FPS)

        with open('levels.json') as f:
            levels = json.load(f)

        print(levels["level1"])

        #start_menu()

        make_level(levels[0])
        #level([make_target([400,0]), make_earth([1000, 500])], Actor("ART/spacebackground.jpg", [0, 0]))

    pygame.quit()

if __name__ == "__main__":
    main()


