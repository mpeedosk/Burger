import pygame
from pygame.locals import *
from random import randint
from Player import *    
from Wall import *
from Enemy import*
from Power import *
from GameObjects import *


#"Nuclear Runner Uncensored"
# konstandid


def menu(not_paused = True,back_img = 'bg.png', full_scr = False, sound = True, checked = True):
    pygame.mixer.music.pause()
    pygame.mixer.stop()
    color = (255,255,255)
    colorbig = (255,255,255)
    if full_scr:
        screen = pygame.display.set_mode((gamewidth, gameheight), FULLSCREEN)
    else:
        screen = pygame.display.set_mode((gamewidth, gameheight))
    # menu fonts 
    start = font1.render("start game" , True, color)
    start_shad = font1.render("start game" , True, (0,0,0))
    start_big = font2.render("start game" , True, colorbig)
    start_big_shad = font2.render("start game" , True, (0,0,0))
    start_rect = start.get_rect()
    start_rect.move_ip(70,220)
    continue_game = font1.render("Continue" , True, color)
    continue_game_paused = font1.render("Continue" , True, (128,128,128))
    continue_game_big = font2.render("Continue" , True, colorbig)
    continue_game_big_paused = font2.render("Continue" , True, (128,128,128))
    
    continue_game_rect = continue_game.get_rect()
    continue_game_rect.move_ip(89,260)
    quit_game = font1.render("quit" , True, color)
    quit_game_big = font2.render("quit" , True, colorbig)
    quit_game_rect = quit_game.get_rect()
    quit_game_rect.move_ip(120,300)
    menu = []
    menu.append(start_rect)
    menu.append(continue_game_rect)
    menu.append(quit_game_rect)
    ##
    menu_wav = pygame.mixer.Sound('Sound\\World\menu1.wav')
    menu_wav2 = pygame.mixer.Sound('Sound\\World\menu2.wav')
    soundon = pygame.image.load('SoundOn.png')
    soundoff = pygame.image.load('SoundOff.png')

    bg = pygame.image.load(back_img)
    cursor = pygame.image.load('Crosshair.png')
    pygame.mouse.set_visible(False)
    joke = font0.render("clean jokes" , True, color)
    checked_img = pygame.image.load("checked.png")
    not_checked_img = pygame.image.load("notchecked.png")
    checked_rect = checked_img.get_rect()
    checked_rect.move_ip(190, 468)
    full_scr_img = font0.render("fullscreen" , True, color)
    full_scr_rect = checked_img.get_rect()
    full_scr_rect.move_ip(190, 438)
    choice = -1
    def outline(text,x,y):
            for pos in ((x-2,y+2),(x+2,y-2),(x-2,y-2),(x+2,y+2)):
                screen.blit(text,pos)      
    x = -150
    y = 1
    sound_rect = soundon.get_rect()
    sound_rect.move_ip(125,500)
    start_anim = True
    end_anim = False
    while True:
        for event in pygame.event.get(): # Vaatab millise eventiga parajasti teguon
            if event.type == MOUSEMOTION and not start_anim and not end_anim:
                choice = Rect(event.pos,(0,0)).collidelist(menu)
            elif event.type == MOUSEBUTTONUP and event.button == 1:
                if menu[choice].collidepoint(event.pos):
                    if not_paused and choice == 1:
                        pass
                    else :
                        menu_wav.play()
                        end_anim = True
                        break
                elif sound_rect.collidepoint(event.pos): sound = not sound; menu_wav2.play()
                elif checked_rect.collidepoint(event.pos): checked = not checked;menu_wav2.play()
                elif full_scr_rect.collidepoint(event.pos): full_scr = not full_scr; menu_wav2.play()
            elif event.type == pygame.QUIT: # kui vajutatakse üleval X siis läheb tsükkel kinni
                end_anim = True
                break
            elif event.type == KEYDOWN: # kui hoida klahvi all, siis object liigub
                if event.key==K_UP or event.key==K_DOWN:
                    if not_paused:
                        if choice != 0: choice = 0
                        else: choice = 2
                    else:
                        choice = (choice + {K_UP:-1,K_DOWN:1}[event.key])%3
                elif event.key == K_RETURN:
                    if not_paused and choice == 1:
                        pass
                    else :
                        menu_wav.play()
                        end_anim = True
                        break
        cx, cy = pygame.mouse.get_pos()
        screen.blit(bg,(0,0))
        if choice == 0 and not start_anim:
            outline(start_big_shad,45,214)
            screen.blit(start_big,(45,214))
        else:
            if x < 70:
                screen.blit(start,(x,220))
            else:outline(start_shad,70,220); screen.blit(start,(70,220))
        if not not_paused:
            if choice == 1 and not start_anim : screen.blit(continue_game_big,(72,254))
            else:
                if x < 109: screen.blit(continue_game,(x-20,260))
                else: screen.blit(continue_game,(89,260))
        else: 
            if x < 109: screen.blit(continue_game_paused,(x-20,260))
            else: screen.blit(continue_game_paused,(89,260))            
        if choice == 2 and not start_anim: screen.blit(quit_game_big,(114,294))
        else:
            if x < 160:
                screen.blit(quit_game,(x-40,300))
            else: screen.blit(quit_game,(120,300))
        if x > 160:
            start_anim = False
            y = 0
        elif x < -200:
            break
        if not_paused:
            if sound:
                    screen.blit(soundon,(125,500))
            else: screen.blit(soundoff,(125,500)); pygame.mixer.stop()
            screen.blit(joke,(90, 470))
            if checked: screen.blit(checked_img,(190, 468))
            else: screen.blit(not_checked_img,(190, 468))
            screen.blit(full_scr_img,(90, 440))
            if full_scr: screen.blit(checked_img,(190, 438))
            else: screen.blit(not_checked_img,(190, 438))
        screen.blit(cursor,(cx-38,cy-38))
        pygame.display.flip()
        if start_anim:
            x += 0.6+ y//3
            y += 1
        elif end_anim:
            x -= 0.6+ y//3
            y += 1
    return choice, sound, checked, full_scr

