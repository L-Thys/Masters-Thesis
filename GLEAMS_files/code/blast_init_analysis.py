import pandas as pd
import glob

# MAXEVAL = 0.001

# # ----- load blast results for finding Streptavidin and human disulfide-isomerase in MSV000078777 --------
# # -- 457 matches --
# results = pd.read_csv("results_from_vsc/blast_results/result_blast_streptav_disisom.csv",delimiter=",")

# # ----- sort results by evalue ---------

# # ----- select matches with evalue < MAXEVAL -----------
# results = results[results["evalue"]<MAXEVAL]

# # ----- look at length query peptide - length of match ----------
# results["lengthdiff"] = results["qlen"] - results["length"]
# results["plengthdiff"] = results["lengthdiff"]/results["qlen"]

# # ----- show all results where the whole query sequence is in the match ---
# # --- this still includes some matches not in unipept (like when the pident is not large )
# with pd.option_context('display.max_rows', None, 'display.max_columns', None): 
#     print(results[results["lengthdiff"]==0][["qaccver","saccver","evalue","pident","sseq","qseq"]])


# # ----- describe results ----------
# # print(results.describe())
# # print(results)

def separating_out_ncorfs():
    files = glob.glob("results_logs_stats/blast/good_e_values/ncORFs_contaminants/*.csv")
    df = pd.read_csv(files.pop(),delimiter=",",index_col=0)
    df=df[~df["saccver"].str.startswith("CONT_")]

    for file_name in files:
        temp = pd.read_csv(file_name,delimiter=",",index_col=0)
        temp = temp[~temp["saccver"].str.startswith("CONT_")]
        if(temp["saccver"].count()>0):
            df = pd.concat([df, temp])
    df=df.reset_index()
    df.drop(labels="index",axis=1).to_csv("results_logs_stats/blast/good_e_values/ncORFs_only.csv")
    print(df["saccver"].nunique())

def contaminant_and_ncorfs():
    # --- nr of matches,  nr of matches with CONT_, number of unique CONT_s, number of matches with ncORFs, nr of matches with high quality match, nr of sequences with high quality match ----
    info={
        "file_name":[],
        "matches":[],
        "contaminant_matches":[],
        "unique_contaminants":[],
        "ncORF_matches":[],
        "unique_ncORFs":[],
    }
    files = glob.glob("results_logs_stats/blast/good_e_values/ncORFs_contaminants/*.csv")
    for file_name in files:
        info["file_name"].append(file_name.split("/")[-1])
        results = pd.read_csv(file_name,delimiter=",")
        info["matches"].append(results["saccver"].count())
        info["contaminant_matches"].append(results[results["saccver"].str.startswith("CONT_")]["saccver"].count())
        info["unique_contaminants"].append(results[results["saccver"].str.startswith("CONT_")]["saccver"].nunique())
        info["ncORF_matches"].append(results[~results["saccver"].str.startswith("CONT_")]["saccver"].count())
        info["unique_ncORFs"].append(results[~results["saccver"].str.startswith("CONT_")]["saccver"].nunique())
    df = pd.DataFrame(data=info)
    df.sort_values(by="file_name").reset_index(inplace=True)
    df.to_csv("results_logs_stats/blast/initial_ncORFs_contaminants_analysis.csv")


def contaminant_and_ncorfs_exact_matches():
    # --- nr of exact matches (I=L), nr of matches with CONT_, number of unique CONT_s, number of matches with ncORFs, nr of matches with high quality match, nr of sequences with high quality match ----
    info={
        "file_name":[],
        "exact_matches":[],
        "exact_contaminant_matches":[],
        "unique_contaminants_exact_match":[],
        "exact_ncORF_matches":[],
        "unique_ncORFs_exact_match":[],
    }
    files = glob.glob("results_logs_stats/blast/good_e_values/ncORFs_contaminants/*.csv")
    for file_name in files:
        info["file_name"].append(file_name.split("/")[-1])
        results = pd.read_csv(file_name,delimiter=",")
        results= results[results["qseq"].str.replace('I','L')==results["sseq"].str.replace('I','L')]
        info["exact_matches"].append(results["saccver"].count())
        info["exact_contaminant_matches"].append(results[results["saccver"].str.startswith("CONT_")]["saccver"].count())
        info["unique_contaminants_exact_match"].append(results[results["saccver"].str.startswith("CONT_")]["saccver"].nunique())
        info["exact_ncORF_matches"].append(results[~results["saccver"].str.startswith("CONT_")]["saccver"].count())
        info["unique_ncORFs_exact_match"].append(results[~results["saccver"].str.startswith("CONT_")]["saccver"].nunique())
    df = pd.DataFrame(data=info)
    df.sort_values(by="file_name").reset_index(inplace=True)
    df.to_csv("results_logs_stats/blast/initial_ncORFs_contaminants_analysis_exact_matches.csv")

def peptides_with_single_match(blast_run):
    info={
        "file_name":[],
        "matches":[],
        "casanovo_peptides_matched":[],
        "casanovo_peptides_with_single_match":[],
        "casanovo_peptides_with_multiple_matches":[]
    }
    files = glob.glob("results_logs_stats/blast/good_e_values/"+blast_run+"/*.csv")
    for file_name in files:
        info["file_name"].append(file_name.split("/")[-1])
        results = pd.read_csv(file_name,delimiter=",")
        info["matches"].append(results["saccver"].count())
        info["casanovo_peptides_matched"].append(results["qaccver"].nunique())
        value_counts=results.groupby("qaccver")["saccver"].nunique()
        info["casanovo_peptides_with_single_match"].append(value_counts[value_counts==1].sum())
        info["casanovo_peptides_with_multiple_matches"].append(value_counts[value_counts!=1].count())
    df = pd.DataFrame(data=info)
    df.sort_values(by="file_name").reset_index(inplace=True)
    df.to_csv("results_logs_stats/blast/peptides_single_match_"+blast_run+".csv")

