import pygame
from random import randint
# types
# bird = 1
# snail = 2
class Enemy_stats(pygame.sprite.Sprite):
    flyright = []
    flyleft = []
    moveright = []
    moveleft = []
    boss = []
    player = None
    def __init__(self, x, y, enemy_type, limit_left, limit_right, speed):
        pygame.sprite.Sprite.__init__(self)
        # level 1 vastased
        if enemy_type == 1:
            for i in range(9):
                self.flyright.append(pygame.image.load('Bird/Chicken/frame' + str(i)+ '.png').convert_alpha())
            for i in range(9):
                self.flyleft.append(pygame.transform.flip(pygame.image.load('Bird/Chicken/frame' + str(i)+ '.png'), True, False))
            self.image = self.flyleft[0]
        elif enemy_type == 2:
            for i in range(12):
                self.moveleft.append(pygame.image.load('Bird/Snail/frame' + str(i)+ '.png').convert_alpha())
            for i in range(12):
                self.moveright.append(pygame.transform.flip(pygame.image.load('Bird/Snail/frame' + str(i)+ '.png'), True, False))
            self.image = self.moveleft[0]
            
        # level 2 vastased
        elif enemy_type == 3:
            self.flyright.clear()
            self.flyleft.clear()
            for i in range(9):
                self.flyright.append(pygame.image.load('Bird/Butterbat/frame' + str(i)+ '.png').convert_alpha())
            for i in range(9):
                self.flyleft.append(pygame.transform.flip(pygame.image.load('Bird/Butterbat/frame' + str(i)+ '.png'), True, False))
            self.image = self.flyright[0]
        elif enemy_type ==4:
            self.moveleft.clear()
            self.moveright.clear()
            for i in range(9):
                self.moveleft.append(pygame.image.load('Bird/Rock/frame' + str(i)+ '.png').convert_alpha())
            for i in range(9):
                self.moveright.append(pygame.transform.flip(pygame.image.load('Bird/Rock/frame' + str(i)+ '.png'), True, False))
            self.image = self.moveleft[0]
            
        # level 3 vastased
        elif enemy_type == 5:
            self.flyright.clear()
            self.flyleft.clear()
            for i in range(6):
                self.flyright.append(pygame.image.load('Bird/Axe/frame' + str(i)+ '.png').convert_alpha())
            self.flyleft = self.flyright
            self.image = self.flyright[0]
            
        elif enemy_type == 6:
            self.moveleft.clear()
            self.moveright.clear()
            for i in range(6):
                self.moveleft.append(pygame.image.load('Bird/SilverFox/frame' + str(i)+ '.png').convert_alpha())
            for i in range(6):
                self.moveright.append(pygame.transform.flip(pygame.image.load('Bird/SilverFox/frame' + str(i)+ '.png'), True, False))
            self.image = self.moveleft[0]
        else:
            for i in range(51):
                self.boss.append(pygame.image.load('Bird/Boss/frame' + str(i)+ '.png').convert_alpha())
            self.image = self.boss[0]
        self.type = enemy_type
        self.rect = self.image.get_rect()
        self.framerate = 0
        self.rect.x = x
        self.rect.y = y
        self.limit_left = limit_left
        self.limit_right= limit_right
        self.speed = speed
        
