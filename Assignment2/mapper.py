#!/usr/bin/env python3
import sys
import csv

# input comes from STDIN (standard input)
reader = csv.DictReader(sys.stdin)

# current location, year and 7Be MDC/7Be CMD (mBq/m3)
current_location = None
current_year = None
current_metric = 0

for row in reader:
    for column, value in row.items():
        if column == "Location/Emplacement":
            current_location = value
        if column == "Collection Start/Début du prélèvement (UTC)":
            current_year = value[:4]
        if column == "7Be MDC/7Be CMD (mBq/m3)":
            current_metric = value

    # write the results to STDOUT (standard output);
    # what we output here will be the input for the
    # reduce step, i.e. the input for reducer.py
    #
    # tab-delimited
    print('(%s, %s)\t%s' % (current_location, current_year, current_metric))
