# This class is responsible for storing all the information of a chess game + responsible for determining
# the valid moves 

class GameState():
    def __init__(self):
        #board is x8x 2d list, each element of the list has 2 characters
        #The first character represents the color of piece (w or b),
        #the 2 nd one represents the type of the piece ('R' for rook, 'N' for Knight, 'B' for Bishop,
        # 'Q' for Queen, 'K' for King, and 'p' for Pawn)
        # "--" represents an empty space, with no pice.
        self.board = [
            ["bR","bN","bB","bQ","bK","bB","bN","bR"],
            ["bp","bp","bp","bp","bp","bp","bp","bp"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["wp","wp","wp","wp","wp","wp","wp","wp"],
            ["wR","wN","wB","wQ","wK","wB","wN","wR"]
        ]
        self.whiteToMove = True
        self.moveLog = []