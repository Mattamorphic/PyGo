'''
    Handles the game logic
'''
from .piece import Piece


class GameLogic:
    def __init__(self, board):
        self.board = board
        self.height, self.width = len(board) - 1, len(board[0]) - 1

        self.players = {
            Piece.White: Player("White"),
            Piece.Black: Player("Black")
        }
        self.currentPlayer = Piece.White
        self.otherPlayer = Piece.Black

    def getCurrentPlayer(self):
        '''
            Returns the current player

            Returns:
                Player
        '''
        return self.currentPlayer

    def getPlayers(self):
        '''
            Returns the players

            Returns:
                dict
        '''
        return self.players

    def reset(self):
        '''
            Reset the players
        '''
        for colour, player in self.players.items():
            player.reset()

    def updateBoard(self, board):
        '''
            Update the board

            Args:
                board (list): Update the board
        '''
        # Get the current count of player pieces on the board
        playerPieceCountBeforeGo = len(self.getPositions(self.currentPlayer))

        # Make a backup of the board
        currentBoard = self.board

        # Set our new board
        self.board = board

        # Scan the board for pieces and dead pieces
        _, opponentRemovedPieces = self.scanBoard(self.currentPlayer,
                                                  self.otherPlayer)
        _, playerRemovedPieces = self.scanBoard(self.otherPlayer,
                                                self.currentPlayer)

        playerScore, _ = self.scanBoard(self.currentPlayer, 0)
        opponentScore, _ = self.scanBoard(self.otherPlayer, 0)

        for row, col in opponentRemovedPieces + playerRemovedPieces:
            self.board[row][col] = Piece.NoPiece

        playerPieceCountAfterGo = len(self.getPositions(self.currentPlayer))
        # Check to see if this was a runtime error
        if playerPieceCountAfterGo < playerPieceCountBeforeGo:
            raise RuntimeError("Suicide rule")

        self.players[self.currentPlayer].setScore(playerScore)
        self.players[self.otherPlayer].setScore(opponentScore)
        (self.currentPlayer,
         self.otherPlayer) = self.otherPlayer, self.currentPlayer
        return self.board

    def getBoard(self):
        return self.board

    def getPositions(self, opponent):
        '''
            Get the opponents to check

            Returns:
                List
        '''
        opponentsToCheck = []
        for row in range(0, self.height + 1):
            for col in range(0, self.width + 1):
                if self.board[row][col] == opponent:
                    opponentsToCheck.append((row, col))
        return opponentsToCheck

    def getAdjacents(self, row, col):
        '''
            Get the adjacent pieces as a list (if they are valid)

            Args:
                row         (int): The current row
                col         (int): The current col

            Returns:
                List
        '''
        return [
            adjacent
            for adjacent in [(row, col - 1) if col > 0 else None, (
                row - 1, col) if row > 0 else None, (
                    row + 1, col) if row < self.height else None, (
                        row, col + 1) if col < self.width else None]
            if adjacent
        ]

    def scanBoard(self, player, opponent):
        '''
            Scan the board and determine the current score for the player

            Returns:
                int
        '''
        # Find all of the opponent positions on the board and iterate
        deadPieces = []
        opponentPositions = self.getPositions(opponent)
        if not opponentPositions:
            return 0, []
        checked = []
        score = 0
        for i, opponentPosition in enumerate(opponentPositions):
            if opponentPosition in checked:
                continue
            checked.append(opponentPosition)
            opponentGroup = [opponentPosition]
            adjacentSpots = []
            group = [opponentPosition]
            # while we have pieces in the opponent group
            while opponentGroup:
                position = opponentGroup.pop()
                # let's keep looking for adjacents
                # for each of the adjacent positions
                for adjacent in self.getAdjacents(*position):
                    if (
                            # If it's already been added into the bucket
                            adjacent in opponentGroup
                            # If it's already an adjacent
                            or adjacent in adjacentSpots
                            # if it's been checked previously
                            or adjacent in checked):
                        continue
                    # if this doesn't include the player,
                    # store this in the bucket (if we don't have it)
                    if self.hasSpecificPiece(opponent, *adjacent):
                        opponentGroup.append(adjacent)
                        group.append(adjacent)
                        checked.append(adjacent)
                    else:
                        adjacentSpots.append(adjacent)
            if self.areAdjacentsCovered(player, adjacentSpots):
                score += len(group)
                deadPieces += group

        return score, deadPieces

    def areAdjacentsCovered(self, player, adjacents):
        '''
            Determine if all the adjacetns are covered

            Args:
                piece       (int):  The piece to check
                adjacents   (list): The adjacents to check

            Returns:
                bool
        '''
        for adjacent in adjacents:
            if not self.hasSpecificPiece(player, *adjacent):
                return False
        return True

    def hasSpecificPiece(self, piece, row, col):
        '''
            Check if a specific piece is at the position on the board

            Args:
                piece   (int): The piece to check
                row     (int): The row on the board
                col     (int): The col on the board

            Returns:
                bool
        '''
        try:
            return self.board[row][col] == piece
        except IndexError:
            print(row, col)
            raise IndexError("list index out of range")

    @staticmethod
    def testLogic():
        board = [[0, 0, 0, 1, 2, 1, 0], [0, 0, 0, 0, 1, 0, 0],
                 [0, 0, 0, 0, 0, 2, 0], [0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0]]

        logic = GameLogic(board)
        print('\n'.join(
            ['\t'.join([str(cell) for cell in row]) for row in board]))
        # blackScore = logic.scanBoard(Piece.Black, Piece.White)
        # print(f"Black: {blackScore}")
        whiteScore = logic.scanBoard(Piece.White, Piece.Black)
        print(f"White: {whiteScore}")


class Player:
    def __init__(self, name):
        self.name = name
        self.score = 0

    def setScore(self, score):
        self.score = score

    def getScore(self):
        return self.score

    def reset(self):
        self.score = 0
