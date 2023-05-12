#include <iostream>
#include <ctime>
using namespace std;

int *gen_array(int n, int type)
{
    int *a = (int *)malloc(n * sizeof(int));
    if (type==0){
        for (int i=0;i<n;i++){
            a[i]=i+1;
        }
    }

    if (type==1){
        for (int i=0;i<n;i++){
            a[i]=n-i;
        }
    }
    
    if (type==2){
        for (int i=0;i<n;i++){
            a[i]=i+1;
        }
        random_shuffle(&a[0],&a[n]);
    }
    
    return a;
}

void insertion_sort(int *a, int length){
    for (int i=1;i<length;i++){
        int q = a[i];
        int j = i-1;
        while (j>=0 && a[j]>q){
            a[j+1]=a[j];
            j--;
        }
        a[j+1]=q;
    }
}

// merge sort
int* merge(int l[], int r[], int l_n, int r_n){
    int *a = (int *)malloc((l_n+r_n) * sizeof(int));
    int i=0;
    int j=0;
    int k=0;
    while (i<l_n && j<r_n){
        if (l[i]<=r[j]){
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

// quick sort
void quick_sort(int *a, int st, int ed){
    if (ed-st<1){
        return;
    }
    int p = a[ed-1]; // pivot = last element
    int i = st-1;
    for (int j=st;j<ed-1;j++){
        if (a[j]<=p){
            i++;
            swap(a[i],a[j]);
        }
    }

    swap(a[i+1],a[ed-1]);
    quick_sort(a,st,i+1);
    quick_sort(a,i+2,ed);
}


void print_array(int a[]){
    int n = 10;
    for (int i=0;i<n;i++){
        cout << a[i] << " ";
    }
}

int main(){
    // cout << "the length of the array: " ;
    // int n;
    // cin >> n;
    // cout << endl;
    int n = 1000000
    string arr_type[3] = {"ascending", "descending", "random"};
    string sort_type[3] = {"insertion", "merge", "quick"};

    for (int i=0;i<3;i++){
        int *arr = gen_array(n, i);
        int result[n];
        cout << arr_type[i] << " order " << endl;
        for (int j=0;j<3;j++){
            clock_t st = clock();
            if (j==0){
                copy(arr, arr+n,result);
                insertion_sort(result, n);
            }
            if (j==1){
                int *result;
                result = merge_sort(arr, n);
            }
            if (j==2){
                copy(arr, arr+n,result);
                quick_sort(result, 0, n);
            }
            clock_t et = clock();
            cout << sort_type[j] << " sort time: " \
                << difftime(et,st)/CLOCKS_PER_SEC << "s" << endl;
            cout << "input: "<< " ";
            print_array(arr); 
            cout << endl;
            cout << "output: " << " ";
            print_array(result); 
            cout << endl;
        }
        cout << endl;
    }
    return 0;
}