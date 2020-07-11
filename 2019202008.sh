#!/bin/bash

argc="$#" 

if [ $argc -eq 2 ]
then
    python3 2019202008_1.py "$1" "$2"
else
    python3 2019202008_2.py "$1"
fi
