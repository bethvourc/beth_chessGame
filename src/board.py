from const import *
from square import Square
from piece import *
from move import Move
from sound import Sound
import copy
import os 

class Board:

    def __init__(self):
        self.squares = [[0, 0, 0, 0, 0, 0, 0, 0] for col in range(COLS)]
        self.last_move = None
        self._create()
        self._add_pieces("white")
        self._add_pieces("black")

    def move(self, piece, move):
        initial = move.initial
        final = move.final

        en_passant_empty = self.squares[final.row][final.col].isempty()

        # console board move update
        self.squares[initial.row][initial.col].piece = None
        self.squares[final.row][final.col].piece = piece
           

        # Pawn promotion
        if isinstance(piece, Pawn):
            # en passant capture
            diff = final.col - initial.col
            if diff != 0 and en_passant_empty:
                # console board move update
                self.squares[initial.row][initial.col + diff].piece = None
                self.squares[final.row][final.col].piece = piece
                sound  = Sound(os.path.join(
                    "assets/sounds/capture.wav"
                ))
                sound.play()

            # pawn en passant
            if self.en_passant(initial, final):
                piece.en_passant  = True

            else:
                # pawn promotion
                self.check_promotion(piece, final)

        # King castling 
        if isinstance(piece, King):
            if self.castling(initial, final):
                diff =  final.col - initial.col
                rook  = piece.left_rook if (diff < 0) else piece.right_rook
                self.move(rook, rook.moves[-1])


        # move
        piece.moved = True

        # clear valid moves
        piece.clear_moves()

        # set last move 
        self.last_move = move

    def valid_move(self, piece, move):
        return move in piece.moves


    def check_promotion(self, piece, final):
        if final.row == 0 or final.row == 7:
            self.squares[final.row][final.col].piece = Queen(piece.color)

    def castling(self, initial, final):
        return abs(initial.col - final.col) == 2
    
    def en_passant(self, initial, final):
        return abs(initial.row - final.row) == 2
    
    # create method to detect check/checkmate 
    def in_check(self, piece, move):
        temp_piece = copy.deepcopy(piece)
        temp_board = copy.deepcopy(self)
        temp_board.move(temp_piece, move)

        for row in range(ROWS):
            for col in range(COLS):
                if temp_board.squares[row][col].has_enemy_piece(piece.color):
                    p = temp_board.squares[row][col].piece
                    temp_board.calc_moves(p, row, col, bool=False)
                    for m in p.moves:
                        if isinstance(m.final.piece, King):
                            return True
        
        return False




    def calc_moves(self, piece, row, col, bool=True):
        """calculate all the valid moves of a piece on a specific position"""

        def pawn_moves():
            steps = 1 if piece.moved else 2

            # vertical moves
            start = row + piece.dir
            end = row + (piece.dir * (1 + steps))
            for possible_move_row in range(start, end, piece.dir):
                if Square.in_range(possible_move_row):
                    if self.squares[possible_move_row][col].isempty():
                        initial = Square(row, col)
                        final = Square(possible_move_row, col)
                        move = Move(initial, final)

                        # check if moves leads to self check
                        if bool:
                            if not self.in_check(piece, move):
                                piece.add_move(move)
                        else:
                            piece.add_move(move)
                        # blocked 
                    else:
                        break
                else:
                    break

            # diagonal moves
            possible_move_row = row + piece.dir
            possible_move_cols = [col-1, col+1]
            for possible_move_col in possible_move_cols:
                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].has_enemy_piece(piece.color):
                        # create initial and final move squares 
                        initial = Square(row, col)
                        final_piece = self.squares[possible_move_row][possible_move_col].piece
                        final = Square(possible_move_row, possible_move_col, final_piece)
                        # create a new move 
                        move = Move(initial, final)
                        # check if moves leads to self check
                        if bool:
                            if not self.in_check(piece, move):
                                # append new move 
                                piece.add_move(move)
                        else:
                            # append new move 
                            piece.add_move(move)


            # en passant moves
            r = 3 if piece.color == "white" else 4
            fr = 2 if piece.color == "white" else 5
            # left en passant 
            if Square.in_range(col - 1) and row == r:
                if self.squares[row][col-1].has_enemy_piece(piece.color):
                    p = self.squares[row][col-1].piece
                    if isinstance(p, Pawn):
                        if p.en_passant:
                            # create initial and final move squares 
                            initial = Square(row, col)
                            final = Square(fr, col-1, p)
                            # create a new move 
                            move = Move(initial, final)
                            # check if moves leads to self check
                            if bool:
                                if not self.in_check(piece, move):
                                    # append new move 
                                    piece.add_move(move)
                            else:
                                # append new move 
                                piece.add_move(move)

            # right en passant 
            if Square.in_range(col+1) and row == r:
                if self.squares[row][col+1].has_enemy_piece(piece.color):
                    p = self.squares[row][col+1].piece
                    if isinstance(p, Pawn):
                        if p.en_passant:
                            # create initial and final move squares 
                            initial = Square(row, col)
                            final = Square(fr, col+1, p)
                            # create a new move 
                            move = Move(initial, final)
                            # check if moves leads to self check
                            if bool:
                                if not self.in_check(piece, move):
                                    # append new move 
                                    piece.add_move(move)
                            else:
                                # append new move 
                                piece.add_move(move)


        def knight_moves():
            possible_moves = [
                (row-2, col+1),
                (row-1, col+2),
                (row+1, col+2),
                (row+2, col+1),
                (row+2, col-1),
                (row+1, col-2),
                (row-1, col-2),
                (row-2, col-1)
            ]

            for possible_move in possible_moves:
                possible_move_row, possible_move_col = possible_move

                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].isempty_or_enemy(piece.color):
                        # create squares of move 
                        initial = Square(row, col)
                        final_piece = self.squares[possible_move_row][possible_move_col].piece
                        final = Square(possible_move_row, possible_move_col, final_piece)
                        # create new move
                        move = Move(initial, final)
                        # check if moves leads to self check
                        if bool:
                            if not self.in_check(piece, move):
                                # append new move 
                                piece.add_move(move)
                            else: break
                        else:
                            # append new move 
                            piece.add_move(move)


        def straightline_moves(incrs):
            for incr in incrs:
                row_incr, col_incr = incr
                possible_move_row = row + row_incr
                possible_move_col = col + col_incr

                while True:
                    if Square.in_range(possible_move_row, possible_move_col):

                        initial = Square(row, col)
                        final_piece = self.squares[possible_move_row][possible_move_col].piece
                        final = Square(possible_move_row, possible_move_col, final_piece)
                        # create a possible new move 
                        move = Move(initial, final)


                        # empty
                        if self.squares[possible_move_row][possible_move_col].isempty():
                            # check if moves leads to self check
                            if bool:
                                if not self.in_check(piece, move):
                                    # append new move 
                                    piece.add_move(move)
                            else:
                                # append new move 
                                piece.add_move(move)


                        # has enemy piece
                        elif self.squares[possible_move_row][possible_move_col].has_enemy_piece(piece.color):
                            # check if moves leads to self check
                            if bool:
                                if not self.in_check(piece, move):
                                    # append new move 
                                    piece.add_move(move)
                            else:
                                # append new move 
                                piece.add_move(move)
                            break

                        # has team piece 
                        elif self.squares[possible_move_row][possible_move_col].has_team_piece(piece.color):         
                            break

                    else:
                        break

                    # incrementing incrs
                    possible_move_row = possible_move_row + row_incr
                    possible_move_col = possible_move_col + col_incr

        """TODO: Don't foget to add code for castling"""
        def king_moves():
            adjs = [
                (row-1, col+0), # up
                (row-1, col+1), # up-right
                (row+0, col+1), # right
                (row+1, col+1), # down-right
                (row+1, col+0), # down 
                (row+1, col-1), # down-left
                (row+0, col-1), # left
                (row-1, col-1) # up-left
            ]

            # normal moves
            for possible_move in adjs:
                possible_move_row, possible_move_col = possible_move

                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].isempty_or_enemy(piece.color):
                        # create squares of move 
                        initial = Square(row, col)
                        final = Square(possible_move_row, possible_move_col)
                        # create new move
                        move = Move(initial, final)
                        # check if moves leads to self check
                        if bool:
                            if not self.in_check(piece, move):
                                # append new move 
                                piece.add_move(move)
                            else: break
                        else:
                            # append new move 
                            piece.add_move(move)


            # castling moves (Queen castling and King side castling)
            if not piece.moved:
                # queen side castling
                left_rook = self.squares[row][0].piece
                if isinstance(left_rook, Rook):
                    if not left_rook.moved:
                        for c in range(1, 4):
                            if self.squares[row][c].has_piece(): # castling is not possible because there are pieces in between 
                                break

                            if c == 3:
                                # adds left rook to King 
                                piece.left_rook = left_rook

                                # rook move
                                initial = Square(row, 0)
                                final = Square(row, 3)
                                moveR = Move(initial, final)

                                # king move
                                initial = Square(row, col)
                                final = Square(row, 2)
                                moveK = Move(initial, final)
                                # check if moves leads to self check
                                if bool:
                                    if not self.in_check(piece, moveK) and not self.in_check(left_rook, moveR):
                                        # append new move to rook
                                        left_rook.add_move(moveR)
                                        # append new move to king
                                        piece.add_move(moveK)
                                else:
                                    # append new move to rook
                                    left_rook.add_move(moveR)
                                    # append new move the king
                                    piece.add_move(moveK)

                # King side castling
                right_rook = self.squares[row][7].piece
                if isinstance(right_rook, Rook):
                    if not right_rook.moved:
                        for c in range(5, 7):
                            if self.squares[row][c].has_piece(): # castling is not possible because there are pieces in between 
                                break

                            if c == 6:
                                # adds right rook to King 
                                piece.right_rook = right_rook

                                # rook move
                                initial = Square(row, 7)
                                final = Square(row, 5)
                                moveR = Move(initial, final)

                                # king move
                                initial = Square(row, col)
                                final = Square(row, 6)
                                moveK = Move(initial, final)

                                # check if moves leads to self check
                                if bool:
                                    if not self.in_check(piece, moveK) and not self.in_check(right_rook, moveR):
                                        # append new move to rook
                                        right_rook.add_move(moveR)
                                        # append new move to king
                                        piece.add_move(moveK)
                                else:
                                    # append new move to rook
                                    right_rook.add_move(moveR)
                                    # append new move the king
                                    piece.add_move(moveK)

        if isinstance(piece, Pawn): 
            pawn_moves() 

        elif isinstance(piece, Knight): 
            knight_moves() 

        elif isinstance(piece, Bishop): 
            straightline_moves([
                (-1, 1), # up-right
                (-1, -1), # up-left
                (1, 1), #down right
                (1, -1) # down left
            ])

        elif isinstance(piece, Rook): 
            straightline_moves([
                (-1, 0), # up
                (0, 1), # left
                (1, 0), # down
                (0, -1), # left
            ])

        elif isinstance(piece, Queen): 
            straightline_moves([
                (-1, 1), # up-right
                (-1, -1), # up-left
                (1, 1), #down right
                (1, -1), # down left
                (-1, 0), # up
                (0, 1), # left
                (1, 0), # down
                (0, -1), # left
            ])

        elif isinstance(piece, King): 
            king_moves()


    def _create(self):
        for row in range(ROWS):
            for col in range(COLS):
                self.squares[row][col] = Square(row, col)


    def _add_pieces(self, color):
        row_pawn, row_other = (6, 7) if color == "white" else (1, 0)

        # creating the pawns
        for col in range(COLS):
            self.squares[row_pawn][col] = Square(row_pawn, col, Pawn(color))

        # creating the knight
        self.squares[row_other][1] = Square(row_other, 1, Knight(color))
        self.squares[row_other][6] = Square(row_other, 6, Knight(color))

        # creating the bishop
        self.squares[row_other][2] = Square(row_other, 2, Bishop(color))
        self.squares[row_other][5] = Square(row_other, 5, Bishop(color))

        # creating the rooks
        self.squares[row_other][0] = Square(row_other, 0, Rook(color))
        self.squares[row_other][7] = Square(row_other, 7, Rook(color))

        # creating the queen
        self.squares[row_other][3] = Square(row_other, 3, Queen(color))

        # creating the king
        self.squares[row_other][4] = Square(row_other, 4, King(color))