#Imports pygame
import pygame
#import module to generate random numbers
import random



#Class that holds all methods and attributes for fighter----------------------------------------
class Fighter():
    #sets constants
    RED = (255, 0, 0)
    #Initialises Fighter
    def __init__(self,player, x,y, flip, data, sprite_list, animation_steps, hit_fx, jump_fx):
        #Sets involved player
        self.player = player
        #Sets the number of frames for loading an animation
        self.size = data[0]
        #Scales the image before stored
        self.scale = data[1]
        #Positions sprite on screen
        self.offset = data[2]
        #Determines cooldown after animation
        self.animation_cooldown = data[3]
        #Determines whether the player needs to flip to attack player
        self.flip = flip
        #Function iterates through and stores each subsurface of the animation in a 2D list
        self.animation_list = self.load_images(sprite_list, animation_steps)
        #Allows animations to be played
        self.action = 1         #0- Attack1, 1- Attack2, 2- Death, 3- Fall, 4- Idle, 5- Jump, 6- Run, 7- TakeHit, 8- Block
        #Stores location of each frame in the animation so it can be iterated through
        self.frame_index = 0
        self.image = self.animation_list[self.action][self.frame_index]
        #Measures time when fighter is created
        self.update_time = pygame.time.get_ticks()
        #creates position for player
        self.rect = pygame.Rect((x,y, 80, 130))
        #sets vertical velocity of player
        self.vel_y = 0
        #Running status
        self.running = False
        #Stores status of player whether jumping or not
        self.jump = False
        #Status of attack type
        self.attack_type = 0
        #Prevents repeated attacks from one button press
        self.attacking = False
        #Adds a cooldown between repeated attacks to prevent spamming
        self.attack_cooldown = 0
        #Status for being hit
        self.hit = False
        #Sets health bar of character to 100HP
        self.health = 100
        #Status of life
        self.alive = True
        #Loads sfx from main
        self.hitfx = hit_fx
        self.jumpfx = jump_fx
        #Sets block status of character
        self.block_status = False
        #Sets block cooldown of character
        self.block_cooldown = 0
        self.update_block_cooldown = False
        #Critical hit status
        self.critical = False

    #-----------IMAGE LOADER-----------------------------------------------
    #extract images from each sprite animation in sprite_list
    def load_images(self,sprite_list, animation_steps):
        animation_list = []
        position = 0
        #For every time it takes the frames in each animation
        for animationNum in animation_steps:
            #It will find the position of the numFrame in animation_steps list
            ########position = animation_steps.index(animationNum)
            #Will use position to find the animation from the sprite_list specific to it
            animation = sprite_list[position]
  
            temp_img_list = []
            #for every frame in animation
            for i in range(0,animationNum):
                #Small img of each frame taken and stored in a temp list
                temp_img = animation.subsurface(i * self.size, 0, self.size, self.size)
                temp_img_scaled = pygame.transform.scale(temp_img, (self.size * self.scale, self.size * self.scale))
                temp_img_list.append(temp_img_scaled)
            animation_list.append(temp_img_list)
            position += 1
        return animation_list







    #Method in Fighter to allow movement with a key press-------------------------------------------
    def move(self, WIDTH, HEIGHT, surface, target, round_over):
        #Sets speed and change in x and y coordinates
        SPEED = 7
        dx = 0
        dy = 0
        #Sets gravity constant
        GRAVITY = 2
        #Defaults animation to idle
        self.running = False
        #Defaults attack type to 0
        
        #self.attack_type = 0
        #Obtains keystrokes
        key = pygame.key.get_pressed()



        #--------Chooses movement based on key press (and if the character is not attacking)----------------------------------------

        #Only lets character move if its not attacking
        if self.attacking == False and self.alive == True and round_over == False:
            #----------------------------------P1-------------------------------------------------
            if self.player == 1:
                if key[pygame.K_s] and self.block_cooldown == 0:
                    self.block_status = True
                else:
                    if self.block_status == True:
                        self.update_block_cooldown = True
                    self.block_status = False
                    #If a pressed, character moves to left
                    if key[pygame.K_a]:
                        dx = -SPEED
                        self.running = True
                    #If d pressed, character moves to the right
                    if key[pygame.K_d]:
                        dx = SPEED
                        self.running = True
                        


                    #JUMPING
                    if key[pygame.K_w] and self.jump == False:
                        self.vel_y = -30
                        #Updates status on jump
                        self.jump = True


                    #ATTACK
                    #Chooses between two different attack options
                    if key[pygame.K_r] or key[pygame.K_t]:
                        if self.hit == True:
                            self.attack_cooldown = 20
                        elif self.hit == False:
                            #Updates status of attack
                            if key[pygame.K_r]:
                                self.attack_type = 1
                            if key[pygame.K_t]:
                                self.attack_type = 2
                            #executes attack function
                            self.attack(target)
            