class Enemy(object):
    world_shift = 0
    limit_left=0
    limit_right=0
    def __init__(self, player):
        self.enemy_flying = pygame.sprite.Group()
        self.enemy_ground = pygame.sprite.Group()
        self.boss = pygame.sprite.Group()
        self.player = player

    def update(self, px, py):
        self.enemy_flying.update()
        self.enemy_ground.update()
        for enemy in self.enemy_flying:

                #or enemy.rect.x >1500
                if enemy.rect.x < -600:
                    self.enemy_flying.remove(enemy)
                if enemy.type == 3:
                    speedy = 2
                    if enemy.rect.x -px < -50:
                        enemy.rect.x += 3
                    elif enemy.rect.x-px > 10:
                        enemy.rect.x -= 3                   
                else:
                    speedy = 4
                    enemy.rect.x -= 5                  

                if enemy.rect.y - py < -10:
                    enemy.rect.y +=speedy
                elif enemy.rect.y - py > 0:
                    enemy.rect.y -=speedy
                    
                if enemy.rect.x < px:
                    frame = (enemy.framerate//3 % len(enemy.flyright))
                    enemy.image = enemy.flyright[frame]
                else:
                    frame = (enemy.framerate//3 % len(enemy.flyleft))
                    enemy.image = enemy.flyleft[frame]
                enemy.framerate +=1
        for enemy in self.enemy_ground:
                enemy.rect.x += enemy.speed
                pos = enemy.rect.x - self.world_shift
                if pos < enemy.limit_left or pos > enemy.limit_right:
                    enemy.speed *=-1
                    
                if enemy.speed > 0:
                    frame = (enemy.framerate//6 % len(enemy.moveright))
                    enemy.image = enemy.moveright[frame]
                else:
                    frame = (enemy.framerate//6 % len(enemy.moveleft))
                    enemy.image = enemy.moveleft[frame]
                enemy.framerate +=1
        for boss in self.boss:
            frame = (boss.framerate//6 % len(boss.boss))
            boss.image = boss.boss[frame]
            boss.framerate += 1              
    def shift_world(self, x):
        self.world_shift += x
        for enemy in self.enemy_flying:
            enemy.rect.x +=x
        for enemy in self.enemy_ground:
            enemy.rect.x +=x
        for enemy in self.boss:
            enemy.rect.x +=x
    def draw(self, screen):
        self.enemy_ground.draw(screen)
        self.enemy_flying.draw(screen)
        self.boss.draw(screen)
class Enemy_1(Enemy):
    def __init__(self, player):
        Enemy.__init__(self, player)
        # liikuvad teod  - x-kordinaat, y-kordinaat, limiit-left, limiit-right, kiirus
    def add_ground_enemy(self):
        snails = [[1250,450,1250,1600,2],
                  [2073,450,2073,3071,8],
                  [4157,380,4157,4320, 1],
                  [4525,312,4365,4531,1],
                  [4563,240,4563,4729,1],
                  [4936,170,4776,4940,1],
                  [5800,450,5720,5920,3],

                  ]
        for snail in snails:
            enemy = Enemy_stats(snail[0], snail[1], 2 , snail[2],snail[3], snail[4])
            self.enemy_ground.add(enemy)
    def add_enemy(self):
        spawn_limit_x = [(-600, self.player.rect.x-500),(self.player.rect.x+400, 1400)]
        spawn_limit_y = [(-200, 300)]
        spawn_x = spawn_limit_x[randint(0,1)]
        spawn_y = spawn_limit_y[0]
        self.enemy_flying.add(Enemy_stats(randint(spawn_x[0], spawn_x[1]), randint(spawn_y[0], spawn_y[1]), 1,0,0,0))

class Enemy_2(Enemy):
    def __init__(self,player):
        Enemy.__init__(self,player)
    def add_ground_enemy(self):
        rocky = [[3000,225,1140,1350,5],
                     [3000,415,1920,2130,5],
                     # 1 rida
                     [2900,420,2900,3120,3],
                     [2900,420,3120,3340,3],
                     [2900,420,3340,3560,3],
                     [2900,420,3560,3780,3],

                     # 2 rida
                     [3000,340,3010,3230,3],
                     [3000,340,3230,3450,3],
                     [3000,340,3450,3670,3],
                     [3000,340,3670,3890,3],

                     # 3 rida
                     [2900,260,3120,3340,3],
                     [2900,260,3340,3560,3],
                     [2900,260,3560,3780,3],
                     # 4 rida
                     [3000,180,3230,3450,3],
                     [3000,180,3450,3670,3],
                     [3000,180,3670,3890,3],
                     # 5 rida
                     [2900,100,3340,3560,3],
                     [2900,100,3560,3780,3],
                     # 6 rida
                     [3000,20,3450,3670,3],
                     [3000,20,3670,3890,3],
                     ]
        for rock in rocky:
            enemy = Enemy_stats(rock[2], rock[1], 4 , rock[2],rock[3], rock[4])
            self.enemy_ground.add(enemy)

            
    def add_enemy(self):
        spawn_limit_x = [(-600, self.player.rect.x-500)]
        spawn_limit_y = [(-200, 300)]
        spawn_x = spawn_limit_x[0]
        spawn_y = spawn_limit_y[0]
        self.enemy_flying.add(Enemy_stats(randint(spawn_x[0], spawn_x[1]), randint(spawn_y[0], spawn_y[1]), 3,0,0,0))        

class Enemy_3(Enemy):
    def __init_(self,player):
        Enemy.__init__(self,player)
    def add_ground_enemy(self):
        # liikuvad teod  - x-kordinaat, y-kordinaat, limiit-left, limiit-right, kiirus
        foxy = [[300, 450 , 170,550,3],
                 ]
        for fox in foxy:
            enemy = Enemy_stats(fox[0], fox[1], 6 , fox[2], fox[3], fox[4])
            self.enemy_ground.add(enemy)
    def boss_axe_throw(self):
        self.enemy_flying.add(Enemy_stats(2703 + self.world_shift, 330, 5,0,0,0))          
    def add_enemy(self):
        enemy = Enemy_stats(2670, 180, "boss" , 0,0, 0)
        self.boss.add(enemy)
