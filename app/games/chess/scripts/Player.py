# Code by Isak Forsberg. Last updated 2024-06-16.

from typing import Literal



class Player:
    def __init__(self, name, color) -> None:
        self.name = name
        self.color = color
        self.score = 0
        self.wins = 0
    

class AI:
    def __init__(self, depth, width, color) -> None:
        self.depth = depth
        self.width = width
        self.color = color

    def testMove(self, board, player2move):
        pass
    
    def calculateMove(self, board, eval):
        maxScore = -100