#----------------------PLAYER 2 MOVEMENT-----------------------------------------
            if self.player == 2:
                if key[pygame.K_DOWN] and self.block_cooldown == 0:
                    self.block_status = True
                else:
                    if self.block_status == True:
                        self.update_block_cooldown = True
                    self.block_status = False
                    #If <- pressed, character moves to left
                    if key[pygame.K_LEFT]:
                        dx = -SPEED
                        self.running = True
                    #If -> pressed, character moves to the right
                    if key[pygame.K_RIGHT]:
                        dx = SPEED
                        self.running = True
                        
                    #JUMPING
                    #if up arrow pressed
                    if key[pygame.K_UP] and self.jump == False:
                        self.vel_y = -30
                        #Updates status on jump
                        self.jump = True

                    #ATTACK
                    #Chooses between two different attack options
                    if key[pygame.K_o] or key[pygame.K_p]:
                        if self.hit == True:
                            self.attack_cooldown = 20
                        elif self.hit == False:
                            #Updates status of attack
                            if key[pygame.K_o]:
                                self.attack_type = 1
                            if key[pygame.K_p]:
                                self.attack_type = 2
                            #executes attack function
                            self.attack(target)



        #Apply gravity onto player
        self.vel_y += GRAVITY # Player accelerates to ground
        dy += self.vel_y # Velocity affects vertical displacement




        #Ensures the player doesn't move off the screen---------------------------------------------

        #If x coordinates after movement is left than 0 --> push right onto the screen
        if self.rect.left + dx < 0:
            dx = - self.rect.left
        #If x coordinates after movement is greater than screen width --> push left onto screen
        if self.rect.right + dx > WIDTH:
            dx = WIDTH - self.rect.right


        #ensures y coordinate doesn't go through the floor
        if self.rect.bottom + dy > HEIGHT -60:
            #Sets downward velocity to 0
            self.vel_y = 0
            #Moves player back onto floor
            dy = HEIGHT -60 - self.rect.bottom
            #As player is on ground, jump status is False
            self.jump = False


        #Ensure players are facing each other

        if target.rect.centerx > self.rect.centerx:
            self.flip = False
        else:
            self.flip = True

        #Apply cooldown
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        if self.block_cooldown > 0:
            self.block_cooldown -= 1



        #updates player position-----------------------------------------------------------------------------------
        self.rect.x += dx
        self.rect.y += dy



    #Updates the animation updates
    def update(self):
        #Check action being performed to choose animation
        if self.health <= 0:
            self.health = 0
            self.alive = False
            self.update_action(2) #Sets to dying animation
        elif self.block_status == True:
            self.update_action(8)
        elif self.hit == True:
            self.update_action(7) #Sets action to getting hit
        elif self.attacking == True:
            if self.hit == True:
                self.attacking = False
                self.attack_cooldown = 20

            else:
                if self.attack_type == 1:
                    self.update_action(0) #Sets action to attack 1
                elif self.attack_type == 2:
                    self.update_action(1) # sets action to attack 2
        elif self.jump == True:
            self.update_action(3) #Sets actions to jumping (fall animation)
            self.jumpfx.play()
        elif self.running == True:
            self.update_action(6) #Sets action to running
        else:
            if self.update_block_cooldown == True and self.block_status == False:
                self.block_cooldown = 100
                self.update_block_cooldown = False
            self.update_action(4) #Reverts back to IDLE


        #Has a 500 ms cooldown before another frame can be played
        animation_cooldown = self.animation_cooldown
        self.image = self.animation_list[self.action][self.frame_index]
        #check if enough time has passed since last update
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
        #Checks if animation has finished
        if self.frame_index >= len(self.animation_list[self.action]):
            #First check if player is dead
            if self.alive == False:
                self.frame_index = len(self.animation_list[self.action]) -1
            else:
                    self.frame_index = 0
                    if self.action == 8:
                            pass
                    
                    if self.action == 0 or self.action == 1:
                        self.attacking = False
                        if self.attack_type == 1:
                            self.attack_cooldown = 20 #Sets action to attack 1
                        elif self.attack_type == 2:
                            self.attack_cooldown = 50 # sets action to attack 2
                        
                    #Updates action to idle if get hit animation is done
                    if self.action == 7:
                        self.hit = False
                        #If player was in an attack, then attack in stopped
                        self.attacking = False
                        if self.attack_type == 1:
                            self.attack_cooldown = 20 #Sets action to attack 1
                        elif self.attack_type == 2:
                            self.attack_cooldown = 50 # sets action to attack 2
                    
                    self.attack_type = 0
               


    #Function that allows the fighter to make an attack------------------------------------------------------------
    def attack(self, target):
        if self.attack_cooldown == 0:
            self.attacking = True
            self.hitfx.play()
            attacking_rect = pygame.Rect(self.rect.centerx - (2 * self.rect.width * self.flip), self.rect.y, 2 * self.rect.width, self.rect.height)
        
            #Checks if the attack hitbox collides with another player
            if attacking_rect.colliderect(target.rect):
                if target.block_status == True:
                    pass
                else:
                    criticalHit = 1
                    if random.randint(1,7) == 1:
                        self.critical = True
                        criticalHit = 2
                    if self.attack_type == 2:
                        target.health -= 10 * criticalHit
                        target.hit = True
                    elif self.attack_type == 1:
                        target.health -= 5 * criticalHit
                        target.hit = True
                


        



    #Updates actions and animations settings
    def update_action(self, new_action):
        if new_action != self.action:
            self.action = new_action
            #Updates animation settings to prevent errors
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()





    #Draws fighter onto screen---------------------------------------------------------------------------------------
    def draw(self, surface):
        #Flips the sprite if required
        img = pygame.transform.flip(self.image, self.flip, False)
        #Draws fighter sprite using offset onto the rectangle hitbox
        surface.blit(img, (self.rect.x - (self.offset[0]), self.rect.y - (self.offset[1])))
