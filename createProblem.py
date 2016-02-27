#!/usr/bin/python

import sys
import random


def subMatrixInvalid(row, col, n):
    for r in row[1:n]:
        if r in col[1:n]:
            return True
    return False


def isDiagonalInvalid(row, col, dia, n):
    for i in range(1, n*n):
        if (dia[i] == row[i]) or (dia[i] == col[i]):
            return True
    
    for i in range(1,n):
        if (dia[i] in row[:n]) or (dia[i] in col[:n]):
            return True

    return False


def main():
    n = int(sys.argv[1])
    size = n*n

    if n == size:
        print('1')
        sys.exit()

    inValid = True

    while inValid:

        # Generate a random row
        sudoku_row = random.sample(range(1,size+1), size)    


        # Create an empty column and set its first element to first element of row
        sudoku_col = [0]
        sudoku_col[0] = sudoku_row[0]

        # Generate list of possible values to put in remaining column cells
        valid_col_set = range(1, size+1)
        valid_col_set.remove(sudoku_row[0])

        # Add these values
        for i in valid_col_set:
            sudoku_col.append(i)

        # Check if these values are valid in the first submatrix.
        # If not then generate a new random list and keep testing.
        new_sudoku_col = [0]
        new_sudoku_col[0] = sudoku_row[0]

        possible_valid_col_set = random.sample(valid_col_set, len(valid_col_set))
        for i in possible_valid_col_set:
            new_sudoku_col.append(i)
        
        sudoku_col = new_sudoku_col


        while subMatrixInvalid(sudoku_row, sudoku_col, n):
            new_sudoku_col = [0]
            new_sudoku_col[0] = sudoku_row[0]

            possible_valid_col_set = random.sample(valid_col_set, len(valid_col_set))
            for i in possible_valid_col_set:
                new_sudoku_col.append(i)
            
            sudoku_col = new_sudoku_col


        sudoku_dia = [0]
        sudoku_dia[0] = sudoku_row[0]

        valid_dia_set = range(1, size+1)
        valid_dia_set.remove(sudoku_row[0])

        for i in valid_dia_set:
            sudoku_dia.append(i)
        
        counter = 0

        while isDiagonalInvalid(sudoku_row, sudoku_col, sudoku_dia, n):
            counter += 1
            if counter == 10:
                inValid = True
                break;
            new_sudoku_dia = [0]
            new_sudoku_dia[0] = sudoku_row[0]

            possible_valid_dia_set = random.sample(valid_dia_set, len(valid_dia_set))

            for i in possible_valid_dia_set:
                new_sudoku_dia.append(i)
            
            sudoku_dia = new_sudoku_dia

        if counter < 10:
            inValid = False


    puzzle = [['' for _ in range(size)] for _ in range(size)]

    for n in range(size):
        puzzle[0][n] = str(sudoku_row[n])
    for n in range(len(sudoku_col)):
        puzzle[n][0] = str(sudoku_col[n])
    for n in range(len(sudoku_dia)):
        puzzle[n][n] = str(sudoku_dia[n])

    output = ""
    for rows in range(len(puzzle)):
        for cols in range(len(puzzle[rows])):
            output += puzzle[rows][cols]+","
        output += "\n"
    
    print(output)


if __name__ == '__main__':
    main()
