import pygame
import time
import math
import random
import copy
import os

# initializing pygame and setting game windows
pygame.init()
screen = pygame.display.set_mode([700, 521])
pygame.display.set_caption("Chess Game")
pygame.display.set_icon( pygame.image.load('./images/icon.png') )
font2 = pygame.font.SysFont(None, 24)
sslide = pygame.mixer.Sound('./sounds/slide_sound.mp3')

# Piece class, represents a chess piece
class Piece():
    def __init__(self, x, y, name, color, type_):
        self.x = x
        self.y = y
        self.name = name
        self.color = color
        self.type_ = type_
        self.first = True
        self.enp = 0

    def __str__(self):
        return self.name

# Chess board with pieces
chessBoard = [
    [None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None],
]

# Chess Black Pieces
blackPieces = [
    Piece(0, 0, "BR", "Black", "Rook"),
    Piece(0, 7, "BR", "Black", "Rook"),
    Piece(0, 1, "BKn", "Black", "Knight"),
    Piece(0, 6, "BKn", "Black", "Knight"),
    Piece(0, 2, "BB", "Black", "Bishop"),
    Piece(0, 5, "BB", "Black", "Bishop"),
    Piece(0, 4, "BK", "Black", "King"),
    Piece(0, 3, "BQ", "Black", "Queen"),
    Piece(1, 0, "BP", "Black", "Pawn"),
    Piece(1, 1, "BP", "Black", "Pawn"),
    Piece(1, 2, "BP", "Black", "Pawn"),
    Piece(1, 3, "BP", "Black", "Pawn"),
    Piece(1, 4, "BP", "Black", "Pawn"),
    Piece(1, 5, "BP", "Black", "Pawn"),
    Piece(1, 6, "BP", "Black", "Pawn"),
    Piece(1, 7, "BP", "Black", "Pawn"),
]

# Chess White Pieces
whitePieces = [
    Piece(7, 0, "WR", "White", "Rook"),
    Piece(7, 7, "WR", "White", "Rook"),
    Piece(7, 1, "WKn", "White", "Knight"),
    Piece(7, 6, "WKn", "White", "Knight"),
    Piece(7, 2, "WB", "White", "Bishop"),
    Piece(7, 5, "WB", "White", "Bishop"),
    Piece(7, 4, "WK", "White", "King"),
    Piece(7, 3, "WQ", "White", "Queen"),
    Piece(6, 0, "WP", "White", "Pawn"),
    Piece(6, 1, "WP", "White", "Pawn"),
    Piece(6, 2, "WP", "White", "Pawn"),
    Piece(6, 3, "WP", "White", "Pawn"),
    Piece(6, 4, "WP", "White", "Pawn"),
    Piece(6, 5, "WP", "White", "Pawn"),
    Piece(6, 6, "WP", "White", "Pawn"),
    Piece(6, 7, "WP", "White", "Pawn"),
]

# Add chess pieces to board
for piece in blackPieces:
    chessBoard[piece.x][piece.y] = piece
for piece in whitePieces:
    chessBoard[piece.x][piece.y] = piece

# Display chess board of console
def showBoard(board):
    for x in range(0, 8):
        print( f"{8-x:<4}", end="")
        for y in range(0, 8):
            # for empty block display *
            if board[x][y] == None:
                print( f"{'*':<3}", end=" ")
            # for blocks containing pieces, display its nickname
            else:
                print( f"{board[x][y].name:<3}", end=" ")
        print("")
    print("\n    ", end="")
    for x in range(0, 8):
        print(f"{chr(97+x):<3}", end=" ")
    print("")

# Show all the moves that the player can make
def showMoves( moves ):
    i = 0
    e = ""
    for move in moves:
        if i%2 == 0:
            e = "           "
        else:
            e = "\n"
        # format: old position - new position
        print( f"Piece: {chessBoard[ move[1] ][ move[2] ].type_} - "+ (str(chr(97+move[2]))+""+str(8-move[1]) )+" - " +(str(chr(97+move[4]))+""+str(8-move[3]) ) + f" { move[0] }", end=e)
        i += 1
    print("")

