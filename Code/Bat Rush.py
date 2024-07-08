import pygame
import sys
import random
from random import choice
import sqlite3
import os
import hashlib
import time
import neat
import pickle


pygame.init()


# colours


purple = (183,33,255)
blue = (72,55,255)
white = (255,255,255)
grey = "#ccccccff"
red = "#FF2400"
green = "green"
black = "#131313"
bright_purple = "#33007b"
bright_blue = "#00CCFF"
orange = "#FFA500"
dark_blue = "#040720"



# Screens and displays

screen_width = 1000
screen_height = 800

screen = pygame.display.set_mode((screen_width,screen_height)) # displays our screen
pygame.display.set_caption("Bat Rush") # Creates a title for game

clock = pygame.time.Clock() # Initialises a clock3


acc_username = False # Account username set as default to false
logged_in = False # Logged in boolean set as default to false


# fonts initialisation

large_font = pygame.font.Font("Bat Rush/Graphics/Aquire-BW0ox.otf",80)
small_font = pygame.font.Font("Bat Rush/Graphics/Aquire-BW0ox.otf",40)
smaller_font = pygame.font.Font("Bat Rush/Graphics/Aquire-BW0ox.otf",20)
smallest_font = pygame.font.Font("Bat Rush/Graphics/Aquire-BW0ox.otf",16)
base_font = pygame.font.Font(None, 40)

# graphics initialisation

cog_surf = pygame.transform.scale(pygame.image.load("Bat Rush/Graphics/cog.png").convert_alpha(), (80,80))
cog_rect = cog_surf.get_rect(center = (50,50))

menu_bg = pygame.transform.scale(pygame.image.load("Bat Rush/Graphics/BG.jpeg").convert_alpha(), (screen_width,screen_height))
game_bg = pygame.transform.scale(pygame.image.load("Bat Rush/Graphics/BG2.png").convert_alpha(), (screen_width,screen_height))

bat_imgs = [pygame.transform.scale_by(pygame.image.load("bat Rush/Graphics/bat1.png"), 4),pygame.transform.scale_by(pygame.image.load("Bat Rush/Graphics/bat2.png"), 4)]
AI_bat_imgs = [pygame.transform.scale_by(pygame.image.load("bat Rush/Graphics/ghost-bat.png"), 4),pygame.transform.scale_by(pygame.image.load("Bat Rush/Graphics/ghost-bat2.png"), 4)]


ground_img = pygame.transform.scale(pygame.image.load("Bat Rush/Graphics/ground.png").convert_alpha(), (540,100))

pipe_img = pygame.transform.scale(pygame.image.load("Bat Rush/Graphics/pipe6.png").convert_alpha(), (100,500))

loadingbox = pygame.transform.scale(pygame.image.load("Bat Rush/Graphics/loadingbox.png").convert_alpha(), (700,120))
loadingbar = pygame.image.load("Bat Rush/Graphics/loadingbar.png").convert_alpha()

back_surf = pygame.transform.scale(pygame.image.load("Bat Rush/Graphics/back3.png").convert_alpha(), (80,80))

cross = pygame.transform.scale(pygame.image.load("Bat Rush/Graphics/cross2.png").convert_alpha(), (60,40))

tick = pygame.transform.scale(pygame.image.load("Bat Rush/Graphics/tick2.png").convert_alpha(), (50,35))

user_icon = pygame.transform.scale(pygame.image.load("Bat Rush/Graphics/profile.png").convert_alpha(), (60,60))

lock = pygame.transform.scale(pygame.image.load("Bat Rush/Graphics/lock.png").convert_alpha(), (60,60))

left_click = pygame.transform.scale(pygame.image.load("Bat Rush/Graphics/blue-mouse.png").convert_alpha(), (400,400))


# Music initialisation

pygame.mixer.music.load("Bat Rush/Audio/music.wav")
pygame.mixer.music.play(loops = -1)



#classes

class Button(): # Class for creating buttons
    def __init__(self, x, y, image, text, type):
        self.x = x
        self.y = y
        self.text = text
        self.type = type
        self.angle = 0

        if self.type == "text" or self.type == "switch1" or self.type == "switch2": # Checks whether our button is text based or image based
            self.surf = small_font.render(self.text, False, white)

        else:
            self.surf = image

        self.rect = self.surf.get_rect(center = (self.x,self.y))

    def draw(self):
        screen.blit(self.surf, self.rect)

    def hover(self):
        if self.rect.collidepoint((mouse_pos)):
            if self.type == "text" or self.type == "switch1" or self.type == "switch2":
                self.surf = small_font.render(self.text, False, blue)

            elif self.type == "cog":
                self.surf = pygame.transform.rotate(cog_surf, self.angle)
                self.rect = self.surf.get_rect(center = (self.x,self.y))
                self.angle += 3

            elif self.type == "back":
                pygame.draw.circle(screen, blue, (50,750), 34, 5)
                

        elif self.rect.collidepoint((mouse_pos)) == False and (self.type == "text" or self.type == "switch1" or self.type == "switch2") == True: # Checks whether the text based button is not being hovered.
            self.surf = small_font.render(self.text, False, white)

    def check_input(self):
        if self.rect.collidepoint((mouse_pos)) and mouse_pressed[0]:

            # check button type

            if self.type == "switch1": 
                if self.text == "High":
                    self.surf = switcher(self.surf, "Low")
                    self.text = "Low"
                elif self.text == "Low":
                    self.surf = switcher(self.surf, "High")
                    self.text = "High"

            elif self.type == "switch2":
                if self.text == "On":
                    self.surf = switcher(self.surf, "Off")
                    self.text = "Off"
                elif self.text == "Off":
                    self.surf = switcher(self.surf, "On")
                    self.text = "On"

            else:
                return True
        
        else:
            return False
            
        


    def update(self):
        self.draw()
        self.hover()



