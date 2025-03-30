import pandas as pd
import sys

RANKCUTOFF = "phylum"
CUTOFF = 2


# command line arguments: output location (ending in /), input file location (ending in /), file name (csv)
df = pd.read_csv(sys.argv[2]+sys.argv[3])

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
groups = groups.join(grouped[["peptide"]].agg(lambda x: list(x)))
groups.rename(columns={"peptide":"peptides"},inplace=True)
groups = grouped[["peptide"]].agg("count").join(groups)
groups.rename(columns={"peptide":"count_specific"},inplace=True)
groups.sort_values(by="count_specific", inplace=True, ascending=False)
groups.reset_index(inplace=True)
groups.to_csv(sys.argv[1]+"all_grouped_"+sys.argv[3])

# ----------------------------

# -- select the entries with more peptides than CUTOFF (also drops nan columns) ----
# selected = groups[groups["count_specific"]>CUTOFF]
# selected.dropna(how='all', axis=1, inplace=True)
# print(selected.drop(columns="peptides"))
# --------------------

# -- add count_including_subtaxa and peptides_including_subtaxa -----
# selected["peptides_including_subtaxa"] = pd.Series()
# selected["count_including_subtaxa"] = pd.Series()
# for index, row in selected.iterrows():
#     taxon_name = row["taxon_name"]
#     taxon_rank = row["taxon_rank"]
#     if (taxon_rank != "no rank"):
#         peptides = df[df[taxon_rank+"_name"]==taxon_name]["peptide"].tolist()
#         selected.at[index, "count_including_subtaxa"] = len(peptides)
#         selected.at[index,"peptides_including_subtaxa"] = peptides
# ---------------


# -- select entries with taxon rank >= RANKCUTOFF (also drops nan columns) --------
# -- for "phylum", lower ranks are ['no rank', 'superkingdom', 'kingdom', 'subkingdom']
# taxon_names = [x[:-5] for x in df.columns if x.endswith("_name")]
# low_ranks = ["no rank"] + taxon_names[:taxon_names.index(RANKCUTOFF)]
# selected = groups[~groups["taxon_rank"].isin(low_ranks)]
# selected.dropna(how='all', axis=1, inplace=True)
# print(selected.drop(columns="peptides"))
# ------------------------------

# -- select entries with more peptides than CUTOFF and with taxon rank >= RANKCUTOFF (also drops nan columns) ---
taxon_names = [x[:-5] for x in df.columns if x.endswith("_name")]
low_ranks = ["no rank"] + taxon_names[:taxon_names.index(RANKCUTOFF)]
selected = groups[groups["count_specific"]>CUTOFF]
selected = selected[~selected["taxon_rank"].isin(low_ranks)]
selected.dropna(how='all', axis=1, inplace=True)
# add count_including_subtaxa and peptides_including_subtaxa
selected["peptides_including_subtaxa"] = pd.Series()
selected["count_including_subtaxa"] = pd.Series()
for index, row in selected.iterrows():
    taxon_name = row["taxon_name"]
    taxon_rank = row["taxon_rank"]
    if (taxon_rank != "no rank"):
        peptides = df[df[taxon_rank+"_name"]==taxon_name]["peptide"].tolist()
        selected.at[index, "count_including_subtaxa"] = len(peptides)
        selected.at[index,"peptides_including_subtaxa"] = peptides
selected.to_csv(sys.argv[1]+sys.argv[3])
# -----------------------------------