# Returns all the moves that pawn can make
def getPawnMoves(piece, board):
    possibleMoves = []
    dirs_ = []
    if piece.color == "Black":
        tmpx = piece.x
        tmpy = piece.y
        # two steps forward
        if piece.first == True:
            if (0 <= tmpx+1 <= 7) and (0 <= tmpx+2 <= 7) and (0 <= tmpy <= 7):
                if board[tmpx+1][tmpy] == None and board[tmpx+2][tmpy] == None:
                    possibleMoves.append( (0, piece.x, piece.y, tmpx+2, tmpy) )
        # one step forward
        if (0 <= tmpx+1 <= 7) and (0 <= tmpy <= 7):
            if board[tmpx+1][tmpy] == None:
                possibleMoves.append( (0, piece.x, piece.y, tmpx+1, tmpy) )
        # diagonal positions
        dirs_ = [ (1, -1), (1, 1), ]

    else:
        tmpx = piece.x
        tmpy = piece.y
        # two steps forward
        if piece.first == True:
            if (0 <= tmpx-1 <= 7) and (0 <= tmpx-2 <= 7) and (0 <= tmpy <= 7):
                if board[tmpx-1][tmpy] == None and board[tmpx-2][tmpy] == None:
                    possibleMoves.append( (0, piece.x, piece.y, tmpx-2, tmpy) )
        # one step forward
        if (0 <= tmpx-1 <= 7) and (0 <= tmpy <= 7):
            if board[tmpx-1][tmpy] == None:
                possibleMoves.append( (0, piece.x, piece.y, tmpx-1, tmpy) )
        # diagonal positions
        dirs_ = [(-1, -1), (-1, 1), ]

    # check if pawn can capture any piece diagonally
    for p in dirs_:
        tmpx = piece.x+p[0]
        tmpy = piece.y+p[1]
        if ( (0 <= tmpx <= 7) and (0 <= tmpy <= 7) ):
            if board[ tmpx ][ tmpy ] == None:
                    # check if the piece is able to make en passant move
                    if piece.color == "Black":
                        if ( (0 <= tmpx+1 <= 7) and (0 <= tmpy <= 7) ):
                            if board[tmpx+1][tmpy] != None:
                                if board[tmpx+1][tmpy].type_ == "Pawn" and board[tmpx+1][tmpy].color =="White" and board[tmpx+1][tmpy].enp == 1:
                                    possibleMoves.append( (2, piece.x, piece.y, tmpx, tmpy) )
                    else:   
                        if ( (0 <= tmpx-1 <= 7) and (0 <= tmpy <= 7) ):
                            if board[tmpx-1][tmpy] != None:
                                if board[tmpx-1][tmpy].type_ == "Pawn" and board[tmpx-1][tmpy].color == "Black" and board[tmpx-1][tmpy].enp == 1:
                                    possibleMoves.append( (2, piece.x, piece.y, tmpx, tmpy) )
            # pawn can capture a chess piece diagonally
            else:
                if board[ tmpx ][ tmpy ].color != piece.color:  
                    possibleMoves.append( (1, piece.x, piece.y, tmpx, tmpy) )
    return possibleMoves

# Return all the moves that queen can make
def getQueenMoves(piece, board):
    opp_color = "White"
    if piece.color == "White":
        opp_color = "Black"
    possibleMoves = []
    # list of directions queens can normally go
    dirs_ = [ (-1, 0), # up direction
        (1, 0), # down direction
        (0, 1), # right direction
        (0, -1), # left direction
        (-1, -1), # top left direction
        (-1, 1), # top right direction
        (1, -1), # bottom left direction
        (1, 1), ] # bottom right direction  
    for p in dirs_:
        tmpx = piece.x
        tmpy = piece.y
        # continue moving in direction if the queen's position is in range
        while( (0 <= (tmpx+p[0]) <= 7) and (0 <= (tmpy+p[1]) <= 7) ):
            tmpx = tmpx+p[0]
            tmpy = tmpy+p[1]
            # if there is no piece on block, queen can move there
            if board[ tmpx ][ tmpy ] == None:
                possibleMoves.append( (0, piece.x, piece.y, tmpx, tmpy) )
            # if there is a piece on block, queen can either capture it or stop one block before it
            else:
                if board[ tmpx ][ tmpy ].color == opp_color:
                    possibleMoves.append( (1, piece.x, piece.y, tmpx, tmpy) )
                break
    return possibleMoves

