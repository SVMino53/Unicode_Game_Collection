# Code made by Isak Forsberg. Last updated 2025-09-16.

from typing import Literal, Self



class Condition:
    def __init__(self, type: Literal["at_square", "sees", "in_check", "moved", "last_move_was"],
            params: dict, not_case: bool = False) -> None:
        """
        A game state condition that must be fulfilled for a move to be valid.

        Args:
            type (Literal["empty", "enemy", "friend", "in_check", "moved", "last_move_was"]): The type of condition.
            params (dict): Additional parameters required for the condition.  
                - For "at_square": {"loc_type": Literal["exact", "relative"], "row": int, "col": int, "has": piece_kwrds | "none"}.  
                - For "sees" {"direction": Literal["N", "E", "S", "W", "NE", "NW", "SE", "SW"], }
                - For "in_check": {"player": Literal["self", "other"]}
                - For "moved": {"times": int}
                - For "last_move_was": {"piece_type": Literal["pawn", "rook", "knight", "bishop", "queen", "king"], "player": Literal["self", "other"]}
        """
        pass
    def __repr__(self):
        pass
    def __str__(self):
        pass
    def check(self) -> bool:
        pass

class CEmpty(Condition):
    def __init__(self, location_type: Literal["exact", "relative", "direction"], row: int, col: int, not_case: bool = False):
        # super().__init__(type, params, not_case)
        pass