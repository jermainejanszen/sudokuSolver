import copy
import time
import threading
from imageParser import ImageParser

def generateBlankBoard():
    board = []
    row = [None]*9
    for i in range(9):
        i = i - 1
        board.append(copy.deepcopy(row))
    return copy.deepcopy(board)

class BoardThread(threading.Thread):
    board = None
    solved = False
    def __init__(self, board):
        super(BoardThread, self).__init__()
        self.board = copy.deepcopy(board)
    def run(self):
        self.solved = self.board.completeSolveHelper()
    def getSolved(self):
        return self.solved

class Board:
    mainBoard = generateBlankBoard()
    
    # Makes a new Board object given a 9x9 array of values
    def __init__(self, boardList=generateBlankBoard()):
        if len(boardList) == 9:
            if len(boardList[0]) == 9:
                self.mainBoard = copy.deepcopy(boardList)
    
    # Makes a new Board object given a string of 81 values
    @classmethod
    def fromString(newBoard, boardValues):
        newBoard = Board()
        inLength = len(boardValues)
        if inLength != 81:
            print("Given values not of right length.")
        else:
            for i in range(inLength):
                newBoard.mainBoard[i//9][i%9] = int(boardValues[i])
        return newBoard
    
    # Prints the board within a 9x9 grid
    def printBoard(self):
        print("+---+---+---+---+---+---+---+---+---+")
        printString = ""
        for i in range(81):
            if i != 0 and i%9 == 0:
                printString += "|\n"
                printString += "+---+---+---+---+---+---+---+---+---+\n"
            if self.mainBoard[i//9][i%9] != 0:
                printString += "| " + str(self.mainBoard[i//9][i%9]) + " "
            else:
                printString += "| " + "  "
        printString += "|\n+---+---+---+---+---+---+---+---+---+"
        print(printString)

    # Checks if a board is valid
    #   1. Has the numbers 1-9 within each 3x3 subgrid
    #   2. Has the numbers 1-9 within each row
    #   3. Has the numbers 1-9 within each column
    def checkValid(self, printErrors=True):
        # check if each sub grid has only one of each number
        for i in range(3):
            rows = self.mainBoard[i*3:i*3+3]
            for j in range(3):
                subgrid = []
                for k in range(3):
                    subgrid.append(rows[k][j*3:j*3+3])
                foundNumbers = []
                for row in subgrid:
                    for value in row:
                        if int(value) in foundNumbers:
                            if printErrors:
                                print("Same number appeared twice in one subgrid.")
                            return False
                        else:
                            if int(value) != 0:
                                foundNumbers.append(int(value))
        # check if each row has only one of each number
        for i in range(9):
            foundNumbers = []
            for j in range(9):
                if self.mainBoard[(i//3)*3 + i%3][j] in foundNumbers:
                    if printErrors:
                        print("Same number appeared twice in one row.")
                    return False
                else:
                    if self.mainBoard[(i//3)*3 + i%3][j] != 0:
                        foundNumbers.append(self.mainBoard[(i//3)*3 + i%3][j])
        # check if each column has only one of each number
        for i in range(9):
            foundNumbers = []
            for j in range(9):
                if self.mainBoard[j][i] in foundNumbers:
                    if printErrors:
                        print("Same number appeared twice in one column.")
                    return False
                else:
                    if self.mainBoard[j][i] != 0:
                        foundNumbers.append(self.mainBoard[j][i])
        return True

    # Checks if the board contains blank cells
    def isComplete(self):
        for i in range(len(self.mainBoard)):
            for j in range(len(self.mainBoard[0])):
                if int(self.mainBoard[i][j]) == 0:
                    return False
        return True
    
    # Solves a simple board where each step has at least one number that
    # can be certainly added
    # Returns True if solved, False otherwise
    def easySolve(self):
        # Check if board is cannot be solved
        if not self.checkValid():
            return False
        
        workingBoard = copy.deepcopy(self.mainBoard)
        # Build table of possible values
        minOptionsLen = 0
        while not Board(workingBoard).isComplete():
            if minOptionsLen > 1:
                return False
            minOptionsLen = 10
            # Find possible values
            for i in range(9):
                for j in range(9):
                    if int(workingBoard[i][j]) != 0:
                        continue
                    else:
                        cellValues = list(range(1, 10))
                        # check other values in row
                        for k in range(9):
                            try:
                                cellValues.remove(workingBoard[i][k])
                            except:
                                continue
                        # check other values in column
                        for k in range(9):
                            try:
                                cellValues.remove(workingBoard[k][j])
                            except:
                                continue
                        # check other values in subgrid
                        rows = workingBoard[(i//3)*3:(i//3)*3+3]
                        subgrid = []
                        for n in range(3):
                            n = n
                            subgrid.append(rows[n][(j//3)*3:(j//3)*3+3])
                        for row in subgrid:
                            for value in row:
                                if int(value) in cellValues:
                                    cellValues.remove(int(value))
                        if len(cellValues) < minOptionsLen:
                            minOptionsLen = len(cellValues)
                        if len(cellValues) == 1:
                            workingBoard[i][j] = int(cellValues[0])
        self.mainBoard = copy.deepcopy(workingBoard)
        return True

    def completeSolveHelper(self):
        workingBoard = copy.deepcopy(self.mainBoard)
        # Build table of possible values
        loopCounter = 0
        while not Board(workingBoard).isComplete():
            if loopCounter > 81:
                print("Unable to solve board.")
                return False

            # Find possible values
            filledACell = False
            currentMinOptionsCell = []
            currentMinOptionsCellSize = 10
            currentMinOptionsCellOptions = []
            for i in range(9):
                for j in range(9):
                    if int(workingBoard[i][j]) != 0:
                        continue
                    else:
                        cellValues = list(range(1, 10))
                        # check other values in row
                        for k in range(9):
                            try:
                                cellValues.remove(workingBoard[i][k])
                            except:
                                continue
                        # check other values in column
                        for k in range(9):
                            try:
                                cellValues.remove(workingBoard[k][j])
                            except:
                                continue
                        # check other values in subgrid
                        rows = workingBoard[(i//3)*3:(i//3)*3+3]
                        subgrid = []
                        for n in range(3):
                            n = n
                            subgrid.append(rows[n][(j//3)*3:(j//3)*3+3])
                        for row in subgrid:
                            for value in row:
                                if int(value) in cellValues:
                                    cellValues.remove(int(value))
                        if len(cellValues) == 1:
                            filledACell = True
                            workingBoard[i][j] = int(cellValues[0])
                        if not filledACell:
                            if len(cellValues) < currentMinOptionsCellSize:
                                currentMinOptionsCell = [i, j]
                                currentMinOptionsCellOptions = copy.deepcopy(cellValues)
                                currentMinOptionsCellSize = len(cellValues)
            if not filledACell:
                foundSolution = False
                threads = []
                for option in currentMinOptionsCellOptions:
                    testBoardValues = copy.deepcopy(workingBoard)
                    testBoardValues[currentMinOptionsCell[0]][currentMinOptionsCell[1]] = option
                    testBoard = Board(testBoardValues)
                    threads.append(BoardThread(testBoard))
                    threads[-1].start()
                for boardThread in threads:
                    boardThread.join()
                    if boardThread.getSolved():
                        foundSolution = True
                        workingBoard[currentMinOptionsCell[0]][currentMinOptionsCell[1]] = int(option)
                        break
                if not foundSolution:
                    return False
            loopCounter += 1
        self.mainBoard = copy.deepcopy(workingBoard)
        return True

    # Solves more difficult boards with multiple possibilities for values
    def completeSolve(self):
        solved = False
        if self.easySolve():
            solved = True
            return solved
        else:
            loopCounter = 0
            while not solved:
                if loopCounter > 81:
                    break
                solved = self.completeSolveHelper()
                loopCounter += 1
            return solved


doneBoard = Board.fromString("246857913189643275573291486418329567637485129952176348764532891321968754895714632")

boardToTest = "200007913180000275573291486400029567637400029952176348700032891320068700895714632"

newImageParser = ImageParser()

boardFromImage = newImageParser.imageToBoardString('testImage.jpg')

unsolvedBoard = Board.fromString(boardFromImage)

unsolvedBoard.printBoard()
didSolveHard = unsolvedBoard.completeSolve()
if didSolveHard:
    print('Solved:')
    unsolvedBoard.printBoard()
else:
    print('Unable to solve.')

