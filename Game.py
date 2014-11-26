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


def menu(not_paused = True,back_img = 'bg.png', full_scr = False, sound = True, cleanjoke = True):
    def outline(text,x,y):
            for pos in ((x-2,y+2),(x+2,y-2),(x-2,y-2),(x+2,y+2)):
                screen.blit(text,pos)
                
    pygame.mixer.music.pause()
    pygame.mixer.stop()
    
    if full_scr:
        screen = pygame.display.set_mode((gamewidth, gameheight), FULLSCREEN)
    else:
        screen = pygame.display.set_mode((gamewidth, gameheight))
        
    # menu fonts 
    start_rect = start.get_rect()
    start_rect.move_ip(70,220)
    new_rect = start.get_rect()
    new_rect.move_ip(70,220)    
    continue_game_rect = continue_game.get_rect()
    continue_game_rect.move_ip(89,260)
    quit_game_rect = quit_game.get_rect()
    quit_game_rect.move_ip(120,300)
    full_scr_rect = checked_img.get_rect()
    full_scr_rect.move_ip(190, 438)
    cleanjoke_rect = checked_img.get_rect()
    cleanjoke_rect.move_ip(190, 468)
    sound_rect = soundon.get_rect()
    sound_rect.move_ip(125,500)
    
    menu = []
    menu.append(start_rect)
    menu.append(continue_game_rect)
    menu.append(quit_game_rect)
    
    bg = pygame.image.load("Graphics/Background/" + back_img).convert_alpha()

    choice = -1
    x = -150
    y = 1



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
                        if sound: menu_wav.play()
                        end_anim = True
                        break
                elif sound_rect.collidepoint(event.pos):
                    sound = not sound
                    if sound: menu_wav2.play()
                elif cleanjoke_rect.collidepoint(event.pos):
                    cleanjoke = not cleanjoke
                    if sound: menu_wav2.play()
                elif full_scr_rect.collidepoint(event.pos):
                    full_scr = not full_scr
                    if full_scr:
                        screen = pygame.display.set_mode((gamewidth, gameheight), FULLSCREEN)
                    else:
                        screen = pygame.display.set_mode((gamewidth, gameheight))
                    if sound:menu_wav2.play()
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
                elif event.key == K_ESCAPE and not not_paused:
                    choice = 1
                    end_anim = True
                    break
                elif event.key == K_RETURN:
                    if not_paused and choice == 1:
                        pass
                    else :
                        if sound:menu_wav.play()
                        end_anim = True
                        break
        cx, cy = pygame.mouse.get_pos()
        screen.blit(bg,(0,0))
        if choice == 0 and not start_anim:
            if not_paused:
                outline(start_big_shad,45,214)
                screen.blit(start_big,(45,214))
            else:
                outline(new_big_shad,59,214)
                screen.blit(new_big,(59,214))
        else:
            if not_paused:
                if x < 70:
                    screen.blit(start,(x,220))
                else:outline(start_shad,70,220); screen.blit(start,(70,220))
            else:
                if x < 70:
                    screen.blit(new,(x,220))
                else:outline(new_shad,81,220); screen.blit(new,(81,220))
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

        if full_scr: screen.blit(checked_img,(190, 438))
        else: screen.blit(not_checked_img,(190, 438))
        screen.blit(full_scr_img,(90, 440))
        if sound:
                screen.blit(soundon,(125,500))
        else: screen.blit(soundoff,(125,500))
        screen.blit(joke,(90, 470))
        if cleanjoke: screen.blit(checked_img,(190, 468))
        else: screen.blit(not_checked_img,(190, 468))

        screen.blit(cursor,(cx-38,cy-38))
        pygame.display.flip()
        if start_anim:
            x += 0.6+ y//3
            y += 1
        elif end_anim:
            x -= 0.6+ y//3
            y += 1
        time.tick(60)
        pygame.display.set_caption("fps: " + str(round(time.get_fps())))
    return choice, sound, cleanjoke, full_scr

def heli_level(level_nr, sound):
        global enemy_ground_wav, enemy_flying_wav, walking
        enemy_ground_wav = pygame.mixer.Sound('Sound\\Level ' + str(level_nr+1)+ '\Ground.ogg')
        enemy_flying_wav = pygame.mixer.Sound('Sound\\Level ' + str(level_nr+1)+ '\Flying.ogg')
        walking = pygame.mixer.Sound('Sound\\Level ' + str(level_nr+1)+ '\Walking.ogg')
        pygame.mixer.music.load('Sound/Level ' + str(level_nr+1)+ '/Theme.ogg')
        if sound: pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.6)
        walking.set_volume(0.6)
        
