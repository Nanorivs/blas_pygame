from miniparts import *

player = create_player((30,600))
life_bar = create_life_bar(player["lives"])


def change_name(player:dict):
    pygame.mouse.set_visible(True)   
    
    def create_button(value:str,posicition:tuple,size:int=(60,80))->dict:
        new_button = {
        "value" : value,
        "hitbox" : pygame.Rect(posicition[0],posicition[1], size[0], size[1] )}
        return new_button

    letters = [
        create_button("q",(50,120)),create_button("w",(150,120)),create_button("e",(240,120)),create_button("r",(330,120)),create_button("t",(420,120)),create_button("y",(520,120)),create_button("u",(610,120)),create_button("i",(700,120)),create_button("o",(790,120)),create_button("p",(890,120)),
        create_button("a",(94,240)),create_button("s",(195,240)),create_button("d",(288,240)),create_button("f",(378,240)),create_button("g",(470,240)),create_button("h",(562,240)),create_button("j",(657,240)),create_button("k",(750,240)),create_button("l",(844,240)),
        create_button("z",(195,355)),create_button("x",(288,355)),create_button("c",(379,355)),create_button("v",(470,355)),create_button("b",(564,355)),create_button("n",(657,355)),create_button("m",(751,355))
]
    delete_button = pygame.Rect(123,473,100,100)
    confirm_button = pygame.Rect(900,500,100,100)


    while True:
        mouse_over_button = False
        for evento in pygame.event.get():

            if evento.type == pygame.QUIT:
                    terminar()

            if evento.type == MOUSEBUTTONDOWN:
                mouse_pos = evento.pos
             
                if len(player["name"]) < 10:
                    
                    for letter in letters:
                        if punto_en_rectangulo(mouse_pos,letter["hitbox"]):
                            SOUND_LETTER.play()
                            player["name"] += letter["value"]
                    

                if punto_en_rectangulo(mouse_pos,delete_button):
                    SOUND_DELETE.play()
                    string = player["name"]
                    player["name"] = string[:-1]
                    

                if punto_en_rectangulo(mouse_pos,confirm_button):
                    if len(player["name"])>0:
                        SOUND_OK.play()
                        menu()
                    else:
                        SOUND_ERROR.play()

        mouse_pos = pygame.mouse.get_pos()
        
        
        for letter in letters:
            if letter["hitbox"].collidepoint(mouse_pos):
                mouse_over_button = True
        if punto_en_rectangulo(mouse_pos,delete_button):
            mouse_over_button = True
        if punto_en_rectangulo(mouse_pos,confirm_button):
            mouse_over_button = True

                                
            
        if mouse_over_button:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        
        screen.blit(BACKGROUND_CHANGENAME,ORIGIN)
        mostrar_texto(screen,f"name:               ",FONT_MAIN_BIG,(400,80),BLACK)
        mostrar_texto(screen,player["name"],FONT_MAIN_BIG,(450,80),PINK)
        pygame.display.flip()
        


       


def gameover(player:dict,lifebar:list):
    gravity_concept["velocity_y"] = 0
    pygame.mouse.set_visible(True)        
    mouse_over_button = False
    give_up = pygame.Rect(600,440,200,50)
    tryagain_button = pygame.Rect(300,440,200,50)
    mouse_pos = None

    screen.blit(tint_surface,ORIGIN)
    mostrar_texto(screen,"GAME OVER",FONT_MAIN,(550,300),BLACK)
    pygame.display.flip()
    player["dead"] = False
    charge_lifebar(life_bar,3)
  
    while True:

        for evento in pygame.event.get():

            if evento.type == pygame.QUIT:
                    terminar()

            if evento.type == MOUSEBUTTONDOWN:
                mouse_pos = evento.pos
                if punto_en_rectangulo(mouse_pos,give_up):
                    save_score(player,"highscore.csv")
                    player["score"] = 0
                    ranking()
                if punto_en_rectangulo(mouse_pos,tryagain_button):
                    player["score"] = 0
                    if player["place"] == "level1":
                        level1()
                    else:
                        boss_1()
                    
        if draw_button(FONT_MAIN,"Menu",give_up, RED, WHITE, ranking):
            mouse_over_button = True
        if draw_button(FONT_MAIN,"Try Again",tryagain_button, GREEN, WHITE, level1):
            mouse_over_button = True

        
        if mouse_over_button:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

            pygame.display.flip()
    

