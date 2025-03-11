import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv("results_logs_stats/spectra_and_psm_count_per_dataset.csv",delimiter=",", index_col=0)
temp = pd.read_csv("results_logs_stats/unfiltered_spectra_per_dataset.csv",delimiter="\t")
temp=temp.rename(columns={"Spectra count": "Unfiltered spectra count"})
df = pd.merge(df, temp, on="dataset id")
df= df.rename(columns={"Spectra count": "number of spectra not identified by GLEAMS", "Unfiltered spectra count":"total number of GLEAMS spectra"})
df=df.sort_values(by="number of spectra not identified by GLEAMS")
df["index"]=range(0,len(df["dataset id"]))

def plot0(df):
    df["percentage"] = df["PSM count"]*100/df["number of spectra not identified by GLEAMS"]
    df = df.sort_values(by='percentage')
    df[["dataset id", "percentage"]].plot.bar(xlabel='', xticks=[], width=0.8)
    plt.show()
    
def plot1 (df):
    df=df.rename(columns={"number of spectra not identified by GLEAMS":"Spectra count" })
    df[["index", "Spectra count", "PSM count"]].plot(x="index",logy=True, xlabel='', title="number of spectra and PSMs per dataset")
    plt.show()

    
def plot2 (df):
    df[["index","total number of GLEAMS spectra", "number of spectra not identified by GLEAMS" , "PSM count"]].plot(x="index",logy=True, xlabel='', title="number of spectra and PSMs per dataset")
    plt.show()
    
    
def plot3 (df):
    df[["index","total number of GLEAMS spectra", "number of spectra not identified by GLEAMS" ]].plot(x="index",logy=True, xlabel='', title="number of spectra per dataset")
    plt.show()
    
# plot1(df)
# plot2(df)
plot3(df)

