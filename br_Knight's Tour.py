import timeit
import referential_array

class Node:
    def __init__(self, item, next):
        self.item = item
        self.next = next

def __str__(self):
    return str(self.item)

class array:
    def __init__(self, size):
        assert size > 0, "size should be positive"
        self.array = referential_array.build_array(size)
        self.count = 0
        self.size = size

    def __len__(self):
        return self.count

    def is_empty(self):
        return self.count == 0

    def is_full(self):
        return self.count == self.size
    
    def add(self, item):
        if not self.is_full():
            self.array[self.count] = item
            self.count += 1

    def delete(self, index):
        valid_index = index >= 0 and index < self.count
        if (valid_index):
            for i in range(index, self.count-1):
                self.array[i] = self.array[i+1]
            self.count -= 1
            
    def print(self):
        for i in range(self.count):
            print(self.array[i], end = " ")
        print()

    def __contains__(self, item):
        for i in range(self.count):
            if self.array[i] == item:
                return True
        return False

class Stack:
    def __init__(self):
        self.top = None
        self.count = 0

    def is_empty(self):
        if self.count:
            return False
        else:
            return True

    def push(self, item):
        self.top = Node(item, self.top)
        self.count += 1

    def pop(self):
        assert not self.is_empty(), "stack is empty"
        item = self.top.item
        self.top = self.top.next
        self.count -= 1
        return item

    def to_list(self):
        res = []
        current = self.top
        while current is not None:
            res.append(current.item)
            current = current.next
        return res

    def __str__(self):
        res = ""
        current = self.top
        while current is not None:
            res += str(current.item) + ", "
            current = current.next
        return res

    def __contains__(self, item):
        current = self.top
        while current is not None:
            if current.item == item:
                return True
            current = current.next
        return False

    def __len__(self):
        return self.count

