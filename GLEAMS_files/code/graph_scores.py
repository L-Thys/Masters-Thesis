import matplotlib.pyplot as plt
import pandas as pd


def good():
    good_scores = scores[scores > 0]
    fig, ax = plt.subplots()
    ax.hist(good_scores, bins=[x/1000.0 for x in range(900, 1005, 5)])
    ax.set_title("histogram of positive good scores")
    ax.set_xticks([x/100.0 for x in range(90, 101, 1)])
    plt.savefig("hist_pos_scores.png")

def bad():
    bad_scores = scores[scores < 0]
    fig, ax = plt.subplots()
    ax.hist(bad_scores, bins=[x/1000.0 for x in range(-100, 5, 5)])
    ax.set_title("histogram of negative good scores")
    ax.set_xticks([x/100.0 for x in range(-10, 1, 1)])
    plt.savefig("hist_neg_scores.png")

scores = pd.read_csv("results_logs_stats/psms_by_dataset_useful_info_sorted/all_sequences_with_duplicates.tab",delimiter="\t", header=None)[2]
good()
# bad()