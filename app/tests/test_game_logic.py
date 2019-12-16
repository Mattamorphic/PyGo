from app.game_logic import GameLogic, KOError, SuicideError, OccupiedError
from app.piece import Piece
import unittest


class TestGameLogic(unittest.TestCase):
    def test_instantiation_of_game_logic_raises_error(self):
        with self.assertRaises(ValueError):
            gl = GameLogic([])
            self.assertTrue(gl.getplayer() == Piece.White)

    def test_instantiation_of_game_logic(self):
        board = [[0 for i in range(0, 7)] for j in range(0, 7)]
        gl = GameLogic(board)
        self.assertTrue(gl.getplayer() == Piece.White)

    def test_get_opponent_positions_empty_board(self):
        board = [[0 for i in range(0, 7)] for j in range(0, 7)]
        gl = GameLogic(board)
        self.assertListEqual([], gl.getPositions(gl.opponent))

    def test_get_opponent_positions_with_pieces(self):
        board = [[0, 0, 0, 1, 2, 1, 0], [0, 0, 0, 0, 1, 0, 0],
                 [0, 0, 0, 0, 0, 2, 0], [0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0]]

        gl = GameLogic(board)
        self.assertListEqual([(0, 4), (2, 5)], gl.getPositions(gl.opponent))

    def test_get_opponent_positions_with_pieces_at_edges(self):
        board = [[2, 0, 0, 0, 0, 0, 2], [0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0],
                 [2, 0, 0, 0, 0, 0, 2]]

        gl = GameLogic(board)
        self.assertListEqual([(0, 0), (0, 6), (6, 0), (6, 6)],
                             gl.getPositions(gl.opponent))

    def test_get_adjacents_middle_board(self):
        board = [[0 for i in range(0, 7)] for j in range(0, 7)]
        gl = GameLogic(board)
        self.assertListEqual([
            (5, 4),
            (4, 5),
            (6, 5),
            (5, 6),
        ], gl.getAdjacents(5, 5))

    def test_get_adjacents_top_edge(self):
        board = [[0 for i in range(0, 7)] for j in range(0, 7)]
        gl = GameLogic(board)
        self.assertListEqual([(0, 4), (1, 5), (0, 6)], gl.getAdjacents(0, 5))

    #
    # def test_get_adjacents_right_edge(self):
    #
    # def test_get_adjacents_bottom_edge(self):
    #
    # def test_get_adjacents_left_edge(self):
    #
    # def test_get_adjacents_out_of_bounds(self):

    def test_has_specific_piece(self):
        board = [[0, 0, 0, 1, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0]]

        gl = GameLogic(board)
        self.assertTrue(gl.hasSpecificPiece(gl.getplayer(), 0, 3))

    def test_doesnt_have_specific_piece(self):
        board = [[0, 0, 0, 1, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0]]

        gl = GameLogic(board)
        self.assertFalse(gl.hasSpecificPiece(gl.getplayer(), 0, 2))

    def test_has_adjacents_covered_single_group(self):
        board = [[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 1, 0, 0, 0],
                 [0, 0, 1, 2, 1, 0, 0], [0, 0, 0, 1, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0]]

        gl = GameLogic(board)
        opponent = gl.getPositions(gl.opponent).pop()
        self.assertTrue(
            gl.areAdjacentsCovered(gl.player, gl.getAdjacents(*opponent)))

    def test_doesnt_have_adjacents_covered_single_group(self):
        board = [[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 1, 0, 0, 0, 0], [0, 1, 2, 0, 0, 0, 0],
                 [0, 0, 1, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0]]

        gl = GameLogic(board)
        opponent = gl.getPositions(gl.opponent).pop()
        self.assertFalse(
            gl.areAdjacentsCovered(gl.player, gl.getAdjacents(*opponent)))

    def test_has_adjacents_covered_single_group_edge(self):
        board = [[0, 0, 1, 2, 1, 0, 0], [0, 0, 0, 1, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0]]

        gl = GameLogic(board)
        opponent = gl.getPositions(gl.opponent).pop()
        self.assertTrue(
            gl.areAdjacentsCovered(gl.player, gl.getAdjacents(*opponent)))

    # def test_has_adjacents_covered_multi_group:
    #     pass

    def test_scan_board_empty(self):
        board = [[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0]]

        gl = GameLogic(board)
        self.assertEqual(0, len(gl.scanBoard(gl.player, gl.opponent)))

    def test_scan_board_no_score(self):
        board = [[0, 0, 1, 1, 2, 1, 2], [0, 0, 2, 2, 0, 2, 0],
                 [0, 0, 2, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 1],
                 [0, 0, 1, 2, 0, 2, 1], [0, 0, 0, 0, 0, 0, 2],
                 [0, 0, 0, 0, 0, 0, 0]]

        gl = GameLogic(board)
        self.assertEqual(0, len(gl.scanBoard(gl.player, gl.opponent)))

    def test_scan_board_score_single_group(self):
        board = [[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 1, 2, 0, 0, 0], [0, 1, 2, 1, 0, 0, 0],
                 [0, 0, 1, 2, 0, 0, 0], [0, 0, 2, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0]]
        gl = GameLogic(board)
        self.assertEqual(1, len(gl.scanBoard(gl.player, gl.opponent)))

    def test_scan_board_score_multi_group(self):
        board = [[0, 0, 0, 0, 0, 0, 0], [0, 0, 1, 2, 0, 0, 0],
                 [0, 1, 2, 1, 0, 0, 0], [0, 1, 2, 1, 0, 0, 0],
                 [0, 0, 1, 2, 0, 0, 0], [0, 0, 2, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0]]
        gl = GameLogic(board)
        self.assertEqual(2, len(gl.scanBoard(gl.player, gl.opponent)))

    def test_scan_board_score_single_group_multi_position(self):
        board = [[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 1, 0, 0, 0],
                 [0, 0, 1, 2, 1, 0, 0], [0, 1, 2, 1, 0, 0, 0],
                 [0, 0, 1, 2, 0, 0, 0], [0, 0, 2, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0]]

        gl = GameLogic(board)
        self.assertEqual(2, len(gl.scanBoard(gl.player, gl.opponent)))

    def test_scan_board_score_multi_group_multi_position(self):
        board = [[0, 0, 0, 0, 0, 0, 0], [0, 0, 1, 2, 0, 0, 0],
                 [0, 1, 2, 1, 0, 0, 1], [0, 1, 2, 1, 0, 1, 2],
                 [0, 0, 1, 2, 0, 1, 2], [0, 0, 2, 0, 0, 2, 1],
                 [0, 0, 0, 0, 0, 2, 0]]
        gl = GameLogic(board)
        self.assertEqual(4, len(gl.scanBoard(gl.player, gl.opponent)))

    def test_update_board_suicide_rule(self):
        board = [[0 for i in range(0, 7)] for j in range(0, 7)]
        gl = GameLogic(board)
        gl.updateBoard(0, 0)
        gl.updateBoard(3, 1)
        gl.updateBoard(0, 1)
        gl.updateBoard(2, 2)
        gl.updateBoard(0, 2)
        gl.updateBoard(3, 3)
        gl.updateBoard(0, 3)
        gl.updateBoard(4, 2)

        with self.assertRaises(SuicideError):
            gl.updateBoard(3, 2)

    def test_is_ko_rule(self):
        board = [[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 1, 2, 0, 0, 0], [0, 1, 2, 0, 2, 0, 0],
                 [0, 0, 1, 2, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0]]
        gl = GameLogic(board)
        gl.updateBoard(3, 3)
        board = [[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 1, 2, 0, 0, 0], [0, 1, 0, 1, 2, 0, 0],
                 [0, 0, 1, 2, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0]]
        with self.assertRaises(KOError):
            gl.updateBoard(3, 2)

    def test_is_occupied_rule(self):
        board = [[0 for i in range(0, 7)] for j in range(0, 7)]
        gl = GameLogic(board)
        gl.updateBoard(0, 0)
        with self.assertRaises(OccupiedError):
            gl.updateBoard(0, 0)
