#include <iostream>
#include <unordered_set>
#include <fstream>
#include <chrono>
#include <map>
#include <sstream>      // std::stringstream
using namespace std;


// command line arguments:
//    output file name (csv), input (csv) file names
int main(int argc, char **argv){
    // get command line argumetns
    if (argc < 3){
        std::cerr<<"not enough args"<<endl;
        return 2;
    }

    map<string, long> dataset_map;
    string line = "";   
    string title = "";   
    string dataset_id;


    for (size_t i = 2; i < argc; i++)
    {
        string input_file_name = argv[i];

        // input file
        ifstream input(input_file_name);  
        if (input.is_open()) {
            cout << "reading file: "<<input_file_name<<endl;
            // skip header line
            getline(input, line);
            getline(input, line);

            while (!input.eof()){
                dataset_id= line.substr(0,line.find("\t"));
                dataset_map[dataset_id] ++;
                getline(input, line);
            }
        }
        else {
            cerr << "problem with input file: " << input_file_name<<endl;
            return 3;
        }
    }
    // open and write to output file
    string output_file_name = argv[1];
    ofstream outfile(output_file_name);
    if (outfile.is_open()){
        outfile << "dataset id\tSpectra count"<<endl;
        for (map<string, long>::iterator it = dataset_map.begin(); it != dataset_map.end(); it++){
            outfile << it->first << "\t" << it->second << endl;
        }
        std::cout << "\nINFO: DONE!\nWrote PSM counts per dataset to "<< output_file_name <<endl;
    }
    else {
        cerr << "problem with output file: " << output_file_name<<endl;
        return 4;
    }
    outfile.close(); 
    return 0;
}

