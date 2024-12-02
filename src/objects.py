from functions import *
from settings import *
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
MAGENTA = (255,0,255)
YELLOW = (255,255,0)
CYAN = (0,255,255)

LIGHT_BLUE = (135, 206, 235)

#GAMEOVER TRANSPARENT SURFACE
tint_surface = pygame.Surface(SCREEN_SIZE)
tint_alpha = 128  # Valor de transparencia (0-255)
tint_surface.fill(RED)
tint_surface.set_alpha(tint_alpha)


def tint_display(color:tuple):
    tint_surface = pygame.Surface(SCREEN_SIZE)
    tint_alpha = 128  # Valor de transparencia (0-255)
    tint_surface.fill(color)
    tint_surface.set_alpha(tint_alpha)
    return tint_surface

def tint_image(image, color):
    tinted_image = image.copy()
    tint_surface = pygame.Surface(image.get_size())
    tint_surface.fill(color)
    tinted_image.blit(tint_surface, (0, 0), special_flags=pygame.BLEND_RGB_ADD)
    return tinted_image



def create_player(position:tuple)->dict:
    player = create_block(PLAYER_FRAMES_IDLE["frames"][0],position[0],position[1],PLAYER_WIDTH,PLAYER_HEIGHT)
    player["frames"] = FRAMES_PLAYER
    player["dead"] = False  
    player["last_pose_left"] = False
    player["run"] = False
    player["speed"] = PLAYER_SPEED
    player["take_damage"] = True
    player["hit"] = False
    player["damage"] = PLAYER_DAMAGE
    player["attack"] = False
    player["score"] = 0
    player["place"] = ""
    player["lives"] = 3
    player["name"] = "player"
    return player

def create_ball(position:tuple,last_pose_left:bool):
    """ position (tuple): (x,y)
    Returns: dict with rect ,image and position on "rect","img" """
    ball = create_block(BALL,position[0],position[1],BALL_SIZE[0],BALL_SIZE[1])
    ball["last_pose_left"] = last_pose_left
    ball["left_limit"] = BALL_LEFT_LIMIT
    ball["right_limit"] = BALL_RIGHT_LIMIT
    ball["speed"] = BALL_SPEED
    return ball

def create_movement_block(image,top,left,left_limit,right_limit,width,height,speed)->dict:
    movement_block = create_block(image,left,top,width,height)
    movement_block["left_limit"] = left_limit
    movement_block["right_limit"] = right_limit
    movement_block["reverse"] = False
    movement_block["speed"] = speed
    return movement_block

def create_static_block_frames(position:tuple,size:tuple,frames:dict):
    new_block = create_block(frames["frames"][0],position[0],position[1],size[0],size[1])
    new_block["frames"] = frames
    return new_block

def create_coin(position:tuple):
    return create_static_block_frames(position,SIZE_COIN,FRAMES_COIN)

def create_heart(position:tuple):
    return create_static_block_frames(position,SIZE_HEART,FRAMES_HEART)

def create_white_explosion(position:tuple,size:tuple):
    return create_static_block_frames(position,size,FRAMES_EXPLOSION)

def create_item_heart(position:tuple):
    return create_static_block_frames(position,SIZE_ITEM_HEART,FRAMES_ITEM_HEART)

def create_item_key(position:tuple):
    return create_static_block_frames(position,SIZE_ITEM_KEY,FRAMES_ITEM_KEY)

def create_door(position:tuple):
    door =  create_static_block_frames(position,SIZE_DOOR,FRAMES_DOOR)
    door["open"] = False
    return door

def create_short_platform(texture,position:tuple)->dict:
    return create_block(texture,position[0],position[1],SIZE_GRASS_SHORT[0],SIZE_GRASS_SHORT[1])
    
def create_long_platform(texture,position:tuple)->dict:
    return create_block(texture,position[0],position[1],SIZE_GRASS_LONG[0],SIZE_GRASS_LONG[1])

def create_hearts_items_boss1(heart_list:list):
    heart_list.append(create_item_heart((68,350)))
    heart_list.append(create_item_heart((986,350)))
    heart_list.append(create_item_heart((70,98)))
    heart_list.append(create_item_heart((490,240)))
    heart_list.append(create_item_heart((490,450)))
    
