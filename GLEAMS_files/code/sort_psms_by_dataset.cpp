#include <iostream>
#include <utility>
#include <fstream>
#include <map>
#include <vector>
#include <sstream>      // std::stringstream
using namespace std;

// this code divides the psms by dataset and writes them to different files

// command line arguments:
//   output location (ending in "/"), (list of) input (mztab) file names
int main(int argc, char **argv){
    // get command line argumetns
    if (argc < 3){
        return 2;
        cerr << "Too few command line arguments" << endl;
    }
    
    // variable to keep track of number of interesting psms (maps inputfile name to pair (no of positive scores, no negative scores))
    map<string, bool> file_has_been_made;
    string psh = "";
    string output_location = argv[1];

    // 1. loop through input files
    //      1.0 fill psh 
    //      1.1 divide psms
    //      1.2 write out to output files
    //          1.2.1 if file has been used before, no need to add the PSH, otherwise, do this
    // 2. write out statistics

    // loop through input files
    for (size_t i = 2; i < argc; i++)
    {
        vector<string> row;
        string word;
        string line;

        // open input file
        string input_file_name = argv[i];
        ifstream input(input_file_name);
        if (input.is_open()) {
            map<string, vector<string>> datasets;
            std::cout << "reading file "<<input_file_name <<endl;

            // skip to PSH line
            line = "";
            while (line.substr(0,3) != "PSH" && !input.eof()){
                getline(input, line);         
            }

            // initialise the psh variable with the PSH line 
            if (psh.size() == 0) {
                psh = line;
            }

            // divide PSMs by dataset
            getline(input,line);
            while (!input.eof()){
                row.clear();
                stringstream s(line);
                while (getline(s, word, '\t')){
                    // add all the column data
                    // of the row to a vector
                    row.push_back(word);
                }
                
                // get the dataset id
                string dataset_id = row[21];
                datasets[dataset_id].push_back(line);
                getline(input,line);
            }
            // write to output
            for (auto it = datasets.begin(); it != datasets.end(); ++it) {
                string output_file_name = output_location+"PSMs_"+it->first+".csv";
                ofstream output(output_file_name,ios::app);
                if (output.is_open()){
                    if (file_has_been_made[it->first]!=true){
                        output << psh <<endl;
                        file_has_been_made[it->first]=true;
                    }
                    for (auto iter = it->second.begin(); iter != it->second.end(); ++iter)
                    {
                        output << *iter << endl;
                    }
                }
                else {
                    cerr << "problem with output file: " << output_file_name<<endl;
                    return 4;
                }
                output.close();
            }
        }
        else {
            cerr << "problem with input file: " << input_file_name<<endl;
            return 3;
        }
        input.close();
    }
    

    // if (outfile.is_open()){
    //     string line;
    //     string psh;

        
    //     // for each input file: extract interesting PSMs and add to output file
    //     for (size_t i = 2; i < argc; i++)
    //     {
    //         vector<string> row;
    //         string word;

    //         // open input file
    //         string input_file_name = argv[i];
    //         ifstream input(input_file_name);
    //         if (input.is_open()) {
    //             int num_pos_psms = 0;
    //             int num_neg_psms = 0;
    //             cout << "extracting interesting PSMs from "<<input_file_name <<endl;

    //             // skip to PSM lines
    //             line = "";
    //             while (line.substr(0,3) != "PSM" && !input.eof()){
    //                 getline(input, line);         
    //             }

    //             while (!input.eof()){
    //                 row.clear();
    //                 stringstream s(line);
    //                 while (getline(s, word, '\t')){
    //                     // add all the column data
    //                     // of the row to a vector
    //                     row.push_back(word);
    //                 }
                    
    //                 // select psm if score is good enough
    //                 double score = stod(row[8]);
    //                 if( score > POS_SCORE_REQ || (score < 0 && score > NEG_SCORE_REQ)){
    //                     // keep track of stats
    //                     if (score > POS_SCORE_REQ){
    //                         num_pos_psms++;
    //                     }else{
    //                         num_neg_psms++;
    //                     }
    //                     // if i != 2, alter spectra_ref to have correct x in ms_run[x]
    //                     if (i!=2) {
    //                         row[14] = "ms_run["+to_string(i-1)+row[14].substr(8);
    //                     }

    //                     // write out columns to output file
    //                     outfile << row[0];
    //                     for (size_t i = 1; i < row.size(); i++)
    //                     {
    //                         outfile << "\t" << row[i];
    //                     }
    //                     outfile << endl;
    //                 } 
    //                 getline(input,line);
    //             }
    //             PSM_stats[input_file_name] = {num_pos_psms, num_neg_psms};
    //         }
    //         else {
    //             cerr << "problem with input file: " << input_file_name<<endl;
    //             return 3;
    //         }
    //         input.close();
    //     }
    // }
    // else {
    //     cerr << "problem with output file: " << output_file_name<<endl;
    //     return 4;
    // }
    // outfile.close();


    // // write stats out to a file
    //     string stats_file_name = argv[1];
    //     ofstream statsfile(stats_file_name+"_stats.csv");
    //     if (statsfile.is_open()){
    //         int pos_stats=0;
    //         int neg_stats=0;
    //         statsfile << "filename\tnumber of interesting PSMs with positive score\tnumber of interesting PSMs with negative score\ttotal number of interesting PSMs"<<endl;
    //         for (size_t i = 2; i < argc; i++)
    //         {
    //             pos_stats += PSM_stats[argv[i]].first;
    //             neg_stats += PSM_stats[argv[i]].second;
    //             statsfile << argv[i] <<"\t"<< PSM_stats[argv[i]].first <<"\t" <<PSM_stats[argv[i]].second <<"\t" << PSM_stats[argv[i]].first+PSM_stats[argv[i]].second << endl;
    //         }
    //         statsfile << "total (" << output_file_name <<")\t"<< pos_stats <<"\t" <<neg_stats <<"\t" << pos_stats+neg_stats << endl;

    //     }
    //     else {
    //         cerr << "problem with output file: " << stats_file_name<<endl;
    //         return 4;
    //     }
    //     statsfile.close();

    // cout << "\nINFO: DONE!\nwrote stats out to file "<< stats_file_name<< "_stats.csv"<<endl;
    // cout << "wrote interesting PSMs to file" << output_file_name << endl;
 
    return 0;
}