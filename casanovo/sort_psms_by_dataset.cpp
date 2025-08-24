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
    
    return 0;
}