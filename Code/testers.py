import pygame
import sys
import random
from random import choice


pygame.init()


# colours


purple = (183,33,255)
blue = (72,55,255)
white = (255,255,255)


# Screens and displays

screen_width = 1000
screen_height = 800

screen = pygame.display.set_mode((screen_width,screen_height)) # displays our screen
pygame.display.set_caption("Bat Rush") # Creates a title for game

clock = pygame.time.Clock() #Makes a clock

# fonts initialisation

title_font = pygame.font.Font("Bat Rush/Graphics/Aquire-BW0ox.otf",100)
small_font = pygame.font.Font("Bat Rush/Graphics/Aquire-BW0ox.otf",40)
smaller_font = pygame.font.Font("Bat Rush/Graphics/Aquire-BW0ox.otf",20)


# graphics initialisation

cog_surf = pygame.transform.scale(pygame.image.load("Bat Rush/Graphics/cog.png").convert_alpha(), (80,80))
cog_rect = cog_surf.get_rect(center = (50,50))

bg_surf = pygame.transform.scale(pygame.image.load("Bat Rush/Graphics/BG.jpeg").convert_alpha(), (screen_width,screen_height))
bg_surf2 = pygame.transform.scale(pygame.image.load("Bat Rush/Graphics/BG2.png").convert_alpha(), (screen_width,screen_height))

bat_imgs = [pygame.transform.scale2x(pygame.image.load("bat Rush/Graphics/bat1.png")),pygame.transform.scale2x(pygame.image.load("Bat Rush/Graphics/bat2.png"))]

ground_img = pygame.image.load("Bat Rush/Graphics/ground.png").convert_alpha()

pipe_img = pygame.transform.scale2x(pygame.image.load("Bat Rush/Graphics/pipe_green.png").convert_alpha())

loadingbox = pygame.transform.scale(pygame.image.load("Bat Rush/Graphics/loadingbox.png").convert_alpha(), (700,120))
loadingbar = pygame.image.load("Bat Rush/Graphics/loadingbar.png").convert_alpha()

back_surf = pygame.transform.scale(pygame.image.load("Bat Rush/Graphics/back3.png").convert_alpha(), (80,80))


# Classes

class Button(): # Class for creating buttons
    def __init__(self, x, y, image, text, type):
        self.x = x
        self.y = y
        self.text = text
        self.type = type
        self.angle = 0

        if self.type == "text" : # Checks whether our button is text based or image based
            self.surf = small_font.render(self.text, False, white)

        else:
            self.surf = image

        self.rect = self.surf.get_rect(center = (self.x,self.y))

    def draw(self):
        screen.blit(self.surf, self.rect)

    def hover(self):
        if self.rect.collidepoint((mouse_pos)):
            if self.type == "text":
                self.surf = small_font.render(self.text, False, blue)

            elif self.type == "cog":
                self.surf = pygame.transform.rotate(cog_surf, self.angle)
                self.rect = self.surf.get_rect(center = (self.x,self.y))
                self.angle += 3

        elif self.rect.collidepoint((mouse_pos)) == False and (self.type == "text") == True: # Checks whether the text based button is not being hovered.
            self.surf = small_font.render(self.text, False, white)

    def check_input(self):
        if self.rect.collidepoint((mouse_pos)) and mouse_pressed[0]:
            return True
        
        else:
            return False
        
    def update(self):
        self.draw()
        self.hover()
        


# Initialising our main menu buttons

play_btn = Button(screen_width/2, 300, None, "Play", "text")
ldb_btn = Button(screen_width/2, 400, None, "Leaderboard", "text")
help_btn = Button(screen_width/2, 500, None, "Help", "text")
quit_btn = Button(screen_width/2, 600, None, "Quit", "text") 


cog_btn = Button(50, 50, cog_surf, None, "cog")


def end_game(): # function to end the game
    pygame.quit()
    sys.exit()


def loading():
    width = 10
    while True:
        for event in pygame.event.get(): # Grabs all our events
            if event.type == pygame.QUIT:
                end_game()

        screen.fill("#131313")
        loading_surf = title_font.render("Loading...",False,white)
        loading_rect = loading_surf.get_rect(center = (screen_width/2,200))
        loadingbox_rect = loadingbox.get_rect(center = (500,400))
        screen.blit(loading_surf, loading_rect)
        screen.blit(loadingbox, loadingbox_rect)

        loadingbar_surf = pygame.transform.scale(loadingbar, (width, 160))
        loadingbar_rect = loadingbar_surf.get_rect(topleft = (155,320))
        screen.blit(loadingbar_surf, loadingbar_rect)

        if width > 680:
            start()
        width += 3

        pygame.display.update()
        clock.tick(60)