class Ground():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.surf = ground_img
        self.rect = self.surf.get_rect(topleft = (self.x, self.y)) # Obtains rectangle for image
        self.velocity = 6

    def draw(self):
        screen.blit(self.surf, self.rect) # Draws the object

    def move(self):
        self.rect.left -= self.velocity
        if self.rect.right < 0: # If object moves off the screen
            self.rect.left = 1000

    def collide(self, bat):
        bat_mask = bat.get_mask() # Obtain mask
        g_mask = pygame.mask.from_surface(self.surf)

        g_offset = (self.x - bat.x, self.y-bat.y) # Obtain relevant offset

        g_overlap = bat_mask.overlap(g_mask, g_offset) # Check whether bat and ground masks overlap (check for collision)
        if g_overlap:
            return True # Collision = True
        else:
            return False

    def update(self):
        self.draw()
        self.move()



class Bat(pygame.sprite.Sprite):
    animation_time = 5 # How long we show each animation

    def __init__(self,x,y, type, SFX):
        super().__init__()
        if type == "AI":
            self.imgs = AI_bat_imgs
        else:
            self.imgs = bat_imgs
        self.x = x
        self.y = y
        self.tick = 0 
        self.velocity = 0
        self.img_count = 0
        self.img = self.imgs[0]
        self.height = self.y
        self.max_displacement = 6.5
        self.jump_sound = pygame.mixer.Sound("Bat Rush/Audio/jump.mp3") # Initialise the jump sound effect
        if SFX == True:
            self.jump_sound.set_volume(0.5) 
        elif SFX == False:
            self.jump_sound.set_volume(0.0) # Reduces vol to 0


    def move(self): # Moves the actual bat
        self.tick += 1

        displacement = self.velocity * self.tick + 1.25 * self.tick ** 2

        if displacement >= self.max_displacement: # limit displacement to 6.5
            displacement = self.max_displacement
        
        if displacement < 0:
            displacement -= 2

        self.y += displacement

    
    def jump(self): 
        self.velocity = -8.7
        self.tick = 0
        self.height = self.y


        self.jump_sound.play() # Plays the jump sound effect


    def draw (self):
        self.img_count += 1

        # Animates the bat

        if self.img_count  < self.animation_time: 
            self.img = self.imgs[0]

        elif self.img_count < self.animation_time * 2: # Bat flapping
            self.img = self.imgs[1]

        elif self.img_count < self.animation_time * 3:
            self.img = self.imgs[1]

        elif self.img_count < self.animation_time * 3+1 : # Bat not flapping
            self.img = self.imgs[0]
            self.img_count = 0


        new_rectangle = self.img.get_rect(center = self.img.get_rect(topleft = (self.x,self.y)).center)
        screen.blit(self.img,new_rectangle.topleft)


    def get_mask(self):
        return pygame.mask.from_surface(self.img)  # Returns a mask of our image (for collision detection)
    
    def reposition(self, x,y):
        self.x = x
        self.y = y
    
    def update(self):
        self.draw()
        self.move()


class Pipe(pygame.sprite.Sprite): 
    def __init__(self,x):
        super().__init__() # Initialise group sprite
        self.x = x
        self.gap = 230 # Gap between 2 pipes
        self.height = 0

        self.pipe_top = pygame.transform.flip(pipe_img,False,True) # Flip the pipe image for the top pipe
        self.pipe_bottom = pipe_img # Normal pipe image for the bottom pipe

        self.top = 0
        self.bottom = 0

        self.passed = False
        self.set_height()

    def set_height (self):
        self.height = random.randrange(60,420) # Set random height for pipe
        self.top = self.height - self.pipe_top.get_height()
        self.bottom = self.height + self.gap # Ensuring bottom and top pipe have constant gap

    def move(self):
        self.x = self.x - 6

    def draw(self):
        screen.blit(self.pipe_top, (self.x,self.top)) # Draws the top pipe
        screen.blit(self.pipe_bottom, (self.x, self.bottom)) # Draws the bottom pipe

    def destroy(self):
        self.kill()


    def collide(self,bat):
        bat_mask = bat.get_mask() # A mask is an array/list of where all the pixels within the image are (more accurate than rectangle collisions)
        t_mask = pygame.mask.from_surface(self.pipe_top) # Top pipe mask
        b_mask = pygame.mask.from_surface(self.pipe_bottom) # Bottom pipe mask

        t_offset = (round(self.x - bat.x), round(self.top - bat.y)) # Obtain top offset to pass into overlap func
        b_offset = (round(self.x - bat.x), round(self.bottom - bat.y)) # Obtain bottom offset to pass into overlap func

        t_overlap = bat_mask.overlap(t_mask,t_offset)
        b_overlap = bat_mask.overlap(b_mask,b_offset)


        if t_overlap or b_overlap:
            return True
        else:
            return False
        
    def update(self):
        self.draw()
        self.move()


