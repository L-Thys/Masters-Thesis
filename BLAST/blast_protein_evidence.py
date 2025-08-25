import pandas as pd
import glob
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# we're looking for peptides that match only to one protein, 
# if two or more of these peptides match to the same protein, we'll count this as "evidence" for the protein 
# (for hupo-hpp guidelines, each peptide must be at least 9 amino acids, and there cannot be overlap (if two peptides do overlap, the total extend must be >= 18 AA))
# we'll look seperately for each dataset, but we'll combine the blast results for the ncorf and the human proteome for each dataset

def proteins_with_multiple_peptide_matches(output_location="data/blast/protein_evidence/"):
    data = {
        "filename":[],
        "proteins":[],
        "proteins with >1 match":[],
        "proteins with evidence":[],
        "contaminant proteins with evidence": [],
        "ncorf proteins with evidence":[]
    }

    files = glob.glob('data/blast/good_e_values/ncORFs_contaminants/fasta_sequences_*.csv')
    for file in files:
        file_name = file.split("/")[-1].split("_")[-1].split(".")[0]
        data["filename"].append(file_name)

        # loading datasets
        ncorfs_cont = pd.read_csv("data/blast/good_e_values/ncORFs_contaminants/fasta_sequences_PSMs_"+file_name+".csv",delimiter=",")
        homo = pd.read_csv("data/blast/good_e_values/homo_sapiens/fasta_sequences_PSMs_"+file_name+".csv",delimiter=",")
        df = pd.concat([ncorfs_cont,homo])

        ncorf_names= ncorfs_cont[~ncorfs_cont["saccver"].str.startswith("CONT_")]["saccver"].unique()

        # filter peptides on having matches with only 1 protein (not same as having on having only one match)
        protein_matches=df.groupby("qaccver",as_index=False)["saccver"].nunique()
        unique_matchin_sequences=protein_matches[protein_matches["saccver"]==1][["qaccver"]]
        df2 = pd.merge(unique_matchin_sequences, df, how="left", on=["qaccver", "qaccver"]).drop("Unnamed: 0", axis=1)
        data["proteins"].append(df2["saccver"].nunique())

        # look for proteins with multiple peptide matches
        peptide_matches=df2.groupby("saccver",as_index=False)["qaccver"].nunique()
        proteins_with_multiple_matches=peptide_matches[peptide_matches["qaccver"]!=1][["saccver"]]
        data["proteins with >1 match"].append(pd.merge(proteins_with_multiple_matches, df, how="left", on=["saccver", "saccver"])["saccver"].nunique())
        peptide_matches=df2.groupby("saccver",as_index=False)
        to_keep = {
            "saccver":[],
            "number_of_matches":[]
        }
        for saccver, group in peptide_matches:
            if len(group)>1:
                # remove sequences that overlap with exact same start or end location on the protein
                group=group.sort_values(["length","sstart"],ascending=False)
                group = group.drop_duplicates(subset="sstart")
                group = group.drop_duplicates(subset="send")
                if len(group)>1:
                    to_keep["saccver"].append(saccver)
                    to_keep["number_of_matches"].append(len(group))
        results= pd.DataFrame(to_keep).sort_values(["number_of_matches"])
        if len(results) != 0:
            results[results["saccver"].isin(ncorf_names)].to_csv(output_location+"ncorfs/"+file_name+".csv") # output ncorf protein results 
            results[results["saccver"].str.startswith("CONT_")].to_csv(output_location+"contaminants/"+file_name+".csv") # output contaminants protein results 
            human = results[~results["saccver"].str.startswith("CONT_")]
            human[~human["saccver"].isin(ncorf_names)].to_csv(output_location+"human/"+file_name+".csv") # output human protein results
            data["proteins with evidence"].append(len(results))
            data["contaminant proteins with evidence"].append(len(results[results["saccver"].str.startswith("CONT_")]))
            data["ncorf proteins with evidence"].append(len(results[results["saccver"].isin(ncorf_names)]))
        else:
            results.to_csv(output_location+"ncorfs/"+file_name+".csv") # output ncorf protein results 
            results.to_csv(output_location+"contaminants/"+file_name+".csv") # output contaminants protein results 
            results.to_csv(output_location+"human/"+file_name+".csv") # output human protein results 
            data["proteins with evidence"].append(0)
            data["contaminant proteins with evidence"].append(0)
            data["ncorf proteins with evidence"].append(0)
   
    df=pd.DataFrame(data=data)
    df.to_csv(output_location+"stats.csv")        



def part_2(file="contaminants_test.csv"):
    # files = glob.glob('data/blast/protein_evidence/ncorfs/*.csv')
    # files = glob.glob('data/blast/protein_evidence/contaminants/*.csv')
    files = glob.glob('data/blast/protein_evidence/human/*.csv')

    df=pd.DataFrame({"saccver":[]})

    for file_name in files:
        file_name_end = file_name.split("/")[-1].split("_")[-1].split(".")[0]
        temp = pd.read_csv(file_name,usecols=[1,2],delimiter=",")
        if len(temp) == 0:
            continue 
        temp.rename(columns={"number_of_matches":file_name_end},inplace=True)
        df = pd.merge(df, temp, on="saccver", how="outer",)

    df.set_index("saccver", inplace=True)
    if file is not None:
        df.to_csv(file)

    df["number_of_datasets"]=df.count(axis=1)
    df.sort_values(by="number_of_datasets", inplace=True)
    # print(df[df["number_of_datasets"]>5]["number_of_datasets"])
    print(df["number_of_datasets"])

def plot_contaminants():
    df=pd.read_csv("data/blast/contaminants_test.csv", index_col=0, header=0)

    # plt.pcolor(df)
    # sns.heatmap(df)
    # plt.yticks(np.arange(0.5, len(df.index), 1), df.index)
    # plt.xticks(np.arange(0.5, len(df.columns), 1), df.columns)
    # plt.show()


    df["number_of_datasets"]=df.count(axis=1)
    df.sort_values(by="number_of_datasets", inplace=True)
    print(df[df["number_of_datasets"]>5]["number_of_datasets"])
    print(df[df["number_of_datasets"]>1]["number_of_datasets"])
    print(len(df[df["number_of_datasets"]>216/5]))
    print(len(df["number_of_datasets"]))


    

# proteins_with_multiple_peptide_matches()
# part_2("human_test.csv")
plot_contaminants()







