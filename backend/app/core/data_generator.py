import random
import string
from typing import List, Tuple

DEFAULT_SIZES = [100, 500, 1000, 5000, 10000, 50000]

# Matrix sizes are smaller since N×N grows fast
MATRIX_SIZES = [10, 50, 100, 200, 500, 1000]

# Graph sizes
GRAPH_SIZES = [100, 500, 2000, 8000, 30000, 100000]

def generate_array(n: int, data_type: str = "random") -> List[int]:
    if data_type == "random":
        return [random.randint(1, 10000) for _ in range(n)]
    elif data_type == "sorted":
        return list(range(1, n + 1))
    elif data_type == "reverse_sorted":
        return list(range(n, 0, -1))
    elif data_type == "nearly_sorted":
        arr = list(range(1, n + 1))
        swaps = max(1, n // 20)
        for _ in range(swaps):
            i, j = random.randint(0, n-1), random.randint(0, n-1)
            arr[i], arr[j] = arr[j], arr[i]
        return arr
    return [random.randint(1, 10000) for _ in range(n)]

def generate_string(n: int) -> str:
    return ''.join(random.choices(string.ascii_lowercase, k=n))

def generate_graph(n: int) -> Tuple[int, List[Tuple[int, int]]]:
    """Returns (num_edges, edge_list) for undirected graph."""
    edges = []
    # Spanning path for connectivity
    for i in range(n - 1):
        edges.append((i, i + 1))
    # Extra random edges (~1.5x nodes)
    extra = n // 2
    for _ in range(extra):
        u = random.randint(0, n - 1)
        v = random.randint(0, n - 1)
        if u != v:
            edges.append((u, v))
    return len(edges), edges

def generate_matrix(n: int) -> List[List[int]]:
    return [[random.randint(0, 100) for _ in range(n)] for _ in range(n)]

def format_input(input_type: str, n: int, data_type: str = "random") -> str:
    """Format stdin data for the C++ harness based on input type."""
    if input_type == "array":
        data = generate_array(n, data_type)
        return f"{n}\n{' '.join(map(str, data))}\n"

    elif input_type == "string":
        s = generate_string(n)
        return f"{n}\n{s}\n"

    elif input_type == "graph":
        num_edges, edges = generate_graph(n)
        edge_lines = '\n'.join(f"{u} {v}" for u, v in edges)
        return f"{n} {num_edges}\n{edge_lines}\n"

    elif input_type == "matrix":
        matrix = generate_matrix(n)
        rows = '\n'.join(' '.join(map(str, row)) for row in matrix)
        return f"{n}\n{rows}\n"

    return f"{n}\n"

def get_sizes_for_type(input_type: str) -> List[int]:
    if input_type == "matrix":
        return MATRIX_SIZES
    if input_type == "graph":
        return GRAPH_SIZES
    return DEFAULT_SIZES
