#include <iostream>
#include <vector>
#include <map>
#include <fstream>
#include <sstream>      // std::stringstream

using namespace std;


// command line arguments:
//   output file name (csv), (list of) input (mztab) file names
int main(int argc, char **argv){
    // get command line arguments
    if (argc < 3){
        return 2;
    }
    map<int, long> buckets;
    float bucket_width = 0.1; 
    string line = "";
    char terminal_char;
    string terminal;
    string score_string;

    // 
    vector<float> bucketing_values;
    float score=-1;
    while(score < 1.0+bucket_width){
        bucketing_values.emplace_back(score);
        score += bucket_width;
    }

    for (size_t i = 2; i < argc; i++)
    {
        string input_file_name = argv[i];

        // input file
        ifstream input(input_file_name);  
        if (input.is_open()) {
            cout << "reading file: "<<input_file_name <<endl;
            while (line.substr(0,3) != "PSM" && !input.eof()){
                getline(input, line);         
            }
            while (!input.eof()){
                stringstream s(line);
                for (size_t i = 0; i < 9; i++)
                {
                    getline(s, score_string, '\t');
                }
                score = stof(score_string);
                for (size_t i = 1; i < bucketing_values.size(); i++)
                {

                    if (score <= bucketing_values[i]){
                        buckets[i]++;
                        break;
                    }
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
    

    // open and write to output file
    string output_file_name = argv[1];
    ofstream outfile(output_file_name);
    if (outfile.is_open()){
        string label;
        outfile << "score bucket\tCount"<<endl;
        long sum = 0;
        for (size_t i = 1; i < bucketing_values.size(); i++){
            label = "]"+to_string(bucketing_values[i-1])+", "+to_string(bucketing_values[i])+"]";
            outfile << label << "\t" << buckets[i] << endl;
            sum += buckets[i];
        }
        cout << "sanity check: the sum of the buckets is "<<to_string(sum)<<endl; 
        std::cout << "\nINFO: DONE!\nWrote score counts to "<< output_file_name <<endl;
    }
    else {
        cerr << "problem with output file: " << output_file_name<<endl;
        return 4;
    }
    outfile.close(); 
    return 0;
}