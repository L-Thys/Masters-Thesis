#include <iostream>
#include <unordered_set>
#include <fstream>
#include <chrono>
using namespace std;


// command line arguments:
//    input (mgf) file name, output file name (csv)
int main(int argc, char **argv){
    // get command line argumetns
    if (argc < 2){
        return 2;
    }

    // open files
    long nr_of_lines = 0;
    string line = "";   


    // filter out the identified spectra
    for (size_t i = 1; i < argc; i++)
    {
        string input_file_name = argv[i];

        // input file
        ifstream input(input_file_name);  
        if (input.is_open()) {
            cout << "reading file: "<<input_file_name<<endl;
            while (!input.eof()){
                getline(input, line); 
                nr_of_lines ++;
                if (nr_of_lines%1000000==0){
                    cout << nr_of_lines<<endl;
                }
                
            }
        }
    }
    std::cout << "\nINFO: DONE!\n" << "nr of lines: " << nr_of_lines<<endl;
    return 0;
}