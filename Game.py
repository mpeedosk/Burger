import pygame
from pygame.locals import *
from random import randint
from Player import *    
from Wall import *
from Enemy import*
from Power import *
from GameObjects import *

# konstandid
gamewidth = 800     # ekraani laius x
gameheight = 600    # ekraani kõrgus y
def heli_level(level_nr):
        global enemy_ground_wav, enemy_flying_wav, walking
        enemy_ground_wav = pygame.mixer.Sound('Sound\\Level ' + str(level_nr+1)+ '\crack.wav')
        enemy_flying_wav = pygame.mixer.Sound('Sound\\Level ' + str(level_nr+1)+ '\Bird.ogg')
        walking = pygame.mixer.Sound('Sound\\Level ' + str(level_nr+1)+ '\Right_left.wav')
        pygame.mixer.music.load('Sound/Level ' + str(level_nr+1)+ '/Theme.ogg')
        #pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.6)
        walking.set_volume(0.6)
def level_shift(current_level_nr):
   pass 
def game():
    pygame.init()
    running = True
    pygame.display.set_caption("Mäng") # mängu nimi
    time = pygame.time.Clock()
    screen = pygame.display.set_mode((gamewidth, gameheight))
    cursor = pygame.image.load('Crosshair.png').convert_alpha()

    # game over
    fontbig = pygame.font.Font(None, 92)
    game_over = fontbig.render("Game Over" , True, (0,0,0))

    # joke variables
    joketime = False
    pygame.mouse.set_visible(False)                     #Peidab hiire noole ära
    
    # graafika
    countdown = []
    star_png = []
    for i in range(10):
        countdown.append(pygame.image.load('Numbers/Nr'+str(i)+'.png').convert_alpha())
    for i in range(4):
        star_png.append(pygame.image.load('Bird\Stars\Star'+ str(i)+ '.png').convert_alpha())
    mustascheright = pygame.image.load('Stache5.png').convert_alpha()
    mustascheleft = pygame.image.load('Stache55.png').convert_alpha()
    player_dead = pygame.image.load('Bird/Masked/Dead2.png').convert_alpha()
    level_1_logo = pygame.image.load('Level3.png').convert_alpha()
    boss_hp_bar = pygame.image.load('boss_hp.png').convert_alpha()
    boss_hp_bar_back = pygame.image.load('boss_hp_back.png').convert_alpha()
    
    #heliefektid
    #pygame.mixer.music.load('Sound\Level 1\RPG theme.ogg')
    #pygame.mixer.music.load('Sound/Level 2/Too-Quiet.ogg')
    #pygame.mixer.music.play(-1)
    #pygame.mixer.music.set_volume(0.6)
    # world 
    joke_wav = pygame.mixer.Sound('Sound\\World\Joke2.wav')
    book_wav =  pygame.mixer.Sound('Sound\\World\Book2.wav')
    star_wav = pygame.mixer.Sound('Sound\\World\Star.wav')
    death_wav = pygame.mixer.Sound('Sound\\World\death.wav')
    death_wav_2 = pygame.mixer.Sound('Sound\\World\die2.wav')
    invinc_hit_wav = pygame.mixer.Sound('Sound\\World\swosh.wav')
    invinc_wav = pygame.mixer.Sound('Sound\\World\Coolio.wav')
    # level 1 helid

    # level 2 helid
    ghost_wav = pygame.mixer.Sound('Sound\\Level 2\Isee.wav')
    #walking = pygame.mixer.Sound('Sound\\Level 2\Right_left.wav')


    
    # player sprite loomine
    player_sprite = pygame.sprite.Group()
    player = Player()
    
    # powerupid
    power_level = []
    power_level.append(Power_1(player))
    power_level.append(Power_2(player))
    power_level.append(Power_3(player))

    stars = 3
    
    #seinad ja platformid
    levels = []
    levels.append(Level_1(player))
    levels.append(Level_2(player))
    levels.append(Level_3(player))
    world_shift = True
    
    # igasugused objectid jne
    objects_level = []
    objects_level.append(Object_1())
    objects_level.append(Object_2())
    objects_level.append(Object_3())
    
    #vastased
    enemy_level = []
    enemy_level.append(Enemy_1(player))
    enemy_level.append(Enemy_2(player))
    enemy_level.append(Enemy_3(player))
    spawn_timer = pygame.time.get_ticks()
    cooldown = 2500
    enemy_count = 0
    boss_hp = 226

    # praegune level
    level_shift = False
    ghost_sound = True
    level_limit = [-5170,-3200,-2190]
    current_level_nr = 1
    current_level = levels[current_level_nr]
    current_enemy = enemy_level[current_level_nr]
    current_power = power_level[current_level_nr]
    current_objects = objects_level[current_level_nr]
    current_enemy.add_ground_enemy()
    plat_up_time = pygame.time.get_ticks()
    enemy_level[2].add_enemy()

    #player
    living = True
    mustache = False
    player.rect.x = 3000
    player.rect.y = 400
    player_sprite.add(player) 
    heli_level(current_level_nr)
    player.level = current_level
    boss_shift = False
    boss_not_added = True
    pause = False
    boss_pause = False
    dmg_boss = False
    boss_living = True
    bomb_counter = 0
    while running:
        for event in pygame.event.get(): # Vaatab millise eventiga parajasti teguon
            if event.type == pygame.QUIT: # kui vajutatakse üleval X siis läheb tsükkel kinni
                running = False
            elif event.type == KEYDOWN: # kui hoida klahvi all, siis object liigub
                if event.key == K_p:
                    if pause:
                        pause = False
                    else:
                        pause = True
                elif event.key == K_RIGHT or event.key == K_d: # liigub paremale
                    if player.left_right == 0:
                        player.direction = "R"
                    player.move(6)
                    walking.play(-1)

                elif event.key == K_LEFT or event.key == K_a: # liigub vasakule
                    if player.left_right == 0:
                        player.direction = "L"
                    player.move(-6)
                    walking.play(-1)
                
                elif event.key == K_DOWN:
                   # current_enemy.boss_axe_throw()
                   # current_level.remove_boss_wall()

                    player.rect.y = -50
                    player.rect.x += 10
                elif event.key == K_SPACE or event.key == K_UP or event.key == K_w:
                    player.jump()
            elif event.type == KEYUP: # kui klahv üles tõuseb, siis liikumine lõppeb.  Esimese argumendi negatiivne vaste, et summa oleks 0
                if event.key == K_RIGHT or event.key == K_d: # lõpetab paremale liikumise
                    player.move(-6)
                    walking.stop()
                elif event.key == K_LEFT or event.key ==K_a: # lõpetab vasakule liikumise
                    player.move(6)
                    walking.stop()
                elif event.key == K_DOWN:
                        pass
            elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                    #current_level.updatehp(boss_hp)
                #print(cx,cy)
                if cx in range(590,675) and cy in range(236,320): 
                    dmg_boss = True
                for enemy in current_enemy.enemy_flying:
                    if enemy.rect.collidepoint((cx, cy)):
                        enemy_flying_wav.play()
                        current_enemy.enemy_flying.remove(enemy)
        if not pause:
            if not boss_pause:
                #--- event lõpp ---
                if pygame.time.get_ticks() - spawn_timer >= cooldown:
                    if current_level_nr == 0:   
                        current_enemy.add_enemy()
                    elif current_level_nr == 1:
                        if current_level.world_shift > -2300:
                            current_enemy.add_enemy()
                    else:
                        if boss_not_added:
                          #  current_enemy.add_enemy()
                            boss_not_added = False
                    spawn_timer = pygame.time.get_ticks()
                if current_objects.joke:
                    current_objects.joke = False
                    current_power.add_joke(2230, 437)
                # Collision kontroll
                power_collide = pygame.sprite.spritecollide(player, current_power.power_list, True)
                for collide in power_collide:
                    if collide.type == 'Paper.png':
                        book_wav.play()
                        joke_play = True
                        when_joke = pygame.time.get_ticks()
                        joke_nr = randint(0,115)
                        joke1, text_x1, jokefont1 = current_power.joke_joke(screen, joke_nr,)
                        joke2, text_x2, jokefont2= current_power.joke_punch(screen, joke_nr)
                        joke11 = jokefont1.render(joke1, True, (0,0,0))
                        joke22 = jokefont2.render(joke2, True, (0,0,0))
                        if len(joke1)< 68: y1=2
                        else: y1 = 1
                        if len(joke2)< 68: y2=2
                        else: y2 = 1
                        joketime = True
                    elif collide.type == 'Star2.png':
                        stars += 1
                        star_wav.play()
                    elif collide.type == 'Orb.png':
                        invinc_wav.play()
                        mustache = True
                        when_stache = pygame.time.get_ticks()
                    else:
                        current_enemy.enemy_ground.empty()
                object_collide = pygame.sprite.spritecollide(player, current_objects.moving_object, False)
                for item in object_collide:
                    if item.type == "exp":
                        living = False
                        deadx = px
                        deady = py
                if current_level_nr !=2:
                    enemy_collide_flying = pygame.sprite.spritecollide(player, current_enemy.enemy_flying, True)
                else:
                    enemy_collide_flying = pygame.sprite.spritecollide(player, current_enemy.enemy_flying, False)
                    for enemy in enemy_collide_flying:
                        if enemy.rect.x+15 < player.rect.x:
                            current_enemy.enemy_flying.remove(enemy)
                if enemy_collide_flying:
                    if mustache:
                        invinc_hit_wav.play()
                    player.living = False
                boss_collide = pygame.sprite.spritecollide(player, current_enemy.boss, False)
                if boss_collide:
                        pass
                        #print("LOL U SUCK")
                enemy_collide_ground = pygame.sprite.spritecollide(player, current_enemy.enemy_ground, True)
                for enemy in enemy_collide_ground:
                    if player.rect.bottom - enemy.rect.top < 20:
                        player.up_down = -14
                        enemy_ground_wav.play()
                    else:
                        if mustache:
                            invinc_hit_wav.play()
                        player.living = False
                        
                if boss_living:
                    if not world_shift and bomb_counter == 8:
                        current_objects.add_pot()
                        current_power.power_list.empty()
                        bomb_counter = 0
                    if dmg_boss and living:
                            if boss_hp > 20:
                                for item in current_objects.layers:
                                    if item.type == 2:
                                        for i in range(10):
                                            boss_hp -=1
                                            item.image = pygame.transform.scale(item.image,(boss_hp, 64))
                            dmg_boss = False
                    if boss_hp < 26:
                        current_enemy.boss.empty()
                        current_level.remove_boss_wall()
                        world_shift = True
                        boss_living = False
                        current_objects.add_head()

                # mängija kordinaatide küsimine
                px = player.rect.x
                py = player.rect.y
                # spritede uuendamine
                player_sprite.update(current_level.wall_list)
                current_objects.update()
                current_enemy.update(px,py)
                current_power.update()
                if stars == 3 and current_level.world_shift <= level_limit[current_level_nr] and player.rect.x > 688:
                    if current_level_nr == 0:
                        level_shift = True
                        level_shift_time = pygame.time.get_ticks()
                        pygame.mixer.stop()
                        pygame.mixer.music.stop()
                        current_enemy.enemy_flying.empty
                        current_enemy.enemy_ground.empty
                        current_level_nr = 1
                        player.rect.x = 100
                        stars = 0
                        current_level = levels[current_level_nr]
                        current_power = power_level[current_level_nr]
                        current_objects = objects_level[current_level_nr]

                        player.level = current_level
                    elif current_level_nr == 1:
                        level_shift = True
                        level_shift_time = pygame.time.get_ticks()
                        pygame.mixer.stop()
                        pygame.mixer.music.stop()
                        current_enemy.enemy_flying.empty
                        current_enemy.enemy_ground.empty
                        current_level_nr = 2
                        player.rect.x = 100
                        current_level = levels[current_level_nr]
                        current_power = power_level[current_level_nr]
                        current_objects = objects_level[current_level_nr]
                        player.level = current_level
                # Tausta muutmine
                #lvl 1 lim
               # if player.rect.x > 500 and current_level.world_shift > -5170:
                if world_shift:
                        if player.rect.x > 500 and current_level.world_shift > level_limit[current_level_nr]:
                            shift = player.rect.x- 500
                            player.rect.x = 500
                            current_level.shift_world(-shift)
                            current_enemy.shift_world(-shift)
                            current_power.shift_world(-shift)
                            current_objects.shift_world(-shift)
                            
                        elif player.rect.x < 240 and current_level.world_shift <0:
                            shift = 240 - player.rect.x
                            player.rect.x = 240
                            current_level.shift_world(shift)
                            current_enemy.shift_world(shift)
                            current_power.shift_world(shift)
                            current_objects.shift_world(shift)
                            
                        if current_level_nr == 2 and boss_living and current_level.world_shift < -1692:
                            boss_shift = True
                            world_shift = False
                            boss_pause = True
                            bomb_counter = 5
                            current_level.add_boss_wall()
            
            ## Boss pause lõpp
            #--- kuvamised---
            # tausta kuvamine
            current_level.update()
            if current_level_nr == 1 and current_level.world_shift < -1200 and ghost_sound:
                    ghost_wav.play()
                    ghost_sound = False
            elif current_level_nr ==2 and pygame.time.get_ticks() - plat_up_time > 1500 and level_shift == False:
                    current_level.add_plat_up("up")
                    current_level.add_plat_up("down")
                    if boss_living: current_enemy.boss_axe_throw()
                    plat_up_time = pygame.time.get_ticks()
                    bomb_counter +=1
            current_level.draw(screen)
            current_objects.draw(screen)
            # mängija kuvamine ekraanile 
            player_sprite.draw(screen)

            if mustache and living:
                px = player.rect.x
                py = player.rect.y
                if player.direction == "R":
                    screen.blit(mustascheright,(px+5,py+30))
                else:
                    screen.blit(mustascheleft,(px-35,py+30))
                get_time_diff =  pygame.time.get_ticks() - when_stache
                if get_time_diff < 1000:
                    screen.blit(countdown[9],(10,45))
                elif get_time_diff < 2000: 
                    screen.blit(countdown[8],(10,45))
                elif get_time_diff < 3000:
                    screen.blit(countdown[7],(10,45))
                elif get_time_diff < 4000:
                    screen.blit(countdown[6],(10,45))
                elif get_time_diff < 5000:
                    screen.blit(countdown[5],(10,45))
                elif get_time_diff < 6000:
                    screen.blit(countdown[4],(10,45))
                elif get_time_diff < 7000:
                    screen.blit(countdown[3],(10,45))
                elif get_time_diff < 8000:
                    screen.blit(countdown[2],(10,45))
                elif get_time_diff < 9000:
                    screen.blit(countdown[1],(10,45))
                elif get_time_diff < 10000:
                    screen.blit(countdown[0],(10,45))
                else:
                    mustache = False
                    
            # powerupid
            current_power.draw(screen)
            # vastaste kuvamine 
            current_enemy.draw(screen)
               
            if joketime:
                screen.blit(joke11, (text_x1-y1,100-y1))
                screen.blit(joke11, (text_x1-y1,100+y1))
                screen.blit(joke11, (text_x1+y1,100-y1))
                screen.blit(joke11, (text_x1+y1,100+y1))
                screen.blit(jokefont1.render(joke1, True, (141,224,130)), (text_x1,100))
                if pygame.time.get_ticks() - when_joke > 2500:
                    if joke_play:
                        joke_wav.play()
                        joke_play = False
                    screen.blit(joke22, (text_x2-y2,140-y2))
                    screen.blit(joke22, (text_x2-y2,140+y2))
                    screen.blit(joke22, (text_x2+y2,140-y2))
                    screen.blit(joke22, (text_x2+y2,140+y2))
                    screen.blit(jokefont2.render(joke2, True, (141,224,130)), (text_x2,140))            
                    if pygame.time.get_ticks() - when_joke > 5500:
                        joketime = False
            # sihiku paigaldamine
            cx, cy = pygame.mouse.get_pos() # hiire positsioon
            screen.blit(cursor,(cx-38,cy-38))
            if stars == 0:
                screen.blit(star_png[0],(10,10))
            elif stars == 1:
                screen.blit(star_png[1],(10,10))
            elif stars == 2:
                screen.blit(star_png[2],(10,10))
            else:
                screen.blit(star_png[3],(10,10))
            if living:
                if player.rect.y > 500 or (player.rect.y < -102 and current_level_nr == 2):
                    #death_wav_2.play()
                    living = False
                    deadx = px
                    deady = py                
                if not player.livingwall:
                    #living = False
                    #death_wav.play()
                    deadx = px
                    deady = py
                if not player.living and not mustache :
                    #living = False
                    #death_wav.play()
                    deadx = px
                    deady = py
                else:
                    player.living = True
            else:
                screen.blit(player_dead,(deadx,deady+40))
                player_sprite.empty()
                walking.set_volume(0)
                current_enemy.enemy_flying.empty()
                screen.blit(game_over, (253,247))
                screen.blit(game_over, (253,253))
                screen.blit(game_over, (247,253))
                screen.blit(game_over, (247,247))          
                screen.blit(fontbig.render("Game Over" , True, (217,217,25)), (250,250))
            if boss_shift:
                if current_level.world_shift > -2185:
                    current_level.shift_world(-3)
                    current_enemy.shift_world(-3)
                    current_power.shift_world(-3)
                    current_objects.shift_world(-3)
                    player.rect.x -= 3
                else:
                    boss_shift = False
                    boss_pause = False
            if level_shift:
                screen.blit(level_1_logo, (0,0))
                if pygame.time.get_ticks() - level_shift_time > 2000:
                    level_shift = False
                    current_enemy = enemy_level[current_level_nr]
                    current_enemy.add_ground_enemy()
                    heli_level(current_level_nr)
            time.tick(60)
            #print(current_objects.moving_object)
            pygame.display.flip() # uuendab tervet ekraani
            pygame.display.set_caption("fps: " + str(round(time.get_fps())))
            #pausi lõpp
    pygame.quit()
        
                
if __name__ == '__main__': 
    game()
