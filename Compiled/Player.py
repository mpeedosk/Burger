import pygame
from Wall import *

#Mängijaga seotud funktsioonid

class Player(pygame.sprite.Sprite):
    
    left_right = 0 # liikumise kiirus
    up_down = 0 # hüppamine
    walls = None 
    level = None
    walkingleft =[] # vasakule liikumise kaadrid
    walkingright =[] # paremale liikumise kaadrid
    direction = "R" # alguses on suund paremale poole
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # laen 9 kaadrit sisse
        for i in range(8):
            self.walkingright.append(pygame.image.load('Graphics/Player/frame' + str(i)+ '.png').convert_alpha())

        for i in range(8):
            self.walkingleft.append(pygame.transform.flip(pygame.image.load('Graphics/Player/frame' + str(i)+ '.png'), True, False))
        # kui ei liigu, siis valib vastavalt suunale pildi
        self.idle_right = pygame.image.load('Graphics/Player/Idle.png').convert_alpha()
        self.idle_left = pygame.transform.flip(pygame.image.load('Graphics/Player/Idle.png'), True, False)
        # kui surematus on peal, siis joonistab vuntsid ette
        self.mustascheright = pygame.image.load('Graphics/Player/StacheR.png').convert_alpha()
        self.mustascheleft = pygame.image.load('Graphics/Player/StacheL.png').convert_alpha()
        self.image = self.walkingleft[0]
        self.rect = self.image.get_rect(height=85)
        # kas mängija elab
        self.living = True
        # kas mängija on saanud platformi tõttu surma
        self.livingwall = True

    # liikumise funktsioon
    def move(self, x):
        self.left_right += x
        
    def update(self, walls):
        # gravitatsioon alati peal
        self.gravity()
        # laseb mängijal seintega reageerida
        self.walls = walls
        # liigub vasakule või paremale
        self.rect.x += self.left_right
        pos = self.rect.x + self.level.world_shift
        if self.direction == "R":
            frame = (pos//15 % len(self.walkingright))
            self.image = self.walkingright[frame]
            if self.left_right == 0: # kui inimene ei liigu
                self.image = self.idle_right
        else: 
            frame = (pos//15 % len(self.walkingleft))
            self.image = self.walkingleft[frame]
            if self.left_right == 0:
                self.image = self.idle_left
        
        # kontrollib kas mängija ja sein on kokku põrkunud
        wallcollide = pygame.sprite.spritecollide(self, self.walls, False)
        for collide in wallcollide:

            # kui liigume paremale, siis pannakse mängija parema külja kordinaaat võrduma seina vasaku küljega
            if abs(collide.rect.left - self.rect.right) < 10:
                self.rect.right = collide.rect.left
            # kui liigume vasakule, siis vastupidi
            elif abs(self.rect.left - collide.rect.right) < 10:
                self.rect.left = collide.rect.right
            # kui mängija ise ei liigu ja platvorm liigub paremale/vasakule
            else:
                if abs(self.rect.left-collide.rect.right) < 10:
                    self.rect.left = collide.rect.right
                elif abs(self.rect.right-collide.rect.left) < 10:
                    self.rect.right = collide.rect.left

        # uuendab üles, alla
        self.rect.y += self.up_down
        wallcollide = pygame.sprite.spritecollide(self, self.walls, False)
        for collide in wallcollide:
            
            if self.up_down > 0:
                self.rect.bottom = collide.rect.top
            else:
                self.rect.top = collide.rect.bottom
            self.up_down = 0
            # kui mängija põrkub liikuva seinaga kokku
            if isinstance(collide, Moving_Wall):
                self.rect.x += collide.left_right

    # gravitatsiooni funktsioon      
    def gravity(self):
        # kui mängija platformi peal alla liigub, siis kiirus on 6
        if self.up_down == 0:
            self.up_down = 6
        else: # kukudes iga tsükkel kiireneb kukumine
            self.up_down += 0.65
            
    def jump(self):
        # vaatab kõigepealt kas platform on all või mitte
        self.rect.y +=7
        wallcollide = pygame.sprite.spritecollide(self, self.walls, False)
        self.rect.y -=7
        if wallcollide:
            self.up_down = -13 # hüppamise kõrgus
            
    # vuntsi joonistamine
    def mustache(self,screen):
        if self.direction == "R":
            screen.blit(self.mustascheright,(self.rect.x+5,self.rect.y+30))
        else:
            screen.blit(self.mustascheleft,(self.rect.x-35,self.rect.y+30))