class database():
    def __init__(self):
        self.create_table() 

    def open_connection(self):
        self.sqlite_connection = sqlite3.connect("Bat Rush/Code/BatRushLDB.db")
        self.cursor = self.sqlite_connection.cursor() # Obtains the SQL cursor

    def close_connection(self):
        self.cursor.close()
        self.sqlite_connection.close()

    def create_table(self):
        self.open_connection() # Open connection 
        self.cursor.execute("CREATE TABLE IF NOT EXISTS LEADERBOARD(UserID INTEGER PRIMARY key AUTOINCREMENT,username VARCHAR(255),pass VARCHAR(255),score INTEGER DEFAULT 0);")
        self.close_connection() # Close connection

    def insert(self, user_name, password, score):
        self.open_connection()
        self.cursor.execute("Insert into LEADERBOARD VALUES (?,?, ?, ?)", (None,user_name,password,score)) # Insert username, password and score
        self.sqlite_connection.commit() # Ensure changes save
        self.close_connection()
    
    def display(self):
        self.open_connection()
        self.cursor.execute("Select * from LEADERBOARD")
        result = self.cursor.fetchall() 
        for row in result: # Iterate through each row returned
            print(row)
            print("\n")
        self.close_connection()

    def login(self, username, password):
        if self.username_exists(username): # Check user is already logged in
            return False
        self.open_connection()
        query = ("Select pass from LEADERBOARD WHERE username = ?")
        param = (username,)
        self.cursor.execute(query,param) # Pass query and parameter to execute
        stored_password = self.cursor.fetchone()[0] # Fetch first data item (the password)
        self.close_connection()
        if stored_password == hashlib.sha256(password.encode()).hexdigest():
            return True
        else:
            return False
        
    def fetch_score(self,username):
        self.open_connection()
        query = "Select score from LEADERBOARD WHERE username = ?"
        param = (username,)
        self.cursor.execute(query,param)
        score = self.cursor.fetchone()[0] # Select first data item (the score)
        self.close_connection()
        return score

    def username_exists(self, username):
        self.open_connection()
        query = "Select COUNT(username) from LEADERBOARD WHERE username = ?"
        param = (username,) 
        self.cursor.execute(query,param)
        count = self.cursor.fetchone()[0] # Obtain no. of common usernames
        self.close_connection()
        if count == 0: # If username is unique
            return True
        else:
            return False
        
    def update_score(self,score,username):
        self.open_connection()
        query = "Update LEADERBOARD set score = ? WHERE username = ?"
        self.cursor.execute(query,(score,username))
        self.sqlite_connection.commit() # Ensure changes are saved
        self.close_connection()
        return score
    
    def fetch_LDBdata(self):
        self.open_connection()
        query = "Select username, score from LEADERBOARD ORDER BY score desc"
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        self.close_connection()
        return result

    

class Textbox():
    
    def __init__(self,x,y,text):
        self.input_rect = pygame.Rect(x,y,370,60)
        self.text = text
        self.special_chars = "!@#$%^&*()-+?_=,<>/"
        self.text_surf = base_font.render(self.text, False, "#131313")
        self.text_rect = self.text_surf.get_rect(topleft = (self.input_rect.x+7, self.input_rect.y + 10))


    def display(self):
        pygame.draw.rect(screen, white, self.input_rect) # Draw textbox
        screen.blit(self.text_surf, self.text_rect)

    def display_cursor(self):
        self.cursor = pygame.Rect(self.text_rect.topright, (3,self.text_surf.get_height()))
        if time.time() % 1 > 0.5: # Causes the cursor to blink every second
            pygame.draw.rect(screen, black , self.cursor)



    def check_input(self):
        if self.input_rect.collidepoint((mouse_pos)) and mouse_pressed[0]: # Check user clicks on textbox
            return True
        
        else:
            return False

    def lengthchecker(self, type): # Checks length of username/password
        if type == "username":
                if len(self.text)<3 or len(self.text)>8:
                    return False
                
                else:
                    return True
                
        elif type == "password":
                if len(self.text)<6 or len(self.text)>12:
                    return False
                else:
                    return True
        
    def max(self): # Checks maximum length of username/password
        if self.text_surf.get_width() > 325:
            return True 
        else:
            return False
        
    def alphanumeric(self): # Checks text contains alphanumerics
        if self.text.isalnum():
            return True
        else:
            return False
        
    def pass_alphanumeric(self): # Checks specifically whether the password contains alphanumerics.
        for x in self.text:
            if x.isalnum() or (x in self.special_chars):
                return True
            else:
                return False



    def special_char(self): # Checks for any special characters in text
        if any(c in self.special_chars for c in self.text):
            return True
        
        else:
            return False
        
        

    def update(self):
        self.display()




# Initialising our main menu buttons

play_btn = Button(screen_width/2, 300, None, "Play", "text")
ldb_btn = Button(screen_width/2, 400, None, "Leaderboard", "text")
help_btn = Button(screen_width/2, 500, None, "Help", "text")
quit_btn = Button(screen_width/2, 600, None, "Quit", "text")  
cog_btn = Button(50, 50, cog_surf, None, "cog")
back_btn = Button(50,750,back_surf,None,"back")
logout_btn = Button(510, 600, None, "Log out", "text")

# Initialising our sign up buttons

submit_btn = Button(260,650,None,"Create","text")
login_btn = Button(750,650,None,"Log in","text")

# settings buttons

graphics_optBtn = Button(600,300,None,"High","switch1")
onoff_btn = Button(600,500,None,"On","switch2")
onoff2_btn = Button(600,400,None,"On","switch2")

# play buttons

normal_mode = Button(screen_width/2, 350, None, "Normal Mode", "text")
AI_mode = Button(screen_width/2, 500, None, "VS AI", "text")
play_again_btn = Button(screen_width/2, 500, None, "play Again", "text")

# difficulty buttons
easy_btn = Button(screen_width/2, 300, None, "Easy", "text")
medium_btn = Button(screen_width/2, 450, None, "Medium", "text")
hard_btn = Button(screen_width/2, 600, None, "Hard", "text")

# Initialising ground

base = Ground(0,700)
base2 = Ground(500,700)
base3 = Ground(1030,700)

# Initialising the main objects


Pipes = pygame.sprite.Group()
Bats = pygame.sprite.GroupSingle()

bat = Bat(50,200, None, True)
Bats.add(bat)