def instructions():
    

    pygame.mouse.set_visible(True)        
    screen.blit(BACKGROUND_CONTROLS,ORIGIN)
    mouse_over_button = False
    mouse_pos = None
    while True:
        back_button = pygame.Rect(940,633,100,50)

        for evento in pygame.event.get():

            if evento.type == pygame.QUIT:
                    terminar()

            if evento.type == MOUSEBUTTONDOWN:
                mouse_pos = evento.pos
                if punto_en_rectangulo(mouse_pos,back_button):
                    
                    menu()
                    
        if draw_button(FONT_MAIN,"Back", back_button, LIGHT_BLUE, YELLOW, menu):
            mouse_over_button = True

        
        if mouse_over_button:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

            pygame.display.flip()



  

def ranking():
    pygame.mouse.set_visible(True)        
    screen.blit(BACKGROUND_RANKING,ORIGIN)
    mouse_over_button = False
    mouse_pos = None
    back_button = pygame.Rect(940,50,100,50)

    with open(get_path_actual("highscore.csv"),"r") as file:

        score_list = []

        header = file.readline()
        header_string = header.strip("\n").split(",")
        player,score = header_string

        content = file.readlines()

        for line in content:
            player_score = {}
            string = line.strip("\n").split(",")

            name,highscore = string
            player_score["name"] = name
            player_score["highscore"] = int(highscore)

            score_list.append(player_score)

        mostrar_texto(screen,f"{player}      ",FONT_MAIN,(400,100),PINK)
        mostrar_texto(screen,"     |",FONT_MAIN,(500,100),PINK)
        mostrar_texto(screen,f"{score}",FONT_MAIN,(700,100),PINK)
        mostrar_texto(screen,"--------------------------",FONT_MAIN,(520,120),PINK)

        left =  400
        top = 150
        left_score = 700
        for score in score_list:
            mostrar_texto(screen,f"{score["name"]}",FONT_MAIN,(left,top), BLACK)
            mostrar_texto(screen,"     |",FONT_MAIN,(500,top),PINK)
            mostrar_texto(screen,f"{score["highscore"]}",FONT_MAIN,(left_score,top), BLACK)
            top += 50
        

        
    while True:
    
        for evento in pygame.event.get():

            if evento.type == pygame.QUIT:
                    terminar()

            if evento.type == MOUSEBUTTONDOWN:
                mouse_pos = evento.pos
                if punto_en_rectangulo(mouse_pos,back_button):
                    menu()
                    
        if draw_button(FONT_MAIN,"Back", back_button, LIGHT_BLUE, YELLOW, menu):
            mouse_over_button = True

        if mouse_over_button:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

            pygame.display.flip()

