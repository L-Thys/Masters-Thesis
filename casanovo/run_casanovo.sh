#!/bin/bash

for file in $(ls ./data/split_mgf_files);
do
    INPUT_FILE=".data/casanovo/split_mgf_files/$1.mgf"
    CASANOVO_OUTPUT_FILE=".data/casonovo/casanovo_results/$1.mztab"
    OUTPUT_FILE="./casanovo/results_with_ids/$1.mztab"

    casanovo sequence ${INPUT_FILE} -o ${CASANOVO_OUTPUT_FILE}
    casanovo/add_spectrum_titles_to_mztab ${INPUT_FILE} ${CASANOVO_OUTPUT_FILE} ${OUTPUT_FILE}
done    