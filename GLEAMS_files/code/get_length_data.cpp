#include <iostream>
#include <utility>
#include <fstream>
#include <map>
#include <vector>
#include <iterator>
#include <algorithm>
#include <sstream>      // std::stringstream
using namespace std;

// this code extracts extracts the datset id, length of peptide and score of each match
// and writes them out to a file

// command line arguments:
//   output file name (mztab), (list of) input (mztab) file names
int main(int argc, char **argv){
    // get command line argumetns
    if (argc < 3){
        cerr << "Too few command line arguments" << endl;
        return 2;
    }
    
    // variable to keep track of number of interesting psms (maps inputfile name to pair (no of positive scores, no negative scores))
    int min_length = 1000;
    int max_length = 0;

    // open output file
    string output_file_name = argv[1];
    ofstream outfile(output_file_name);

    if (outfile.is_open()){
        string line;
        outfile << "dataset id\tlength of peptide\tscore" << endl;

        // for each input file: extract info and add to output file
        for (size_t i = 2; i < argc; i++)
        {
            vector<string> row;
            string word;

            // open input file
            string input_file_name = argv[i];
            ifstream input(input_file_name);
            if (input.is_open()) {
                cout << "reading "<<input_file_name <<endl;

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

                   
                    string peptide = row[1];
                    // take into account the fact that in some peptide sequences, a number (formatted like +57.04) is given instead of a amino acid character
                    // the numbers and points are removed, leaving only the plus sign to be counted as an amino acid
                    peptide.erase(std::remove_if(peptide.begin(), peptide.end(), ::isdigit), peptide.end());
                    peptide.erase(std::remove(peptide.begin(), peptide.end(), '.'), peptide.end());
                    peptide.erase(std::remove(peptide.begin(), peptide.end(), '+'), peptide.end());

                    int peptide_length = peptide.length();
                    string score = row[8];
                    string dataset_id = row[21];
                    
                    // keep track of min and max peptide lengths
                    if (min_length>peptide_length) min_length=peptide_length;
                    if (max_length<peptide_length) max_length=peptide_length;

                    outfile << row[21] << "\t" << peptide_length << "\t" << row[8] <<endl;
                    getline(input,line);
                }
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
    cout << "DONE! wrote peptide length data to file " << output_file_name << endl;
    cout << "smallest peptide has length " << min_length << ", largest has length " << max_length <<endl;
    return 0;
}