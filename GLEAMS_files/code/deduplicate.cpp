#include <iostream>
#include <utility>
#include <fstream>
#include <map>
#include <vector>
#include <iterator>
#include <algorithm>
#include <sstream>      // std::stringstream
using namespace std;

// deduplicate based on sequence in column COL, keeping best score (from third column)
// assumes file has been sorted on column COL


// command line arguments:
//   output file name (csv), input (csv) file name
int main(int argc, char **argv){
    // get command line argumetns
    if (argc < 3){
        cerr << "Too few command line arguments" << endl;
        return 2;
    }

    int COL = 1;
    // open output file
    string output_file_name = argv[1];
    ofstream outfile(output_file_name);
    string current_match = "";
    float current_best_score;
    string current_best_psm;

    if (outfile.is_open()){
        string line;
        vector<string> row;
        string word;
        // open input file
        string input_file_name = argv[2];
        ifstream input(input_file_name);
        if (input.is_open()) {
            cout << "reading "<<input_file_name <<endl;
            outfile << "sequence\tcleaned_sequence\tsearch_engine_score[1]\topt_ms_run[1]_aa_scores\ttitle" <<endl;
            getline(input, line); 

            while (!input.eof()){
                if (line == "sequence\tcleaned_sequence\tsearch_engine_score[1]\topt_ms_run[1]_aa_scores\ttitle") continue;
                row.clear();
                stringstream s(line);
                while (getline(s, word, '\t')){
                    // add all the column data
                    // of the row to a vector
                    row.push_back(word);
                }
                if (row[COL]==current_match){
                    if (stof(row[2])>current_best_score){
                        current_best_psm = line;
                    current_best_score = stof(row[2]);
                    }
                }
                else {
                    outfile << current_best_psm << endl;
                    current_match = row[COL];
                    current_best_psm = line;
                    current_best_score = stof(row[2]);
                }
                getline(input,line);
            }
        }
        else {
            cerr << "problem with input file: " << input_file_name<<endl;
            return 3;
        }
        input.close();
    
    }
    else {
        cerr << "problem with output file: " << output_file_name<<endl;
        return 4;
    }
    outfile.close();
    cout << "\nINFO: DONE!"<<endl;
    cout << "wrote to "+output_file_name<<endl;
    return 0;
}