'''
    Handles the game logic
'''
from .piece import Piece


class GameLogic:
    '''
        GameLogic controls the scoring and rules of the game

        Args:
            board (list): The board matrix

    '''
    def __init__(self, board):
        if not board:
            raise ValueError(
                "Board must be a list of lists of equal dimensions")
        self.startingBoard = board
        self.reset()

    def getplayer(self):
        '''
            Returns the current player

            Returns:
                Player
        '''
        return self.player

    def getPlayers(self):
        '''
            Returns the players

            Returns:
                Dict
        '''
        return self.players

    def reset(self):
        '''
            Reset the game
        '''
        self.board = self.startingBoard
        self.height, self.width = len(self.startingBoard) - 1, len(
            self.startingBoard[0]) - 1
        self.previousBoards = []
        self.players = {
            Piece.White: Player("White"),
            Piece.Black: Player("Black")
        }
        self.player = Piece.White
        self.opponent = Piece.Black

    def updateBoard(self, row, col):
        '''
            Update the board

            Args:
                board (list): Update the board

            Returns:
                List
        '''
        # is this space occupied?
        if self.board[row][col] == self.opponent:
            raise OccupiedError()
        # Update the board, and store a copy of the original
        self.previousBoards.append([list(row) for row in self.board])
        self.board[row][col] = self.player
        # Scan the board for pieces and dead pieces
        for row, col in self.getRemovedPieces(self.player, self.opponent):
            self.board[row][col] = Piece.NoPiece
        # Board backup
        if self.isKoRule():
            self.board = self.previousBoards.pop()
            raise KOError()

        for row, col in self.getRemovedPieces(self.opponent, self.player):
            self.board[row][col] = Piece.NoPiece

        # Get the piece count after removing piecees
        playerPieceCount = len(self.getPositions(self.player))
        opponentPieceCount = len(self.getPositions(self.opponent))

        # Check if the player has hit the suicide rule
        if self.isSuicideRule(playerPieceCount):
            self.board = self.previousBoards.pop()
            raise SuicideError()

        # Update the players
        self.players[self.player].setPieces(playerPieceCount)
        self.players[self.player].setScore(
            self.getCapturedLandCount(self.player) + playerPieceCount)
        self.players[self.opponent].setPieces(opponentPieceCount)
        self.players[self.opponent].setScore(
            self.getCapturedLandCount(self.opponent) + opponentPieceCount)

        self.switchPlayers()
        return self.board

    def isKoRule(self):
        '''
            Is the KO rule in effect

            Returns:
                Bool
        '''
        if len(self.previousBoards) < 2:
            return False
        return self.previousBoards[-2] == self.board

    def isSuicideRule(self, newPieceCount):
        '''
            Is the suicide rule in effect

            Returns:
                Bool
        '''
        return self.players[self.player].getPieces() >= newPieceCount

    def switchPlayers(self):
        '''
            Swap the players
        '''
        (self.player, self.opponent) = self.opponent, self.player

    def getRemovedPieces(self, player, opponent):
        '''
            Find the taken pieces to remove

            Args:
                player     (Piece): The player
                opponent   (Piece): The opponent

            Returns:
                List
        '''
        return self.scanBoard(player, opponent)

    def getCapturedLandCount(self, player):
        '''
            Get the score for the player

            Args:
                player      (Piece): The player
                pieceCount  (int):   The current pieces

            Returns:
                Int
        '''
        return len(self.scanBoard(player, Piece.NoPiece))

    def getBoard(self):
        '''
            Return the board

            Returns:
                List
        '''
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
                list
        '''
        # Pieces that will need removing
        deadPieces = []
        opponentPositions = self.getPositions(opponent)
        if not opponentPositions:
            return []
        checked = []
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
                deadPieces += group

        return deadPieces

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


class Player:
    '''
        Represent a player

        Args:
            name (str): The name for the player
    '''
    def __init__(self, name):
        self.name = name
        self.score = 0
        self.pieces = 0

    def setScore(self, score):
        '''
            Setter for the score attribute

            Args:
                score (int): The new score
        '''
        self.score = score

    def setPieces(self, pieces):
        '''
            Setter for the piece count attribute

            Args:
                pieces (int): The new pieces
        '''
        self.pieces = pieces

    def getScore(self):
        '''
            Getter for the score attribute

            Returns:
                Int
        '''
        return self.score

    def getPieces(self):
        '''
            Getter for the pieces count attribute

            Returns:
                Int
        '''
        return self.pieces

    def reset(self):
        '''
            Reset the attributes
        '''
        self.score = 0
        self.pieces = 0


class KOError(Exception):
    '''
        Custom exception class for KOError
    '''
    pass


class SuicideError(Exception):
    '''
        Custom exception class for SuicideError
    '''
    pass


class OccupiedError(Exception):
    '''
        Custom exception class for OccupiedError
    '''
    pass
