#!/bin/bash
FILES=$(ls -1 test2/)
for f in $FILES
do
        cat test2/$f >> test.tab
done
sort -k2  test.tab > test2.tab