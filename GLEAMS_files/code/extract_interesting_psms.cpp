#include <iostream>
#include <utility>
#include <fstream>
#include <map>
#include <vector>
#include <sstream>      // std::stringstream
using namespace std;

// this code extracts the PSMs with a score > 0.9 or between -0.1 and 0 (strictly negative)
// can extract PSMs from multiple files and combine them into one file

// command line arguments:
//   output file name (mztab), (list of) input (mztab) file names
int main(int argc, char **argv){
    // get command line argumetns
    if (argc < 3){
        return 2;
        cerr << "Too few command line arguments" << endl;
    }

    // set variables for score requirements
    double POS_SCORE_REQ = 0.9;
    double NEG_SCORE_REQ = -0.1;
    
    // variable to keep track of number of interesting psms (maps inputfile name to pair (no of positive scores, no negative scores))
    map<string, pair<int,int>> PSM_stats;

    // open output file
    string output_file_name = argv[1];
    ofstream outfile(output_file_name);

    if (outfile.is_open()){
        string line;
        string psh;

        // write metadata section to output file
        // open first input file
        string input_file_name = argv[2];
        ifstream input(input_file_name);
        if (input.is_open()) {
            cout << "writing metadata section based on file "<<input_file_name << "\n" <<endl;

            // copy over the first lines of the mztab file
            for (size_t i = 0; i < 3; i++)
            {
                getline(input, line);
                outfile << line <<endl;
            }
            // add more information about specifics of file
            outfile << "MTD\tdescription\tCasanovo identification file " << output_file_name    
                << ". Compiled from multiple Casanovo identification runs (see ms_run[i]-location for identity of mgf files). "
                << "opt_ms_run[1]_aa_scores and search_engine_score[1] from Casanovo v4.2.1, recalculated so that search_engine_score[1] is geometric mean. " 
                << "Order of opt_ms_run[1]_aa_scores reversed from Casanovo v4.2.1 result to account for bug in Casanovo v4.2.1." << endl;
            // skip over original description & write out the rest of the metadata
            getline(input, line);
            while (line.substr(0,22) != "MTD\tms_run[1]-location" && !input.eof()){
                getline(input, line);         
                outfile << line << endl;
            }
            // keep PSH line to add later on
            getline(input, psh);
        }
        else {
            cerr << "problem with input file: " << input_file_name<<endl;
            return 3;
        }
        input.close();
        // add ms_run[x]-location for the rest of the input files
        for (size_t i = 3; i < argc; i++)
        {
            // open input file
            string input_file_name = argv[i];
            ifstream input(input_file_name);
            if (input.is_open()) {
                // skip to line that contains ms_run[1]-location
                line = "";
                while (line.substr(0,22) != "MTD\tms_run[1]-location" && !input.eof()){
                    getline(input, line);         
                }
                // write ms_run[i-1]-location to output file
                outfile << "MTD\tms_run[" << i-1 <<"]-location" << line.substr(22) << endl;
            }
            else {
                cerr << "problem with input file: " << input_file_name<<endl;
                return 3;
            }
            input.close();
        }
        outfile << psh << endl;
        // --- end of metadata section ---

        // for each input file: extract interesting PSMs and add to output file
        for (size_t i = 2; i < argc; i++)
        {
            vector<string> row;
            string word;

            // open input file
            string input_file_name = argv[i];
            ifstream input(input_file_name);
            if (input.is_open()) {
                int num_pos_psms = 0;
                int num_neg_psms = 0;
                cout << "extracting interesting PSMs from "<<input_file_name <<endl;

                // skip to PSM lines
                line = "";
                while (line.substr(0,3) != "PSM" && !input.eof()){
                    getline(input, line);         
                }

                while (!input.eof()){
                    row.clear();
                    stringstream s(line);
                    while (getline(s, word, '\t')){
                        // add all the column data
                        // of the row to a vector
                        row.push_back(word);
                    }
                    
                    // select psm if score is good enough
                    double score = stod(row[8]);
                    if( score > POS_SCORE_REQ || (score < 0 && score > NEG_SCORE_REQ)){
                        // keep track of stats
                        if (score > POS_SCORE_REQ){
                            num_pos_psms++;
                        }else{
                            num_neg_psms++;
                        }
                        // if i != 2, alter spectra_ref to have correct x in ms_run[x]
                        if (i!=2) {
                            row[14] = "ms_run["+to_string(i-1)+row[14].substr(8);
                        }

                        // write out columns to output file
                        outfile << row[0];
                        for (size_t i = 1; i < row.size(); i++)
                        {
                            outfile << "\t" << row[i];
                        }
                        outfile << endl;
                    } 
                    getline(input,line);
                }
                PSM_stats[input_file_name] = {num_pos_psms, num_neg_psms};
            }
            else {
                cerr << "problem with input file: " << input_file_name<<endl;
                return 3;
            }
            input.close();
        }
    }
    else {
        cerr << "problem with output file: " << output_file_name<<endl;
        return 4;
    }
    outfile.close();
    // write stats out to a file
        string stats_file_name = argv[1];
        ofstream statsfile(stats_file_name+"_stats.csv");
        if (statsfile.is_open()){
            int pos_stats=0;
            int neg_stats=0;
            statsfile << "filename\tnumber of interesting PSMs with positive score\tnumber of interesting PSMs with negative score\ttotal number of interesting PSMs"<<endl;
            for (size_t i = 2; i < argc; i++)
            {
                pos_stats += PSM_stats[argv[i]].first;
                neg_stats += PSM_stats[argv[i]].second;
                statsfile << argv[i] <<"\t"<< PSM_stats[argv[i]].first <<"\t" <<PSM_stats[argv[i]].second <<"\t" << PSM_stats[argv[i]].first+PSM_stats[argv[i]].second << endl;
            }
            statsfile << "total (" << output_file_name <<")\t"<< pos_stats <<"\t" <<neg_stats <<"\t" << pos_stats+neg_stats << endl;

        }
        else {
            cerr << "problem with output file: " << stats_file_name<<endl;
            return 4;
        }
        statsfile.close();

    cout << "\nINFO: DONE!\nwrote stats out to file "<< stats_file_name<< "_stats.csv"<<endl;
    cout << "wrote interesting PSMs to file" << output_file_name << endl;
 
    return 0;
}