#! /usr/bin/python

#  Example program to try and solve sudoku, from loading a text file 9x9 with space or 0
#  for unknown values

#  Usage <thisfile> filename

#
#  History
#
#  Date     Ver  Who  Comment
#  xxAug18  0.1  CPN  Initial verison
#  xxSep18  0.2  CPN  WIP
#  13Sep18  0.3  CPN  Move from "12...9" to [1] [2] ... [9]

#
#  Import Libraries
#
import sys

#  
#  Debug variable
#
debug = True
debug = False

#
#  Variables
#

puzzle = [[[0] * 10 for i in range (9)] for i in range (9) ]
puzzleSum = 0

#
#  Procs
#

def usage():
  print("Usage: "+sys.argv[0]+" datafile")


def loadFile(filename, puzzle):
#
#  function to load the raw file, which should be 9 lines of 9 numbers
#
  lineCnt = 0
  dataInObj = open (filename, "r")

  for line in dataInObj:
    for i in range(9):
      lineVal = int(line[i])
      puzzle[lineCnt][i][0] = lineVal
      if lineVal == 0:
        for j in range(1,10):
          puzzle[lineCnt][i][j] = j
      else:
        for j in range(1,10):
          puzzle[lineCnt][i][j] = 0
    lineCnt += 1


def validateAll():
#
#  Proc to validate everything.  First check all the squares, then rows, then columns
#
  validateSquares()
  validateRows()
  validateColumns()


def validateRows():
#
#  Proc to validate the rows
#
  for i in range(9):
    validateArea((i,0),(i,8))
 

def validateColumns():
#
#  Proc to validate the columns
#
  for i in range(9):
    validateArea((0,i),(8,i))
 

def validateSquares():
#
#  Proc to validate each square in tern
#
  validateArea((0,0),(2,2))
  validateArea((0,3),(2,5))
  validateArea((0,6),(2,8))
  validateArea((3,0),(5,2))
  validateArea((3,3),(5,5))
  validateArea((3,6),(5,8))
  validateArea((6,0),(8,2))
  validateArea((6,3),(8,5))
  validateArea((6,6),(8,8))


def validateArea(posStart, posStop):
#
#  Proc to validate an area - called by validate(Row/Column/Square) with the start and end 
#  positions.  In the event of a dupicate being flagged then exit out after reporting error
#
  numList = [0] * 10
  # print ("Start " + str(posStart) + " " + str(posStop))
  startRow = posStart[0]
  startCol = posStart[1]
  stopRow = posStop[0] 
  stopCol = posStop[1]
  for x in range (startRow, stopRow+1):
    for y in range (startCol, stopCol+1):
      # print (puzzle[x][y][0])
      cellVal = puzzle[x][y][0]
      numList[int(cellVal)] += 1
  if debug:
    print(numList)
#  Check for duplicate numbers
  if max(numList[1:]) > 1:
    print("Error : " + str(posStart) + " " + str(posStop) + " " + str(numList))
    exit()
  return(numList)
  
def checkMark():
#
#  Now check the marks for each unassigned square, and assign as required
#
  for x in range(9):
    for y in range(9):
      if debug:
        print (str(x) + " " + str(y))
      if puzzle[x][y][0] == 0:
        retVal = checkCell(x,y)  


def checkCell(x,y):
#
#  Proc to check what numbers are currently in the row, column and square
#
  numList = []
  newList = []
  # First check all the rows
  for i in range(9):
      numList.append(puzzle[x][i][0])
  # Then check columns
  for i in range(9):
      numList.append(puzzle[i][y][0])
  # Now check the active square
  cellX = x - x%3
  cellY = y - y%3
  for i in range(cellX, cellX + 3):
    for j in range(cellY, cellY + 3):
      numList.append(puzzle[i][j][0])
  
  for i in range(1,10):
    if i not in numList:
      newList.append(i)

  if len(newList) == 1:
    puzzle[x][y][0] = newList[0]
  else:
    for i in range(1,10):
      if not (i in numList):
        puzzle[x][y][i] = i
  return newList
  # print puzzle
      

def displayPuzzle(puzzle):
  for x in range(9):
    for y in range(9):
      print puzzle[x][y][0],
    print ""


def getSum(puzzle):
  puzzleSum = 0
  for x in range(9):
    for y in range(9):
      puzzleSum += puzzle[x][y][0]
  return puzzleSum
    
def checkSingle():
#
#  Proc to check if a number is only present in a row, column or square
#  This should check rows, colums and squares
#
  for x in range(9):
    for y in range(9):
      if (puzzle[x][y][0] != 0):    
        # Only make this check if the cell isn't populated
        listRow = validateArea((x,0),(x,8))
        print listRow




#
#  Main program
#

c_args = len(sys.argv)

if debug:
  print ("Num args "+str(c_args))

if c_args != 2:
  usage()
  exit()

fileName = str(sys.argv[1])

if debug:
  print puzzle

loadFile(fileName, puzzle)

if debug:
  print puzzle

#
#  Initial check to confirm that the file is correct before starting to solve
#
validateAll()

if debug:
  print puzzle

#
#  programme loop to check.  Monitoring the sum, to see when progress has stopped
#
while puzzleSum != 405:
  checkMark()
  checkSingle()
  print "F",
  oldPuzzleSum = puzzleSum
  puzzleSum = getSum(puzzle)
  if (oldPuzzleSum == puzzleSum):
    #  Loop?
    print
    print ("Puzzle is static")
    exit()

print

displayPuzzle(puzzle)

exit()

