#!/bin/bash

path_to_pvss="/afs/cern.ch/work/v/vyeroshe/pvssarchive"
variables="PLDAQTELL40:lumi_counters.*"

# fill=$1
# t_start=$2
# t_end=$3

fill="test"
t_start="2022-05-29 6:00:00"
t_end="2022-05-29 10:00:00"


$path_to_pvss/remotePVSSExport.sh "$t_start" "$t_end" $variables > "Data/lumivar_$fill.csv"
