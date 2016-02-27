#!/usr/bin/python
import sys

def literal(i, j, k, n2):
    return fit(i, n2) + fit(j, n2) + fit(k, n2)

def fit(n, n2):
    diff = len(str(n2)) - len(str(n))
    
    zeros = ["0" for i in range(0, diff)]
    fitn = ''.join(zeros)

    fitn += str(n)
    return fitn


def readInitial(n, fname):
    dimacs = ""
    dimacs += "c Adding random values for first row, first column and main diagonal\n"
    lines = [word[:-1].split(',') for line in open(fname, 'r') for word in line.split()]

    
    literals = [ (literal(i+1, j+1, lines[i][j], n*n) + " 0\n") for i in range(0, len(lines)) for j in range(0, len(lines[i])) if lines[i][j] != '' ]
    literals = ''.join(literals)

    dimacs += literals
    
    return dimacs

def reduction1(n, initial):
    n2      = n * n
    atoms   = n2 * n2 * n2
    clauses = 0
    dimacs  = initial
    digits = len(str(n2))

    
    dimacs += "c There is at most one number in each cell\n"
    for i in range(1, n2 + 1):
      for j in range(1, n2 + 1):
        for k in range(1, n2):
          for h in range(k + 1, n2 + 1):
            dimacs += "-" + literal(i, j, k, n2) + " -" + literal(i, j, h, n2) + " 0\n"
            clauses += 1
    
    dimacs += "c There is at least one number in each cell\n"
    for i in range(1, n2 + 1):
      for j in range(1, n2 + 1):
        for k in range(1, n2 + 1):
          dimacs += literal(i, j, k, n2) + " "
        dimacs += "0\n"
        clauses += 1

    
    dimacs += "c Each number appears at most once in each row\n"
    for j in range(1, n2 + 1):
      for k in range(1, n2 + 1):
        for i in range(1, n2):
          for h in range(i + 1, n2 + 1):
            dimacs += "-" + literal(i, j, k, n2) + " -" + literal(h, j, k, n2) + " 0\n"
            clauses += 1
    
    dimacs += "c Each number appears at least once in each row\n"
    for j in range(1, n2 + 1):
      for k in range(1, n2 + 1):
        for i in range(1, n2 + 1):
          dimacs += literal(i, j, k, n2) + " "
        dimacs += "0\n"
        clauses += 1

    dimacs += "c Each number appears at most once in each column\n"
    for i in range(1, n2 + 1):
      for k in range(1, n2 + 1):
        for j in range(1, n2):
          for h in range(j + 1, n2 + 1):
            dimacs += "-" + literal(i, j, k, n2) + " -" + literal(i, h, k, n2) + " 0\n"
            clauses += 1

    dimacs += "c Each number appears at least once in each column\n"
    for i in range(1, n2 + 1):
      for k in range(1, n2 + 1):
        for j in range(1, n2 + 1):
          dimacs += literal(i, j, k, n2) + " "
        dimacs += "0\n"
        clauses += 1

    dimacs += "c Each number appears at most once in each " + str(n) + "*" + str(n) + " sub-matrix\n"
    for k in range(1, n2 + 1):
        for x in range(0, n):
            for y in range(0, n):
                for i in range(1, n + 1):
                    for j in range(1, n + 1):
                        for z in range(j + 1, n + 1):
                          dimacs += "-" + literal(n*x + i, n*y + j, k, n2) + " -" + literal(n*x + i, n*y + z, k, n2) + " 0\n"
                          clauses += 1

    for k in range(1, n2 + 1):
        for x in range(0, n):
            for y in range(0, n):
                for i in range(1, n + 1):
                    for j in range(1, n + 1):
                        for z in range(i + 1, n + 1):
                            for w in range(1, n + 1):
                              dimacs += "-" + literal(n*x + i, n*y + j, k, n2) + " -" + literal(n*x + z, n*y + w, k, n2) + " 0\n"
                              clauses += 1

    dimacs += "c Each number appears at least once in each " + str(n) + "*" + str(n) + " sub-matrix\n"
    for k in range(1, n2 + 1):
        for x in range(0, n):
            for y in range(0, n):
                for i in range(1, n + 1):
                    for j in range(1, n + 1):
                      dimacs += literal(n*x + i, n*y + j, k, n2) + " "
        dimacs += "0\n"
        clauses += 1


    dimacs = "c Created by Sudoku Dimacs Creator\n" + dimacs
    dimacs = "p cnf " + str(atoms) + " " + str(clauses) + "\n" + dimacs

    print(dimacs),

def reduction2(n, initial):
    n2      = n * n
    atoms   = n2 * n2 * n2
    clauses = 0
    dimacs  = initial
    digits  = len(str(n2))

    dimacs += "c At least one number in each entry\n"
    for i in range(1, n2 + 1):
      for j in range(1, n2 + 1):
        for k in range(1, n2 + 1):
          dimacs += literal(i, j, k, n2) + " "
        dimacs += "0\n"
        clauses += 1
    
    
    dimacs += "c A number is not repeated in a row\n"
    for i in range(1, n2 + 1):
      for j in range(1, n2 + 1):
        for k in range(1, n2 + 1):
          for j_s in range(j+1, n2 + 1):
            dimacs += "-" + literal(i, j, k, n2) + " -" + literal(i, j_s, k, n2) + " 0\n"
            clauses += 1
    
    dimacs += "c A number is not repeated in a column\n"
    for i in range(1, n2 + 1):
      for j in range(1, n2 + 1):
        for k in range(1, n2 + 1):
          for i_s in range(i+1, n2 + 1):
            dimacs += "-" + literal(i, j, k, n2) + " -" + literal(i_s, j, k, n2) + " 0\n"
            clauses += 1


    dimacs += "c A number is not repeated in a " + str(n) + "*" + str(n) + " sub-matrix\n"
    for k in range(1, n2+1):
        for x in range(0, n):
            for y in range(0, n):
                for i in range(1, n+1):
                    for j in range(1, n+1):
                        for z in range(j+1, n+1):
                            dimacs += "-" + literal(n*x + i, n*y + j, k, n2) + " -" + literal(n*x + i, n*y + z, k, n2) + " 0\n"
                            clauses += 1

    for k in range(1, n2+1):
        for x in range(0, n):
            for y in range(0, n):
                for i in range(1, n+1):
                    for j in range(1, n+1):
                        for z in range(i+1, n+1):
                            for w in range(1, n+1):
                                dimacs += "-" + literal(n*x + i, n*y + j, k, n2) + " -" + literal(n*x + z, n*y + w, k, n2) + " 0\n"
                                clauses += 1


    dimacs = "c Created by Sudoku Dimacs Creator\n" + dimacs
    dimacs = "p cnf " + str(atoms) + " " + str(clauses) + "\n" + dimacs

    print(dimacs),

def main():
    n = int(sys.argv[1])
    reduction = int(sys.argv[2])
    initial = sys.argv[3]

    initialClauses = readInitial(n, initial)
    
    if reduction == 1:
        reduction1(n, initialClauses)
    elif reduction == 2:
        reduction2(n, initialClauses)

if __name__ == '__main__':
    main()
