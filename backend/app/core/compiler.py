import subprocess
import tempfile
import uuid
from pathlib import Path

SANDBOX_DIR = Path(__file__).parent.parent.parent / "sandbox"
TEMP_DIR = Path(tempfile.gettempdir()) / "algo_profiler"

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
    template_path = TEMPLATES.get(input_type, TEMPLATES["array"])
    template = template_path.read_text()
    return template.replace("{{USER_CODE}}", user_code)

def compile_source(full_source: str) -> Path:
    """Compile full C++ source and return path to binary."""
    TEMP_DIR.mkdir(parents=True, exist_ok=True)
    job_id = uuid.uuid4().hex[:8]
    src_path = TEMP_DIR / f"solution_{job_id}.cpp"
    bin_path = TEMP_DIR / f"solution_{job_id}.out"

    src_path.write_text(full_source)

    try:
        result = subprocess.run(
            [
                "g++", "-O2", "-std=c++17",
                "-D_FORTIFY_SOURCE=2",
                "-fstack-protector-strong",
                "-Wno-unused-result",
                "-o", str(bin_path),
                str(src_path)
            ],
            capture_output=True,
            text=True,
            timeout=30
        )
    finally:
        src_path.unlink(missing_ok=True)

    if result.returncode != 0:
        clean_error = result.stderr.replace(str(TEMP_DIR), "")
        raise CompilationError(clean_error)

    return bin_path
