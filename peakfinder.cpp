#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <sstream>
#include <climits>
using namespace std;

vector < vector<int> > read_file(string file_name){
    ifstream file(file_name);
    string line;
    vector< vector<int> > matrix;
    while (getline(file,line)){
        vector<int> row;
        stringstream iss(line);
        int n;
        while (iss >> n){
            row.push_back(n);
        }
        matrix.push_back(row);
    }
    return matrix;
}

void print_matrix(vector <vector<int>> matrix, int r, int c){
        for (int i=0;i<r;i++){
        for (int j=0;j<c;j++){
            cout << matrix[i][j] << " ";
        }
        cout << endl;
    }
}

int find_max_in_column(vector<vector<int>> matrix, int j){
    int max = INT_MIN;
    int max_i = 0;
    for (int i=0;i<matrix.size();i++){
        if (matrix[i][j]>max){
            max = matrix[i][j];
            max_i = i;
        }
    }
    return max_i;
}

int for_compare(vector<vector<int>> matrix, int i, int j){
    if (i<0 || i>=matrix.size() || j<0 || j>=matrix[0].size()){
        return INT_MIN;
    }
    else{
        return matrix[i][j];
    }
}

void peak_finder(vector<vector<int>> matrix, int& pr, int& pc, int& pv){
    int r = matrix.size();
    int c = matrix[0].size();
    int i=0;
    int j=c/2;
    int st_j=0;
    int ed_j=c;

    while (ed_j-st_j>=1){
        i = find_max_in_column(matrix, j);
        cout << "i: " << i << " j: " << j << " st_j: " << st_j << " ed_j: " << ed_j << endl; //debug
        if ((ed_j-st_j)==1){
            cout << "n_col==1" << endl; //debug
            pr = i;
            pc = st_j;
            pv = matrix[pr][pc];
            return;
        }
        i = find_max_in_column(matrix,j);
        if (for_compare(matrix, i, j-1) > for_compare(matrix, i, j)){
            cout << "pick left" << endl; //debug
            ed_j = j-1;
            j = (ed_j+st_j)/2;
            continue;
        }
        if (for_compare(matrix, i, j+1) > for_compare(matrix, i, j)){
            cout << "pick right" << endl; //debug
            st_j = j+1;
            j = (ed_j+st_j)/2;
            continue;
        }
        else{
            cout << "pick the current column" << endl; //debug
            pr = i;
            pc = j;
            pv = matrix[pr][pc];
            return;
        }
    }
}

int main(){
    string file_name;
    cout << "Please enter the file name (e.g. input.txt): " << endl;
    cin >> file_name;
    //file_name = "input.txt";
    vector< vector<int>  > matrix;
    matrix = read_file(file_name);
    int r = matrix.size();
    int c = matrix[0].size();

    print_matrix(matrix,r,c);

    int peak_r;
    int peak_c;
    int peak_v;

    peak_finder(matrix, peak_r, peak_c, peak_v);
    cout << "Peak value: " << peak_v << endl;
    cout << "Peak position: (" << peak_r + 1 << ", " << peak_c + 1 << ") " << endl;

}