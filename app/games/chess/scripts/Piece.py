# Code by Isak Forsberg. Last updated 2025-09-16.

from typing import Literal
from scripts.Condition import Condition



class Move:
    def __init__(self, type: Literal["exact", "relative", "directional"],
            row: int, col: int, conditions: list[list[Condition]]) -> None:
        pass

class Piece:
    def __init__(
            self, 
            piece_type : Literal["pawn", "rook", "knight", "bishop", "queen", "king"], 
            color : Literal["white", "black"], 
            row : int, 
            col : int) -> None:
        self.pieceType = piece_type
        self.color = color
        self.row = row
        self.col = col
        self.moves = 0
        self.setChar()
        self.setValue()

    def __str__(self) -> str:
        return self.char

    def setChar(self):
        if self.color == 'white':
            self.char = ord('\u265a')   # White king sympol
        else:
            self.char = ord('\u2654')   # Black king symbol
        if self.pieceType == 'queen':
            self.char += 1
        elif self.pieceType == 'rook':
            self.char += 2
        elif self.pieceType == 'bishop':
            self.char += 3
        elif self.pieceType == 'knight':
            self.char += 4
        elif self.pieceType == 'pawn':
            self.char += 5
        self.char = chr(self.char)
    
    def setValue(self):
        if self.pieceType == 'pawn':
            self.value = 1
        elif self.pieceType == 'rook':
            self.value = 5
        elif self.pieceType in ['knight', 'pishop']:
            self.value = 3
        elif self.pieceType == 'queen':
            self.value = 8
        else:
            self.value = 100

    def promote(self, piece_type) -> None:
        """Exclusively for pawns! Promotes pawn to a given higher rank piece."""
        self.pieceType = piece_type
        self.setChar()
        self.setValue()