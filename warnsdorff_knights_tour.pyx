from timeit import default_timer as timer

class ChessBoard:
    """
    2D array representing a chess board. [y] [x] or [1] [a] positioning
    """
    def __init__(self, size):
        self.size = size
        self._board = [['0' for _ in range(size)] for _ in range(size)]

    def __str__(self):
        res = ''
        for y in range(self.size):
            for x in range(self.size):
                res  += str(self._board[x][y]) + ' '
            res += '\n'
        return res

    def __getitem__(self, index):
        return self._board[index]
    
    def placePiece(self, piece):
        position = piece.getPosition()
        self._board[position[0]][position[1]] = piece
    
    def markPos(self, pos):
        self._board[pos[0]][pos[1]] = '*'
    
    def unmarkPos(self, pos):
        self._board[pos[0]][pos[1]] = '0'

class Knight:
    def __init__(self, xPos, yPos):
        self._position = (xPos, yPos)
        self.validMoves = []
    
    def __str__(self):
        return 'K'

    def getValidMoves(self, board, pos):
        """Finds and returns an array of tuples representing the valid moves a knight can make
        from the given position."""
        validMoves = []  # array to store valid moves
        knightX, knightY = pos[0], pos[1]
        # check upper moves
        if (knightY-2 >= 0 and knightX+1 < board.size and board[knightX+1][knightY-2] == '0'):  # upper right
            validMoves.append((knightX+1, knightY-2))
        if (knightY-2 >= 0 and knightX-1 >= 0 and board[knightX-1][knightY-2] == '0'):  # upper left
            validMoves.append((knightX-1, knightY-2))

        # check lower moves
        if (knightY+2 < board.size and knightX+1 < board.size and board[knightX+1][knightY+2] == '0'):  # lower right
            validMoves.append((knightX+1, knightY+2))
        if (knightY+2 < board.size and knightX-1 >= 0 and board[knightX-1][knightY+2] == '0'):  # lower left
            validMoves.append((knightX-1, knightY+2))

        # check right moves
        if (knightY-1 >= 0 and knightX+2 < board.size and board[knightX+2][knightY-1] == '0'):  # right upper
            validMoves.append((knightX+2, knightY-1))
        if (knightY+1 < board.size and knightX+2 < board.size and board[knightX+2][knightY+1] == '0'):  # right upper
            validMoves.append((knightX+2, knightY+1))

        # check left moves
        if (knightY-1 >= 0 and knightX-2 >= 0 and board[knightX-2][knightY-1] == '0'):  # left upper
            validMoves.append((knightX-2, knightY-1))
        if (knightY+1 < board.size and knightX-2 >= 0 and board[knightX-2][knightY+1] == '0'):  # left lower
            validMoves.append((knightX-2, knightY+1))
        self.validMoves = validMoves
        return validMoves

    def setPosition(self, pos):
        self._position = pos
    
    def getPosition(self):
        return self._position

class KnightsTour:
    def __init__(self):
        self.chessBoard = None
        self.knight = None
        self.moveStk = []
        self.over = False
        self.endMoves = 0
    
    def moveKnight(self, pos):
        self.knight.setPosition(pos)  # set the knight's attributes
        self.chessBoard.placePiece(self.knight)  # move the knight to the new location
        self.knight.getValidMoves(self.chessBoard, self.knight.getPosition())  # generate the knight's valid moves
    
    def checkGameOver(self):
        if len(self.knight.validMoves) == 0:
            if len(self.moveStk) == self.endMoves:
                self.over = True
                return True

    def findSolution(self, pSolution):
        validMoves = self.knight.validMoves
        if self.checkGameOver():
            return pSolution

        # forms a rank table for the valid moves avaliable using Warndorff's rule
        heuristicOrder = [self.getHeuristic(e) for e in validMoves]

        # sorts the valid moves according to the rank table
        queuedMoves = [x for _, x in sorted(zip(heuristicOrder, validMoves))]

        for move in queuedMoves:  # try each valid move
            # make the move
            self.chessBoard.markPos(self.knight.getPosition()) 
            self.moveKnight(move)
            self.moveStk.append(move)  # push this move onto stack

            pSolution.append(move)
            # recursive call
            potentialSolution = self.findSolution(pSolution)
            if potentialSolution is not None:
                return potentialSolution

            # undo the move
            pSolution.pop()
            self.chessBoard.unmarkPos(self.moveStk.pop())  # pop and unmark the current move
            pos = self.moveStk[-1]  # get the previous move
            self.moveKnight(pos)  # move knight on the previous move

        # if we are here, the game is not over and we have no more moves
        return None
    
    def getHeuristic(self, position):
        return len(self.knight.getValidMoves(self.chessBoard, position))

    def start(self):
        print('========Knight\'s Tour========')
        boardSize = int(input('Enter the board size: '))
        self.chessBoard = ChessBoard(boardSize)
        self.endMoves = boardSize * boardSize
        print(self.chessBoard)
        pos = input('Enter the starting position of the knight: ').split()
        pos = (int(pos[0]), int(pos[1]))

        try:
            self.knight = Knight(pos[0], pos[1])  # place the knight
            self.chessBoard.placePiece(self.knight)  # place the knight on the board
            self.knight.getValidMoves(self.chessBoard, self.knight.getPosition())  # generate the knight's valid moves
            self.moveStk.append(pos)  # push the starting move onto the stack
        except Exception as e:  # invalid position entered!
            print(e)
    
    def printMenu(self):
        print()
        print(self.chessBoard)
        print('============================')
        print('Valid Moves: ' + str(self.knight.validMoves))
        print('============================')
        print(('Enter option:'))

    def nextOption(self):
        choice = input()
        if choice == "Solution":
            start = timer()
            solution = self.findSolution([])
            print('Solution: ' + str(solution))
            print('Moves: ' + str(len(solution)))
            print('Time taken: ' + str(timer() - start))
        elif choice == 'Undo':
            if len(self.moveStk) > 1:
                self.chessBoard.unmarkPos(self.moveStk.pop())  # pop and unmark the current move
                pos = self.moveStk[-1]  # get the previous move
                self.moveKnight(pos)  # move knight on the previous move
            else:
                print('No moves to undo!')
        else:
            try:
                choice = choice.split()
                move = (int(choice[0]), int(choice[1]))
                if move in self.knight.validMoves:
                    self.chessBoard.markPos(self.knight.getPosition()) 
                    self.moveKnight(move)
                    self.moveStk.append(move)  # push this move onto stack
                else:
                    print('Invalid Move!')
            except Exception as e:  # invalid option entered!
                print(e)
        # check if game is over
        self.checkGameOver()


if __name__ == '__main__':
    game = KnightsTour()

    game.start()

    while not game.over:
        game.printMenu()
        game.nextOption()
    
    print(game.chessBoard)
    print('YOU WIN!')
