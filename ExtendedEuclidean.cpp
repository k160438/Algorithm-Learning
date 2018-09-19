#include <iostream>
using namespace std;

void ExtEuc(int a, int b, int &x, int &y)
{
    int tmp;
    if (b == 0)
    {
        x = 1;
        y = 0;
    }
    else
    {
        ExtEuc(b, a % b, x, y);
        tmp = x;
        x = y;
        y = tmp - a / b * y;
    }
}

int main()
{
    int a, b, x, y;
    cin >> a >> b;
    ExtEuc(a, b, x, y);
    cout << x << ' ' << y << endl;
    return 0;
}