# A group project by Manpreet and Vaibhav

# To be designed at the end:
# Castling
# En Passant
# Pawn Upgradation

#To Do
#Board Initialisation -- Done
#Pieces Movement List -- Done
#Pieces can cut each other -- Done
#Check check after each move -- Done
#All possible Turns Dictionary -- Done
#Alternative turns -- Done
#Expand Illegal Moves (Check) -- Done
#Checkmate and Stalemate to be integrated -- Done
#Document -- Done ig

#Might add board position list for easy reference

#-------------------------------------------------------------------------#

import os,time      #For clearscreen and to stop program, basically so that user will like the chess

clearConsole = lambda: os.system('cls' if os.name in ('nt', 'dos') else 'clear')
#Cleaar Screen copied from net

#Reference:
WHITE = 0
BLACK = 1

PIECE_DICT = {1: 'P', 2: 'N', 3: 'B', 4: 'R', 5: 'Q', 6: 'K'}   #References
FILES = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']                #The coloumns
REV_FILES = [0, 1, 2, 3, 4, 5, 6, 7]                            #Coloumns in numbers


class Square:
    #Each square of the board
    
    def __init__(self, y, x, piece=None):  # Input row, coloumn = y, x (Might change to x,y if persisted)
        self.x = x
        self.y = y
        self.piece = piece

    def __repr__(self):  # When square is called, prints the square rank+file
        return FILES[self.x] + str(self.y + 1)

    def __str__(self):  # When print() is called, prints the piece on it
        if self.piece == None:
            return " "
        else:
            return PIECE_DICT[self.piece.type]


class Board:
    #Our ChessBoard

    def __init__(self):     #Initialises an empty chessboard
        board = []
        for i in range(8):  # The ranks (rows)
            row = []
            for j in range(8):  # The files (coloumns)
                sq = Square(i, j)
                row.append(sq)
            board.append(row)
        self.board = board

    def board_reset(self):  #Resets the board for a new game, adds the pieces to the correct position
        # Pawns
        for i in range(8):
            self.board[1][i].piece = Pawn(0, self.board[1][i])
            self.board[6][i].piece = Pawn(1, self.board[6][i])

        # Manual work... :'(

        # Rooks
        self.board[0][0].piece = Rook(0, self.board[0][0])
        self.board[0][7].piece = Rook(0, self.board[0][7])
        self.board[7][0].piece = Rook(1, self.board[7][0])
        self.board[7][7].piece = Rook(1, self.board[7][7])

        # Knights
        self.board[0][1].piece = Knight(0, self.board[0][1])
        self.board[0][6].piece = Knight(0, self.board[0][6])
        self.board[7][1].piece = Knight(1, self.board[7][1])
        self.board[7][6].piece = Knight(1, self.board[7][6])

        # Bishops
        self.board[0][2].piece = Bishop(0, self.board[0][2])
        self.board[0][5].piece = Bishop(0, self.board[0][5])
        self.board[7][2].piece = Bishop(1, self.board[7][2])
        self.board[7][5].piece = Bishop(1, self.board[7][5])

        # Queen
        self.board[0][3].piece = Queen(0, self.board[0][3])
        self.board[7][3].piece = Queen(1, self.board[7][3])

        # King
        self.board[0][4].piece = King(0, self.board[0][4])
        self.board[7][4].piece = King(1, self.board[7][4])

    def __str__(self):      #Prints the current piece position
        for i in range(7, -1, -1):
            temp = [self.board[i][j] for j in range(8)]
            print(*temp)
        #Might add another printing line which prints the board positions for easy reference
        return ""
    
    def isCheck(self, king):    #Whether king is in check
        #Iterates over all pieces and seeing whether it is threating the king or not
        for i in range(8):
            for j in range(8):
                sq = self.board[i][j]
                if sq.piece != None and sq.piece.col != king.col:
                    if king.sq in sq.piece.move_list():
                        return True
        return False

    def turn_dict(self, col):   #Returns all the possible moves of a colour

        move_dict = {1:[], 2:[],3:[],4:[], 5:[], 6:[]}  #Initialise
        
        #Loops over all possible case and adds the moves
        for i in range(8):  
            for j in range(8):
                sq = self.board[i][j]
                if sq.piece != None and sq.piece.col == col:
                    move_dict[sq.piece.type].append(repr(sq) + " " + str(sq.piece.move_list()))
        return move_dict

    def isCheckmate(self, king):    #Checks whether king is in Checkmate
        return self.isCheck(king) and self.isMate(king)
    
    def isStalemate(self, king):    #Checks whether king is in stalemate
        return (not self.isCheck(king)) and self.isMate(king)
    
    def isMate(self, king):     #A common function for checking whether the king is in mate or not
        #Check or stale would be added later xp
        #Basically the commonality between stale and check, whether the king is threatened over
        #any position move of any other piece of king's color

        for i in range(1,7):
            all_moves = self.turn_dict(king.col)
            for j in all_moves[i]:
                initial, final_list = j[0:2], j[4:-1]
                if len(final_list)==0:
                    pass
                else:
                    final_list = list(final_list.split(", "))
                    initial = convert_square(initial)
                    print(initial ,final_list)
                    for j in range(len(final_list)):
                        final = convert_square(final_list[j])
                        temp = final.piece
                        initial.piece.move(final)
                        if self.isCheck(king):
                            final.piece.force_move(initial)
                            final.piece = temp
                        else:
                            final.piece.force_move(initial)
                            final.piece = temp
                            return False
        return True


