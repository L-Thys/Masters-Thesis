#include <iostream>
#include <unordered_set>
#include <fstream>
#include <chrono>
using namespace std;


// command line arguments:
//    input (mgf) file name, output file name (csv)
int main(int argc, char **argv){
    cout << argc <<endl;
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
            string title="";
            string dataset_id="";
            outfile<<"dataset\ttitle\n";
            while (!mgf.eof()){
                while (line.substr(0,5) != "TITLE" && !mgf.eof()){
                    getline(mgf, line);                
                }
                if (line.substr(0,5) == "TITLE"){
                    title = line.substr(13);
                    dataset_id = title.substr(0, title.find(":"));
                    outfile << dataset_id << "\t"<<line.substr(6)<<"\n";
                    nr_of_spectra ++;
                    getline(mgf, line);                
                }
                if (nr_of_spectra%1000000==0){
                    std::cout<<"read "<< nr_of_spectra << " spectra" <<endl;
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