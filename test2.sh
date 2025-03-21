#!/bin/bash
FILES=$(ls -1 results_logs_stats/psms_by_dataset_with_cleaned_sequences)
for f in $FILES
do
        output=$(GLEAMS_files/code/Interesting_data_only test/$f results_logs_stats/psms_by_dataset_with_cleaned_sequences/$f)
done
