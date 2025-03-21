#include <iostream>
#include <utility>
#include <fstream>
#include <map>
#include <vector>
#include <iterator>
#include <algorithm>
#include <sstream>      // std::stringstream
using namespace std;

// make two file with information on sections of repeated amino acids
// one output file will contain positive scores, the other negative ones
// expects columns of input to be "sequence, cleaned_sequence, search_engine_score[1], opt_ms_run[1]_aa_scores, title"


// command line arguments:
//   output file name (no filetype extension), input (csv) file name
int main(int argc, char **argv){
    // get command line argumetns
    if (argc < 3){
        cerr << "Too few command line arguments" << endl;
        return 2;
    }

    // open output file
    string output_file_name = argv[1];
    ofstream pos_outfile(output_file_name+"_pos.csv");
    ofstream neg_outfile(output_file_name+"_neg.csv");

    string sequence = "";

    if (pos_outfile.is_open()){
        if(neg_outfile.is_open()){
            string line;
            vector<string> row;
            string word;
            // open input file
            string input_file_name = argv[2];
            ifstream input(input_file_name);
    
            if (input.is_open()) {
                cout << "reading "<<input_file_name <<endl;
                pos_outfile << "cleaned_sequence\tsearch_engine_score[1]\ttitle\tlongest_repeat_length\tno_of_repeats_3_or_longer\tsequence_length" <<endl;
                neg_outfile << "cleaned_sequence\tsearch_engine_score[1]\ttitle\tlongest_repeat_length\tno_of_repeats_3_or_longer\tsequence_length" <<endl;
                getline(input, line); 
                getline(input, line); 
    
    
                while (!input.eof()){
                    row.clear();
                    stringstream s(line);
                    while (getline(s, word, '\t')){
                        // add all the column data
                        // of the row to a vector
                        row.push_back(word);
                    }
    
                    // calculate repeat info
                    sequence = row[1];
                    int sequence_length = 0;
                    int nr_repeats = 0;
                    int count = 1;
                    int longest_count = 1;
    
                    int maxC = 1;
                    for (int i=0; i<sequence.length(); i++){
                        if (sequence[i] == sequence[i+1] && i < sequence.length()-1)
                            count++;
                        else{
                            if (count >= 3) nr_repeats++;
                            if (count > longest_count) longest_count = count;
                            count=1;
                        }
                    }
    
                    if (stof(row[2])>0){
                        pos_outfile << sequence <<"\t" << row[2] << "\t" << row[4] << "\t" << longest_count << "\t" << nr_repeats << "\t" << sequence.length()<<endl;
                    }
                    else {
                        neg_outfile << sequence <<"\t" << row[2] << "\t" << row[4] << "\t" << longest_count << "\t" << nr_repeats << "\t" << sequence.length()<<endl;
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
    }
    else {
        cerr << "problem with output file: " << output_file_name<<endl;
        return 4;
    }
    pos_outfile.close();
    neg_outfile.close();
    cout << "\nINFO: DONE!"<<endl;
    cout << "wrote to "<<output_file_name <<"_pos.csv and "<<output_file_name <<"_neg.csv" <<endl;
    return 0;
}