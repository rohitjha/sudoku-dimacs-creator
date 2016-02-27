#!/bin/bash

if [ $# -ne 2 ]
	then
	echo "Usage: ./run.sh n r, where n is the size and r is the reduction method (1 or 2)."
	exit 1
fi

N="$1"
RED="$2"

if [[ RED -ne 1 && RED -ne 2 ]]
	then
	echo "Usage: ./run.sh n r, where r is either 1 or 2"
	exit 1
fi

SAT=minisat
PARAM="-cpu-lim 3600"
INITIAL=initial.state
INPUT=sudoku.in
OUTPUT=sudoku.out
PYTHON=python

echo "Randomly generating the first row, first column and the main diagonal..."
$PYTHON createProblem.py $N > $INITIAL

echo "The Sudoku problem is..."
if [ "$N" -eq "1" ]
	then
	echo "1"
else
	$PYTHON showProblem.py $INITIAL
fi

echo "Generating DIMACS format input for $SAT ..."
$PYTHON generateDIMACS.py $N $RED $INITIAL > $INPUT

echo "Input file generated: $INPUT"
echo "Running SAT solver now..."
$SAT $INPUT $OUTPUT

$PYTHON showResult.py $N $OUTPUT
