import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import csv
import sys

# command line arguments: output file (png), list of input files (csv)

dict = {}
for i in range(2, len(sys.argv)):
    file_name = sys.argv[i]
    i = -1
    with open(file_name, mode ='r')as file:
        csvFile = csv.reader(file, delimiter='\t')
        # skip header row
        next(csvFile,None)
        for line in csvFile:
            if i in dict:
                dict[i] += int(line[1])
            else:
                dict[i] = int(line[1])
            i+=0.1

labels = dict.keys()
values = dict.values()

fig, ax = plt.subplots()
hbars = ax.bar(labels, values,width=0.1,  edgecolor="white",align="edge")

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.bar_label(hbars, fmt=lambda x: f'{x /1000:.0f}k')


ax.set_title('Casanovo Scores histogram')

ax.yaxis.set_major_formatter(ticker.EngFormatter(unit=''))
ax.set(xlim=(-1,1), xticks=np.arange(-1,1.1,0.2))
fig.set_figwidth(10)
fig.set_figheight(6)
plt.savefig(sys.argv[1])