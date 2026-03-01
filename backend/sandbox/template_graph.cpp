#include <iostream>
#include <vector>
#include <string>
#include <algorithm>
#include <chrono>
#include <queue>
#include <stack>
#include <unordered_map>
#include <unordered_set>
#include <climits>
#include <cmath>

// ===== USER CODE START =====
{{USER_CODE}}
// ===== USER CODE END =====

int main() {
    int N, E;
    std::cin >> N >> E;
    std::vector<std::vector<int>> adj(N);
    for (int i = 0; i < E; i++) {
        int u, v;
        std::cin >> u >> v;
        adj[u].push_back(v);
        adj[v].push_back(u);
    }

    auto start = std::chrono::high_resolution_clock::now();
    solve(adj, N);
    auto end = std::chrono::high_resolution_clock::now();

    double elapsed = std::chrono::duration<double, std::milli>(end - start).count();
    std::cout << elapsed << std::endl;
    return 0;
}
