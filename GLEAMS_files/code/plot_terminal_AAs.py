import matplotlib.pyplot as plt
import numpy as np
import csv
import sys

# command line arguments: output file (png), list of input files (csv)

dict = {}
for i in range(2, len(sys.argv)):
    file_name = sys.argv[i]
    with open(file_name, mode ='r')as file:
        csvFile = csv.reader(file, delimiter='\t')
        # skip header row
        next(csvFile,None)
        for line in csvFile:
            if line[0] in dict:
                dict[line[0]] += int(line[1])
            else:
                dict[line[0]] = int(line[1])

sorted_dict ={k: v for k, v in sorted(dict.items(), key=lambda item: item[1],reverse=True)}

labels = sorted_dict.keys()
values = sorted_dict.values()

fig, ax = plt.subplots()
hbars = ax.barh(labels, values)
ax.invert_yaxis()


# Add some text for labels, title and custom x-axis tick labels, etc.
ax.bar_label(hbars, fmt='{:,.0f}', padding=8)
ax.set_xlabel('number of sequences ending in given amino acid')
ax.set_title('terminal amino acids')

plt.savefig(sys.argv[1])