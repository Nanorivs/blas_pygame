from functions import *
import pygame
from pygame.locals import *

#IMPORT FRAMES FUNCTION

def amount_elements_path(ruta):
    """Contar elementos de un directorio

    Args:
        ruta (string): directorio del archivo

    Returns:
        int: cantidad de elementos del directorio
    """
    import os
    try:
        # Obtener la lista de elementos en la carpeta
        elementos = os.listdir(ruta)
        # Contar los elementos
        return len(elementos)
    except FileNotFoundError:
        return "La carpeta no existe"
    except NotADirectoryError:
        return "La ruta especificada no es una carpeta"
    except PermissionError:
        return "Permiso denegado para acceder a la carpeta"

def create_frames_dict(path_frames:str,object_size:tuple,extension:str = "png")->dict:
    """Carpeta con frames a diccionario con :
                "frames" : tupla de frames
                "amount" : cantidad de frames
                "extension" : extension del frame "png" "jpg"...

    Args:
        path_frames (str): directorio con los frames general  ->  ...assets/player/jump/  
        object_size (tuple):ancho y largo del objeto a pintar con el frame    """
    frames_list =  []

    amount_frames = amount_elements_path(path_frames)
    for i in range(amount_frames):
        image = pygame.transform.scale(pygame.image.load(f"{path_frames}{i}.{extension}"),object_size)
        frames_list.append(image)
    frames_list = tuple(frames_list)

    return {
        "frames" : frames_list,
        "amount" : amount_frames,
        "universal_frame_index" : 0}
#Score
highscore = [0]
score = [0]

#display
WIDTH = 1080
HEIGHT = 720
SCREEN_SIZE = ( WIDTH,HEIGHT)
SCREEN_MIDDLE_WIDTH =WIDTH // 2
SCREEN_MIDDLE_HEIGHT = HEIGHT // 2
SCREEN_CENTER = (SCREEN_MIDDLE_WIDTH,SCREEN_MIDDLE_HEIGHT)
ORIGIN = (0,0)

# Inicializar Pygame
pygame.init()

# Configurar la pantalla
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Blas")

# Configurar el reloj
clock = pygame.time.Clock()


play_music = {
    "menu" : True
}

#clock
FPS = 60

#rect = pygame.Rect((0,0),(1,2))
#Events
FRAMES_TIMER = USEREVENT + 1
pygame.time.set_timer(FRAMES_TIMER,100)

TIME_OUT = USEREVENT + 2
DAMAGE_COUTDOWN = USEREVENT + 3
DAMAGE_ACTIVATE = USEREVENT + 4

ENEMY_HIT_COUTDOWN = USEREVENT + 5

FRAME_ATTACK_TIME = USEREVENT + 6





#Player-----------------------------------------------------------------------------------------------------------------------------
PLAYER_WIDTH = 70
PLAYER_HEIGHT = 70
PLAYER_SIZE = (PLAYER_WIDTH,PLAYER_HEIGHT)

##############################################################  SPRITES  #################################################################
# ------player--------------------------------------------------------------------------------------------------------------------
PLAYER_SPEED = 5
PLAYER_DAMAGE = 1
PLAYER_FRAMES_IDLE =  create_frames_dict("./src/assets/characters/player/idle/",PLAYER_SIZE,"png")
PLAYER_FRAMES_WALK = create_frames_dict("./src/assets/characters/player/walk/",PLAYER_SIZE,"png") 
PLAYER_FRAMES_RUN = create_frames_dict("./src/assets/characters/player/run/",PLAYER_SIZE,"png") 
PLAYER_FRAMES_JUMP = create_frames_dict("./src/assets/characters/player/jump/",PLAYER_SIZE,"png") 
PLAYER_FRAMES_DEATH = create_frames_dict("./src/assets/characters/player/death/",PLAYER_SIZE,"png") 
PLAYER_FRAMES_ATTACK = create_frames_dict("./src/assets/characters/player/attack/",PLAYER_SIZE,"png")

