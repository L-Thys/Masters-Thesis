import pandas as pd

df=pd.read_csv("results_logs_stats/all_sequences_completely_deduplicated.tab",delimiter="\t")
df["sequence"].to_csv("all_peptides_deduplicated.csv", index=False)