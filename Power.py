import pygame
f = open("naljad.txt")
joke = []
punchline = []
for rida in f:
    joke.append(rida.split("/")[0].strip())
    punchline.append(rida.split("/")[1].strip())
f.close()

def joke_font_size(jokelist, joke_nr):
    jokelenght = len(jokelist[joke_nr])
    if jokelenght <= 30:
        joke_size = 33
    if jokelenght <= 40:
        joke_size = 30
    elif jokelenght <= 50:
        joke_size = 28
    elif jokelenght <= 60:
        joke_size = 26
    elif jokelenght <=65:
        joke_size = 24
    elif jokelenght <= 72:
        joke_size = 22
    elif jokelenght <=80:
        joke_size = 20
    else:
        joke_size = 16
    return joke_size

class PowerUp(pygame.sprite.Sprite):
    def __init__(self, powertype):
        pygame.sprite.Sprite.__init__(self)
        if powertype == 1:
            self.image = pygame.image.load('Paper.png').convert_alpha()
        elif powertype == 2:
            self.image = pygame.image.load('Star2.png').convert_alpha()
        elif powertype == 3:
            self.image = pygame.image.load('Orb.png').convert_alpha()
        elif powertype == 4:
            self.image = pygame.image.load('Lever_Right.png').convert_alpha()
        elif powertype == 5:
            self.image = pygame.image.load('Lever_Left.png').convert_alpha()

        self.rect = self.image.get_rect()
        self.type = powertype

class Powerlvl(object):
    world_shift = 0
    def __init__(self, player):
        self.power_list = pygame.sprite.Group()
        self.player = player
    def update(self):
        self.power_list.update()
    def draw(self,screen):
        self.power_list.draw(screen)
    def shift_world(self,x):
        self.world_shift+=x
        for power in self.power_list:
            power.rect.x += x
    def joke_joke(self,screen, joke_nr):
            joke_font = joke_font_size(joke, joke_nr)
            jokefont = pygame.font.Font('norwester.otf', joke_font)
            text_x = 400 - jokefont.size(joke[joke_nr])[0]/2
            return joke[joke_nr], text_x , jokefont
    def joke_punch(self,screen, joke_nr):
            joke_font = joke_font_size(punchline, joke_nr)
            jokefont = pygame.font.Font('norwester.otf', joke_font)
            text_x = 400 - jokefont.size(punchline[joke_nr])[0]/2
            return punchline[joke_nr], text_x , jokefont
class Power_1(Powerlvl):
    def __init__(self, player):
        Powerlvl.__init__(self,player)
        # powerupid pilt, x-kord, y-kord, 
        powerjokes = [[1110, 265, 1],
                    [3053, 312, 1],
                    [4000, 180, 1],
                    [2023, 440, 1],
                    [1820,190, 2],
                    [4290,140, 2],
                    [5253,40,  2],
                    [3405, 477, 3],
                    ]
        
        for item in powerjokes:
            power = PowerUp(item[2])
            power.rect.x = item[0]
            power.rect.y = item[1]
            power.player = self.player  
            self.power_list.add(power)
            
class Power_2(Powerlvl):
    
    def __init__(self, player):
        Powerlvl.__init__(self,player)
        # powerupid pilt, x-kord, y-kord, 
        powerjokes = [
                      [1185, 280, 1],
                      [2230, 100, 1],
                      [3600, 300, 1],
                      
                      [ 370, 220, 2],
                      [2035, 440, 2],
                      [3600, 300, 2],
                    
                      [2745, -55, 3],
                      
                      [3945, 445, 4],
                    ]
        for item in powerjokes:
            power = PowerUp(item[2])
            power.rect.x = item[0]
            power.rect.y = item[1]
            power.player = self.player  
            self.power_list.add(power)
class Power_3(Powerlvl):
    pass
