# Code by Isak Forsberg. Last updated 2025-09-16.

from typing import Literal
from scripts.Board import Board
from scripts.Player import Player, AI
from scripts.Piece import Piece



class Game:
    def __init__(self) -> None:
        self.gameMode : int = 0             # 1 = Player vs Player; 2 = Player vs AI; 3 = AI vs AI
        self.board : Board = None           # Chess board
        self.players : list[Player] = []    # Human players currently playing
        self.ais : list[AI] = []            # AIs currently playing
        self.toMove = 'white'
        self.curPl = None                   # Whoever's move it is currently
        self.eval : int = 0                 # The game evaluation
        self.inp = ''                       # User input

    def movePiece(self, p_color : str, fromCo : str, toCo : str) -> bool:
        if self.board.p1Color == 'white':
            fRow = 8 - int(fromCo[1])
            fCol = ord(fromCo[0].lower()) - 97
            tRow = 8 - int(toCo[1])
            tCol = ord(toCo[0].lower()) - 97
        else:
            fRow = int(fromCo[1]) - 1
            fCol = 105 - ord(fromCo[0].lower())
            tRow = int(toCo[1]) - 1
            tCol = 105 - ord(toCo[0].lower())
        p = self.board.pieces[fRow][fCol]
        if p == None:
            print('Selected square is empty!\n')
            return False
        elif p.color != p_color:
            print('That\'s not your piece!\n')
            return False
        else:
            s = self.board.pieces[tRow][tCol]
            rel = (tRow - fRow, tCol - fCol)
            if p_color == self.board.p1Color:
                dirMult = -1
            else:
                dirMult = 1
            canMove = False
            if p.pieceType == 'pawn':
                if (rel == (dirMult, 0) and s == None or
                    rel == (dirMult, -1) and s != None and p.color != s.color or
                    rel == (dirMult, -1) and s == None and self.board.pieces[tRow - dirMult][tCol] == self.lastMoved or
                    rel == (dirMult, 1) and s != None and p.color != s.color or
                    rel == (dirMult, 1) and s == None and self.board.pieces[tRow - dirMult][tCol] == self.lastMoved or
                    rel == (2*dirMult, 0) and p.moves == 0 and self.board.pieces[fRow + dirMult][fCol] == None and s == None):
                    canMove = True
            elif p.pieceType == 'rook':
                if rel[0] == 0 or rel[1] == 0:
                    dist = max(abs(rel[0]), abs(rel[1]))
                    dirc = (rel[0] // dist, rel[1] // dist)
                    isBlocked = False
                    for i in range(1, dist):
                        if self.board.pieces[fRow + dirc[0]*i][fCol + dirc[1]*i] != None:
                            isBlocked = True
                            break
                    if not isBlocked and (s == None or p.color != s.color):
                        canMove = True
            elif p.pieceType == 'knight':
                if abs(rel[0]) == 1 and abs(rel[1]) == 2 or abs(rel[0]) == 2 and abs(rel[1]) == 1:
                    if s == None or p.color != s.color:
                        canMove = True
            elif p.pieceType == 'bishop':
                if abs(rel[0]) == abs(rel[1]):
                    dist = abs(rel[0])
                    dirc = (rel[0] // dist, rel[1] // dist)
                    isBlocked = False
                    for i in range(1, dist):
                        if self.board.pieces[fRow + dirc[0]*i][fCol + dirc[1]*i] != None:
                            isBlocked = True
                            break
                    if not isBlocked and (s == None or p.color != s.color):
                        return True
            elif p.pieceType == 'queen':
                if rel[0] == 0 or rel[1] == 0 or abs(rel[0]) == abs(rel[1]):
                    dist = max(abs(rel[0]), abs(rel[1]))
                    dirc = (rel[0] // dist, rel[1] // dist)
                    isBlocked = False
                    for i in range(1, dist):
                        if self.board.pieces[fRow + dirc[0]*i][fCol + dirc[1]*i] != None:
                            isBlocked = True
                            break
                    if not isBlocked and (s == None or p.color != s.color):
                        return True
            elif p.pieceType == 'king':
                if (abs(rel[0]) < 2 and abs(rel[1]) < 2 or
                    rel[1] == 2 and p.moves == 0 and self.board[p.row][p.col + 1:] == [None, None]):
                    if s == None or p.color != s.color:
                        canMove = True
        if canMove:
            if p.pieceType == 'pawn':
                if abs(rel[1]) == 1 and self.board.pieces[tRow][tCol] == None:
                    self.pieces[tRow - 1][tCol] = None
                    print('An passant!\n')
                elif (p.color == self.board.p1Color and tRow == 7 or
                    p.color == self.board.p2Color and tRow == 0):
                    inp = input('Promotion! What should your pawn promote to?\n"q" -> Queen\n"r" -> Rook\n"b" -> Bishop\n"n" -> Knight\n>>> ')
                    while not inp.lower() in ['q', 'r', 'b', 'n']:
                        inp = input('Invalid input! Please type "q", "r", "b" or "n" to promote your pawn.\n>>> ').lower()
                    if inp == 'q':
                        pType = 'queen'
                    elif inp == 'r':
                        pType = 'rook'
                    elif inp == 'b':
                        pType == 'bishop'
                    else:
                        pType == 'knight'
                    p.promote(pType)
            # Castling
            p.moves += 1
            self.board.pieces[fRow][fCol] = None
            self.board.pieces[tRow][tCol] = p
            self.lastMoved = p
            return True
        else:
            print('Cannot move piece!\n')
            return False

    def start(self):
        print('Welcome to chess! The only chess that ever chessed! Is that a verb? It is now! :D\n\n')
        self.menu()
        print('Thanks for playing! Bye bye! :)')

    def menu(self):
        self.inp = 'new'  # Starts off by setting up a new game.
        while self.inp != 'quit':  # Exits loop when player types "quit".
            # Set up a new game.
            if self.inp == 'new':
                self.players = []
                self.ais = []
                self.toMove = 'white'
                self.inp = input('How do you want to play? [1, 2, 3]\n1: Player vs Player\n2: Player vs AI\n3: AI vs AI\n>>> ')
                while not self.inp in ['1', '2', '3']:
                    self.inp = input('Invalid input! Please type "1", "2" or "3" to choose a game mode.\n>>> ')
                self.gameMode = int(self.inp)
                if self.gameMode <= 2:  # Player 1 is human.
                    name1 = input('Nice! What is your name player 1?\n>>> ')
                    while not self.inp == 'y':
                        self.inp = input(f'"{name1}". Did I get that right? [y, n]\n>>> ').lower()
                        while not self.inp in ['y', 'n']:
                            self.inp = input('Invalid input! Please type "y" (yes) or "n" (no).\n>>> ').lower()
                        if self.inp == 'n':
                            name1 = input('Sorry! I must have missheard you. What is your name then player 1?\n>>> ')
                    self.inp = input('Ok, cool! And what color of pieces will you play with? [w, b]\n>>> ').lower()
                    while not self.inp in ['w', 'b']:
                        self.inp = input('Invalid input! Please type "w" (white) or "b" (black).\n>>> ').lower()
                    if self.inp == 'w':
                        self.players.append(Player(name1, 'white'))
                    else:
                        self.players.append(Player(name1, 'black'))
                    if self.gameMode == 1:  # Player 2 is human.
                        name2 = input(f'Thank you {name1}! Now, player 2, what is your name?\n>>> ')
                        while not self.inp == 'y':
                            self.inp = input(f'"{name2}". Did I get that right? [y, n]\n>>> ').lower()
                            while not self.inp in ['y', 'n']:
                                self.inp = input('Invalid input! Please type "y" (yes) or "n" (no).\n>>> ').lower()
                            if self.inp == 'n':
                                name2 = input('Sorry! I must have missheard you. What is your name then player 2?\n>>> ')
                        if self.players[0].color == 'white':
                            self.players.append(Player(name2, 'black'))
                        else:
                            self.players.append(Player(name2, 'white'))
                        print(f'{name1} and {name2}. Fun to have you both here! :)\n')
                    else:  # Player 2 is AI.
                        w = input(f'Thank you {name1}! Now, how advanced should the AI be? First write its width. (Higher value makes it slower!)\n>>> ')
                        while not w.isdigit() or int(w) < 1:
                            w = input('Invalid input! Please type an integer greater than 0.\n>>> ')
                        w = int(w)
                        d = input('Great! What should the depth be? (Higher value makes it slower!)\n>>> ')
                        while not d.isdigit() or int(d) < 1:
                            d = input('Invalid input! Please type an integer greater than 0.\n>>> ')
                        d = int(d)
                        if self.players[0].color == 'white':
                            self.ais.append(AI(d, w, 'black'))
                        else:
                            self.ais.append(AI(d, w, 'white'))
                    self.board = Board(self.players[0].color)
                else:  # Both players are AI.
                    w = input(f'Cool! How advanced should the first AI be? First write its width. (Higher value makes it slower!)\n>>> ')
                    while not w.isdigit() or w < 1:
                        w = input('Invalid input! Please type an integer greater than 0.\n>>> ')
                    w = int(w)
                    d = input('Great! What should the depth be? (Higher value makes it slower!)\n>>> ')
                    while not d.isdigit() or d < 1:
                        d = input('Invalid input! Please type an integer greater than 0.\n>>> ')
                    d = int(d)
                    self.inp = input('And which color of pieces should the first AI play as? [w, b]\n>>> ').lower()
                    while not self.inp in ['w', 'b']:
                        self.inp = input('Invalid input! Please type "w" (white) or "b" (black).\n>>> ').lower()
                    if self.inp == 'w':
                        self.ais.append(AI(d, w, 'white'))
                    else:
                        self.ais.append(AI(d, w, 'black'))
                    w = input(f'Super duper! How advanced should the second AI be? First write its width. (Higher value makes it slower!)\n>>> ')
                    while not w.isdigit() or w < 1:
                        w = input('Invalid input! Please type an integer greater than 0.\n>>> ')
                    w = int(w)
                    d = input('Great! What should the depth be? (Higher value makes it slower!)\n>>> ')
                    while not d.isdigit() or d < 1:
                        d = input('Invalid input! Please type an integer greater than 0.\n>>> ')
                    d = int(d)
                    if self.ais[0].color == 'white':
                        self.ais.append(AI(d, w, 'black'))
                    else:
                        self.ais.append(AI(d, w, 'white'))
                self.play()

    def play(self):
        print('Alright! Let\'s play! :D\n')
        while not self.inp in ['quit', 'new']:
            print(self.board)
            if len(self.players) >= 1 and self.players[0].color == self.toMove:
                self.curPl = self.players[0]
            elif len(self.players) == 2 and self.players[1].color == self.toMove:
                self.curPl = self.players[1]
            elif self.ais[0].color == self.toMove:
                self.curPl = self.ais[0]
            else:
                self.curPl = self.ais[1]
            print(f'It\'s your turn {self.curPl.name}!')
            self.inp = input('What would you like to do? [move, view, reset, quit]\n>>> ').lower()
            while not self.inp in ['move', 'view', 'reset', 'quit']:
                self.inp = input('Invalid input! Please type "move", "view", "reset" or "quit".\n>>> ').lower()
            if self.inp == 'reset':
                self.inp = input('Are you super sure you want to reset the game? This game will not be saved. [y, n]\n>>> ').lower()
                while not self.inp in ['y', 'n']:
                    self.inp = input('Invalid input! Please type "y" (yes) or "n" (no).\n>>> ').lower()
                if self.inp == 'y':
                    print()
                    self.inp = 'new'
                    return
            elif self.inp == 'quit':
                self.inp = input('Are you super sure you want to quit the game? This game will not be saved. [y, n]\n>>> ').lower()
                while not self.inp in ['y', 'n']:
                    self.inp = input('Invalid input! Please type "y" (yes) or "n" (no).\n>>> ').lower()
                if self.inp == 'y':
                    print()
                    self.inp = 'quit'
                    return
            elif self.inp == 'move':
                hasMoved = False
                while not hasMoved:
                    if self.curPl in self.players:
                        self.inp = input('Select the piece you want to move. (Example: "a6")\n>>> ').lower()
                        let = 'abcdefgh'
                        num = '12345678'
                        while len(self.inp) != 2 or not self.inp[0] in let or not self.inp[1] in num:
                            print('Invalid input! Input has to be a letter between a-h followed by a digit between 1-8.')
                            print('Examples of valid inputs: "a6", "h8", "A1", "D4".')
                            self.inp = input('Please type the coordinates of a valid piece.\n>>> ').lower()
                        fromCo = self.inp
                        self.inp = input('Where should the piece move? (Type "undo" to select another piece.)\n>>> ').lower()
                        while self.inp != 'undo' and (len(self.inp) != 2 or not self.inp[0] in let or not self.inp[1] in num):
                            print('Invalid input! Input has to be a letter between a-h followed by a digit between 1-8.')
                            print('Examples of valid inputs: "a6", "h8", "A1", "D4". (Type "undo" to slect another piece.)')
                            self.inp = input('Please type he coordinates of a valid piece\n>>> ').lower()
                        if self.inp != 'undo':
                            toCo = self.inp
                            hasMoved = self.movePiece(self.toMove, fromCo, toCo)
                    else:
                        self.curPl.calculateMove(self.board, self.eval)
                if self.toMove == 'white':
                    self.toMove = 'black'
                else:
                    self.toMove = 'white'