# Returns all the moves that the rook can make
def getRookMoves(piece, board):
    opp_color = "White"
    if piece.color == "White":
        opp_color = "Black"
    # list of all the directions rook can go
    possibleMoves = []
    dirs_ = [ (-1, 0), # up direction
        (1, 0), # down direction
        (0, 1), # right direction
        (0, -1),] # left direction
    for p in dirs_:
        tmpx = piece.x
        tmpy = piece.y
        # continue moving in direction if the position of piece is in range
        while( (0 <= (tmpx+p[0]) <= 7) and (0 <= (tmpy+p[1]) <= 7) ):
            tmpx = tmpx+p[0]
            tmpy = tmpy+p[1]
            # if there is no piece on block, rook can move there
            if board[ tmpx ][ tmpy ] == None:
                possibleMoves.append( (0, piece.x, piece.y, tmpx, tmpy) )
            # if there is a piece on block, rook can either capture it or stop one block before that piece
            else:
                if board[ tmpx ][ tmpy ].color == opp_color:
                    possibleMoves.append( (1, piece.x, piece.y, tmpx, tmpy) )
                break
    return possibleMoves

# Returns all the moves that bishop can make
def getBishopMoves(piece, board):
    opp_color = "White"
    if piece.color == "White":
        opp_color = "Black"
    possibleMoves = []
    # list of directions where a bishop can move
    dirs_ = [ (-1, -1), # top left direction
        (-1, 1), # top right direction
        (1, -1), # bottom left direction
        (1, 1), ] # bottom right direction  
    for p in dirs_:
        tmpx = piece.x
        tmpy = piece.y
        # continue moving in direction if the position of piece is in range
        while( (0 <= (tmpx+p[0]) <= 7) and (0 <= (tmpy+p[1]) <= 7) ):
            tmpx = tmpx+p[0]
            tmpy = tmpy+p[1]
            # if there is no piece on block, bishop can move there
            if board[ tmpx ][ tmpy ] == None:
                possibleMoves.append( (0, piece.x, piece.y, tmpx, tmpy) )
            # if there is a piece on block, bishop can either capture it or stop one block before that piece
            else:
                if board[ tmpx ][ tmpy ].color == opp_color:
                    possibleMoves.append( (1, piece.x, piece.y, tmpx, tmpy) )
                break
    return possibleMoves

# Returns all the moves that a knight can make
def getKnightMoves(piece, board):
    opp_color = "White"
    if piece.color == "White":
        opp_color = "Black"
    possibleMoves = []
    # list of all the possible blocks where knight can move
    dirs_ = [ (-2, -1), (-1, -2), (-2, 1), (-1, 2), (1, -2), (2, -1), (1, 2), (2, 1), ]
    for p in dirs_:
        tmpx = piece.x+p[0]
        tmpy = piece.y+p[1]
        if (0 <= tmpx <= 7) and (0 <= tmpy <= 7):
            # if there is no piece on block, knight can move there
            if board[ tmpx ][ tmpy ] == None:
                possibleMoves.append( (0, piece.x, piece.y, tmpx, tmpy) )
            # if there is a piece on block, knight can either capture it or stop one block before that piece
            else:
                if board[ tmpx ][ tmpy ].color == opp_color:
                    possibleMoves.append( (1, piece.x, piece.y, tmpx, tmpy) )
    return possibleMoves
    possibleMoves = []

# Returns all the moves that a king can make
def getKingMoves(piece, board):
    possibleMoves = []
    # list of all the positions where a king can go
    dirs_ = [ (-1, 0), (1, 0), (0, 1), (0, -1), (-1, -1), (-1, 1), (1, -1), (1, 1), ]
    for p in dirs_:
        tmpx = piece.x+p[0]
        tmpy = piece.y+p[1]
        if ( (0 <= tmpx <= 7) and (0 <= tmpy <= 7) ):
            if board[ tmpx ][ tmpy ] == None:
                # check if this position leads to a check
                possibleMoves.append( (0, piece.x, piece.y, tmpx, tmpy) )
            else:
                if board[ tmpx ][ tmpy ].color != piece.color:
                    # king can capture this piece    
                    possibleMoves.append( (1, piece.x, piece.y, tmpx, tmpy) )
    return possibleMoves