ChessBoard = Board()        #Our ChessBoard in this game
#Big name, I know. Had to write a few many times...


class Piece:
    #The base class for all the pieces on the board with move function

    def __init__(self, color, square, piece_type=None):
        self.type = piece_type
        self.sq = square
        self.col = color

    def can_move(self, dest):
        board = ChessBoard.board
        if board[dest.y][dest.x].piece == None or board[dest.y][dest.x].piece.col != self.col:
            return True
        return False
    
    def move(self, dest):           #If legal, then can move
        if dest in self.move_list():
            del dest.piece
            dest.piece = self
            self.sq.piece = None
            self.sq = dest
            return True
        
        else:
            return False
    
    def force_move(self,dest):      #Clear from name
        del dest.piece
        dest.piece = self
        self.sq.piece = None
        self.sq = dest


class King(Piece):
    def __init__(self, color, square, piece_type = 6):
        super().__init__(color, square, piece_type)

    def move_list(self):
        #Generates the legal move list of the piece
        moves = []
        row = self.sq.y
        coloumn = self.sq.x
        board = ChessBoard.board

        for i in range(-1, 2):
            for j in range(-1, 2):
                if row+i < 8 and row+i > -1 and coloumn+j < 8 and coloumn+j > -1:
                    if board[row+i][coloumn+j].piece == None or board[row+i][coloumn+j].piece.col != self.col:
                        if i==0 and j==0:
                            pass
                        else:
                            moves.append(board[row+i][coloumn+j])

        return moves


