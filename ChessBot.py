# A group project by Manpreet and Vaibhav

# To be designed at the end:
# Castling
# En Passant
# Pawn Upgradation

#-------------------------------------------------------------------------#

WHITE = 0
BLACK = 1

PIECE_DICT = {1: 'P', 2: 'N', 3: 'B', 4: 'R', 5: 'Q', 6: 'K'}
FILES = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
REV_FILES = [0, 1, 2, 3, 4, 5, 6, 7]


class Square:
    def __init__(self, y, x, piece=None):  # Input row, coloumn = y,x
        self.x = x
        self.y = y
        self.col = (x+y+1) % 2
        self.piece = piece

    def __repr__(self):  # When square is called, prints the square rank+file
        return FILES[self.x] + str(self.y + 1)

    def __str__(self):  # When print() is called, prints the piece on it
        if self.piece == None:
            return " "
        else:
            return PIECE_DICT[self.piece.type]


class Board:
    def __init__(self):
        board = []
        for i in range(8):  # The ranks (rows)
            row = []
            for j in range(8):  # The files (coloumns)
                sq = Square(i, j)
                row.append(sq)
            board.append(row)
        self.board = board

    def board_reset(self):
        # Pawns
        for i in range(8):
            self.board[1][i].piece = Pawn(0, self.board[1][i])
            self.board[6][i].piece = Pawn(1, self.board[6][i])

        # Manual work... Welp

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

    def __str__(self):
        for i in range(7, -1, -1):
            temp = [self.board[i][j] for j in range(8)]
            print(*temp)
        return ""


ChessBoard = Board()


class Piece:
    def __init__(self, color, square, piece_type=None):
        self.type = piece_type
        self.sq = square
        self.col = color

    def can_move(self, dest):
        board = ChessBoard.board
        if board[dest.y][dest.x].piece == None or board[dest.y][dest.x].piece.col != self.col:
            return True
    
    def move(self, dest):
        if dest in self.move_list():
            dest.piece = self
            self.sq.piece = None
            self.sq = dest
        
        else:
            print("Illegal Move")


class King(Piece):
    def __init__(self, color, square, piece_type=6):
        super().__init__(color, square, piece_type)

    def move_list(self):
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
    def __init__(self, color, square, piece_type=5):
        super().__init__(color, square, piece_type)
    
    def move_list(self):
        moves = []
        board = ChessBoard.board
        row = self.sq.y
        coloumn = self.sq.x

        for i in range(1,8):
            if row+i < 8 and coloumn+i < 8 and self.can_move(board[row+i][coloumn+i]):
                moves.append(board[row+i][coloumn+i])
            else:
                break
        
        for i in range(1,8):
            if row-i > -1 and coloumn-i > -1 and self.can_move(board[row-i][coloumn-i]):
                moves.append(board[row-i][coloumn-i])
            else:
                break
        
        for i in range(1,8):
            if row+i < 8 and coloumn-i > -1 and self.can_move(board[row+i][coloumn-i]):
                moves.append(board[row+i][coloumn-i])
            else:
                break
        
        for i in range(1,8):
            if row-i > -1 and coloumn+i < 8 and self.can_move(board[row-i][coloumn+i]):
                moves.append(board[row-i][coloumn+i])
            else:
                break

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
            else:
                break
        
        for i in range(1,8):
            if row-i > -1 and coloumn-i > -1 and self.can_move(board[row-i][coloumn-i]):
                moves.append(board[row-i][coloumn-i])
            else:
                break
        
        for i in range(1,8):
            if row+i < 8 and coloumn-i > -1 and self.can_move(board[row+i][coloumn-i]):
                moves.append(board[row+i][coloumn-i])
            else:
                break
        
        for i in range(1,8):
            if row-i > -1 and coloumn+i < 8 and self.can_move(board[row-i][coloumn+i]):
                moves.append(board[row-i][coloumn+i])
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



print(ChessBoard)