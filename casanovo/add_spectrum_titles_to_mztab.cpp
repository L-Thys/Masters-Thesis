#include <iostream>
#include <unordered_set>
#include <fstream>
#include <chrono>
#include <map>
#include <vector>
#include <sstream>      // std::stringstream
#include <unordered_set>
using namespace std;


// command line arguments:
//    input file name (mgf), mztab file name (mztab), output file name (mztab)
int main(int argc, char **argv){
    // get command line argumetns
    if (argc != 4){
        return 2;
    }
    string mgf_file_name = argv[1];
    string mztab_file_name = argv[2];
    string output_file_name = argv[3];

    // open mgf file
    ifstream mgf(mgf_file_name);

    // get ids
    map<int, string> titles;
    if (mgf.is_open()) {
        cout << "reading file: "<<mgf_file_name<<endl;
        int nr_of_spectra = 0;
        string line = "";
        string title = "";
        while (!mgf.eof()){
            while (line.substr(0,5) != "TITLE" && !mgf.eof()){
                getline(mgf, line);
            }
            if (line.substr(0,5) == "TITLE"){
                title =line.substr(6);
                title.pop_back(); // to remove "\r"
                titles[nr_of_spectra] = title;
                nr_of_spectra ++;
                getline(mgf, line);
            }
        }
        std::cout << "INFO: "<< nr_of_spectra << " titles extracted\n" <<endl;
    }
    else {
	cerr << "problem with inputfile: " << mgf_file_name<<endl;
	return 3;
    }
    mgf.close();

    // open mztab files
    ifstream mztab(mztab_file_name);
    ofstream output(output_file_name);

    // add ids to mzab file
    if (mztab.is_open()) {
        cout << "reading file: "<<mztab_file_name<<endl;
        unordered_set<string> spectra_ids_added;
        int nr_of_titles_added = 0;
        vector<string> row;
        vector<string> title_parts;
        string word;
        string title_part;
        string spectra_ref;
        string line;
        string title;
        getline(mztab, line);

        if (output.is_open()){
            while (line.substr(0,3) != "PSH" && !mztab.eof()){
                output << line << endl;
                getline(mztab, line);
            }
            // line contains the PSH line
            output << line << "\ttitle\tMassIVE_dataset_id\tfile_name\tscan_number" << endl;
            getline(mztab, line);

            while (!mztab.eof()){
                row.clear();
                stringstream s(line);
                while (getline(s, word, '\t'))
                    {
                        // add all the column data
                        // of a row to a vector
                        row.push_back(word);
                    }
                spectra_ref = row[14];
                try
                {
                    // the spectra ref is of format 'ms_run[1]:index=0'
                    title = titles.at(stoi(spectra_ref.substr(16)));
                    stringstream t(title);
                    title_parts.clear();
                    // titles follow format mzspec:\<MassIVE dataset id>:\<file name>:scan:\<scan number>
                    while (getline(t, title_part, ':'))
                    {
                        // add all the column data
                        // of a row to a vector
                        title_parts.push_back(title_part);
                    }
                    output << line << "\t" << title << "\t" << title_parts[1] << "\t" << title_parts[2] << "\t" << title_parts[4] <<endl;
                    nr_of_titles_added ++;
                    spectra_ids_added.insert(title);
                }
                catch(const std::out_of_range& ex)
                {
                    cerr << "ERROR: did not find title for spectra_ref" << spectra_ref<<endl;
                    output << line << "\t" << endl;
                }
                getline(mztab, line);
            }
        }
	else {
		cerr << "problem with output file: " << output_file_name<<endl;
        	return 4;
    	}
        output.close();
        std::cout << "\nINFO: DONE!\n";
        cout << "writing to file: "<<output_file_name<<endl;
        cout << nr_of_titles_added << " titles added" <<endl;
        cout << spectra_ids_added.size() << " unique titles added" <<endl;
    }
    else {
        cerr << "problem with mztab file: " << mztab_file_name<<endl;
        return 5;
    }

    mztab.close();
    return 0;
}
