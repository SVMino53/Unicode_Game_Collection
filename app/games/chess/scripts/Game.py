# Code by Isak Forsberg. Last updated 2025-09-16.

# from typing import Literal
from scripts.Board import Board
from scripts.Player import Player, AI
# from scripts.Piece import Piece



class Game:
    def __init__(self) -> None:
        self.game_mode : int = 0            # 1 = Player vs Player; 2 = Player vs AI; 3 = AI vs AI
        self.board : Board = None           # Chess board
        self.players : list[Player] = []    # Human players currently playing
        self.ais : list[AI] = []            # AIs currently playing
        self.to_move = 'white'
        self.cur_player = None              # Whoever's move it is currently
        self.eval : int = 0                 # The game evaluation
        self.inp = ''                       # User input

    def movePiece(self, player_color : str, from_square : str, to_square : str) -> bool:
        if self.board.p1_color == 'white':
            from_row = 8 - int(from_square[1])
            from_col = ord(from_square[0].lower()) - 97
            to_row = 8 - int(to_square[1])
            to_col = ord(to_square[0].lower()) - 97
        else:
            from_row = int(from_square[1]) - 1
            from_col = 105 - ord(from_square[0].lower())
            to_row = int(to_square[1]) - 1
            to_col = 105 - ord(to_square[0].lower())
        piece = self.board.pieces[from_row][from_col]
        if piece is None:
            print('Selected square is empty!\n')
            return False
        elif piece.color != player_color:
            print('That\'s not your piece!\n')
            return False
        else:
            s = self.board.pieces[to_row][to_col]
            rel = (to_row - from_row, to_col - from_col)
            if player_color == self.board.p1_color:
                dir_mult = -1
            else:
                dir_mult = 1
            can_move = False
            if piece.piece_type == 'pawn':
                if (rel == (dir_mult, 0) and s is None or
                    rel == (dir_mult, -1) and s is not None and piece.color != s.color or
                    rel == (dir_mult, -1) and s is None and self.board.pieces[to_row - dir_mult][to_col] == self.last_moved or
                    rel == (dir_mult, 1) and s is not None and piece.color != s.color or
                    rel == (dir_mult, 1) and s is None and self.board.pieces[to_row - dir_mult][to_col] == self.last_moved or
                    rel == (2*dir_mult, 0) and piece.moves == 0 and self.board.pieces[from_row + dir_mult][from_col] is None and s is None):
                    can_move = True
            elif piece.piece_type == 'rook':
                if rel[0] == 0 or rel[1] == 0:
                    dist = max(abs(rel[0]), abs(rel[1]))
                    dirc = (rel[0] // dist, rel[1] // dist)
                    is_blocked = False
                    for i in range(1, dist):
                        if self.board.pieces[from_row + dirc[0]*i][from_col + dirc[1]*i] is not None:
                            is_blocked = True
                            break
                    if not is_blocked and (s is None or piece.color != s.color):
                        can_move = True
            elif piece.piece_type == 'knight':
                if abs(rel[0]) == 1 and abs(rel[1]) == 2 or abs(rel[0]) == 2 and abs(rel[1]) == 1:
                    if s is None or piece.color != s.color:
                        can_move = True
            elif piece.piece_type == 'bishop':
                if abs(rel[0]) == abs(rel[1]):
                    dist = abs(rel[0])
                    dirc = (rel[0] // dist, rel[1] // dist)
                    is_blocked = False
                    for i in range(1, dist):
                        if self.board.pieces[from_row + dirc[0]*i][from_col + dirc[1]*i] is not None:
                            is_blocked = True
                            break
                    if not is_blocked and (s is None or piece.color != s.color):
                        return True
            elif piece.piece_type == 'queen':
                if rel[0] == 0 or rel[1] == 0 or abs(rel[0]) == abs(rel[1]):
                    dist = max(abs(rel[0]), abs(rel[1]))
                    dirc = (rel[0] // dist, rel[1] // dist)
                    is_blocked = False
                    for i in range(1, dist):
                        if self.board.pieces[from_row + dirc[0]*i][from_col + dirc[1]*i] is not None:
                            is_blocked = True
                            break
                    if not is_blocked and (s is None or piece.color != s.color):
                        return True
            elif piece.piece_type == 'king':
                if (abs(rel[0]) < 2 and abs(rel[1]) < 2 or
                    rel[1] == 2 and piece.moves == 0 and self.board[piece.row][piece.col + 1:] == [None, None]):
                    if s is None or piece.color != s.color:
                        can_move = True
        if can_move:
            if piece.piece_type == 'pawn':
                if abs(rel[1]) == 1 and self.board.pieces[to_row][to_col] is None:
                    self.pieces[to_row - 1][to_col] = None
                    print('An passant!\n')
                elif (piece.color == self.board.p1_color and to_row == 7 or
                    piece.color == self.board.p2_color and to_row == 0):
                    inp = input('Promotion! What should your pawn promote to?\n"q" -> Queen\n"r" -> Rook\n"b" -> Bishop\n"n" -> Knight\n>>> ')
                    while inp.lower() not in ['q', 'r', 'b', 'n']:
                        inp = input('Invalid input! Please type "q", "r", "b" or "n" to promote your pawn.\n>>> ').lower()
                    if inp == 'q':
                        piece_type = 'queen'
                    elif inp == 'r':
                        piece_type = 'rook'
                    elif inp == 'b':
                        piece_type == 'bishop'
                    else:
                        piece_type == 'knight'
                    piece.promote(piece_type)
            # Castling
            piece.moves += 1
            self.board.pieces[from_row][from_col] = None
            self.board.pieces[to_row][to_col] = piece
            self.last_moved = piece
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
                self.to_move = 'white'
                self.inp = input('How do you want to play? [1, 2, 3]\n1: Player vs Player\n2: Player vs AI\n3: AI vs AI\n>>> ')
                while self.inp not in ['1', '2', '3']:
                    self.inp = input('Invalid input! Please type "1", "2" or "3" to choose a game mode.\n>>> ')
                self.game_mode = int(self.inp)
                if self.game_mode <= 2:  # Player 1 is human.
                    name1 = input('Nice! What is your name player 1?\n>>> ')
                    while not self.inp == 'y':
                        self.inp = input(f'"{name1}". Did I get that right? [y, n]\n>>> ').lower()
                        while self.inp not in ['y', 'n']:
                            self.inp = input('Invalid input! Please type "y" (yes) or "n" (no).\n>>> ').lower()
                        if self.inp == 'n':
                            name1 = input('Sorry! I must have missheard you. What is your name then player 1?\n>>> ')
                    self.inp = input('Ok, cool! And what color of pieces will you play with? [w, b]\n>>> ').lower()
                    while self.inp not in ['w', 'b']:
                        self.inp = input('Invalid input! Please type "w" (white) or "b" (black).\n>>> ').lower()
                    if self.inp == 'w':
                        self.players.append(Player(name1, 'white'))
                    else:
                        self.players.append(Player(name1, 'black'))
                    if self.game_mode == 1:  # Player 2 is human.
                        name2 = input(f'Thank you {name1}! Now, player 2, what is your name?\n>>> ')
                        while not self.inp == 'y':
                            self.inp = input(f'"{name2}". Did I get that right? [y, n]\n>>> ').lower()
                            while self.inp not in ['y', 'n']:
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
                    w = input('Cool! How advanced should the first AI be? First write its width. (Higher value makes it slower!)\n>>> ')
                    while not w.isdigit() or w < 1:
                        w = input('Invalid input! Please type an integer greater than 0.\n>>> ')
                    w = int(w)
                    d = input('Great! What should the depth be? (Higher value makes it slower!)\n>>> ')
                    while not d.isdigit() or d < 1:
                        d = input('Invalid input! Please type an integer greater than 0.\n>>> ')
                    d = int(d)
                    self.inp = input('And which color of pieces should the first AI play as? [w, b]\n>>> ').lower()
                    while self.inp not in ['w', 'b']:
                        self.inp = input('Invalid input! Please type "w" (white) or "b" (black).\n>>> ').lower()
                    if self.inp == 'w':
                        self.ais.append(AI(d, w, 'white'))
                    else:
                        self.ais.append(AI(d, w, 'black'))
                    w = input('Super duper! How advanced should the second AI be? First write its width. (Higher value makes it slower!)\n>>> ')
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
        while self.inp not in ['quit', 'new']:
            print(self.board)
            if len(self.players) >= 1 and self.players[0].color == self.to_move:
                self.cur_player = self.players[0]
            elif len(self.players) == 2 and self.players[1].color == self.to_move:
                self.cur_player = self.players[1]
            elif self.ais[0].color == self.to_move:
                self.cur_player = self.ais[0]
            else:
                self.cur_player = self.ais[1]
            print(f'It\'s your turn {self.cur_player.name}!')
            self.inp = input('What would you like to do? [move, view, reset, quit]\n>>> ').lower()
            while self.inp not in ['move', 'view', 'reset', 'quit']:
                self.inp = input('Invalid input! Please type "move", "view", "reset" or "quit".\n>>> ').lower()
            if self.inp == 'reset':
                self.inp = input('Are you super sure you want to reset the game? This game will not be saved. [y, n]\n>>> ').lower()
                while self.inp not in ['y', 'n']:
                    self.inp = input('Invalid input! Please type "y" (yes) or "n" (no).\n>>> ').lower()
                if self.inp == 'y':
                    print()
                    self.inp = 'new'
                    return
            elif self.inp == 'quit':
                self.inp = input('Are you super sure you want to quit the game? This game will not be saved. [y, n]\n>>> ').lower()
                while self.inp not in ['y', 'n']:
                    self.inp = input('Invalid input! Please type "y" (yes) or "n" (no).\n>>> ').lower()
                if self.inp == 'y':
                    print()
                    self.inp = 'quit'
                    return
            elif self.inp == 'move':
                has_moved = False
                while not has_moved:
                    if self.cur_player in self.players:
                        self.inp = input('Select the piece you want to move. (Example: "a6")\n>>> ').lower()
                        let = 'abcdefgh'
                        num = '12345678'
                        while len(self.inp) != 2 or self.inp[0] not in let or self.inp[1] not in num:
                            print('Invalid input! Input has to be a letter between a-h followed by a digit between 1-8.')
                            print('Examples of valid inputs: "a6", "h8", "A1", "D4".')
                            self.inp = input('Please type the coordinates of a valid piece.\n>>> ').lower()
                        from_square = self.inp
                        self.inp = input('Where should the piece move? (Type "undo" to select another piece.)\n>>> ').lower()
                        while self.inp != 'undo' and (len(self.inp) != 2 or self.inp[0] not in let or self.inp[1] not in num):
                            print('Invalid input! Input has to be a letter between a-h followed by a digit between 1-8.')
                            print('Examples of valid inputs: "a6", "h8", "A1", "D4". (Type "undo" to slect another piece.)')
                            self.inp = input('Please type he coordinates of a valid piece\n>>> ').lower()
                        if self.inp != 'undo':
                            to_square = self.inp
                            has_moved = self.movePiece(self.to_move, from_square, to_square)
                    else:
                        self.cur_player.calculateMove(self.board, self.eval)
                if self.to_move == 'white':
                    self.to_move = 'black'
                else:
                    self.to_move = 'white'