Pipes.add(Pipe(550))
Pipes.add(Pipe(1000))

# Initialise the DBMS

LDB_dbms = database()

BG_high = True # Sets graphics mode to high as default


# functions

def display_bg(play = False): # Checks which background to display

    if BG_high == True and play == False: # 1st background as user is not playing yet
        screen.fill("black")
        screen.blit(menu_bg,(0,0))

    if BG_high == True and play == True: # 2nd background as user is playing the gmae
        screen.fill("black")
        screen.blit(game_bg,(0,0))        

    elif BG_high == False: # User sets the graphics mode to lwo
        screen.fill(dark_blue)


def logout():

    # Lets user logout by resetting relevant values

    global acc_score, acc_username, logged_in
    acc_username = False
    acc_score = 0
    logged_in = False



def score_checker(score): # Used to check whether score obtained is greater than score stored.
    global acc_score
    if score>acc_score:
        acc_score = score
        LDB_dbms.update_score(acc_score, acc_username)



def account_displayer(): # Displays the user's account
    
    if acc_username == False: # Does not function if the user has not yet logged in
        pass
    else:
        account_rect = pygame.Rect(790,10,200,100) # x, y, width and height
        pygame.draw.rect(screen, bright_purple, account_rect, 0, 10)

        # Draws icon
        pygame.draw.rect(screen, white, pygame.Rect(920,30,50,50), 0, 10)
        screen.blit(pygame.transform.scale(user_icon, (40,40)), (924,35))

        # Display username, and high score
        text_displayer(845,43,acc_username,"smallest",white)
        text_displayer(845,73,"High Score ","smallest",white)
        text_displayer(905,73, str(acc_score),"smallest",red)


    
def message(correct, page):
    
    # For the sign up page

    if page == "sign up":
        if correct == "yes": # Successful account creation
            text_displayer(510, 700, "Account created", "smaller", green)

        elif correct == "no": # Unsuccessful account creation
            text_displayer(515, 700, "Requirements not met", "smaller", red)

        elif correct == "usernamefalse":
            text_displayer(515, 700, "Username taken", "smaller", red)

        else: 
            pass

     # For the login page  

    elif page == "login": # Successful login
        if correct == "yes":
            text_displayer(screen_width/2, 720, "Logging in...", "smaller", green)

        elif correct == "no": # Unsuccessful login
            text_displayer(screen_width/2, 720, "Invalid credentials", "smaller", red)

        else:
            pass
        

def resetter(): # Reset obstacles and bat
    bat.reposition(80,200)
    for pipe in Pipes:
        pipe.destroy()
    Pipes.add(Pipe(500))
    Pipes.add(Pipe(1000))


def switcher(surface, text): #function for toggle buttons
    surface = small_font.render(text, False, white)
    return surface
    



def text_displayer(x, y, text, size, colour): # function to display text based on size and colour
    if size == "large":
        text_surf = large_font.render(text, False, colour)
    elif size == "small":
        text_surf = small_font.render(text, False, colour)
    elif size == "smaller":
        text_surf = smaller_font.render(text, False, colour)
    else:
        text_surf = smallest_font.render(text, False, colour)

    text_rect = text_surf.get_rect(center = (x,y))
    screen.blit(text_surf,text_rect)




def end_game(): # function to end the game
    pygame.quit()
    sys.exit()


def game_over(): # Game over screen
    resetter()
    score_checker(score)

    while True:
        for event in pygame.event.get(): # Grabs all our events
            if event.type == pygame.QUIT:
                end_game()
            if event.type == pygame.MOUSEBUTTONUP:
                if cog_btn.check_input():
                    settings()
                if back_btn.check_input():
                    main_menu()
                if play_again_btn.check_input():
                    gamemodes()

        display_bg() # Display background


        text_displayer(screen_width/2, 300, "GAME OVER", "large", purple)
        text_displayer(screen_width/2, 400, f"Score {score}", "large", white)

        pygame.draw.rect(screen, green, pygame.Rect(314,472,370,60),0,10)


        global mouse_pos
        mouse_pos = pygame.mouse.get_pos()
        global mouse_pressed
        mouse_pressed = pygame.mouse.get_pressed()

        cog_btn.update()
        back_btn.update()
        play_again_btn.update()

        pygame.display.update()
        clock.tick(60)




def loading(type, difficulty = None): # Loading screen
    width = 10
    while True:
        for event in pygame.event.get(): # Grabs all our events
            if event.type == pygame.QUIT:
                end_game()

        screen.fill("#131313")
        loading_surf = large_font.render("Loading...",False,white)
        loading_rect = loading_surf.get_rect(center = (screen_width/2,200))
        loadingbox_rect = loadingbox.get_rect(center = (500,400))
        screen.blit(loading_surf, loading_rect)
        screen.blit(loadingbox, loadingbox_rect)

        loadingbar_surf = pygame.transform.scale(loadingbar, (width, 160))
        loadingbar_rect = loadingbar_surf.get_rect(topleft = (155,320))
        screen.blit(loadingbar_surf, loadingbar_rect)

        account_displayer()

        if width > 680:
            if type == "normal": 
                start()
            elif type == "AI":
                if difficulty == "easy": # load relevant difficulty bat
                    genome = [(1,load_bat("easy"))]
                    
                elif difficulty == "medium":
                    genome = [(1,load_bat("medium"))]
                   
                else:
                    genome = [(1,load_bat("hard"))]
                
                playerVsAI(genome,config)
                    
        width += 8 # How much the bar increases by in each loop

        pygame.display.update()
        clock.tick(60)



