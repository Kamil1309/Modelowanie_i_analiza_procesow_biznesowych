import pygame as pg
from pygame.locals import *

from pm4py.objects.log.importer.xes import factory as xes_import_factory

import sys
import os

from load import make_text, load_image
from button import Button
from file_path import get_file_path

def make_log_look(data, pos, color, left=False):
    """
    :param data: data that will be transformed into log look
    :param pos: pos of transformed data
    :param color: color of transformed data
    :param left: optional parameter, if it's number then transformed data will be aligned to left possition of this param
    """
    log_text = "<"
    for event_num, event in enumerate(data):
        log_text += data[event_num]
        if event_num < len(data)-1:
            log_text += ','
    log_text += ">"
    
    log_text, log_text_rect = make_text( text= log_text , font_name= 'calibri-font-sv\Calibri Bold.ttf'\
                                        , size= 25, pos= pos\
                                        , text_color= color, text_background_color= (0, 0, 0))
    if left != False:
        log_text_rect.left = left
        
    return log_text, log_text_rect

def BPMN_add_row(BPMN):
    BPMN.append( [ [] for i in range(0, len( BPMN[ len(BPMN)-1 ] ) ) ] )
    return BPMN

def BPMN_add_column(BPMN):
    if len(BPMN) > 0:
        for i in range(0, len(BPMN)):
            BPMN[i].append([])
    else:
        BPMN.append([[]])
    return BPMN

def BPMN_draw_line( surf, start_pos, end_pos, arrow = False, arrow_s_r = None, size = 3 ):
    if arrow:
        pg.draw.line( surf, (72, 144, 220), start_pos, end_pos, 3 )
        arrow_s_r[1].right = end_pos[0]
        arrow_s_r[1].top = end_pos[1] - arrow_s_r[1].height/2 + 1
        surf.blit( arrow_s_r[0], arrow_s_r[1] )
    else:
        pg.draw.line(surf, (72, 144, 220), start_pos, end_pos, size)

def create_activity_surf( name ):
    # load corners
    top_left_corner, top_left_corner_rect = load_image("top_left_corner.png") 
    top_right_corner, top_right_corner_rect = load_image("top_right_corner.png")
    bottom_right_corner, bottom_right_corner_rect = load_image("bottom_right_corner.png")
    bottom_left_corner, bottom_left_corner_rect = load_image("bottom_left_corner.png")

    #create text
    text, text_rect = make_text( text= name, font_name= 'calibri-font-sv\Calibri Bold.ttf'\
                                , size= 20, pos= (0,0)\
                                , text_color= (255, 180, 69), text_background_color= (0, 0, 0))
    
    #create activity surface
    activity_surf = pg.Surface( (text_rect.width + 40, text_rect.height + 50) ).convert()
    activity_surf.fill( (0, 0, 0) )
    activity_surf_rect = activity_surf.get_rect( topleft = (0,0) )

    #set corners position
    top_left_corner_rect.topleft = (0, 0)
    top_right_corner_rect.topright = (activity_surf_rect.width, 0)
    bottom_right_corner_rect.bottomright = (activity_surf_rect.width, activity_surf_rect.height)
    bottom_left_corner_rect.bottomleft = (0, activity_surf_rect.height)
    #set text position
    text_rect.center = activity_surf_rect.center

    activity_surf.blit( top_left_corner, top_left_corner_rect )
    activity_surf.blit( top_right_corner, top_right_corner_rect )
    activity_surf.blit( bottom_right_corner, bottom_right_corner_rect )
    activity_surf.blit( bottom_left_corner, bottom_left_corner_rect )

    BPMN_draw_line(activity_surf, (top_left_corner_rect.right, top_left_corner_rect.top + 2), ( top_right_corner_rect.left, top_right_corner_rect.top + 2), False, None, 5 )
    BPMN_draw_line(activity_surf, (top_right_corner_rect.right - 3, top_right_corner_rect.bottom), ( bottom_right_corner_rect.right - 3, bottom_right_corner_rect.top), False, None, 5 )
    BPMN_draw_line(activity_surf, (bottom_right_corner_rect.left, bottom_right_corner_rect.bottom - 3), ( bottom_left_corner_rect.right, bottom_left_corner_rect.bottom - 3), False, None, 5 )
    BPMN_draw_line(activity_surf, (bottom_left_corner_rect.left + 2, bottom_left_corner_rect.top), ( top_left_corner_rect.left + 2, top_left_corner_rect.bottom), False, None, 5 )

    activity_surf.blit( text, text_rect )

    return activity_surf, activity_surf_rect

