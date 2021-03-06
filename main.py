import json
import copy
import pygame.mouse
from objects import*
pygame.init()
pygame.font.init()

window = (1280, 720)
screen = pygame.display.set_mode(window)
pygame.display.set_caption("Orbital Odyssey")

FPS = 30
GRAV_CONST = 5
VEL = 5

FONT = pygame.font.SysFont("helveticaneue", 30)
UI_SIZE = [100,100]
num_levels = 6
count = 0
def update_window(objects):
    global count
    for object in objects:
        if isinstance(object, Player):
            if count >= 3:
                count = 0
            screen.blit(object.animation[int(count)], object.location)
            count += 0.1
        else:
            screen.blit(object.image, object.location)
            if isinstance(object, Portal):
                screen.blit(object.image2, object.location2)
    pygame.display.flip()

def update_gravity(rocket, actors):
    force_x = 0
    force_y = 0
    for actor in actors:
        if actor.has_gravity:
            y = actor.get_center()[1] - rocket.get_center()[1]
            x = actor.get_center()[0] - rocket.get_center()[0]
            distance_squared = (x ** 2) + (y ** 2)
            gravity = GRAV_CONST / distance_squared
            force_x += gravity * x
            force_y += gravity * y
    rocket.velocity[0] += force_x
    rocket.velocity[1] += force_y

def check_collision(rocket, actors):
    global cooldown
    rocket_rect = pygame.Rect(rocket.location[0], rocket.location[1], rocket.radius[0]*2, rocket.radius[1]*2)
    for actor in actors:
        if isinstance(actor, Portal):
            if rocket_rect.colliderect(actor.rect) and not cooldown:
                rocket.location[0] = actor.rect2[0]
                rocket.location[1] = abs(rocket.location[1]-actor.rect[1]) + actor.rect2[1]
                cooldown = True
            elif rocket_rect.colliderect(actor.rect2) and not cooldown:
                rocket.location = actor.location.copy()
                cooldown = True
            elif not rocket_rect.colliderect(actor.rect) and not rocket_rect.colliderect(actor.rect2):
                cooldown = False
        if rocket_rect.colliderect(actor.rect):
            if actor.is_target:
                return 2
            elif not isinstance(actor, Portal):
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
                    return 0
                if level_select.image.get_rect(topleft=level_select.location).collidepoint(pygame.mouse.get_pos()):
                    return select_menu()
                if exit_button.image.get_rect(topleft=exit_button.location).collidepoint(pygame.mouse.get_pos()):
                    pygame.quit()
        update_window(objects)

def select_menu():
    selecting = True
    level_select_screen = Actor("ART/levelselectscreen.png", [0, 0])
    back_button = Actor("ART/backbutton.png", [610, 650])
    objects = [level_select_screen, back_button]

    buttons = []
    texts = []

    n = 0
    for i in range(4):
        for j in range(3):
            buttons.append(Actor("ART/levelbutton.png", [130 + 420*j, 180 + 100*i]))
            buttons[n].image = pygame.transform.scale(buttons[n].image, [180,40])
            text_surface = FONT.render("LEVEL " + str(n+1), False, (255,255,255))
            text = Text(text_surface, [130 + 420*j, 180 + 100*i])
            texts.append(text)
            n += 1

    objects.extend(buttons)
    objects.extend(texts)
            
    while selecting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.image.get_rect(topleft=back_button.location).collidepoint(pygame.mouse.get_pos()):
                    selecting = False
                    start_menu()
                for i in range(len(buttons)):
                    if buttons[i].image.get_rect(topleft=buttons[i].location).collidepoint(pygame.mouse.get_pos()):
                        return i

        update_window(objects)

def end_screen():
    end = Actor("ART/amogus.png", [0,0])
    you_win = Actor("ART/youwin.png", [400,200])
    end.image = pygame.transform.scale(end.image, window)
    objects = [end, you_win]
    ending = True
    while ending:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        update_window(objects)