def menu():
    
    save_score(player,"highscore.csv")
    rect_jugar = pygame.Rect(400, 200, 300, 50)
    rect_instrucciones = pygame.Rect(400, 300, 300, 50)
    rect_ranking = pygame.Rect(400, 400, 300, 50)
    rect_changename = pygame.Rect(400, 500, 300, 50)
    rect_salir = pygame.Rect(400, 600, 300, 50)

    if play_music["menu"]:
        music_load(MUSIC_MENU)
        music_play()
        play_music["menu"] = False

    pygame.mouse.set_visible(True)

    screen.blit(BACKGROUND_MENU,ORIGIN)

    pygame.display.flip()
    
    mouse_pos = None
    mostrar_texto(screen,"Blas",FONT_TITLE,(355,100),BLACK)
    mostrar_texto(screen,"Blas",FONT_TITLE,(350,100),YELLOW)

    while True:

        for evento in pygame.event.get():

            if evento.type == pygame.QUIT:
                    terminar()

            if evento.type == MOUSEBUTTONDOWN:
                mouse_pos = evento.pos
                if punto_en_rectangulo(mouse_pos,rect_jugar):
                    SOUND_OPTION.play()
                    level1()
                if punto_en_rectangulo(mouse_pos,rect_instrucciones):
                    SOUND_OPTION.play()
                    instructions()
                if punto_en_rectangulo(mouse_pos,rect_ranking):
                    SOUND_OPTION.play()
                    ranking()
                if punto_en_rectangulo(mouse_pos,rect_changename):
                    SOUND_OPTION.play()
                    change_name(player)
                if punto_en_rectangulo(mouse_pos,rect_salir):
                    SOUND_OPTION.play()
                    terminar()

        
        draw_button(FONT_MAIN,"Play", rect_jugar, LIGHT_BLUE, YELLOW, level1)
            
        draw_button(FONT_MAIN,"Controls",rect_instrucciones, LIGHT_BLUE, YELLOW, instructions)
            
        draw_button(FONT_MAIN,"Ranking", rect_ranking , LIGHT_BLUE, YELLOW, ranking)
            
        draw_button(FONT_MAIN,"Change name", rect_changename , LIGHT_BLUE, YELLOW, change_name)
            
        draw_button(FONT_MAIN,"Exit", rect_salir , RED, YELLOW, exit)
            
    
        pygame.display.flip()


