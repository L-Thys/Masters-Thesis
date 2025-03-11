import matplotlib.pyplot as plt
import numpy as np
import sys

# command line arguments: output file (png), list of input files (csv)

data = np.array([])
for i in range(2, len(sys.argv)):
    file_name = sys.argv[i]
    new_data = np.genfromtxt(file_name, delimiter=',')
    data=np.append(data,new_data )
    
data = data[data>=-100]
data = data[data<=100]   
fig, ax = plt.subplots()
hbars = ax.hist(data,bins=200)

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_title('neutral mass difference histogram')
plt.xlim()
plt.savefig(sys.argv[1])