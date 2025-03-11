#include <iostream>
#include <vector>
#include <map>
#include <fstream>
#include <sstream>      // std::stringstream

using namespace std;


// command line arguments:
//   output file name (csv), (list of) input (mztab) file names
int main(int argc, char **argv){
    // get command line argumetns
    if (argc < 3){
        return 2;
    }
    map<string, long> amino_acid_map;
    string line = "";
    char terminal_char;
    string terminal;
    string sequence;

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
                for (size_t i = 0; i < 2; i++)
                {
                    getline(s, sequence, '\t');
                }
                terminal_char = sequence.back();
                if (terminal_char >= 48 && terminal_char <= 57){
                    terminal.clear();
                    while (terminal_char != '+'){
                        terminal.insert(0,1,terminal_char);
                        sequence.pop_back();
                        terminal_char = sequence.back();
                    }
                    terminal.insert(0,1,'+');
                }else{
                    terminal = terminal_char;
                }
                amino_acid_map[terminal] ++;
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
        outfile << "Amino Acid\tCount"<<endl;
        for (map<string, long>::iterator it = amino_acid_map.begin(); it != amino_acid_map.end(); it++){
            outfile << it->first << "\t" << it->second << endl;
        }
        std::cout << "\nINFO: DONE!\nWrote terminal amino acid counts to "<< output_file_name <<endl;
    }
    else {
        cerr << "problem with output file: " << output_file_name<<endl;
        return 4;
    }
    outfile.close(); 
    return 0;
}