#include <string>
#include <vector>
#include <cmath>
#include "solution.h"
#include <iostream>
using namespace std;

int return_nines(int n){
    int result = 0;
    for (int i=0;i<n;i++){
        result = result*10 + 9;
    }
    return result;
}

int get_nine_padded_number(int a){
    int n_digit = 1;
    int tmp_a = a;
    while(tmp_a>=10){
        ++n_digit;
        tmp_a = tmp_a/10;
    }
    return a*pow(10,3-n_digit) + return_nines(3-n_digit);
}

int compare(int a, int b){
    // input = 1~999
    int nine_padded_a = a;
    int nine_padded_b = b;
    
    nine_padded_a = get_nine_padded_number(a);
    nine_padded_b = get_nine_padded_number(b);
    if (nine_padded_a>nine_padded_b){
        return 1;
    }
    else if (nine_padded_a==nine_padded_b){
        return 0;
    }
    else{
        return -1;
    }
}

int* merge(int l[], int r[], int l_n, int r_n){
    int *a = (int *)malloc((l_n+r_n) * sizeof(int));
    int i=0;
    int j=0;
    int k=0;
    while (i<l_n && j<r_n){
        if (compare(l[i],r[j])==1||compare(l[i],r[j])==0){
            a[k]=l[i];
            i++;
        }
        else{
            a[k]=r[j];
            j++;
        }
        k++;
    }
    while (i<l_n){
        a[k]=l[i];
        i++;
        k++;
    }
    while (j<r_n){
        a[k]=r[j];
        j++;
        k++;
    }
    return a;
}

int* merge_sort(int a[], int length){
    if (length==1){
        return a;
    }
    int m = length/2;
    int *l = (int *)malloc(m * sizeof(int));
    int *r = (int *)malloc((length-m) * sizeof(int));
    for (int i=0;i<m;i++){
        l[i]=a[i];
    }
    for (int i=m;i<length;i++){
        r[i-m]=a[i];
    }
    int *left = merge_sort(l, m);
    int *right = merge_sort(r, length-m);
    int *result = merge(left,right,m,length-m);
    return result;
}

vector< vector<int> > classify_by_the_first_digit(vector<int> numbers){
    vector< vector<int> > groups;
    int first_digit = 0;
    int n_zeros = 0;
    int n_thousands = 0;
    // assign 0 and 1000 to the 0's group
    for (int i=1;i<10;i++){
        vector<int> group;
        groups.push_back(group);
    }
    for (int i=0;i<numbers.size();i++){
        if (numbers[i]==0){
            ++n_zeros;
            continue;
        }
        if (numbers[i]==1000){
            ++n_thousands;
            continue;
        }
        first_digit = numbers[i];
        while (first_digit>=10){
            first_digit = first_digit/10;
        }
        groups[first_digit].push_back(numbers[i]);
    }
    vector<int> thousands(n_thousands,1000);
    vector<int> zeros(n_zeros,0);   
    groups[0].insert(groups[0].end(), thousands.begin(), thousands.end());
    groups[0].insert(groups[0].end(), zeros.begin(), zeros.end());
    for (int i=1;i<10;i++){
        int length = groups[i].size();
        if (length==0){
            continue;  
        }
        int *sorted = merge_sort(&groups[i][0],length);
        groups[i] = vector<int>(sorted,sorted+length);
    }
    return groups;
}


string solution(vector<int> numbers){
    string answer = "";

    // select the numbers with the first digit i
    // all numbers transformed to 3-digit numbers
    // filling the empty digits with 9
    vector<vector<int>> groups;
    groups = classify_by_the_first_digit(numbers);
    for (int i=9;i>=0;i--){
        for (int j=0;j<groups[i].size();j++){
            answer += to_string(groups[i][j]);
        }
    }

    return answer;
}
