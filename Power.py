import pygame

f = open("clean.txt")
joke_clean = []
punchline_clean = []
for rida in f:
    joke_clean.append(rida.split("/")[0].strip())
    punchline_clean.append(rida.split("/")[1].strip())
f.close()

f = open("both.txt")
joke_both = []
punchline_both = []
for rida in f:
    joke_both.append(rida.split("/")[0].strip())
    punchline_both.append(rida.split("/")[1].strip())
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
    def __init__(self,filename):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(filename).convert_alpha()
        self.rect = self.image.get_rect()
        self.type = filename

class Powerlvl():
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
            
    def joke_joke_clean(self,screen, joke_nr):
        joke_font = joke_font_size(joke_clean, joke_nr)
        jokefont = pygame.font.Font('norwester.otf', joke_font)
        text_x = 400 - jokefont.size(joke_clean[joke_nr])[0]/2
        return joke_clean[joke_nr], text_x , jokefont
    
    def joke_punch_clean(self,screen, joke_nr):
        joke_font = joke_font_size(punchline_clean, joke_nr)
        jokefont = pygame.font.Font('norwester.otf', joke_font)
        text_x = 400 - jokefont.size(punchline_clean[joke_nr])[0]/2
        return punchline_clean[joke_nr], text_x , jokefont
    
    def joke_joke_both(self,screen, joke_nr):
        joke_font = joke_font_size(joke_both, joke_nr)
        jokefont = pygame.font.Font('norwester.otf', joke_font)
        text_x = 400 - jokefont.size(joke_both[joke_nr])[0]/2
        return joke_both[joke_nr], text_x , jokefont
    def joke_punch_both(self,screen, joke_nr):
        joke_font = joke_font_size(punchline_both, joke_nr)
        jokefont = pygame.font.Font('norwester.otf', joke_font)
        text_x = 400 - jokefont.size(punchline_both[joke_nr])[0]/2
        return punchline_both[joke_nr], text_x , jokefont
    def add_joke(self,x,y):
        power = PowerUp('Paper.png')
        power.rect.x = x + self.world_shift
        power.rect.y = y 
        power.player = self.player  
        self.power_list.add(power)
        
class Power_1(Powerlvl):
    def __init__(self, player):
        Powerlvl.__init__(self,player)
        # powerupid pilt, x-kord, y-kord, 
        powerjokes = [[1110, 265,'Paper.png'],
                    [3053, 312,'Paper.png'],
                    [4000, 180,'Paper.png'],
                    [2023, 440,'Paper.png'],
                    [1820,190, 'Star2.png'],
                    [4290,140, 'Star2.png'],
                    [5253,40,  'Star2.png'],
                    [3405, 477, 'Orb.png'],
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
                      [1185, 280,'Paper.png'],
                      [2230, 100,'Paper.png'],
                      [3600, 300,'Paper.png'],
                      
                      [ 370, 220,'Star2.png'],
                      [2035, 440,'Star2.png'],
                      [3600, 300,'Star2.png'],
                    
                      [2745, -55,'Orb.png'],
                    ]
        for item in powerjokes:
            power = PowerUp(item[2])
            power.rect.x = item[0]
            power.rect.y = item[1]
            power.player = self.player  
            self.power_list.add(power)
class Power_3(Powerlvl):
    def __init__(self, player):
        Powerlvl.__init__(self,player)
        # powerupid pilt, x-kord, y-kord, 
        powerjokes = [
                      [440, 280,'Paper.png'],
                      [972, 280,'Paper.png'],
                      [1580, 75,'Paper.png'],
                      [1935, 160,'Orb.png'],
                      [2922, 465, 'Burger.png'],
                      ]
        for item in powerjokes:
            power = PowerUp(item[2])
            power.rect.x = item[0]
            power.rect.y = item[1]
            power.player = self.player  
            self.power_list.add(power)
