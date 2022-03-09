import json
from objects import*
pygame.init()

window = (1280, 720)
screen = pygame.display.set_mode(window)
pygame.display.set_caption("Orbital Odyssey")

FPS = 30
GRAV_CONST = 5
VEL = 5

def update_window(objects):
    for object in objects:
        screen.blit(object.image, object.location)
    pygame.display.flip()

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

def check_collision(rocket, actors):
    rocket_rect = pygame.Rect(rocket.location[0], rocket.location[1], rocket.radius[0]*2, rocket.radius[1]*2)
    for actor in actors:
        actor_rect = pygame.Rect(actor.location[0], actor.location[1], actor.radius[0]*2, actor.radius[1]*2)
        if rocket_rect.colliderect(actor_rect):
            if actor.is_target:
                return 2
            else:
                return 1
        elif rocket.location[0] > 1400 or rocket.location[0] < -100 or rocket.location[1] > 800 or rocket.location[1] < -100:
            return 1
    return 0

def start_menu():
    start_screen = Actor("ART/startmenu.png", [0, 0])
    start_button = Actor("ART/startbutton.png", [110,540])
    level_select = Actor("ART/levelselect.png", [220, 600])
    exit_button = Actor("ART/exitgame.png", [330,660])
    objects = [start_screen, start_button, level_select, exit_button]
    starting = True
    while starting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.image.get_rect(topleft=start_button.location).collidepoint(pygame.mouse.get_pos()):
                    starting = False
                if level_select.image.get_rect(topleft=level_select.location).collidepoint(pygame.mouse.get_pos()):
                    starting = False
                    select_menu()
                if exit_button.image.get_rect(topleft=exit_button.location).collidepoint(pygame.mouse.get_pos()):
                    pygame.quit()
        update_window(objects)

def select_menu():
    selecting = True
    level_select_screen = Actor("ART/levelselectscreen.png", [0, 0])
    back_button = Actor("ART/backbutton.png", [610, 650])
    objects = [level_select_screen, back_button]
    while selecting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.image.get_rect(topleft=back_button.location).collidepoint(pygame.mouse.get_pos()):
                    selecting = False
                    start_menu()
        update_window(objects)

def success():
    running = True
    success = Actor("ART/success.png", [0, 100])
    next_level_button = Actor("ART/nextlevel.png", [400, 600])

def failure():
    running = True
    failure = Actor("ART/failure.png", [0, 100])
    retry = Actor("ART/retry.png", [480, 550])
    main_menu = Actor("ART/mainmenubutton.png", [460, 640])
    objects = [failure, retry, main_menu]
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if retry.image.get_rect(topleft=retry.location).collidepoint(pygame.mouse.get_pos()):
                    return True
                elif main_menu.image.get_rect(topleft=main_menu.location).collidepoint(pygame.mouse.get_pos()):
                    return False
        update_window(objects)

def make_level(actors, background):
    rocket = Player("ART/rocket.png", [0, 10])
    objects = [background] + actors + [rocket]

    launching = False
    designing = True
    has_selected = False
    running = True
    retry = False
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

            if check == 1:
                objects.remove(rocket)
                update_window(objects)
                running = False
                retry = failure()
            elif check == 2:
                print("SUCCESS!")
                running = False

        update_window(objects)
    if retry:
        make_level(actors, background)

def main():
    running = True
    levels = []
    while running:
        #speed of while loop
        clock = pygame.time.Clock()
        clock.tick(FPS)

        start_menu()

        # with open('levels.json') as f:
        #     levels = json.load(f)
        #
        # print(levels["level1"]["background"])
        #make_level(levels["level1"]["actors"],levels["level1"]["background"])

        level1 = [make_target([950, 300]), make_astroids([600,100]), make_redplanet([400,500])], Actor("ART/spacebackground.jpg", [0, 0])
        make_level(*level1)

    pygame.quit()

if __name__ == "__main__":
    main()


