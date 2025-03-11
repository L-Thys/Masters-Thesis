#!/bin/bash
FILES=$(ls -1 results_logs_stats/sorted_sequences_by_dataset)
for f in $FILES
do
        output=$(sort -u results_logs_stats/sorted_sequences_by_dataset/$f >> sorted_unique_sequences_by_dataset/$f)
done
