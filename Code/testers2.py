import pygame
import sys

pygame.init()

clock = pygame.time.Clock()

screen = pygame.display.set_mode([800,800])
base_font = pygame.font.Font(None,20)
text = ''

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.type == pygame.K_BACKSPACE:
                text = text[:-1]
            else:
                text += event.unicode


        
    screen.fill((0,0,0))
    surf = base_font.render(text, False, (255,255,255))
    screen.blit(surf, (0,0))

    pygame.display.update()
    clock.tick(60)