#!/bin/bash
# README: run this file from the root of the project

g++ Unipept/list_sequences_only.cpp -o Unipept/list_sequences_only

for file in $(ls ./data/casanovo/psms_by_dataset);
do
    INPUT_FILE="data/casanovo/psms_by_dataset/$file"
    OUTPUT_FILE="./data/sequences_only/$file"
    Unipept/list_sequences_only $OUTPUT_FILE $INPUT_FILE
done
 
for f in $(ls data/sequences_only/);
do 
    peptfilter < data/sequences_only/$f | unipept pept2lca -e -a > data/unipept/unipept_results/$f
done

for f in $(ls data/sequences_only/);
do
python Unipept/unipept_analysis.py data/unipept/unipept_analysis/ data/unipept/unipept_results/ $f

done


