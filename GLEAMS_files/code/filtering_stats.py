import matplotlib.pyplot as plt
import numpy as np

files = ("cluster_ident_2", "cluster_ident_n", "combined")
penguin_means = {
    'Total Spectra': (23.27, 21.43, 44.70),
    'Unidentified by GLEAMS': (21.31, 18.11, 39.42),
    # 'Identified': (1.96, 3.32, 5.28),
    'Casanovo PSMs': (21.29, 18.02, 39.31),
    'Good Casanovo Scores': (1.91, 2.44, 4.35)
}

x = np.arange(len(files))  # the label locations
width = 0.25  # the width of the bars
multiplier = 0

fig, ax = plt.subplots()

for attribute, measurement in penguin_means.items():
    offset = width * multiplier
    rects = ax.bar(x + offset, measurement, width, label=attribute)
    ax.bar_label(rects, padding=3)
    multiplier += 1

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('number of spectra (millions)')
ax.set_title('spectra by GLEAMS file')
ax.set_xticks(x + width, files)
ax.legend(loc='upper left', ncols=1)

plt.savefig("filtering_stats.png")