# Return the castling move, if king can make it
def castling_move(king, board):
    possibleMoves = []
    # check if king's first move has not been made yet 
    if king.first == True:
        if king.color == "Black":
            # check if left side rook has not made its first move
            if board[0][0] != None:
                if board[0][0].type_ == "Rook" and board[0][0].first == True:
                    empty_blocks = True
                    for i in [1, 2, 3]:
                        if board[0][i] != None:
                            empty_blocks = False
                    if empty_blocks == True:
                        possibleMoves.append( (3, king.x, king.y, 0, 0) )
            # check if right side rook has not made its first move
            if board[0][7] != None:
                if board[0][7].type_ == "Rook" and board[0][7].first == True:
                    empty_blocks = True
                    for i in [5, 6]:
                        if board[0][i] != None:
                            empty_blocks = False
                    if empty_blocks == True:
                        possibleMoves.append( (3, king.x, king.y, 0, 7) )
        else:
            # check if left side rook has not made its first move
            if board[7][0] != None:
                if board[7][0].type_ == "Rook" and board[7][0].first == True:
                    empty_blocks = True
                    for i in [1, 2, 3]:
                        if board[7][i] != None:
                            empty_blocks = False
                    if empty_blocks == True:
                        possibleMoves.append( (3, king.x, king.y, 7, 0) )
            # check if left side rook has not made its first move
            if board[7][7] != None:
                if board[7][7].type_ == "Rook" and board[7][7].first == True:
                    empty_blocks = True
                    for i in [5, 6]:
                        if board[0][i] != None:
                            empty_blocks = False
                    if empty_blocks == True:
                        possibleMoves.append( (3, king.x, king.y, 7, 7) )
    return possibleMoves

# Returns all the moves for player even those which attack/capture king
def getAllMoves(color_, board, opt):
    possibleMoves = []
    for i in range(0, 8):
        for j in range(0, 8):
            if board[i][j] != None:
                if board[i][j].color == color_:
                    # depanding on piece type, get its moves
                    if board[i][j].type_ == "Queen":
                        possibleMoves.extend( getQueenMoves(board[i][j], board) )
                    elif board[i][j].type_ == "Rook":
                        possibleMoves.extend( getRookMoves(board[i][j], board) )
                    elif board[i][j].type_ == "Bishop": 
                        possibleMoves.extend( getBishopMoves(board[i][j], board) )
                    elif board[i][j].type_ == "Knight":
                        possibleMoves.extend( getKnightMoves(board[i][j], board) )
                    elif board[i][j].type_ == "Pawn": 
                        possibleMoves.extend( getPawnMoves(board[i][j], board) )
                    # if king moves are asked to add
                    elif board[i][j].type_ == "King": 
                        if opt == 1:
                            possibleMoves.extend( getKingMoves(board[i][j], board) )
    return possibleMoves

# Returns all moves for player but filtering those which were capturing king
def getAllMoves2(color_, board, opt):
    possibleMoves = getAllMoves(color_, board, opt)
    # find the king piece on board
    king = None
    for i in range(0, 8):
        for j in range(0, 8):
            if board[i][j] != None:
                if board[i][j].type_ == "King" and board[i][j].color == color_:
                    king = board[i][j]
                    break
    # if king moves are to be added, add castling move as well
    if opt == 1:
        possibleMoves.extend( castling_move(king, board) )

    # remove moves that land directly on King's position and also remove those which put king in check
    moves2 = []
    for move in possibleMoves:
        # if new position for move is empty
        if board[ move[3] ][ move[4] ] == None:
            tmpBoard = copy.deepcopy( board )
            movePiece( tmpBoard, move[0], move[1], move[2], move[3], move[4] )
            #  if the move does not put king into check, add the move
            if isChecked( king, tmpBoard ) == False:
                moves2.append( move )
        # if there is a piece on new position
        else:
            #  if the piece is not king and the move does not put king into check, add the move
            if board[ move[3] ][ move[4] ].type_ != "King":
                tmpBoard = copy.deepcopy( board )
                movePiece( tmpBoard, move[0], move[1], move[2], move[3], move[4] )
                if isChecked( king, tmpBoard ) == False:
                    moves2.append( move )
    possibleMoves = moves2
    return possibleMoves

# Return if the king is in check or not
def isChecked(king, board):
    # get all the moves that the pieces of other player can make
    if king.color == "White":
        # get all black pieces's moves
        moves = getAllMoves("Black", board, 1)
    else:
        # get all white pieces moves
        moves = getAllMoves("White", board, 1)
    # check if there is move that attacks king
    attacking = 0
    for move in moves:
        if move[3] == king.x and move[4] == king.y:
            attacking += 1
    return attacking > 0

