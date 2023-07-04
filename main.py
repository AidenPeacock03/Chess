import numpy as np
import tkinter as tk
from functools import partial

class Board:
    def __init__(self):
        # flip MSB for white = 0 black = 1
        # pawn = 0b001, rook = 0b010, knight = 0b011, bishop = 0b100, queen = 0b101, king = 0b110, 0 = empty square
        self.takenpiece = None
        self.state = np.zeros((8, 8))
        self.pawn = np.zeros((8, 8))
        self.state = self.state.astype(int)
        self.pawn = self.state.astype(int)
        self.turn = 0
        self.whiteking = [7, 4]
        self.blacking = [0, 4]
        self.cflag = 0
        self.movestore = []
        self.latch = 0

        # pawn setup
        for i in range(8):
            self.state[1, i] = 0b1001
            self.state[6, i] = 0b0001
            self.pawn[1, i] = 1
            self.pawn[6, i] = 2

        # black pieces
        self.state[0, 0] = 0b1010
        self.state[0, 1] = 0b1011
        self.state[0, 2] = 0b1100
        self.state[0, 3] = 0b1101
        self.state[0, 4] = 0b1110
        self.state[0, 5] = 0b1100
        self.state[0, 6] = 0b1011
        self.state[0, 7] = 0b1010
        #white pieces
        self.state[7, 0] = 0b0010
        self.state[7, 1] = 0b0011
        self.state[7, 2] = 0b0100
        self.state[7, 3] = 0b0101
        self.state[7, 4] = 0b0110
        self.state[7, 5] = 0b0100
        self.state[7, 6] = 0b0011
        self.state[7, 7] = 0b0010

        win = tk.Tk()
        self.Button_ID = []
        self.Boarddict = {}
        self.Boarddict["99"] = tk.PhotoImage(file=r"0.png")
        c = 0
        for i in range(8):
            for j in range(8):
                if (i + j) % 2 == 0:
                    colour = "#FFBEB0"
                else:
                    colour = "#A64A36"
                strinky = ("{}{}".format(i, j))
                self.Boarddict[strinky] = tk.PhotoImage(file=r"{}.png".format(self.state[i, j]))
                win.B = tk.Button(bg=colour, activebackground="lawn green", image=self.Boarddict[strinky],
                                   height=60, width=60, command=partial(self.move, c))
                win.B.grid(row=i, column=j)
                self.Button_ID.append(win.B)
                c += 1

        win.mainloop()

    def legal_list(self, row, col):
        knight = False
        moves = []
        if self.state[row, col] & 0b0111 == 0b0010: #rook
            identity = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        elif self.state[row, col] & 0b0111 == 0b0100: #bishop
            identity = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        elif self.state[row, col] & 0b0111 == 0b0101: #queen
            identity = [(1, 1), (1, -1), (-1, 1), (-1, -1), (1, 0), (-1, 0), (0, 1), (0, -1)]
        elif self.state[row, col] & 0b0111 == 0b0011: #knight
            knight = True
            identity = [(2, 1), (2, -1), (1, 2), (1, -2), (-2, 1), (-1, 2), (-1, -2), (-2, -1)]
        elif self.state[row, col] & 0b0111 == 0b0110: #king
            knight = True
            identity = [(1, 1), (1, 0), (0, 1), (1, -1), (-1, 1), (-1, 0), (0, -1), (-1, -1)]
        elif self.state[row, col] == 0b0001: #white pawn
            if self.pawn[row, col] == 2:
                identity = [(-1, 0), (-2, 0)]
                if self.state[row-2, col] != 0:
                    identity = [(-1, 0)]
                elif self.state[(row-1, col)]:
                    identity = []
            else:
                identity = [(-1, 0)]
                if self.state[row-1, col] != 0:
                    identity = []
            if self.state[row-1, col-1] != 0:
                identity.append((-1, -1))
            if col+1 < 8 and self.state[row-1, col+1] != 0:
                identity.append((-1, 1))
            knight = True
        elif self.state[row, col] == 0b1001: #black pawn
            if self.pawn[row, col] == 1:
                identity = [(1, 0), (2, 0)]
                if self.state[row + 2, col] != 0:
                    identity = [(1, 0)]
                elif self.state[(row + 1, col)]:
                    identity = []
            else:
                identity = [(1, 0)]
                if self.state[row+1, col] != 0:
                    identity = []
            if row+1 < 8 and self.state[row+1, col-1] != 0:
                identity.append((1, -1))
            if row+1 < 8 and col+1 < 8 and self.state[row+1, col+1] != 0:
                identity.append((1, 1))
            knight = True
        else:
            identity = []

        for i in range(len(identity)):
            n = identity[i][0]
            m = identity[i][1]
            check = True
            while check:
                if row+n > 7 or col+m > 7 or row+n < 0 or col+m < 0:
                    check = False
                elif self.state[row+n,col+m] == 0:
                    moves.append((row+n, col+m))
                elif (self.state[row+n,col+m] ^ self.state[row, col]) >> 3 == 1:
                    moves.append((row+n, col+m))
                    check = False
                else:
                    check = False
                n += identity[i][0]
                m += identity[i][1]
                if knight:
                    check = False
        return moves

    def in_check(self):
        if self.turn%2 == 0:
            kingsquare = self.whiteking
        else:
            kingsquare = self.blacking
        for i in range(8):
            for j in range(8):
                if (self.state[i, j] ^ self.state[kingsquare[0], kingsquare[1]]) >> 3 == 1 and self.state[i, j] != 0:
                    legalmoves = self.legal_list(i, j)
                    if (kingsquare[0], kingsquare[1]) in legalmoves:
                        self.cflag += 1
        if self.cflag > 0:
            self.cflag = 0
            return True
        else:
            self.cflag = 0
            return False

    def move(self, c):
        bname = self.Button_ID[c]
        self.movestore.append(bname)
        if len(self.movestore) == 2:
            info1 = self.movestore[0].grid_info()
            info2 = self.movestore[1].grid_info()
            piece = (info1["row"], info1["column"])
            square = (info2["row"], info2["column"])
            moves = self.legal_list(piece[0], piece[1])
            self.dummymove(piece, square, False)
            if self.in_check():
                moves = []
            self.dummymove(piece, square, True)
            print(self.state)
            if square in moves and (self.state[piece] >= 9 and self.turn % 2 == 1 or self.state[piece] < 9 and self.turn % 2 == 0):
                if (info1["row"] + info1["column"]) % 2 == 0:
                    self.movestore[1].config(bg="#FFBEB0", image=self.Boarddict["99"])
                else:
                    self.movestore[1].config(bg="#A64A36", image=self.Boarddict["99"])

                if (info2["row"] + info2["column"]) % 2 == 0:
                    self.movestore[0].config(bg="#FFBEB0")
                else:
                    self.movestore[0].config(bg="#A64A36")
                self.movestore[0].grid(row=info2["row"], column=info2["column"])
                self.movestore[1].grid(row=info1["row"], column=info1["column"])

                self.state[square] = self.state[piece]
                self.state[piece] = 0
                self.turn += 1
                if piece[0] == self.whiteking[0] and piece[1] == self.whiteking[1]:
                    self.whiteking[0] = square[0]
                    self.whiteking[1] = square[1]
                if piece[0] == self.blacking[0] and piece[1] == self.blacking[1]:
                    self.blacking[0] = square[0]
                    self.blacking[1] = square[1]
            self.movestore.clear()
            print(self.state)

    def dummymove(self, piece, square, undo):
        if piece == square:
            return
        if not undo:
            moves = self.legal_list(piece[0], piece[1])
            if square in moves and (
                    self.state[piece] >= 9 and self.turn % 2 == 1 or self.state[piece] < 9 and self.turn % 2 == 0):
                self.latch = 0
                self.takenpiece = self.state[square]
                self.state[square] = self.state[piece]
                self.state[piece] = 0
                if piece[0] == self.whiteking[0] and piece[1] == self.whiteking[1]:
                    self.whiteking[0] = square[0]
                    self.whiteking[1] = square[1]
                if piece[0] == self.blacking[0] and piece[1] == self.blacking[1]:
                    self.blacking[0] = square[0]
                    self.blacking[1] = square[1]
            else:
                self.latch = 1

        elif self.latch == 0:
            self.state[piece] = self.state[square]
            self.state[square] = self.takenpiece
            if square[0] == self.whiteking[0] and square[1] == self.whiteking[1]:
                self.whiteking[0] = piece[0]
                self.whiteking[1] = piece[1]
            if square[0] == self.blacking[0] and square[1] == self.blacking[1]:
                self.blacking[0] = piece[0]
                self.blacking[1] = piece[1]















game = Board()
