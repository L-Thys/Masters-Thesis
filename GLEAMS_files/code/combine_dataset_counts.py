import matplotlib.pyplot as plt
import glob
import pandas as pd

files = glob.glob('./GLEAMS_files/code/spectra_per_dataset_data/*.csv')

df = pd.read_csv(files.pop(),delimiter="\t")
 
i =0
for file_name in files:
    temp = pd.read_csv(file_name,delimiter="\t")
    temp=temp.rename(columns={"Spectra count": "Spectra count "+str(i)})
    i+=1
    df = pd.merge(df, temp, on="dataset id", how="outer")
    

df["sum"] = df.drop("dataset id",axis=1).sum(axis=1)


result = df[["dataset id","sum"]]

psms = pd.read_csv("./results_logs_stats/count_psms_per_dataset_filtered_cluster_ident.csv",delimiter=",")
result = pd.merge(result, psms, on="dataset id")
result = result.rename(columns={"sum":"Spectra count"})
result.to_csv("spectra_and_psm_count_per_dataset.csv")

