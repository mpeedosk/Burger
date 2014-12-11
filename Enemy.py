import pygame
from random import randint
# vastastega seotud koodid ja värgid
"""
enemy types
1 = chicken
2 = snail
3 = bat
4 = rock
5 = axe
6 = fox
7 = spike
"""
# vastaste alusklass, kus kõik tulenevad
class Enemy_stats(pygame.sprite.Sprite):
    
    # listid animatsiooni kaadrite jaoks, lendavad vastased
    flyright = []
    flyleft = []
    # listid kõndivatele vastastele
    moveright = []
    moveleft = []
    # bossi kaadrid
    boss = []
    # muutuja playerile, et erinevad sprited saavad omavahel suhelda, hiljem vaja
    player = None
    #konstruktor, parameetrid on x ja y kordinaadid, vastaste tüüp, vasakule ja paremale liikumise limiit, kiirus
    
    def __init__(self, x, y, enemy_type, limit_left, limit_right, speed):
        #käivitab sprite
        pygame.sprite.Sprite.__init__(self)
        # level 1 vastased
        if enemy_type == 1:
            # teeb listi tühjaks, kui eelmisest kutsumisest kaadrid alles jäid
            self.flyright.clear()
            self.flyleft.clear()
            # laeb 9 pilti ja konverteerib ära paremaks formaadiks
            for i in range(9):
                self.flyright.append(pygame.image.load('Graphics/Enemy/Level 1/Chicken/frame' + str(i)+ '.png').convert_alpha())
            for i in range(9):
                # pöörab pildid ümber, vasakule/paremale liikumine
                self.flyleft.append(pygame.transform.flip(pygame.image.load('Graphics/Enemy/Level 1/Chicken/frame' + str(i)+ '.png'), True, False)) # True vertikaalne pööramine, false horisontaalne
            # sprite imagiks võtab listi esimese elemendi
            self.image = self.flyleft[0]
            
        # teised on analoogsed esimesega    
        elif enemy_type == 2:
            self.moveleft.clear()
            self.moveright.clear()
            for i in range(12):
                self.moveleft.append(pygame.image.load('Graphics/Enemy/Level 1/Snail/frame' + str(i)+ '.png').convert_alpha())
            for i in range(12):
                self.moveright.append(pygame.transform.flip(pygame.image.load('Graphics/Enemy/Level 1/Snail/frame' + str(i)+ '.png'), True, False))
            self.image = self.moveleft[0]
            
        # level 2 vastased
        elif enemy_type == 3:
            self.flyright.clear()
            self.flyleft.clear()
            for i in range(9):
                self.flyright.append(pygame.image.load('Graphics/Enemy/Level 2/Butterbat/frame' + str(i)+ '.png').convert_alpha())
            for i in range(9):
                self.flyleft.append(pygame.transform.flip(pygame.image.load('Graphics/Enemy/Level 2/Butterbat/frame' + str(i)+ '.png'), True, False))
            self.image = self.flyright[0]
            
        elif enemy_type ==4:
            self.moveleft.clear()
            self.moveright.clear()
            for i in range(9):
                self.moveleft.append(pygame.image.load('Graphics/Enemy/Level 2/Rock/frame' + str(i)+ '.png').convert_alpha())
            for i in range(9):
                self.moveright.append(pygame.transform.flip(pygame.image.load('Graphics/Enemy/Level 2/Rock/frame' + str(i)+ '.png'), True, False))
            self.image = self.moveleft[0]
            
        # level 3 vastased
        elif enemy_type == 5:
            self.flyright.clear()
            self.flyleft.clear()
            for i in range(6):
                self.flyright.append(pygame.image.load('Graphics/Enemy/Level 3/Axe/frame' + str(i)+ '.png').convert_alpha())
            self.flyleft = self.flyright
            self.image = self.flyright[0]
            
        elif enemy_type == 6:
            self.moveleft.clear()
            self.moveright.clear()
            for i in range(6):
                self.moveleft.append(pygame.image.load('Graphics/Enemy/Level 3/SilverFox/frame' + str(i)+ '.png').convert_alpha())
            for i in range(6):
                self.moveright.append(pygame.transform.flip(pygame.image.load('Graphics/Enemy/Level 3/SilverFox/frame' + str(i)+ '.png'), True, False))
            self.image = self.moveleft[0]
        # orade jaoks on ainult vaja ühte pilti
        elif enemy_type == 7:
            self.image = pygame.image.load("Graphics/World/Spike.png").convert_alpha()
        # bossi jaoks ei ole vaja ümberpööratud versiooni
        else:
            for i in range(51):
                self.boss.append(pygame.image.load('Graphics/Enemy/Level 3/Boss/frame' + str(i)+ '.png').convert_alpha())
            self.image = self.boss[0]
        # annab igale spritele omad muutujad
        self.type = enemy_type
        self.rect = self.image.get_rect()
        # loendur kaadrite jaoks
        self.framerate = 0
        self.rect.x = x
        self.rect.y = y
        self.limit_left = limit_left
        self.limit_right= limit_right
        self.speed = speed
        