class Tour:
    def __init__(self, size = 8):
        """
        Initialize instance variables
        Pre-condition: None
        Post-condition: Tour object created
        Args:
            None
        Returns:
            None
        Complexity:
        Best-case = Worst-case = O(1)
        This function has a constant time complexity
        """

        self.size = size
        self.board = [[0 for x in range(size)] for y in range(size)]
        self.knight = [None, None]
        self.previousMoves = Stack()
        self.startPos = [None, None]
        self.endPos = []

    def clearBoard(self):
        """
        Clears board to all "0"s
        Pre-condition: A tour object has been created
        Post-condition: self.board is fully occupied by "0"s
        Args:
            None
        Returns:
            None
        Complexity:
        Best-case = Worst-case = O(1)
        Since size of board is fixed, this function has constant complexity
        """
        
        self.board = [[0 for x in range(self.size)] for y in range(self.size)]

    def clearKnight(self):
        """
        Resets position of knight to [None, None]
        Pre-condition: A tour object has been created
        Post-condition: self.knight has value of [None, None]
        Args:
            None
        Returns:
            None
        Complexity:
        Best-case = Worst-case = O(1)
        Constant complexity
        """
        
        self.knight = [None, None]

    def clearPreviousMoves(self):
        """
        Clears the stack of previous moves
        Pre-condition: A tour object has been created
        Post-condition: self.previousMoves will be an empty stack
        Args:
            None
        Returns:
            None
        Complexity:
        Best-case = Worst-case = O(1)
        Since __init__ of stack object is O(1), this function's complexity
        is also O(1)
        """
        
        self.previousMoves = Stack()

    def printBoard(self):
        """
        Prints board, x (left to right), y (up to down)
        Pre-condition: A tour object has been created
        Post-condition: Current board will be printed
        Args:
            None
        Returns:
            None
        Complexity:
        Best-case = Worst-case = O(1)
        Since size of board is constant (8x8) the time complexity to print
        the board is also constant
        """
        
        for y in range(len(self.board)):
            temp = ""
            for x in range(len(self.board[y])):
                temp += str(self.board[x][y]) + " "
            print(temp)
        print()

    def placeKnight(self, knight_pos):
        """
        Marks current position with "*" and then moves knight to position
        indicated by knight_pos. Then marks knight_pos with "K"
        Pre-condition: A tour object is created
        Post-condition: self.knight will contain knight_pos, the previous
                        position of the knight will be pushed onto stack
                        'previousMoves'. The previous and current position
                        of the knight will be '*' and 'K' respectively on
                        the board
        Args:
            List of length 2, knight_pos, containing [x coordinate, y coordinate]
            x and y must be < self.size and > 0
        Returns:
            None
        Complexity:
        Best-case = Worst-case = O(1)

        """
        
        if self.knight[0] is not None and self.knight[1] is not None:
            self.board[self.knight[0]][self.knight[1]] = "*"
            # pushes old position onto stack
            self.previousMoves.push([self.knight[0], self.knight[1]])
        self.knight = knight_pos # updates position of knight
        self.board[self.knight[0]][self.knight[1]] = "K"

    def undo(self):
        """
        Marks current position with "0" and then pop previous move from
        stack. Then moves knight to popped position, and marks position with
        "K"
        Pre-condition: A tour object has been created
        Post-condition: The current position of self.knight will be remarked
                        as '0'. The previous position will be popped off stack
                        and marked with 'K'
        Args:
            None
        Returns:
            None
        Complexity:
        Best-case = Worst-case = O(1)

        
        """
        
        if self.previousMoves.is_empty():
            print("No moves to undo")
        else:
            self.board[self.knight[0]][self.knight[1]] = "0"
            previous = self.previousMoves.pop()  # pop previous position
            self.knight = previous  # moves knight to previous position
            self.board[self.knight[0]][self.knight[1]] = "K"  # mark with "K"

    def next_moves(self, knight_pos):
        """
        Returns the next possible moves made by a knight from knight_pos
        Pre-condition: A tour object has been created
        Post-condition: None
        Args:
            List of length 2, knight_pos, containing (x coordinate, y coordinate)
        Returns:
            array of length 8, containing lists of length 2 representing
            possible squares for a knight to move to on a 8x8 board, not
            including squares contained in self.previousMoves
        Complexity:
        Best-case = Worst-case = O(1)
        The function always calculates the 8 possible moves of a knight and then
        decides whether the move is valid
        """
        
        knight_moves = [[-2,-1],[-2,1],[2,-1],[2,1],[-1,2],[1,2],[-1,-2],[1,-2]]
        nextMoves = array(self.size)

        for i in range(len(knight_moves)):
          check = [knight_pos[0] + knight_moves[i][0], knight_pos[1] + knight_moves[i][1]]
          if check[0] < self.size and check[0] >= 0:  # check x value within board
            if check[1] < self.size and check[1] >= 0:  # check y value within board
              if check not in self.previousMoves:  # check square not visited
                nextMoves.add(check)

        return nextMoves

    def winCheck(self):
        """
        Check if all squares have been visited and knight can jump back
        to starting square as the final move. In other words, check if the
        game is won.
        Pre-condiion: A tour object has been created
        Post-condition: None
        Args:
            None
        Returns:
            Boolean, True if game is won, False if game is not won
        Complexity:
        Best-case = O(1) - if knight_pos is the first item in endPos
        Worst-case = O(n) - if knight_pos is the last item in endPos, or
                            knight_pos is not in endPos
        n = length of endPos
        """
        
        if len(self.previousMoves) >= 63:
            if self.knight in self.endPos:
                return True
        return False

    def findSolution(self):
        """
        Returns remaining moves to solve the puzzle and time taken to find
        the solution
        Pre-condition: A tour object has been created, self.knight is not
                       [None, None]
        Post-condition: None
        Args:
            None
        Returns:
            List solution containing lists of length 2 containing positions
            of knight in order to solve the puzzle from the point of calling
            Float time_taken contains the time taken for
            self.findSolutionHelper([]) to run
        Complexity:
        x.x
        
        """
        
        start = timeit.default_timer()
        solution = self.findSolutionHelper([])
        time_taken = timeit.default_timer() - start
        if solution:
            return solution, time_taken
        else:
            return None, time_taken
        
    def findSolutionHelper(self, pSolution):
        """
        Helper function for findSolution(self). Recursively tries possible
        moves until winning continuation is found
        Pre-condition: A tour object has been created, self.knight is not
                       [None, None]
        Post-condition: pSolution contains the remaining steps to solve the
                        puzzle
        Args:
            List pSolution, list to store the solution to the puzzle
        Returns:
            List containing solution to the puzzle, or None if no solution
            is found
        Complexity:
        x.x
        
        """
        
        nextMoves = self.next_moves(self.knight)

        # if not won, try each next move
        if self.winCheck():
            # make a copy of previousMoves
            pSolution.insert(0, self.startPos)  # add start position as final move
            return pSolution  # return solution as list
        else:
            for trial in range(len(nextMoves)):
                self.placeKnight(nextMoves.array[trial])
                pSolution.insert(0, nextMoves.array[trial])
                foundFlag = self.findSolutionHelper(pSolution)
                self.undo()
                if foundFlag:
                    return foundFlag
                pSolution.pop(0)
        return None

