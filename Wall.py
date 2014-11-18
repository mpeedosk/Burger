import pygame
gameheight = 600
gamewidth = 800

class Wall(pygame.sprite.Sprite):
    def __init__(self, image_data, width, height):
        #käivitamine
        pygame.sprite.Sprite.__init__(self)
        # seina suuruse ja värvi parameetrid
        # seina asukoha määramine
        if image_data == False:
            self.image = pygame.Surface([width, height])
            self.image.set_colorkey((0,0,0))
        else:
            self.image = pygame.image.load(image_data)
            self.image = pygame.transform.scale(self.image,(width, height))
        self.rect = self.image.get_rect()
        #self.rect.y = y
        #self.rect.x = x
        
class Level(object):
    #wall_list = None    
    world_shift = 0
    
    def __init__(self, player):
        self.wall_list = pygame.sprite.Group()
        self.player = player
        
    def update(self):
        self.wall_list.update()
    def draw(self, screen):
        screen.blit(self.background_1,(self.world_shift//2-5,0))
        screen.blit(self.background_2,(self.world_shift-5,0))
        self.wall_list.draw(screen)
    def shift_world(self, x):
        self.world_shift += x
        for wall in self.wall_list:
            wall.rect.x += x

class Falling_Plat(Wall):
    def update(self):
        self.rect.y -=3
        hit = pygame.sprite.collide_rect(self, self.player)
        self.rect.y +=3
        if hit:
            if self.type == 1:
                self.falling = True
            else:
                if self.type ==2:
                    self.rect.y+= 5
                else:
                    self.rect.y-=5
        if self.falling:
            self.rect.y += self.fallspeed
            self.fallspeed += .2
        if self.rect.top > 530 or self.rect.bottom < 0:
            self.wall_list.remove(self)

class UpDown_Plat(Wall):
    def update(self):
        self.rect.y += self.speed
        if self.rect.top > 530 or self.rect.bottom < -102:
            self.wall_list.remove(self)    
            
class Moving_Wall(Wall):
    left_right = 0
    up_down = 0

    limit_top=0
    limit_bot=0
    limit_left=0
    limit_right=0

    #player = None

    def update(self):
        # parem/vasak
        self.rect.x += self.left_right
        hit = pygame.sprite.collide_rect(self, self.player)
        if hit:
            if self.left_right <0:
                self.player.rect.right = self.rect.left                
            else:
                self.player.rect.left = self.rect.right
        # üles/alla
        self.rect.y += self.up_down
        hit = pygame.sprite.collide_rect(self, self.player)
        if hit:
            if self.up_down < 0:
                self.player.rect.bottom = self.rect.top
            else:
                if self.type == 2:
                    self.player.livingwall = False
                else:
                    self.player.rect.top = self.rect.bottom
        # kontrollib kas peab suunda vahetama        
        if self.rect.bottom > self.limit_bot or self.rect.top < self.limit_top:
            self.up_down *=-1

        pos = self.rect.x - self.level.world_shift
        if pos < self.limit_left or pos > self.limit_right:
            self.left_right *=-1
    

class Level_1(Level):
    def __init__(self, player):
        Level.__init__(self, player)
        self.background_1 = pygame.image.load("sky.png").convert_alpha()
        self.background_2 = pygame.image.load("Ground.png").convert_alpha()
                    #picture, width, height, x , y
        objects = [["Outside\Rock.png",50,104, 700, 396],
                   ["Outside\Rock.png",50,227, 870, 273],
                   ["World\Platform_07.png", 140, 45, 1065, 150],
                   ["World\Platform_06.png", 140,45, 1065, 300],
                   ["World\Plat_YellowGreen.png", 110, 40, 2150, 230],
                   ["World\Plat_Grey.png", 50, 40, 2500, 330],
                   ["World\Plat_Brown.png", 110, 40, 2650, 250],
                   ["World\Plat_Grey.png", 110, 40, 3025, 350],
                   ["World\Plat_Purp.png", 110, 40, 3370, 510],
                   ["World\Platform_08.png", 110, 40, 2925, 180],
                   ["World\Plat_Brown.png", 70, 40, 4280, 180],
                   ["World\Plat_Brown.png", 30, 20, 5260, 80],
                   ["World\Platform_08.png", 50, 20, 5500, 330],
                    # no picture, width, height, x, y
                   [False, 5,500, 0, 0],
                   [False, 5,500, 5970, 0],
                   [False, 1663, 5, 0, 500],
                   [False, 1098, 5, 2023, 500],
                   [False, 422, 5, 3745, 500],
                   [False, 210, 5, 4168, 435],
                   [False, 210, 5, 4375, 365],
                   [False, 210, 5, 4585, 295],
                   [False, 195, 5, 4793, 225],
                   [False, 5, 300, 4983, 270],
                   [False, 270, 5, 5730, 500],
                   ]
        for i in objects:
            item = Wall(i[0],i[1],i[2])
            item.rect.x = i[3]
            item.rect.y = i[4]
            item.player = self.player
            self.wall_list.add(item)
            
        # liikuvad objektid, - pilt, pildi laius, kõrgus ,  x kordinaat, y kordinaat, x limiit, kiirus
        moving_leftright = [#["Outside\Sand_Tile_Half_Round-01.png",150, 26, 2000, 375, 2400,3],
                            ["World\Log.png", 92, 30, 1676, 552, 1932, 3],
                            ["World\Small.png", 55, 25, 3125, 190, 3500, 8],
                            ["World\Log.png", 80, 26, 5000, 520, 5250, 2],
                            ]
        
        for i in moving_leftright:
            item = Moving_Wall(i[0], i[1],i[2])
            item.rect.x = i[3]
            item.rect.y= i[4]
            item.limit_left = i[3]
            item.limit_right = i[5]
            item.left_right = i[6]
            item.player = self.player
            item.level = self
            self.wall_list.add(item)
        # üles alla liikuvad objektid, pilt, pildi laius, pildi kõrgus, x kordinaat, y, kordinaat, y lim, kiirus
        moving_updown = [["World\Wood.png", 42, 42, 2023, 285, 494, 6,2],
                         ["World\Plat_Yellow_spikes.png", 150, 20, 3745, 180, 410, 2,2],
                         ["World\Plat_Grey.png", 100, 35, 5350, 120, 320, 2,1],
                         ["World\Plat_Grey.png", 100, 35, 5350, 260, 460, 2,1],
                         #["Outside\Obstacle_Spike_Down.png",208, 9, 1400, 100, 500 , 6]
                        ]
        for i in moving_updown:
            item = Moving_Wall(i[0], i[1],i[2])
            item.rect.x = i[3]
            item.rect.y= i[4]
            item.limit_top = i[4]
            item.type = i[7]
            item.limit_bot = i[5]
            item.up_down = i[6]
            item.player = self.player
            item.level = self
            self.wall_list.add(item)
    
        
class Level_2(Level):
    def __init__(self, player):
        Level.__init__(self, player)
        self.background_1 = pygame.image.load("DungeonWall.png").convert_alpha()
        self.background_2 = pygame.image.load("DungeonGround.png").convert_alpha()
                    #picture, width, height, x , y
        objects = [[False, 5,500, 0, 0],
                   [False, 5,500, 5970, 0],
                   [False, 1390, 5, 0, 513],
                   [False, 1050, 5, 2916, 513],
                   [False, 197 , 5 , 2698, 313],
                   [False, 5, 140 , 2890, 373],
                   [False, 5, 240 , 2698, 373],

                   ["World\Plat_dung_1.png", 113, 18, 1150, 320],
                   #["World\RockSD.png", 108, 30, 911, 470, 1111, 4],
                   #["World\RockSD.png", 54, 30, 951, 440, 1111, 5],
                   [False, 5, 1100, 3995, -500],
                   ]
        for i in objects:
            item = Wall(i[0],i[1],i[2])
            item.rect.x = i[3]
            item.rect.y = i[4]
            item.player = self.player
            self.wall_list.add(item)
            
        # liikuvad objektid, - pilt, pildi laius, kõrgus ,  x kordinaat, y kordinaat, x limiit, kiirus
        moving_leftright = [["World\RockSD_2.png", 145, 40, 871, 450, 1020, 5],
                            #["World\RockSD.png", 145, 40, 2000, 430, 2200, 5],
                            ]
        
        for i in moving_leftright:
            item = Moving_Wall(i[0], i[1],i[2])
            item.rect.x = i[3]
            item.rect.y= i[4]
            item.limit_left = i[3]
            item.limit_right = i[5]
            item.left_right = i[6]
            item.player = self.player
            item.level = self
            self.wall_list.add(item)
        # üles alla liikuvad objektid, pilt, pildi laius, pildi kõrgus, x kordinaat, y, kordinaat, y lim, kiirus
        moving_updown = [["World\Spikes4.png", 137, 107, 500, 30, 435, 5,2],
                         ["World\Spikes4.png", 137, 107, 637, 105, 450, 4,2],
                         ["World\Spikes4.png", 137, 107, 774, 180, 465, 3,2],
                         ["World\Plat_dung_1.png", 113, 18, 2200, 200,460,2,2],

                        ]
        for i in moving_updown:
            item = Moving_Wall(i[0], i[1],i[2])
            item.rect.x = i[3]
            item.rect.y= i[4]
            item.limit_top = i[4]
            item.limit_bot = i[5]
            item.up_down = i[6]
            item.type = i[7]
            item.player = self.player
            item.level = self
            self.wall_list.add(item)
            
        falling =[["World\Plat_dung_2.png", 113, 18, 1300, 200,1,1],
                  ["World\Plat_dung_2.png", 113, 18, 1500, 120,1,1],                  
                  ["World\Plat_dung_2.png", 113, 18, 1750, 190,2,1],
                  ["World\Plat_dung_4.png", 113, 18, 2000, 240,5,2],
                  ["World\Plat_dung_4.png", 113, 18, 2400, 440,5,3],
                    ]
        for i in falling:
            item = Falling_Plat(i[0],i[1],i[2])
            item.rect.x = i[3]
            item.rect.y = i[4]
            item.type = i[6]
            item.player = self.player
            item.fallspeed = i[5]
            item.wall_list = self.wall_list
            item.falling = False
            self.wall_list.add(item)
class Level_3(Level):
    def __init__(self, player):
        Level.__init__(self, player)
        self.background_1 = pygame.image.load("CaveBack2.png").convert_alpha()
        self.background_2 = pygame.image.load("CaveGround.png").convert_alpha()
        self.plat_2 = pygame.image.load("World\Plat_dung_2.png").convert_alpha()
        objects = [[False, 5,500, 0, 0],
                   [False, 2308, 5, 0, 500],
                   [False, 400, 5, 2738, 500],
                   [False, 5, 500, 2990, 0],
                   ]
        for i in objects:
            item = Wall(i[0],i[1],i[2])
            item.rect.x = i[3]
            item.rect.y = i[4]
            item.player = self.player
            self.wall_list.add(item)
    def add_boss_wall(self):
        wall = Wall(False, 5,555)
        wall.rect.x = 2180 + self.world_shift 
        wall.rect.y = 0
        self.wall_list.add(wall)
    def remove_boss_wall(self):
        for wall in self.wall_list:
            if wall.rect.height == 555:
                self.wall_list.remove(wall)
    def add_plat_up(self,up_down):
        item = UpDown_Plat("World\Plat_dung_2.png", 115, 18)

        if up_down == "down":
            item.rect.x = 2570 + self.world_shift
            item.rect.y = -102
            item.speed = 2

        else:
            item.rect.x = 2365 + self.world_shift
            item.rect.y = 520            
            item.speed = -2
        item.wall_list = self.wall_list
        self.wall_list.add(item)
