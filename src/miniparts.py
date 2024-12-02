from objects import *


#-------------------------------------------------------------------------------UPDATE MOVEMENTS------------------------------------------------------------------------
def move_left_rect(item:dict,movement:bool,left_limit:int):
    """Desplazar rectangulo a la izquierda
    left_limit(int): limite lateral de desplazamiento
    item(dict) : diccionario con: 
                "rect" : rectangulo pygame
                "speed" : velocidad  """    
    if movement:
        item["rect"].left -= item["speed"] 
        if item["rect"].left < left_limit:
            item["rect"].left = left_limit
    
def move_right_rect(item:dict,movement:bool,right_limit:int):
    """Desplazar rectangulo a la derecha
    right_limit(int): limite lateral de desplazamiento
    item(dict) : diccionario con: 
                "rect" : rectangulo pygame
                "speed" : velocidad  """
    if movement:
        item["rect"].right += item["speed"]
        if item["rect"].right > right_limit:
            item["rect"].right = right_limit

def move_up_rect(item:dict,movement:bool,up_limit:int):
    """Desplazar rectangulo hacia arriba
    right_limit(int): limite lateral de desplazamiento
    item(dict) : diccionario con: 
                "rect" : rectangulo pygame
                "speed" : velocidad  """
    if movement:
        item["rect"].top -= item["speed"]
        if item["rect"].top > up_limit:
            item["rect"].top = up_limit

def move_down_rect(item:dict,movement:bool,down_limit:int):
    """Desplazar rectangulo hacia abajo
    right_limit(int): limite lateral de desplazamiento
    item(dict) : diccionario con: 
                "rect" : rectangulo pygame
                "speed" : velocidad  """
    if movement:
        item["rect"].bottom += item["speed"]
        if item["rect"].bottom > down_limit:
            item["rect"].bottom = down_limit

            
            
def platform_movement(platform:list):
    """ actualizar movimiento de items
        platform (list): lista de diccionarios, que representan objetos/items en el juego con:
        "rect" : rectangulo
        "speed"(int) : velocidad del objeto
        "reverse"(bool) : indica el sentido del movimiento True si es derecha 
        "left_limit" : limite izquierdo en coordenadas X
        "right_limit" : limite derecho en coordenadas Y  """
    for item in platform:

            if item["reverse"]:
                move_left_rect(item,True,item["left_limit"])
            else:
                move_right_rect(item,True,item["right_limit"])

            if item["rect"].left == item["left_limit"]:
                 item["reverse"] = False
            if item["rect"].right == item["right_limit"]:
                 item["reverse"] = True


def move_enemies(enemy_list:list):
    for enemy in enemy_list:
        if not enemy["hit"]:

            if enemy["reverse"]:
                move_left_rect(enemy,True,enemy["left_limit"])

            else:
                move_right_rect(enemy,True,enemy["right_limit"])
            
            if enemy["rect"].left == enemy["left_limit"]:
                enemy["reverse"] = False
            elif enemy["rect"].right == enemy["right_limit"]:
                enemy["reverse"] = True
                

        else:
            enemy["image"] = enemy["frames"]["hurt"]

def move_balls(balls_list:list):
    if len(balls_list) > 0:
        for ball in balls_list[:]:
            if ball["last_pose_left"]:
                move_left_rect(ball,True,ball["left_limit"])
            else:
                move_right_rect(ball,True,ball["right_limit"])
            if ball["rect"].left == ball["left_limit"] or ball["rect"].right == ball["right_limit"] :
                balls_list.remove(ball)

def move_boss1(boss:dict,target:dict):
    boss["move_up"]= False
    boss["move_down"] = False
    boss["move_left"] = False
    boss["move_right"] = False 
    boss["move_same"] = False   


    if target["rect"].bottom + 5 < boss["rect"].bottom:
        boss["rect"].bottom -= boss["speed"]
        boss["move_up"] = True

    elif target["rect"].bottom -5 > boss["rect"].bottom:
        boss["rect"].bottom += boss["speed"]
        boss["move_down"] = True
    else : 
        boss["move_same"] = True



    if target["rect"].left < boss["rect"].left:
        boss["rect"].left -= boss["speed"]
        boss["move_left"] =  True
        boss["last_pose_left"] = True

    elif target["rect"].left > boss["rect"].left:
        boss["rect"].left += boss["speed"]
        boss["move_right"] = True
        boss["last_pose_left"] = False
    
    #if (target["rect"].bottom == boss["rect"].bottom):
        



          
#-----------------------------------------------------------------------------------------------COLISIONES-------------------------------------------------------------------
def fall_in_surface(rect1:pygame.Rect,rect2:pygame.Rect):
    """Si rect1 sobrepasa rect2 verticalmente, rect1 se apoyara en rect2
    rect1 : pygame.Rect
    rect2 : pygame.Rect
    boolean_answer (bool) : Si True, indica si rect1 sobrepasa a rect2 en booleano
    """
    
    if  rect1.bottom > rect2.top:   
        rect1.bottom = rect2.top
        gravity_concept["velocity_y"] = 0
        gravity_concept["is_jumping"] = False   
    