def level1():
    

    music_load(MUSIC_LVL1)
    music_volume(300)
    music_play(100)
    ground = create_ground(TEXTURE_GROUND,(0,650))
    platform = create_platform_lvl1()
    move_platform = create_move_platform_lvl1()
    spikes_platform = create_spikes_platform_lvl1()
    enemies = create_enemies_platform_lvl1()
    balls = []
    hit_enemies = []
    coins = create_coins_list_lvl1()
    explosions = []
    heart_items = []
    items_to_remove = []

    door = create_door((10,500))

    player["place"] = "level1"
    player["rect"].center = (30,600)

    move_left = False
    move_right = False
    flag_muted = False

    heart_items.append(create_item_heart((140,333)))
    keys = []
    keys.append(create_item_key((1020,50)))
    # Bucle principal del juego
    while True:
        teclas = pygame.key.get_pressed()
        clock.tick(FPS)
        change_frame = False
        player["run"] = False

        for evento in pygame.event.get():
            if evento.type == QUIT:
                pygame.quit()
                sys.exit()
            
                
            if evento.type == KEYDOWN:
                if not player["dead"]:
                    if evento.key == K_SPACE and  gravity_concept["is_jumping"] == False  and  gravity_concept["velocity_y"] == 0:
                        gravity_concept["velocity_y"] = JUMP_STRENGTH
                        gravity_concept["is_jumping"] = True
                        SOUND_JUMP.play()


                    if evento.key == K_a:
                        move_left = True
                        move_right = False
                        player["last_pose_left"] = True
                
                    if evento.key == K_d:
                        move_right = True
                        move_left = False
                        player["last_pose_left"] = False

                    if evento.key == K_m:
                        if not flag_muted:
                            mute(sounds)
                            flag_muted = True
                        else:
                            mute(sounds,mute=False)
                            flag_muted = False
                           
                       
                    if evento.key == K_p: 
                    
                        pygame.mixer.music.pause()
                        SOUND_PAUSE.play()
                        screen.blit(tint_display((BLACK)),ORIGIN)
                        mostrar_texto(screen,"Pause",FONT_MAIN,SCREEN_CENTER)
                        pygame.display.flip()
                        wait_user(K_p)
                    
                        if not flag_muted :
                            SOUND_PAUSE.play()
                            pygame.mixer.music.unpause()

                    if evento.key == K_RSHIFT:
                        player["attack"] = True
                        SOUND_BALL.play()
                        pygame.time.set_timer(FRAME_ATTACK_TIME,400)

                        if player["last_pose_left"]:
                            balls.append(create_ball(player["rect"].midleft,True))
                        else:
                            balls.append(create_ball(player["rect"].midright,False))

            if evento.type == KEYUP:
                if evento.key == K_a :    
                    move_left = False
                if evento.key == K_d:
                    move_right = False

            if evento.type == FRAMES_TIMER:
                change_frame = True

            if evento.type == DAMAGE_COUTDOWN:
                pygame.time.set_timer(DAMAGE_COUTDOWN,0)
                player["take_damage"] = False
                pygame.time.set_timer(DAMAGE_ACTIVATE,FPS * 20)

            if evento.type == DAMAGE_ACTIVATE:
                pygame.time.set_timer(DAMAGE_ACTIVATE,0)
                player["take_damage"] = True
                player["hit"] = False

            if evento.type == ENEMY_HIT_COUTDOWN:
                pygame.time.set_timer(ENEMY_HIT_COUTDOWN,0)
                for enemy in hit_enemies[:]:
                    enemy["hit"] = False
                    hit_enemies.remove(enemy)

            if evento.type == FRAME_ATTACK_TIME:
                pygame.time.set_timer(FRAME_ATTACK_TIME,0)
                player["attack"] = False

              
            if evento.type == TIME_OUT:
                pygame.time.set_timer(TIME_OUT, 0)
                gameover(player,life_bar)
      
        #-------------------------------------------------------MOVEMENTS------------------------------------------------#

        #PLAYER
        gravity_concept["velocity_y"] += GRAVITY
        player["rect"].top += gravity_concept["velocity_y"]

        if teclas[K_LSHIFT] and (move_left or move_right):
            player["run"] = True
            player["speed"] = PLAYER_SPEED + 3
            
        else:
             player["speed"] = PLAYER_SPEED

            
        if not player["dead"]:
                move_left_rect(player,move_left,0)
                move_right_rect(player,move_right,WIDTH)       
       
        #BALL
        move_balls(balls)

        #PLATFORM
        platform_movement(move_platform)
        platform_movement(enemies)
 
        #----------------------------------------------------COLLISION-----------------------------------------------------#

        #GROUND
        fall_in_surface(player["rect"],ground["rect"])

        #PLATFORM
        if gravity_concept["velocity_y"] >  0:
                player_on_static_platforms(player["rect"],platform)
                player_on_move_platforms(player["rect"],move_platform)
        
        if not player["dead"]:
        
            #SPIKES
            for spikes in spikes_platform:
                if detectar_colision(player["rect"],spikes["rect"]):
                    player["dead"] = True
                    
                    life_bar.clear()
                    music_stop()
                    SOUND_DEATH.play()
                    break

            #PLAYER TOUCHS OPEN DOOR
            if door["open"] and player["rect"].midbottom == door["rect"].midbottom:
                boss_1()
            #PLAYER TOUCHS COINS
            for coin in coins[:]:
                if detectar_colision(player["rect"],coin["rect"]):
                    player["score"] += 50
                    coins.remove(coin)
                    SOUND_COIN.play()
            
            #PLAYER TOUCHS HEART ITEMS
            for heart in heart_items:
                if detectar_colision(player["rect"],heart["rect"]):
                    charge_lifebar(life_bar,1)
                    SOUND_ITEM_HEART.play()
                    items_to_remove.append(heart)
            
            #PLAYER TOUCHS KEYS
            for key in keys:
                if detectar_colision(player["rect"],key["rect"]):
                    door["move_frames"] = True
                    door["open"] = True
                    SOUND_ITEM_KEY.play()
                    items_to_remove.append(key)

            #PLAYER TOUCHS ENEMIES
            if player["take_damage"]:
               
                for enemy in enemies:
                    if detectar_colision(player["rect"],enemy["rect"]):
                        if len(life_bar) >= enemy["damage"]:
                                for i in range(enemy["damage"]):
                                    life_bar.pop()
                                player["hit"] = True
                                pygame.time.set_timer(DAMAGE_COUTDOWN,1)
                                SOUND_HURT.play()

                if len(life_bar) == 0:
                    player["dead"] = True
                    music_stop()
                    SOUND_DEATH.play()

            #BALL TOUCHES ENEMIES
            for ball in balls:
                for enemy in enemies[:]:

                    if detectar_colision(ball["rect"],enemy["rect"]):
                        if not enemy["hit"]:
                            items_to_remove.append(ball)
                            enemy["life"] -= player["damage"]
                            enemy["hit"] = True
                            SOUND_ENEMY_HURT.play()
                            if enemy["life"] < 1:
                                player["score"] += 100
                                explosions.append(create_white_explosion(enemy["rect"].center,enemy["size"]))
                                enemies.remove(enemy)
                                SOUND_EXPLOSION.play()
                            else:
                                hit_enemies.append(enemy)
                                pygame.time.set_timer(ENEMY_HIT_COUTDOWN,FPS * 6)

                
                 
        #-----------------------------------------------------FRAMES---------------------------------------------------------#            
        if change_frame :
               
                #ENEMIES
                update_enemy_frames(enemies)

                #LIFE BAR
                update_statics_blocks_frames(life_bar)

                #COINS
                update_statics_blocks_frames(coins)

                #HEARTS
                update_statics_blocks_frames(heart_items)

                #KEYS
                update_statics_blocks_frames(keys)

                #EXPLOSIONS
                update_statics_blocks_frames(explosions,temporal=True,remove_list=items_to_remove)

                #"DOOR"
                move_frames(door)

                #PLAYER
                if gravity_concept["is_jumping"]: 
                    update_character_frame(player,"jump")

                else:

                    if player["run"]:
                        update_character_frame(player,"run")
                    else:
                        update_character_frame(player,"walk")
                        
                    if not move_left and not move_right:
                        update_character_frame(player,"idle")
                        

                if player["attack"]:
                        update_character_frame(player,"attack")
                if player["hit"] :
                        player["img"] = tint_image(player["img"],RED)
                if player["dead"] :
                    update_character_frame(player,"death")
                    
                    if player["frames"]["death"]["universal_frame_index"] == 0:
                        pygame.time.set_timer(TIME_OUT, FPS)


        #------------------------------------------------------REMOVE ITEMS-----------------------------------------------

        remove_item(balls,items_to_remove)
        remove_item(explosions,items_to_remove)
        remove_item(heart_items,items_to_remove)
        remove_item(keys,items_to_remove)


        items_to_remove.clear()

                     
        #-------------------------------------------------------PRINT------------------------------------------------------
   
        screen.blit(BACKGROUND_LVL1,ORIGIN)
        screen.blit(door["img"],door["rect"])
        blit_static_surface(coins)
        blit_static_surface(platform)
        blit_static_surface(life_bar)
        blit_static_surface(move_platform)
        blit_static_surface(spikes_platform)
        blit_static_surface(enemies)
        blit_static_surface(balls)
        blit_static_surface(heart_items)
        blit_static_surface(keys)
        screen.blit(ground["img"],ground["rect"])
        screen.blit(player["img"],player["rect"])
        blit_static_surface(explosions)
        mostrar_texto(screen,f"score:  {player["score"]}",FONT_MAIN,(500,30),PINK)
      

        pygame.display.flip()

