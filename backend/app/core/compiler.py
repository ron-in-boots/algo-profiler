from pathlib import Path

SANDBOX_DIR = Path(__file__).parent.parent.parent / "sandbox"

TEMPLATES = {
    "array":  SANDBOX_DIR / "template_array.cpp",
    "string": SANDBOX_DIR / "template_string.cpp",
    "graph":  SANDBOX_DIR / "template_graph.cpp",
    "matrix": SANDBOX_DIR / "template_matrix.cpp",
}

class CompilationError(Exception):
    pass

class ValidationError(Exception):
    pass

def inject_template(user_code: str, input_type: str = "array") -> str:
    """Inject user code into the appropriate C++ harness template."""
    template_path = TEMPLATES.get(input_type, TEMPLATES["array"])
    template = template_path.read_text()
    return template.replace("{{USER_CODE}}", user_code)