def start(): # function for start screen

    global score
    score = 0


    while True:
        for event in pygame.event.get(): # Grabs all our events
            if event.type == pygame.QUIT:
                end_game()
            if event.type == pygame.MOUSEBUTTONUP:
                if cog_btn.check_input():
                    settings()
                else:
                    bat.jump()

        display_bg(True)


        add_pipe = False

        global mouse_pos
        mouse_pos = pygame.mouse.get_pos()
        global mouse_pressed
        mouse_pressed = pygame.mouse.get_pressed()

        for pipe in Pipes:
            if pipe.collide(bat): # Bat collision with pipe
                game_over()

            if pipe.x + pipe.pipe_top.get_width() < 0: # Check whether the pipe is off the screen
                pipe.destroy()

            if not pipe.passed and pipe.x < bat.x: # Pipe has passed the bat
                pipe.passed = True
                add_pipe = True

            pipe.update()

        if add_pipe: # Score incremented and new pipe added
            score += 1
            Pipes.add(Pipe(1000))

        # Check for bat collisions with the ground

        if base.collide(bat):
            game_over()


        if base2.collide(bat):
            game_over()


        if base3.collide(bat):
            game_over()


        
        text_displayer(900,50,  f"Score {score}", "small", white) # Displays the score

        cog_btn.update()
        base.update()
        base2.update()
        base3.update()
        

        bat.update()


        pygame.display.update()
        clock.tick(60)


def sign_up(): # function for sign up screens
    timer = 0
    username = ""
    password = ""
    # Username/password textboxes states

    username_active = False
    password_active = False

    correct = ""
    

    while True:
        for event in pygame.event.get(): # Grabs all our events
            if event.type == pygame.QUIT:
                end_game()
            if event.type == pygame.MOUSEBUTTONUP:
                if cog_btn.check_input():
                    settings()
                if back_btn.check_input():
                    main_menu()
                if submit_btn.check_input():
                    if username_textbox.lengthchecker("username") and password_textbox.lengthchecker("password") and password_textbox.special_char() and username_textbox.alphanumeric() and \
                        password_textbox.pass_alphanumeric():
                        if LDB_dbms.username_exists(username):
                            hashed_password = hashlib.sha256(password.encode()).hexdigest() # The hashed version of the password
                            LDB_dbms.insert(username,hashed_password,0)
                            correct = "yes"
                        else:
                            correct = "usernamefalse"
                    else:
                        correct = "no"
                        

                if login_btn.check_input():
                    login()

            # textbox activation
            
            if username_textbox.check_input():
                username_active = True
                password_active = False
            elif password_textbox.check_input():
                password_active = True
                username_active = False


            # textboxes


            if event.type == pygame.KEYDOWN:

                # Username textbox


                if username_active == True and password_active == False: # Checks user clicks on textbox
                    if event.key == pygame.K_BACKSPACE:
                        username = username[:-1]
                    elif username_textbox.max():
                        pass
                    else:
                        username += event.unicode


                # Password textbox
                    

                elif username_active == False and password_active == True:
                    if event.key == pygame.K_BACKSPACE:
                        password = password[:-1]
                    elif password_textbox.max():
                        pass
                    else:
                        password += event.unicode
                        password_textbox.display_cursor()


        # Define our textboxes
                        
        display_bg()
                        
        username_textbox = Textbox(80,312,username) 
        password_textbox = Textbox(80,490,password)

        text_displayer(screen_width/2, 150, "Sign up", "large", purple)

        message(correct, "sign up")
        account_displayer()

        # Username display
        
        text_displayer(260, 280, "Username", "small", white)
        rect = pygame.Rect(80,252,370,60)
        pygame.draw.rect(screen, white, rect,3)
        username_textbox.update()

        # Password display

        text_displayer(260, 460, "Password", "small", white)
        rect2 = pygame.Rect(80,430,370,60)
        pygame.draw.rect(screen, white, rect2,3)
        password_textbox.update()

        if username_active == True and password_active == False:
            username_textbox.display_cursor()

        elif username_active == False and password_active == True:
            password_textbox.display_cursor()




        global mouse_pos
        mouse_pos = pygame.mouse.get_pos()
        global mouse_pressed
        mouse_pressed = pygame.mouse.get_pressed()

        # username and password checks

        if not username_textbox.lengthchecker("username"):
            screen.blit(cross, (510,250))
            text_displayer(770, 270, "Username between 3-8 characters","smaller",red)

                
        else:
            screen.blit(tick, (510,250))
            text_displayer(770, 270, "Username between 3-8 characters","smaller",green)

                
        if not password_textbox.lengthchecker("password"):
            screen.blit(cross, (510,290))
            text_displayer(775, 310, "Password between 6-12 characters","smaller",red)

        else:
            screen.blit(tick, (510,290))
            text_displayer(775, 310, "Password between 6-12 characters","smaller",green)





        if username_textbox.alphanumeric() and password_textbox.pass_alphanumeric():
            screen.blit(tick, (510,330))
            text_displayer(717, 350, "Alphanumeric characters","smaller",green)
        else:
            screen.blit(cross, (510,330))
            text_displayer(717, 350, "Alphanumeric characters","smaller",red)

        if password_textbox.special_char():
            screen.blit(tick, (510,370))
            text_displayer(760, 390, "Password contains special char","smaller",green)
        
        else:
            screen.blit(cross, (510,370))
            text_displayer(760, 390, "Password contains special char","smaller","red")

        submit_btn.update()
        cog_btn.update()
        back_btn.update()
        login_btn.update()

        pygame.display.update()
        clock.tick(60)


