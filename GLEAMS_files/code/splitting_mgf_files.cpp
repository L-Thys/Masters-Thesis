#include <iostream>
#include <unordered_set>
#include <fstream>
#include <chrono>
using namespace std;

// command line arguments:
//    input_file, number of spectra per output file, output_file_name
int main(int argc, char **argv){
    // get command line argumetns
    if (argc != 4){
        cerr << "failed: not correct number of command line arguments";
        return 2;
    }
    string mgf_file = argv[1];
    long spectra_per_file = 0;
    string output_file_name = argv[3];
    try {
        spectra_per_file = stol(argv[2]);
    }
    catch(const std::exception& e) {
        std::cerr << "problem with startline or endline: " <<  e.what() << '\n';
        return 3;
    }

    // open files
    ifstream mgf(mgf_file);

    int output_file_number = 0;

    // filter out the identified spectra
    if (mgf.is_open()) {
        long line_number = 0;
        bool got_to_end = false;

        while (!got_to_end){
            ofstream outfile(output_file_name+"_"+to_string(output_file_number)+".mgf");
            if (outfile.is_open()){
                string line = "";
                int nr_of_spectra = 0;
                while (nr_of_spectra<spectra_per_file && !mgf.eof()){
                    getline(mgf, line);
                    outfile << line +"\n";
                    if(line == "END IONS\r"){
                        nr_of_spectra ++;
                    }
                }
                if(mgf.eof()){
                    got_to_end = true;
                    cout << "file number "<<output_file_number<< " created"<<endl;
                    cout << output_file_number+1 << " files created"<<endl;
                    cout << "Last file contains " << nr_of_spectra << " files"<<endl;
                }else{
                    cout << "file number "<<output_file_number<< " created"<<endl;
                    output_file_number++;
                }
            }
            outfile.close();
        }
    
    }
    mgf.close();
    return 0;
}