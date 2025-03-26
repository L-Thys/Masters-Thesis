import pandas as pd
import sys


df = pd.read_csv("results_from_vsc/all_sequences_PSMs_MSV000078777.csv")
 
# -- see list of taxa ranks: --
# for x in df.columns:
#     if x.endswith("_name"):
#         print(x[:-5])


df.dropna(how='all', axis=1, inplace=True)
names = [x for x in df.columns if x.endswith("_name")]
df = df[["peptide", "taxon_rank"]+names]

# -- see list of non nan taxa ranks: --
# for x in df.columns:
#     if x.endswith("_name"):
#         print(x[:-5])

# --- group by taxon name ----
grouped = df.groupby("taxon_name")
groups = grouped.head(1).drop(columns=["peptide"]).set_index("taxon_name")
groups = grouped[["peptide"]].agg(lambda x: list(x)).join(groups)
groups.rename(columns={"peptide":"peptides"},inplace=True)
groups = grouped[["peptide"]].agg("count").join(groups)
groups.rename(columns={"peptide":"count"},inplace=True)
groups.sort_values(by="count", inplace=True, ascending=False)
groups.reset_index(inplace=True)
# ----------------------------

# -- select the entries with more peptides than CUTOFF (also drops nan columns) ----
CUTOFF = 2
selected = groups[groups["count"]>CUTOFF]
selected.dropna(how='all', axis=1, inplace=True)
print(selected.drop(columns="peptides"))
# --------------------

# -- select entries with taxon rank >= RANKCUTOFF (also drops nan columns) --------
# -- for "phylum", lower ranks are ['no rank', 'superkingdom', 'kingdom', 'subkingdom']
RANKCUTOFF = "phylum"
taxon_names = [x[:-5] for x in df.columns if x.endswith("_name")]
low_ranks = ["no rank"] + taxon_names[:taxon_names.index(RANKCUTOFF)]
selected = groups[~groups["taxon_rank"].isin(low_ranks)]
selected.dropna(how='all', axis=1, inplace=True)
# print(selected.drop(columns="peptides"))
# ------------------------------

# -- select entries with more peptides than CUTOFF and with taxon rank >= RANKCUTOFF (also drops nan columns) ---
selected = groups[groups["count"]>CUTOFF][~groups["taxon_rank"].isin(low_ranks)]
selected.dropna(how='all', axis=1, inplace=True)
print(selected.drop(columns="peptides"))
selected.to_csv("test.csv")
# -----------------------------------

# TODO: add peptides of subtaxa as extra columns, and add total count
#       this does mean we might double count
