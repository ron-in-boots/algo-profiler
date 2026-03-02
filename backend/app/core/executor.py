import subprocess
import resource
import signal
import os
from pathlib import Path
from typing import List, Dict
from app.core.data_generator import format_input, get_sizes_for_type
from app.core.compiler import inject_template, compile_source

TRIALS = 3

def set_sandbox_limits(max_memory_mb: int, max_time_sec: int):
    mem_bytes = max_memory_mb * 1024 * 1024
    resource.setrlimit(resource.RLIMIT_AS, (mem_bytes, mem_bytes))
    resource.setrlimit(resource.RLIMIT_CPU, (max_time_sec, max_time_sec))
    resource.setrlimit(resource.RLIMIT_FSIZE, (0, 0))
    resource.setrlimit(resource.RLIMIT_NPROC, (1, 1))
    resource.setrlimit(resource.RLIMIT_NOFILE, (10, 10))

def run_once(binary_path: Path, n: int, input_type: str,
             data_type: str, max_memory_mb: int, max_time_sec: int) -> Dict:
    stdin_data = format_input(input_type, n, data_type)
    try:
        proc = subprocess.run(
            [str(binary_path)],
            input=stdin_data,
            capture_output=True,
            text=True,
            timeout=max_time_sec,
            preexec_fn=lambda: set_sandbox_limits(max_memory_mb, max_time_sec)
        )
        if proc.returncode != 0:
            if proc.returncode == -signal.SIGKILL:
                return {"status": "memory_limit_exceeded"}
            if proc.returncode == -signal.SIGXCPU:
                return {"status": "cpu_limit_exceeded"}
            return {"status": "runtime_error", "error": proc.stderr[:200]}
        output = proc.stdout.strip()
        if not output:
            return {"status": "no_output"}
        return {"status": "ok", "time_ms": float(output)}
    except subprocess.TimeoutExpired:
        return {"status": "timeout"}
    except Exception as e:
        return {"status": "error", "error": str(e)}

def run_single(source_code: str, n: int, input_type: str = "array",
               data_type: str = "random", max_memory_mb: int = 256,
               max_time_sec: int = 10) -> Dict:
    # Compile first
    try:
        binary_path = compile_source(source_code)
    except Exception as e:
        return {"n": n, "time_ms": None, "status": "compilation_error", "error": str(e)}

    times = []
    last_error = None

    for _ in range(TRIALS):
        result = run_once(binary_path, n, input_type, data_type,
                         max_memory_mb, max_time_sec)
        if result["status"] == "ok":
            times.append(result["time_ms"])
        else:
            last_error = result
            break

    binary_path.unlink(missing_ok=True)

    if not times:
        return {"n": n, "time_ms": None, **(last_error or {"status": "error"})}

    times.sort()
    return {
        "n": n,
        "time_ms": round(times[len(times) // 2], 4),
        "status": "ok",
        "error": None
    }

def run_profile(source_code: str, sizes: List[int] = None,
                input_type: str = "array", data_type: str = "random",
                max_memory_mb: int = 256, max_time_sec: int = 10) -> List[Dict]:
    if sizes is None:
        sizes = get_sizes_for_type(input_type)

    results = []
    for n in sizes:
        result = run_single(source_code, n, input_type, data_type,
                            max_memory_mb, max_time_sec)
        results.append(result)
        if result["status"] in ("timeout", "memory_limit_exceeded", "cpu_limit_exceeded"):
            break

    return results
