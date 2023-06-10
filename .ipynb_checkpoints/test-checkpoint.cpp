#include <iostream>
#include <vector>

using namespace std;

int k = 2;

void nextflag(vector<int> &flag) {
    int n = flag.size();
    if (flag[n - 1] == n - 2) {
        flag.clear();
        return;
    }
    int j = 1;
    for (int i = n - 1; i >= 2; i--) {
        if (flag[i-1] != flag[i] - 1) {
            j = i;
            break;
        }
    }
    flag[j]--;
    for (int i = j+1; i < n; i++) {
        flag[i] = k*i - 1;
    }
}

void nextdfa(vector<int> &last, vector<int> &flag) {
    int j = 0;
    int l = 1;
    int n = flag.size();
    if (last.size() != 0) {
        int i = n - 1;
        for (j = k*n - 1; j > 0; j--) {
            if (i != 0 && flag[i] == j) {
                i--;
            }
            else if (last[j] < i) {
                break;
            }
        }
        
        if (j == 0 && (flag[1] == 1 || last[0] == 1)) {
            last.clear();
            return;
        }
        else {
            last[j]++;
            j++;
            l = i+1;
        }
    }
    else {
        for (int i = 0; i < k*n; i++) {
            last.push_back(0);
        }
        for (int i = 0; i < n; i++) {
            last[flag[i]] = i;
        }
    }

    for (int i = j; i < k*n; i++) {
        if (l < n && i == flag[l]) {
            l++;
        }
        else {
            last[i] = 0;
        }
    }
}

vector<vector<int> > gen(int n) {
    vector<vector<int> > final;
    vector<int> flag;
    flag.push_back(0);
    for (int i = 1; i < n; i++) {
        flag.push_back(i*k-1);
    }

    while (flag.size() != 0) {
        vector<int> last;
        nextdfa(last, flag);
        while (last.size() != 0) {
            final.push_back(last);
            nextdfa(last, flag);
        }
        nextflag(flag);
    }
    return final;
}

int main() {
    int n = 6;
    vector<vector<int> > final = gen(n);
    cout << final.size() << "\n";
    // for (int i = 0; i < final.size(); i++) {
    //     cout << "[";
    //     for (int j = 0; j < final[i].size(); j++) {
    //         cout << final[i][j] << ", ";
    //     }
    //     cout << "]\n";
    // }
}