BALL_SPEED = 9
BALL_WIDTH = 20
BALL_HEIGHT = 20
BALL_SIZE = (BALL_WIDTH,BALL_HEIGHT)
BALL_LEFT_LIMIT = 0 - BALL_WIDTH
BALL_RIGHT_LIMIT = WIDTH + BALL_WIDTH
BALL = pygame.transform.scale((pygame.image.load("./src/assets/items/ball/ball.png")),BALL_SIZE)

FRAMES_PLAYER = { 
    "idle" :  PLAYER_FRAMES_IDLE,
    "walk" : PLAYER_FRAMES_WALK,
    "run" : PLAYER_FRAMES_RUN,
    "jump" : PLAYER_FRAMES_JUMP,
    "death" : PLAYER_FRAMES_DEATH,
    "attack" : PLAYER_FRAMES_ATTACK
}

SOUND_HASTA_LA_VISTA_BABY = pygame.mixer.Sound("./src/assets/sounds/hlvb.wav")
SOUND_HURT = pygame.mixer.Sound("./src/assets/sounds/hurt.wav")
SOUND_JUMP = pygame.mixer.Sound("./src/assets/sounds/jump.wav")
SOUND_DEATH = pygame.mixer.Sound("./src/assets/sounds/death.mp3")
SOUND_BALL = pygame.mixer.Sound("./src/assets/sounds/ball.wav")


#----ghost-------------------------------------------------------------------------------------------------------------------------

ENEMY_FLYINGROBOT_SIZE = (100,70)
ENEMY_FLYINGROBOT_WALK = create_frames_dict("./src/assets/characters/flying_robot/walk/",ENEMY_FLYINGROBOT_SIZE,"png")
ENEMY_FLYINGROBOT_DAMAGE = 1
ENEMY_FLYINGROBOT_LIFE = 5
ENEMY_FLYINGROBOT_SPEED = 3

FRAMES_FLYINGROBOT = {
    "walk" : ENEMY_FLYINGROBOT_WALK["frames"],
    "amount" : ENEMY_FLYINGROBOT_WALK["amount"],
}
#----gummy-------------------------------------------------------------------------------------------------------------------------
ENEMY_GUMMY_SIZE = (50,50)
ENEMY_GUMMY_WALK = create_frames_dict("./src/assets/characters/gummy/walk/",ENEMY_GUMMY_SIZE,"png")
ENEMY_GUMMY_DAMAGE = 1
ENEMY_GUMMY_LIFE = 3
ENEMY_GUMMY_SPEED = 2

FRAMES_GUMMY ={
    "walk" : ENEMY_GUMMY_WALK["frames"],
    "amount" : ENEMY_GUMMY_WALK["amount"],
    }

#----form--------------------------------------------------------------------------------------------------------------------------
ENEMY_WORM_SIZE = (100,50)
ENEMY_WORM_WALK = create_frames_dict("./src/assets/characters/worm/walk/",ENEMY_WORM_SIZE,"png")
ENEMY_WORM_DAMAGE = 1
ENEMY_WORM_LIFE = 4
ENEMY_WORM_SPEED = 2

FRAMES_WORM ={
    "walk" : ENEMY_WORM_WALK["frames"],
    "amount":  ENEMY_WORM_WALK["amount"],
}

#----slime-------------------------------------------------------------------------------------------------------------------------
ENEMY_SLIME_SIZE = (100,100)
ENEMY_SLIME_WALK = create_frames_dict("./src/assets/characters/slime/walk/",ENEMY_SLIME_SIZE,"png")
ENEMY_SLIME_DAMAGE = 1
ENEMY_SLIME_LIFE = 10
ENEMY_SLIME_SPEED = 1
                                   
FRAMES_SLIME = {
    "walk" : ENEMY_SLIME_WALK["frames"],
    "amount": ENEMY_SLIME_WALK["amount"],
}

