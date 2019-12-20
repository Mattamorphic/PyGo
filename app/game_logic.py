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
    SKIP_LIMIT = 2

    def __init__(self, board):
        # If a board isn't created, then fail
        if not board:
            raise ValueError(
                "Board must be a list of lists of equal dimensions")
        # Create copy of the board (we need to ensure this isn't by reference)
        self.startingBoard = self.copyBoard(board)
        # Reset the logic
        self.reset()

    def getPlayer(self):
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
        # Create a copy of the board and store this
        self.board = self.copyBoard(self.startingBoard)
        # Set the heigh / width based on the dimensions of this
        self.height, self.width = len(self.startingBoard) - 1, len(
            self.startingBoard[0]) - 1
        # Set a skip counter
        self.skipCount = 0
        # Store previous instances of the board
        self.previousBoards = []
        # Store the players
        self.players = {
            Piece.White: Player("White", (255, 255, 255)),
            Piece.Black: Player("Black", (0, 0, 0))
        }
        # Set the current players
        self.player = Piece.White
        self.opponent = Piece.Black

    def skip(self):
        '''
            Allow a player to skip there go
        '''
        # Increment the skip counter
        self.skipCount += 1
        # Check to see if we have hit the skip limit
        if self.skipCount >= self.SKIP_LIMIT:
            # If we have, raise a game over
            raise GameOverPassError()
        # Switch player and opponent
        self.switchPlayers()

    def copyBoard(self, board):
        '''
            Create a copy of the board, without reference. Nested lists cause
            issues on direct assignment

            Args:
                board (list): Board

            Returns:
                list
        '''
        return [list(row) for row in board]

    def updateBoard(self, row, col):
        '''
            Update the board

            Args:
                board (list): Update the board

            Returns:
                List
        '''
        # A turn has taken place, so reset the skip counter
        self.skipCount = 0
        # Is this space occupied?
        if self.board[row][col] == self.opponent:
            raise OccupiedError()
        # Update the board, and store a copy of the original
        self.previousBoards.append(self.copyBoard(self.board))
        # Make the move
        self.board[row][col] = self.player
        # Scan the board for pieces and dead pieces
        for row, col in self.getRemovedPieces(self.player, self.opponent):
            self.board[row][col] = Piece.NoPiece

        # Is this a KO instance?
        if self.isKoRule():
            self.board = self.previousBoards.pop()
            raise KOError()

        # Remove any pieces for the opponent side
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
        # Players current piece count (used for suicide rule checks)
        self.players[self.player].setPieces(playerPieceCount)
        # Players current score
        self.players[self.player].setScore(
            self.getCapturedLandCount(self.player) + playerPieceCount)
        # Opponents current piece count (used for suicide rule checks)
        self.players[self.opponent].setPieces(opponentPieceCount)
        # Opponents current score
        self.players[self.opponent].setScore(
            self.getCapturedLandCount(self.opponent) + opponentPieceCount)

        # Turn over, switch players
        self.switchPlayers()
        # Return the latest board
        return self.board

    def isKoRule(self):
        '''
            Is the KO rule in effect

            Returns:
                Bool
        '''
        # If there haven't been two turns, then there's no chance of this
        if len(self.previousBoards) < 2:
            return False
        # Compare the last player turn with this player turn
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
        # A store for our opponents
        opponentsToCheck = []
        # Nested loop through the board matrix
        for row in range(0, self.height + 1):
            for col in range(0, self.width + 1):
                # If this is an opponent, then add it to the list
                if self.board[row][col] == opponent:
                    opponentsToCheck.append((row, col))
        # Return the list
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
        # Return a list of indexes as tuples around the given matrix position
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
        # Create a list to store dead pieces
        deadPieces = []
        # Get the opponent positions as a list of tuples representing vertices
        opponentPositions = self.getPositions(opponent)
        # If this is empty, then return an empty list
        if not opponentPositions:
            return []
        # Store any checked positions to prevent infinite loops
        checked = []
        # Iterate through each opponent position
        for opponentPosition in opponentPositions:
            # If this has been previously checked, skip ahead
            if opponentPosition in checked:
                continue
            # Add this to our checked list
            checked.append(opponentPosition)
            # Create a bucket for pieces in this group starting with
            # the current position, this will be emptied
            opponentGroup = [opponentPosition]
            # Create a list to store all adjacents around this group
            adjacentSpots = []
            # This will be filled with the group
            group = [opponentPosition]
            # while we have pieces in the opponent group bucket
            while opponentGroup:
                # Get the last elementgit
                position = opponentGroup.pop()
                # Get the adjacents for this piece
                for adjacent in self.getAdjacents(*position):
                    # Check the adjacent
                    if (
                            # If it's already been added into the bucket
                            adjacent in opponentGroup
                            # If it's already an adjacent
                            or adjacent in adjacentSpots
                            # if it's been checked previously
                            or adjacent in checked):
                        continue
                    # If this adjacent has the opponent piece...
                    if self.hasSpecificPiece(opponent, *adjacent):
                        # We need to check this for adjacents
                        opponentGroup.append(adjacent)
                        # This is part of the group
                        group.append(adjacent)
                        # This piece will be checked so don't check twice
                        checked.append(adjacent)
                    else:
                        # Else this is an adjacent that we need to see
                        # if the player is covering
                        adjacentSpots.append(adjacent)
            if self.areAdjacentsCovered(player, adjacentSpots):
                # If all adjacents are covered, then these are dead pieces
                deadPieces += group
        # Return the dead pieces to be removed
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
            raise IndexError("list index out of range")

    '''
        Get the player with the highest score

        Returns:
            Player
    '''
    def getLeadingPlayer(self):
        winner = self.players[Piece.White]
        for id, player in self.players.items():
            if player.getScore() > winner.getScore():
                winner = player
        return winner


class Player:
    '''
        Represent a player

        Args:
            name (str): The name for the player
    '''
    TIMER = 120

    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.reset()

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

    def deductTimeRemaining(self, time):
        self.timeRemaining -= time

    def getColor(self):
        return self.color

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

    def getName(self):
        return self.name

    def getTimeRemaining(self):
        return self.timeRemaining

    def hasTimeLeft(self):
        return self.timeRemaining > 0

    def reset(self):
        '''
            Reset the attributes
        '''
        self.score = 0
        self.pieces = 0
        self.timeRemaining = self.TIMER


class GameOverPassError(Exception):
    '''
        Custom exception class for GameOverPassError
    '''
    pass


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
