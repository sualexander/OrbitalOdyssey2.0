import pygame
pygame.init()


window = (1920, 1080)
black = 0, 0, 0

screen = pygame.display.set_mode(window)
pygame.display.set_caption("Orbital Odyssey")

background = pygame.image.load("ART/spacebackground.jpg")
rocket = pygame.image.load("ART/rocket.png")




class Planet:
    def __init__(self, image):
        self.image = pygame.image.load(image)


earth = Planet("ART/earth.png")

def main():
    running = True

    screen.blit(background, (0,0))

    screen.blit(rocket,(0,500))
    screen.blit(earth.image, (1000,500))

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()


