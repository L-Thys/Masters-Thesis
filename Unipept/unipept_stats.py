import pandas as pd
import matplotlib.pyplot as plt
import glob

def stats_per_file():
    data = {
        "filename":[],
        "Casanovo PSMs":[],
        "unique Casanovo PSMs":[],
        "unique sequences":[],
        "unipept matches": [],
        "unipept unique matches":[]
    }

    files = glob.glob("data/unipept/unipept_results/*.csv")

    for file in files:
        file_name = file.split("/")[-1].split("_")[-1].split(".")[0]
        unipept = pd.read_csv("data/unipept/unipept_results/sequences_PSMs_"+file_name+".csv", usecols =[0,1,2,3])
        all_sequences = pd.read_csv("data/casanovo/psms_by_dataset/PSMs_"+file_name+".csv",usecols = ['sequence'], low_memory = True, sep="\t")
        all_sequences_simplified = pd.read_csv("data/sequences_only/PSMs_"+file_name+".csv",header=None)

        unipept_with_count = pd.merge(unipept, all_sequences_simplified.groupby(by=[0],as_index=False).size(), how="left", left_on=["peptide"], right_on=[0])


        data["filename"].append(file_name)
        data["Casanovo PSMs"].append(len(all_sequences))
        data["unique Casanovo PSMs"].append(all_sequences["sequence"].nunique())
        data["unique sequences"].append(all_sequences_simplified[0].nunique())
        data["unipept matches"].append(unipept_with_count["size"].sum())
        data["unipept unique matches"].append(len(unipept_with_count))

    df=pd.DataFrame(data=data)
    df.to_csv("data/unipept/stats/stats_per_file.csv")

def total_stats():
    files = glob.glob("data/unipept/unipept_results/*.csv")

    unipept = pd.DataFrame()

    for file in files:
        file_name = file.split("/")[-1].split("_")[-1].split(".")[0]
        temp_unipept = pd.read_csv("data/unipept/unipept_results/sequences_PSMs_"+file_name+".csv", usecols =[0])
        all_sequences_simplified = pd.read_csv("data/sequences_only/PSMs_"+file_name+".csv",header=None)
        unipept_with_count = pd.merge(temp_unipept, all_sequences_simplified.groupby(by=[0],as_index=False).size(), how="left", left_on=["peptide"], right_on=[0])
        unipept = pd.concat([unipept,unipept_with_count])
        unipept = unipept.groupby(by=[0],as_index=False).sum()
    print("total PSMs with unipept matches: ", unipept["size"].sum())
    print("unipept unique matches: ", len(unipept))

def combined_data_low_ranks():
    files = glob.glob("data/unipept/unipept_results/*.csv")
    low_ranks = ['no rank', 'taxon', 'superkingdom', 'kingdom', 'subkingdom']
    unipept = pd.DataFrame()

    for file in files:
        file_name = file.split("/")[-1].split("_")[-1].split(".")[0]
        temp_unipept = pd.read_csv("data/unipept/unipept_results/sequences_PSMs_"+file_name+".csv", usecols =[0,3])
        all_sequences_simplified = pd.read_csv("data/sequences_only/PSMs_"+file_name+".csv",header=None)
        unipept_with_count = pd.merge(temp_unipept[temp_unipept["taxon_rank"].isin(low_ranks)], all_sequences_simplified.groupby(by=[0],as_index=False).size(), how="left", left_on=["peptide"], right_on=[0])
        unipept_with_count = unipept_with_count.groupby(by=["taxon_rank"],as_index=False)["size"].sum()
        unipept = pd.concat([unipept,unipept_with_count])
        unipept = unipept.groupby(by=["taxon_rank"],as_index=False)["size"].sum()
        print(file_name)
    print(unipept)
    # results:
    #      taxon_rank    size
    # 0       kingdom  111216
    # 1       no rank  906042
    # 2    subkingdom     796
    # 3  superkingdom  150603
    print(unipept[unipept["taxon_rank"]!="no rank"]["size"].sum())
    # result:      262615

# stats_per_file()
# total_stats()
combined_data_low_ranks()

