# Code by Isak Forsberg. Last updated 2025-09-16.

# from typing import Literal
from scripts.Piece import Piece



class Board:
    def __init__(self, p1_color : str) -> None:
        self.p1_color = p1_color
        if p1_color == 'white':
            self.p2_color = 'black'
            piece_setup = ['rook', 'knight', 'bishop', 'queen', 'king', 'bishop', 'knight', 'rook']
        else:
            self.p2_color = 'white'
            piece_setup = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook']
        self.last_moved = None
        self.pieces = [[Piece(piece_setup[i], self.p2_color, 0, i) for i in range(8)]]  # 2d list of the pieces on the board.
        self.pieces.append([Piece('pawn', self.p2_color, 1, i) for i in range(8)])
        for _ in range(4):
            self.pieces.append([None for _ in range(8)])
        self.pieces.append([Piece('pawn', self.p1_color, 6, i) for i in range(8)])
        self.pieces.append([Piece(piece_setup[i], self.p1_color, 7, i) for i in range(8)])

    def __str__(self) -> str:
        output = '\n'*5 + ' '*2 + '-'*33 + '\n'
        for i in range(8):
            if self.p1_color == 'white':
                output += f'{8 - i}'
            else:
                output += f'{1 + i}'
            output += ' | '
            for p in self.pieces[i]:
                if p is None:
                    output += ' '
                else:
                    output += str(p)
                
                output += ' | '
            output += '\n' + ' '*2 + '-'*33 + '\n'
        if self.p1_color == 'white':
            output += '    A   B   C   D   E   F   G   H\n'
        else:
            output += '    H   G   F   E   D   C   B   A\n'
        return output
    # def copyBoard(board : Board) -> Board:
    #     copy = Board(board.p1_color)
    #     copy.pieces = []
    #     for l in board.pieces:
    #         copy.pieces.append([p for p in l])
    #     copy.last_moved = board.last_moved