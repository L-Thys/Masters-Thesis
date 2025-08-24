#include <iostream>
#include <unordered_set>
#include <fstream>
#include <chrono>
using namespace std;

// command line arguments:
    //    input_file, filter_id_file, output_file_name, start_line, end_line
int main(int argc, char **argv){
    // get command line argumetns
    if (argc != 4){
        return 2;
    }
    string mgf_file = argv[1];
    string filter_file_name = argv[2];
    string output_file_name = argv[3];
   
    auto start = chrono::high_resolution_clock::now();
    // open files
    ifstream mgf(mgf_file);
    ifstream filter_file(filter_file_name);
    ofstream outfile(output_file_name);


    // prepare filter: set of ids of identified spectra
    unordered_set<string> filter;
    if (filter_file.is_open()) {
        string line;
        while (getline(filter_file, line)) {
            filter.insert(line+"\r");
        }
        filter_file.close();
        // cout << "filter size start: " << filter.size()<<endl;
    }else{
        cerr << "problem with opening filter file" <<endl;
        return 5;
    }

    // filter out the identified spectra
    if (mgf.is_open()) {
        if (outfile.is_open()){
            int nr_of_spectra = 0;
            int nr_of_spectra_removed = 0;
            string line = "";
            string out = "";
            while (!mgf.eof()){

                // start searching at BEGIN IONS
                while(line != "BEGIN IONS\r"){
                    if(mgf.eof()) break;
                    getline(mgf, line);
                }
                out += line +"\n";
                nr_of_spectra ++;

                // find TITLE=
                while(line.substr(0,5) != "TITLE"){
                    if(mgf.eof()) break;
                    getline(mgf, line);
                    out += line +"\n";
                }

                // skip empty lines at the end of files
                if(line.size()==0){
                    if(mgf.eof()) break;
                    getline(mgf, line);
                }
                                
                // see if the title can be found in filter
                auto search = filter.find(line.substr(6));
                if (search == filter.end()){
                    while(line!= "END IONS\r"){
                        if(mgf.eof()) break;
                        getline(mgf, line);
                        out += line +"\n";
                    }
                    outfile << out << "\n";
                }else{
                    // this spectrum has already been identified, remove from filter and move on to next spectrum
                    filter.erase(search);
                    nr_of_spectra_removed++;
                }

            }
            std::cout << nr_of_spectra << " spectra searched, " << nr_of_spectra_removed << " spectra removed" <<endl;
        }
        outfile.close();
    }
    mgf.close();

    auto stop = chrono::high_resolution_clock::now();
    auto duration = chrono::duration_cast<chrono::milliseconds>(stop - start);
    cout << "this calculation took "<< duration.count() <<" milliseconds"<< endl;

    return 0;
}