#----robotrabbit--------------------------------------------------------------------------------------------------------------------
ENEMY_ROBOTRABBIT_SIZE = (100,100)
ENEMY_ROBOTRABBIT_WALK = create_frames_dict("./src/assets/characters/rabbit_robot/walk/",ENEMY_ROBOTRABBIT_SIZE,"png")
ENEMY_ROBOTRABBIT_DAMAGE = 1
ENEMY_ROBOTRABBIT_LIFE = 5
ENEMY_ROBOTRABBIT_SPEED = 15

FRAMES_ROBOTRABBIT ={
    "walk" : ENEMY_ROBOTRABBIT_WALK["frames"],
    "amount": ENEMY_ROBOTRABBIT_WALK["amount"],
}
#----Boss1-------------------------------------------------------------------------------------------------------------------------
BOSS1_SIZE = (150,150)
BOSS1_DAMAGE = 1
BOSS1_LIFE =  40
BOSS1_SPEED = 1.8
BOSS1_BEHIND = create_frames_dict("./src/assets/characters/skullghost_boss/walk/",BOSS1_SIZE,"png")
BOSS1_DEATH = create_frames_dict("./src/assets/characters/skullghost_boss/death/",BOSS1_SIZE,"png")
BOSS1_FRONT = create_frames_dict("./src/assets/characters/skullghost_boss/front/",BOSS1_SIZE,"png")
BOSS1_HURT = create_frames_dict("./src/assets/characters/skullghost_boss/hurt/",BOSS1_SIZE,"png")
BOSS1_WALK = create_frames_dict("./src/assets/characters/skullghost_boss/walk/",BOSS1_SIZE,"png")
BOSS1_WALK_DOWN = create_frames_dict("./src/assets/characters/skullghost_boss/walk_down/",BOSS1_SIZE,"png")
BOSS1_WALK_UP = create_frames_dict("./src/assets/characters/skullghost_boss/walk_up/",BOSS1_SIZE,"png")

FRAMES_BOSS1 = {
    "behind" : BOSS1_BEHIND,
    "death" : BOSS1_DEATH,
    "front" : BOSS1_DEATH,
    "hurt" : BOSS1_HURT,
    "walk" : BOSS1_WALK,
    "walk_down" : BOSS1_WALK_DOWN,
    "walk_up" : BOSS1_WALK_UP }

#----door-------------------------------------------------------------------------------------------------------------------------
SIZE_DOOR = (130,150)
FRAMES_DOOR = create_frames_dict("./src/assets/items/door/",SIZE_DOOR,"png")

#----coin-------------------------------------------------------------------------------------------------------------------------
SIZE_COIN = (50,50)
FRAMES_COIN = create_frames_dict("./src/assets/items/coin/",SIZE_COIN,"png")
SOUND_COIN = pygame.mixer.Sound("./src/assets/sounds/collect_coin.mp3")

#----heart-------------------------------------------------------------------------------------------------------------------------
SIZE_HEART = (50,50)
FRAMES_HEART = create_frames_dict("./src/assets/items/heart/",SIZE_HEART,"png") 

#----key---------------------------------------------------------------------------------------------------------------------------
SIZE_ITEM_KEY = (50,50)
FRAMES_ITEM_KEY = create_frames_dict("./src/assets/items/key/",SIZE_ITEM_KEY,"png") 
SOUND_ITEM_KEY = pygame.mixer.Sound("./src/assets/sounds/key.mp3")

#----explosion-------------------------------------------------------------------------------------------------------------------------
SIZE_EXPLOSION = (100,100)  
FRAMES_EXPLOSION = create_frames_dict("./src/assets/items/white_explosion/",SIZE_EXPLOSION,"png")
SOUND_EXPLOSION = pygame.mixer.Sound("./src/assets/sounds/explosion.wav")
SOUND_EXPLOSION.set_volume(0.3)

#----item heart-------------------------------------------------------------------------------------------------------------------------
SIZE_ITEM_HEART = (60,60)
FRAMES_ITEM_HEART = create_frames_dict("./src/assets/items/mini_heart/",SIZE_ITEM_HEART,"png")
SOUND_ITEM_HEART = pygame.mixer.Sound("./src/assets/sounds/heart.wav")

