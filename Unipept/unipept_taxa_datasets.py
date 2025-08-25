import pandas as pd
import glob
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def part_1():
    DO_RANK_CUTOFF = False
    DO_COUNT_CUTOFF = True
    RANKCUTOFF = "phylum"
    CUTOFF = 2

    files = glob.glob('data/unipept/unipept_analysis/sequences_PSMs_*.csv')
    # files = glob.glob('data/unipept/unipept_analysis/all_grouped*.csv')

    df=pd.DataFrame({"taxon_name":[],"count_specific":[]})


    for file_name in files:
        file_name_end = file_name.split("/")[-1].split("_")[-1].split(".")[0]
        temp = pd.read_csv(file_name,delimiter=",")
        if "taxon_name" not in temp.columns or "count_specific" not in temp.columns:
            continue
        if DO_RANK_CUTOFF:
            taxon_names = [x[:-5] for x in temp.columns if x.endswith("_name")]
            if RANKCUTOFF not in taxon_names:
                continue
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
    # print(df)

    df["number_of_datasets"]=df.count(axis=1)
    df.sort_values(by="number_of_datasets", inplace=True)
    print(df[df["number_of_datasets"]>216/5]["number_of_datasets"])
    print(len(df[df["number_of_datasets"]>216/5]["number_of_datasets"]))

    # plt.pcolor(df)
    # sns.heatmap(df)
    # plt.yticks(np.arange(0.5, len(df.index), 1), df.index)
    # plt.xticks(np.arange(0.5, len(df.columns), 1), df.columns)
    # plt.show()

def part_2(subset, subset_rank, file):

    files = glob.glob('data/unipept/unipept_analysis/sequences_PSMs_*.csv')
    # files = glob.glob('data/unipept/unipept_analysis/all_grouped*.csv')

    df=pd.DataFrame({"taxon_name":[],"count_specific":[]})


    for file_name in files:
        file_name_end = file_name.split("/")[-1].split("_")[-1].split(".")[0]
        temp = pd.read_csv(file_name,delimiter=",")
        if "taxon_name" not in temp.columns or "count_specific" not in temp.columns:
            print(file_name_end)
            continue
        taxon_names = [x[:-5] for x in temp.columns if x.endswith("_name")]
        if subset_rank not in taxon_names:
            continue
        temp = temp[temp[subset_rank+"_name"]==subset]
        temp = temp[["taxon_name","count_specific"]]
        if len(temp) == 0:
            continue 
        temp.rename(columns={"count_specific":file_name_end},inplace=True)
        df = pd.merge(df, temp, on="taxon_name", how="outer")

    # df.fillna(0)
    df.set_index("taxon_name", inplace=True)
    if file is not None:
        df.to_csv(file)
    # print(df)

    df["number_of_datasets"]=df.count(axis=1)
    df.sort_values(by="number_of_datasets", inplace=True)
    print(df[df["number_of_datasets"]>1]["number_of_datasets"])
    print(len(df[df["number_of_datasets"]>9]["number_of_datasets"]))
    print(len(df[df["number_of_datasets"]>1]["number_of_datasets"]))
    print(len(df["number_of_datasets"]))

    # plt.pcolor(df)
    # sns.heatmap(df)
    # plt.yticks(np.arange(0.5, len(df.index), 1), df.index)
    # plt.xticks(np.arange(0.5, len(df.columns), 1), df.columns)
    # plt.show()

def part_3():
    files = glob.glob('data/unipept/unipept_analysis/all_grouped*.csv')

    df=pd.DataFrame({"taxon_name":[],"count_specific":[]})
    for file_name in files:
        file_name_end = file_name.split("/")[-1].split("_")[-1].split(".")[0]
        temp = pd.read_csv(file_name,delimiter=",")
        if "taxon_name" not in temp.columns or "count_specific" not in temp.columns:
            continue
        taxon_names = [x[:-5] for x in temp.columns if x.endswith("_name")]
        if "phylum" not in taxon_names:
            continue
        low_ranks = ["no rank"] + taxon_names[:taxon_names.index("phylum")]
        temp = temp[~temp["taxon_rank"].isin(low_ranks)]
        temp = temp[["taxon_name","count_specific"]]
        temp.rename(columns={"count_specific":file_name_end},inplace=True)
        df = pd.merge(df, temp, on="taxon_name", how="outer")

    df.set_index("taxon_name", inplace=True)
    print(len(df[df.max(axis=1)<3]))
    print(len(df[df.max(axis=1)>2]))

part_1()
# part_2("Bacteria","superkingdom", "data/bacteria.csv")
# part_2("Viruses","superkingdom", "data/Viruses.csv")
# part_3()