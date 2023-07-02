import pygame
import sys

from const import *
from game import Game


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
            game.show_pieces(screen)


            for event in pygame.event.get():
                # click
               if event.type == pygame.MOUSEBUTTONDOWN:
                dragger.update_mouse(event.pos)

                clicked_row = dragger.mouseY // SQSIZE
                clicked_col = dragger.mouseX // SQSIZE

                # if clicked square has a piece
                if board.squares[clicked_row][clicked_col].has_piece():
                   piece = board.squares[clicked_row][clicked_col].piece
                   dragger.save_initial(event.pos)
               
               elif event.type == pygame.MOUSEMOTION:
                pass
               
               elif event.type == pygame.MOUSEBUTTONUP:
                pass
               
               elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()

main = Main()
main.mainloop()