if __name__ == "__main__":
    
    brd = Tour(8)  # 8x8 chess board

    while True:

        # print current board and menu
        brd.printBoard()
        print("Menu")
        print("********")
        print("1. Start new game")
        print("2. Next Positions")
        print("3. Solution")
        print("4. Undo")
        print("5. Quit")
        choice = input()  # get menu choice from user

        if choice == "1":  # start new game
            # reset game
            brd.clearBoard()
            brd.clearKnight()
            brd.clearPreviousMoves()
            print()
            
            print("Enter starting position (x y separated by space): ")  # get starting position
            try:
                x, y = input().strip().split()
                x, y = int(x), int(y)
                brd.startPos = [x, y]
                brd.endPos = brd.next_moves(brd.startPos)  # get valid ending positions
                brd.placeKnight(brd.startPos)  # move knight to starting position
            except ValueError:  # if input is not of correct format
                print("Invalid entry")
            except IndexError:  # if input is out of range of board(8x8)
                print("Position is out of range of board")

        elif choice == "2":  # continue with next moves
            if brd.knight[0] is not None and brd.knight[1] is not None:
                nextMoves = brd.next_moves(brd.knight)  # get list of possible moves
                if not nextMoves.is_empty():
                    print("Next moves:")
                    nextMoves.print()
                    try:
                        print("Enter next position (x y separated by space):")
                        x, y = input().strip().split()  # get input
                        x, y = int(x), int(y)
                        if [x, y] in nextMoves:  # check if move is legal
                            brd.placeKnight([x, y])
                            if brd.winCheck():  # check if game is won
                                brd.printBoard()
                                print("Winn3r!")
                                break
                        else:  # if illegal move is attempted
                            print("That is not a legal move")
                    except ValueError:  # if input is not of the correct format
                        print("Invalid entry")
                    except IndexError:  # if input is out of range of board(8x8)
                        print("Position is out of range of board")
                else:
                    print("No next moves")

        elif choice == "3":  # find solution
            if brd.knight[0] is not None and brd.knight[1] is not None:
                solution, time_taken = brd.findSolution()
                if solution:  # if solution is found
                    print(solution)
                    print("Time taken: " + str(time_taken) + " seconds")
                else:  # if no solution is found
                    print("No solution found")
                    print("Time taken: " + str(time_taken) + " seconds")
            else:
                print("Cannot solve from empty position")

        elif choice == "4":  # undo last move
            brd.undo()

        elif choice == "5":  # quit
            break

        else:
            print("Invalid option")
 
        