# Move piece to new position on board
def movePiece(board, moveType, oldX, oldY, newX, newY):
    # if it is normal move or capture move
    if moveType == 0 or moveType == 1:
        # update board pieces, piece's internal info like x, y coordinates
        board[newX][newY] = board[oldX][oldY]
        board[newX][newY].x = newX
        board[newX][newY].y = newY
        board[newX][newY].first = False
        if board[newX][newY].type_ == "Pawn":
            # If first move of pawn was 2 steps, set enp to 1 for en passant
            if abs(oldX-newX) == 2:
                board[newX][newY].enp = 1
            # if pawn reached the end of board promote pawn to queen
            if newX == 0 or newX == 7:
                if board[newX][newY].color == "White" and newX == 0:
                    board[newX][newY].name = "WQ"
                    board[newX][newY].type_ = "Queen"
                elif board[newX][newY].color == "Black" and newX == 7:
                    board[newX][newY].name = "BQ"
                    board[newX][newY].type_ = "Queen"
        board[oldX][oldY] = None
    elif moveType == 2:
        # if move was En Passant
        board[newX][newY] = board[oldX][oldY]
        board[newX][newY].x = newX
        board[newX][newY].y = newY
        board[oldX][oldY] = None
        if board[newX][newY].color == "White":
            board[newX-1][newY] = None
        else:
            board[newX+1][newY] = None
    elif moveType == 3:
        # if it was Castling move
        if oldY > newY:
            # if castling was between king and left corner rook
            board[oldX][oldY-2] = board[oldX][oldY]
            board[oldX][oldY-2].y = oldY-2
            board[oldX][oldY-2].first = False
            board[oldX][oldY] = None

            board[oldX][oldY-1] = board[newX][newY]
            board[oldX][oldY-1].y = oldY-1
            board[oldX][oldY-1].first = False
            board[newX][newY] = None
        else:
            # if castling was between king and right corner rook
            board[oldX][oldY+2] = board[oldX][oldY]
            board[oldX][oldY+2].y = oldY+2
            board[oldX][oldY+2].first = False
            board[oldX][oldY] = None

            board[oldX][oldY+1] = board[newX][newY]
            board[oldX][oldY+1].y = oldY-1
            board[oldX][oldY+1].first = False
            board[newX][newY] = None

# Return all the moves of player
def getMoves(color_, board):
    # find the king piece on board
    king = ""
    for i in range(0, 8):
        for j in range(0, 8):
            if board[i][j] != None:
                if board[i][j].type_ == "King" and board[i][j].color == color_:
                    king = board[i][j]
                    break

    state = 0
    moves = []
    # check if the king is in check or not
    if king != "":
        if isChecked( king, board):
            # king is in check
            state = 1
            moves = getKingMoves( king, board )
            king_moves = []
            # get all the moves of king that get the king out of check
            for move in moves:
                if board[move[3]][move[4]] != None:
                    if board[move[3]][move[4]].type_ == "King":
                        continue
                tmpBoard = copy.deepcopy( board )
                movePiece( tmpBoard, move[0], move[1], move[2], move[3], move[4] )
                if isChecked( tmpBoard[ move[3] ][ move[4] ], tmpBoard ) == False:
                    king_moves.append( move )
            # if there is no legal move of king available
            if len( king_moves ) == 0:
                # get all the moves of other pieces that get king out of check
                moves = getAllMoves2(color_, board, 0)
                # if there are no moves that can be made then the king is checkmatted
                if len(moves) == 0:
                    state = 2
            else:
                # return the moves of king that will get him out of check
                moves = king_moves
        else:
            # if king is not in  check
            moves = getAllMoves2(color_, board, 1)
            # if there are no moves that king can made then it is stalemate
            if len(moves) == 0:
                state = 3
    return (state, moves)