def player_on_static_platforms(rect:pygame.Rect,platform:list):
    for block in platform:
                        if detectar_colision(rect,block["rect"]):

                            if rectangulo_en_mitad_rectangulo2(rect,block["rect"]):
                            
                                    #correccion bordes de plataforma a tener en cuenta para apoyar al personaje
                                if rect.left < block["rect"].right - HIT_BOX_PRECISION_SIDES and rect.right > block["rect"].left + HIT_BOX_PRECISION_SIDES:

                                    rect.bottom = block["rect"].top + HIT_BOX_PRECISION_HEIGHT
                                    gravity_concept["velocity_y"] = 0
                                    gravity_concept["is_jumping"] = False

def player_on_move_platforms(rect:pygame.Rect,platform:list):
    for  air_block in  platform:
        if detectar_colision(rect,air_block["rect"]):
            if rectangulo_en_mitad_rectangulo2(rect,air_block["rect"]):
                
                
                if rect.left < air_block["rect"].right and rect.right > air_block["rect"].left :
                    rect.bottom = air_block["rect"].top + HIT_BOX_PRECISION_HEIGHT

                    if air_block["reverse"]:
                        rect.left -= air_block["speed"]
                    else:
                        rect.left += air_block["speed"]

                    gravity_concept["velocity_y"] = 0
                    gravity_concept["is_jumping"] = False

#-----------------------------------------------------------------------------UPDATE FRAMES-----------------------------------------------------------------------------
def update_character_frame(character:dict,action:str):
    """
    Args:
        character (dict): with keys:
            "last_pose_left"(bool) : last side ( left or right)
            "frames"(dict) : with keys:
                "action"(list) : frame list

        action (str): action to do """
    frame_index = character["frames"][action]["universal_frame_index"]
    frame = character["frames"][action]["frames"][frame_index]

    character["frames"][action]["universal_frame_index"] += 1
    if character["frames"][action]["universal_frame_index"] == character["frames"][action]["amount"]:
        character["frames"][action]["universal_frame_index"] = 0

    
    if character["last_pose_left"]:
        character["img"] = flip_image(frame)
    else:
        character["img"] = frame

#----------------------------------------
def update_boss1_frames(boss:dict):
    action = None
    
    if boss["move_up"]:
        action = "walk_up"
    if boss["move_down"]:
        action = "walk_down"
    if boss["move_same"]:
        action = "walk"

    

    
    update_character_frame(boss,action)
    
    if boss["hit"]:
        boss["img"] = tint_image(boss["img"],RED)
    
#----------------------------------------
def update_enemy_frames(enemy_list:list):
     for enemy in enemy_list:

        image = enemy["frames"]["walk"][enemy["current_frame"]]
        enemy["current_frame"] += 1 
        
        if enemy["current_frame"] > enemy["frames"]["amount"] - 1:
            enemy["current_frame"] = 0


        if enemy["hit"]:
        
            if enemy["reverse"]:
               enemy["img"] = flip_image(tint_image(image,RED))
            else:
               enemy["img"] = tint_image(image,RED)

        else:     
          

          if enemy["reverse"]:
               enemy["img"] = flip_image(image) 
          else:
               enemy["img"] = image

#----------------------------------------------------------------------------------------
def update_statics_blocks_frames(items_list:list,temporal:bool = None,remove_list:list = None):
    """Update images from statics blocks with frames,if temporal also removes at last frame
    Args:
        items_list (list): list of dicts
            item(dict):
                "img" : image
                "frames"(dict):
                        "frames"(list): images list
                        "current_frame_index"(int) 
                        "amount"(int) : frames amount    """
    if len(items_list) > 0:
       
       if temporal:
            for item in items_list:
                index = item["current_frame"]
                image = item["frames"]["frames"][index]
                item["img"] = image

                item["current_frame"] += 1
        
                if item["current_frame"] > item["frames"]["amount"] - 1:
                    item["current_frame"] = 0
                    remove_list.append(item)
                
       else:
        for item in items_list:
            index = item["frames"]["universal_frame_index"]
            image = item["frames"]["frames"][index]
            item["img"] = image

        item["frames"]["universal_frame_index"] += 1
    
            
        if item["frames"]["universal_frame_index"] > item["frames"]["amount"] - 1:
            item["frames"]["universal_frame_index"] = 0


def move_frames(item:dict):
    """Update frames in one direction (first to last or last to first)
    Args:
        item (dict): with keys:
            "move_frames"(bool) : if True, update frames to one direction (first to last or last to first)
            "current_frame"(int): an individual index frame
            "reverse_frames"(bool): if True, frames going last to first
            "frames"(dict):
                "amount"(int): amount frames
                "frames"(list): frames list (images)
    """
    
    if item["move_frames"]:
        next_frame = -1 if item["reverse_frames"] else 1

        item["current_frame"] += next_frame
        item["img"] = item["frames"]["frames"][item["current_frame"]]

        if item["current_frame"] == 0:
            item["move_frames"] = False
            item["reverse_frames"] = False
        
        elif item["current_frame"] == item["frames"]["amount"] - 1:
            item["move_frames"]= False
            item["reverse_frames"] = True


    
#--------------------------------------------------------------------------IMPRESIONES--------------------------------------------------------------------

def blit_static_surface(list:list):
    """Imprimir en pantalla superficies sin frames cambiantes
        list: diccionarios con las siguientes claves:
            "img" : imagen
            "rect": rectangulo  """
    if len(list) > 0:
        for dictionary in list:
            screen.blit(dictionary["img"],dictionary["rect"])



def remove_item(items:list,items_to_remove:list):

    for  item in items:
        if item in items_to_remove:
            items.remove(item)

