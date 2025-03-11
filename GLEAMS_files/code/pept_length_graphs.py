import matplotlib.pyplot as plt
import glob
import pandas as pd
import numpy as np


files = glob.glob('results_logs_stats/length_data/length_data_filtered_cluster_ident_*.mztab')

# concatenate data from all files
dfs = []
for file_name in files:
    temp = pd.read_csv(file_name,delimiter="\t")
    dfs.append(temp)
df = pd.concat(dfs)

def lengths_graphs():
    fig, ax = plt.subplots()
    ax.hist(df["length of peptide"], bins=91, log=True)
    ax.set_title("histogram of peptide lengths (log scale)")
    ax.set_xticks(range(0,100,10))
    ax.set_xlabel("length of peptide sequence")
    ax.set_ylabel("nr of PSMs with given peptide length")
    ax.grid()
    plt.savefig("peptide_lengths_log.png")

    fig, ax = plt.subplots()
    ax.hist(df["length of peptide"], bins=91)
    ax.set_title("histogram of peptide lengths")
    ax.set_xticks(range(0,100,10))
    ax.set_xlabel("length of peptide sequence")
    ax.set_ylabel("nr of PSMs with given peptide length")
    ax.grid()
    plt.savefig("peptide_lengths.png")

def lengths_with_mean_score():
    grouped = df[["length of peptide","score"]].groupby("length of peptide")
    mean = grouped.mean()
    median = grouped.median()

    fig, ax = plt.subplots()
    ax.hist(df["length of peptide"], bins=91, log=True)
    ax.set_title("histogram of peptide lengths (log scale)")
    ax.set_xticks(range(0,100,10))
    ax.set_xlabel("length of peptide sequence")
    ax.set_ylabel("nr of PSMs with given peptide length")
    ax.tick_params(axis='y', labelcolor="tab:blue")
    ax.grid()

    ax2 = ax.twinx()
    ax2.plot(mean, color='tab:red')
    ax2.tick_params(axis='y', labelcolor="tab:red")
    ax2.set_ylabel("mean score of PSMs with given peptide")
    plt.savefig("peptide_lengths_with_mean_score.png")


def interesting():
    df_interesting = pd.read_csv("results_logs_stats/length_data_interesting_results.mztab",delimiter="\t")

    fig, ax = plt.subplots()
    ax.hist(df["length of peptide"], bins=91, log=True)
    ax.hist(df_interesting["length of peptide"], bins=55, log=True, color='tab:red', alpha=0.7)
    ax.set_title("histogram of peptide lengths (log scale)")
    ax.set_xticks(range(0,100,10))
    ax.set_xlabel("length of peptide sequence")
    ax.set_ylabel("nr of PSMs with given peptide length")
    ax.legend(["all PSMs", "PSMs with good score"])
    ax.grid()


    plt.savefig("peptide_lengths_with_good_scores.png")


df_interesting = pd.read_csv("results_logs_stats/length_data_interesting_results.mztab",delimiter="\t")

fig, ax = plt.subplots()
ax.hist(df["length of peptide"], bins=91)
ax.hist(df_interesting["length of peptide"], bins=55, color='tab:red', alpha=0.7)
ax.set_title("histogram of peptide lengths")
ax.set_xticks(range(0,100,10))
ax.set_xlabel("length of peptide sequence")
ax.set_ylabel("nr of PSMs with given peptide length")
ax.legend(["all PSMs", "PSMs with good score"])
ax.grid()


plt.savefig("peptide_lengths_with_good_scores.png")