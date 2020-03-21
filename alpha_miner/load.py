import pygame as pg
from pygame.compat import geterror 
import os

main_dir = os.path.split(os.path.abspath(__file__))[0]

image_dir = os.path.join(main_dir, 'images')

def load_image( name ):
    """ 
    Function for loading images

    :param name: name of image file
    """

    fullname = os.path.join(image_dir, name)
    try:
        image = pg.image.load(fullname)
    except pg.error:
        print ('Cannot load image:', fullname)
        raise SystemExit(str(geterror()))
    image = image.convert_alpha() 
    
    return image, image.get_rect()


#font_dir = os.path.join(main_dir, 'fonts') # idk why doesn't work
font_dir = os.path.join('fonts')

def load_font( *, font_name, size ):
    """ 
    Function for loading fonts

    :param name: path to font from main game dir.
    """

    fullname = os.path.join(font_dir, font_name)
    try:
        font = pg.font.Font( fullname, size )
    except pg.error:
        print ('Cannot load font:', fullname)
        raise SystemExit(str(geterror()))
    
    return font

def make_text( *, text = "No text given" ,font_name = None, size = 10, pos = ( 0, 0 ), text_color = (255,255,255), text_background_color = (0,0,0) ):
    font = load_font( font_name = font_name, size = size)
    text = font.render( text, 1, text_color, text_background_color )
    text_pos = text.get_rect( centerx = pos[0], centery = pos[1] )
    return text, text_pos