#include <iostream>
#include <utility>
#include <fstream>
#include <map>
#include <vector>
#include <iterator>
#include <algorithm>
#include <sstream>      // std::stringstream
using namespace std;

// this code makes a file that lists the psms with only following columns: sequence, cleaned_sequence, search_engine_score[1], opt_ms_run[1]_aa_scores,	title
// the input needs to already include the cleaned_sequence column


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


    if (outfile.is_open()){
        string line;
        vector<string> row;
        string word;
        // open input file
        string input_file_name = argv[2];
        ifstream input(input_file_name);
        if (input.is_open()) {
            cout << "reading "<<input_file_name <<endl;
            getline(input, line); 
            outfile << "sequence\tcleaned_sequence\tsearch_engine_score[1]\topt_ms_run[1]_aa_scores\ttitle" <<endl;
            getline(input, line);

            while (!input.eof()){
                row.clear();
                stringstream s(line);
                while (getline(s, word, '\t')){
                    // add all the column data
                    // of the row to a vector
                    row.push_back(word);
                }
                
                outfile<<row[1]<<"\t"<<row[24]<<"\t"<<row[8]<<"\t"<<row[19]<<"\t"<<row[20]<<"\t"<<endl;
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