#!/bin/bash
FILES=$(ls -1 results_logs_stats/psms_by_dataset_useful_info_sorted)
for f in $FILES
do
        output=$(sort -k1 -u results_logs_stats/psms_by_dataset_useful_info_sorted/$f > test/$f)
done