class Alpha_Miner_Algorithm():
    """Alpha Miner Algorithm"""
    def __init__(self, window, path):
        """Alpha Miner Algorithm - constructor"""

        self.window = window
        self.window_rect = self.window.get_rect() 
        self.path = path

        #Create background surface
        # self.bg = pg.Surface( self.window.get_size() ).convert()
        # self.bg.fill( (0, 0, 0) )
        # self.bg_rect = self.bg.get_rect( topleft = (0,0) )

        #Create menu images
        img_folder = "alg_buttons"
        self.buttons = {
                "left" : [None, False, (self.window_rect.width * 4.5/10, self.window_rect.height *11/12)],
                "right" : [None, False, (self.window_rect.width * 5.5/10, self.window_rect.height* 11/12)],
                "exit" : [None, False, (self.window_rect.width * 1/12, self.window_rect.height* 12/13)],
                }
            #Buttons possition
        
        #creating buttons
        all_buttons = []

        for i, button_name in enumerate( self.buttons ):
            self.buttons[button_name][0] = ( Button(folder_name = img_folder, \
                                            img_name = button_name, pos = self.buttons[button_name][2] ) )
            all_buttons.append ( self.buttons[button_name][0] )

        self.allsprites = pg.sprite.RenderPlain( all_buttons )

        #Create main menu text
        self.main_text, self.main_text_rect = make_text( text= "Alpha miner algorithm", font_name= 'calibri-font-sv\Calibri Bold.ttf'\
                                                    , size= 35, pos= (self.window_rect.centerx, 40)\
                                                    , text_color= (72, 144, 220), text_background_color= (0, 0, 0))
        #self.bg.blit( self.text, self.text_rect )#Blit text on background

        self.initialized = -1
        self.current_phase = 0

        self.phase_range = (0, 4)
        #Initialize clock
        self.clock = pg.time.Clock()

        self.click_down = False
        self.click_up = False

    def initialization(self):
        if self.current_phase == 0:#####################################
            #Create 
            log = xes_import_factory.apply(self.path)
            self.L = [[],[]] # L[0] - real names of whole traces, L[1] - new names of whole traces
            self.diff_names = [[],[],[],[]] # L[0] - surf of real names, L[1] - surf of new names
            for trace_num, trace in enumerate(log):
                self.L[0].append([]) # New trace with real names
                self.L[1].append([]) # New trace with new names
                for event_num, event in enumerate(trace):
                    self.L[0][trace_num].append(event["concept:name"])
                    self.L[1][trace_num].append(event["concept:name"])
                    if event["concept:name"] not in self.diff_names[0]:
                        self.diff_names[0].append(event["concept:name"])
                        self.diff_names[1].append(str(chr(97 + len(self.diff_names[0])-1 )))
                        self.diff_names[2].append(event["concept:name"])
                        self.diff_names[3].append(str(chr(97 + len(self.diff_names[0])-1 )))

            self.TL = self.diff_names[1][:]#Creating Tl set of all tasks in the log L (use in phase 1)
            for trace_num in range(0, len(self.L[0]) ):
                for event_num in range(0, len(self.L[0][trace_num]) ):
                    index_of_real = self.diff_names[0].index(self.L[1][trace_num][event_num])
                    self.L[1][trace_num][event_num] = self.diff_names[1][index_of_real]

            for name_num in range(0, len(self.diff_names[0])):
                org_name, org_name_rect = make_text( text= self.diff_names[0][name_num], font_name= 'calibri-font-sv\Calibri Bold.ttf'\
                                                        , size= 25, pos= (self.window_rect.width*3/8, self.window_rect.height*(6+name_num)/25)\
                                                        , text_color= (72, 144, 220), text_background_color= (0, 0, 0))
                new_name, new_name_rect = make_text( text= self.diff_names[1][name_num], font_name= 'calibri-font-sv\Calibri Bold.ttf'\
                                                        , size= 25, pos= (self.window_rect.width*6/8, self.window_rect.height*(6+name_num)/25)\
                                                        , text_color= (72, 144, 220), text_background_color= (0, 0, 0))
                self.diff_names[0][name_num] = [org_name, org_name_rect]
                self.diff_names[1][name_num] = [new_name, new_name_rect]

            org_name_text, org_name_text_rect = make_text( text= "Original name", font_name= 'calibri-font-sv\Calibri Bold.ttf'\
                                                        , size= 25, pos= (self.window_rect.width*3/8, self.window_rect.height*4/25)\
                                                        , text_color= (255, 180, 69), text_background_color= (0, 0, 0))
            new_name_text, new_name_text_rect = make_text( text= "New name", font_name= 'calibri-font-sv\Calibri Bold.ttf'\
                                                        , size= 25, pos= (self.window_rect.width*6/8, self.window_rect.height*4/25)\
                                                        , text_color= (255, 180, 69), text_background_color= (0, 0, 0))
            #Create picture
            self.bg0 = pg.Surface( self.window.get_size() ).convert()
            self.bg0.fill( (0, 0, 0) )
            self.bg0_rect = self.bg0.get_rect( topleft = (0,0) )

            pg.draw.line(self.bg0, (255,134,69), (self.window_rect.width*5/8, self.window_rect.height*5/25),\
                        (self.window_rect.width*5/8, self.window_rect.height*(6 + len(self.diff_names[0]))/25),2)

            self.bg0.blit( self.main_text, self.main_text_rect )
            self.bg0.blit( org_name_text, org_name_text_rect )
            self.bg0.blit( new_name_text, new_name_text_rect )
            for i in range(0, len(self.diff_names[0])):
                self.bg0.blit( self.diff_names[0][i][0], self.diff_names[0][i][1] )
                self.bg0.blit( self.diff_names[1][i][0], self.diff_names[1][i][1] )
                if i != 0:
                    pg.draw.line(self.bg0, (255,199,115), (self.window_rect.width*2/8, self.window_rect.height*(11+2*i)/50),\
                                (self.window_rect.width*7/8, self.window_rect.height*(11+2*i)/50 ),1)
            self.initialized = 0

        elif self.current_phase == 1:#####################################
            # Creating L - full log (of all traces)
            L_caption, L_caption_rect = make_text( text= "L  = " , font_name= 'calibri-font-sv\Calibri Bold.ttf'\
                                                        , size= 25, pos= (self.window_rect.width*2/16, self.window_rect.height*4/25)\
                                                        , text_color= (255, 180, 69), text_background_color= (0, 0, 0))
            self.L_surf = []
            for trace_num in range( 0, len(self.L[1]) ):
                log_text, log_text_rect = make_log_look(self.L[1][trace_num], \
                    (0, self.window_rect.height*(4+ trace_num)/25), (72, 144, 220), self.window_rect.width*5/32)
                self.L_surf.append([])

                self.L_surf[trace_num].append(log_text)
                self.L_surf[trace_num].append(log_text_rect)

            #Create TL - set of all tasks in the log L 
            TL_caption, TL_caption_rect = make_text( text= "TL  = " , font_name= 'calibri-font-sv\Calibri Bold.ttf'\
                                                        , size= 25, pos= (self.window_rect.width*2/16, self.window_rect.height*(4+len(self.L[1])+1)/25)\
                                                        , text_color= (255, 180, 69), text_background_color= (0, 0, 0))
            
            TL_text, TL_text_rect = make_log_look(self.TL, \
                    (0, self.window_rect.height*(4+len(self.L[1])+1)/25), (72, 144, 220), self.window_rect.width*5/32)

            #Create TI - set of tasks that appear at least once as first task of a case in the log L 
            #Create TO - set of tasks that appear at least once as last task of a case in the log L 
            self.TI = []
            self.TO = []
            for trace_num, trace in enumerate( self.L[1] ):
                if trace[0] not in self.TI:
                    self.TI.append( trace[0] )
                if trace[len(trace)-1] not in self.TO:
                    self.TO.append( trace[len(trace)-1] )

            TI_caption, TI_caption_rect = make_text( text= "TI  = " , font_name= 'calibri-font-sv\Calibri Bold.ttf'\
                                                        , size= 25, pos= (self.window_rect.width*2/16, self.window_rect.height*(4+len(self.L[1])+3)/25)\
                                                        , text_color= (255, 180, 69), text_background_color= (0, 0, 0))
            TO_caption, TO_caption_rect = make_text( text= "TO  = " , font_name= 'calibri-font-sv\Calibri Bold.ttf'\
                                                        , size= 25, pos= (self.window_rect.width*2/16, self.window_rect.height*(4+len(self.L[1])+5)/25)\
                                                        , text_color= (255, 180, 69), text_background_color= (0, 0, 0))
            
            TI_text, TI_text_rect = make_log_look(self.TI, \
                    (0, self.window_rect.height*(4+len(self.L[1])+3)/25), (72, 144, 220), self.window_rect.width*5/32)
            TO_text, TO_text_rect = make_log_look(self.TO, \
                    (0, self.window_rect.height*(4+len(self.L[1])+5)/25), (72, 144, 220), self.window_rect.width*5/32)

            #Create footprint matrix
            self.footprint_matrix = [ ["#" for i in range(0, len(self.TL)+1 )] for i in range(0, len(self.TL)+1 )]
            self.footprint_matrix[0][0] = ""
            for i in range(0, len(self.TL) ):
                self.footprint_matrix[0][i+1] = self.TL[i]
                self.footprint_matrix[i+1][0] =self.TL[i]

            checked_pair = [1,1]
            for i in range(0, len(self.L[1]) ):
                for j in range(0, len(self.L[1][i])-1 ):
                    checked_pair[0] = self.L[1][i][j]
                    checked_pair[1] = self.L[1][i][j+1]
                    self.footprint_matrix[self.TL.index(checked_pair[0])+1][self.TL.index(checked_pair[1])+1] = "f"
            for i in range(1, len(self.footprint_matrix)):
                for j in range(1, len(self.footprint_matrix) ):
                    if self.footprint_matrix[i][j] == "f":
                        if self.footprint_matrix[j][i] == "f":
                            self.footprint_matrix[i][j] = "||"
                            self.footprint_matrix[j][i] = "||"
                        else:
                            self.footprint_matrix[i][j] = "right"
                            self.footprint_matrix[j][i] = "left"


            #Load images of arrows
            left_arrow, left_arrow_rect = load_image("left.png")
            right_arrow, right_arrow_rect = load_image("right.png")

            #Create picture
            self.bg1 = pg.Surface( self.window.get_size() ).convert()
            self.bg1.fill( (0, 0, 0) )
            self.bg1_rect = self.bg1.get_rect( topleft = (0,0) )

            self.bg1.blit( L_caption, L_caption_rect )
            self.bg1.blit( self.main_text, self.main_text_rect )

            self.bg1.blit( TL_caption, TL_caption_rect )
            self.bg1.blit( TL_text, TL_text_rect )

            self.bg1.blit( TI_caption, TI_caption_rect )
            self.bg1.blit( TI_text, TI_text_rect )

            self.bg1.blit( TO_caption, TO_caption_rect  )
            self.bg1.blit( TO_text, TO_text_rect )

            for trace_num, trace in enumerate(self.L_surf): 
                self.bg1.blit( trace[0], trace[1] )

            footprint_matrix_pos = (self.window_rect.width * 1/2, self.window_rect.height * 1/6)

                #display footprint matrix
            for i in range(0, len(self.footprint_matrix)):
                for j in range(0, len(self.footprint_matrix[i])):
                    if self.footprint_matrix[i][j] != "left" and self.footprint_matrix[i][j] != "right":
                        if self.footprint_matrix[i][j] == "#" or self.footprint_matrix[i][j] == "||":
                            color = (72, 144, 220)
                        else:
                            color = (255, 180, 69)
                        char, char_rect = make_text( text=  self.footprint_matrix[i][j], font_name= 'calibri-font-sv\Calibri Bold.ttf'\
                                                            , size= 20, pos= (footprint_matrix_pos[0] + j*25, footprint_matrix_pos[1] + i*25)\
                                                            , text_color= color, text_background_color= (0, 0, 0))
                        self.bg1.blit( char, char_rect )
                    else:
                        if self.footprint_matrix[i][j] == "left":
                            left_arrow_rect.center = (footprint_matrix_pos[0] + j*25, footprint_matrix_pos[1] + i*25)
                            self.bg1.blit( left_arrow, left_arrow_rect )
                        else:
                            right_arrow_rect.center = (footprint_matrix_pos[0] + j*25, footprint_matrix_pos[1] + i*25)
                            self.bg1.blit( right_arrow, right_arrow_rect )
                            
            TI_text, TI_text_rect 

            self.initialized = 1

        elif self.current_phase == 2:#####################################
            #Create XL - set of potential task connections
            self.XLa = [[],[]] # XL - pattern a : a -> b
            self.XLb = [[],[]] # XL - pattern b : a -> (b#c)
            self.XLc = [[],[]] # XL - pattern c : (b#c) -> d
                
            for i in range(0, len(self.footprint_matrix)):
                for j in range(0, len(self.footprint_matrix[i])):
                    #pattern a
                    if self.footprint_matrix[i][j] == "right":
                        self.XLa[0].append( self.footprint_matrix[i][0] )
                        self.XLa[1].append( self.footprint_matrix[0][j] )
                        #pattern b
                        for k in range(j+1, len(self.footprint_matrix[i])):
                            if self.footprint_matrix[i][k] == "right":
                                if self.footprint_matrix[j][k] == "#":
                                    self.XLb[0].append( self.footprint_matrix[i][0] )
                                    self.XLb[1].append([])
                                    self.XLb[1][len(self.XLb[1])-1].append( self.footprint_matrix[0][j] )
                                    self.XLb[1][len(self.XLb[1])-1].append( self.footprint_matrix[0][k] )
                    #pattern c - can use same 'for' loops because the matrix is square
                    if self.footprint_matrix[j][i] == "right":
                        for k in range(j+1, len(self.footprint_matrix[i])):
                            if self.footprint_matrix[k][i] == "right":
                                if self.footprint_matrix[j][k] == "#":
                                    self.XLc[0].append([])
                                    self.XLc[0][len(self.XLc[0])-1].append( self.footprint_matrix[j][0] )
                                    self.XLc[0][len(self.XLc[0])-1].append( self.footprint_matrix[k][0] )
                                    self.XLc[1].append( self.footprint_matrix[0][i] )
            #create XL captions
            XL_caption, XL_caption_rect = make_text( text= "XL  = " , font_name= 'calibri-font-sv\Calibri Bold.ttf'\
                                                        , size= 25, pos= (self.window_rect.width*3/28, self.window_rect.height*5/25)\
                                                        , text_color= (255, 180, 69), text_background_color= (0, 0, 0))
            XLa_caption, XLa_caption_rect = make_text( text= "pattern a  = " , font_name= 'calibri-font-sv\Calibri Bold.ttf'\
                                                        , size= 25, pos= (self.window_rect.width*9/28, self.window_rect.height*3/25)\
                                                        , text_color= (255, 180, 69), text_background_color= (0, 0, 0))
            XLb_caption, XLb_caption_rect = make_text( text= "pattern b  = " , font_name= 'calibri-font-sv\Calibri Bold.ttf'\
                                                        , size= 25, pos= (self.window_rect.width*17/28, self.window_rect.height*3/25)\
                                                        , text_color= (255, 180, 69), text_background_color= (0, 0, 0))
            XLc_caption, XLc_caption_rect = make_text( text= "pattern c = " , font_name= 'calibri-font-sv\Calibri Bold.ttf'\
                                                        , size= 25, pos= (self.window_rect.width*23/28, self.window_rect.height*3/25)\
                                                        , text_color= (255, 180, 69), text_background_color= (0, 0, 0))
            
            #create XL patterns surfaces
            XL_text = [[], []]
            for pattern_num in range(0, len(self.XLa[0])):
                if pattern_num % 2 == 0:
                    position =  (self.window_rect.width*7/28, self.window_rect.height*(5+pattern_num/2)/25)
                else:
                    position =  (self.window_rect.width*11/28, self.window_rect.height*(5+(pattern_num-1)/2)/25)
                XLa_t, XLa_t_rect = make_text( text= "%c -> %c" %(self.XLa[0][pattern_num],self.XLa[1][pattern_num]), font_name= 'calibri-font-sv\Calibri Bold.ttf'\
                                                        , size= 25, pos= position\
                                                        , text_color= (72, 144, 220), text_background_color= (0, 0, 0))
                XL_text[0].append(XLa_t)
                XL_text[1].append(XLa_t_rect)

            for pattern_num in range(0, len(self.XLb[0])):
                XLb_t, XLb_t_rect = make_text( text= "%c -> (%c # %c)" %(self.XLb[0][pattern_num],self.XLb[1][pattern_num][0],self.XLb[1][pattern_num][1]), font_name= 'calibri-font-sv\Calibri Bold.ttf'\
                                                        , size= 25, pos= (self.window_rect.width*17/28, self.window_rect.height*(5+pattern_num)/25)\
                                                        , text_color= (72, 144, 220), text_background_color= (0, 0, 0))
                XL_text[0].append(XLb_t)
                XL_text[1].append(XLb_t_rect)

            for pattern_num in range(0, len(self.XLc[0])):
                XLc_t, XLc_t_rect = make_text( text= "(%c # %c) -> %c" %(self.XLc[0][pattern_num][0], self.XLc[0][pattern_num][1], self.XLc[1][pattern_num]), font_name= 'calibri-font-sv\Calibri Bold.ttf'\
                                                        , size= 25, pos= (self.window_rect.width*23/28, self.window_rect.height*(5+pattern_num)/25)\
                                                        , text_color= (72, 144, 220), text_background_color= (0, 0, 0))
                XL_text[0].append(XLc_t)
                XL_text[1].append(XLc_t_rect)

            #create YL caption
            YL_caption, YL_caption_rect = make_text( text= "YL  = " , font_name= 'calibri-font-sv\Calibri Bold.ttf'\
                                                        , size= 25, pos= (self.window_rect.width*3/28, self.window_rect.height*(5 + 1 + round(len(self.XLa[0])/2))/25)\
                                                        , text_color= (255, 180, 69), text_background_color= (0, 0, 0))

            #Create YL - subset of XL 
            self.YLa = [[],[]] # YL - pattern a : a -> b
            self.YLb = [[],[]] # YL - pattern b : a -> (b#c)
            self.YLc = [[],[]] # YL - pattern c : (b#c) -> d

            self.YLb[0] = self.XLb[0][:]
            for pattern_num in range(0, len(self.XLb[1])): 
                self.YLb[1].append( self.XLb[1][pattern_num][:] ) 

            for pattern_num in range(0, len(self.XLc[0])): 
                self.YLc[0].append( self.XLc[0][pattern_num][:] ) 
            self.YLc[1] = self.XLc[1][:]

            for pattern_num_a in range(0, len(self.XLa[0])):
                add = True
                for pattern_num_b in range(0, len(self.YLb[0])): 
                    if self.XLa[0][pattern_num_a] in self.YLb[0][pattern_num_b] and self.XLa[1][pattern_num_a] in self.YLb[1][pattern_num_b]:
                        add = False
                for pattern_num_c in range(0, len(self.YLc[0])): 
                    if self.XLa[0][pattern_num_a] in self.YLc[0][pattern_num_c] and self.XLa[1][pattern_num_a] in self.YLc[1][pattern_num_c]:
                        add = False
                if add == True:
                    self.YLa[0].append(self.XLa[0][pattern_num_a])
                    self.YLa[1].append(self.XLa[1][pattern_num_a])

            #create YL patterns surfaces
            YL_text = [[], []]
            for pattern_num in range(0, len(self.YLa[0])):
                if pattern_num % 2 == 0:
                    position =  (self.window_rect.width*7/28, self.window_rect.height*(5 + pattern_num/2 + 1 + round(len(self.XLa[0])/2))/25)
                else:
                    position =  (self.window_rect.width*11/28, self.window_rect.height*(5+(pattern_num-1)/2 + 1 + round(len(self.XLa[0])/2))/25)
                XLa_t, XLa_t_rect = make_text( text= "%c -> %c" %(self.YLa[0][pattern_num],self.YLa[1][pattern_num]), font_name= 'calibri-font-sv\Calibri Bold.ttf'\
                                                        , size= 25, pos= position\
                                                        , text_color= (72, 144, 220), text_background_color= (0, 0, 0))
                YL_text[0].append(XLa_t)
                YL_text[1].append(XLa_t_rect)

            for pattern_num in range(0, len(self.YLb[0])):
                XLb_t, XLb_t_rect = make_text( text= "%c -> (%c # %c)" %(self.YLb[0][pattern_num],self.YLb[1][pattern_num][0],self.YLb[1][pattern_num][1]), font_name= 'calibri-font-sv\Calibri Bold.ttf'\
                                                        , size= 25, pos= (self.window_rect.width*17/28, self.window_rect.height*(5 + pattern_num + 1 + round(len(self.XLa[0])/2))/25)\
                                                        , text_color= (72, 144, 220), text_background_color= (0, 0, 0))
                YL_text[0].append(XLb_t)
                YL_text[1].append(XLb_t_rect)

            for pattern_num in range(0, len(self.YLc[0])):
                XLc_t, XLc_t_rect = make_text( text= "(%c # %c) -> %c" %(self.YLc[0][pattern_num][0], self.YLc[0][pattern_num][1], self.YLc[1][pattern_num]), font_name= 'calibri-font-sv\Calibri Bold.ttf'\
                                                        , size= 25, pos= (self.window_rect.width*23/28, self.window_rect.height*(5 + pattern_num + 1 + round(len(self.XLa[0])/2))/25)\
                                                        , text_color= (72, 144, 220), text_background_color= (0, 0, 0))
                YL_text[0].append(XLc_t)
                YL_text[1].append(XLc_t_rect)

            #Create picture
            self.bg2 = pg.Surface( self.window.get_size() ).convert()
            self.bg2.fill( (0, 0, 0) )
            self.bg2_rect = self.bg2.get_rect( topleft = (0,0) )

            self.bg2.blit( self.main_text, self.main_text_rect )

            self.bg2.blit( XL_caption, XL_caption_rect )
            self.bg2.blit( XLa_caption, XLa_caption_rect )
            self.bg2.blit( XLb_caption, XLb_caption_rect )
            self.bg2.blit( XLc_caption, XLc_caption_rect )

            for pattern_num in range(0, len(XL_text[0]) ):
                self.bg2.blit( XL_text[0][pattern_num], XL_text[1][pattern_num] ) 

            self.bg2.blit( YL_caption, YL_caption_rect )

            for pattern_num in range(0, len(YL_text[0]) ):
                self.bg2.blit( YL_text[0][pattern_num], YL_text[1][pattern_num] ) 

            self.initialized = 2

        elif self.current_phase == 3:#####################################
            #Import graphics
            start_bpmn, start_bpmn_rect = load_image("start.png")
            end_bpmn, end_bpmn_rect = load_image("end.png")
            exclusive_bpmn, exclusive_bpmn_rect = load_image("exclusive.png")
            parallel_bpmn, parallel_bpmn_rect = load_image("parallel.png")
            arrow_right, arrow_right_rect = load_image("arrow_right.png")
            #Create bpmn # BPMN is a table, field with number i, j is table [ surface, surface_rect ]
            self.BPMN_connections = [[],[]]
            self.BPMN = []
            
            #create activities surfaces
            activities_surfaces = [[],[]] # first table are letters, second are surfaces with rects
            activities_surfaces[0] = self.diff_names[3][:]

            for i in self.diff_names:
                print(i)

            for name in self.diff_names[2]:
                activities_surfaces[1].append([])
                a_s, a_s_rect = create_activity_surf( name )
                activities_surfaces[1][ len(activities_surfaces[1])-1 ].append( a_s )
                activities_surfaces[1][ len(activities_surfaces[1])-1 ].append( a_s_rect )

            #creating start event
            if len(self.TI) == 2: 
                self.BPMN = BPMN_add_column( self.BPMN )
                self.BPMN[0][0].append(start_bpmn)#adding start event
                self.BPMN[0][0].append(start_bpmn_rect)
                self.BPMN_connections[0].append([0,-1])#adding connection from 'nowhere' into start
                self.BPMN_connections[1].append([0,0])

                self.BPMN = BPMN_add_column( self.BPMN )
                self.BPMN[0][1].append(exclusive_bpmn)#adding exclusive gateway
                self.BPMN[0][1].append(exclusive_bpmn_rect)

                self.BPMN = BPMN_add_column( self.BPMN )
                self.BPMN = BPMN_add_row( self.BPMN )
                self.BPMN[0][2].append( activities_surfaces[1][activities_surfaces[0].index( self.TI[0] )][0] )#adding first activity
                self.BPMN[0][2].append( activities_surfaces[1][activities_surfaces[0].index( self.TI[0] )][1] )
                self.BPMN_connections[0].append([0,1])#adding connection from 'end' into 'nowhere'
                self.BPMN_connections[1].append([0,2])

                self.BPMN[1][2].append( activities_surfaces[1][activities_surfaces[0].index( self.TI[1] )][0] )#adding first activity
                self.BPMN[1][2].append( activities_surfaces[1][activities_surfaces[0].index( self.TI[1] )][1] )
                self.BPMN_connections[0].append([0,1])#adding connection from 'end' into 'nowhere'
                self.BPMN_connections[1].append([1,2])
            else:
                self.BPMN = BPMN_add_column( self.BPMN )
                self.BPMN[0][0].append(start_bpmn)#adding start event
                self.BPMN[0][0].append(start_bpmn_rect)
                self.BPMN_connections[0].append([0,-1])#adding connection from 'nowhere' into start
                self.BPMN_connections[1].append([0,0])

                self.BPMN = BPMN_add_column( self.BPMN )
                self.BPMN[0][1].append( activities_surfaces[1][activities_surfaces[0].index( self.TI[0] )][0] )#adding first activity
                self.BPMN[0][1].append( activities_surfaces[1][activities_surfaces[0].index( self.TI[0] )][1] )
                self.BPMN_connections[0].append([0,0])#adding connection from 'end' into 'nowhere'
                self.BPMN_connections[1].append([0,1])

            #creating end event
            self.BPMN = BPMN_add_column( self.BPMN )
            self.BPMN = BPMN_add_column( self.BPMN )
            for end_event_num in range(0, len(self.TO) ):
                if len(self.BPMN )-1 < end_event_num:
                    self.BPMN = BPMN_add_row( self.BPMN )
                self.BPMN[end_event_num][len(self.BPMN[end_event_num])-2].append( activities_surfaces[1][activities_surfaces[0].index( self.TO[end_event_num] )][0] )#adding first activity
                self.BPMN[end_event_num][len(self.BPMN[end_event_num])-2].append( activities_surfaces[1][activities_surfaces[0].index( self.TO[end_event_num] )][1] )

                self.BPMN[end_event_num][len(self.BPMN[end_event_num])-1].append( end_bpmn )#adding first activity
                self.BPMN[end_event_num][len(self.BPMN[end_event_num])-1].append( end_bpmn_rect )

                self.BPMN_connections[0].append([end_event_num, len(self.BPMN[end_event_num])-2])#adding connection from 'end' into 'nowhere'
                self.BPMN_connections[1].append([end_event_num, len(self.BPMN[end_event_num])-1])
            

            #Create picture
            self.bg3 = pg.Surface( self.window.get_size() ).convert()
            self.bg3.fill( (0, 0, 0) )
            self.bg3_rect = self.bg3.get_rect( topleft = (0,0) )

            self.bg3.blit( self.main_text, self.main_text_rect )

            #bliting connections
            for i in range(0, len(self.BPMN_connections[0]) ):
                if self.BPMN_connections[0][i][1] != -1:
                    start_pos = ( self.window_rect.width * (self.BPMN_connections[0][i][1] * 2 + 1)/(len(self.BPMN[0]) * 2), self.window_rect.height * (self.BPMN_connections[0][i][0] * 2 + 1)/(len(self.BPMN) * 2)  )
                    start_surf_rect = self.BPMN[ self.BPMN_connections[0][i][0] ][ self.BPMN_connections[0][i][1] ][1]
                    start_pos = (start_pos[0] + start_surf_rect.width/2 , start_pos[1])
                else:
                    start_pos = ( self.window_rect.width * 1/(len(self.BPMN[0]) * 4), self.window_rect.height * (self.BPMN_connections[0][i][0] * 2 + 1)/(len(self.BPMN) * 2)  )
                
                if self.BPMN_connections[1][i][1] != 1000:
                    end_pos = ( self.window_rect.width * (self.BPMN_connections[1][i][1] * 2 + 1)/(len(self.BPMN[0]) * 2), self.window_rect.height * (self.BPMN_connections[1][i][0] * 2 + 1)/(len(self.BPMN) * 2)  )
                    end_surf_rect = self.BPMN[ self.BPMN_connections[1][i][0] ][ self.BPMN_connections[1][i][1] ][1]
                    end_pos = (end_pos[0] - end_surf_rect.width/2 , end_pos[1])
                else:
                    end_pos = ( self.window_rect.width * ((len(self.BPMN[1]) * 2) - 1)/(len(self.BPMN[1]) * 2), self.window_rect.height * (self.BPMN_connections[1][i][0] * 2 + 1)/(len(self.BPMN) * 2)  )

                BPMN_draw_line(self.bg3, start_pos, end_pos, True, [arrow_right, arrow_right_rect])

            #bliting activities, events ....
            for i in range(0, len(self.BPMN)):
                for j in range(0, len(self.BPMN[i])):
                    if len(self.BPMN[i][j]) == 2:
                        self.BPMN[i][j][1].center = ( self.window_rect.width * (2*j+1) / (2*len(self.BPMN[i]) ), self.window_rect.height * (2*i+1) / (2*len(self.BPMN) ) )
                        self.bg3.blit( self.BPMN[i][j][0], self.BPMN[i][j][1] )

            self.initialized = 3

        elif self.current_phase == 4:#####################################
            #Create picture
            self.bg4 = pg.Surface( self.window.get_size() ).convert()
            self.bg4.fill( (0, 0, 0) )
            self.bg4_rect = self.bg4.get_rect( topleft = (0,0) )

            self.text4, self.text_rect4 = make_text( text= "4", font_name= 'calibri-font-sv\Calibri Bold.ttf'\
                                                    , size= 35, pos= (self.window_rect.centerx,self.window_rect.centery)\
                                                    , text_color= (72, 144, 220), text_background_color= (0, 0, 0))
            self.bg4.blit( self.text4, self.text_rect4 )

            self.initialized = 1

            self.initialized = 4
    
    def display(self, ):
        if self.current_phase == 0:
            self.window.blit( self.bg0, self.bg0_rect )
        elif self.current_phase == 1:
            self.window.blit( self.bg1, self.bg1_rect )
        elif self.current_phase == 2:
            self.window.blit( self.bg2, self.bg2_rect )
        elif self.current_phase == 3:
            self.window.blit( self.bg3, self.bg3_rect )
        elif self.current_phase == 4:
            self.window.blit( self.bg4, self.bg4_rect )

    def run(self):
        """Main loop"""

        while not self.handle_events():
            mx, my = pg.mouse.get_pos()

            if self.current_phase > self.initialized:
                self.initialization()

            self.display()

            self.allsprites.update()
            self.allsprites.draw( self.window )

            #button images support
            for i, button_name in enumerate( self.buttons ):
                if self.buttons[button_name][0].rect.collidepoint( ( mx, my ) ):
                    if self.click_down == True:
                        self.buttons[button_name][0].push()
                    elif self.click_up == True:
                        self.buttons[button_name][1] = True #option was choosed
                    else:
                        self.buttons[button_name][0].release()
                else:
                    self.buttons[button_name][0].release()

            #button reaction support
            for i, button_name in enumerate( self.buttons ):
                if self.buttons[button_name][1] == True:
                    if button_name == "right":
                        if self.current_phase < self.phase_range[1]:
                            self.current_phase += 1
                    if button_name == "left":
                        if self.current_phase > self.phase_range[0]:
                            self.current_phase -= 1
                    if button_name == "exit":
                        return True
                    self.buttons[button_name][1] = False

            pg.display.flip()

            self.clock.tick(60)

    def handle_events(self):
        """
        Handling system events

        :return True if pg reported a quit event
        """
        self.click_up = False
        for event in pg.event.get():
            if event.type == pg.locals.QUIT:
                pg.quit()
                sys.exit() 
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                return True
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.click_down = True
            elif event.type == MOUSEBUTTONUP:
                if event.button == 1:
                    self.click_up = True
                    self.click_down = False