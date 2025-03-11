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
    string line = "";
    string score_string;
    float neutral_mass_diff;
    float calc_mz;
    float exp_mz;
    float charge;
    float score;

    string output_file_name = argv[1];
    ofstream outfile(output_file_name);
    if (outfile.is_open()){
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

                stringstream s(line);
                for (size_t i = 0; i < 15; i++)
                {
                    if (i==9){
                        score = stof(score_string);
                    }
                    else if (i==12){
                        charge = stof(score_string);
                    }
                    else if (i==13){
                        exp_mz = stof(score_string);
                    }
                    else if (i==14)
                    {
                        calc_mz= stof(score_string);
                    } 
                    
                    getline(s, score_string, '\t');
                }
                if(score <0 && score > -0.1){
                    neutral_mass_diff=(calc_mz - exp_mz) * charge;
                }
                outfile << neutral_mass_diff;
                
                getline(input,line);
                while (!input.eof()){
                    stringstream s(line);
                    for (size_t i = 0; i < 15; i++)
                    {
                        if (i==9){
                            score = stof(score_string);
                        }
                        else if (i==12){
                            charge = stof(score_string);
                        }
                        else if (i==13){
                            exp_mz = stof(score_string);
                        }
                        else if (i==14)
                        {
                            calc_mz= stof(score_string);
                        } 
                        getline(s, score_string, '\t');
                    }
                    neutral_mass_diff=(calc_mz - exp_mz) * charge;
                    if(score <0 && score > -0.1){
                        outfile <<',' << neutral_mass_diff;
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
    outfile.close(); 
    std::cout << "\nINFO: DONE!\nWrote neutral mass diffs to "<< output_file_name <<endl;

    return 0;
}