import pygame as pg
from pygame.locals import *

# from pm4py.objects.log.importer.xes import factory as xes_import_factory

# import sys
# import os

from load import make_text, load_image

class BPMN():
    def __init__(self, activities):
        """
        :param activities: table [[],[]] first table are real names of activities, second are new names
        """
        self._board = [[None]]
        self._connections = { "from" : [],
                              "to" : []}
        self.start_bpmn, self.start_bpmn_rect = load_image("start.png")
        self.start_text, self.start_text_rect = make_text( text= "START", font_name= 'calibri-font-sv\Calibri Bold.ttf'\
                                                    , size= 15, pos= (self.start_bpmn_rect.width/2, 60)\
                                                    , text_color= (72, 144, 220), text_background_color= (0, 0, 0))
        self.start_bpmn.blit( self.start_text, self.start_text_rect )

        self.end_bpmn, self.end_bpmn_rect = load_image("end.png")
        self.end_text, self.end_text_rect = make_text( text= "END", font_name= 'calibri-font-sv\Calibri Bold.ttf'\
                                                    , size= 15, pos= (self.end_bpmn_rect.width/2, 60)\
                                                    , text_color= (72, 144, 220), text_background_color= (0, 0, 0))
        self.end_bpmn.blit( self.end_text, self.end_text_rect )

        self.exclusive_bpmn, self.exclusive_bpmn_rect = load_image("exclusive.png")
        self.parallel_bpmn, self.parallel_bpmn_rect = load_image("parallel.png")
        self.arrow_right, self.arrow_right_rect = load_image("arrow_right.png")
        self.arrow_left, self.arrow_left_rect = load_image("arrow_left.png")

        self.already_on = []

        self.activities_surfaces = [[],[]] # table where first row are names of activities e.g ["a", "b"], and second row are surfaces and surfaces_rects of this activities e.g [ [a_surf, a_surf_rect], [b_surf, b_surf_rect]]
        self.activities_surfaces[0] = activities[1][:]

        for name in activities[0]:
            self.activities_surfaces[1].append([])
            a_s, a_s_rect = self.create_activity_surf( name )
            self.activities_surfaces[1][ len(self.activities_surfaces [1])-1 ].append( a_s )
            self.activities_surfaces[1][ len(self.activities_surfaces [1])-1 ].append( a_s_rect )

    @property
    def height(self):
        return len(self._board)

    @property
    def width(self):
        return len(self._board[0])

    def create_start(self, TI):
        #create start
        if len( TI ) == 2: 
            self.add_elem_on_board( "start", [0,0])
            self.add_column()
            self.add_elem_on_board( "exclusive", [0,1])
            self.add_connection([0,0], [0,1])

            self.add_column()
            self.add_row()

            self.add_elem_on_board( TI[0], [0,2])
            self.add_connection([0,1], [0,2])

            self.add_elem_on_board( TI[1], [1,2])
            self.add_connection([0,1], [1,2])
        elif len( TI ) == 1: 
            self.add_elem_on_board( "start", [0,0])
            self.add_column()

            self.add_elem_on_board( TI[0], [0,1])
            self.add_connection([0,0], [0,1])
        else:
            print( "BPMN model isnt ready for more then 2 start activities" )

    def create_end(self, TI, TO):
        #create end
        self.start_width = self.width

        self.add_column()
        for to_elem in TO:
            if to_elem in TI: 
                if self.get_activity( [ TI.index(to_elem), 2 ] ) == None: # If place that we want put elem into is empty
                    self.add_elem_on_board( "end", [ TI.index(to_elem), 2 ])
                else:# If not we have to find free place to move element
                    for row_num in range( 0, self.height ):# go through whole column
                        if self.get_activity( [row_num, self.start_width] ) == None: # if we find empty place we move element there
                            found = True
                            move_elem( [ TI.index(to_elem), 2 ], [row_num, self.start_width] )
                            self.add_elem_on_board( "end", [ TI.index(to_elem), 2 ])
                        if found == False:#otherwise we have to add new row and then move elem
                            self.add_row()
                            move_elem([ TI.index(to_elem), 2 ], [self.height - 1, self.start_width])
                            self.add_elem_on_board( "end", [ TI.index(to_elem), 2 ])
            else:
                if self.width == self.start_width + 1:
                    self.add_column()
                found = False
                for row_num in range( 0, self.height ):
                    if self.get_activity( [row_num, self.start_width] ) == None:
                        found = True
                        self.add_elem_on_board( to_elem, [ row_num, self.start_width ])
                        self.add_elem_on_board( "end", [ row_num, self.start_width + 1 ])
                        self.add_connection(  [ row_num, self.start_width ], [ row_num, self.start_width + 1 ] )
                        break
                    if found == False:
                        self.add_row()
                        self.add_elem_on_board( to_elem, [ self.height - 1, self.start_width ])
                        self.add_elem_on_board( "end", [ self.height - 1, self.start_width + 1 ])
                        self.add_connection(  [ self.height - 1, self.start_width ], [ self.height - 1, self.start_width + 1 ] )
                        break

    def create_patt_a(self, TI, TO, YLa):
        #create pattern a
        #checking how many fields separate the beginning and the end 
        move_about = 0
        what_side = -1
        for pat_num in range(0, len(YLa[0])):
            if YLa[0][pat_num] in TI and YLa[1][pat_num] in TO:
                pass
            elif (YLa[0][pat_num] not in TI and YLa[1][pat_num] in TO) or (YLa[0][pat_num] in TI and YLa[1][pat_num] not in TO):
                if what_side == -1:
                    move_about = 1
                    if YLa[0][pat_num] in TI:
                        what_side = 0
                    elif YLa[1][pat_num] in TO:
                        what_side = 1
                elif what_side == 0:
                    if YLa[1][pat_num] in TO:
                        move_about = 2
                        what_side = 2
                        break
                elif what_side == 1:
                    if YLa[0][pat_num] in TI :
                        move_about = 2
                        what_side = 2
                        break
            else:
                move_about = 2
                break
        #adding columns
        self.add_column(move_about)
        #moving all elements from "move_about" number of columns to the right
        for i in range(0, 2):
            for row_num in range(0, self.height):
                self.move_elem( [row_num, self.width - 1 - i - move_about] , [row_num, self.width - 1 - i])

        #putting pattern a on board
        for pat_num in range(0, len(YLa[0])):
            if YLa[0][pat_num] in TI and YLa[1][pat_num] in TO:# if start activity and end activity is in pattern a
                self.add_connection( find_in_board(YLa[0][pat_num]), find_in_board(YLa[1][pat_num]) )

            elif YLa[0][pat_num] in TI:# if start activity is in pattern a
                coord = self.find_in_board( YLa[0][pat_num] )
                if YLa[1][pat_num] not in self.already_on:
                    if self._board[ coord[0]][ coord[1] + 1] == None:
                        self.add_elem_on_board( YLa[1][pat_num], [coord[0], coord[1] + 1] )
                        self.add_connection( coord, [coord[0], coord[1] + 1] )
                    else:
                        found = False
                        for row_num in range(0, self.height): 
                            if self._board[row_num][coord[1] + 1] == None:
                                found = True
                                self.add_elem_on_board( YLa[1][pat_num], [row_num, coord[1] + 1] )
                                self.add_connection( coord, [row_num, coord[1] + 1] )
                                break
                        if found == False:
                            self.add_row()
                            self.add_elem_on_board( YLa[1][pat_num], [self.height - 1, coord[1] + 1] )
                            self.add_connection( coord, [self.height - 1, coord[1] + 1] )
                else:#if element is already on board
                    self.add_connection( coord, self.find_in_board( YLa[1][pat_num]  ) )
                
            elif YLa[1][pat_num] in TO:# if end activity is in pattern a
                coord = self.find_in_board( YLa[1][pat_num] )
                if YLa[0][pat_num] not in self.already_on:
                    self.add_elem_on_board( YLa[0][pat_num], [coord[0], coord[1] - 1] )
                    self.add_connection( [coord[0], coord[1] - 1], coord )
                else:
                    self.add_connection( self.find_in_board( YLa[0][pat_num]  ) , coord)

        for pat_num in range(0, len(YLa[0])):
            found = False
            if YLa[0][pat_num] not in self.already_on and YLa[1][pat_num] not in self.already_on:
                if YLa[0][pat_num] not in TI and YLa[1][pat_num] not in TO:
                    for row_num in range(0, self.height):
                        if self._board[row_num][self.start_width] == None and self._board[row_num][self.start_width + 1] == None:
                            found = True
                            if YLa[0][pat_num] not in self.already_on:
                                self.add_elem_on_board( YLa[0][pat_num], [row_num, self.start_width] )
                            if YLa[1][pat_num] not in self.already_on:
                                self.add_elem_on_board( YLa[1][pat_num], [row_num, self.start_width + 1] )
                            self.add_connection( self.find_in_board( YLa[0][pat_num]  ), self.find_in_board( YLa[1][pat_num]  ) )
                            break
                    if found == False:
                        self.add_row()
                        if YLa[0][pat_num] not in self.already_on:
                            self.add_elem_on_board( YLa[0][pat_num], [self.height - 1, self.start_width] )
                        if YLa[1][pat_num] not in self.already_on:
                            self.add_elem_on_board( YLa[1][pat_num], [self.height - 1, self.start_width + 1] )
                        self.add_connection( self.find_in_board( YLa[0][pat_num]  ), self.find_in_board( YLa[1][pat_num]  ) )
            else:
                self.add_connection( self.find_in_board( YLa[0][pat_num]  ), self.find_in_board( YLa[1][pat_num]  ) )

    def create_patt_b(self, YLb):
        #create pattern b
        #put YLb[0] and "exclusive" on board
        for pat_num in range(0, len(YLb[0])):
            if YLb[0][pat_num] not in YLb[0][0:pat_num]:# if you haven't checked this name yet
                if YLb[0][pat_num] not in self.already_on:# YLb[0][pat_num] isn't already on board
                    found = False
                    for row_num in range(0, self.height):# we try to find two places with "None" placed next to each other
                        if found == False:
                            for col_num in range( self.start_width, self.width - 2 ):
                                if self._board[row_num][col_num] == None and self._board[row_num][col_num + 1] == None:
                                    found = True
                                    self.add_elem_on_board( YLb[0][pat_num], [row_num, col_num] )
                                    self.add_elem_on_board( "exclusive", [row_num, col_num + 1] )
                                    self.add_connection( [row_num, col_num], [row_num, col_num + 1] )
                                    break
                    if found == False:
                        self.add_row()
                        self.add_elem_on_board( YLb[0][pat_num], [self.height - 1, self.start_width] )
                        self.add_elem_on_board( "exclusive", [self.height - 1, self.start_width + 1] )
                        self.add_connection( [self.height - 1, self.start_width ], [self.height - 1, self.start_width + 1] )
                else:#if YLb[0][pat_num] is already on board we just add exclusive
                    coord = self.find_in_board( YLb[0][pat_num] )
                    if self._board[ coord[0]][ coord[1] + 1 ] == None:
                        self.add_elem_on_board ( "exclusive", [ coord[0], coord[1] + 1 ] )
                        self.add_connection( [ coord[0], coord[1] ], [ coord[0], coord[1] + 1 ] )
                    else:
                        self.add_column()
                        for i in range(0, self.width - 2 - coord[1] ):
                            for row_num in range(0, self.height):
                                self.move_elem( [row_num, self.width - 1 - i - 1] , [row_num, self.width - 1 - i])
                        self.add_elem_on_board ( "exclusive", [ coord[0], coord[1] + 1 ] )
                        self.add_connection( [ coord[0], coord[1] ], [ coord[0], coord[1] + 1 ] )
        
        # put YLb[1] on board
        for pat_num in range(0, len(YLb[1])):
            elem_0 = YLb[1][pat_num][0]
            elem_1 = YLb[1][pat_num][1]
            coord = self.find_in_board( YLb[0][pat_num] )
            for con_num in range( 0, len( self._connections['from'] ) ):
                if self._connections['from'][con_num] == coord:
                    if self._board[ self._connections['to'][con_num][0] ][ self._connections['to'][con_num][1] ] == "exclusive":
                        coord = self._connections['to'][con_num]
                        break
            #coord = [ coord[0], coord[1] + 1 ]# set coord on coordinates of exclusive
            if elem_0 in self.already_on and elem_1 in self.already_on:
                coord_0 = self.find_in_board( elem_0 )
                coord_1 = self.find_in_board( elem_1 )
                self.add_connection( coord, coord_0)
                self.add_connection( coord, coord_1)
            elif (elem_0 not in self.already_on and elem_1 in self.already_on) or (elem_0 in self.already_on and elem_1 not in self.already_on):
                if elem_0 in self.already_on:
                    coord_0 = self.find_in_board( elem_0 )
                else:
                    coord_0 = self.find_in_board( elem_1 )
                # coord_0 is are cooridinates of element of YLb[1][pat_num] that is on board
                found = False
                if self.height >= coord_0[0] + 2:
                    if self._board[ coord_0[0] + 1 ][ coord_0[1] ] == None:
                        found = True
                if found == False:
                    self.add_row()
                    for row_num_of_move in range(0, self.height - 2 - coord_0[0] ):
                        self.move_elem( [coord_0[1] + 1 + row_num_of_move, coord_0[1] ], [coord_0[1] + 2 + row_num_of_move, coord_0[1] ])
                self.add_elem_on_board( elem_1, [ coord_0[0] + 1, coord_0[1] ] )
                self.add_connection( coord, coord_0)
                self.add_connection( coord, [ coord_0[0] + 1, coord_0[1] ])

            elif elem_0 not in self.already_on and elem_1 not in self.already_on:
                if self._board[ coord[0]][ coord[1] + 1 ] == None and self._board[ coord[0] + 1][ coord[1] + 1 ] == None:
                    pass
                else:
                    self.add_column()
                    for i in range(0, self.width - 2 - coord[1] ):
                        for row_num in range(coord[0], coord[0]+2):
                            self.move_elem( [row_num, self.width - 1 - i - 1] , [row_num, self.width - 1 - i])
                self.add_elem_on_board( elem_0, [ coord[0], coord[1] + 1 ] )
                self.add_elem_on_board( elem_1, [ coord[0] + 1, coord[1] + 1 ] )
                self.add_connection( coord, [ coord[0], coord[1] + 1 ] )
                self.add_connection( coord, [ coord[0] + 1, coord[1] + 1 ] )

    def create_patt_c(self, YLc):
        #create pattern c
        #put YLc[1] and "exclusive" on board
        for pat_num in range(0, len(YLc[1])):
            if YLc[1][pat_num] not in YLc[1][0:pat_num]:# if you haven't checked this name yet
                if YLc[1][pat_num] not in self.already_on:# YLc[1][pat_num] isn't already on board
                    found = False
                    for row_num in range(0, self.height):# we try to find two places with "None" placed next to each other
                        if found == False:
                            for col_num in range( self.start_width + 1, self.width - 2 ):
                                if self._board[row_num][col_num] == None and self._board[row_num][col_num - 1] == None:
                                    found = True
                                    self.add_elem_on_board( YLc[1][pat_num], [row_num, col_num] )
                                    self.add_elem_on_board( "exclusive", [row_num, col_num - 1] )
                                    self.add_connection( [row_num, col_num - 1], [row_num, col_num] )
                                    break
                    if found == False:
                        self.add_row()
                        self.add_elem_on_board( YLc[0][pat_num], [self.height - 1, self.width - 2] )
                        self.add_elem_on_board( "exclusive", [self.height - 1, self.width - 3] )
                        self.add_connection( [self.height - 1, self.width - 3 ], [self.height - 1, self.width - 2] )
                else:#if YLc[0][pat_num] is already on board we just add exclusive
                    coord = self.find_in_board( YLc[1][pat_num] )
                    if self._board[ coord[0]][ coord[1] - 1 ] == None:
                        self.add_elem_on_board ( "exclusive", [ coord[0], coord[1] - 1 ] )
                        self.add_connection( [ coord[0], coord[1] - 1], [ coord[0], coord[1] ] )
                    else:
                        self.add_column()
                        for i in range(0, self.width - 2 - coord[1] + 1 ):
                            for row_num in range(0, self.height):
                                self.move_elem( [row_num, self.width - 1 - i - 1] , [row_num, self.width - 1 - i])
                        self.add_elem_on_board ( "exclusive", [ coord[0], coord[1] ] ) # YLc[i] was moved on right so we put exclusive on place
                        self.add_connection( [ coord[0], coord[1] ], [ coord[0], coord[1] + 1 ] )
        # put YLc[0] on board
        for pat_num in range(0, len(YLc[1])):
            elem_0 = YLc[0][pat_num][0]
            elem_1 = YLc[0][pat_num][1]
            coord = self.find_in_board( YLc[1][pat_num] )
            coord = [ coord[0], coord[1] - 1 ]# set coord on coordinates of exclusive
            if elem_0 in self.already_on and elem_1 in self.already_on:
                coord_0 = self.find_in_board( elem_0 )
                coord_1 = self.find_in_board( elem_1 )
                self.add_connection( coord_0, coord)
                self.add_connection( coord_1, coord)
            elif (elem_0 not in self.already_on and elem_1 in self.already_on) or (elem_0 in self.already_on and elem_1 not in self.already_on):
                if elem_0 in self.already_on:
                    coord_0 = self.find_in_board( elem_0 )
                else:
                    coord_0 = self.find_in_board( elem_1 )
                # coord_0 is are cooridinates of element of YLc[0][pat_num] that is on board
                found = False
                if self.height >= coord_0[0] + 2: # check if there is one more row under elem_0
                    if self._board[ coord_0[0] + 1 ][ coord_0[1] ] == None:
                        found = True
                if found == False:
                    self.add_row()
                    for row_num_of_move in range(0, self.height - 2 - coord_0[0] ):# how many objects you need to move
                        self.move_elem( [coord_0[1] + 1 + row_num_of_move, coord_0[1] ], [coord_0[1] + 2 + row_num_of_move, coord_0[1] ])
                self.add_elem_on_board( elem_1, [ coord_0[0] + 1, coord_0[1] ] )
                self.add_connection( coord_0, coord)
                self.add_connection( [ coord_0[0] + 1, coord_0[1] ], coord)

            elif elem_0 not in self.already_on and elem_1 not in self.already_on:
                if self._board[ coord[0]][ coord[1] - 1 ] == None and self._board[ coord[0] + 1][ coord[1] - 1 ] == None:
                    pass
                else:
                    self.add_column()
                    for i in range(0, self.width - 2 - coord[1] + 1 ):
                        for row_num in range(coord[0], coord[0]+2):
                            self.move_elem( [row_num, self.width - 1 - i - 1] , [row_num, self.width - 1 - i])
                self.add_elem_on_board( elem_0, [ coord[0], coord[1] ] )
                self.add_elem_on_board( elem_1, [ coord[0] + 1, coord[1] ] )
                self.add_connection( [ coord[0], coord[1] ], coord )
                self.add_connection( [ coord[0] + 1, coord[1] ], coord )

    def create_patt_d(self):
        #create pattern d
        for activity in self.already_on:
            connections = []
            activities = []
            coord = self.find_in_board( activity )
            for con_num in range(0, len( self._connections['from'] )):
                if self._connections['from'][con_num] == coord:
                    if len( self._board[ self._connections['to'][con_num][0] ][ self._connections['to'][con_num][1] ] ) == 1:
                        connections.append( [ self._connections['to'][con_num][0], self._connections['to'][con_num][1] ])
                        activities.append( self._board[ self._connections['to'][con_num][0] ][ self._connections['to'][con_num][1] ])
            if len(connections) >= 2: 
                self.add_column()
                for i in range(0, self.width - 2 - coord[1] ):
                    for row_num in range(0, self.height):
                        self.move_elem( [row_num, self.width - 1 - i - 1] , [row_num, self.width - 1 - i])
                self.add_elem_on_board( "parallel", [coord[0], coord[1] + 1] )
                self.add_connection( coord, [coord[0], coord[1] + 1] )

                for con_num in range(0, len( self._connections['from'] )):
                    if self._connections['from'][con_num] == coord:
                        for activ in activities:
                            if self._connections['to'][con_num] == self.find_in_board( activ ):
                                self._connections['from'][con_num][1] += 1
    
    def create_patt_e(self):
        #create pattern e
        for activity in self.already_on:
            connections = []
            activities = []
            coord = self.find_in_board( activity )
            for con_num in range(0, len( self._connections['to'] )):
                if self._connections['to'][con_num] == coord:
                    if len( self._board[ self._connections['from'][con_num][0] ][ self._connections['from'][con_num][1] ] ) == 1:
                        connections.append( [ self._connections['from'][con_num][0], self._connections['from'][con_num][1] ])
                        activities.append( self._board[ self._connections['from'][con_num][0] ][ self._connections['from'][con_num][1] ])
            if len(connections) >= 2: 
                self.add_column()
                for i in range(0, self.width - 2 - coord[1] + 1):
                    for row_num in range(0, self.height):
                        self.move_elem( [row_num, self.width - 1 - i - 1] , [row_num, self.width - 1 - i])
                self.add_elem_on_board( "parallel", [coord[0], coord[1]] )
                self.add_connection(  coord, [coord[0], coord[1] + 1])

                for con_num in range(0, len( self._connections['to'] )):
                    if self._connections['to'][con_num] == [ coord[0], coord[1] + 1 ]:
                        for activ in activities:
                            if self._connections['from'][con_num] == self.find_in_board( activ ):
                                self._connections['to'][con_num][1] -= 1

    def organize(self):


    def run(self, TI, TO, YLa, YLb, YLc):
        self.create_start( TI )
        self.create_end( TI, TO )
        self.create_patt_a( TI, TO, YLa )
        self.create_patt_b( YLb )
        self.create_patt_c( YLc )
        self.create_patt_d()
        self.create_patt_e()

        self.organize()
    
        return self.width, self.height

    def add_elem_on_board(self, elem_name, pos):
        """
        put elem surface and elem surface_rect into board on pos
        :param elem: name of element that will be added on board e.g "a"
        :param pos: position on the board on which the element is to be placed e.g [0, 5], 0 - row, 5 - col
        """
        #if (elem_name not in self.already_on) or (elem_name == "start" or elem_name == "end" or elem_name == "exclusive" or elem_name == "parallel"):
        if elem_name not in self.already_on:
            if self.get_activity(pos) == None:
                self._board[ pos[0] ][ pos[1] ] = elem_name 
                if elem_name != "start" and elem_name != "end" and elem_name != "exclusive" and elem_name != "parallel":
                    self.already_on.append(elem_name)
            else:
                print("you wanted to place: ", elem_name, " on place: ", pos[0], pos[1], " but there is already some surf")
        else:
            print("you wanted to place ", elem_name, "but it's already on board")

    def move_elem(self, from_pos, where_pos):
        if self.get_activity(where_pos) == None:
            self._board[where_pos[0]][where_pos[1]] = self._board[from_pos[0]][from_pos[1]]
            self._board[from_pos[0]][from_pos[1]] = None
            for start_pos in self._connections["from"]:
                if from_pos == start_pos: 
                    self._connections["from"][ self._connections["from"].index(start_pos)] = where_pos
                
            for end_pos in self._connections["to"]:
                if from_pos == end_pos: 
                    self._connections["to"][ self._connections["to"].index(end_pos)] = where_pos

    def move_all_right(self, start_width, how_much):
        """moves all elements on board to the right starting from "start_width" column

        :param start_width: number of column from where all columns will be move to the right
        :param how_much: number of fileds that all element will be moved to the right
        

    def find_in_board(self, name):
        """can find position of activity on the board when you give its name"""
        for row_num in range(0, len(self._board)):
            for col_num in range(0, len(self._board[row_num])):
                if self._board[row_num][col_num] == name:
                    return [row_num, col_num]
           
    def ele_pos(self, surf, pos_board):
        """returns possition on surface of element of given position in board
        
        :param surface: surface on which the BPMN model will be drawn, size is important
        :param pos_board: position of the element on the board whose position on the surface is to be returned, given as two integers [ column, row ]
        :return pos: pos in pixels of element given with pos
        """
        pos = [surf.get_width() * (pos_board[1] + 0.5)/self.width, surf.get_height() * (pos_board[0] + 0.5)/self.height]

        return pos

    def get_activity(self, pos):
        """gives name of activiti on given position on board"""
        if self._board[pos[0]][pos[1]] != None:
            return self._board[pos[0]][pos[1]]
        else:
            return None

    def add_connection(self, start_pos, end_pos):
        not_double = True
        for conn_num in range(0, len( self._connections['from'] ) ):
            if self._connections['from'][conn_num] == start_pos and self._connections['to'][conn_num] == end_pos:
                not_double = False
        if not_double:
            self._connections["from"].append([])
            self._connections["to"].append([])
            self._connections["from"][len(self._connections["from"])-1].append( start_pos[0] )
            self._connections["from"][len(self._connections["from"])-1].append( start_pos[1] )
            self._connections["to"][len(self._connections["to"])-1].append( end_pos[0] )
            self._connections["to"][len(self._connections["to"])-1].append( end_pos[1] )

    def create_activity_surf(self, name ):
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
        activity_surf = pg.Surface( (text_rect.width + 30, text_rect.height + 40) ).convert()
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

        self.draw_line(activity_surf, (top_left_corner_rect.right, top_left_corner_rect.top + 2), ( top_right_corner_rect.left, top_right_corner_rect.top + 2), False, 5 )
        self.draw_line(activity_surf, (top_right_corner_rect.right - 3, top_right_corner_rect.bottom), ( bottom_right_corner_rect.right - 3, bottom_right_corner_rect.top), False, 5 )
        self.draw_line(activity_surf, (bottom_right_corner_rect.left, bottom_right_corner_rect.bottom - 3), ( bottom_left_corner_rect.right, bottom_left_corner_rect.bottom - 3), False, 5 )
        self.draw_line(activity_surf, (bottom_left_corner_rect.left + 2, bottom_left_corner_rect.top), ( top_left_corner_rect.left + 2, top_left_corner_rect.bottom), False, 5 )

        activity_surf.blit( text, text_rect )

        return activity_surf, activity_surf_rect
    
    def get_activity_surf(self, name):
        if name != None:
            if name == "start":
                elem_surf, elem_surf_rect = self.start_bpmn, self.start_bpmn_rect
            elif name == "end":
                elem_surf, elem_surf_rect = self.end_bpmn, self.end_bpmn_rect
            elif name == "exclusive":
                elem_surf, elem_surf_rect = self.exclusive_bpmn, self.exclusive_bpmn_rect
            elif name == "parallel":
                elem_surf, elem_surf_rect = self.parallel_bpmn, self.parallel_bpmn_rect
            else:
                index = self.activities_surfaces[0].index( name )
                elem_surf = self.activities_surfaces[1][index][0]
                elem_surf_rect = self.activities_surfaces[1][index][1]

            return elem_surf, elem_surf_rect
        return None

    def add_row(self, how_many = 1):
        for j in range(0, how_many):
            self._board.append( [ None for i in range(0, self.width ) ] )

    def add_column(self, how_many = 1):
        for j in range(0, how_many):
            for i in range(0, self.height):
                self._board[i].append( None )

    def draw_line(self, surf, start_pos, end_pos, arrow = False, size = 3 ):
        if arrow:
            pg.draw.line( surf, (72, 144, 220), start_pos, end_pos, size )
            if start_pos[0] <= end_pos[0]:
                self.arrow_right_rect.right = end_pos[0]
                self.arrow_right_rect.top = end_pos[1] - self.arrow_right_rect.height/2 + 1
                surf.blit( self.arrow_right, self.arrow_right_rect )
            elif start_pos[0] > end_pos[0]:
                self.arrow_left_rect.left = end_pos[0]
                self.arrow_left_rect.top = end_pos[1] - self.arrow_left_rect.height/2 + 1
                surf.blit( self.arrow_left, self.arrow_left_rect )
        else:
            pg.draw.line(surf, (72, 144, 220), start_pos, end_pos, size)

    def draw_on(self, surf):
        """drawing BPMN model on given surface
        
        :param surface: surface on which the BPMN model will be drawn"""
        #bliting connections
        for connection_num in range(0, len(self._connections["from"]) ):
            start_pos = self.ele_pos( surf, self._connections["from"][connection_num] )
            if self.get_activity_surf(self.get_activity( self._connections["from"][connection_num] )) != None:
                start_surf, start_surf_rect = self.get_activity_surf(self.get_activity( self._connections["from"][connection_num] ))
            else:
                print("you try to get activity surf of start element with pos", self._connections["from"][connection_num], " but on this pos there is no elem")
            
            end_pos = self.ele_pos( surf, self._connections["to"][connection_num] )
            if self.get_activity_surf( self.get_activity( self._connections["to"][connection_num] )) != None:
                end_surf, end_surf_rect = self.get_activity_surf( self.get_activity( self._connections["to"][connection_num] )) #connection must end before activity, not in middle
            else:
                print("you try to get activity surf of end element with pos", self._connections["to"][connection_num], " but on this pos there is no elem")
            
            if start_pos[0] <= end_pos[0]:
                if self._board[ self._connections["from"][connection_num][0] ][ self._connections["from"][connection_num][1] ] != "start":
                    start_pos[0] += start_surf_rect.width/2
                else:
                    start_pos[0] += 15
                if self._board[ self._connections["to"][connection_num][0] ][ self._connections["to"][connection_num][1] ] != "end":
                    end_pos[0] -= end_surf_rect.width/2
                else:
                    end_pos[0] -= 15
            elif start_pos[0] > end_pos[0]:
                start_pos[0] -= start_surf_rect.width/2
                if self._board[ self._connections["to"][connection_num][0] ][ self._connections["to"][connection_num][1] ] != "end":
                    end_pos[0] += end_surf_rect.width/2
                else:
                    end_pos[0] += 15

            # self.draw_line( surf, start_pos, [ start_pos[0] + (end_pos[0] - start_pos[0])/2, start_pos[1] ] )
            # self.draw_line( surf, [ start_pos[0] +  (end_pos[0] - start_pos[0])/2, start_pos[1] ], [ start_pos[0] + (end_pos[0] - start_pos[0])/2, end_pos[1] ] )
            # self.draw_line( surf, [ start_pos[0] +  (end_pos[0] - start_pos[0])/2, end_pos[1] ], end_pos, True )

            self.draw_line( surf, start_pos, end_pos, True )

        #bliting activities, events ....
        for c in range(0, len(self._board)):
            for r in range(0, len(self._board[c])):
                if self._board[c][r] != None:#If there is name on possition
                    elem_surf, elem_surf_rect = self.get_activity_surf( self._board[c][r] )
                    elem_surf_rect.center = self.ele_pos(surf, [c, r])
                    surf.blit( elem_surf, elem_surf_rect )
