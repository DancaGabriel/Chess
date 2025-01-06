# This file is reponsilble for receiving the user input and displaying the current game status.

import pygame as p
from ChessEngine import GameState
from ChessEngine import Move

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
    validMoves = gs.getValidMoves()
    moveMade = False # flag variable when a move is made
    loadImages()
    running = True
    sqSelected =() # no square is selected initially, keep track of the last click of the user(row, column)
    playerClicks = [] #keep track of player clicks
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos() #(x,y) position of the mouse
                col = location[0] // SQ_SIZE
                row = location[1] // SQ_SIZE
                if sqSelected == (row,col):  # the user clicked the same sqaure twice ( undo move )
                    sqSelected = () # deselect
                    playerClicks = []
                else:
                   sqSelected = (row, col)
                   playerClicks.append(sqSelected) # append for 1st and 2nd clicks
                if len(playerClicks) == 2: # append after the 2nd click
                    move = Move(playerClicks[0],playerClicks[1],gs.board)
                    print(move.getChessNotation())
                    if move in validMoves:
                        gs.makeMove(move)
                        moveMade = True
                    sqSelected = ()
                    playerClicks = []
            #key_handler
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    gs.undoMove()
                    moveMade = True
        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False          
                    
                
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