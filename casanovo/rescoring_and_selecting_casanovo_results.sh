#!/bin/bash

for file in $(ls ./data/casanovo/results_with_ids);
do
    INPUT_FILE="data/casanovo/results_with_ids/$1"
    RESCORED_OUTPUT_FILE=".data/casonovo/rescored_results/$1"
    OUTPUT_FILE="./casanovo/good_psms/$1"

    ./casanovo/rescoring_casanovo $INPUT_FILE $RESCORED_OUTPUT_FILE
    ./casanovo/extract_interesting_psms $OUTPUT_FILE $RESCORED_OUTPUT_FILE
done    