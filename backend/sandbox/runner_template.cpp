#include <iostream>
#include <vector>
#include <string>
#include <chrono>
#include <cstdlib>
#include <algorithm>
#include <unordered_map>
#include <queue>
#include <stack>

// ===== USER CODE START =====
{{USER_CODE}}
// ===== USER CODE END =====

int main() {
    // Read input size N from stdin
    int N;
    std::cin >> N;

    // Read the dataset from stdin
    std::vector<int> data(N);
    for (int i = 0; i < N; i++) {
        std::cin >> data[i];
    }

    // Start timing
    auto start = std::chrono::high_resolution_clock::now();

    // Call user function
    solve(data, N);

    // Stop timing
    auto end = std::chrono::high_resolution_clock::now();
    double elapsed = std::chrono::duration<double, std::milli>(end - start).count();

    // Output just the time in milliseconds
    std::cout << elapsed << std::endl;

    return 0;
}
