#Credits to LuizMelo for the sprites
#Credits to Daniel Linssen for the fonts


#imports pygame
import pygame
#import random
import random
#imports the Fighter class from fighter.py
from SlashAssets.fighter import Fighter
from SlashAssets.button import Button



#Initialises pygame

pygame.init()

#sets constants width and height of screen
WIDTH, HEIGHT = 1000, 500

victory_fx = pygame.mixer.Sound("SlashAssets/SoundEffects/SFX/LevelUp.wav")
victory_fx.set_volume(0.5)

score_fx = pygame.mixer.Sound("SlashAssets/SoundEffects/SFX/score.wav")
score_fx.set_volume(0.75)



#Sets display and title for screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Slasherz")

#CONTROLS FRAMERATE OF THE GAME
clock = pygame.time.Clock()
FPS = 60



#Function for drawing text
def draw_text(text, font, text_col, x,y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x,y))

def round_music_loader(prevRandom):
     #Loads music and sounds
     decide = False
     while decide == False:
        randomNum = random.randint(0,3)
        if randomNum != prevRandom:
            if randomNum == 0:
                pygame.mixer.music.load("SlashAssets/FantasyAdventureMusic/DecisiveBattleDevi.wav")
                decide = True
            elif randomNum == 1:
                pygame.mixer.music.load("SlashAssets/FantasyAdventureMusic/IcyCaveDevi.wav")
                decide = True
            elif randomNum == 2:
                pygame.mixer.music.load("SlashAssets/FantasyAdventureMusic/MysteriousDungeonDevi.wav")
                decide = True
            elif randomNum == 3:
                pygame.mixer.music.load("SlashAssets/FantasyAdventureMusic/PrepareBattleDevi.wav")
                decide = True

        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1, 0.0, 5000)#Plays it on repeat and fades in
        return randomNum 


#Functioning for drawing bg onto screen
def draw_bg(bg):
    #Scales the background to the size of the screen
    scaled_bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))
    screen.blit(scaled_bg, (0,0))

def draw_plx(bg_images, bg_width, scroll):
    for x in range(5):
        speed = 0
        for i in bg_images:
            screen.blit(i,((x * bg_width) - scroll * speed,0))
            speed += 0.2

def Critical(player1, player2):
    if player1.critical == True:
        return True
    elif player2.critical == True:
        return True
    else:
        return False

#Creates a graphic for the player's health
def draw_health_bar(health, x, y):
    YELLOW = (255,255,0)
    RED = (255,0,0)
    WHITE = (255,255,255)
    #Calculates ratio of health remaining
    hp = health/100
    pygame.draw.rect(screen, WHITE, (x-3, y-3, 406, 36))
    #Red bar shows max health, which is revealed as yellow bar decreases :. red bar shows health lost
    pygame.draw.rect(screen, RED, (x, y, 400, 30))
    #Displays current health
    pygame.draw.rect(screen, YELLOW, (x, y, 400 * hp, 30))


