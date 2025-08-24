import csv

input_files = ["data/input/cluster_ident_2.mztab", "data/input/cluster_ident_n.mztab"]
output_files = ["data/input/cluster_ident_2_ids.txt", "data/input/cluster_ident_n_ids.txt"]

for i in range(len(input_files)):
    with open(output_files[i], "w") as outputfile:
        outputfile.write("")

    with open(output_files[i], "a") as outputfile:
        with open(input_files[i], "r") as csvfile:
            csvreader = csv.reader(csvfile, delimiter="\t")

            for x in range(43):
            # This skips the first rows of the mzTab file.
                next(csvreader)
            for row in csvreader:
                outputfile.write(row[2]+"\n")
        