class Queen(Piece):
    def __init__(self, color, square, piece_type = 5):
        super().__init__(color, square, piece_type)
    
    def move_list(self):
        moves = []
        board = ChessBoard.board
        row = self.sq.y
        coloumn = self.sq.x

        #Bishops move
        for i in range(1,8):
            if row+i < 8 and coloumn+i < 8 and self.can_move(board[row+i][coloumn+i]):
                moves.append(board[row+i][coloumn+i])
                if board[row+i][coloumn+i].piece != None:
                    break
            else:
                break
        
        for i in range(1,8):
            if row-i > -1 and coloumn-i > -1 and self.can_move(board[row-i][coloumn-i]):
                moves.append(board[row-i][coloumn-i])
                if board[row-i][coloumn-i].piece != None:
                    break
            else:
                break
        
        for i in range(1,8):
            if row+i < 8 and coloumn-i > -1 and self.can_move(board[row+i][coloumn-i]):
                moves.append(board[row+i][coloumn-i])
                if board[row+i][coloumn-i].piece != None:
                    break
            else:
                break
        
        for i in range(1,8):
            if row-i > -1 and coloumn+i < 8 and self.can_move(board[row-i][coloumn+i]):
                moves.append(board[row-i][coloumn+i])
                if board[row-i][coloumn+i].piece != None:
                    break
            else:
                break
        
        #Rook's moves
        for i in range(1,8):
            if row+i<8 and row+i >-1:
                if board[row+i][coloumn].piece != None:
                    if board[row+i][coloumn].piece.col != self.col:
                        moves.append(board[row+i][coloumn])
                    break

                else:
                    moves.append(board[row+i][coloumn])
            else:
                break
        
        for i in range(-1,-8, -1):
            if row+i < 8 and row+i > -1:
                if board[row+i][coloumn].piece != None:
                    if board[row+i][coloumn].piece.col != self.col:
                        moves.append(board[row+i][coloumn])
                    break

                else:
                    moves.append(board[row+i][coloumn])
            else:
                break
        
        for i in range(1,8):
            if coloumn+i<8 and coloumn+i >-1:
                if board[row][coloumn+i].piece != None:
                    if board[row][coloumn+i].piece.col != self.col:
                        moves.append(board[row][coloumn+i])
                    break

                else:
                    moves.append(board[row][coloumn+i])
            else:
                break
        
        for i in range(-1,-8,-1):
            if coloumn+i<8 and coloumn+i >-1:
                if board[row][coloumn+i].piece != None:
                    if board[row][coloumn+i].piece.col != self.col:
                        moves.append(board[row][coloumn+i])
                    break

                else:
                    moves.append(board[row][coloumn+i])
            else:
                break

        return moves


class Rook(Piece):
    def __init__(self, color, square, piece_type=4):
        super().__init__(color, square, piece_type)
    
    def move_list(self):
        moves = []
        board = ChessBoard.board
        row = self.sq.y
        coloumn = self.sq.x

        for i in range(1,8):
            if row+i<8 and row+i >-1:
                if board[row+i][coloumn].piece != None:
                    if board[row+i][coloumn].piece.col != self.col:
                        moves.append(board[row+i][coloumn])
                    break

                else:
                    moves.append(board[row+i][coloumn])
            else:
                break
        
        for i in range(-1,-8, -1):
            if row+i < 8 and row+i > -1:
                if board[row+i][coloumn].piece != None:
                    if board[row+i][coloumn].piece.col != self.col:
                        moves.append(board[row+i][coloumn])
                    break

                else:
                    moves.append(board[row+i][coloumn])
            else:
                break
        
        for i in range(1,8):
            if coloumn+i<8 and coloumn+i >-1:
                if board[row][coloumn+i].piece != None:
                    if board[row][coloumn+i].piece.col != self.col:
                        moves.append(board[row][coloumn+i])
                    break

                else:
                    moves.append(board[row][coloumn+i])
            else:
                break
        
        for i in range(-1,-8,-1):
            if coloumn+i<8 and coloumn+i >-1:
                if board[row][coloumn+i].piece != None:
                    if board[row][coloumn+i].piece.col != self.col:
                        moves.append(board[row][coloumn+i])
                    break

                else:
                    moves.append(board[row][coloumn+i])
            else:
                break
        
        return moves


class Bishop(Piece):
    def __init__(self, color, square, piece_type=3):
        super().__init__(color, square, piece_type)
    
    def move_list(self):
        moves = []
        row = self.sq.y
        coloumn = self.sq.x
        board = ChessBoard.board
        
        for i in range(1,8):
            if row+i < 8 and coloumn+i < 8 and self.can_move(board[row+i][coloumn+i]):
                moves.append(board[row+i][coloumn+i])
                if board[row+i][coloumn+i].piece != None:
                    break
            else:
                break
        
        for i in range(1,8):
            if row-i > -1 and coloumn-i > -1 and self.can_move(board[row-i][coloumn-i]):
                moves.append(board[row-i][coloumn-i])
                if board[row-i][coloumn-i].piece != None:
                    break
            else:
                break
        
        for i in range(1,8):
            if row+i < 8 and coloumn-i > -1 and self.can_move(board[row+i][coloumn-i]):
                moves.append(board[row+i][coloumn-i])
                if board[row+i][coloumn-i].piece != None:
                    break
            else:
                break
        
        for i in range(1,8):
            if row-i > -1 and coloumn+i < 8 and self.can_move(board[row-i][coloumn+i]):
                moves.append(board[row-i][coloumn+i])
                if board[row-i][coloumn+i].piece != None:
                    break
            else:
                break
        
        return moves