def login(): 
    username = ""
    password = ""
    username_active = False
    password_active = False
    login_btn = Button(500,670,None,"Log in","text")
    timer_true = False
    timer = 0

    correct = ""


    while True:
        for event in pygame.event.get(): # Grabs all our events
            if event.type == pygame.QUIT:
                end_game()
            if event.type == pygame.MOUSEBUTTONUP:
                if cog_btn.check_input():
                    settings()
                if back_btn.check_input():
                    sign_up()

                # Check for login btn click and that username and password already meet requirements  

                if login_btn.check_input():
                    if loginusername_textbox.lengthchecker("username") and loginpassword_textbox.lengthchecker("password") and loginpassword_textbox.special_char() and \
                     loginusername_textbox.alphanumeric() and loginpassword_textbox.pass_alphanumeric() and LDB_dbms.login(username,password):
                        if LDB_dbms.login(username, password): # Check for a successful login
                            global acc_score, acc_username 
                            acc_score = LDB_dbms.fetch_score(username) # Store current score
                            acc_username = username # Store username
                            correct = "yes"
                            timer_true = True
                            global logged_in
                            logged_in = True
                        else:
                            correct = "no"
                    else:
                        correct = "no"


            # textbox activation
            
            if loginusername_textbox.check_input():
                username_active = True
                password_active = False
            elif loginpassword_textbox.check_input():
                password_active = True
                username_active = False


            # textboxes


            if event.type == pygame.KEYDOWN:

                # Username textbox


                if username_active == True and password_active == False: # Checks user clicks on textbox
                    if event.key == pygame.K_BACKSPACE:
                        username = username[:-1]
                    elif loginusername_textbox.max():
                        pass
                    else:
                        username += event.unicode


                # Password textbox
                    

                elif username_active == False and password_active == True:
                    if event.key == pygame.K_BACKSPACE:
                        password = password[:-1]
                    elif loginpassword_textbox.max():
                        pass
                    else:
                        password += event.unicode


        display_bg()


        text_displayer(screen_width/2, 150, "Login", "large", purple)

        loginusername_textbox = Textbox(314,312,username)
        loginpassword_textbox = Textbox(314,512,password)

        message(correct, "login")
        account_displayer()

        # username 
        
        text_displayer(500, 282, "Username", "small", "white")
        rect = pygame.Rect(314,252,370,60)
        pygame.draw.rect(screen, white, rect,3)
        loginusername_textbox.update()


        # password

        text_displayer(500, 482, "Password", "small", white)
        rect = pygame.Rect(314,452,370,60)
        pygame.draw.rect(screen, white, rect,3)
        loginpassword_textbox.update()

        screen.blit(user_icon, (200,304))
        pygame.draw.rect(screen, white, pygame.Rect(190,292,80,80),3,10)

        screen.blit(lock, (200,504))
        pygame.draw.rect(screen, white, pygame.Rect(190,492,80,80),3,10)


        if username_active == True and password_active == False:
            loginusername_textbox.display_cursor()

        elif username_active == False and password_active == True:
            loginpassword_textbox.display_cursor()

        if timer_true:
            timer += 2.5
            if timer == 300:
                gamemodes()


        global mouse_pos
        mouse_pos = pygame.mouse.get_pos()
        global mouse_pressed
        mouse_pressed = pygame.mouse.get_pressed()

        cog_btn.update()
        back_btn.update()
        login_btn.update()


        pygame.display.update()
        clock.tick(60) 



def gamemodes(): # Gamemodes screen
    while True:
        for event in pygame.event.get(): # Grabs all our events
            if event.type == pygame.QUIT:
                end_game()
            if event.type == pygame.MOUSEBUTTONUP:
                if cog_btn.check_input():
                    settings()
                if back_btn.check_input():
                    main_menu()
                if normal_mode.check_input():
                    loading("normal")
                if AI_mode.check_input():
                    difficulty()

        display_bg()

        # Display the title and the different gammodes

        text_displayer(screen_width/2,150, "Gamemodes", "large", purple)
        account_displayer()

        pygame.draw.rect(screen, white, pygame.Rect(340,310,320,75),3,10)

        pygame.draw.rect(screen, white, pygame.Rect(340,460,320,75),3,10)



        global mouse_pos
        mouse_pos = pygame.mouse.get_pos()
        global mouse_pressed
        mouse_pressed = pygame.mouse.get_pressed()


        cog_btn.update()
        back_btn.update()
        normal_mode.update()
        AI_mode.update()

        pygame.display.update()
        clock.tick(60)  

def difficulty():
    while True:
        for event in pygame.event.get(): # Grabs all our events
            if event.type == pygame.QUIT:
                end_game()
            if event.type == pygame.MOUSEBUTTONUP:
                if cog_btn.check_input():
                    settings()
                if back_btn.check_input():
                    gamemodes()
                if easy_btn.check_input(): # Easy difficulty
                    loading("AI","easy")

                elif medium_btn.check_input(): # Medium difficulty
                    loading("AI","medium")

                elif hard_btn.check_input(): # Hard difficulty
                    loading("AI","hard")

        display_bg()

        text_displayer(screen_width/2, 150, "Select difficulty", "large", purple)

        # Provides 3 difficulties for the player

        pygame.draw.rect(screen, green, pygame.Rect(314,272,370,60),0,10) # Rectangle 1
        pygame.draw.rect(screen, blue, pygame.Rect(314,272,370,60),3,10) # Border 1

        pygame.draw.rect(screen, orange, pygame.Rect(314,422,370,60),0,10)
        pygame.draw.rect(screen, blue, pygame.Rect(314,422,370,60),3,10)

        pygame.draw.rect(screen, red, pygame.Rect(314,572,370,60),0,10)
        pygame.draw.rect(screen, blue, pygame.Rect(314,572,370,60),3,10)


        global mouse_pos
        mouse_pos = pygame.mouse.get_pos()
        global mouse_pressed
        mouse_pressed = pygame.mouse.get_pressed()

        cog_btn.update()
        back_btn.update()
        easy_btn.update()
        medium_btn.update()
        hard_btn.update()

        pygame.display.update()
        clock.tick(60)

