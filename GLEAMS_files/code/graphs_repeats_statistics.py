import matplotlib.pyplot as plt
import pandas as pd

def longest_repeat_histogram(df,rang):
    df[["longest_repeat_length"]].hist(log=True,bins=range(1,rang))
    plt.show()

def nr_repeats(df,rang):
    df[["no_of_repeats_3_or_longer"]].hist(log=True,bins=range(0,rang))
    plt.show()

def mean_score_longest_repeat(df, rang):
    grouped = df[["longest_repeat_length","search_engine_score[1]"]].groupby("longest_repeat_length")
    mean = grouped.mean()
    fig, ax = plt.subplots()
    ax.set_title("mean score by length of longest amino acid repeat")
    ax.plot(mean, color="red")
    ax.grid()

    ax2 = ax.twinx()
    ax2.hist(df["longest_repeat_length"], bins=range(1,rang), log=True, alpha=0.3, color="grey")
    ax2.tick_params(axis='y', labelcolor="grey")
    plt.show()

def percentage_longest_repeat(df):
    df.plot.scatter(x="sequence_length", y="longest_repeat_length")
    plt.show()

def posititve():
    pos_df = pd.read_csv("results_logs_stats/repeat_stats_pos.csv",delimiter="\t", usecols=[1,3,4,5])
    # print(pos_df.describe())
    longest_repeat_histogram(pos_df,33)
    nr_repeats(pos_df,9)
    mean_score_longest_repeat(pos_df,33)
    # percentage_longest_repeat(pos_df)

def negative():
    neg = pd.read_csv("results_logs_stats/repeat_stats_neg.csv",delimiter="\t", usecols=[1,3,4,5])
    # print(neg.describe())
    longest_repeat_histogram(neg,40)
    nr_repeats(neg,8)
    mean_score_longest_repeat(neg,40)    


posititve()
# negative()