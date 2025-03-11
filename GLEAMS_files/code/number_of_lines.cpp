#include <iostream>
#include <fstream>
using namespace std;

int main(int argc, char **argv){
    // open file
    ifstream mgf( argv[1]);

    if (mgf.is_open()) {
        long i = 0;  
        string line = "";
  
        while ( mgf.peek()!=EOF){
            getline(mgf, line);
            i++;
        }
        
        cout << "number of lines: "<< i << endl;
    
    }

    return 0;
}