def boss_1():

    music_load(MUSIC_BOSS1)
    music_play(100)
    flag_muted = False
    move_platform = create_move_platform_lvl2()
    balls = []
    explosions = []
    heart_list = []
    create_hearts_items_boss1(heart_list)
    items_to_remove = []
    platform_boss1 = create_platform_boss1()
    
    door = create_door((933,0))

    boss = create_boss_lv1()

    player["place"] = "boss1"
    player["rect"].center = (970,0)

    move_left = False
    move_right = False

    boss_dead = False
   

    # Bucle principal del juego
    while True:
        teclas = pygame.key.get_pressed()
        clock.tick(FPS)
        change_frame = False
        player["run"] = False
        

        mostrar_texto(screen,f"score:{player["score"]}",FONT_MAIN,(500,30),PINK)
        for evento in pygame.event.get():
            if evento.type == QUIT:
                pygame.quit()
                sys.exit()
            
                
            if evento.type == KEYDOWN:
                if not player["dead"]:
                    if evento.key == K_SPACE and  gravity_concept["is_jumping"] == False  and  gravity_concept["velocity_y"] == 0:
                        gravity_concept["velocity_y"] = JUMP_STRENGTH
                        gravity_concept["is_jumping"] = True
                        SOUND_JUMP.play()


                    if evento.key == K_a:
                        move_left = True
                        move_right = False
                        player["last_pose_left"] = True
                
                    if evento.key == K_d:
                        move_right = True
                        move_left = False
                        player["last_pose_left"] = False

                    if evento.key == K_m:
                        if not flag_muted:
                            mute(sounds)
                            flag_muted = True
                            print(flag_muted)
                        else:
                            mute(sounds,mute=False)
                            flag_muted = False
                            print(flag_muted)
                       

                    if evento.key == K_p: 
                        pygame.mixer.music.pause()
                        SOUND_PAUSE.play()
                        screen.blit(tint_display((BLACK)),ORIGIN)
                        mostrar_texto(screen,"Pause",FONT_MAIN,SCREEN_CENTER)
                        pygame.display.flip()
                        wait_user(K_p)
                        if not flag_muted :
                            SOUND_PAUSE.play()
                            pygame.mixer.music.unpause()
                                
                    if evento.key == K_RSHIFT:
                        player["attack"] = True
                        SOUND_BALL.play()
                        pygame.time.set_timer(FRAME_ATTACK_TIME,500)

                        if player["last_pose_left"]:
                            balls.append(create_ball(player["rect"].midleft,True))
                        else:
                            balls.append(create_ball(player["rect"].midright,False))

            if evento.type == KEYUP:
                if evento.key == K_a :    
                    move_left = False
                if evento.key == K_d:
                    move_right = False

            if evento.type == FRAMES_TIMER:
                change_frame = True

            if evento.type == DAMAGE_COUTDOWN:
                pygame.time.set_timer(DAMAGE_COUTDOWN,0)
                player["take_damage"] = False
                pygame.time.set_timer(DAMAGE_ACTIVATE,FPS * 20)

            if evento.type == DAMAGE_ACTIVATE:
                pygame.time.set_timer(DAMAGE_ACTIVATE,0)
                player["take_damage"] = True
                player["hit"] = False

            if evento.type == ENEMY_HIT_COUTDOWN:
                pygame.time.set_timer(ENEMY_HIT_COUTDOWN,0)
                boss["hit"] = False
                
            if evento.type == FRAME_ATTACK_TIME:
                pygame.time.set_timer(FRAME_ATTACK_TIME,0)
                player["attack"] = False

            if evento.type == TIME_OUT:
                pygame.time.set_timer(TIME_OUT, 0)
                gameover(player,life_bar)
            
        #-------------------------------------------------------MOVEMENTS------------------------------------------------#

        #PLAYER
        gravity_concept["velocity_y"] += GRAVITY
        player["rect"].top += gravity_concept["velocity_y"]

        if teclas[K_LSHIFT] and (move_left or move_right):
            player["run"] = True
            player["speed"] = PLAYER_SPEED + 3
            
        else:
             player["speed"] = PLAYER_SPEED

            
        if not player["dead"]:
                move_left_rect(player,move_left,0)
                move_right_rect(player,move_right,WIDTH)       
       
        #BALL
        move_balls(balls)

        #PLATFORM
        platform_movement(move_platform)

        #BOSS
        if boss["life"] > 0:
            move_boss1(boss,player)
        else:
            boss["rect"].bottom += GRAVITY * 3
            
            if not boss_dead:
                SOUND_HASTA_LA_VISTA_BABY.play()
                boss_dead = True
        #----------------------------------------------------COLLISION-----------------------------------------------------#

        #PLATFORM
        if gravity_concept["velocity_y"] >  0:
                player_on_static_platforms(player["rect"],platform_boss1)
                player_on_move_platforms(player["rect"],move_platform)
        
        if not player["dead"]:
 
            #PLAYER TOUCHS OPEN DOOR
            if door["open"] and rectangulo_en_mitad_rectangulo2(player["rect"],door["rect"]):
                music_stop()
                menu()
 
            #PLAYER TOUCHS HEART ITEMS
            for heart in heart_list:
                if detectar_colision(player["rect"],heart["rect"]):
                    charge_lifebar(life_bar,1)
                    items_to_remove.append(heart)
                    SOUND_ITEM_HEART.play()
            

            #PLAYER TOUCHS ENEMIES
            if player["take_damage"]:
               if boss["life"] > 0:
                    if detectar_colision(player["rect"],boss["rect"]):
                        if len(life_bar) >= boss["damage"]:
                                for i in range(boss["damage"]):
                                    life_bar.pop()
                                player["hit"] = True
                                pygame.time.set_timer(DAMAGE_COUTDOWN,1)
                                SOUND_HURT.play()

            if len(life_bar) == 0:
                player["dead"] = True
                music_stop()
                SOUND_DEATH.play()

            #BALL TOUCHES ENEMIES
            for ball in balls:
            
                if detectar_colision(ball["rect"],boss["rect"]):
                    if not boss["hit"]:
                        items_to_remove.append(ball)
                        boss["life"] -= player["damage"]
                        boss["hit"] = True
                        player["score"] += 50
                        SOUND_ENEMY_HURT.play()
                        if boss["life"] < 1:
                            player["score"] += 1000
                            door["move_frames"] = True
                            door["open"] = True
                            SOUND_ITEM_KEY.play()
                            explosions.append(create_white_explosion(boss["rect"].center,BOSS1_SIZE))
                            boss["img"] = BOSS1_DEATH["frames"][0]
                            SOUND_EXPLOSION.play()
                        else:
                            pygame.time.set_timer(ENEMY_HIT_COUTDOWN,FPS * 6)

            #PLAYER FALLS
            if player["rect"].top > HEIGHT:
                life_bar.clear()
            

            
        #-----------------------------------------------------FRAMES---------------------------------------------------------#            
        if change_frame :
               
                #ENEMIES
                if boss["life"] > 0:
                    update_boss1_frames(boss)
                elif boss["rect"].top < HEIGHT:
                    if len(explosions) == 0:
                        explosions.append(create_white_explosion(boss["rect"].topleft,BOSS1_SIZE))
                        explosions.append(create_white_explosion(boss["rect"].topright,BOSS1_SIZE))
                        explosions.append(create_white_explosion(boss["rect"].midbottom,BOSS1_SIZE))
                    SOUND_EXPLOSION.play()

                #LIFE BAR
                update_statics_blocks_frames(life_bar)

                #HEARTS
                update_statics_blocks_frames(heart_list)

                #EXPLOSIONS
                update_statics_blocks_frames(explosions,temporal=True,remove_list=items_to_remove)

                #"DOOR"
                move_frames(door)

                #PLAYER
                if gravity_concept["is_jumping"]: 
                    update_character_frame(player,"jump")

                else:

                    if player["run"]:
                        update_character_frame(player,"run")
                    else:
                        update_character_frame(player,"walk")
                        
                    if not move_left and not move_right:
                        update_character_frame(player,"idle")
                        

                if player["attack"]:
                        update_character_frame(player,"attack")
                if player["hit"] :
                        player["img"] = tint_image(player["img"],RED)
                if player["dead"] :
                    update_character_frame(player,"death")
                    
                    if player["frames"]["death"]["universal_frame_index"] == 0:
                        pygame.time.set_timer(TIME_OUT, FPS)


        #------------------------------------------------------REMOVE ITEMS-----------------------------------------------

        remove_item(balls,items_to_remove)
        remove_item(explosions,items_to_remove)
        remove_item(heart_list,items_to_remove)

        items_to_remove.clear()

                     
        #-------------------------------------------------------PRINT------------------------------------------------------
   
        screen.blit(BACKGROUND_BOSS1,ORIGIN)
        screen.blit(door["img"],door["rect"])
        blit_static_surface(life_bar)
        blit_static_surface(move_platform)
        blit_static_surface(platform_boss1)
        blit_static_surface(balls)
        blit_static_surface(heart_list)
        screen.blit(player["img"],player["rect"])
        screen.blit(boss["img"],boss["rect"])
        blit_static_surface(explosions)
        mostrar_texto(screen,f"score:{player["score"]}",FONT_MAIN,(500,30),PINK)
 

      

        pygame.display.flip()

