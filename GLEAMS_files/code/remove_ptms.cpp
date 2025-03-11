#include <iostream>
#include <utility>
#include <fstream>
#include <map>
#include <vector>
#include <iterator>
#include <algorithm>
#include <sstream>      // std::stringstream
using namespace std;

// this code adds a column that lists the sequence without any TPMs

// command line arguments:
//   output file name (csv), input (csv) file name
int main(int argc, char **argv){
    // get command line argumetns
    if (argc < 3){
        cerr << "Too few command line arguments" << endl;
        return 2;
    }

    // open output file
    string output_file_name = argv[1];
    ofstream outfile(output_file_name);
    int i =0;


    if (outfile.is_open()){
        string line;
        vector<string> row;
        string word;
        // open input file
        string input_file_name = argv[2];
        ifstream input(input_file_name);
        if (input.is_open()) {
            // cout << "reading "<<input_file_name <<endl;
            getline(input, line); 
            outfile<<line<<"\tcleaned_sequence"<<endl;
            getline(input, line);

            while (!input.eof()){
                i++;
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
                peptide.erase(std::remove(peptide.begin(), peptide.end(), '-'), peptide.end());

                outfile<<line<<"\t"<<peptide<<endl;
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
    // cout << "\nINFO: DONE!"<<endl;
    // cout << "wrote to "+output_file_name<<endl;
    // cout << "number of psms: "<< i <<endl;
    cout <<i<<endl;
    return 0;
}