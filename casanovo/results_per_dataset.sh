#!/bin/bash

FILES="./interesting_psms_casanovo/*.mztab"

./casanovo/sort_psms_by_dataset ./data/casanovo/psms_by_dataset/ $FILES
