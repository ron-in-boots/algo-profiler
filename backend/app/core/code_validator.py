import re
from typing import Tuple

BLOCKED_INCLUDES = [
    "fstream", "ifstream", "ofstream",
    "cstdlib", "stdlib.h",
    "unistd.h",
    "sys/socket.h", "netinet",
    "pthread.h",
    "dlfcn.h",
    "signal.h",
    "sys/mman.h",
    "execinfo.h",
]

BLOCKED_FUNCTIONS = [
    r"\bsystem\s*\(",
    r"\bexec[lv]?\s*\(",
    r"\bfork\s*\(",
    r"\bpopen\s*\(",
    r"\bfreopen\s*\(",
    r"\bfopen\s*\(",
    r"\bmmap\s*\(",
    r"\bptrace\s*\(",
    r"\bgetenv\s*\(",
    r"\bsetenv\s*\(",
    r"\bchmod\s*\(",
    r"\bchown\s*\(",
    r"__asm__",
    r"\basm\s*\(",
]

# Required signatures per input type
REQUIRED_SIGNATURES = {
    "array":  r"void\s+solve\s*\(\s*std::vector\s*<\s*int\s*>\s*&\s*\w+\s*,\s*int\s+\w+\s*\)",
    "string": r"void\s+solve\s*\(\s*std::string\s*&\s*\w+\s*,\s*int\s+\w+\s*\)",
    "graph":  r"void\s+solve\s*\(\s*std::vector\s*<\s*std::vector\s*<\s*int\s*>\s*>\s*&\s*\w+\s*,\s*int\s+\w+\s*\)",
    "matrix": r"void\s+solve\s*\(\s*std::vector\s*<\s*std::vector\s*<\s*int\s*>\s*>\s*&\s*\w+\s*,\s*int\s+\w+\s*\)",
}

SIGNATURE_HINTS = {
    "array":  "void solve(std::vector<int>& data, int N)",
    "string": "void solve(std::string& data, int N)",
    "graph":  "void solve(std::vector<std::vector<int>>& adj, int N)",
    "matrix": "void solve(std::vector<std::vector<int>>& matrix, int N)",
}

MAX_CODE_LENGTH = 65536
MAX_LINES = 500

def validate_code(code: str, input_type: str = "array") -> Tuple[bool, str]:
    if not code.strip():
        return False, "Code cannot be empty."
    if len(code) > MAX_CODE_LENGTH:
        return False, f"Code too long. Maximum {MAX_CODE_LENGTH} characters allowed."
    if code.count('\n') > MAX_LINES:
        return False, f"Code too long. Maximum {MAX_LINES} lines allowed."

    # Check signature
    pattern = REQUIRED_SIGNATURES.get(input_type, REQUIRED_SIGNATURES["array"])
    hint = SIGNATURE_HINTS.get(input_type, SIGNATURE_HINTS["array"])
    if not re.search(pattern, code):
        return False, f"Your code must contain exactly this function signature:\n{hint}"

    # Check blocked includes
    for include in BLOCKED_INCLUDES:
        pattern_inc = rf"#\s*include\s*[<\"]{re.escape(include)}[>\"]"
        if re.search(pattern_inc, code):
            return False, f"Blocked include: <{include}>. System calls are not allowed."

    # Check blocked functions
    for pattern_fn in BLOCKED_FUNCTIONS:
        if re.search(pattern_fn, code):
            return False, f"Blocked system call detected. Not allowed for security reasons."

    # Block main redefinition
    if re.search(r"\bint\s+main\s*\(", code):
        return False, "Do not define main(). Only define the solve() function."

    if re.search(r"\bFILE\s*\*", code):
        return False, "FILE* operations are not allowed."

    return True, ""