# Evaluation function
def fitness(turn, board):
    whitePoints = 0
    blackPoints = 0
    for i in range(0, 8):
        for j in range(0, 8):
            if board[i][j] != None:
                # count the points each piece of player that is available on board
                if board[i][j].type_ == "Queen":
                    if board[i][j].color == "White":
                        whitePoints += 90
                    else:
                        blackPoints += 90
                elif board[i][j].type_ == "Rook":
                    if board[i][j].color == "White":
                        whitePoints += 50
                    else:
                        blackPoints += 50
                elif board[i][j].type_ == "Bishop":
                    if board[i][j].color == "White":
                        whitePoints += 30
                    else:
                        blackPoints += 30
                    
                elif board[i][j].type_ == "Knight":
                    if board[i][j].color == "White":
                        whitePoints += 30
                    else:
                        blackPoints += 30
                
                elif board[i][j].type_ == "Pawn":
                    if board[i][j].color == "White":
                        whitePoints += 10
                    else:
                        blackPoints += 10
                    
                elif board[i][j].type_ == "King":
                    if board[i][j].color == "White":
                        whitePoints += 900
                    else:
                        blackPoints += 900
    # fitness of board is black points minus white points
    return blackPoints - whitePoints

# Minimax algorithm
def minimax(turn, board):
    # if its black's turn, choose a move that maximizes the fitness
    if turn == "Black":
        ft, move_ = max_value("Black", board, 0, 2)
    # if its white's turn, choose a move that minimizes the fitness
    else:
        ft, move_ = min_value("White", board, 0, 2)
    return (ft, move_)

def max_value(turn, board, depth, max_depth):
    # if max depth reached return fitness of current state of board
    if depth == max_depth:
        return ( fitness(turn, board), 0)
    else:
        # get all the moves of player
        state_, moves_ = getMoves(turn, board)
        # if its checkmated, stalemate or there are no moves
        if state_ == 2 or state_ == 3 or len(moves_) == 0:
            return (-1000, 0)
        else:
            # copy board, make move, find its fitness, add fitness to list
            tmpB = copy.deepcopy( board )
            movePiece( tmpB, moves_[0][0], moves_[0][1], moves_[0][2], moves_[0][3], moves_[0][4] )
            max_ft = fitness(turn, tmpB)
            m_ = moves_[0]
            ft_arr = []
            for m in moves_:
                tmpBoard = copy.deepcopy( board )
                movePiece(tmpBoard, m[0], m[1], m[2], m[3], m[4])
                f, mv = min_value("White", tmpBoard, depth+1, max_depth)
                if f > max_ft:
                    max_ft = f
                    m_ = mv
                ft_arr.append(f)
            # return max fitness move
            same_moves = [ moves_[i] for i in range(0, len(moves_)) if ft_arr[i] == f ]
            m_ = random.choice(same_moves)
            return (max_ft, m_)

def min_value(turn, board, depth, max_depth):
    # if max depth reached return fitness of current state of board
    if depth == max_depth:
        return ( fitness(turn, board), 0)
    else:
        # get all the moves of player
        state_, moves_ = getMoves(turn, board)
        # if its checkmated, stalemate or there are no moves
        if state_ == 2 or state_ == 3 or len(moves_) == 0:
            return (-1000, 0)
        else:
            # copy board, make move, find its fitness, add fitness to list
            tmpB = copy.deepcopy( board )
            movePiece( tmpB, moves_[0][0], moves_[0][1], moves_[0][2], moves_[0][3], moves_[0][4] )
            min_ft = fitness(turn, tmpB)
            m_ = moves_[0]
            ft_arr = []
            for m in moves_:
                tmpBoard = copy.deepcopy( board )
                movePiece(tmpBoard, m[0], m[1], m[2], m[3], m[4])
                f, mv = max_value("Black", tmpBoard, depth+1, max_depth)
                if f < min_ft:
                    min_ft = f
                    m_ = mv
                ft_arr.append(f)
            # return min fitness move
            same_moves = [ moves_[i] for i in range(0, len(moves_)) if ft_arr[i] == f ]
            m_ = random.choice(same_moves)
            return (min_ft, m_)

state1 = 0 # current overall status of game for white player
state2 = 0 # current overall status of game for black player
turn = "White"

# Draw Box: draws box on specified coordinates and surface
def drawBox(x, y, color, surf):
    pygame.draw.rect(surf, color, (x, y, 65, 65))

# Images of pieces for games
Rook_Img = [
    pygame.transform.scale( pygame.image.load('./images/Rook_Black.png'), (60, 60)),
    pygame.transform.scale( pygame.image.load('./images/Rook_White.png'), (60, 60)),
    ]

Knight_Img = [
    pygame.transform.scale( pygame.image.load('./images/Knight_Black.png'), (60, 60)),
    pygame.transform.scale( pygame.image.load('./images/Knight_White.png'), (60, 60)),
    ]

