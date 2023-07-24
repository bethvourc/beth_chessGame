"""Time stamp: 1:38:33"""
import pygame
import sys

from pygame.locals import *
from const import *
from game import Game
from square import Square
from move import Move

class StartMenu():
    def __init__(self):
        self.size = self.width, self.height = (1100, 1500)
        pygame.init()
        pygame.mixer.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption("BETH CHESS")

        self.button_font = pygame.font.Font("src/start_menu_assets/marta.regular.otf", 12)

        # Load the tutorial background image
        self.background_image = pygame.image.load("src/start_menu_assets/chess_menu.png").convert_alpha()
        self.background_image = pygame.transform.scale(self.background_image, self.size)

        # Create a play button to start game
        self.play_button = pygame.Rect(610, self.height - 810, 500, 300)
        self.play_button_image = pygame.image.load("src/start_menu_assets/play_button.png").convert_alpha()
        self.play_button_image = pygame.transform.scale(self.play_button_image, (400, 200))
        self.play_button_image_rect = self.play_button_image.get_rect(center=self.play_button.center)

        # hover bool
        self.play_button_hovered = False

        # Create a play button hover effect on mouse detection
        self.play_button_hover = pygame.Rect(610, self.height - 810, 500, 300)
        self.play_button_hover_image = pygame.image.load("src/start_menu_assets/play_button_hover.png").convert_alpha()
        self.play_button_hover_image = pygame.transform.scale(self.play_button_hover_image, (400, 200))
        self.play_button_hover_image_rect = self.play_button_hover_image.get_rect(center=self.play_button_hover.center)


    def run(self):
        running = True

        while running:
            self.clock.tick(60)

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    running = False

                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mouse_pos = event.pos

                        if self.play_button.collidepoint(mouse_pos):
                            running = False
                            pygame.quit()
                            main_menu = Main()
                            main_menu.mainloop()

                elif event.type == MOUSEMOTION:
                    mouse_pos = event.pos

                    if self.play_button.collidepoint(mouse_pos):
                        self.play_button_hovered = True
                    else:
                        self.play_button_hovered = False



            # Blit the background image onto the screen
            self.screen.blit(self.background_image, (0, 0))

            # Handles the hover state
            if self.play_button_hovered:
                self.screen.blit(self.play_button_hover_image, self.play_button_image_rect)
            else:
                self.screen.blit(self.play_button_image, self.play_button_image_rect)


            pygame.display.update()    


class Main:

    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH,HEIGHT))
        pygame.display.set_caption("Beth CHESS")
        self.game = Game()

    def mainloop(self):
        
        game = self.game
        screen = self.screen
        dragger = self.game.dragger
        board = self.game.board

        while True:
            game.show_bg(screen)
            game.show_last_move(screen)
            game.show_moves(screen)
            game.show_pieces(screen)

            game.show_hover(screen)

            if dragger.dragging:
               dragger.update_blit(screen)


            for event in pygame.event.get():
                # click
               if event.type == pygame.MOUSEBUTTONDOWN:
                dragger.update_mouse(event.pos)

                clicked_row = dragger.mouseY // SQSIZE
                clicked_col = dragger.mouseX // SQSIZE

                # if clicked square has a piece
                if board.squares[clicked_row][clicked_col].has_piece():
                   piece = board.squares[clicked_row][clicked_col].piece
                   # check valid piece (color)
                   if piece.color == game.next_player:
                        board.calc_moves(piece, clicked_row, clicked_col, bool=True)
                        dragger.save_initial(event.pos)
                        dragger.drag_piece(piece)
                        # show methods
                        game.show_bg(screen)
                        game.show_moves(screen)
                        game.show_pieces(screen)
               
               elif event.type == pygame.MOUSEMOTION:
                    motion_row = event.pos[1] // SQSIZE
                    motion_col = event.pos[0] // SQSIZE

                    game.set_hover(motion_row, motion_col)

                    # check if piece is actually being dragged
                    if dragger.dragging:
                        dragger.update_mouse(event.pos)
                        # show methods
                        game.show_bg(screen)
                        game.show_last_move(screen)
                        game.show_moves(screen)
                        game.show_pieces(screen)
                        game.show_hover(screen)
                        dragger.update_blit(screen)
               
               elif event.type == pygame.MOUSEBUTTONUP:
                    

                    if dragger.dragging:
                       dragger.update_mouse(event.pos)

                       released_row = dragger.mouseY // SQSIZE
                       released_col = dragger.mouseX // SQSIZE

                       # create possible move
                       initial = Square(dragger.initial_row, dragger.initial_col)
                       final = Square(released_row, released_col)
                       move = Move(initial, final)

                        # valid move?
                       if board.valid_move(dragger.piece, move):
                          # normal caputure
                          captured = board.squares[released_row][released_col].has_piece()
                          board.move(dragger.piece, move)

                          board.set_true_en_passant(dragger.piece)
                          # sound
                          game.play_sound(captured)
                          # draw
                          game.show_bg(screen)
                          game.show_last_move(screen)
                          game.show_pieces(screen)
                          # next turn 
                          game.next_turn()

                    dragger.undrag_piece()

                # Key press
               elif event.type ==pygame.KEYDOWN:
                   

                   # changing theme
                   if event.key == pygame.K_t:
                       game.change_theme()

                   # changing theme
                   if event.key == pygame.K_r:
                       game.reset()
                       game = self.game
                       board = self.game.board
                       dragger = self.game.dragger
               
               elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()

start = StartMenu()
start.run()