def start(): # function for start screen
    while True:
        for event in pygame.event.get(): # Grabs all our events
            if event.type == pygame.QUIT:
                end_game()
            if event.type == pygame.MOUSEBUTTONUP:
                if cog_btn.check_input():
                    settings()

        screen.fill("black")
        screen.blit(bg_surf, (0,0))

        start_surf = title_font.render("Start", False, purple)
        start_rect = start_surf.get_rect(center = (screen_width/2, 200))


        global mouse_pos
        mouse_pos = pygame.mouse.get_pos()
        global mouse_pressed
        mouse_pressed = pygame.mouse.get_pressed()

        cog_btn.update()

        screen.blit(start_surf, start_rect)
    
        pygame.display.update()
        clock.tick(60)

def sign_up(): # function for the sign up screen
    timer = 0
    while True:
        for event in pygame.event.get(): # Grabs all our events
            if event.type == pygame.QUIT:
                end_game()
            if event.type == pygame.MOUSEBUTTONUP:
                if cog_btn.check_input():
                    settings()

        screen.fill("black")
        screen.blit(bg_surf, (0,0))

        sign_surf = title_font.render("Sign up", False, purple)
        sign_rect = sign_surf.get_rect(center = (screen_width/2, 200))


        global mouse_pos
        mouse_pos = pygame.mouse.get_pos()
        global mouse_pressed
        mouse_pressed = pygame.mouse.get_pressed()

        cog_btn.update()

        screen.blit(sign_surf, sign_rect)

        if timer>1000:
            loading()

        timer += 10
    
        pygame.display.update()
        clock.tick(60)


def LDB(): # function for the leaderboard screen
    while True:
        for event in pygame.event.get(): # Grabs all our events
            if event.type == pygame.QUIT:
                end_game()
            if event.type == pygame.MOUSEBUTTONUP:
                if cog_btn.check_input():
                    settings()

        screen.fill("black")
        screen.blit(bg_surf, (0,0))

        LDB_surf = title_font.render("Leaderboard", False, purple)
        LDb_rect = LDB_surf.get_rect(center = (screen_width/2, 200))


        global mouse_pos
        mouse_pos = pygame.mouse.get_pos()
        global mouse_pressed
        mouse_pressed = pygame.mouse.get_pressed()

        cog_btn.update()

        screen.blit(LDB_surf, LDb_rect)
    
        pygame.display.update()
        clock.tick(60)


def help(): # function for the help screen
    while True:
        for event in pygame.event.get(): # Grabs all our events
            if event.type == pygame.QUIT:
                end_game()
            if event.type == pygame.MOUSEBUTTONUP:
                if cog_btn.check_input():
                    settings()

        screen.fill("black")
        screen.blit(bg_surf, (0,0))

        help_surf = title_font.render("Help", False, purple)
        help_rect = help_surf.get_rect(center = (screen_width/2, 200))


        global mouse_pos
        mouse_pos = pygame.mouse.get_pos()
        global mouse_pressed
        mouse_pressed = pygame.mouse.get_pressed()

        cog_btn.update()

        screen.blit(help_surf, help_rect)
    
        pygame.display.update()
        clock.tick(60)


def settings(): # function for the settings screen
    while True:
        for event in pygame.event.get(): # Grabs all our events
            if event.type == pygame.QUIT:
                end_game()
            if event.type == pygame.MOUSEBUTTONUP:
                if cog_btn.check_input():
                    settings()

        screen.fill("black")
        screen.blit(bg_surf, (0,0))

        settings_surf = title_font.render("Settings", False, purple)
        settings_rect = settings_surf.get_rect(center = (screen_width/2, 200))


        global mouse_pos
        mouse_pos = pygame.mouse.get_pos()
        global mouse_pressed
        mouse_pressed = pygame.mouse.get_pressed()

        cog_btn.update()

        screen.blit(settings_surf, settings_rect)
    
        pygame.display.update()
        clock.tick(60)


def main_menu(): # function for main menu
    animation_index = 0
    angle = 0
    while True: 
        for event in pygame.event.get(): # Grabs all our events
            if event.type == pygame.QUIT:
                end_game()
            if event.type == pygame.MOUSEBUTTONUP: # Checks mouse click
                if play_btn.check_input():
                    sign_up()
                if ldb_btn.check_input():
                    LDB()
                if quit_btn.check_input():
                    run = False
                    end_game()
                if cog_btn.check_input():
                    settings()
                if help_btn.check_input():
                    help()
                    

        # Mouse positions  

        global mouse_pos
        mouse_pos = pygame.mouse.get_pos()
        global mouse_pressed
        mouse_pressed = pygame.mouse.get_pressed()

        title_surf = title_font.render("Bat Rush", False, purple)
        title_rect = title_surf.get_rect(center = (screen_width/2, 200))

        screen.blit(bg_surf,(0,0)) # Background
        screen.blit(title_surf, title_rect) # Title


        play_btn.update()
        ldb_btn.update()
        quit_btn.update()
        cog_btn.update()
        help_btn.update()

        if animation_index == 1.3:
            animation_index = 0

        
        animation_index += 0.1
        print(int(animation_index))
        surf = bat_imgs[int(animation_index)]

        rect = surf.get_rect(center = (100,400))
        screen.blit(surf, rect)


        

        pygame.display.update() # Updates the screen
        clock.tick(60) # 60 fps


main_menu()