def heli_level(level_nr):
        global enemy_ground_wav, enemy_flying_wav, walking
        enemy_ground_wav = pygame.mixer.Sound('Sound\\Level ' + str(level_nr+1)+ '\crack.wav')
        enemy_flying_wav = pygame.mixer.Sound('Sound\\Level ' + str(level_nr+1)+ '\Bird.ogg')
        walking = pygame.mixer.Sound('Sound\\Level ' + str(level_nr+1)+ '\Right_left.wav')
        pygame.mixer.music.load('Sound/Level ' + str(level_nr+1)+ '/Theme.ogg')
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.6)
        walking.set_volume(0.6)
        
def game(sound, clean, full_scr):
    running = True
    pygame.display.set_caption("Little Combat 2000") # mängu nimi
    time = pygame.time.Clock()
    if full_scr:
        screen = pygame.display.set_mode((gamewidth, gameheight), FULLSCREEN)
    else:
        screen = pygame.display.set_mode((gamewidth, gameheight))
        
    cursor = pygame.image.load('Crosshair.png').convert_alpha()

    # game over
    youdied = pygame.image.load("Dead.png").convert_alpha() 

    # joke variables
    joketime = False
    pygame.mouse.set_visible(False)                     #Peidab hiire noole ära
    
    # graafika
    
    player_dead = pygame.image.load('Bird/Masked/Dead2.png').convert_alpha()
    level_logo = []
    for i in range(3):
        level_logo.append(pygame.image.load('Level'+str(i+1)+'.png').convert_alpha())
    boss_hp_bar = pygame.image.load('boss_hp.png').convert_alpha()
    boss_hp_bar_back = pygame.image.load('boss_hp_back.png').convert_alpha()
    
    #heliefektid
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
    cooldown = 4500
    enemy_count = 0
    boss_hp = 226

    # praegune level
    ghost_sound = True
    level_limit = [-5170,-3190,-2190]
    current_level_nr = 0
    current_level = levels[current_level_nr]
    current_enemy = enemy_level[current_level_nr]
    current_power = power_level[current_level_nr]
    current_objects = objects_level[current_level_nr]
    plat_up_time = pygame.time.get_ticks()

    #player
    living = True
    mustache = False
    player.rect.x = 250
    player.rect.y = 350
    player_sprite.add(player) 
    player.level = current_level
    level_shift = True
    level_shift_time = pygame.time.get_ticks()
    boss_shift = False
    boss_pause = False
    dmg_boss = False
    boss_living = True
    bomb_counter = 0
    new_game = False
    state = 0
    while running:
        if not boss_pause:
            if not level_shift:
                for event in pygame.event.get(): # Vaatab millise eventiga parajasti teguon
                    if event.type == pygame.QUIT: # kui vajutatakse üleval X siis läheb tsükkel kinni
                        running = False
                        state = 0
                    elif event.type == KEYDOWN: # kui hoida klahvi all, siis object liigub
                        if event.key == K_ESCAPE and living:
                            option = menu(False, full_scr = full_scr)[0]
                            pygame.mixer.music.unpause()
                            if option == 0:
                                pygame.mixer.music.stop()
                                state = 3
                                running = False
                            elif option == 2:
                                running = False
                                state = 0
                            
                    if event.type == KEYDOWN: # kui hoida klahvi all, siis object liigub
                        if event.key == K_RIGHT: # liigub paremale
                            if player.left_right == 0:
                                player.direction = "R"
                            player.move(6)
                            walking.play(-1)

                        elif event.key == K_LEFT: # liigub vasakule
                            if player.left_right == 0:
                                player.direction = "L"
                            player.move(-6)
                            walking.play(-1)
                        elif event.key == K_UP:
                            player.jump()
                        elif event.key == K_DOWN:
                            pass 
                    elif event.type == KEYUP: # kui klahv üles tõuseb, siis liikumine lõppeb.  Esimese argumendi negatiivne vaste, et summa oleks 0
                        if event.key == K_RIGHT: # lõpetab paremale liikumise
                            player.move(-6)
                            walking.stop()
                        elif event.key == K_LEFT: # lõpetab vasakule liikumise
                            player.move(6)
                            walking.stop()
                    elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                        if cx in range(590,675) and cy in range(236,320): 
                            dmg_boss = True
                        for enemy in current_enemy.enemy_flying:
                            if enemy.rect.collidepoint((cx, cy)):
                                enemy_flying_wav.play()
                                current_enemy.enemy_flying.remove(enemy)
            else:
                if current_level_nr != 0: player.rect.x = 90
                else: player.rect.x = 250
            #--- event lõpp ---
            if pygame.time.get_ticks() - spawn_timer >= cooldown:
                if current_level_nr != 1:   
                    current_enemy.add_enemy()
                else:
                    if current_level.world_shift > -2300:
                        current_enemy.add_enemy()
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
                    if clean:
                        joke_nr = randint(0,61)
                        joke1, text_x1, jokefont1 = current_power.joke_joke_clean(screen, joke_nr)
                        joke2, text_x2, jokefont2= current_power.joke_punch_clean(screen, joke_nr)   
                    else:
                        joke_nr = randint(0,119)
                        joke1, text_x1, jokefont1 = current_power.joke_joke_both(screen, joke_nr)
                        joke2, text_x2, jokefont2= current_power.joke_punch_both(screen, joke_nr)
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
            object_collide = pygame.sprite.spritecollide(player, current_objects.moving_object, False)
            for item in object_collide:
                if item.type == "exp":
                    player.living = False
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
                player.living = False
                
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
                                    for i in range(5):
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
                    stars = 3
                    current_level = levels[current_level_nr]
                    current_power = power_level[current_level_nr]
                    current_objects = objects_level[current_level_nr]
                    player.level = current_level
                    mustache = False

                    
                elif current_level_nr == 1:
                    level_shift = True
                    level_shift_time = pygame.time.get_ticks()
                    pygame.mixer.stop()
                    pygame.mixer.music.stop()
                    current_enemy.enemy_flying.empty
                    current_enemy.enemy_ground.empty
                    current_level_nr = 2
                    current_level = levels[current_level_nr]
                    current_power = power_level[current_level_nr]
                    current_objects = objects_level[current_level_nr]
                    player.level = current_level
                    mustache = False

            # Tausta muutmine
            #lvl 1 lim
           # if player.rect.x > 500 and current_level.world_shift > -5170:
            if world_shift and living and not level_shift:
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
        else:
            for event in pygame.event.get(): # Vaatab millise eventiga parajasti teguon
                if event.type == pygame.QUIT: # kui vajutatakse üleval X siis läheb tsükkel kinni
                    running = False
                    state = 0
            player.left_right = 0
            pygame.event.clear()
        ## Boss pause lõpp

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
        #--- kuvamised---
        # tausta kuvamine
        current_level.draw(screen)
        current_objects.draw(screen)
        # mängija kuvamine ekraanile 
        player_sprite.draw(screen)

        if mustache and living:
            player.mustache(screen)
            current_objects.stach_timer(screen,when_stache)
            if pygame.time.get_ticks() - when_stache > 10000:
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
        current_objects.stars(screen, stars)

        if living:
            if player.rect.y > 500 or (player.rect.y < -102 and current_level_nr == 2):
                death_wav_2.play()
                game_over_timer = pygame.time.get_ticks()

                living = False
                deadx = px
                deady = py                
            if not player.livingwall:
                game_over_timer = pygame.time.get_ticks()

                living = False
                death_wav.play()
                deadx = px
                deady = py
            if not player.living and not mustache :
                game_over_timer = pygame.time.get_ticks()
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
            screen.blit(youdied, (253,247))
            if pygame.time.get_ticks() - game_over_timer > 3000:
                state = 1
                break
        if not sound:
            pygame.mixer.stop()
            pygame.mixer.music.stop()
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
            screen.blit(level_logo[current_level_nr], (0,0))
            if pygame.time.get_ticks() - level_shift_time > 2000:
                level_shift = False
                current_enemy = enemy_level[current_level_nr]
                current_enemy.add_ground_enemy()
                enemy_level[2].add_boss()
                heli_level(current_level_nr)
        time.tick(60)
        print(player.rect.x)
        pygame.display.flip() # uuendab tervet ekraani
        pygame.display.set_caption("fps: " + str(round(time.get_fps())))
    return state,full_scr, sound, clean

if __name__ == '__main__':
    pygame.font.init()
    pygame.init()
    gamewidth = 800     # ekraani laius x
    gameheight = 600    # ekraani kõrgus y
    font0 = pygame.font.Font('norwester.otf',15)
    font1 = pygame.font.Font('norwester.otf',30)
    font2 = pygame.font.Font('norwester.otf',40)
    mäng = [0,0,0,0]
    while True:
        if mäng[0] == 0:
            menüü = menu()
        elif mäng[0] == 1:
            menüü = menu(True, "bg_over.png", mäng[1], mäng[2], mäng[3])
        if menüü[0] == 0:
            mäng = game(menüü[1], menüü[2], menüü[3])
        elif menüü[0] == 2 or menüü[0] == -1: break
        if mäng[0] == 0: break

    pygame.quit()
