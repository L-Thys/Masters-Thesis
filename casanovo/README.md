# Preprocessing
## Step 0: make sure the necessary input files are present
- from the project's root folder, in `data/input`, make sure that the following files are present:
    - `cluster_ident_2.mztab` and `cluster_ident_n.mztab`
    - `cluster_ident_2.mgf` and `cluster_ident_n.mgf`
- if these are not present, they can be downloaded with FTP from https://massive.ucsd.edu/ProteoSAFe/dataset_files.jsp?task=e899fe376adc48838d837e43697a3fb8
    - be aware that these files are close to 180 GB in total 

## Step 1: extract spectrum ids from mzTab files
- from project's root folder, run 
    ```
    python casanovo/extract_PSM_ids.py
    ```
- this generates files `data/input/cluster_ident_2_ids.txt` and `data/input/cluster_ident_n_ids.txt`

## Step 2: filter out identified spectra
- compile filtering_unidentified_spectra.cpp 
    ```  
    g++ casanovo/filtering_identified_spectra.cpp -o casanovo/filtering_identified_spectra
    ```    
- run filtering_identified_spectra twice
    ```
    casanovo/filtering_identified_spectra data/input/cluster_ident_n.mgf data/input/cluster_ident_n_ids.txt data/input/filtered_cluster_ident_n.mgf
    ``` 
    ```
    casanovo/filtering_identified_spectra data/input/cluster_ident_2.mgf data/input/cluster_ident_2_ids.txt data/input/filtered_cluster_ident_2.mgf
    ``` 
    - this creates files `filtered_cluster_ident_2.mgf` and `filtered_cluster_ident_n.mgf`
## Step 3: split spectra files into smaller files
- compile splitting_mgf_files.cpp
    ```  
    g++ casanovo/splitting_mgf_files.cpp -o casanovo/splitting_mgf_files
    ``` 

- run filtering_identified_spectra twice
    ```
    casanovo/splitting_mgf_files data/input/filtered_cluster_ident_2.mgf 50000 data/casanovo/split_mgf_files/filtered_cluster_ident_n 
    ```
    ```
    casanovo/splitting_mgf_files data/input/filtered_cluster_ident_2.mgf 50000 data/casanovo/split_mgf_files/filtered_cluster_ident_2 
    ```
# Casanovo
## step 1: compile `casanovo/add_spectrum_titles_to_mztab.cpp`
```g++ casanovo/add_spectrum_titles_to_mztab.cpp -o casanovo/add_spectrum_titles_to_mztab```
## Step 2: run casanovo on all files in `data/split_mgf_files`
- run `./casanovo/run_casanovo.sh`


# Selecting well scoring Casanovo results
## step 1: compiling
- compile `rescoring_casanovo.cpp`
```g++ casanovo/rescoring_casanovo.cpp -o casanovo/rescoring_casanovo```
- compile `extract_interesting_psms.cpp`
```g++ casanovo/extract_interesting_psms.cpp -o casanovo/extract_interesting_psms```
- compile `/sort_psms_by_dataset.cpp`
```g++ casanovo/sort_psms_by_dataset.cpp -o casanovo/sort_psms_by_dataset```

## step 2: selecting good results
- run `casanovo/rescoring_and_selecting_casanovo_results.sh`

## step 3: sort results according to dataset
- run `casanovo/results_per_dataset.sh`

