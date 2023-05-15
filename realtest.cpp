#include <iostream>
#include <sstream>
#include <vector>
#include <regex>
#include <string>
#include "solution.h"
using namespace std;

vector<int> parse_input(string int_s){
    vector<int> int_v;
    cout << int_s << endl;
    int_s.erase(remove(int_s.begin(),int_s.end(),' '),int_s.end());
    int_s.erase(remove(int_s.begin(),int_s.end(),'['),int_s.end());
    int_s.erase(remove(int_s.begin(),int_s.end(),']'),int_s.end());

    istringstream iss(int_s);
    string token;
    int i,n;
    while (getline(iss,token,',')){
        if (n>=1000000){
            cout << "ERROR: exceeds maximum numbers 1000,000" << endl;
            exit(1);
        }
        i = stoi(token);
        if (i<0 || i>1000){
            cout << "ERROR: " << i << " is out of range 0~1000" << endl;
            exit(1);
        }
        int_v.push_back(i);
        ++n;
    }
    return int_v;
}

int main(){
    string int_s;
    cout << "Please enter a sequence of zero or positive integers separated by comma: " << endl;
    cout << "1) each interger should be less than 1,000" << endl;
    cout << "2) the lenght of the sequence should be less than 1000,000" << endl;
    cout << "e.g.: [0,12,245,38]" << endl;
    getline(cin,int_s);

    vector<int> int_v = parse_input(int_s);

    cout << "input seq:" << endl;
    int print_upto = 5;
    if (int_v.size()<print_upto){
        print_upto = int_v.size();
    }
    for (int i=0;i<print_upto;i++){
        cout << int_v[i] << " ";
    }
    int (int_v.size()>print_upto) ? cout << "..." << endl : cout << endl;

    string answer;
    answer = solution(int_v);
    cout << "output: " << answer << endl;
    return 0;
}