def game(sound, clean, full_scr):
    running = True
    game_credits = False
    if full_scr:
        screen = pygame.display.set_mode((gamewidth, gameheight), FULLSCREEN)
    else:
        screen = pygame.display.set_mode((gamewidth, gameheight))

    # joke variables
    joketime = False
    
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
    current_level_nr = 1
    current_level = levels[current_level_nr]
    current_enemy = enemy_level[current_level_nr]
    current_power = power_level[current_level_nr]
    current_objects = objects_level[current_level_nr]
    plat_up_time = pygame.time.get_ticks()

    #player
    living = True
    mustache = False
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
                        if event.key == K_ESCAPE and living and player.left_right == 0: # muidu bug liikumisega
                            option = menu(False, full_scr = full_scr, sound = sound)
                            pygame.mixer.music.unpause()
                            sound = option[1]
                            if option[3] != full_scr:
                                if option[3]:
                                    full_scr = True
                                    screen = pygame.display.set_mode((gamewidth, gameheight), FULLSCREEN)
                                else:
                                    full_scr = False
                                    screen = pygame.display.set_mode((gamewidth, gameheight))

                            if not sound:
                                pygame.mixer.music.stop()
                            clean = option[2]
                            if option[0] == 0:
                                pygame.mixer.music.stop()
                                state = 3
                                running = False
                            elif option[0] == 2:
                                running = False
                                state = 0
                            
                    if event.type == KEYDOWN: # kui hoida klahvi all, siis object liigub
                        if event.key == K_RIGHT: # liigub paremale
                            if player.left_right == 0:
                                player.direction = "R"
                            player.move(6)
                            if sound:walking.play(-1)

                        elif event.key == K_LEFT: # liigub vasakule
                            if player.left_right == 0:
                                player.direction = "L"
                            player.move(-6)
                            if sound:walking.play(-1)
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
                                if sound:enemy_flying_wav.play()
                                current_enemy.enemy_flying.remove(enemy)
            else:
                if current_level_nr != 0: player.rect.x = 90
                else: player.rect.x = 350
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
                    if sound:book_wav.play()
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
                elif collide.type == 'Star.png':
                    stars += 1
                    if sound:star_wav.play()
                elif collide.type == 'Orb.png':
                    if sound:invinc_wav.play()
                    mustache = True
                    when_stache = pygame.time.get_ticks()
                else:
                    game_credits_timer = pygame.time.get_ticks()
                    game_credits = True
                    pygame.mixer.stop()
                    pygame.mixer.music.stop()
                    if sound: game_credits_wav.play()
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
                    if sound:invinc_hit_wav.play()
                player.living = False

            boss_collide = pygame.sprite.spritecollide(player, current_enemy.boss, False)
            if boss_collide:
                player.living = False
                
            enemy_collide_ground = pygame.sprite.spritecollide(player, current_enemy.enemy_ground, True)
            for enemy in enemy_collide_ground:
                if player.rect.bottom - enemy.rect.top < 20:
                    player.up_down = -14
                    if sound:enemy_ground_wav.play()
                else:
                    if mustache:
                        if sound:invinc_hit_wav.play()
                    player.living = False
                    
            if boss_living:
                if not world_shift and bomb_counter == 8:
                    current_objects.add_pot()
                    for item in current_power.power_list:
                        if item.type == "Paper.png":
                            current_power.power_list.remove(item)
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
                if sound:ghost_wav.play()
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
                    if sound:joke_wav.play()
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
                if sound:death_wav_2.play()
                game_over_timer = pygame.time.get_ticks()

                living = False
                deadx = px
                deady = py                
            if not player.livingwall:
                game_over_timer = pygame.time.get_ticks()

                living = False
                if sound:death_wav.play()
                deadx = px
                deady = py
            if not player.living and not mustache :
                game_over_timer = pygame.time.get_ticks()
                #living = False
                #if sound:death_wav.play()
                deadx = px
                deady = py
            else:
                player.living = True
        else:
            screen.blit(player_dead,(deadx,deady+40))
            player_sprite.empty()
            walking.set_volume(0)
            current_enemy.enemy_flying.empty()
            screen.blit(youdied, (247,256))
            if pygame.time.get_ticks() - game_over_timer > 3000:
                state = 1
                break
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
                heli_level(current_level_nr, sound)
        if game_credits:
            screen.blit(game_credits_img,(0,0))
            if pygame.time.get_ticks() - game_credits_timer > 10800:
                state = 4
                break
        time.tick(60)
        pygame.display.flip() # uuendab tervet ekraani
        pygame.display.set_caption("fps: " + str(round(time.get_fps())))
    return state,full_scr, sound, clean