##########################################################  PLATFORMS  ##############################################################

TEXTURE_SPIKES_PLATFORM = pygame.image.load("./src/assets/platform/spikes_long.png")

HIT_BOX_PRECISION_SIDES = 24
HIT_BOX_PRECISION_HEIGHT = 10


##########################################################  MUSIC  ###################################################################
MUSIC_MENU = "./src/assets/music/menu.mp3"
MUSIC_LVL1 = "./src/assets/music/level1.mp3"
MUSIC_BOSS1 = "./src/assets/music/boss.wav"

#SOUNDS 
SOUND_ENEMY_HURT =  pygame.mixer.Sound("./src/assets/sounds/enemy_hurt.wav")
SOUND_PAUSE = pygame.mixer.Sound("./src/assets/sounds/pause.mp3")
SOUND_LETTER = pygame.mixer.Sound("./src/assets/sounds/letter.mp3")
SOUND_OK = pygame.mixer.Sound("./src/assets/sounds/ok.mp3")
SOUND_DELETE = pygame.mixer.Sound("./src/assets/sounds/delete.mp3")
SOUND_OPTION = pygame.mixer.Sound("./src/assets/sounds/choose_option.mp3")
SOUND_ERROR = pygame.mixer.Sound("./src/assets/sounds/error.mp3")

#IMAGES
BACKGROUND_MENU = pygame.transform.scale(pygame.image.load("./src/assets/backgrounds/sky.jpg"),SCREEN_SIZE)
BACKGROUND_LVL1 = pygame.transform.scale(pygame.image.load("./src/assets/backgrounds/landscape.jpg"),SCREEN_SIZE)
BACKGROUND_BOSS1 = pygame.transform.scale(pygame.image.load("./src/assets/backgrounds/fight.png"),SCREEN_SIZE)
BACKGROUND_CONTROLS = pygame.transform.scale(pygame.image.load("./src/assets/backgrounds/controls.png"),SCREEN_SIZE)
BACKGROUND_RANKING =pygame.transform.scale(pygame.image.load("./src/assets/backgrounds/ranking.png"),SCREEN_SIZE)
BACKGROUND_CHANGENAME =pygame.transform.scale(pygame.image.load("./src/assets/backgrounds/name_screen.png"),SCREEN_SIZE)


#FONTS
FONT_MAIN = pygame.font.Font("./src/assets/fonts/main.ttf",60)
FONT_MAIN_BIG = pygame.font.Font("./src/assets/fonts/main.ttf",100)
FONT_TITLE = pygame.font.Font("./src/assets/fonts/title.otf",100)


#OBJECTS
TEXTURE_AIR_SPIKE = pygame.image.load("./src/assets/platform/air_spike.png")
SIZE_AIR_SPIKE = (80,80)




TEXTURE_GRASS_SHORT = pygame.image.load("./src/assets/platform/air1.png")
SIZE_GRASS_SHORT = (200,50)

TEXTURE_GRASS_LONG = pygame.image.load("./src/assets/platform/air_long.png")
SIZE_GRASS_LONG = (790,40)


TEXTURE_FLOATING_GROUND= pygame.image.load("./src/assets/platform/floating_ground.png")
SIZE_FLOATING_GROUND = (100,50)

TEXTURE_GROUND = pygame.image.load("./src/assets/platform/ground_image.png")
SIZE_GROUND = (WIDTH,HEIGHT//10)




GRAVITY = 0.5
JUMP_STRENGTH = -13
gravity_concept = {
    "gravity" : GRAVITY,
    "velocity_y" : 0,
    "jump_strength" : JUMP_STRENGTH,
    "is_jumping" : False }


sounds = [SOUND_EXPLOSION,SOUND_HURT,SOUND_ITEM_KEY,SOUND_BALL,SOUND_COIN,SOUND_DEATH,SOUND_ITEM_KEY,SOUND_ITEM_HEART,SOUND_JUMP,SOUND_ENEMY_HURT]