def win():
    resetter()

    while True:
        for event in pygame.event.get(): # Grabs all our events
            if event.type == pygame.QUIT:
                end_game()
            if event.type == pygame.MOUSEBUTTONUP:
                if cog_btn.check_input():
                    settings()
                if back_btn.check_input():
                    main_menu()
                if play_again_btn.check_input():
                    gamemodes()

        display_bg()

        # Displays the title and the player score

        text_displayer(screen_width/2, 300, "You Beat the AI", "large", purple)
        text_displayer(screen_width/2, 400, f"Your Score {score}", "small", white)
        pygame.draw.rect(screen, green, pygame.Rect(314,472,370,60),0,10)


        global mouse_pos
        mouse_pos = pygame.mouse.get_pos()
        global mouse_pressed
        mouse_pressed = pygame.mouse.get_pressed()

        cog_btn.update()
        back_btn.update()
        play_again_btn.update()

        pygame.display.update()
        clock.tick(60)

def LDB(): # function for leaderboard screen
    result = LDB_dbms.fetch_LDBdata()

    while True:
        for event in pygame.event.get(): # Grabs all our events
            if event.type == pygame.QUIT:
                end_game()
            if event.type == pygame.MOUSEBUTTONUP:
                if cog_btn.check_input():
                    settings()
                if back_btn.check_input():
                    main_menu()

        display_bg()

        text_displayer(screen_width/2, 150, "Leaderboard", "large", purple)

        text_displayer(236,300,"Rank","smaller",bright_blue)

        text_displayer(466, 300, "Username", "smaller", bright_blue)
        text_displayer(700, 300, "Score", "smaller", bright_blue)

        row_y_pos = 350

        for i in range(10): # Draws the purple boxes around the usernames
            pygame.draw.rect(screen, purple, pygame.Rect(368,row_y_pos-10,200,20),0,10)
            row_y_pos += 35


        for i in range(0,2): # Iterates through first the usernames, and then the scores
            count = 1
            row_y_pos = 350
            for row in result:
                    if count<=10:
                        text_displayer(230,row_y_pos,str(count),"smaller",white)
                        data = str((row)[i]) # Obtains first data item in the current row
                        text_displayer(460+240*i, row_y_pos, data, "smaller", white) # Ensures username and score are separately written
                        row_y_pos += 35
                        count += 1
                    else:
                        break

            

        global mouse_pos
        mouse_pos = pygame.mouse.get_pos()
        global mouse_pressed
        mouse_pressed = pygame.mouse.get_pressed() 


        cog_btn.update()
        back_btn.update()
        account_displayer()

        pygame.display.update()
        clock.tick(60)


def settings(): # function for settings
    while True:
        for event in pygame.event.get(): # Grabs all our events
            if event.type == pygame.QUIT:
                end_game()
            if event.type == pygame.MOUSEBUTTONUP:
                if cog_btn.check_input():
                    settings()
                if back_btn.check_input():
                    main_menu()
                
                if logout_btn.check_input():
                    if logged_in == True and acc_username != False:
                        logout()

                graphics_optBtn.check_input()
                onoff_btn.check_input()
                onoff2_btn.check_input()
                    

        display_bg()

        if onoff_btn.text == "Off": # SFX button = off
            global bat
            bat = Bat(80,200, None, False)
        else:
            bat = Bat(80,200, None, True)

        if graphics_optBtn.text == "Low": # Graphics button = Low
            global BG_high
            BG_high = False

        elif graphics_optBtn.text == "High": 
            BG_high = True

        if onoff2_btn.text == "Off": # Music button = "Off"
            pygame.mixer.music.pause()

        elif onoff2_btn.text == "On":
            pygame.mixer.music.unpause()
            

        global mouse_pos
        mouse_pos = pygame.mouse.get_pos()
        global mouse_pressed
        mouse_pressed = pygame.mouse.get_pressed()

        text_displayer(500, 150, "Settings", "large", purple)
        text_displayer(400, 300, "Graphics |", "small", white)
        text_displayer(425, 400, "Music   |", "small", white)
        text_displayer(435, 500, "SFX    |", "small", white)

        ticks = pygame.time.get_ticks()
        millis = ticks % 1000
        seconds = int(ticks/1000 % 60)
        minutes = int(ticks/60000 % 60)
    

        out='{minutes:02d}:{seconds:02d}:{millis}'.format(minutes=minutes, millis=millis, seconds=seconds) # Output in minutes, seconds, milliseconds
        text_surf = base_font.render(out, False, white)
        text_rect = text_surf.get_rect(center = (510,650))
        screen.blit(text_surf,text_rect)
        
        account_displayer()

        cog_btn.update()
        back_btn.update()
        graphics_optBtn.update()
        onoff_btn.update()
        onoff2_btn.update()

        if acc_username != False: # Provide the option for the user to logout
            pygame.draw.rect(screen, "red", pygame.Rect(410,575,200,55), 0, 10)
            logout_btn.update()

        pygame.display.update()
        clock.tick(60)


