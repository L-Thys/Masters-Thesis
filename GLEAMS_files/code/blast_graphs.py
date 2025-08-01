import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv("results_logs_stats/blast/blast_ncORFs_contaminants_stats.csv",delimiter=",")
temp = pd.read_csv("results_logs_stats/blast/initial_ncORFs_contaminants_analysis.csv",delimiter=",")
temp2 = pd.read_csv("results_logs_stats/blast/initial_ncORFs_contaminants_analysis_exact_matches.csv",delimiter=",")
df = pd.merge(df, temp, on="file_name")
df = pd.merge(df, temp2, on="file_name")
df=df.sort_values(by="matched_sequences")
df["index"]=range(0,len(df["file_name"]))


def plot0(df):
    df["percentage"] = df["matches_evalue_lt_0.001"]*100/df["matched_sequences"]
    df = df.sort_values(by='percentage')
    df[["file_name", "percentage"]].plot.bar(xlabel='', xticks=[], width=1, title="ncORFs and contaminants - percentage of blast matches with e-value < 0.001 by dataset")
    plt.show()
    

def plot1(df):
    df[["index", "matched_sequences", "matches_evalue_lt_0.001", "matches"]].plot(x="index",logy=True, xlabel='')
    plt.show()


def plot2(df):
    df=df.sort_values(by="matches_evalue_lt_0.001")
    df["index"]=range(0,len(df["file_name"]))
    df[["index", "matches_evalue_lt_0.001", "contaminant_matches", "ncORF_matches"]].plot(x="index",logy=True, xlabel='')
    plt.show()
    
    
def plot3(df):
    df[["index", "unique_contaminants", "unique_ncORFs"]].plot(x="index",logy=True, xlabel='')
    plt.show()
    

def plot4(df):
    df = df.sort_values(by='contaminant_matches')
    df["index"]=range(0,len(df["file_name"]))
    df[["index", "contaminant_matches", "unique_contaminants"]].plot(x="index",logy=True, xlabel='', title="number contaminant matches and number of unique contaminants (e-value < 0.001)")
    plt.show()   
    
def plot5(df):
    df=df[df["ncORF_matches"]>0]
    df = df.sort_values(by='ncORF_matches')
    df["index"]=range(0,len(df["file_name"]))
    df[["index", "unique_ncORFs"]].plot(x="index", xlabel='', title="number ncORF matches and number of unique ncORFS (e-value < 0.001)")
    plt.show()    

def plot6(df):
    df["percentage e-value < 0.001"] = df["matches_evalue_lt_0.001"]*100/df["matched_sequences"]
    df["percentage e-value < 0.001 and exact match"] = df["exact_matches"]*100/df["matched_sequences"]
    df = df.sort_values(by='percentage e-value < 0.001')
    df[["file_name", "percentage e-value < 0.001", "percentage e-value < 0.001 and exact match"]].plot.bar(xlabel='', xticks=[], width=1, title="ncORFs and contaminants - percentage of blast matches with with good e-value (and exact match (I=L)) by dataset")
    plt.show()

def plot7(df):
    df["percentage of matches with e-value < 0.001 that is a contaminant"] = df["contaminant_matches"]*100/df["matches_evalue_lt_0.001"]
    df = df.sort_values(by='percentage of matches with e-value < 0.001 that is a contaminant')
    df[["file_name", "percentage of matches with e-value < 0.001 that is a contaminant"]].plot.bar(xlabel='', xticks=[], width=1)
    plt.show()
    

def no_of_datasets_with_ncorfs(df):
    print("no of datasets with ncorf matches: ", df[df["ncORF_matches"]>0]["ncORF_matches"].count())

def no_of_datasets_with_exact_ncorfs(df):
    print("no of datasets with ncorf matches: ", df[df["exact_ncORF_matches"]>0]["exact_ncORF_matches"].count())

def percentage_of_peptides_with_single_protein_match():
    df = pd.read_csv("results_logs_stats/blast/peptides_single_match_homo_sapiens.csv",delimiter=",")
    peptides = df["casanovo_peptides_matched"].sum()
    single_matches=df["casanovo_peptides_with_single_match"].sum()
    print("for homo sapiens, "+str(single_matches/peptides*100)+" percent of matched peptides match only to a single protein")

    df = pd.read_csv("results_logs_stats/blast/peptides_single_match_ncORFs_contaminants.csv",delimiter=",")
    peptides = df["casanovo_peptides_matched"].sum()
    single_matches=df["casanovo_peptides_with_single_match"].sum()
    print("for the ncORFs and contaminants, "+str(single_matches/peptides*100)+" percent of matched peptides match only to a single protein")

    df = pd.read_csv("results_logs_stats/blast/peptides_single_match_exact_matches_homo_sapiens.csv",delimiter=",")
    peptides = df["casanovo_peptides_matched"].sum()
    single_matches=df["casanovo_peptides_with_single_match"].sum()
    print("for homo sapiens (exact matches only), "+str(single_matches/peptides*100)+" percent of matched peptides match only to a single protein")

    df = pd.read_csv("results_logs_stats/blast/peptides_single_match_exact_matches_ncORFs_contaminants.csv",delimiter=",")
    peptides = df["casanovo_peptides_matched"].sum()
    single_matches=df["casanovo_peptides_with_single_match"].sum()
    print("for the ncORFs and contaminants (exact matches only), "+str(single_matches/peptides*100)+" percent of matched peptides match only to a single protein")
    
def peptides_matching_ncORF_and_homo_sapiens():
    df = pd.read_csv("results_logs_stats/blast/matches_ncorf_homo_sapiens_intersection.csv",delimiter=",")
    peptides = df["homo_sapiens_and_ncorf_matched_peptides"].sum()
    print(peptides)




# plot0(df)
# plot1(df)
# plot2(df)
# plot3(df)
# plot4(df)
# plot5(df)
# plot6(df)
# plot7(df)
# no_of_datasets_with_ncorfs(df)
# no_of_datasets_with_exact_ncorfs(df)
# percentage_of_peptides_with_single_protein_match()
# peptides_matching_ncORF_and_homo_sapiens()
