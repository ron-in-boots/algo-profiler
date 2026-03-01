import Editor from '@monaco-editor/react'

export const EXAMPLES = {
  array: {
    label: "Array / Sorting",
    examples: {
      "Bubble Sort — O(N²)": `void solve(std::vector<int>& data, int N) {
    for (int i = 0; i < N - 1; i++)
        for (int j = 0; j < N - i - 1; j++)
            if (data[j] > data[j+1])
                std::swap(data[j], data[j+1]);
}`,
      "std::sort — O(N log N)": `void solve(std::vector<int>& data, int N) {
    std::sort(data.begin(), data.end());
}`,
      "Linear Search — O(N)": `void solve(std::vector<int>& data, int N) {
    int target = data[N/2];
    long long idx = -1;
    for (int i = 0; i < N; i++)
        if (data[i] == target) { idx = i; break; }
    if (idx < 0) data[0] = 0;
}`,
      "Two Sum (Hash) — O(N)": `void solve(std::vector<int>& data, int N) {
    std::unordered_map<int,int> seen;
    int target = data[0] + data[N-1];
    for (int i = 0; i < N; i++) {
        if (seen.count(target - data[i])) { data[0] = i; return; }
        seen[data[i]] = i;
    }
}`,
    }
  },
  string: {
    label: "String",
    examples: {
      "Reverse String — O(N)": `void solve(std::string& data, int N) {
    int l = 0, r = N - 1;
    while (l < r) std::swap(data[l++], data[r--]);
}`,
      "Count Chars — O(N)": `void solve(std::string& data, int N) {
    std::unordered_map<char,int> freq;
    for (char c : data) freq[c]++;
    long long mx = 0;
    for (auto& p : freq) mx = std::max(mx, (long long)p.second);
    if (mx < 0) data[0] = 'x';
}`,
      "Naive Pattern Match — O(N²)": `void solve(std::string& data, int N) {
    std::string pat = data.substr(0, std::min(5, N/4));
    int M = pat.size(), found = 0;
    for (int i = 0; i <= N - M; i++) {
        bool match = true;
        for (int j = 0; j < M; j++)
            if (data[i+j] != pat[j]) { match = false; break; }
        if (match) found++;
    }
    if (found < 0) data[0] = 'x';
}`,
    }
  },
  graph: {
    label: "Graph",
    examples: {
      "BFS — O(N + E)": `void solve(std::vector<std::vector<int>>& adj, int N) {
    std::vector<bool> visited(N, false);
    std::queue<int> q;
    q.push(0); visited[0] = true;
    long long count = 0;
    while (!q.empty()) {
        int node = q.front(); q.pop(); count++;
        for (int nb : adj[node])
            if (!visited[nb]) { visited[nb] = true; q.push(nb); }
    }
    if (count < 0) adj[0][0] = 0;
}`,
      "DFS — O(N + E)": `void solve(std::vector<std::vector<int>>& adj, int N) {
    std::vector<bool> visited(N, false);
    std::stack<int> s;
    s.push(0); visited[0] = true;
    long long count = 0;
    while (!s.empty()) {
        int node = s.top(); s.pop(); count++;
        for (int nb : adj[node])
            if (!visited[nb]) { visited[nb] = true; s.push(nb); }
    }
    if (count < 0) adj[0][0] = 0;
}`,
    }
  },
  matrix: {
    label: "Matrix / DP",
    examples: {
      "Matrix Traverse — O(N²)": `void solve(std::vector<std::vector<int>>& matrix, int N) {
    long long sum = 0;
    for (int i = 0; i < N; i++)
        for (int j = 0; j < N; j++)
            sum += matrix[i][j];
    if (sum < 0) matrix[0][0] = 0;
}`,
      "Matrix Multiply — O(N³)": `void solve(std::vector<std::vector<int>>& matrix, int N) {
    std::vector<std::vector<int>> result(N, std::vector<int>(N, 0));
    for (int i = 0; i < N; i++)
        for (int j = 0; j < N; j++)
            for (int k = 0; k < N; k++)
                result[i][j] += matrix[i][k] * matrix[k][j];
    matrix = result;
}`,
      "LIS — O(N²)": `void solve(std::vector<std::vector<int>>& matrix, int N) {
    std::vector<int> flat;
    for (auto& row : matrix) for (int x : row) flat.push_back(x);
    int M = flat.size();
    std::vector<int> dp(M, 1);
    for (int i = 1; i < M; i++)
        for (int j = 0; j < i; j++)
            if (flat[j] < flat[i]) dp[i] = std::max(dp[i], dp[j]+1);
    long long ans = *std::max_element(dp.begin(), dp.end());
    if (ans < 0) matrix[0][0] = 0;
}`,
    }
  }
}

export default function CodeEditor({ value, onChange }) {
  return (
    <div className="h-full">
      <Editor
        height="100%"
        defaultLanguage="cpp"
        value={value}
        onChange={onChange}
        theme="vs-dark"
        options={{
          fontSize: 15,
          lineHeight: 24,
          minimap: { enabled: false },
          scrollBeyondLastLine: false,
          wordWrap: 'on',
          automaticLayout: true,
          tabSize: 4,
          lineNumbers: 'on',
          fontFamily: "'Fira Code', 'Cascadia Code', monospace",
          fontLigatures: true,
          renderLineHighlight: 'line',
          padding: { top: 16, bottom: 16 },
        }}
      />
    </div>
  )
}
