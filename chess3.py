W = 0
B = 1
FILES = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
class Square:
    def __init__(self, file, rank):
        #Files are from 0 to 7, a to  h
        #Ranks are from 0 to 7, 1 to 8

        self.file = file
        self.rank = rank


    def __eq__(self, other):
        return (self.rank == other.rank) and (self.file == other.file)

    def __repr__(self):
        return FILES[self.file] + str(self.rank + 1)

    
    def isOccupied(self):
        for piece in Board.piece_list:
            if piece.sq == self:
                return True

        return False

    #MY PLAN WAS TO USE whichPiece once we have checked isOccupied, I thought this would be more readable, but ofcourse doing them together is more efficient
    def whichPiece(self):
        for piece in Board.piece_list:
            if piece.sq == self:
                return piece

            
        return None
             







class Piece:
    def __init__(self, sq, col):
        self.sq = sq
        self.col = col


    def move(self, sq1, sq2):
        #DO WE NEED TO CONSIDER THE EXCEPTION WHEN THERE IS A FRIENDLY PIECE HERE? OR CAN WE JUST TAKE CARE OF THAT IN LEGAL LIST?
        p1 = sq1.whichPiece()
        if not sq2.isOccupied():
            p1.sq = sq2

        else:
            p1.sq = sq2
            Board.piece_list.remove(sq2.whichPiece())




class Board:
    #We build a piece list here, which contains all the piece objects
    def __init__(self):
        sq_list = [[]]
        for i in range(8):
            for j in range(8):
                sq = Square(j, i)
                sq_list[i].append(sq)
            if i < 7:
                sq_list.append([])
        piece_list = []
        for i in range(8):
            piece = Pawn(Square(i, 1), W)
            piece_list.append(piece)
            
        for j in range(8):
            piece = Pawn(Square(j, 6), B)
            piece_list.append(piece)

        bishop1 = Bishop(Square(5, 0), W)
        piece_list.append(bishop1)
        rook1 = Rook(Square(7, 0), W)
        piece_list.append(rook1)
        #white_king = King(Square(4, 0), W)
        #black_king = King(Square(4, 7), B)
        

            
            
        self.sq_list = sq_list
        self.piece_list = piece_list

    def __str__(self):
        empty_string = ''
        for i in range(8):
            for j in range(8):
                if self.sq_list[j][i].isOccupied():
                    p = self.sq_list[j][i].whichPiece()
                    empty_string = empty_string + ' ' + str(p.type) + ' (' + str(p.sq.file) + str(p.sq.rank) + ' )'
            empty_string = empty_string + '\n'
        return empty_string



    def move(self, sq1, sq2):
        if sq1.isOccupied() and not sq2.isOccupied():
            p1 = sq1.whichPiece()
            p1.sq = sq2

        elif sq1.isOccupied() and sq2.isOccupied():
            p1 = sq1.whichPiece()
            p2 = sq2.whichPiece()
            p1.sq = sq2
            self.piece_list.remove(p2)







class Pawn(Piece):
    def __init__(self, sq, col):
        super().__init__(sq, col)


    def __str__(self):
        return str(self.sq.file) + str(self.sq.rank)

    def legal_moves(self):
        legals = []
        if self.sq.rank == 1:
            #We append the squares which are reachable
            sq1 = Square(self.sq.file, self.sq.rank + 1)
            sq2 = Square(self.sq.file, self.sq.rank + 2)
            legals.append(sq1)
            legals.append(sq2)

        else:
            sq1 = Square(self.sq.file, self.sq.rank + 1)
            legals.append(sq1)


        if self.sq.file == 0:
            if Board.sq_list[self.sq.file + 1][self.sq.rank + 1].isOccupied() and Board.sq_list[self.sq.file + 1][self.sq.rank + 1].whichPiece().col != self.col:
                sq = Square(self.sq.file + 1, self.sq.rank + 1)
                legals.append(sq)

            else:
                pass

        elif self.sq.file == 7:
            if Board.sq_list[self.sq.file - 1][self.sq.rank - 1].isOccupied() and Board.sq_list[self.sq.file - 1][self.sq.rank - 1].whichPiece().col != self.col:
                sq = Square(self.sq.file - 1, self.sq.rank - 1)
                legals.append(sq)


         #ADDING en passent, and promotion later

        else:
            if Board.sq_list[self.sq.file + 1][self.sq.rank + 1].isOccupied() and Board.sq_list[self.sq.file + 1][self.sq.rank + 1].whichPiece().col != self.col:
                sq = Square(self.sq.file + 1, self.sq.rank + 1)
                legals.append(sq)

            
            if Board.sq_list[self.sq.file - 1][self.sq.rank - 1].isOccupied() and Board.sq_list[self.sq.file - 1][self.sq.rank - 1].whichPiece().col != self.col:
                sq = Square(self.sq.file - 1, self.sq.rank - 1)
                legals.append(sq)



        return legals