Bishop_Img = [
    pygame.transform.scale( pygame.image.load('./images/Bishop_Black.png'), (60, 60)),
    pygame.transform.scale( pygame.image.load('./images/Bishop_White.png'), (60, 60)),
    ]

Queen_Img = [
    pygame.transform.scale( pygame.image.load('./images/Queen_Black.png'), (60, 60)),
    pygame.transform.scale( pygame.image.load('./images/Queen_White.png'), (60, 60)),
    ]

King_Img = [
    pygame.transform.scale( pygame.image.load('./images/King_Black.png'), (60, 60)),
    pygame.transform.scale( pygame.image.load('./images/King_White.png'), (60, 60)),
    ]

Pawn_Img = [
    pygame.transform.scale( pygame.image.load('./images/Pawn_Black.png'), (55, 55)),
    pygame.transform.scale( pygame.image.load('./images/Pawn_White.png'), (55, 55)),
    ]

# Show image on the surface on specified coordinates
def showImg(surf, img, x, y):
    surf.blit(img, (x+3, y+3) )

# show pieces on chess board on screen
def showPieces(surf, board):
    for i in range(0, 8):
        for j in range(0, 8):
            if board[i][j] != None:
                # depanding on piece type and its color display the piece
                if board[i][j].type_ == "Rook":
                    if board[i][j].color == "Black":
                        showImg(surf, Rook_Img[0], j*65, i*65 )
                    else:
                        showImg(surf, Rook_Img[1], j*65, i*65 )

                if board[i][j].type_ == "Knight":
                    if board[i][j].color == "Black":
                        showImg(surf, Knight_Img[0], j*65, i*65 )
                    else:
                        showImg(surf, Knight_Img[1], j*65, i*65 )

                if board[i][j].type_ == "Bishop":
                    if board[i][j].color == "Black":
                        showImg(surf, Bishop_Img[0], j*65, i*65 )
                    else:
                        showImg(surf, Bishop_Img[1], j*65, i*65 )

                if board[i][j].type_ == "Queen":
                    if board[i][j].color == "Black":
                        showImg(surf, Queen_Img[0], j*65, i*65 )
                    else:
                        showImg(surf, Queen_Img[1], j*65, i*65 )

                if board[i][j].type_ == "King":
                    if board[i][j].color == "Black":
                        showImg(surf, King_Img[0], j*65, i*65 )
                    else:
                        showImg(surf, King_Img[1], j*65, i*65 )

                if board[i][j].type_ == "Pawn":
                    if board[i][j].color == "Black":
                        showImg(surf, Pawn_Img[0], j*65, i*65 )
                    else:
                        showImg(surf, Pawn_Img[1], j*65, i*65 )

# Return a string of old and new move in alphanumeric format
def moveToStr(x1, y1, x2, y2):
    return (str(chr(97+y1))+""+str(8-x1) )+" - " +(str(chr(97+y2))+""+str(8-x2) )

# Display special status of game, if currently any
def displayStatus(screen):
    screen.blit( font2.render( status, True, (255, 255, 255) ), (530, 400) )

# Check if there are only king pieces remaining on board
def justKings(board):
    whitePoints = 0
    blackPoints = 0
    for i in range(0, 8):
        for j in range(0, 8):
            if board[i][j] != None:
                # count white pieces
                if board[i][j].color == "White":
                    whitePoints += 1
                # count black pieces
                else:
                    blackPoints += 1
    return (blackPoints == 1 and whitePoints == 1)

# Game related variables
fc = None   # first move
sc = None   # second move
one_time_white = True
one_time_black = True
moves = []
moves_list = []
status = ""
status_display = False

