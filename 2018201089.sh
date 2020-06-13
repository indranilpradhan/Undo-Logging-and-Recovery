#!/bin/bash
if [ "$#" -eq 2 ]
    then
    	python2 2018201089_1.py "$1" "$2" > 2018201089_1.txt
else
	python2 2018201089_2.py "$1" > 2018201089_2.txt
fi
