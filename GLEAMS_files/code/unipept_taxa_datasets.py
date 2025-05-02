import pandas as pd
import sys
import glob
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

DO_RANK_CUTOFF = True
DO_COUNT_CUTOFF = True
RANKCUTOFF = "phylum"
CUTOFF = 2
FILE = "test2.csv"


# files = glob.glob('results_from_vsc/unipept_analysis/sequences_PSMs_*.csv')
files = glob.glob('results_from_vsc/unipept_analysis_all_grouped/*.csv')

first_filename = files.pop()
file_name_end = first_filename.split("/")[-1].split("_")[-1].split(".")[0]
df=pd.read_csv(first_filename,delimiter=",")
if DO_RANK_CUTOFF:
    taxon_names = [x[:-5] for x in df.columns if x.endswith("_name")]
    low_ranks = ["no rank"] + taxon_names[:taxon_names.index(RANKCUTOFF)]
    df = df[~df["taxon_rank"].isin(low_ranks)]
df = df[["taxon_name","count_specific"]]
df.rename(columns={"count_specific":file_name_end},inplace=True)


for file_name in files:
    file_name_end = file_name.split("/")[-1].split("_")[-1].split(".")[0]
    temp = pd.read_csv(file_name,delimiter=",")
    if "taxon_name" not in temp.columns or "count_specific" not in temp.columns:
        print(file_name_end)
        continue
    if DO_RANK_CUTOFF:
        taxon_names = [x[:-5] for x in temp.columns if x.endswith("_name")]
        low_ranks = ["no rank"] + taxon_names[:taxon_names.index(RANKCUTOFF)]
        temp = temp[~temp["taxon_rank"].isin(low_ranks)]
    temp = temp[["taxon_name","count_specific"]]
    temp.rename(columns={"count_specific":file_name_end},inplace=True)
    df = pd.merge(df, temp, on="taxon_name", how="outer")

# df.fillna(0)
df.set_index("taxon_name", inplace=True)
if DO_COUNT_CUTOFF:
    df["highest"]= df.max(axis=1)
    df = df[df["highest"]>CUTOFF].drop(columns="highest")
if FILE is not None:
    df.to_csv(FILE)
# print(df)

# plt.pcolor(df)
# sns.heatmap(df)
# plt.yticks(np.arange(0.5, len(df.index), 1), df.index)
# plt.xticks(np.arange(0.5, len(df.columns), 1), df.columns)
# plt.show()