def success():
    running = True
    success = Actor("ART/success.png", [0, 100])
    next_level_button = Actor("ART/nextlevel.png", [480, 550])
    main_menu = Actor("ART/mainmenubutton.png", [460, 640])
    objects = [success, next_level_button, main_menu]
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if next_level_button.image.get_rect(topleft=next_level_button.location).collidepoint(pygame.mouse.get_pos()):
                    return True
                elif main_menu.image.get_rect(topleft=main_menu.location).collidepoint(pygame.mouse.get_pos()):
                    return False
        update_window(objects)

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
    rocket = Player("ART/rocket.png", [0, 10], ["ART/rocket.png", "ART/rocket2.png", "ART/rocket3.png"])
    ui = Actor("ART/ui.png", [0, 600])

    originals = []
    moveables = []
    for actor in actors:
        new = copy.copy(actor)
        if new.can_move:
            new.image = pygame.transform.scale(new.image, UI_SIZE)
            moveables.append(new)
        else:
            originals.append(new)

    objects = [background] + originals + [rocket] + [ui] + moveables

    launching = False
    designing = True
    has_selected = False
    running = True
    retry = False
    next_level = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
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
                for actor in (moveables):
                    if actor.image.get_rect(topleft=actor.location).collidepoint(pygame.mouse.get_pos()) and actor.can_move:
                        actor.has_gravity = True
                        actor.image = pygame.transform.scale(actor.image, actor.original_size)
                        actor.location = (mouse_pos[0] - actor.radius[0], mouse_pos[1] - actor.radius[1])
                        actor.rect = pygame.Rect(actor.location[0], actor.location[1], actor.radius[0]*2, actor.radius[1]*2)

        if launching:
            update_gravity(rocket, originals + moveables)
            rocket.location[0] += rocket.velocity[0]
            rocket.location[1] += rocket.velocity[1]

            check = check_collision(rocket, originals + moveables)

            if check == 1:
                objects.remove(rocket)
                update_window(objects)
                running = False
                retry = failure()
            elif check == 2:
                next_level = success()
                running = False

        update_window(objects)
    if retry:
        return 0
    if not retry and not next_level:
        return 1
    else:
        return 2

def main():
    running = True
    levels = []
    for i in range(num_levels):
        levels.append("level" + str(i+1))
    while running:
        clock = pygame.time.Clock()
        clock.tick(FPS)

        # with open('levels.json') as f:
        #     levels = json.load(f)
        #
        # print(levels["level1"]["background"])
        #make_level(levels["level1"]["actors"],levels["level1"]["background"])

        level_data = {"level1": [[make_target([950, 250])], Actor("ART/spacebackground.jpg", [0, 0])],
                      "level2": [[make_target([950, 100]), make_astroids([400, 450]), make_astroids([450,-100])], Actor("ART/spacebackground.jpg", [0, 0])],
                      "level3": [[make_target([950, 300]), make_astroids([650,160]), make_redplanet([100, 610]), make_redplanet([400, 610])], Actor("ART/spacebackground.jpg", [0, 0])],
                      "level4": [[make_target([950,50]), make_astroids([300,0]), make_astroids([700, 400]), make_redplanet([100, 610]), make_redplanet([400, 610])], Actor("ART/spacebackground.jpg", [0, 0])],
                      "level5": [[make_target([950, 300]), make_portal([400,100],[800,500]), make_astroids([500,0]), make_astroids([700,400])], Actor("ART/spacebackground.jpg", [0, 0])],
                      "level6": [[make_target([200, 450]), make_astroids([100, 200]), make_astroids([110,400]), make_portal([800, 400],[500,50]), make_redplanet([100, 610]), make_redplanet([400, 610])], Actor("ART/spacebackground.jpg", [0, 0])]
                      }

        pygame.mixer.music.load("MUSIC/menu.mp3")
        pygame.mixer.music.play(-1)
        i = start_menu()

        pygame.mixer.music.load("MUSIC/level.mp3")
        pygame.mixer.music.play(-1)
        while i < (len(levels)):
            data = level_data.get(levels[i])
            next = make_level(*data)
            if next == 0:
                i -= 1
            elif next == 1:
                break
            i += 1
            if next == 2 and i == num_levels:
                end_screen()
    pygame.quit()


if __name__ == "__main__":
    main()