def Menu(FPS, WIDTH, HEIGHT, screen, clock, score_fx, victory_fx):
    count = 0
    scroll = 0
    #loads background image onto screen
    bg_images = []
    for i in range(1,8):
        bg = pygame.image.load(f"SlashAssets/Grassy_Mountains/layers_fullcolor/plx-{i}.png").convert_alpha()
        scaled_bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))
        bg_images.append(scaled_bg)
    bg_width = bg_images[0].get_width()
    
    
    pygame.mixer.music.load("SlashAssets/FantasyAdventureMusic/TitleThemeDevi.wav")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1, 0.0, 5000)

    bg_overlay = pygame.image.load("SlashAssets/Title_controls2.png").convert_alpha()
    menu_font = pygame.font.Font("SlashAssets/UI/pixelfont.ttf", 30)
    img = pygame.image.load("SlashAssets/UI/button_rounded_GB.png")
    image = pygame.transform.scale(img, (200, 60))

    run = True
    while run:
        #Initialises frame rate
        clock.tick(FPS)
        #draws background
        draw_plx(bg_images, bg_width, scroll)
        draw_bg(bg_overlay)

        

        #gets mouse pos
        mouse_pos = pygame.mouse.get_pos()


        PLAY_BUTTON = Button(image, (WIDTH//2 -20,300), "PLAY", menu_font, "#d7fcd4", "White")
        QUIT_BUTTON = Button(image, (WIDTH//2 -20,370), "QUIT", menu_font, "#d7fcd4", "White")


        for button in [PLAY_BUTTON, QUIT_BUTTON]:
            button.changeColour(mouse_pos)
            button.update(screen)


        if pygame.time.get_ticks() - count >= 50: #If 1 second has passed
                scroll += 0.15 #Decrement count down by 1
                count = pygame.time.get_ticks()



        #Searches for events = event handler
        for event in pygame.event.get():
            #If window is closed, the game ends
            if event.type == pygame.QUIT:
                pygame.mixer.music.stop()
                run = False
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.CheckForInput(mouse_pos):
                    
                    victory_fx.play()
                    pygame.mixer.music.stop()
                    round_music_loader(0)
                    PlayGame(FPS, WIDTH, HEIGHT, screen, clock, score_fx)
                if QUIT_BUTTON.CheckForInput(mouse_pos):
                    pygame.mixer.music.stop()
                    score_fx.play()
                    run = False
                    pygame.quit()
                    return

        #Constantly updates the display
        pygame.display.update()


def Pause(FPS, WIDTH, HEIGHT, screen, clock, score_fx, prev_random):
    go_menu = False
    
    menu_font = pygame.font.Font("SlashAssets/UI/pixelfont.ttf", 30)
    bg = pygame.image.load("SlashAssets/PauseBG.png")
    small_pause_image = pygame.image.load("SlashAssets/pause_button.png")
    pause_image = pygame.transform.scale(small_pause_image, (50, 50))


    small_pause_circle = pygame.image.load("SlashAssets/pause_circle.png")
    pause_circle = pygame.transform.scale(small_pause_circle, (60, 60))
    mute_circle = pygame.transform.scale(small_pause_circle, (75, 75))

    mute_small = pygame.image.load("SlashAssets/MuteIcon.png")
    mute_icon = pygame.transform.scale(mute_small, (100, 100))
    
    
    continue_img = pygame.image.load("SlashAssets/UI/button_rounded_GB.png")
    continue_image = pygame.transform.scale(continue_img, (240, 80))
    quit_img = pygame.transform.scale(continue_img, (220, 75))

    
    pause = True
    while pause:
        clock.tick(FPS)
        draw_bg(bg)
        screen.blit(pause_circle, (WIDTH/2 -30, 10))
        screen.blit(mute_circle, (WIDTH-120,HEIGHT - 120))
        #gets mouse pos
        mouse_pos = pygame.mouse.get_pos()
        CONTINUE_BUTTON = Button(continue_image, (WIDTH/2,220), "RESUME", menu_font, "#d7fcd4", "White")
        QUIT_BUTTON = Button(quit_img, (WIDTH/2,310), "MENU", menu_font, "#d7fcd4", "White")
        PAUSE_BUTTON = Button(pause_image, (WIDTH/2, 40), "", menu_font, "#d7fcd4", "White")
        MUTE_BUTTON = Button(mute_icon, (WIDTH-80,HEIGHT - 80), "", menu_font, "#d7fcd4", "White")

        

        for button in [CONTINUE_BUTTON, PAUSE_BUTTON, QUIT_BUTTON, MUTE_BUTTON]:
            button.changeColour(mouse_pos)
            button.update(screen)



        for event in pygame.event.get():
            #If window is closed, the game ends
            if event.type == pygame.QUIT:
                go_menu = True
                pygame.mixer.music.stop()
                score_fx.play()
                pygame.mixer.music.load("SlashAssets/FantasyAdventureMusic/TitleThemeDevi.wav")
                pygame.mixer.music.set_volume(0.5)
                pygame.mixer.music.play(-1, 0.0, 5000)
                pause = False
                break
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PAUSE_BUTTON.CheckForInput(mouse_pos) or CONTINUE_BUTTON.CheckForInput(mouse_pos):
                    pygame.mixer.music.stop()
                    score_fx.play()
                    round_music_loader(2)
                    pause = False
                    break
                if QUIT_BUTTON.CheckForInput(mouse_pos):
                    go_menu = True
                    pygame.mixer.music.stop()
                    score_fx.play()
                    pygame.mixer.music.load("SlashAssets/FantasyAdventureMusic/TitleThemeDevi.wav")
                    pygame.mixer.music.set_volume(0.5)
                    pygame.mixer.music.play(-1, 0.0, 5000)
                    pause = False
                    break
                if MUTE_BUTTON.CheckForInput(mouse_pos):
                    score_fx.play()
                    if pygame.mixer.music.get_volume() > 0:
                        pygame.mixer.music.set_volume(0)
                    else:
                        pygame.mixer.music.set_volume(0.5)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.mixer.music.stop()
                score_fx.play()
                round_music_loader(prev_random)
                pause = False
                break
    
        #Constantly updates the display
        pygame.display.update()
    return go_menu





#When function is executed, the game will play---------------------------------------------------------------------
def PlayGame(FPS, WIDTH, HEIGHT, screen, clock, score_fx):
    
    #loads background image onto screen
    bg = pygame.image.load("SlashAssets/FreePixelArtForest/Background.png").convert_alpha()

    menu_font = pygame.font.Font("SlashAssets/UI/pixelfont.ttf", 30)
    small_pause_image = pygame.image.load("SlashAssets/pause_button.png")
    pause_image = pygame.transform.scale(small_pause_image, (50, 50))

    small_pause_circle = pygame.image.load("SlashAssets/pause_circle.png")
    pause_circle = pygame.transform.scale(small_pause_circle, (60, 60))

    

    #Define game variables
    countdown = 4
    count_update = pygame.time.get_ticks()
    score = [0,0] #P1 score, P2 score
    round_over = False
    ROUND_OVER_COOLDOWN = 3000

    #DEFINES SIZES OF SPRITES
    SAMURAI_SIZE = 200
    SAMURAI_SCALE = 2
    SAMURAI_OFFSET = [170, 130]
    samurai_data = [SAMURAI_SIZE, SAMURAI_SCALE, SAMURAI_OFFSET, 50]
    VILLAIN_SIZE = 126
    VILLAIN_SCALE = 2.3
    VILLAIN_OFFSET = [102, 60]
    villain_data = [VILLAIN_SIZE, VILLAIN_SCALE, VILLAIN_OFFSET, 30]

    #sets previous music
    prev_random = 2
    


    #Sets sound effects from the assets folder
    hit_fx = pygame.mixer.Sound("SlashAssets/SoundEffects/SFX/Hit.wav")
    hit_fx.set_volume(0.75)

    jump_fx = pygame.mixer.Sound("SlashAssets/SoundEffects/SFX/Jump.wav")
    jump_fx.set_volume(0.5)

    



    #------load spritesheets--------------------
    #----P1----------
    P1_Attack1_animation = pygame.image.load("SlashAssets/MartialHero2/Sprites/Attack1.png").convert_alpha()
    P1_Attack2_animation = pygame.image.load("SlashAssets/MartialHero2/Sprites/Attack2.png").convert_alpha()
    P1_Death_animation = pygame.image.load("SlashAssets/MartialHero2/Sprites/Death.png").convert_alpha()
    P1_Fall_animation = pygame.image.load("SlashAssets/MartialHero2/Sprites/Fall.png").convert_alpha()
    P1_Idle_animation = pygame.image.load("SlashAssets/MartialHero2/Sprites/Idle.png").convert_alpha()
    P1_Jump_animation = pygame.image.load("SlashAssets/MartialHero2/Sprites/Jump.png").convert_alpha()
    P1_Run_animation = pygame.image.load("SlashAssets/MartialHero2/Sprites/Run.png").convert_alpha()
    P1_TakeHit_animation = pygame.image.load("SlashAssets/MartialHero2/Sprites/TakeHit.png").convert_alpha()
    P1_Block_animation = pygame.image.load("SlashAssets/MartialHero2/Sprites/Block2.png").convert_alpha()
    #Stores them in a list so they can be passed as a parameter into fighter
    P1_Sprite_An = [P1_Attack1_animation,P1_Attack2_animation,P1_Death_animation,P1_Fall_animation,P1_Idle_animation,P1_Jump_animation,P1_Run_animation,P1_TakeHit_animation, P1_Block_animation]

    #--------P2------------------------
    P2_Attack1_animation = pygame.image.load("SlashAssets/MartialHero3/Sprite/Attack1.png").convert_alpha()
    P2_Attack2_animation = pygame.image.load("SlashAssets/MartialHero3/Sprite/Attack3.png").convert_alpha()
    P2_Death_animation = pygame.image.load("SlashAssets/MartialHero3/Sprite/Death.png").convert_alpha()
    P2_Fall_animation = pygame.image.load("SlashAssets/MartialHero3/Sprite/Fall.png").convert_alpha()
    P2_Idle_animation = pygame.image.load("SlashAssets/MartialHero3/Sprite/Idle.png").convert_alpha()
    P2_Jump_animation = pygame.image.load("SlashAssets/MartialHero3/Sprite/Jump.png").convert_alpha()
    P2_Run_animation = pygame.image.load("SlashAssets/MartialHero3/Sprite/Run.png").convert_alpha()
    P2_TakeHit_animation = pygame.image.load("SlashAssets/MartialHero3/Sprite/TakeHit.png").convert_alpha()
    P2_Block_animation = pygame.image.load("SlashAssets/MartialHero3/Sprite/Block1.png").convert_alpha()

    #Stores them in a list so they can be passed as a parameter into fighter
    P2_Sprite_An = [P2_Attack1_animation,P2_Attack2_animation,P2_Death_animation,P2_Fall_animation,P2_Idle_animation,P2_Jump_animation,P2_Run_animation,P2_TakeHit_animation,P2_Block_animation]




    #No. of animations images per animation 
    #(Attack1,Attack2,Death,Fall,Idle,Jump,Run,TakeHit) in that order
    
    P1animation = [4,4,7,2,4,2,8,3,1]
    P2animation = [7,9,11,3,10,3,8,3,1]



    #SlashAssets/Fonts/m6x11.ttf

    #define font
    count_font = pygame.font.Font("SlashAssets/UI/pixelfont.ttf", 60)
    critical_font = pygame.font.Font("SlashAssets/UI/pixelfont.ttf", 30)
    player_font = pygame.font.Font("SlashAssets/UI/pixelfont.ttf", 19)


    #Creates two fighters using Fighter class
    player1 = Fighter(1, 200, 310, False, samurai_data, P1_Sprite_An, P1animation, hit_fx, jump_fx)
    player2 = Fighter(2, 700, 310, True, villain_data, P2_Sprite_An, P2animation, hit_fx, jump_fx)
    
    
    # LOOPS THE GAME using while loop
    run = True
    while run:

        #Initialises frame rate
        clock.tick(FPS)

        #draws background
        draw_bg(bg)

        

        #Show player health
        draw_health_bar(player1.health, 20, 20)
        draw_health_bar(player2.health, 580, 20)

        #Has text for player 1 and 2 beneath health bars
        draw_text("PLAYER 1          SCORE: " + str(score[0]), player_font, (255,255,255), 20, 60)
        draw_text("PLAYER 2          SCORE: " + str(score[1]), player_font, (255,255,255), 695, 60)


        screen.blit(pause_circle, (WIDTH/2 -30, 10))

        #Creates buttons and mouse position
        mouse_pos = pygame.mouse.get_pos()
        PAUSE_BUTTON = Button(pause_image, (WIDTH/2, 40), "", menu_font, "White", "White")
        for button in [PAUSE_BUTTON]:
            button.changeColour(mouse_pos)
            button.update(screen)

        



        if countdown <= 0:
            #Moves fighters with key presses
            player1.move(WIDTH, HEIGHT, screen, player2, round_over)
            player2.move(WIDTH, HEIGHT, screen, player1, round_over)
        elif countdown == 1:
            draw_text("FIGHT!", count_font, (255,0,0), WIDTH/2 - 110, HEIGHT/3)
            if pygame.time.get_ticks() - count_update >= 1000: #If 1 second has passed
                countdown -= 1 #Decrement count down by 1
                count_update = pygame.time.get_ticks()
        else:
            #display count
            draw_text(str(countdown -1), count_font, (255,0,0), WIDTH/2 -20, HEIGHT/3)
            if pygame.time.get_ticks() - count_update >= 1000: #If 1 second has passed
                countdown -= 1 #Decrement count down by 1
                count_update = pygame.time.get_ticks()

        #Updates fighter animations
        player1.update()
        player2.update()

        #Draws fighters onto screen
        player1.draw(screen)
        player2.draw(screen)

        if Critical(player1, player2) == False:
            critical_count = pygame.time.get_ticks()
        else:
            draw_text("CRITICAL HIT!", critical_font, (255,0,0), WIDTH/2 - 110, HEIGHT/3)
            
        if pygame.time.get_ticks() >= critical_count +1000:
                    player1.critical = False
                    player2.critical = False

        #Check for player defeat
        if round_over == False:
            #if P1 dies, P2 score increases and the round is over
            if player1.alive == False:
                score[1] += 1
                round_over = True
                round_over_time = pygame.time.get_ticks()
            #Same with P2
            elif player2.alive == False:
                score[0] += 1
                round_over = True
                round_over_time = pygame.time.get_ticks()
        else:
            #Displays victory if round ends
            
            draw_text("VICTORY!", count_font, (0,0,255), WIDTH/2 - 200, HEIGHT/3)
            if pygame.time.get_ticks() - round_over_time > ROUND_OVER_COOLDOWN:
                #Resets round
                round_over = False
                countdown = 4
                score_fx.play()
                #resets and chooses random game music
                pygame.mixer.music.stop()
                new_prev = round_music_loader(prev_random)
                prev_random = new_prev
                #Resets players
                player1 = Fighter(1, 200, 310, False, samurai_data, P1_Sprite_An, P1animation, hit_fx, jump_fx)
                player2 = Fighter(2, 700, 310, True, villain_data, P2_Sprite_An, P2animation, hit_fx, jump_fx)

        #Searches for events = event handler
        for event in pygame.event.get():
            #If window is closed, the game ends
            if event.type == pygame.QUIT:
                pygame.mixer.music.stop()
                score_fx.play()
                pygame.mixer.music.load("SlashAssets/FantasyAdventureMusic/TitleThemeDevi.wav")
                pygame.mixer.music.set_volume(0.5)
                pygame.mixer.music.play(-1, 0.0, 5000)
                run = False
                break

            #HANDLES BUTTON CLICKS
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PAUSE_BUTTON.CheckForInput(mouse_pos):
                    pygame.mixer.music.stop()
                    score_fx.play()
                    pygame.mixer.music.load("SlashAssets/SoundEffects/SFX/AdventureLoop.wav")
                    pygame.mixer.music.set_volume(0.5)
                    pygame.mixer.music.play(-1, 0.0, 5000)
                    go_menu = Pause(FPS, WIDTH, HEIGHT, screen, clock, score_fx, prev_random)
                    pygame.mixer.music.stop()
                    if go_menu == True:
                        score_fx.play()
                        pygame.mixer.music.load("SlashAssets/FantasyAdventureMusic/TitleThemeDevi.wav")
                        pygame.mixer.music.set_volume(0.5)
                        pygame.mixer.music.play(-1, 0.0, 5000)
                        run = False
                        break
                    else:
                        round_music_loader(2)


            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.mixer.music.stop()
                score_fx.play()
                pygame.mixer.music.load("SlashAssets/SoundEffects/SFX/AdventureLoop.wav")
                pygame.mixer.music.set_volume(0.5)
                pygame.mixer.music.play(-1, 0.0, 5000)
                go_menu = Pause(FPS, WIDTH, HEIGHT, screen, clock, score_fx, prev_random)
                pygame.mixer.music.stop()
                if go_menu == True:
                    score_fx.play()
                    pygame.mixer.music.load("SlashAssets/FantasyAdventureMusic/TitleThemeDevi.wav")
                    pygame.mixer.music.set_volume(0.5)
                    pygame.mixer.music.play(-1, 0.0, 5000)
                    run = False
                    break
                else:
                    round_music_loader(2)

                

        #Constantly updates the display
        pygame.display.update()



if __name__ == "__main__":
    Menu(FPS, WIDTH, HEIGHT, screen, clock, score_fx, victory_fx)
    pygame.quit()