class Knight(Piece):
    def __init__(self, color, square, piece_type=2):
        super().__init__(color, square, piece_type)
    
    def move_list(self):
        moves = []
        row = self.sq.y
        coloumn = self.sq.x
        board = ChessBoard.board
        if row+2 < 8 and coloumn+1 < 8 and self.can_move(board[row+2][coloumn+1]):
            moves.append(board[row+2][coloumn+1])
        if row+2 < 8 and coloumn > 0 and self.can_move(board[row+2][coloumn-1]):
            moves.append(board[row+2][coloumn-1])
        
        if row+1 < 8 and coloumn+2 < 8 and self.can_move(board[row+1][coloumn+2]):
            moves.append(board[row+1][coloumn+2])
        if row+1 < 8 and coloumn-2 > -1 and self.can_move(board[row+1][coloumn-2]):
            moves.append(board[row+1][coloumn-2])
        
        if row-2 > -1 and coloumn+1 < 8 and self.can_move(board[row-2][coloumn+1]):
            moves.append(board[row-2][coloumn+1])
        if row-2 > -1 and coloumn-1 > -1 and self.can_move(board[row-2][coloumn-1]):
            moves.append(board[row-2][coloumn-1])
        
        if row-1 > -1 and coloumn+2 < 8 and self.can_move(board[row-1][coloumn+2]):
            moves.append(board[row-1][coloumn+2])
        if row-1 > -1 and coloumn-2 > -1 and self.can_move(board[row-1][coloumn-2]):
            moves.append(board[row-1][coloumn-2])

        return moves        


class Pawn(Piece):
    def __init__(self, color, square, piece_type=1):
        super().__init__(color, square, piece_type)
        self.first_move = True

    def move_list(self):
        moves = []
        row = self.sq.y
        coloumn = self.sq.x
        board = ChessBoard.board

        if self.col == 0 and row != 7:
            if board[row+1][coloumn].piece == None:
                moves.append(board[row+1][coloumn])
            if row == 1 and self.first_move and board[row+2][coloumn].piece == None:
                moves.append(board[row+2][coloumn])
            if coloumn != 7 and board[row+1][coloumn+1].piece != None and \
                    board[row+1][coloumn+1].piece.col == 1:
                moves.append(board[row+1][coloumn+1])
            if coloumn != 0 and board[row+1][coloumn-1].piece != None and \
                    board[row+1][coloumn-1].piece.col == 1:
                moves.append(board[row+1][coloumn-1])

        elif self.col == 1 and row != 0:
            if board[row-1][coloumn].piece == None:
                moves.append(board[row-1][coloumn])
            if row == 6 and self.first_move and board[row-2][coloumn].piece == None:
                moves.append(board[row-2][coloumn])
            if coloumn != 7 and board[row-1][coloumn+1].piece != None and \
                    board[row-1][coloumn+1].piece.col == 0:
                moves.append(board[row-1][coloumn+1])
            if coloumn != 0 and board[row-1][coloumn-1].piece != None and \
                    board[row-1][coloumn-1].piece.col == 0:
                moves.append(board[row-1][coloumn-1])

        return moves




ChessBoard.board_reset()
board = ChessBoard.board


def convert_square(s):
    #Converts the input to the corresponding square of the board
    i = FILES.index(s[0])
    j = int(s[1])-1
    return board[j][i]

