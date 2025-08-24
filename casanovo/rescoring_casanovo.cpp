#include <iostream>
#include <unordered_set>
#include <fstream>
#include <chrono>
#include <map>
#include <cmath>
#include <vector>
#include <sstream>      // std::stringstream
#include <unordered_set>
using namespace std;


// command line arguments:
//    input file name (mztab), output file name (mztab)
int main(int argc, char **argv){
    // get command line argumetns
    if (argc != 3){
        return 2;
    }
    string input_file_name = argv[1];
    string output_file_name = argv[2];

    // open files
    ifstream input(input_file_name);
    ofstream output(output_file_name);

    // rescoring casanovo scores
    if (input.is_open()) {
        cout << "reading file: "<<input_file_name<<endl;

        if (output.is_open()){
            string line;
            getline(input, line);

            // copying MTD and PSH lines to output file
            while (line.substr(0,3) != "PSM" && !input.eof()){
                output << line << endl;
                getline(input, line);         
            }

            vector<double> aa_scores;
            vector<string> row;
            while (!input.eof()){
                row.clear();
                aa_scores.clear();
                stringstream s(line);
                string word;
                // add all the column data of this row to a vector
                while (getline(s, word, '\t'))
                    {
                        row.push_back(word);
                    }
                
                // get search engine score, record if the score is negative
                // if negative calculate positive score
                double search_engine_score = stod(row[8]);
                bool neg_score = false;
                if (search_engine_score <0){
                    search_engine_score+= 1;
                    neg_score = true;
                }

                // get amino acid scores and put into vector
                stringstream aa_scores_string(row[19]);
                while (getline(aa_scores_string, word, ',')) {
                    aa_scores.push_back(stod(word));
                }

                // recalculate scores
                double sum = 0;
                // Undo the average of peptide score with AA scores: `aa_scores_new = aa_scores * 2 - peptide_score`
                for (size_t i = 0; i < aa_scores.size(); i++)
                {
                    aa_scores[i] = aa_scores[i]*2 - search_engine_score;
                    sum += log(aa_scores[i]);
                }
                // Calculate new peptide score as geometric mean of AA scores: `peptide_score_new = exp(mean(log(aa_scores_new)))`
                search_engine_score = exp(sum/aa_scores.size());
                // Recalculate AA scores: `aa_scores_new_new = (aa_scores_new + peptide_score_new) / 2`
                for (size_t i = 0; i < aa_scores.size(); i++)
                {
                    aa_scores[i] = (aa_scores[i]+search_engine_score)/2;
                }
                // if search engine score was negative, turn negative again
                if (neg_score) search_engine_score -=1;


                // write out columns to output file (up to search_engine_score)
                for (size_t i = 0; i < 8; i++)
                {
                    output << row[i] << "\t";
                }
                // write search engine score to output file
                output << search_engine_score << "\t";
                // write out columns to output file (up to amino acid scores)
                for (size_t i = 9; i < 19; i++)
                {
                    output << row[i] << "\t";
                }
                // write amino acid scores to output file
                for (int i = aa_scores.size()-1; i > 0; i--)
                {
                    output << aa_scores[i] << ",";
                }
                output << aa_scores[0];
                 // write out columns to output file (starting past amino acid scores)
                for (size_t i = 20; i < row.size(); i++)
                {
                    output <<"\t" << row[i];
                }
                output << endl;
                getline(input, line);         
            }
        } else {
            cerr << "problem opening output"<<endl;
            return 3;
        }
        output.close();
        cout << "writen to file: "<<output_file_name<<"\n"<<endl;
    }else {
        cerr << "problem opening input"<<endl;
        return 4;
    }
    input.close();
    return 0;
}