def help(): # function for help screen

    while True:
        for event in pygame.event.get(): # Grabs all our events
            if event.type == pygame.QUIT:
                end_game()
            if event.type == pygame.MOUSEBUTTONUP:
                if cog_btn.check_input():
                    settings()
                if back_btn.check_input():
                    main_menu()

        display_bg()

        # Displays the relevant text and graphics for the help page

        text_displayer(500,150, "Help", "large", purple)

        text_displayer(700,300, "Avoid the obstacles!", "smaller", white)
        text_displayer(700,400, "Gain a point after passing an obstacle!", "smaller", white)
        text_displayer(700,500, "Left click the mouse to jump!", "smaller", white)

        account_displayer()

        text_displayer(500,600, "Username should contain alphanumerics","smaller",red)
        text_displayer(500,650, "Password should contain either special characters or alphanumerics.","smaller",red)

        global mouse_pos
        mouse_pos = pygame.mouse.get_pos()
        global mouse_pressed
        mouse_pressed = pygame.mouse.get_pressed()

        screen.blit(left_click, (100,200))


        cog_btn.update()
        back_btn.update()

        pygame.display.update()
        clock.tick(60)


def main_menu(): # function for main menu
    angle = 0
    while True: 
        for event in pygame.event.get(): # Grabs all our events
            if event.type == pygame.QUIT:
                end_game()
            if event.type == pygame.MOUSEBUTTONUP: # Checks mouse click
                if play_btn.check_input():
                    if logged_in == False:
                        sign_up()
                    else:
                        gamemodes()
                if ldb_btn.check_input():
                    LDB()
                if quit_btn.check_input():
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

        display_bg()


        text_displayer(screen_width/2, 150, "Bat Rush", "large", purple)

        account_displayer()

        play_btn.update()
        ldb_btn.update()
        quit_btn.update()
        cog_btn.update()
        help_btn.update()

        

        

        pygame.display.update() # Updates the screen
        clock.tick(60) # 60 fps


def playerVsAI(genomes,config):

    # 3 lists containing the neural networks, the bats and the genomes

    nets_lst = []
    bats_lst = []
    genome_lst = []



    for _,genome in genomes:
        net = neat.nn.FeedForwardNetwork.create(genome, config) # Set up a neural network for each genome
        nets_lst.append(net) # Add it to the neural net list
        bats_lst.append(Bat(150,200, "AI", False))
        genome.fitness = 0 # Assign fitness function
        genome_lst.append(genome) # Add to genome list

    global score
    score = 0

    for pipe in Pipes:
        pipe.destroy()
    Pipes.add(Pipe(550))
    Pipes.add(Pipe(1000))


    while True:
        for event in pygame.event.get(): # Grabs all our events
            if event.type == pygame.QUIT:
                end_game()
            if event.type == pygame.MOUSEBUTTONUP:
                if cog_btn.check_input():
                    settings()
                else:
                    bat.jump()


        display_bg(True)


        global mouse_pos
        mouse_pos = pygame.mouse.get_pos()
        global mouse_pressed
        mouse_pressed = pygame.mouse.get_pressed()


        add_pipe = False
        pipe_index = 0

        # Checks which pipe to look at

        if len(bats_lst) > 0:
            
            if len(Pipes) > 1 and bats_lst[0].x > Pipes.sprites()[0].x + Pipes.sprites()[0].pipe_top.get_width():  # if pipe passed
                pipe_index = 1 
                
        else:
            break      


        # Bat movement  


        for genome_id, AI_bat in enumerate(bats_lst):  
            genome_lst[genome_id].fitness += 0.1
            AI_bat.move()

            
            output = nets_lst[genome_id].activate((AI_bat.y, abs(AI_bat.y - Pipes.sprites()[pipe_index].height), abs(AI_bat.y - Pipes.sprites()[pipe_index].bottom))) # Passing in our values

            if output[0] > 0.5:  # Tanh activation function used.
                AI_bat.jump()




        # Updating and checking for collisions with pipes

        for pipe in Pipes:

            pipe.update()

            for genome_id,AI_bat in enumerate(bats_lst):
                if pipe.collide(AI_bat):
                    genome_lst[genome_id].fitness -= 1 # Reduce fitness score

                    # Pop from all lists

                    bats_lst.pop(genome_id) 
                    nets_lst.pop(genome_id)
                    genome_lst.pop(genome_id)
                    win() # Call win function

            if pipe.collide(bat):
                game_over()
                    

            if not pipe.passed and pipe.x < bat.x: # Checking whether pipe has passed yet
                pipe.passed = True
                add_pipe = True



            if pipe.x + pipe.pipe_top.get_width() < 0: # Check whether the pipe is off the screen
                pipe.destroy()


        if add_pipe:
            score += 1
            for genome in genome_lst:
                genome.fitness += 5
            Pipes.add(Pipe(1000))


        # Updating and checking for collisions with the ground

        for genome_id, AI_bat in enumerate(bats_lst):
            if base.collide(AI_bat) or base2.collide(AI_bat) or base3.collide(AI_bat):
                    
                    # Pop from all lists

                    bats_lst.pop(genome_id) 
                    nets_lst.pop(genome_id)
                    genome_lst.pop(genome_id)
                    win()                


        text_displayer(900,50,  f"Score {score}", "small", white) # Displays the score

        if base.collide(bat) or base2.collide(bat) or base3.collide(bat):
            game_over()

        base.update()
        base2.update()
        base3.update()
        cog_btn.update()
        bat.update()


        for AI_bat in bats_lst:
            AI_bat.draw()

        pygame.display.update()
        clock.tick(60)


def load_bat(difficulty): # Loads relevant bat from file
    with open(f"Bat Rush/Code/{difficulty}.pkl","rb") as f: # Reopens the file and loads the bat
        genome = pickle.load(f)
        return genome
    
    
if __name__ == "__main__": 
    local_dir = os.path.dirname(__file__) # grab directory to our file
    config_path = os.path.join(local_dir,"config-feedforward.txt") # join local directory to the name of the configuration file
    config = neat.config.Config(neat.DefaultGenome,neat.DefaultReproduction,neat.DefaultSpeciesSet,neat.DefaultStagnation,config_path) # Define all subheadings
    main_menu()

# Made by Aditya Ranjan