import pytest
import logging
import config
import chess
import yaml
import os
import shutil
import sys
import importlib
from strategies import SimpleStrategy

if __name__ == "__main__":
    sys.exit(f"The script {os.path.basename(__file__)} should only be run by pytest.")
shutil.copyfile("lichess.py", "correct_lichess.py")
shutil.copyfile("test_bot/lichess.py", "lichess.py")
lichess_bot = importlib.import_module("lichess-bot")

logger = logging.getLogger(__name__)


@pytest.mark.parametrize(
    "fen,first_move,expected",
    [
        ("3b4/pp2kprp/8/1Bp5/4R3/1P6/P4PPP/1K6 b - - 0 22", "e7f8", "e4e8"),
        ("q2Q3k/1p4p1/3R1N1p/6r1/8/7P/PP3PP1/6K1 b - - 8 44", "a8d8", "d6d8"),
        ("3r4/pB3R2/1p2p3/8/kP4b1/2P1B3/P4P2/4K3 w - - 1 29", "b7e4", "d8d1"),
    ],
)
def test_simple_strategy_mate_in_1(fen, first_move, expected) -> None:
    with open("./config.yml.default") as file:
        CONFIG = yaml.safe_load(file)
    CONFIG["token"] = ""
    CONFIG["engine"]["name"] = "SimpleStrategy"
    CONFIG["engine"]["protocol"] = "homemade"
    CONFIG["pgn_directory"] = "TEMP/homemade_game_record"
    config.insert_default_values(CONFIG)
    bot = SimpleStrategy(commands=[], options={}, stderr=None, draw_or_resign=CONFIG)
    board = chess.Board(fen)
    board.push_uci(first_move)
    move = bot.search(board)

    assert move.move == chess.Move.from_uci(expected)


@pytest.mark.parametrize(
    "fen,expected",
    [
        (
            "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
            0,
        ),  #  starting position
        ("4k3/8/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", 4000),
    ],
)
def test_simple_strategy_eval(fen, expected) -> None:
    with open("./config.yml.default") as file:
        CONFIG = yaml.safe_load(file)
    CONFIG["token"] = ""
    CONFIG["engine"]["name"] = "SimpleStrategy"
    CONFIG["engine"]["protocol"] = "homemade"
    CONFIG["pgn_directory"] = "TEMP/homemade_game_record"
    config.insert_default_values(CONFIG)
    bot = SimpleStrategy(commands=[], options={}, stderr=None, draw_or_resign=CONFIG)
    board = chess.Board(fen)

    assert bot.eval(board) == expected


@pytest.mark.parametrize(
    "fen,first_move,expected", ## Several One Move + Hanging Piece puzzles from lichess
    [
        (
            "r1b1k2r/ppppqppp/2n2n2/2b1p3/2P1P3/3P1NP1/PP3PBP/RNBQK2R b KQkq - 0 6",
            "c5f2",
            "e1f2",
        ),
        (
            "rnbqk2r/pp3ppp/4pn2/2bp4/8/2P2NP1/PP2PPBP/RNBQK2R b KQkq - 1 6",
            "c5f2",
            "e1f2",
        ),
        (
            "r2qkbnr/ppp3pp/2np4/4p3/2B1PpbP/2NP1N2/PPP2PP1/R1BQK2R w KQkq - 3 7",
            "c4f7",
            "e8f7",
        ),
        (
            "rnbq1rk1/pp2nppp/3b4/3p4/3p1P2/3B1N2/PPP3PP/RNBQ1RK1 w - - 0 9",
            "d3h7",
            "g8h7",
        ),
        ("5nk1/6b1/3p4/3Pp1Q1/P5b1/8/4q1P1/2B2RK1 w - - 0 37", "f1f8", "g8f8"),
        ("5rk1/5p1p/3n2p1/8/1R3KP1/1N5r/P4P2/4R3 b - - 0 31", "h3f3", "f4f3"),
        ("5r1k/1p1q2pp/p2p4/5rP1/5P1P/P1P1P3/1P4Q1/R1B4K b - - 0 24", "f5d5", "g2d5"),
        ("8/8/5k2/5p2/5Kp1/3B3r/8/6R1 w - - 4 45", "g1f1", "h3d3"),
        ("2Q5/5ppk/5n1p/4p3/2P1q3/7P/6PK/8 b - - 0 35", "e4c4", "c8c4"),
        ("r2r2k1/5ppp/p1RNp1b1/1p6/1P6/P4P2/5KPP/3R4 b - - 2 23", "g6c2", "c6c2"),
        ("5r1k/6p1/1R3p1p/1p5n/P3N3/3P4/1r4PP/5R1K b - - 0 28", "b5a4", "b6b2"),
    ],
)
def test_simple_strategy_get_best_moves(fen, first_move, expected) -> None:
    with open("./config.yml.default") as file:
        CONFIG = yaml.safe_load(file)
    CONFIG["token"] = ""
    CONFIG["engine"]["name"] = "SimpleStrategy"
    CONFIG["engine"]["protocol"] = "homemade"
    CONFIG["pgn_directory"] = "TEMP/homemade_game_record"
    config.insert_default_values(CONFIG)
    bot = SimpleStrategy(commands=[], options={}, stderr=None, draw_or_resign=CONFIG)
    board = chess.Board(fen)
    board.push_uci(first_move)

    assert bot.get_best_moves(board) == [chess.Move.from_uci(expected)]
