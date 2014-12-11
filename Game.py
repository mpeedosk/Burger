import pygame
from pygame.locals import *
from random import randint
from Player import *    
from Wall import *
from Enemy import*
from Power import *
from GameObjects import *

# menüü funktsioon
# parameetriteks on kas on pausi peal, tausta pilt, täisekraan, heli, naljad, level
def menu(not_paused = True,back_img = 'bg.png', full_scr = False, sound = True, cleanjoke = True, current_level_nr = 0):
    # teksti outline
    def outline(text,x,y):
            # sama teksti kuvatakse 4 erinevas kohas musta kirjaga, et tekiks outline efekt
            for pos in ((x-2,y+2),(x+2,y-2),(x-2,y-2),(x+2,y+2)):
                screen.blit(text,pos)
    # kui menüü käivitatakse, lõpetame heliefektide esitamise
    pygame.mixer.music.pause()
    pygame.mixer.stop()
    # kui on menüü käivitamise ajal on täisekraan valitud
    if full_scr:
        screen = pygame.display.set_mode((gamewidth, gameheight), FULLSCREEN)
    else:
        screen = pygame.display.set_mode((gamewidth, gameheight))
        
    # menüü fontid, teksti taga on nähtamatu ristkülik  
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
    lvl1_rect= lvl1_img.get_rect()
    lvl1_rect.move_ip(130,410)
    lvl2_rect= lvl1_img.get_rect()
    lvl2_rect.move_ip(160,410)
    lvl3_rect= lvl1_img.get_rect()
    lvl3_rect.move_ip(190,410)

    # panen ristkülikud listi
    menu = []
    menu.append(start_rect)
    menu.append(continue_game_rect)
    menu.append(quit_game_rect)
    # tausta kuvamine
    bg = pygame.image.load("Graphics/Background/" + back_img).convert_alpha()
    # millise valikuga tegemist on, -1 näita, et ükski pole valitud
    choice = -1
    # alguse/lõpu animatsiooni muutujad
    x = -150
    y = 1


    start_anim = True
    end_anim = False
    
    while True:
        for event in pygame.event.get(): # Vaatab millise eventiga parajasti teguon
            if event.type == MOUSEMOTION and not start_anim and not end_anim: # vaatab kus hiir on ja kui pole animatsiooni aeg, siis teeb valiku ära
                # vaatab kas hiir on mõne menüülisti elemendi peal
                choice = Rect(event.pos,(0,0)).collidelist(menu)
            # kui hiirega vajutada kuhugi
            elif event.type == MOUSEBUTTONUP and event.button == 1:
                # kui toimub collide
                if menu[choice].collidepoint(event.pos):
                    # kui pole pausi peal ja valik on üks, siis ei tee midagi
                    # selleks et kui mängu ei toimu ei saaks continue panna
                    if not_paused and choice == 1:
                        pass
                    else :
                        # kui valik on tehtud, mängib lõpuheli, alustab lõpuanimatsiooni ja lõpetab funktsiooni
                        if sound: menu_wav.play() # kui heli on peal mängib
                        end_anim = True
                        break
                    # kui soundi valikut vajutatakse
                elif sound_rect.collidepoint(event.pos):
                    sound = not sound # teeb valiku vastupidiseks
                    if sound: menu_wav2.play()
                elif cleanjoke_rect.collidepoint(event.pos):
                    cleanjoke = not cleanjoke
                    if sound: menu_wav2.play()
                elif full_scr_rect.collidepoint(event.pos):
                    full_scr = not full_scr
                    # kui täisekraani peale pannakse, siis kohe muudab ära
                    if full_scr:
                        screen = pygame.display.set_mode((gamewidth, gameheight), FULLSCREEN)
                    else:
                        screen = pygame.display.set_mode((gamewidth, gameheight))
                    if sound:menu_wav2.play() 
                elif lvl1_rect.collidepoint(event.pos):
                    current_level_nr = 0
                    if sound: menu_wav2.play()
                elif lvl2_rect.collidepoint(event.pos):
                    current_level_nr = 1
                    if sound: menu_wav2.play()
                elif lvl3_rect.collidepoint(event.pos):
                    current_level_nr = 2
                    if sound: menu_wav2.play()
            elif event.type == pygame.QUIT: # kui vajutatakse üleval x-i siis läheb lõpuanimatsioon käima ja lõpetab tsükli ära
                end_anim = True
                break
            elif event.type == KEYDOWN: # võimaldab klaviatuuriga valikuid teha
                if event.key==K_UP or event.key==K_DOWN:
                    if not_paused: 
                        if choice != 0: choice = 0 # kui pole pausi peal siis laseb kahe vahel valida
                        else: choice = 2
                    else:
                        # kui on pausi peal siis võtab valikuks jäägi kolmest
                        choice = (choice + {K_UP:-1,K_DOWN:1}[event.key])%3
                        
                elif event.key == K_ESCAPE and not not_paused: # laseb escape nupuga pausi pealt ära panna
                    choice = 1
                    end_anim = True
                    break
                elif event.key == K_RETURN: # laseb enteriga valiku teha
                    if sound:menu_wav.play()
                    end_anim = True
                    break
        # hiire positsiooni küsimine
        cx, cy = pygame.mouse.get_pos()
        screen.blit(bg,(0,0))
    	# teeb valitud levelile kasti ümber
        if current_level_nr ==0:
            level_selected = (130,410)
        elif current_level_nr == 1:
            level_selected = (160,410)
        else:
            level_selected = (190,410)
        # vastavalt valikule teeb ühe teksti suuremaks
        # algusanimatsiooni puhul ei lase
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
        # continue kuvamine
        if not not_paused:
            if choice == 1 and not start_anim : screen.blit(continue_game_big,(72,254))
            else:
                if x < 109: screen.blit(continue_game,(x-20,260))
                else: screen.blit(continue_game,(89,260))
        else: 
            if x < 109: screen.blit(continue_game_paused,(x-20,260))
            else: screen.blit(continue_game_paused,(89,260))
        # quit kuvamine
        if choice == 2 and not start_anim: screen.blit(quit_game_big,(114,294))
        else:
            if x < 160:
                screen.blit(quit_game,(x-40,300))
            else: screen.blit(quit_game,(120,300))
            
        #  animatsiooni limiidid, kui tekstide x kordinaat jõuab 160, lõpetab animatsiooni ära
        if x > 160:
            start_anim = False
            y = 0

        # kui teksti x kordinaat on vähem kui -200, siis lõpetab kogu funktsiooni ära
        elif x < -200:
            break
        # levelite kuvamine
        if not_paused:
            screen.blit(level_nr,(90,412))
            screen.blit(lvl3_img,(190, 410))
            screen.blit(lvl2_img,(160, 410))
            screen.blit(lvl1_img,(130, 410))
            screen.blit(level_select_img,(level_selected))
        # täisekraani valik
        if full_scr: screen.blit(checked_img,(190, 438))
        else: screen.blit(not_checked_img,(190, 438))
        screen.blit(full_scr_img,(90, 440))
    	# heli valiku kuvamine
        if sound:
                screen.blit(soundon,(125,500))
        else: screen.blit(soundoff,(125,500))
    	# nalja valiku kuvamine
        screen.blit(joke,(90, 470))
        if cleanjoke: screen.blit(checked_img,(190, 468))
        else: screen.blit(not_checked_img,(190, 468))
        # uue hiire kuvamine
        screen.blit(cursor,(cx-38,cy-38))
        pygame.display.flip()
        # animatsiooni kiiruse muutmine
        if start_anim:
            x += 0.6+ y//3
            y += 1
        elif end_anim:
            x -= 0.6+ y//3
            y += 1
        time.tick(60)
        #pygame.display.set_caption("fps: " + str(round(time.get_fps())))
    return choice, sound, cleanjoke, full_scr,current_level_nr

