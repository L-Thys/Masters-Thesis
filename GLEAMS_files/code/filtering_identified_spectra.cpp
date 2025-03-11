#include <iostream>
#include <unordered_set>
#include <fstream>
#include <chrono>
using namespace std;
// todo: start and end line 
//  - if endline != end ions: keep going to end ions
//  - if endline > number of lines, stop at nr of lines
//  - if endline = not given: to to end of file
//  - if startline != start ions, to to start ions and start filtering from there

// idea: each time a pattern matched it could be discarded from the next search iteration

// workflow:
//  - import ./mztab_files/ids_cluster_ident_2.txt & read into usefull (iterable?) list-type thingy
//  - read ./mgf_files/cluster_ident_2.mgf spectrum by spectrum (starting at startline & ending in end line)
//      - check if id is in list
//          - if id is not in list, copy whole spectrum over to output file (don't forget empty line in between)
//          - if id is in list, do not copy over, go to next spectrum

// command line arguments:
//    input_file, filter_id_file, number_of_output_files, start_line, end_line
int main(int argc, char **argv){
    // get command line argumetns
    if (argc != 6){
        return 2;
    }
    string mgf_file = argv[1];
    string filter_file_name = argv[2];
    string output_file_name = argv[3];
    long startline = 0;
    long endline = 0;
    try {
        startline = stol(argv[4]);
        endline = stol(argv[5]);
    }
    catch(const std::exception& e) {
        std::cerr << "problem with startline or endline: " <<  e.what() << '\n';
        return 3;
    }
    if (startline >= endline || startline < 0 || endline < 0){
        cerr << "invalid startline or endline" << endl;
        return 4;
    }

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
            long i = 0;
            while ( i < startline){
                getline(mgf, line);
                i++;
            }
            while (i<endline){
                string out = "";

                // start searching at BEGIN IONS
                while(line != "BEGIN IONS\r"){
                    getline(mgf, line);
                    i++;
                    if (i>= endline){
                        break;
                    }
                }
                if (i>= endline){
                    break;
                }
                out += line +"\n";
                nr_of_spectra ++;

                // find TITLE=
                while(line.substr(0,5) != "TITLE"){
                    getline(mgf, line);
                    out += line +"\n";
                    i++;
                }
                // see if the title can be found in filter
                auto search = filter.find(line.substr(6));
                if (search == filter.end()){
                    while(line!= "END IONS\r"){
                        getline(mgf, line);
                        out += line +"\n";
                        i++;
                    }
                    outfile << out << "\n";
                }else{
                    // this spectrum has already been identified, remove from filter and move on to next spectrum
                    filter.erase(search);
                    nr_of_spectra_removed++;
                }
            }
            std::cout <<  "searched up to line "<< i <<endl;
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