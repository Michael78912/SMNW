#include <iostream>
#include <math.h>

int main() {
    int arr [1000];
    int tary = 20, tarx = 20, chary = 10, charx = 10;
    int it;
    //std::cout << (chary - tary) / (pow(charx - tarx, 2)) << "\n[";


    for(int i=10; i<610; i++){
        arr[i]=(-0.1)*pow((i-20),2)+tary;
        std::cout << arr[i] << ", ";
        //std::cout << pow(i-20,2)+20 << ", ";
    }
    return 0;
}