def create_coins_list_lvl1()->list:
    coins = []
    left = 190
    top = 510
  
    #lower row
    for i in range(14):
        coins.append(create_coin(position=(left,top)))
        left += SIZE_COIN[0]
    #middle row
    coins.append(create_coin(position=(583,337)))
    coins.append(create_coin(position=(618,301)))
    coins.append(create_coin(position=(664,269)))
    coins.append(create_coin(position=(723,267)))
    coins.append(create_coin(position=(771,296)))
    coins.append(create_coin(position=(813,342)))
    #upper row
    left = 316
    top = 50
    for i in range(13):
        coins.append(create_coin(position=(left,top)))
        left+= SIZE_COIN[0]

    return coins



def create_life_bar(hearts:int)->list:
    lives = []
    left = 5
    top = 5
    for i in range(hearts):
        lives.append(create_heart(position=(left,top)))
        left += SIZE_HEART[0]
    return lives

def create_platform_lvl1()->list:
    platform = []
    #up one level =  -130
    platform.append(create_short_platform(TEXTURE_GRASS_SHORT,(895,560)))
    platform.append(create_short_platform(TEXTURE_GRASS_SHORT,(895,430)))
    platform.append(create_short_platform(TEXTURE_GRASS_SHORT,(400,385)))
    platform.append(create_short_platform(TEXTURE_GRASS_SHORT,(80,385)))
    platform.append(create_short_platform(TEXTURE_GRASS_SHORT,(0,255)))
    platform.append(create_long_platform(TEXTURE_GRASS_LONG,(300,100)))
    return  platform

def create_platform_boss1()->list:
    platform_2 = []
    #up one level =  -130
    platform_2.append(create_short_platform(TEXTURE_GRASS_SHORT,(880,130)))
    platform_2.append(create_short_platform(TEXTURE_GRASS_SHORT,(0,145)))
    platform_2.append(create_long_platform(TEXTURE_GRASS_LONG,(100,300)))
    platform_2.append(create_long_platform(TEXTURE_GRASS_LONG,(100,500)))
    platform_2.append(create_short_platform(TEXTURE_GRASS_SHORT,(915,400)))
    platform_2.append(create_short_platform(TEXTURE_GRASS_SHORT,(0,400)))

    
    return  platform_2




def create_move_platform_lvl1()->list:
    platform = []
    platform.append(create_movement_block(image=TEXTURE_FLOATING_GROUND,left=800,top=560,left_limit=30,right_limit=895,width=100,height=50,speed=5))
    return  platform

def create_move_platform_lvl2()->list:
    platform = []
    platform.append(create_movement_block(image=TEXTURE_FLOATING_GROUND,left=0,top=640,left_limit=0,right_limit=WIDTH,width=250,height=50,speed=20))
    return  platform



def create_spikes_platform_lvl1():
    platform = []
    #Air spikes
    platform.append(create_block(image=TEXTURE_AIR_SPIKE,left=290,top=380,width=80,height=80))
    platform.append(create_block(image=TEXTURE_AIR_SPIKE,left=0,top=380,width=80,height=80))
    platform.append(create_block(image=TEXTURE_AIR_SPIKE,left=700,top=380,width=80,height=80))
    platform.append(create_block(image=TEXTURE_AIR_SPIKE,left=620,top=380,width=80,height=80))
    #Ground spikes
    platform.append(create_block(image=TEXTURE_SPIKES_PLATFORM,left=150,top=600,width=SIZE_GROUND[0],height=SIZE_GROUND[1]))
    return  platform

def create_enemy(position:tuple,size:tuple,limits:tuple,damage:int,frames:dict,life:int,speed:int):
    """ position (tuple): posicion inicial (X;Y)
        size (tuple):  (width,height)
        limits (tuple): (left limit X,left limit X)
        damage(int): enemy damage
        frames (dict): dict with images on key"frames" 
        life(int): enemy life
        speed(int): enemy speed   """
    enemy = create_movement_block(image=frames["walk"][0],left=position[0],top=position[1],left_limit=limits[0],right_limit=limits[1],width=size[0],height=size[1],speed=speed)
    enemy["damage"] = damage
    enemy["life"] = life
    enemy["speed"] = speed
    enemy["frames"] = frames
    enemy["current_frame"] = 0
    enemy["reverse"] = False
    enemy["hit"] = False
    return enemy

