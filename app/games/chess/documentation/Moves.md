# Chess Piece Moves and Conditions
## About
This document describes every possible move in chess and what condintions need to be met to make each move.

## Table of Contents
- [Terms](#terms)
- [General Conditions](#general-conditions)
- [Pawn](#pawn)
    - [Regular](#regular)
    - [Two Steps](#two-steps)
    - [Capture](#capture)
    - [Regular Promotion](#regular-promotion)
    - [Capture Promotion](#capture-promotion)
    - [Left En Passante](#left-en-passante)
    - [Right En Passante](#right-en-passante)
- [Rook](#rook)
    - [Regular](#regular-1)
- [Knight](#knight)
    - [Regular](#regular-2)
- [Bishop](#bishop)
    - [Regular](#regular-3)
- [Queen](#queen)
    - [Regular](#regular-4)
- [King](#king)
    - [Regular](#regular-5)
    - [Left Castling](#left-castling)
    - [Right Castling](#right-castling)

## Terms
- **Squre has...**
    - **nothing** - The square that this piece is being moved to is empty.
    - **own piece** - The square that this piece is being moved to is occupied by one of your other pieces.
    - **opponent's piece** - The square that this piece is being moved to is occupied by one of the opponent's pieces.
- **Sees square** - The squares along the path, (excluding the square that the piece is being moved to), are empty.
- ***Piece*** **not moved** - *Piece* has not moved yet. (*piece* is some chess piece described by color and name. May be "this piece".)
- **White piece** - The piece being moved is white.
- **Black piece** - The piece being moved is black.
- **On rank** ***rank*** - The piece being moved is currently on rank *rank*. (*rank* is some integer between 1 and 8.)
- ***Piece*** **at** ***coordinate*** - A specific *piece* is at a certain *coordinate*. (*piece* is some chess piece described by color and name, and *coordinate* is the x and y coordinate, written as (*x*, *y*), relative to the moving piece's current location.)
- **Opponent's move was** ***move*** - The last move by the opponent was *move*. (*move* is the name of the move and the name of the type of piece that was moved.)
    - *(Optional)* **...to** ***coordinate*** - The square the opponet's piece was moved to. (*coordinate* is the x and y coordinate, written as (*x*, *y*), relative to the moving piece's current location.)
- **Not in check** - You are not currently in check.
- **No checks on path** - *(Only for Castling.)* On each square along the path, you would not be in check if the king was there.

## General Conditions
These conditions must always be met when moving a piece.
- Square has nothing *or* square has opponent's piece.
- Cannot move if it causes oneself to be in check.

## Pawn
### Regular

#### Move

#### Conditions
- Square has nothing.

### Two Steps
#### Move

#### Conditions
- Square has nothing.
- Sees square.
- This piece has not moved.

### Capture
#### Move

#### Conditions
- Square has opponent's piece.

### Regular Promotion
#### Move

#### Conditions
- Square has nothing.
- White piece *and* rank is 7  
*or* black piece *and* rank is 2.

### Capture Promotion
#### Move

#### Conditions
- Square has opponent's piece.
- White piece *and* rank is 7 *or* black piece *and* rank is 2.

### Left En Passante
#### Move

#### Conditions
- Square has nothing.
- White piece *and* rank is 5 *and* opponent's move was Two Steps (pawn) to (-1, 0)  
*or* black piece *and* rank is 4 *and* opponent's move was Two Steps (pawn) to (1, 0)

### Right En Passante
#### Move

#### Conditions
- Square has nothing.
- White piece *and* rank is 5 *and* opponent's move was Two Steps (pawn) to (1, 0)  
*or* black piece *and* rank is 4 *and* opponent's move was Two Steps (pawn) to (-1, 0)


## Rook
### Regular
- Sees square.


## Knight
### Regular


## Bishop
### Regular
- Sees square.


## Queen
### Regular
- Sees square.


## King
### Regular

### Left Castling
- Sees Square.
- This piece has not moved.
- Own left rook has not moved.
- Not in check.
- No check on path.

### Right Castling
- Sees Square.
- This piece has not moved.
- Own right rook has not moved.
- Not in check.
- No check on path.