# klass vastaste uuendamiseks ja funktsioonide määramiseks    
class Enemy(object):
    
    # näitab kui palju maailm on nihkunud
    world_shift = 0
    limit_left=0
    limit_right=0
    
    def __init__(self, player):

        #tekitab grupid
        self.enemy_flying = pygame.sprite.Group()
        self.enemy_ground = pygame.sprite.Group()
        self.spike_list = pygame.sprite.Group()
        self.boss = pygame.sprite.Group()
        self.player = player

    # uuendab vastaseid
    # parameetrid on mängija x ja y kordinaadid
    def update(self, px, py):
        # uuendab sprite gruppe
        self.enemy_flying.update()
        self.enemy_ground.update()
        # tsükkel vastaste asukoha muumiseks
        for enemy in self.enemy_flying:
            # kui vastane on ekraanist liiga palju välja läinud, eemaldatakse ta ära
            if enemy.rect.x < -1000:
                self.enemy_flying.remove(enemy)
                
            # olenevalt vastaste tüübist määrab liikumise kiiruse
            if enemy.type == 1 or enemy.type == 3: # kui on tegemist kana või nahkhiirega
                speedy = 5
                # horisontaalne liikumine mängija suhtes
                # kui vastane on vasakul pool ekraani 
                if enemy.rect.x -px < -50:
                    enemy.rect.x += 5
                # kui vastane on paremal pool ekraani
                elif enemy.rect.x-px > 10:
                    enemy.rect.x -= 3                 
            else: # kirves
                speedy = 4
                enemy.rect.x -= 4
                
            # vertikaalne liikumine
            if enemy.rect.y - py < -10:
                enemy.rect.y +=speedy
            elif enemy.rect.y - py > 0:
                enemy.rect.y -=speedy
            # olenevalt kummal pool vastane on, võtab vastavad kaadrid    
            if enemy.rect.x < px:
                frame = (enemy.framerate//3 % len(enemy.flyright))
                enemy.image = enemy.flyright[frame]
            else:
                frame = (enemy.framerate//3 % len(enemy.flyleft))
                enemy.image = enemy.flyleft[frame]
            # iga tsükkel suurendab kaadrite loendurit
            enemy.framerate +=1
            
        # maas liikuvad vastased, toimub ainult horisontaalne liikumine
        for enemy in self.enemy_ground:
            # uuendab positsiooni
            enemy.rect.x += enemy.speed
            # positsioon koos maailma nihkega
            pos = enemy.rect.x - self.world_shift
            # kui on limiidini jõudnud, siis pöörab ennast ümber
            if pos < enemy.limit_left or pos > enemy.limit_right:
                enemy.speed *=-1
            # vastavalt sellele, kas kiirus on positiivne või negatiivne, määrab ära kummad kaadrid kuvada
            if enemy.speed > 0:
                frame = (enemy.framerate//6 % len(enemy.moveright))
                enemy.image = enemy.moveright[frame]
            else:
                frame = (enemy.framerate//6 % len(enemy.moveleft))
                enemy.image = enemy.moveleft[frame]
            # suurendab loendurit
            enemy.framerate +=1
        # ogad, toimub ainult vertikaalne liikumine
        for spike in self.spike_list:
            spike.rect.y += spike.speed
            # kui kiirus on alla 2.5, siis on kiirendus aeglasem
            if spike.speed < 2.5:
                spike.speed += 0.05
            # kui üle siis hakkab järjest kiiremini kukkuma
            else: spike.speed += 0.15
            # kui jõuab piisavalt alla, eemaldab ennast listist
            if spike.rect.y > 500:
                self.spike_list.remove(spike)
        # bossi uuendamie
        for boss in self.boss:
            frame = (boss.framerate//6 % len(boss.boss))
            boss.image = boss.boss[frame]
            boss.framerate += 1

    # method maailma nihkeks
    def shift_world(self, x):
        # vastavalt x-le liigutab kõiki listides olevaid elemente teatud kordinaatide võrra
        self.world_shift += x
        for enemy in self.enemy_flying:
            enemy.rect.x +=x
        for enemy in self.enemy_ground:
            enemy.rect.x +=x
        for enemy in self.boss:
            enemy.rect.x +=x
        for spike in self.spike_list:
            spike.rect.x +=x
            
    # kuvab kõikide listide sisu ekraanile
    def draw(self, screen):
        self.enemy_ground.draw(screen)
        self.enemy_flying.draw(screen)
        self.boss.draw(screen)
        self.spike_list.draw(screen)

# iga leveli vastased eraldi

class Enemy_1(Enemy):
    
    def __init__(self, player):
        Enemy.__init__(self, player)

    # vastased, kes leveli vahetades muutuvad
    def add_ground_enemy(self):
        # listide list vastastest
        # x-kodrinaat, y-kordinaat, vasak limiit, parem limiit, kiirus
        snails = [[1250,450,1250,1600,2],
                  [2073,450,2073,3071,8],
                  [4157,380,4157,4320,1],
                  [4525,312,4365,4531,1],
                  [4563,240,4563,4729,1],
                  [4936,170,4776,4940,1],
                  [5800,450,5720,5920,3],
                  ]
        # käib listi iga elemendi läbi ja kutsub baaskonstruktori välja
        for snail in snails:
            enemy = Enemy_stats(snail[0], snail[1], 2 , snail[2],snail[3], snail[4])
            self.enemy_ground.add(enemy) # lisab tekitatud sprite listi

    # vastased, kes tulevad jooksvalt juurde, ehk lendavad vastased
    def add_enemy(self):
        # sättestan piirkonnad, kuhu vastane võib tekkida
        spawn_limit_x = [(-600, self.player.rect.x-500)] # erilist mõtet praegu pole sellel, kuid kui tahan piirkondi lisada, tuleks lihtsalt listi muuta
        spawn_limit_y = [(-600, 300)] 
        spawn_x = spawn_limit_x[0] # samuti praegu mõtet ei ole, kuid kui tahan mitut piirkonda määrata siis pean ühe valima
        spawn_y = spawn_limit_y[0]
        self.enemy_flying.add(Enemy_stats(randint(spawn_x[0], spawn_x[1]), randint(spawn_y[0], spawn_y[1]), 1,0,0,0))# randintiga valib tekkimis x ja y kordinaadid
# ülejäänud levelid analoogsed 1. leveliga

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
        # laen alguses pildi ühe korra ära, pole mõttet mitu korda sama pilti laadida
        self.spike_img = pygame.image.load("Graphics/World/Spike.png").convert_alpha()
        
    def add_ground_enemy(self):
        # liikuvad rebased - x-kordinaat, y-kordinaat,  vasak limiit, parem limiit, kiirus
        foxy = [[300, 450 , 170,550,3],
                [1220, 450 , 1020, 1675,3],
                [1520, 450 , 1020, 1675,3],
                [1220, 450 , 1020, 1675,5],
                [1520, 450 , 1020, 1675,5],
                [2000, 450 , 1845, 2005,3],
                [1850, 450 , 1845, 2005,3],
                 ]
        for fox in foxy:
            enemy = Enemy_stats(fox[0], fox[1], 6 , fox[2], fox[3], fox[4])
            self.enemy_ground.add(enemy)
            
    # bossi kirved
    def boss_axe_throw(self):
        self.enemy_flying.add(Enemy_stats(2703 + self.world_shift, 330, 5,0,0,0))
        
    # ora lisamine
    def add_enemy(self):
        self.spike_list.add(Enemy_stats(randint(200, 750), -77, 7, 0,0,0))
        
    # bossi lisamine
    def add_boss(self):
        self.boss.add(Enemy_stats(2670 + self.world_shift, 180, "boss" , 0,0, 0))