running = True
while running:
    checkbox = 0

    for event in pygame.event.get():
        # user clicked the close button on window
        if event.type == pygame.QUIT:
            running = False

        # if its white's turn, then save which piece he wants to move and where 
        if event.type == pygame.MOUSEBUTTONDOWN:
            if turn == "White":
                x,y = pygame.mouse.get_pos()
                x //= 65
                y //= 65
                if fc == None:
                    fc = (x,y)
                elif sc == None:
                    sc = (x, y)
                elif fc != None and sc!= None:
                    fc = (x, y)
                    sc = None

    # fill the background with greenish color
    screen.fill((1, 20, 15))

    # display the checked board
    for x in range(0, 8):
        for y in range(0, 8):
            if checkbox:
                drawBox(x*65, y*65, (214, 214, 214), screen)
            else:
                drawBox(x*65, y*65, (6, 71, 54), screen)
            checkbox = 1 - checkbox
        checkbox = 1 - checkbox

    # highlight selected pieces
    if fc != None:
        drawBox(fc[0]*65, fc[1]*65, (194, 60, 50), screen)
    if sc != None:
        drawBox(sc[0]*65, sc[1]*65, (194, 60, 50), screen)

    # display chess pieces
    showPieces(screen, chessBoard)

    # show which player's turn it is
    screen.blit( font2.render( "Turn: "+turn, True, (255, 255, 255) ), (560, 50) )
    # display 10 recent moves
    i = 0
    for s in moves_list[:10]:
        screen.blit( font2.render( s, True, (255, 255, 255) ), (550, 100+i) )
        i += 30

    # display any special status the game players currently has
    displayStatus(screen)

    # show all the things on screen
    pygame.display.flip()

    # if there are only kings remaining then it is draw
    if justKings(chessBoard) == True:
        status = "Draw"
        running = False
        continue

    # if it is black's turn
    if turn == "Black":
        # get moves for black player
        if one_time_black == True:
            state2, moves = getMoves(turn, chessBoard)
            # player is checkmated
            if state2 == 2:
                status = "Checkmatted,W Wins"
                print("Black is Checkmatted. White Wins")
                running =False
            # stalemate
            elif state2 == 3:
                status = "Satelmate"
                print("Satelmate. Draw")
                running = False
            # if player can make a move, select the best move and move the piece
            if running == True:
                f, m = minimax("Black", chessBoard)
                movePiece(chessBoard, m[0], m[1], m[2], m[3], m[4])
                moves_list.insert( 0, "B "+chessBoard[m[3]][m[4]].type_+" "+moveToStr(m[1], m[2], m[3], m[4]) )
                # play piece slide sound
                sslide.play()
                pygame.time.delay(100)
                sslide.stop()
                turn = "White"
                one_time_white == True

    else:
        # get the moves for white player
        if one_time_white == True:
            state1, moves = getMoves(turn, chessBoard)
            # player is checkmated
            if state1 == 2:
                status = "Checkmatted,B Wins"
                print("White is Checkmatted. Black Wins")
                running = False
            # stalemate
            elif state1 == 3:
                status = "Satelmate"
                print("Satelmate. Draw")
                running = False
            one_time_white = False

        # if player is checked in or not
        if state1 == 0 or state1 == 1:
            if state1 == 1:
                status = "Checked"
            else:
                status = ""

            # if we got both choices for move, old as well as new
            if fc != None and sc != None:
                pygame.time.delay(20)
                oldx = fc[1]
                oldy = fc[0]
                newx = sc[1]
                newy = sc[0]

                # if we have a piece on old position and its color is same as player whose turn it is
                if chessBoard[oldx][oldy] != None and chessBoard[oldx][oldy].color == turn:
                    # check if the move was valid by looking it in the list of moves that player can make
                    i = 0
                    found = False
                    for i in range(0, len(moves) ):
                        if moves[i][1] == oldx and moves[i][2] == oldy and moves[i][3] == newx and moves[i][4] == newy:
                            found = True
                            index = i
                            break
                    if found:
                        # move was valid so move the piece to new position
                        movePiece(chessBoard, moves[i][0], moves[i][1], moves[i][2], moves[i][3], moves[i][4])
                        moves_list.insert(0, "W "+chessBoard[newx][newy].type_+" "+moveToStr(oldx, oldy, newx, newy) )
                        # play piece slide sound
                        sslide.play()
                        pygame.time.delay(100)
                        sslide.stop()
                        # if king is in check, update status
                        st, mv = getMoves(turn, chessBoard)
                        if st == 1:
                            status = "Checked"
                        else:
                            status = ""
                        turn = "Black"
                        one_time_white = True
                        fc = None
                        sc = None
                    else:
                        #print("Invalid Move")
                        sc = None
                        fc = None
                else:
                    fc = None
                    sc = None
                    #print("Invalid Move2")

# display game's final status
pygame.draw.rect(screen, (1, 20, 15), (520, 395, 100, 100))
displayStatus(screen)
pygame.display.update()

# wait some time before terminating the program
pygame.time.delay(3000)
pygame.quit()