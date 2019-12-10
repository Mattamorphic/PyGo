from app.game_logic import GameLogic
from app.piece import Piece

import unittest


class TestGameLogic(unittest.TestCase):
    def test_instantiation_of_game_logic(self):
        gl = GameLogic([[0]])
        self.assertTrue(gl.getCurrentPlayer() == Piece.White)

    def test_get_opponent_positions_empty_board(self):
        board = [[0 for i in range(0, 7)] for j in range(0, 7)]
        gl = GameLogic(board)
        self.assertListEqual([], gl.getPositions(gl.otherPlayer))

    def test_get_opponent_positions_with_pieces(self):
        board = [[0, 0, 0, 1, 2, 1, 0], [0, 0, 0, 0, 1, 0, 0],
                 [0, 0, 0, 0, 0, 2, 0], [0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0]]

        gl = GameLogic(board)
        self.assertListEqual([(0, 4), (2, 5)], gl.getPositions(gl.otherPlayer))

    def test_get_opponent_positions_with_pieces_at_edges(self):
        board = [[2, 0, 0, 0, 0, 0, 2], [0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0],
                 [2, 0, 0, 0, 0, 0, 2]]

        gl = GameLogic(board)
        self.assertListEqual([(0, 0), (0, 6), (6, 0), (6, 6)],
                             gl.getPositions(gl.otherPlayer))

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
        self.assertTrue(gl.hasSpecificPiece(gl.getCurrentPlayer(), 0, 3))

    def test_doesnt_have_specific_piece(self):
        board = [[0, 0, 0, 1, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0]]

        gl = GameLogic(board)
        self.assertFalse(gl.hasSpecificPiece(gl.getCurrentPlayer(), 0, 2))

    def test_has_adjacents_covered_single_group(self):
        board = [[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 1, 0, 0, 0],
                 [0, 0, 1, 2, 1, 0, 0], [0, 0, 0, 1, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0]]

        gl = GameLogic(board)
        opponent = gl.getPositions(gl.otherPlayer).pop()
        self.assertTrue(
            gl.areAdjacentsCovered(gl.currentPlayer,
                                   gl.getAdjacents(*opponent)))

    def test_doesnt_have_adjacents_covered_single_group(self):
        board = [[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 1, 0, 0, 0, 0], [0, 1, 2, 0, 0, 0, 0],
                 [0, 0, 1, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0]]

        gl = GameLogic(board)
        opponent = gl.getPositions(gl.otherPlayer).pop()
        self.assertFalse(
            gl.areAdjacentsCovered(gl.currentPlayer,
                                   gl.getAdjacents(*opponent)))

    def test_has_adjacents_covered_single_group_edge(self):
        board = [[0, 0, 1, 2, 1, 0, 0], [0, 0, 0, 1, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0]]

        gl = GameLogic(board)
        opponent = gl.getPositions(gl.otherPlayer).pop()
        self.assertTrue(
            gl.areAdjacentsCovered(gl.currentPlayer,
                                   gl.getAdjacents(*opponent)))

    # def test_has_adjacents_covered_multi_group:
    #     pass

    def test_scan_board_empty(self):
        board = [[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0]]

        gl = GameLogic(board)
        self.assertEqual(0, gl.scanBoard(gl.currentPlayer, gl.otherPlayer)[0])

    def test_scan_board_no_score(self):
        board = [[0, 0, 1, 1, 2, 1, 2], [0, 0, 2, 2, 0, 2, 0],
                 [0, 0, 2, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 1],
                 [0, 0, 1, 2, 0, 2, 1], [0, 0, 0, 0, 0, 0, 2],
                 [0, 0, 0, 0, 0, 0, 0]]

        gl = GameLogic(board)
        self.assertEqual(0, gl.scanBoard(gl.currentPlayer, gl.otherPlayer)[0])

    def test_scan_board_score_single_group(self):
        board = [[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 1, 2, 0, 0, 0], [0, 1, 2, 1, 0, 0, 0],
                 [0, 0, 1, 2, 0, 0, 0], [0, 0, 2, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0]]
        gl = GameLogic(board)
        self.assertEqual(1, gl.scanBoard(gl.currentPlayer, gl.otherPlayer)[0])

    def test_scan_board_score_multi_group(self):
        board = [[0, 0, 0, 0, 0, 0, 0], [0, 0, 1, 2, 0, 0, 0],
                 [0, 1, 2, 1, 0, 0, 0], [0, 1, 2, 1, 0, 0, 0],
                 [0, 0, 1, 2, 0, 0, 0], [0, 0, 2, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0]]
        gl = GameLogic(board)
        self.assertEqual(2, gl.scanBoard(gl.currentPlayer, gl.otherPlayer)[0])

    def test_scan_board_score_single_group_multi_position(self):
        board = [[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 1, 0, 0, 0],
                 [0, 0, 1, 2, 1, 0, 0], [0, 1, 2, 1, 0, 0, 0],
                 [0, 0, 1, 2, 0, 0, 0], [0, 0, 2, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0]]

        gl = GameLogic(board)
        self.assertEqual(2, gl.scanBoard(gl.currentPlayer, gl.otherPlayer)[0])

    def test_scan_board_score_multi_group_multi_position(self):
        board = [[0, 0, 0, 0, 0, 0, 0], [0, 0, 1, 2, 0, 0, 0],
                 [0, 1, 2, 1, 0, 0, 1], [0, 1, 2, 1, 0, 1, 2],
                 [0, 0, 1, 2, 0, 1, 2], [0, 0, 2, 0, 0, 2, 1],
                 [0, 0, 0, 0, 0, 2, 0]]
        gl = GameLogic(board)
        self.assertEqual(4, gl.scanBoard(gl.currentPlayer, gl.otherPlayer)[0])

    def test_update_board_suicide_rule(self):
        board = [[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 1, 2, 0, 0, 0], [0, 1, 0, 1, 2, 0, 0],
                 [0, 0, 1, 2, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0]]
        gl = GameLogic(board)
        board[3][2] = gl.getCurrentPlayer()
        with self.assertRaises(RuntimeError):
            gl.updateBoard(board)
