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
        self.moveFunctions = {'p':self.getPawnMoves, 'R':self.getRookMoves, 'N':self.getKnightMoves, 
                              'B':self.getBishopMoves, 'Q':self.getQueenMoves, 'K':self.getKingMoves}
        self.whiteToMove = True
        self.moveLog = []
        self.whiteKingLocation = (7,4)
        self.blackKingLocation = (0,4)
        self.checkMate = False
        self.staleMate = False
    '''
    Takes a  move as a paramter and executes it
    '''
    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move) #log the move
        self.whiteToMove = not self.whiteToMove
        if move.pieceMoved == 'wK':
            self.whiteKingLocation = (move.endRow, move.endCol)
        elif move.pieceMoved == 'bK':
            self.blackKingLocation = (move.endRow, move.endCol)
        
        
        
    '''
    Undo the last move
    '''
    def undoMove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove
            if move.pieceMoved == 'wK':
                self.whiteKingLocation = (move.startRow, move.startCol)
            elif move.pieceMoved == 'bK':
                self.blackKingLocation = (move.startRow, move.startCol)
        
    '''
    All moves considering checks
    '''
    def getValidMoves(self):
       moves = self.getAllPossibleMoves()
       
       for i in range(len(moves) - 1, -1, -1):
           self.makeMove(moves[i])
           self.whiteToMove = not self.whiteToMove
           if self.inCheck():
              moves.remove(moves[i]) 
           self.whiteToMove = not self.whiteToMove
           self.undoMove()      
       
       if len(moves) == 0: #either checkmate or stalemate
           if self.inCheck():
               self.checkMate = True
           else:
               self.staleMate = True
       else:
             self.checkMate = False
             self.staleMate = False
               
               
       return moves
    
    
    '''
    Determine if the current player is in checl
    '''
    def inCheck(self):
        if self.whiteToMove:
            return self.squareUnderAttack(self.whiteKingLocation[0], self.whiteKingLocation[1])
        else:
            return self.squareUnderAttack(self.blackKingLocation[0], self.blackKingLocation[1])

        
        
    '''
    Determine if the enemy can attack the square r,c 
    '''
    def squareUnderAttack(self, r, c):
           self.whiteToMove = not self.whiteToMove
           oppMoves = self.getAllPossibleMoves()
           self.whiteToMove = not self.whiteToMove
           for move in oppMoves:
              if move.endRow == r and move.endCol == c:
                  return True
           return False
              
              
              
    '''
    All moves without considering checks
    '''
    def getAllPossibleMoves(self):
         moves = []
         for r in range(len(self.board)):
             for c in range(len(self.board[r])):
                 turn = self.board[r][c][0]
                 if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                     piece = self.board[r][c][1]
                     self.moveFunctions[piece](r,c, moves)
         return moves
                     
   
    '''
    Get all the pawn moves for the pawn located at row, col
    '''
    def getPawnMoves(self,r,c,moves):
        if self.whiteToMove: # white pawn moves
            if self.board[r-1][c] == "--":
                moves.append(Move((r,c),(r-1,c),self.board))
                if r == 6 and self.board[r-2][c] == "--":
                    moves.append(Move((r,c),(r-2,c),self.board))
            if c-1 >= 0:
                if self.board[r-1][c-1][0] == 'b': #capture left
                     moves.append(Move((r,c),(r-1,c-1),self.board))
            if c+1 <= 7:
                if self.board[r-1][c+1][0] == 'b': #capture right   
                     moves.append(Move((r,c),(r-1,c+1),self.board))
        else:
            if self.board[r+1][c] == "--": # black pawn moves
                moves.append(Move((r,c),(r+1,c),self.board))
                if r == 1 and self.board[r+2][c] == "--":
                    moves.append(Move((r,c),(r+2,c),self.board))
            if c-1 >= 0:
                if self.board[r+1][c-1][0] == 'w': #capture left
                     moves.append(Move((r,c),(r+1,c-1),self.board))
            if c+1 <= 7:
                if self.board[r+1][c+1][0] == 'w': #capture right   
                     moves.append(Move((r,c),(r+1,c+1),self.board))
                

    '''
    Get all the rook moves for the pawn located at row, col
    '''
    def getRookMoves(self, r, c, moves):
        directions = ((-1, 0), (1, 0), (0, -1), (0, 1))
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:  # on board
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--":  # empty space valid
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor:  # enemy piece valid
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else:  # friendly piece invalid
                        break
                else:  # off board
                    break

    
    
    '''
    Get all the bishop moves for the pawn located at row, col
    '''
    def getBishopMoves(self, r, c, moves):
        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1))  # 4 diagonals
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:  # on board
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--":  # empty space valid
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor:  # enemy piece valid
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else:  # friendly piece invalid
                        break
                else:  # off board
                    break

    
    
    '''
    Get all the knight moves for the pawn located at row, col
    '''
    def getKnightMoves(self, r, c, moves):
        knightMoves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        allyColor = "w" if self.whiteToMove else "b"
        for m in knightMoves:
            endRow = r + m[0]
            endCol = c + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:  # on board
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor:  # not an ally piece (empty or enemy piece)
                    moves.append(Move((r, c), (endRow, endCol), self.board))

    
    '''
    Get all the queen moves for the pawn located at row, col
    '''
    def getQueenMoves(self,r,c,moves):
        self.getRookMoves(r,c,moves)
        self.getBishopMoves(r,c,moves)
    
    
    '''
    Get all the king moves for the pawn located at row, col
    '''
    def getKingMoves(self, r, c, moves):
        kingMoves = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
        allyColor = "w" if self.whiteToMove else "b"
        for i in range(8):
            endRow = r + kingMoves[i][0]
            endCol = c + kingMoves[i][1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:  # on board
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor:  # not an ally piece (empty or enemy piece)
                    moves.append(Move((r, c), (endRow, endCol), self.board))

        
                        
 

class Move():
    
    ranksToRows = {"1":7, "2":6,"3":5, "4":4, "5":3, "6":2, "7":1, "8":0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a":0,"b":1,"c":2,"d":3,"e":4,"f":5,"g":6,"h":7}
    colsToFiles = {v: k for k, v in  filesToCols.items()}
    
    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.moveId = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol
        print(self.moveId)
         
         
         
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveId == other.moveId
        return False
         
    def getChessNotation(self):
        return self.getRankedFile(self.startRow, self.startCol) +  self.getRankedFile(self.endRow, self.endCol) 
        
    def getRankedFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r] #Ba4
    
    

        
    