def peptides_with_single_match_for_exact_matches(blast_run):
    info={
        "file_name":[],
        "matches":[],
        "casanovo_peptides_matched":[],
        "casanovo_peptides_with_single_match":[],
        "casanovo_peptides_with_multiple_matches":[]
    }
    files = glob.glob("results_logs_stats/blast/good_e_values/"+blast_run+"/*.csv")
    for file_name in files:
        info["file_name"].append(file_name.split("/")[-1])
        results = pd.read_csv(file_name,delimiter=",")
        results= results[results["qseq"].str.replace('I','L')==results["sseq"].str.replace('I','L')]
        info["matches"].append(results["saccver"].count())
        info["casanovo_peptides_matched"].append(results["qaccver"].nunique())
        value_counts=results.groupby("qaccver")["saccver"].nunique()
        info["casanovo_peptides_with_single_match"].append(value_counts[value_counts==1].sum())
        info["casanovo_peptides_with_multiple_matches"].append(value_counts[value_counts!=1].count())
    df = pd.DataFrame(data=info)
    df.sort_values(by="file_name").reset_index(inplace=True)
    df.to_csv("results_logs_stats/blast/peptides_single_match_exact_matches_"+blast_run+".csv")

def peptides_matching_ncORF_and_homo_sapiens():
    info={
        "file_name":[],
        "ncorf_matched_peptides":[],
        "homo_sapiens_matched_peptides":[],
        "homo_sapiens_and_ncorf_matched_peptides":[],
        "exact_ncorf_matched_peptides":[],
        "exact_homo_sapiens_matched_peptides":[],
        "exact_homo_sapiens_and_ncorf_matched_peptides":[],
    }
    files = glob.glob("results_logs_stats/blast/good_e_values/ncORFs_contaminants/*.csv")
    for file in files:
        file_name=file.split("/")[-1]
        info["file_name"].append(file_name)
        ncorfs = pd.read_csv(file,delimiter=",")
        ncorfs=ncorfs[~ncorfs["saccver"].str.startswith("CONT_")]
        homo = pd.read_csv("results_logs_stats/blast/good_e_values/homo_sapiens/"+file_name,delimiter=",")
        ncorf_pepts = ncorfs["qaccver"].unique()
        homo_pepts = homo["qaccver"].unique()
        both_pepts=list(set(ncorfs) & set(homo_pepts))
        info["ncorf_matched_peptides"].append(len(ncorf_pepts))
        info["homo_sapiens_matched_peptides"].append(len(homo_pepts))
        info["homo_sapiens_and_ncorf_matched_peptides"].append(len(both_pepts))
        ncorfs= ncorfs[ncorfs["qseq"].str.replace('I','L')==ncorfs["sseq"].str.replace('I','L')]
        homo= homo[homo["qseq"].str.replace('I','L')==homo["sseq"].str.replace('I','L')]
        ncorf_pepts = ncorfs["qaccver"].unique()
        homo_pepts = homo["qaccver"].unique()
        both_pepts=list(set(ncorfs) & set(homo_pepts))
        info["exact_ncorf_matched_peptides"].append(len(ncorf_pepts))
        info["exact_homo_sapiens_matched_peptides"].append(len(homo_pepts))
        info["exact_homo_sapiens_and_ncorf_matched_peptides"].append(len(both_pepts))
    df = pd.DataFrame(data=info)
    df.sort_values(by="file_name").reset_index(inplace=True)
    df.to_csv("results_logs_stats/blast/matches_ncorf_homo_sapiens_intersection.csv")

def mismatches(blast_run):
    info={
        "file_name":[],
        "matches":[],
        "biggest_mismatches":[],
        "median_mismatch":[],
        "median_mismatch_with_exact_matches":[],
        "highest_percentage_mismatched":[],
        "median_percentage_mismatched":[],
        "median__percentage_mismatch_with_exact_matches":[],
    }
    mismatches
    files = glob.glob("results_logs_stats/blast/good_e_values/"+blast_run+"/*.csv")
    for file_name in files:
        info["file_name"].append(file_name.split("/")[-1])
        results = pd.read_csv(file_name,delimiter=",")
        mis= results.apply(lambda x: sum(1 for a, b in zip(x["qseq"].replace('I','L'), x["sseq"].replace('I','L')) if a != b),axis=1)
        mis["length"]=results["length"]
        mismatches = pd.concat([mis,mismatches])

    print("max mismatch: ", mismatches.max())
    print("median mismatch: ", mismatches[mismatches!=0].median())
    print("median mismatch (with exact matches): ", mismatches.median())
    print("max percentage mismatch: ", (mismatches/mismatches["length"]).max())
    

# contaminant_and_ncorfs()
# contaminant_and_ncorfs_exact_matches()
# separating_out_ncorfs()
# peptides_with_single_match("ncORFs_contaminants")
# peptides_with_single_match("homo_sapiens")
# peptides_with_single_match_for_exact_matches("ncORFs_contaminants")
# peptides_with_single_match_for_exact_matches("homo_sapiens")
# peptides_matching_ncORF_and_homo_sapiens()
mismatches("ncORFs_contaminants")
mismatches("homo_sapiens")


# results = pd.read_csv("results_logs_stats/blast/good_e_values/ncORFs_contaminants/fasta_sequences_PSMs_MSV000080679.csv",delimiter=",")
# print(results[~results["saccver"].str.startswith("CONT_")])