# funktsioon helide muutmiseks leveli vahetusel
def heli_level(level_nr, sound):
    global enemy_ground_wav, enemy_flying_wav, walking # kasutan globaalseid muutujaid
    # iga level tuleb helid asendada
    enemy_ground_wav = pygame.mixer.Sound('Sound\\Level ' + str(level_nr+1)+ '\Ground.ogg')
    enemy_flying_wav = pygame.mixer.Sound('Sound\\Level ' + str(level_nr+1)+ '\Flying.ogg')
    walking = pygame.mixer.Sound('Sound\\Level ' + str(level_nr+1)+ '\Walking.ogg')
    pygame.mixer.music.load('Sound/Level ' + str(level_nr+1)+ '/Theme.ogg')
    if sound: pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.6)
    walking.set_volume(0.6)
    
# mängu põhifunktsioon
def game(sound, clean, full_scr,current_level_nr):
    running = True
    game_credits = False
    # vastavalt täisekraani valikule teeb otsuse
    if full_scr:
        screen = pygame.display.set_mode((gamewidth, gameheight), FULLSCREEN)
    else:
        screen = pygame.display.set_mode((gamewidth, gameheight))

    
    # playeri loomine
    player_sprite = pygame.sprite.Group()
    player = Player()
    
    # powerupid
    power_level = []
    power_level.append(Power_1(player))
    power_level.append(Power_2(player))
    power_level.append(Power_3(player))
    stars = 0
    joketime = False
    
    #seinad ja platformid
    levels = []
    levels.append(Level_1(player))
    levels.append(Level_2(player))
    levels.append(Level_3(player))
    level_shift_time = pygame.time.get_ticks()
    # kas lubame maailma nihkumist või mitte
    world_shift = True
    # loading screeni kuvamine
    level_shift = True
    
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
    # kui tihti uus vastane saab tekkida
    cooldown = 4500
    # bossi muutujad
    boss_hp = 226 # elud
    boss_shift = False # bossini jõudes maailma nihkumine 
    dmg_boss = False
    boss_living = True
    bomb_counter = 0
    
    # praegune level
    ghost_sound = True
    level_limit = [-5170,-3190,-2190]
    current_level = levels[current_level_nr]
    current_enemy = enemy_level[current_level_nr]
    current_power = power_level[current_level_nr]
    current_objects = objects_level[current_level_nr]
    plat_up_time = pygame.time.get_ticks()

    # mängija
    living = True # kas mängija on elus
    mustache = False # surematus
    player.rect.y = 350
    player_sprite.add(player) 
    player.level = current_level
    cheat = False # kas teeme sohki 
    state = 0 # vaatab kuidas mäng lõppes
    while running:
        # lülitab mõned funktsioonid välja, kui bossi juurde ekraan nihkub
        if not boss_shift:
            # lülitab mõned funktsioonid välja kui loading screen ees
            if not level_shift:
                for event in pygame.event.get(): # Vaatab millise eventiga parajasti tegu on
                    if event.type == pygame.QUIT: # kui vajutatakse üleval X siis laheb tsükkel kinni
                        running = False
                        state = 0
                        
                    elif event.type == KEYDOWN: # kui hoida klahvi all, siis object liigub
                        if event.key == K_ESCAPE and living and player.left_right == 0: # kui player on elus ja ei liigu, siis laseb escape vajutades pausi peale panna
                            option = menu(False, full_scr = full_scr, sound = sound) # käivitab menu funktsiooni
                            pygame.mixer.music.unpause() 
                            sound = option[1]
                            # kui muutusi toimub valikutes, vahetab need kohe ära
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
                            
                        if event.key == K_RIGHT: # liigub paremale
                            if player.left_right == 0:
                                player.direction = "R" # suund vaja animatsiooni jaoks
                            player.move(6)
                            if sound:walking.play(-1) # mängib liikumise heli

                        elif event.key == K_LEFT: # liigub vasakule
                            if player.left_right == 0:
                                player.direction = "L"
                            player.move(-6)
                            if sound:walking.play(-1)
                            
                        elif event.key == K_p:
                            print("cheat")
                            cheat = not cheat
                            
                        elif event.key == K_UP:
                            player.jump()
                            
                    elif event.type == KEYUP: # kui klahv üles tõuseb, siis liikumine lõppeb.
                        if event.key == K_RIGHT: # l6petab paremale liikumise
                            player.move(-6) 
                            walking.stop()
                        elif event.key == K_LEFT: # l6petab vasakule liikumise
                            player.move(6)
                            walking.stop()
                            
                    elif event.type == MOUSEBUTTONDOWN and event.button == 1: # bossi pea sihtimine
                        if cx in range(590,675) and cy in range(236,320): 
                            dmg_boss = True # kui hiir on õiges kohas ja vajutada vasakut nuppu, siis võtab bossi eludest maha teatud arv elusid
                        for enemy in current_enemy.enemy_flying: # teiste liikuvate vastaste tapmine
                            if enemy.rect.collidepoint((cx, cy)): # kui collidepoint ühtib hiire positsiooniga 
                                if sound:enemy_flying_wav.play()
                                current_enemy.enemy_flying.remove(enemy)
                                
            else: # kui on level shifti aeg, siis hoiab mängijat ühe koha peal
                if current_level_nr != 0: player.rect.x = 90
                else: player.rect.x = 350 # esimesel levelil on teine alguspunkt
                
	    #--- Level shift lõpp----#
            # vaatab kas uue vastase võib lisada
            if pygame.time.get_ticks() - spawn_timer >= cooldown:
                # esimesel levelil ei ole eritingimusi 
                if current_level_nr == 0:
                    current_enemy.add_enemy()
                # teisel levelil lõpetab vastaste lisamise kui piisavalt kaugel
                elif current_level_nr== 1:
                    if current_level.world_shift > -2300:
                        current_enemy.add_enemy()
                # uue timeri saamine
                spawn_timer = pygame.time.get_ticks()
                
            # bossi juures naljade tekitamine
            if current_objects.joke:
                current_objects.joke = False
                current_power.add_joke(2230, 437)
                
            # COLLIDE algus #
            #powerupid
            power_collide = pygame.sprite.spritecollide(player, current_power.power_list, True)
            for collide in power_collide:
                # naljad
                if collide.type == 'Paper.png':
                    if sound:book_wav.play()
                    joke_play = True
                    when_joke = pygame.time.get_ticks()
                    # mustade ja puhaste naljade puhul erinevad funktsioonid
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
                    # olenevalt nalja pikkusest valime outline suuruse
                    if len(joke1)< 68: y1=2
                    else: y1 = 1
                    if len(joke2)< 68: y2=2
                    else: y2 = 1
                    # aktiveerime nalja kuvamise ekraanile
                    joketime = True
                # tähed
                elif collide.type == 'Star.png':
                    stars += 1
                    if sound:star_wav.play()
                # surematus
                elif collide.type == 'Orb.png':
                    if sound:invinc_wav.play()
                    mustache = True
                    when_stache = pygame.time.get_ticks()
                    
                # lõpu burger
                else:
                    game_credits_timer = pygame.time.get_ticks()
                    game_credits = True
                    pygame.mixer.stop()
                    pygame.mixer.music.stop()
                    if sound: game_credits_wav.play()
                
            # bossi plahvatuse collide
            object_collide = pygame.sprite.spritecollide(player, current_objects.moving_object, False)
            for item in object_collide:
                if item.type == "exp":
                    if not cheat: player.living = False
                    
            # vastavalt levelile vaatame, kas pärast kokkupõrget eemaldame vastase või mitte
            if current_level_nr !=2:
                enemy_collide_flying = pygame.sprite.spritecollide(player, current_enemy.enemy_flying, True)
            else: # level 3 puhul ei eemalda me kirveid, sest vaja on et ta veel liiguks paarkümmend pixlit
                enemy_collide_flying = pygame.sprite.spritecollide(player, current_enemy.enemy_flying, False)
                for enemy in enemy_collide_flying:
                    if enemy.rect.x+15 < player.rect.x: # kui kirve vasak pool on playerist käbinud
                        current_enemy.enemy_flying.remove(enemy)
            # kui vastasega kokkupõrge
            if enemy_collide_flying:
                # kui surematus on peal mängib heli
                if mustache:
                    if sound:invinc_hit_wav.play()
                if not cheat:player.living = False
                
            # orade kokkupõrge
            spike_collide = pygame.sprite.spritecollide(player, current_enemy.spike_list, True)
            if spike_collide:
                if not cheat: player.living = False
                
            # bossi kokkupõrge
            boss_collide = pygame.sprite.spritecollide(player, current_enemy.boss, False)
            if boss_collide:
                if not cheat: player.living = False

            # maas liikuvate vastastega kokkupõrge
            enemy_collide_ground = pygame.sprite.spritecollide(player, current_enemy.enemy_ground, True)
            for enemy in enemy_collide_ground:
                if player.rect.bottom - enemy.rect.top < 20: # vaatab, kas mängija on vastasele peale hüppanud
                    player.up_down = -14 # teeb hüppe
                    if sound:enemy_ground_wav.play()
                else: # kui on kokkupõrganud, aga ei ole peale hüpanud
                    if mustache:
                        if sound:invinc_hit_wav.play()
                    if not cheat: player.living = False
            # COLLIDE lõpp #
            if boss_living:
                if not world_shift and bomb_counter == 8: # kui ei ole bossi juures ja kui pommi loendur on 8
                    current_objects.add_pot() # lisab uue pommi
                    for item in current_power.power_list:
                        if item.type == "Paper.png": # kustutab olemasolevad naljad, et mitu üksteise peale ei tuleks
                            current_power.power_list.remove(item)
                    bomb_counter = 0 # nullib loenduri
                # kui bossi tuleb kahjustada
                if dmg_boss and living:
                        # viimane piir kus elusid näha on ekraani peal
                        if boss_hp > 20:
                            for item in current_objects.layers:
                                if item.type == 2:
                                    for i in range(5): # iga kord vähendab elude riba pikkust 5 pixli võrra
                                        boss_hp -=1
                                        item.image = pygame.transform.scale(item.image,(boss_hp, 64))
                        dmg_boss = False # tähistab et töö on lõpetatud
                # kui bossi elusid pole enam ekraanil näha 
                if boss_hp < 26:
                    current_enemy.boss.empty() # eemaldab bossi ära
                    current_level.remove_boss_wall() # eemaldab seina mis takistas mängijal bossi juuerst ära joosta
                    world_shift = True  # laseb maailmal nihkuda jälle
                    boss_living = False # teatab, et boss on surnud 
                    current_objects.add_head() # lisab hobuse pea

            # mangija kordinaatide küsimine
            px = player.rect.x
            py = player.rect.y
            
            # spritede uuendamine
            player_sprite.update(current_level.wall_list)
            current_objects.update()
            current_enemy.update(px,py)
            current_power.update()

            # levelite vahetus
            if stars == 3 and current_level.world_shift <= level_limit[current_level_nr] and player.rect.x > 688:

                if current_level_nr == 0:
                    level_shift = True # aktiveerib loading screeni
                    level_shift_time = pygame.time.get_ticks()
                    pygame.mixer.stop() # lõpetab muusika esituse
                    pygame.mixer.music.stop()
                    current_enemy.enemy_flying.empty # kustutab olemasolevad vastased ära
                    current_enemy.enemy_ground.empty
                    current_level_nr = 1 # muudab leveli numbrit
                    stars = 0 # nullib tähed ära
                    current_level = levels[current_level_nr] # uued levelid jne
                    current_power = power_level[current_level_nr]
                    current_objects = objects_level[current_level_nr]
                    player.level = current_level
                    mustache = False # võtab surematuse maha

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
                    
            # maailma nihutamine
            if world_shift and living and not level_shift:
                # kui mängija liigub paremale, nihutame maailma vasakule
                if player.rect.x > 500 and current_level.world_shift > level_limit[current_level_nr]: # kui mängija on ekraanil 500. pixli juures
                    shift = player.rect.x- 500
                    player.rect.x = 500
                    current_level.shift_world(-shift)
                    current_enemy.shift_world(-shift)
                    current_power.shift_world(-shift)
                    current_objects.shift_world(-shift)
                # kui mängija liigub vasakule, nihutame maailma paremale
                elif player.rect.x < 240 and current_level.world_shift <0: # kui mängija on 240 pixli juures
                    shift = 240 - player.rect.x
                    player.rect.x = 240
                    current_level.shift_world(shift)
                    current_enemy.shift_world(shift)
                    current_power.shift_world(shift)
                    current_objects.shift_world(shift)
                # kui boss on elus, on level 3 ja maailm on piisavalt nihkunud
                if current_level_nr == 2 and boss_living and current_level.world_shift < -1692:
                    boss_shift = True # aktiveerib bossi nihkumine 
                    world_shift = False # tekistab maailma nihkumise
                    bomb_counter = 5 # pommi loenduri paneb 5
                    current_level.add_boss_wall() # lisab seina juurde, et mängija bossi juurest ära ei jookseks
                    current_enemy.spike_list.empty
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    running = False
                    state = 0
            player.left_right = 0
            pygame.event.clear()
            
        # Boss shift lõpp # 
        # uuendab platforme ja tausta
        current_level.update()
        
        # mängib teise leveli keskel heli
        if current_level_nr == 1 and current_level.world_shift < -1200 and ghost_sound:
            if sound:ghost_wav.play()
            ghost_sound = False
        # level 3 värgid
        elif current_level_nr ==2 and pygame.time.get_ticks() - plat_up_time > 1500 and level_shift == False:
            # lisab üles alla platformid
            current_level.add_plat_up("up")
            current_level.add_plat_up("down")
            if  current_level.world_shift > -1650: # lõpus ei lisa enam orasid
                current_enemy.add_enemy() 
            if boss_living and boss_hp < 226: # kui boss elab ja tal on elusid läinud, hakkab kirveid viskama
                current_enemy.boss_axe_throw()
            plat_up_time = pygame.time.get_ticks()
            bomb_counter +=1
            
        #--- kuvamised---#
            
        # tausta kuvamine
        current_level.draw(screen)
        current_objects.draw(screen)
        
        # mangija kuvamine ekraanile 
        player_sprite.draw(screen)

        # kui mängija elab ja surematus on peal
        if mustache and living:
            player.mustache(screen) # kuvab vuntsid
            current_objects.stach_timer(screen,when_stache)
            if pygame.time.get_ticks() - when_stache > 10000: # 10 sekundi pärast deaktiveerib
                    mustache = False

        # powerupid
        current_power.draw(screen)
        # vastaste kuvamine 
        current_enemy.draw(screen)

        # naljade kuvamine
        
        if joketime:
            # outline
            screen.blit(joke11, (text_x1-y1,100-y1))
            screen.blit(joke11, (text_x1-y1,100+y1))
            screen.blit(joke11, (text_x1+y1,100-y1))
            screen.blit(joke11, (text_x1+y1,100+y1))
            # tekst
            screen.blit(jokefont1.render(joke1, True, (141,224,130)), (text_x1,100))
            # teise rea kuvamine
            if pygame.time.get_ticks() - when_joke > 2500:
                if joke_play:
                    if sound:joke_wav.play()
                    joke_play = False
                # outline
                screen.blit(joke22, (text_x2-y2,140-y2))
                screen.blit(joke22, (text_x2-y2,140+y2))
                screen.blit(joke22, (text_x2+y2,140-y2))
                screen.blit(joke22, (text_x2+y2,140+y2))
                #tekst
                screen.blit(jokefont2.render(joke2, True, (141,224,130)), (text_x2,140))            
                if pygame.time.get_ticks() - when_joke > 7000:
                    joketime = False
                    
        # sihiku paigaldamine
        cx, cy = pygame.mouse.get_pos() # hiire positsioon
        screen.blit(cursor,(cx-38,cy-38))
        
        # tähtede kuvamine
        current_objects.stars(screen, stars)
        # kui teeme sohki, kuvame üleval nurgas linnukest
        if cheat:
            screen.blit(checked_img,(778,0))
        # kui mängija elab
        if living:
            # kui mängija kukub kuhugi või kui ta on level 3 liiga kõrgel
            if player.rect.y > 500 or (player.rect.y < -102 and current_level_nr == 2):
                if sound:death_wav_2.play()
                game_over_timer = pygame.time.get_ticks()
                living = False # mängija ei ela
                deadx = px # suremise kordinaadid
                deady = py                
            if not player.livingwall:
                game_over_timer = pygame.time.get_ticks()
                living = False
                if sound:death_wav.play()
                deadx = px
                deady = py
            if not player.living and not mustache  :
                game_over_timer = pygame.time.get_ticks()
                living = False
                if sound:death_wav.play()
                deadx = px
                deady = py
            else: #kui surematus on peal
                player.living = True
        else: # kui mängija ei ela
            screen.blit(player_dead,(deadx,deady+40)) # mängija laip
            player_sprite.empty() # kustutame mängija sprite ära
            walking.set_volume(0) #kõndimist pole kuulda
            current_enemy.enemy_flying.empty()
            screen.blit(youdied, (247,256)) # kuvame teksti ekraanile
            if pygame.time.get_ticks() - game_over_timer > 3000: # ootame 3 sekundit ja läheme tagasi menüü juurde
                state = 1
                break
            
        # kui bossi nihkumine toimub
        if boss_shift:
            # vaatab kas maailm on piisavalt nihkunud
            if current_level.world_shift > -2185:
                # nihutab kõike 3 pikslit iga tsükkel
                current_level.shift_world(-3)
                current_enemy.shift_world(-3)
                current_power.shift_world(-3)
                current_objects.shift_world(-3)
                player.rect.x -= 3
            else:
                boss_shift = False
                
        # loading screen
        if level_shift:
            # kuvab leveli pildi ekraanile
            screen.blit(level_logo[current_level_nr], (0,0))
            if pygame.time.get_ticks() - level_shift_time > 2000: # ootab 2 sekundit
                level_shift = False # lõpetab loading screeni ära
                current_enemy = enemy_level[current_level_nr] # lisab lendavad vastased
                current_enemy.add_ground_enemy() # lisab kõndivad vastased
                enemy_level[2].add_boss() # lisab bossi
                heli_level(current_level_nr, sound) # muudab helid
                
        # kui mäng saab läbi
        if game_credits:
            
            current_enemy.boss.empty() # eemaldab bossi ära
            screen.blit(game_credits_img,(0,0))
            if pygame.time.get_ticks() - game_credits_timer > 10800:
                state = 4
                break
        time.tick(60)
        pygame.display.flip() # uuendab tervet ekraani
        #pygame.display.set_caption("fps: " + str(round(time.get_fps())))
    return state,full_scr, sound, clean,current_level_nr

