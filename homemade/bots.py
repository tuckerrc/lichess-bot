import chess
from chess.engine import PlayResult, Limit
from engine_wrapper import MinimalEngine, MOVE
from typing import Any
import random
import logging

logger = logging.getLogger(__name__)

class SimpleStrategy(MinimalEngine):
    def search(self, board: chess.Board, *args: Any) -> PlayResult:
        moves = list(board.legal_moves)
        logger.info(board)
        checkmates = []
        for m in moves:
            new_board = board.copy()
            new_board.push(m)
            if new_board.is_checkmate():
                checkmates.append(m)

        if len(checkmates) > 0:
            return PlayResult(checkmates[0], None)

        best_moves = self.get_best_moves(board)
        return PlayResult(random.choice(best_moves), None)

    def get_best_moves(self, board: chess.Board) -> Any: # Better type later
        moves = list(board.legal_moves)
        bot_color = board.turn

        best_moves = moves.copy() # Assume all moves are best (prevents an empty return list)
        best_move_score = self.eval(board)
        logger.info({"best_move_score": best_move_score})
        for m in moves:
            new_board = board.copy()
            new_board.push(m)
            move_score = self.eval(new_board)
            if bot_color:
                if move_score > best_move_score:
                    best_move_score = move_score
                    best_moves = [m]
                elif move_score == best_move_score:
                    best_moves.append(m)
            else:
                ## For chess.BLACK negative scores are better
                if move_score < best_move_score:
                    best_move_score = move_score
                    best_moves = [m]
                elif move_score == best_move_score:
                    best_moves.append(m)
        logger.info({"best_moves": best_moves, "best_move_score": best_move_score})

        return best_moves


    def piece_value(self, board: chess.Board) -> int:
        PIECE_VALUE = {
            chess.PAWN: 100,
            chess.KNIGHT: 300,
            chess.BISHOP: 350,
            chess.ROOK: 500,
            chess.QUEEN: 900,
            chess.KING: 10000,
        }

        pieces = board.piece_map().values()
        score = 0

        for piece in pieces:
            piece_value = PIECE_VALUE[piece.piece_type]
            if piece.color == chess.WHITE:
                score += piece_value
            else:
                score -= piece_value

        return score

    def eval(self, board: chess.Board) -> int:
        return self.piece_value(board)
