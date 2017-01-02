import pygame

class Wall(pygame.sprite.Sprite):
    def __init__(self, image_data, width, height):
        #käivitamine
        pygame.sprite.Sprite.__init__(self)
        # seina suuruse ja värvi parameetrid
        # seina asukoha määramine
        if image_data == False: # pildita platformid
            self.image = pygame.Surface([width, height])
            self.image.set_colorkey((0,0,0)) # platformi nähtamatuks tegemine
        else: # pildiga platformid
            self.image = pygame.image.load(image_data)
            self.image = pygame.transform.scale(self.image,(width, height))
        self.rect = self.image.get_rect()
        
class Level(object):

    world_shift = 0
    
    def __init__(self, player):
        self.wall_list = pygame.sprite.Group()
        self.player = player

    # uuendamine
    def update(self):
        self.wall_list.update()
        
    # joonistamine
    def draw(self, screen):
        screen.blit(self.background_1,(self.world_shift//2-5,0)) # tagatausta joonistamine, liigub 2 korda aeglasemalt kui platformid
        screen.blit(self.background_2,(self.world_shift-5,0)) # esitausta joonistamine
        self.wall_list.draw(screen)

    # nihutamine
    def shift_world(self, x):
        self.world_shift += x
        for wall in self.wall_list:
            wall.rect.x += x

# kukuvad platformid
class Falling_Plat(Wall):
    def update(self):
        # vaatab kas on kokkupõrge mängijaga
        self.rect.y -=3
        hit = pygame.sprite.collide_rect(self, self.player)
        self.rect.y +=3
        
        if hit:
            # kui tüüp=1 kukub lihtsalt maha
            if self.type == 1:
                self.falling = True
            else: 
                if self.type ==2: # kui tüüp on kaks kukub niikaua kui mängija peal seisab
                    self.rect.y+= 5
                else:
                    self.rect.y-=5
                    
        # kukub kiirendavalt
        if self.falling:
            self.rect.y += self.fallspeed
            self.fallspeed += .2
            
        # kui platform jõuab piisavalt madalale või liiga kõrgele eemaldatakse ta ära
        if self.rect.top > 530 or self.rect.bottom < 0:
            self.wall_list.remove(self)

# ülesalla liikuv platform
class UpDown_Plat(Wall):
    
    def update(self):
        self.rect.y += self.speed
        if self.rect.top > 530 or self.rect.bottom < -150:
            self.wall_list.remove(self)    
            
class Moving_Wall(Wall):
    # liikumise kiirused
    left_right = 0
    up_down = 0
    # limiidid
    limit_top=0
    limit_bot=0
    limit_left=0
    limit_right=0

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
                    self.player.livingwall = False # kui mängija alumise servaga pihta saab, sureb ära
                else:
                    self.player.rect.top = self.rect.bottom
                    
        # kontrollib kas peab suunda vahetama        
        if self.rect.bottom > self.limit_bot or self.rect.top < self.limit_top:
            self.up_down *=-1

        pos = self.rect.x - self.level.world_shift
        if pos < self.limit_left or pos > self.limit_right:
            self.left_right *=-1
    
# level ühe platformid
class Level_1(Level):
    def __init__(self, player):
        Level.__init__(self, player)
        # taustad
        self.background_1 = pygame.image.load("Graphics/Background/Level 1 Back.png").convert_alpha()
        self.background_2 = pygame.image.load("Graphics/Background/Level 1 Ground.png").convert_alpha()

                    #pilt, pikkus, kõrgus, x , y
        objects = [["Graphics\World\Rock.png",50,104, 700, 396],
                   ["Graphics\World\Rock.png",50,227, 870, 273],
                   ["Graphics\World\Plat_teal_2.png", 140, 45, 1065, 150],
                   ["Graphics\World\Plat_teal.png", 140,45, 1065, 300],
                   ["Graphics\World\Plat_YellowGreen.png", 110, 40, 2150, 230],
                   ["Graphics\World\Plat_Grey.png", 50, 40, 2500, 330],
                   ["Graphics\World\Plat_Brown.png", 110, 40, 2650, 250],
                   ["Graphics\World\Plat_Grey.png", 110, 40, 3025, 350],
                   ["Graphics\World\Plat_Purp.png", 110, 40, 3370, 510],
                   ["Graphics\World\Plat_Green.png", 110, 40, 2925, 180],
                   ["Graphics\World\Plat_Brown.png", 70, 40, 4280, 180],
                   ["Graphics\World\Plat_Brown.png", 30, 20, 5260, 80],
                   ["Graphics\World\Plat_Green.png", 50, 20, 5510, 330],
                   
                    # pildita, pikkus, kõrgus, x, y
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
        
        # käib kõik listi elemendid läbi
        for i in objects:
            item = Wall(i[0],i[1],i[2])
            item.rect.x = i[3]
            item.rect.y = i[4]
            item.player = self.player
            self.wall_list.add(item)
            
        # liikuvad platformid, - pilt, pildi laius, kõrgus ,  x kordinaat, y kordinaat, x limiit, kiirus
        moving_leftright = [["Graphics\World\Log.png", 92, 30, 1676, 552, 1932, 3],
                            ["Graphics\World\Small.png", 55, 25, 3125, 190, 3500, 8],
                            ["Graphics\World\Log.png", 80, 26, 5000, 520, 5200, 2],
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
        
        # üles alla liikuvad platformid, pilt, pildi laius, pildi kõrgus, x kordinaat, y, kordinaat, y lim, kiirus
        moving_updown = [["Graphics\World\Wood.png", 42, 42, 2030, 270, 480, 6,2],
                         ["Graphics\World\Plat_Yellow_spikes.png", 150, 20, 3745, 180, 410, 2,2],
                         ["Graphics\World\Plat_Grey.png", 100, 35, 5350, 120, 335, 2,1],
                         ["Graphics\World\Plat_Grey.png", 100, 35, 5350, 260, 475, 2,1],
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
    
# level 2 platformid
class Level_2(Level):
    def __init__(self, player):
        Level.__init__(self, player)
        # taust
        self.background_1 = pygame.image.load("Graphics/Background/Level 2 Back.png").convert_alpha()
        self.background_2 = pygame.image.load("Graphics/Background/Level 2 Ground.png").convert_alpha()
                    #pilt, laius, kõrgus, x , y
        objects = [[False, 5,500, 0, 0],
                   [False, 5,500, 5970, 0],
                   [False, 1390, 5, 0, 513],
                   [False, 1050, 5, 2916, 513],
                   [False, 197 , 5 , 2698, 313],
                   [False, 5, 140 , 2890, 373],
                   [False, 5, 240 , 2698, 373],
                   [False, 5, 1100, 3995, -500],

                   ["Graphics\World\Plat_dung_1.png", 113, 18, 1150, 320],
                   ]
        
        for i in objects:
            item = Wall(i[0],i[1],i[2])
            item.rect.x = i[3]
            item.rect.y = i[4]
            item.player = self.player
            self.wall_list.add(item)
            
        # liikuvad platformid, - pilt, pildi laius, kõrgus ,  x kordinaat, y kordinaat, x limiit, kiirus
       
        item = Moving_Wall("Graphics\World\Rock4.png", 145,40)
        item.rect.x = 871
        item.rect.y= 450
        item.limit_left = 871
        item.limit_right = 1020
        item.left_right = 5
        item.player = self.player
        item.level = self
        self.wall_list.add(item)
        
        # üles alla liikuvad platformid, pilt, pildi laius, pildi kõrgus, x kordinaat, y, kordinaat, y lim, kiirus
        moving_updown = [["Graphics\World\Spikes.png", 137, 107, 500, 30, 435, 5,2],
                         ["Graphics\World\Spikes.png", 137, 107, 637, 105, 450, 4,2],
                         ["Graphics\World\Spikes.png", 137, 107, 774, 180, 465, 3,2],
                         ["Graphics\World\Plat_dung_1.png", 113, 18, 2200, 200,460,2,2],
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
            
        # langevad platformid
        falling =[["Graphics\World\Plat_dung_2.png", 113, 18, 1300, 200,1,1],
                  ["Graphics\World\Plat_dung_2.png", 113, 18, 1500, 120,1,1],                  
                  ["Graphics\World\Plat_dung_2.png", 113, 18, 1750, 190,2,1],
                  ["Graphics\World\Plat_dung_4.png", 113, 18, 2000, 240,5,2],
                  ["Graphics\World\Plat_dung_4.png", 113, 18, 2400, 440,5,3],
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

# level 3 platformid
class Level_3(Level):
    
    def __init__(self, player):
        Level.__init__(self, player)
        # taustad
        self.background_1 = pygame.image.load("Graphics/Background/Level 3 Back.png").convert_alpha()
        self.background_2 = pygame.image.load("Graphics/Background/Level 3 Ground.png").convert_alpha()
        # loeme pildi ühe korra sisse, et ei peaks uuesti lugema
        self.plat_2 = pygame.image.load("Graphics\World\Plat_dung_2.png").convert_alpha()

                    #pilt, laius, kõrgus, x , y        
        objects = [[False, 5,500, 0, 0],
                   [False, 2308, 5, 0, 500],
                   [False, 400, 5, 2738, 500],
                   [False, 5, 500, 2990, 0],
                   
                   ["Graphics\World\Rock3.png", 150, 20, 390, 320],
                   ["Graphics\World\Rock3.png", 150, 20, 630, 220],
                   ["Graphics\World\Rock3.png", 150, 20, 870, 120],
                   ["Graphics\World\Rock2.png", 48, 174, 972, 326],
                   ["Graphics\World\Rock2.png", 30, 70, 1825, 430],
                   ["Graphics\World\Rock2.png", 30, 113, 2145, 387],
                   ]
        
        for i in objects:
            item = Wall(i[0],i[1],i[2])
            item.rect.x = i[3]
            item.rect.y = i[4]
            item.player = self.player
            self.wall_list.add(item)
            
        # üksik liikuv platform
        item = Moving_Wall("Graphics\World\Plat_dung_3.png", 115, 18)
        item.rect.x = 1100
        item.rect.y= 250
        item.limit_left = 1100
        item.limit_right = 1350
        item.left_right = 5
        item.player = self.player
        item.level = self
        self.wall_list.add(item)

        # langevad platformid
        falling =[["Graphics\World\Plat_dung_3.png", 113, 18, 1550, 120,1,1],
                  ["Graphics\World\Plat_dung_3.png", 113, 18, 1900, 200,1,1],                  
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

    # sein, mis ei lase mängijal bossiga kaklemise ajal ära joosta
    def add_boss_wall(self):
        wall = Wall(False, 5,555)
        wall.rect.x = 2180 + self.world_shift 
        wall.rect.y = 0
        self.wall_list.add(wall)

    # eemaldab ülevaloleva seina
    def remove_boss_wall(self):
        for wall in self.wall_list:
            if wall.rect.height == 555:
                self.wall_list.remove(wall)

    # lisab üles/alla liikuva platformi
    def add_plat_up(self,up_down):
        item = UpDown_Plat("Graphics\World\Plat_dung_3.png", 115, 18)

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
