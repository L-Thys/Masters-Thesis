import pandas as pd
# we're looking for peptides that match only to one protein, 
# if two or more of these peptides match to the same protein, we'll count this as "evidence" for the protein 
# (for hupo-hpp guidelines, each peptide must be at least 9 amino acids, and there cannot be overlap (if two peptides do overlap, the total extend must be >= 18 AA))
# we'll look seperately for each dataset, but we'll combine the blast results for the ncorf and the human proteome for each dataset

def load_df(dataset_name):
    ncorfs_cont = pd.read_csv("results_logs_stats/blast/good_e_values/ncORFs_contaminants/"+dataset_name+".csv",delimiter=",")
    homo = pd.read_csv("results_logs_stats/blast/good_e_values/homo_sapiens/"+dataset_name+".csv",delimiter=",")
    return pd.concat([ncorfs_cont, homo])

def select_uniquely_matching_sequences(df):
    # taking a brake to check if there are instances where the same peptide matches multiple times with the same protein
    # result: this happens, filter on having matches with only 1 protein, not on having only one match
    protein_matches=df.groupby("qaccver",as_index=False)["saccver"].nunique()
    unique_matchin_sequences=protein_matches[protein_matches["saccver"]==1][["qaccver"]]
    return pd.merge(unique_matchin_sequences, df, how="left", on=["qaccver", "qaccver"]).drop("Unnamed: 0", axis=1)

# next step: look for proteins with multiple peptide matches

# ---------- tesing zone --------------
df= load_df("fasta_sequences_PSMs_MSV000080679")
select_uniquely_matching_sequences(df)






