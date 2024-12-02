import pygame
from pygame.locals import *
from settings import *

import sys

BLACK = (0,0,0)
WHITE = (255,255,255)
GREY = (200,200,200)
DARK_GREY = (20,20,20)
PINK = (255,0,127)

def create_block(image = None,left=0, top=0, width=50, height=50):
    if image != None:
        image = pygame.transform.scale(image,(width,height))
    return { "rect": pygame.Rect(left, top, width, height),
             "img": image,
             "current_frame" : 0 ,
             "size" : (width,height),
             "move_frames" : False,
             "reverse_frames": False,
             }

def mostrar_texto(superficie,texto,fuente,coordenada,color = WHITE,color_fondo = None):
    sticker = fuente.render(texto,True,color,color_fondo)
    rect = sticker.get_rect(center = coordenada)
    superficie.blit(sticker,rect ) 
    

def draw_button(font,text, rect, color, hover_color, action=None,letter_color = BLACK):
    from settings  import screen
    mouse_pos = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    hovered = rect.collidepoint(mouse_pos)
    
    if hovered:
        
        pygame.draw.rect(screen, hover_color, rect)
        if click[0] == 1 and action:
            pygame.time.delay(200)
            action()
    else:

        pygame.draw.rect(screen, color, rect)

    text_surf = font.render(text, True, letter_color)
    screen.blit(text_surf, (rect.x + (rect.width - text_surf.get_width()) // 2, rect.y + (rect.height - text_surf.get_height()) // 2))

    

def terminar():
    pygame.quit()
    exit()

def punto_en_rectangulo(punto:tuple,rectangulo)->bool:
    """Determinar si un punto (x,y) esta presente en un rectangulo

    Args:
        punto (tuple): coordenadas
        rectangulo (Rect): rectangulo en donde pueden estar las coordenadas

    Returns:
        bool: True: el punto esta dentro del rectangulo / False """
    x,y= punto
    return x >= rectangulo.left and x <= rectangulo.right and  y >= rectangulo.top and y <= rectangulo.bottom

def extremos_de_rectangulo(rectangulo:dict)->tuple:
    """
    Args:
        rectangulo (dict): Un rectangulo

    Returns:
        una tupla con (x,y) en cada indice, cada una es la coordenada de un extremo
        (topleft,topright,bottom_left,bottom_right)
    """

    top_left = rectangulo.topleft
    
    top_right = rectangulo.topright
    bottom_left = rectangulo.bottomleft
    bottom_right  = rectangulo.bottomright    

    return ((top_left),(top_right),(bottom_left),(bottom_right))

def detectar_colision(rectangulo1,rectangulo2)->bool:

    extremos_rectangulo1 = extremos_de_rectangulo(rectangulo1)
    extremos_rectangulo2 = extremos_de_rectangulo(rectangulo2)

    for punto in range(len(extremos_rectangulo1)):
        if punto_en_rectangulo(extremos_rectangulo1[punto],rectangulo2) or punto_en_rectangulo(extremos_rectangulo2[punto],rectangulo1):
            return True
    return False

def rectangulo_dentro_laterales(rectangulo1:pygame.Rect,rectangulo2:pygame.Rect)->bool:
    """Devuelve True si el rectangulo 1 se encuentra dentro de los laterales del rectangulo 2"""
    return rectangulo1.left <= rectangulo2.right and rectangulo1.right >= rectangulo2.left

def rectangulo_dentro_cotas(rectangulo1:pygame.Rect,rectangulo2:pygame.Rect):
    return rectangulo1.top >=  rectangulo2.top and rectangulo1.bottom <= rectangulo2.bottom

def sobre_rectangulo(rectangulo1:pygame.Rect,rectangulo2:pygame.Rect)->bool:
    """ Devuelve True si rectangulo1 se encuentra por encima de rectangulo 2"""
    retorno = False

    if rectangulo1.bottom <= rectangulo2.top:
        if rectangulo_dentro_laterales(rectangulo1,rectangulo2):
            retorno = True

    return retorno

def rectangulo_en_mitad_rectangulo2(rectangulo1:pygame.Rect,rectangulo2:pygame.Rect,superior= True)->bool:
    """Devuelve True si rectangulo1 se encuentra en la mitad superior del rectangulo 2"""
    
    if superior:
        return rectangulo_dentro_laterales(rectangulo1,rectangulo2) and rectangulo1.bottom <= rectangulo2.centery
                
    else:
        return rectangulo_dentro_laterales(rectangulo1,rectangulo2) and rectangulo1.bottom >= rectangulo2.centery
        
def aleatory_rect_side()->str:
    import random
    sides = ("center","left","right","top","bottom")
    return random.choice(sides)

    
def wait_user(tecla):
    continuar = True
    while continuar:
        for evento in pygame.event.get():
            if evento.type == QUIT:
                terminar()
            if evento.type == KEYDOWN:
                if evento.key == tecla:
                    continuar = False

def wait_user_click(rect_imagen:pygame.Rect):

    continuar = True
    while continuar:
        for evento in pygame.event.get():
            if evento.type == QUIT:
                terminar()
            if evento.type == MOUSEBUTTONDOWN:
                if evento.button == 1:
                    if punto_en_rectangulo(evento.pos,rect_imagen):
                        continuar = False

def is_empty_list(list:list)->bool:
    if len(list) == 0:
        raise ValueError("Lista vacia")

#############################
def binary_search(list:list):
    try:
        is_empty_list(list)


    except Exception as error:
        print(error)

def mapear_lista(lista:list,clave:str)->list:
    new_list = []
    try:
        is_empty_list(lista)
        for dictionary in lista:
            new_list.append(dictionary[clave])
        return new_list
    except Exception as error:
        print(error)

def swap_list(lista:list,i:int,j:int):
     aux = lista[i]
     lista[i] = lista[j]
     lista[j] = aux

def get_path_actual(nombre_archivo):
    import os
    directorio_actual = os.path.dirname(__file__) #devuelve el directorio , mas no el archivo (ruta hasta directorio csv)
    return os.path.join(directorio_actual,nombre_archivo)#esto joinea el directorio y el nombre del archivo es el nombre del archivo csv

def detect_empty_file(directory:str)->bool:
    try:
        with open(directory,"r",encoding="UTF-8") as file:
            pass
        return False
    except Exception:
        return True
    

def complete_empty_file(directory:str):
  
    if detect_empty_file(directory):
        with open(directory,"w",encoding="UTF-8") as file:
           
            header = "PLAYER,HIGHSCORE\n" 
            file.write(header)
            for row in range(10):
                for column in range(2):
                    line = ",nobody,0"
                line = line.lstrip(",") + "\n"
                file.write(line)
                 

def save_score(player:dict,file_name:str):

    directorio = get_path_actual(file_name)
    complete_empty_file(directorio) 

    score_list = []

    with open(directorio,"r",encoding="UTF-8") as highscore_file:

        header = highscore_file.readline()
        lines =  highscore_file.readlines()

        for line in lines:
            highscore_player = {}
            line = line.strip("\n").split(",") #cortar strings
            
            name,highscore = line
            highscore_player["name"] = str(name)
            highscore_player["highscore"] = int(highscore)

            score_list.append(highscore_player) 

  
        current_highscore_player = {}
        current_highscore_player["name"] = player["name"]
        current_highscore_player["highscore"] = player["score"]

        score_list.append(current_highscore_player)

        for index in range(len(score_list)-1):
            for next_index in range(index+1,len(score_list)):
                if score_list[index]["highscore"] < score_list[next_index]["highscore"]:
                    swap_list(score_list,index,next_index)
        score_list.pop()


    with open(directorio,"w",encoding="UTF-8") as file:
        header = "PLAYER,HIGHSCORE\n" 
        file.write(header)
        
        for index in range(len(score_list)):
            line = str(score_list[index]["name"])+","+str(score_list[index]["highscore"]) + "\n"
            file.write(line)
    
    
def mute(sounds,mute = True):    
    volume = 1
    if mute:
        volume = 0

    for sound in sounds:
        sound.set_volume(volume)  
    pygame.mixer.music.set_volume(volume)  

 
    




        


       
       

        
        


     



        


