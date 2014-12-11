import pygame
from Power import *

# põhiklass
class AllObject(pygame.sprite.Sprite):
    # Surematu loendus, arvud 0-9
    countdown = []
    
    def __init__(self, image_data, width, height, object_type):
        pygame.sprite.Sprite.__init__(self)
        self.frames = [] # igale esindalaje anname kaadrite jaoks listi
        if object_type == 1:
            # objektid mis ei vaja animatsiooni
            self.image = pygame.image.load(image_data)
            self.image = pygame.transform.scale(self.image,(width, height))
        elif object_type == 2: # kasutame width muutujat kaadrite arvu määramiseks
            for i in range(width):
                self.frames.append(pygame.image.load(image_data + str(i)+ '.png').convert_alpha())
            self.image = self.frames[0]
            self.framelim = height # kasutame height muutujat kaadrite limiidi mõõtmiseks
        self.rect = self.image.get_rect()
        self.framerate = 0
        
class GameObject(object):
    
    world_shift = 0
    joke = False
    countdown = []
    star_png = []
    
    def __init__(self):
        self.normal_object = pygame.sprite.Group()
        self.moving_object = pygame.sprite.Group()
        #järjekord oluline
        self.layers = pygame.sprite.OrderedUpdates()
        # laema ühe korra failid ära
        for i in range(10):
            self.countdown.append(pygame.image.load('Graphics/UI/Numbers/Nr'+str(i)+'.png').convert_alpha())
        for i in range(4):
            self.star_png.append(pygame.image.load('Graphics/UI/Stars/Star'+ str(i)+ '.png').convert_alpha())
            
    def update(self):
        self.layers.update()
        self.moving_object.update()
        self.normal_object.update()
        # käime terve liikutavate objektide listi läbi
        for enemy in self.moving_object:
            frame = (enemy.framerate//6 % len(enemy.frames))
            enemy.image = enemy.frames[frame]
            enemy.framerate +=1
            if enemy.type == "fire": # tule puhul on meil lõpmatu loop
                enemy.framerate += 1
            elif enemy.type == "crow" and enemy.framerate > 1106: # varese pea puhul teeme kaks loopi 
                self.moving_object.remove(enemy)
            if enemy.framelim > 0: # kui limiit on olemas, siis teeme kuni jõuame limiidini
                if frame > enemy.framelim:
                    self.moving_object.remove(enemy)
                    if enemy.type == "bomb": # kui bommiga on tegemist, siis lõppedes teeme plahvatuse
                        self.explosion()
                    elif enemy.type == "exp": # kui plahvatus ära lõppeme, teeme nalja
                        self.joke = True

    # ekaanile joonistamine
    def draw(self, screen):
        self.normal_object.draw(screen)
        self.moving_object.draw(screen)
        self.layers.draw(screen)

    # objektide nihutamine
    def shift_world(self,x):
        self.world_shift +=x
        for item in self.layers:
            item.rect.x += x
        for item in self.normal_object:
            item.rect.x += x
        for item in self.moving_object:
            item.rect.x += x

    # surematuse taimer
    def stach_timer(self,screen,when_stache):
        # arvutab ajaerinevuse, kuvab vastava numbri ekraanile
        get_time_diff =  pygame.time.get_ticks() - when_stache
        if get_time_diff < 1000:
            screen.blit(self.countdown[9],(10,45))
        elif get_time_diff < 2000: 
            screen.blit(self.countdown[8],(10,45))
        elif get_time_diff < 3000:
            screen.blit(self.countdown[7],(10,45))
        elif get_time_diff < 4000:
            screen.blit(self.countdown[6],(10,45))
        elif get_time_diff < 5000:
            screen.blit(self.countdown[5],(10,45))
        elif get_time_diff < 6000:
            screen.blit(self.countdown[4],(10,45))
        elif get_time_diff < 7000:
            screen.blit(self.countdown[3],(10,45))
        elif get_time_diff < 8000:
            screen.blit(self.countdown[2],(10,45))
        elif get_time_diff < 9000:
            screen.blit(self.countdown[1],(10,45))
        else:
            screen.blit(self.countdown[0],(10,45))

    # vastavalt sellele palju tähti on kuvab õige tähtede arvu
    def stars(self,screen,stars):
        if stars == 0:
            screen.blit(self.star_png[0],(10,10))
        elif stars == 1:
            screen.blit(self.star_png[1],(10,10))
        elif stars == 2:
            screen.blit(self.star_png[2],(10,10))
        else:
            screen.blit(self.star_png[3],(10,10))        


# level 1 objektid
class Object_1(GameObject):
    def __init__(self):
        
        GameObject.__init__(self)
                            # pilt, kaadrite arv, kaadrite limiit, objecti tüüp
        fire = AllObject('Graphics/World/Fire/frame', 22,0, 2)
        fire.rect.x = 230 + self.world_shift
        fire.rect.y = 405
        fire.type = "fire"
        self.moving_object.add(fire)

# level 2 objektid, ei ole muutusi võrreldes lvl 1-ga
class Object_2(GameObject):
    def __init__(self):
        
        GameObject.__init__(self)
        
        crow = AllObject('Graphics/World/Crow/frame', 92,0, 2)
        crow.rect.x = 265 + self.world_shift
        crow.rect.y = 10
        crow.type = "crow"
        self.moving_object.add(crow)

# level 3 objektid
class Object_3(GameObject):
    def __init__(self):
        GameObject.__init__(self)
        # bossi elude mõõtja
        hp = [["Graphics/UI/Boss/boss_hp_back.png", 256, 64,1,1],
              ["Graphics/UI/Boss/boss_hp_fill.png", 226, 64,2,1],
              ["Graphics/UI/Boss/boss_hp.png", 256, 64,3,1],
            ]

        for h in hp:
            health = AllObject(h[0], h[1], h[2], h[4])
            health.rect.x = 2700
            health.rect.y = 20
            health.type = h[3]
            self.layers.add(health)
            
    # funktsioon pommide lisamiseks
    def add_pot(self):
        bomb = AllObject('Graphics/PowerUp/Pot/frame', 45,43, 2)
        bomb.rect.x = 2220 + self.world_shift
        bomb.rect.y = 405
        bomb.type = "bomb"
        self.moving_object.add(bomb)

    # funktsioon plahatuse lisamiseks
    def explosion(self):
        exp = AllObject('Graphics/World/Explosion/frame', 19, 17, 2)
        exp.rect.x = 2185 + self.world_shift 
        exp.rect.y = 340
        exp.type = "exp"
        self.moving_object.add(exp)

    # funktsioon bossi pea lisamiseks
    def add_head(self):
        head = AllObject('Graphics/Enemy/Level 3/Boss/Horsehead.png',224,189, 1)
        head.rect.x = self.world_shift + 2755
        head.rect.y = 320
        self.normal_object.add(head)
        
