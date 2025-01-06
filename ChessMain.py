# This file is reponsilble for receiving the user input and displaying the current game status.

import pygame as p
from ChessEngine import GameState

WIDTH = HEIGHT = 512 # size of the window
DIMENSION = 8 
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15 #for animations
IMAGES = {}

'''
Initialize a global disctionary of images, will be called once in the main
'''

def loadImages():
    pieces = {"bR","bB","bN","bQ","bK","bp","wR","wB","wN","wQ","wK","wp"}
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ_SIZE,SQ_SIZE))
    
'''
The main driver of our code. This will handle the user input and updating the graphics
'''

def main():
    p.init()
    screen = p.display.set_mode((WIDTH,HEIGHT), p.NOFRAME)
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = GameState()
    loadImages()
    running = True
    
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
        drawGameState(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()
        
'''
Responsible for all the graphics within a current game state.
'''        

def drawGameState(screen, gs):
    drawBoard(screen) # Draw the swaures on the board
    drawPieces(screen, gs.board) #draw the pieces on top of the squares
    
    
'''
Draw the squares on the board
'''
def drawBoard(screen):
    colors = [p.Color("white"), p.Color("gray")]
    for i in range(DIMENSION):
        for j in range(DIMENSION):
            color = colors[((i + j) % 2)]
            p.draw.rect(screen, color, p.Rect(i*SQ_SIZE, j*SQ_SIZE, SQ_SIZE, SQ_SIZE))    
            
    
'''
Draw the pieces on the board using the current GameState,board
'''    
def drawPieces(screen, board):
    for i in range(DIMENSION):
        for j in range(DIMENSION):
            piece = board[i][j]
            
            if piece != "--": # not empty
                screen.blit(IMAGES[piece], p.Rect(j*SQ_SIZE, i*SQ_SIZE, SQ_SIZE, SQ_SIZE))
    
if __name__ == "__main__":
    main()