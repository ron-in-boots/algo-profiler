#include <iostream>
#include <vector>
#include <string>
#include <algorithm>
#include <chrono>
#include <unordered_map>
#include <unordered_set>
#include <climits>
#include <cmath>

// ===== USER CODE START =====
{{USER_CODE}}
// ===== USER CODE END =====

int main() {
    int N;
    std::cin >> N;
    std::string data;
    std::cin >> data;

    auto start = std::chrono::high_resolution_clock::now();
    solve(data, N);
    auto end = std::chrono::high_resolution_clock::now();

    double elapsed = std::chrono::duration<double, std::milli>(end - start).count();
    std::cout << elapsed << std::endl;
    return 0;
}
