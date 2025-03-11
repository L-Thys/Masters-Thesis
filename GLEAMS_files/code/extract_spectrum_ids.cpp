#include <iostream>
#include <unordered_set>
#include <fstream>
#include <chrono>
using namespace std;


// command line arguments:
//    input (mgf) file name, output file name (csv)
int main(int argc, char **argv){
    // get command line argumetns
    if (argc != 3){
        return 2;
    }
    string mgf_file_name = argv[1];
    string output_file_name = argv[2];

    // open files
    ifstream mgf(mgf_file_name);
    ofstream outfile(output_file_name);

    if (mgf.is_open()) {
        cout << "reading file: "<<mgf_file_name<<endl;
        if (outfile.is_open()){
            int nr_of_spectra = 0;
            string line = "";   
            outfile<<"index\ttitle\n";
            while (!mgf.eof()){
                while (line.substr(0,5) != "TITLE" && !mgf.eof()){
                    getline(mgf, line);                
                }
                if (line.substr(0,5) == "TITLE"){
                    outfile << nr_of_spectra << "\t"<<line.substr(6)<<"\n";
                    nr_of_spectra ++;
                    getline(mgf, line);                
                }
            }
            std::cout << "\nINFO: DONE!\n"<< nr_of_spectra << " ids extracted" <<endl;
        }
        outfile.close();
        cout<<"created file (tab-sperated csv format): "<<output_file_name<<endl; 
    }
    mgf.close();

    return 0;
}