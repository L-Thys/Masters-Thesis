import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import glob

MAXEVAL = 0.001

def calculate_missmatches(row):
    sequence1=row["sseq"].replace("L", "I") 
    sequence2=row["qseq"].replace("L", "I")
    dist = 0
    for i in range(len(sequence1)):
        if sequence1[i] != sequence2[i]:
            dist += 1
    return dist

def calculate_substitutions(row):
    sequence1=row["sseq"].replace("L", "I") 
    sequence2=row["qseq"].replace("L", "I")
    dist = 0
    for i in range(len(sequence1)):
        if sequence1[i] != sequence2[i]:
            if sequence1[i] != "-" and sequence2[i] != "-":
                dist += 1
    return dist

def extra_stats(df):
    df["subs"]=df.apply(calculate_substitutions, axis=1)
    df["mismatches"]=df.apply(calculate_missmatches, axis=1)
    df["p_ident"]=(df["qlen"]-df["mismatches"])/df["qlen"]*100
    df.drop(labels=["pident"],axis=1,inplace=True)
    df["length_diff"]=df["qlen"]-df["qend"]+df["qstart"]-1
    return df

def intial_analysis():

    # ----- load blast results for finding Streptavidin and human disulfide-isomerase in MSV000078777 --------
    # -- 457 matches --
    results = pd.read_csv("fasta_sequences_PSMs_MSV000078777.csv",delimiter=",")

    # ----- new identity measures --------
    results=extra_stats(results)
    results.drop(labels=["qlen","qstart","qend"],axis=1,inplace=True)

    # results.drop(labels=["qlen", "sseq"],axis=1,inplace=True)


    # ----- plot evalues histogram ---------
    # fig, ax = plt.subplots()
    # ax.hist(results["evalue"],bins=10**np.linspace(0, 1, 10))
    # ax.set_title("histogram of evalues")
    # ax.set_xscale("log")
    # # ax.set_xticks([x/100.0 for x in range(90, 101, 1)])
    # # plt.savefig("hist_pos_scores.png")
    # plt.show()

    # fig, ax = plt.subplots()
    # ax.hist(results["evalue"])
    # ax.set_title("histogram of evalues")
    # # ax.set_xticks([x/100.0 for x in range(90, 101, 1)])
    # # plt.savefig("hist_pos_scores.png")
    # plt.show()

    # fig, ax = plt.subplots()
    # ax.hist(results[results["evalue"]<0.001]["evalue"])
    # ax.set_title("histogram of evalues")
    # # ax.set_xticks([x/100.0 for x in range(90, 101, 1)])
    # # plt.savefig("hist_pos_scores.png")
    # plt.show()

    # ----- plot evalues ---------
    # results = results.sort_values(by="evalue").reset_index()
    # results["evalue"].plot(logy=True)
    # plt.show()

    # ----- stats -----
    print("total number of sequences: 1225")
    print("number of matches: ", results["qaccver"].count())
    print("number of matched sequences: ", results["qaccver"].nunique())
    print("number of sequences with a high quality match (evalue < 0.001): ", results[results["evalue"]<0.001]["qaccver"].nunique())
    print("matches: ")
    with pd.option_context('display.max_rows', None): 
        print(results[results["evalue"]<0.001])

    # ----- describe results ----------
    # print(results.describe())
    # print(results)    

def select_matches_good_evalue(files, location_new_files, evalue=MAXEVAL):
    files = glob.glob(files)
    for file_name in files:
        newfile = location_new_files + file_name.rsplit('/', 1)[1]
        results = pd.read_csv(file_name,delimiter=",")
        results[results["evalue"]<evalue].to_csv(newfile,sep=",")

def stats_all_datasets(csv_filename, files):
    # --- nr of matches, number of matched sequences, nr of matches with high quality match, nr of sequences with high quality match ----
    info={
        "file_name":[],
        "matches":[],
        "matched_sequences":[],
        "matches_evalue_lt_0.001":[],
        "matched_seqs_eval_lt_0.001":[]
    }
    files = glob.glob(files)
    for file_name in files:
        info["file_name"].append(file_name.split("/")[-1])
        results = pd.read_csv(file_name,delimiter=",")
        info["matches"].append(results["qaccver"].count())
        info["matched_sequences"].append(results["qaccver"].nunique())
        info["matches_evalue_lt_0.001"].append(results[results["evalue"]<0.001]["qaccver"].count())
        info["matched_seqs_eval_lt_0.001"].append(results[results["evalue"]<0.001]["qaccver"].nunique())
    df = pd.DataFrame(data=info)
    df.sort_values(by="file_name").reset_index(inplace=True)
    df.to_csv(csv_filename)


    
# stats_all_datasets("results_logs_stats/blast/blast_homo_sapiens_stats.csv", 'results_from_vsc/blast_results/homo_sapiens/*.csv')
# stats_all_datasets("results_logs_stats/blast/blast_ncORFs_contaminants_stats.csv", 'results_from_vsc/blast_results/ncORFs_contaminants/*.csv')

# select_matches_good_evalue('results_from_vsc/blast_results/ncORFs_contaminants/*.csv',"results_logs_stats/blast/good_e_values/ncORFs_contaminants/")
select_matches_good_evalue('results_from_vsc/blast_results/homo_sapiens/*.csv',"results_logs_stats/blast/good_e_values/homo_sapiens/")