class Bishop(Piece):
    def __init__(self, sq, col):
        super().__init__(sq, col)

    #THE ONLY PROBLEM IS THAT THE BISHOP CAN BE BLOCKED IN, WE MUST TAKE CARE OF THAT
    def legal_moves(self):
        legals = []
        #NO EDGE CASES HERE
        F = self.sq.file
        R = self.sq.rank
        i = 1
        
        while F + i < 8 and R + i < 8:
            sq = Square(F + i, R + i)
            if sq.isOccupied() and sq.whichPiece().col != self.col:
                legals.append(sq)
                break

            elif sq.isOccupied() and sq.whichPiece().col == self.col:
                break

            else:
                legals.append(sq)
                i = i + 1


        i = 1
        while F + i < 8 and R - i > -1:
            sq = Square(F + i, R - i)
            if sq.isOccupied() and sq.whichPiece().col != self.col:
                legals.append(sq)
                break

            elif sq.isOccupied() and sq.whichPiece().col == self.col:
                break

            else:
                legals.append(sq)
                i = i + 1


        i = 1
        while F - i > -1 and R - i > -1:
            sq = Square(F - i, R - i)
            if sq.isOccupied() and sq.whichPiece().col != self.col:
                legals.append(sq)
                break

            elif sq.isOccupied() and sq.whichPiece().col == self.col:
                break

            else:
                legals.append(sq)
                i = i + 1

        i = 1
        while F - i > -1 and R + i < 8:
            sq = Square(F - i, R + i)
            if sq.isOccupied() and sq.whichPiece().col != self.col:
                legals.append(sq)
                break

            elif sq.isOccupied() and sq.whichPiece().col == self.col:
                break

            else:
                legals.append(sq)
                i = i + 1


            
            
            
                
        return legals
        #we search in various directions
            
            

class Rook(Piece):
    def __init__(self, sq, col):
        super().__init__(sq, col)


    def legal_moves(self):
        legals = []
        F = self.sq.file
        R = self.sq.rank

        i = 1
        while F + i < 8:
            sq = Square(F + i, R)
            if sq.isOccupied() and sq.whichPiece().col != self.col:
                legals.append(sq)
                break

            elif sq.isOccupied() and sq.whichPiece().col == self.col:
                break

            else:
                legals.append(sq)
                i = i + 1


        i = 1
        while F - i > 0:
            sq = Square(F - i, R)
            if sq.isOccupied() and sq.whichPiece().col != self.col:
                legals.append(sq)
                break

            elif sq.isOccupied() and sq.whichPiece().col == self.col:
                break

            else:
                legals.append(sq)
                i = i + 1


        i = 1
        while R + i < 8:
            sq = Square(F, R + i)
            if sq.isOccupied() and sq.whichPiece().col != self.col:
                legals.append(sq)
                break

            elif sq.isOccupied() and sq.whichPiece().col == self.col:
                break

            else:
                legals.append(sq)
                i = i + 1

        i = 1
        while R - i > 0:
            sq = Square(F, R - i)
            if sq.isOccupied() and sq.whichPiece().col != self.col:
                legals.append(sq)
                break

            elif sq.isOccupied() and sq.whichPiece().col == self.col:
                break

            else:
                legals.append(sq)
                i = i + 1

        return legals
            


Board = Board()

sq1 = Square(7, 1)
sq2 = Square(7, 3)
Board.move(sq1, sq2)
sq3 = Square(6, 6)
sq4 = Square(6, 4)
Board.move(sq3, sq4)
Board.move(sq2, sq4)


print(Square(7, 0).whichPiece().legal_moves())
    