def current_play(counter):
    #The game runner

    clearConsole()
    try:
        if counter == 0:    #White's move

            print(ChessBoard)

            print ("White's Turn: Input Initial and Final Squares")
            move = list(input().split())
            initial = convert_square(move[0])
            final = convert_square(move[1])

            if initial.piece.col == 0:  #Checks whether the colour is correct
                temp = initial.piece.move(final)    #Temporary moves the piece to see whether it is valid

                if  temp == False:
                    clearConsole()
                    print("Please Input a Legal Move")
                    time.sleep(1)
                    return current_play(counter)

                elif ChessBoard.isCheck(WK):    #If the move puts king in check
                    clearConsole()
                    print("Error: White King in Check after the move. Be aware!")
                    print(ChessBoard)
                    time.sleep(2)
                    final.piece.force_move(initial)
                    return current_play(counter)

            else:
                clearConsole()
                print("Please Input White's Move")
                time.sleep(1)
                return current_play(counter)
        
        else:
            print(ChessBoard)

            print ("Black's Turn: Input Initial and Final Squares")
            move = list(input().split())
            initial = convert_square(move[0])
            final = convert_square(move[1])
            
            if initial.piece.col == 1:
            
                if initial.piece.move(final) == False:
                    clearConsole()
                    print("Please Input a Legal Move")
                    time.sleep(1)
                    return current_play(counter)

                elif ChessBoard.isCheck(BK):
                    clearConsole()
                    print("Error: Black King in Check after the move. Be aware!")
                    print(ChessBoard)
                    time.sleep(2)
                    final.piece.force_move(initial)
                    return current_play(counter)
            
            else:
                clearConsole()
                print("Please Input Black's Move")
                time.sleep(1)
                return current_play(counter)

    except:
        clearConsole()
        print("Please Input as per Move Notation: 'Initial' + ' ' + 'Final'")
        print("Make Sure the initial place has a piece")        #Correct this
        time.sleep(1)
        return current_play(counter)

    return (counter+1)%2


ChessBoard.board_reset()    #Initialise the board

#Oof... Hard Work again...

# White Pieces
WP1 = ChessBoard.board[1][0].piece
WP2 = ChessBoard.board[1][1].piece
WP3 = ChessBoard.board[1][2].piece
WP4 = ChessBoard.board[1][3].piece
WP5 = ChessBoard.board[1][4].piece
WP6 = ChessBoard.board[1][5].piece
WP7 = ChessBoard.board[1][6].piece
WP8 = ChessBoard.board[1][7].piece

WR1 = ChessBoard.board[0][0].piece
WR2 = ChessBoard.board[0][7].piece

WN1 = ChessBoard.board[0][1].piece
WN2 = ChessBoard.board[0][6].piece

WB1 = ChessBoard.board[0][2].piece
WB2 = ChessBoard.board[0][5].piece

WQ = ChessBoard.board[0][3].piece

WK = ChessBoard.board[0][4].piece

# Black Pieces
BP1 = ChessBoard.board[6][0].piece
BP2 = ChessBoard.board[6][1].piece
BP3 = ChessBoard.board[6][2].piece
BP4 = ChessBoard.board[6][3].piece
BP5 = ChessBoard.board[6][4].piece
BP6 = ChessBoard.board[6][5].piece
BP7 = ChessBoard.board[6][6].piece
BP8 = ChessBoard.board[6][7].piece

BR1 = ChessBoard.board[7][0].piece
BR2 = ChessBoard.board[7][7].piece

BN1 = ChessBoard.board[7][1].piece
BN2 = ChessBoard.board[7][6].piece

BB1 = ChessBoard.board[7][2].piece
BB2 = ChessBoard.board[7][5].piece

BQ = ChessBoard.board[7][3].piece

BK = ChessBoard.board[7][4].piece


counter = 0
while not (ChessBoard.isCheckmate(WK) or ChessBoard.isStalemate(WK) or\
    ChessBoard.isStalemate(BK) or ChessBoard.isCheckmate(BK)):
    counter = current_play(counter)

clearConsole()
if ChessBoard.isCheckmate(WK):
    print("Black Wins! Congrats!")
elif ChessBoard.isCheckmate(BK):
    print("White Wins! Congrats!")
else:
    print("Great Play! It's a tie!")


print(ChessBoard)