def create_enemy_flyingrobot(position:tuple,limits:tuple):
    return create_enemy(position,ENEMY_FLYINGROBOT_SIZE,limits,ENEMY_FLYINGROBOT_DAMAGE,FRAMES_FLYINGROBOT,ENEMY_FLYINGROBOT_LIFE,ENEMY_FLYINGROBOT_SPEED)

def create_enemy_gummy(position:tuple,limits:tuple):
    return create_enemy(position,ENEMY_GUMMY_SIZE,limits,ENEMY_GUMMY_DAMAGE,FRAMES_GUMMY,ENEMY_GUMMY_LIFE,ENEMY_GUMMY_SPEED)

def create_enemy_worm(position:tuple,limits:tuple):
    return create_enemy(position,ENEMY_WORM_SIZE,limits,ENEMY_WORM_DAMAGE,FRAMES_WORM,ENEMY_WORM_LIFE,ENEMY_WORM_SPEED)

def create_enemy_slime(position:tuple,limits:tuple):
    return create_enemy(position,ENEMY_SLIME_SIZE,limits,ENEMY_SLIME_DAMAGE,FRAMES_SLIME,ENEMY_SLIME_LIFE,ENEMY_SLIME_SPEED)

def create_enemy_robotrabbit(position:tuple,limits:tuple):
    return create_enemy(position,ENEMY_ROBOTRABBIT_SIZE,limits,ENEMY_ROBOTRABBIT_DAMAGE,FRAMES_ROBOTRABBIT,ENEMY_ROBOTRABBIT_LIFE,ENEMY_ROBOTRABBIT_SPEED)

def create_ground(texture,position:tuple)->dict:
    return  create_block(texture,position[0],position[1],SIZE_GROUND[0],SIZE_GROUND[1])

def create_enemies_platform_lvl1()->list:
    enemies_list = []
    enemies_list.append(create_enemy_flyingrobot((213,276),(0,WIDTH)))
    enemies_list.append(create_enemy_gummy((985,390),(885,WIDTH)))
    enemies_list.append(create_enemy_worm((400,340),(400,600)))
    enemies_list.append(create_enemy_slime((0,170),(0,200)))
    enemies_list.append(create_enemy_robotrabbit((306,20),(306,WIDTH)))

    return  enemies_list

def create_boss_lv1()->dict:

    boss1 = create_block(BOSS1_WALK["frames"][0],0,0,BOSS1_SIZE[0],BOSS1_SIZE[1])
    boss1["life"] = BOSS1_LIFE
    boss1["frames"] = FRAMES_BOSS1
    boss1["dead"] = False  
    boss1["last_pose_left"] = False
    boss1["speed"] = BOSS1_SPEED
    boss1["take_damage"] = True
    boss1["hit"] = False
    boss1["damage"] = BOSS1_DAMAGE
    boss1["move_left"] = False
    boss1["move_right"] = False
    boss1["move_up"] = False
    boss1["move_down"] = False
    boss1["move_same"] = False


    return boss1

def charge_lifebar(life_bar:list,lives:int):
    
    for i in range(lives):
        if len(life_bar) == 0:
              life_bar.append(create_heart((5,5)))  

        else:  
            left = life_bar[-1]["rect"].right 
            top = life_bar[-1]["rect"].top
            life_bar.append(create_heart((left,top)))

def music_load(adress:str):
    pygame.mixer.music.load(adress)

def music_play(loops = 0,):
    pygame.mixer.music.play(loops)
def music_stop():
    pygame.mixer.music.stop()

def music_volume(volume:float = (0.1)):
    pygame.mixer.music.set_volume(volume)

def music_pause():
    pygame.mixer.music.pause()

def music_unpause():
    pygame.mixer.music.unpause()

def flip_image(image,horizontal:bool = True,vertical:bool = False):
    return pygame.transform.flip(image,horizontal,vertical)