if __name__ == '__main__':
    
    # käivitab pygame moodulid jne, sätestame konstandid
    pygame.font.init()
    time = pygame.time.Clock()
    pygame.init()
    pygame.display.set_caption("Where's my burger")
    gamewidth = 800     # ekraani laius
    gameheight = 600    # ekraani kõrgus
    screen = pygame.display.set_mode((gamewidth, gameheight))
    mang = [0,0,0,0]    # tühi list
    color = (255,255,255) # menüü teksti värvid
    pygame.mouse.set_visible(False) # peidab tavalise hiire ära
    
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
    level_nr = font0.render("Level" , True, color)
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
    lvl1_img = pygame.image.load("Graphics/UI/lvl1.png").convert_alpha()
    lvl2_img = pygame.image.load("Graphics/UI/lvl2.png").convert_alpha()
    lvl3_img = pygame.image.load("Graphics/UI/lvl3.png").convert_alpha()
    level_select_img = pygame.image.load("Graphics/UI/nos.png").convert_alpha()
    
    # menüü taustad
    game_credits_img = pygame.image.load('Graphics/Background/credits.png').convert_alpha()
    player_dead = pygame.image.load('Graphics/Player/Dead.png').convert_alpha()
    level_logo = []
    for i in range(3):
        level_logo.append(pygame.image.load('Graphics/Background/Level'+str(i+1)+'.png').convert_alpha())
    boss_hp_bar = pygame.image.load('Graphics/UI/Boss/boss_hp.png').convert_alpha()
    boss_hp_bar_back = pygame.image.load('Graphics/UI/Boss/boss_hp_back.png').convert_alpha()
    youdied = pygame.image.load("Graphics/Background/Dead.png").convert_alpha() 
    
    # mangu heliefektid 
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
        if mang[0] == 0: # kui mängu pole varem mängitud
            menüü = menu()
        elif mang[0] == 1: # kui mängija kaotas
            menüü = menu(True, "bg_over.png", mang[1], mang[2], mang[3], mang[4])
        elif mang[0] == 4: # kui mängija tegi läbi
            menüü = menu(True, "bg_end.png", mang[1], mang[2], mang[3], 0)            
        if menüü[0] == 0: # kui paus on 
            mang = game(menüü[1], menüü[2], menüü[3], menüü[4])
        elif menüü[0] == 2 or menüü[0] == -1: break #ui menüüst pandi kinni
        if mang[0] == 0: break 

    pygame.quit()