if __name__ == '__main__':
    
    pygame.font.init()
    time = pygame.time.Clock()
    pygame.init()
    screen = pygame.display.set_mode((gamewidth, gameheight))
    pygame.display.set_caption("Where's my burger")
    gamewidth = 800     # ekraani laius x
    gameheight = 600    # ekraani kõrgus y
    mäng = [0,0,0,0]
    color = (255,255,255)
    pygame.mouse.set_visible(False)
    
    #menüü fontid/text
    
    font0 = pygame.font.Font('norwester.otf',15)
    font1 = pygame.font.Font('norwester.otf',30)
    font2 = pygame.font.Font('norwester.otf',40)
    start = font1.render("start game" , True, color)
    start_shad = font1.render("start game" , True, (0,0,0))
    start_big = font2.render("start game" , True, color)
    start_big_shad = font2.render("start game" , True, (0,0,0))
    new = font1.render("new game" , True, color)
    new_shad = font1.render("new game" , True, (0,0,0))
    new_big = font2.render("new game" , True, color)
    new_big_shad = font2.render("new game" , True, (0,0,0))
    continue_game = font1.render("Continue" , True, color)
    continue_game_paused = font1.render("Continue" , True, (128,128,128))
    continue_game_big = font2.render("Continue" , True, color)
    continue_game_big_paused = font2.render("Continue" , True, (128,128,128))
    quit_game = font1.render("quit" , True, color)
    quit_game_big = font2.render("quit" , True, color)
    full_scr_img = font0.render("fullscreen" , True, color)
    joke = font0.render("clean jokes" , True, color)
    
    # menu audio
    menu_wav = pygame.mixer.Sound('Sound\\World\Menu1.ogg')
    menu_wav2 = pygame.mixer.Sound('Sound\\World\Menu2.ogg')
    # menüü graafika
    soundon = pygame.image.load('Graphics/UI/SoundOn.png').convert_alpha()
    soundoff = pygame.image.load('Graphics/UI/SoundOff.png').convert_alpha()
    cursor = pygame.image.load('Graphics/UI/Crosshair.png').convert_alpha()
    checked_img = pygame.image.load("Graphics/UI/checked.png").convert_alpha()
    not_checked_img = pygame.image.load("Graphics/UI/notchecked.png").convert_alpha()
    
    # mängu konstandid
    game_credits_img = pygame.image.load('Graphics/Background/credits.png').convert_alpha()
    player_dead = pygame.image.load('Graphics/Player/Dead.png').convert_alpha()
    level_logo = []
    for i in range(3):
        level_logo.append(pygame.image.load('Graphics/Background/Level'+str(i+1)+'.png').convert_alpha())
    boss_hp_bar = pygame.image.load('Graphics/UI/Boss/boss_hp.png').convert_alpha()
    boss_hp_bar_back = pygame.image.load('Graphics/UI/Boss/boss_hp_back.png').convert_alpha()
    youdied = pygame.image.load("Graphics/Background/Dead.png").convert_alpha() 
    
    # mängu heliefektid 
    joke_wav = pygame.mixer.Sound('Sound\\World\Drum.ogg')
    book_wav =  pygame.mixer.Sound('Sound\\World\Book.ogg')
    star_wav = pygame.mixer.Sound('Sound\\World\Star.ogg')
    death_wav = pygame.mixer.Sound('Sound\\World\Death2.ogg')
    death_wav_2 = pygame.mixer.Sound('Sound\\World\Death.ogg')
    invinc_hit_wav = pygame.mixer.Sound('Sound\\World\Hit.ogg')
    invinc_wav = pygame.mixer.Sound('Sound\\World\Stache.ogg')
    game_credits_wav = pygame.mixer.Sound('Sound\\World\Credits.ogg')
    ghost_wav = pygame.mixer.Sound('Sound\\Level 2\Ghost.ogg')


    while True:
        if mäng[0] == 0:
            menüü = menu()
        elif mäng[0] == 1:
            menüü = menu(True, "bg_over.png", mäng[1], mäng[2], mäng[3])
        elif mäng[0] == 4:
            menüü = menu(True, "bg_end.png", mäng[1], mäng[2], mäng[3])            
        if menüü[0] == 0:
            mäng = game(menüü[1], menüü[2], menüü[3])
        elif menüü[0] == 2 or menüü[0] == -1: break
        if mäng[0] == 0: break

    pygame.quit()
