import pygame

class AllObject(pygame.sprite.Sprite):
    frames = []
    def __init__(self, image_data, width, height, object_type):
        pygame.sprite.Sprite.__init__(self)
        if object_type == 1:
            self.image = pygame.image.load(image_data)
            self.image = pygame.transform.scale(self.image,(width, height))
        elif object_type == 2:
            self.frames.clear()
            for i in range(width):
                self.frames.append(pygame.image.load(image_data + str(i)+ '.png').convert_alpha())
            self.image = self.frames[0]
            self.framelim = height
        self.rect = self.image.get_rect()
        self.framerate = 0
class GameObject(object):
    world_shift = 0
    def __init__(self):
        self.normal_object = pygame.sprite.Group()
        self.moving_object = pygame.sprite.Group()
        #järjekord oluline
        self.layers = pygame.sprite.OrderedUpdates()
    def update(self):
        self.layers.update()
        self.moving_object.update()
        self.normal_object.update()
        for enemy in self.moving_object:
            frame = (enemy.framerate//6 % len(enemy.frames))
            enemy.image = enemy.frames[frame]
            enemy.framerate +=1
            if frame > enemy.framelim:
                self.moving_object.remove(enemy)
                if enemy.type == "bomb":
                    self.explosion()

    def draw(self, screen):
        self.normal_object.draw(screen)
        self.moving_object.draw(screen)
        self.layers.draw(screen)
        
    def shift_world(self,x):
        self.world_shift +=x
        for item in self.layers:
            item.rect.x += x
        for item in self.normal_object:
            item.rect.x += x

class Object_1(GameObject):
    def __init__(self):
        GameObject.__init__(self)
        pass
class Object_2(GameObject):
    def __init__(self):
        GameObject.__init__(self)
        pass    
class Object_3(GameObject):
    def __init__(self):
        GameObject.__init__(self)
        hp = [["boss_hp_back.png", 256, 64,1,1],
              ["boss_hp_fill.png", 226, 64,2,1],
              ["boss_hp.png", 256, 64,3,1],
            ]
        for h in hp:
            health = AllObject(h[0], h[1], h[2], h[4])
            health.rect.x = 2700
            health.rect.y = 20
            health.type = h[3]
            self.layers.add(health)
    def add_pot(self):
        bomb = AllObject('Bird/Pot/frame', 45,43, 2)
        bomb.rect.x = 25
        bomb.rect.y = 405
        bomb.type = "bomb"
        self.moving_object.add(bomb)
    def explosion(self):
        exp = AllObject('Bird/Explosion/frame', 19, 17, 2)
        exp.rect.x = -10
        exp.rect.y = 340
        exp.type = "exp"
        self.moving_object.add(exp)
    def add_head(self):
        head = AllObject('Bird/Horsehead.png',224,189, 1)
        head.rect.x = self.world_shift + 2755
        head.rect.y = 320
        self.normal_object.add(head)
        
