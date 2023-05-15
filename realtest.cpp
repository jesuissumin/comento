#include <iostream>
#include <sstream>
#include <vector>
#include <regex>
#include <string>
using namespace std;

vector<int> parse_input(string int_s){
    vector<int> int_v;
    cout << int_s << endl;
    int_s.erase(remove(int_s.begin(),int_s.end(),' '),int_s.end());
    int_s.erase(remove(int_s.begin(),int_s.end(),'['),int_s.end());
    int_s.erase(remove(int_s.begin(),int_s.end(),']'),int_s.end());

    istringstream iss(int_s);
    string token;
    while (getline(iss,token,',')){
        cout << token << endl;
        int_v.push_back(stoi(token));
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
    for (int i=0;i<int_v.size();i++){
        cout << int_v[i] << " ";
    }
    cout << endl;
}