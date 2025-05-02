import pandas as pd
import matplotlib.pyplot as plt

import sys

RANKCUTOFF = "phylum"
CUTOFF = 2


# command line arguments: output location (ending in /), input file location (ending in /), file name (csv)
df = pd.read_csv("test.csv")
grouped = df.groupby(["peptide"])["protein_name"].count()
print(grouped.describe())

# dropped = df.drop_duplicates(subset=['peptide', 'taxon_id', 'protein_name'])
# grouped_dropped = dropped.groupby(['taxon_id', 'protein_name'])
# groups = grouped_dropped.head(1).drop(columns=["peptide"])
# groups = grouped_dropped[["peptide"]].agg("count").merge(groups, on=["protein_name", "taxon_id"])
# groups.rename(columns={"peptide":"count"},inplace=True)
# groups = groups.merge(grouped_dropped[["peptide"]].agg(lambda x: list(x)).reset_index(), on=["protein_name", "taxon_id"])
# groups.rename(columns={"peptide":"peptides"},inplace=True)
# groups.sort_values(by="count",inplace=True)
# print(groups)

# grouped_by_taxon_id = groups.groupby("taxon_id")
# taxon_protein_count = grouped_by_taxon_id["protein_name"].count()

    
