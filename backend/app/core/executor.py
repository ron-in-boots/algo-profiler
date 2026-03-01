import subprocess
import uuid
import os
from pathlib import Path
from typing import List, Dict
from app.core.data_generator import format_input, get_sizes_for_type

TRIALS = 3
SANDBOX_IMAGE = "algo-profiler-sandbox"

def compile_and_run_in_docker(source_code: str, stdin_data: str,
                               max_memory_mb: int = 512,
                               max_time_sec: int = 15) -> Dict:
    job_id = uuid.uuid4().hex[:8]
    src_path = f"/tmp/algo_src_{job_id}.cpp"

    try:
        # Write full source to temp file
        with open(src_path, 'w') as f:
            f.write(source_code)

        # Verify file was written
        if not os.path.exists(src_path):
            return {"status": "error", "error": "failed to write source file"}

        cmd = [
            "docker", "run", "--rm",
            "--network", "none",
            "--memory", f"{max_memory_mb}m",
            "--memory-swap", f"{max_memory_mb * 2}m",
            "--cpus", "1",
            "--pids-limit", "64",
            "-i",
            "--volume", f"{src_path}:/sandbox/source.cpp:ro",
            SANDBOX_IMAGE,
            "sh", "-c",
            "g++ -O2 -std=c++17 -o /tmp/sol /sandbox/source.cpp 2>&1 && /tmp/sol"
        ]

        proc = subprocess.run(
            cmd,
            input=stdin_data,
            capture_output=True,
            text=True,
            timeout=max_time_sec + 10
        )

        if proc.returncode != 0:
            return {
                "status": "runtime_error",
                "error": (proc.stderr or proc.stdout)[:300]
            }

        # Last line is the timing output
        lines = proc.stdout.strip().split('\n')
        output = lines[-1].strip()

        if not output:
            return {"status": "no_output"}

        return {"status": "ok", "time_ms": float(output)}

    except subprocess.TimeoutExpired:
        return {"status": "timeout"}
    except ValueError as e:
        return {"status": "bad_output", "error": str(e)}
    except Exception as e:
        return {"status": "error", "error": str(e)}
    finally:
        try:
            os.unlink(src_path)
        except:
            pass

def run_single(source_code: str, n: int, input_type: str = "array",
               data_type: str = "random", max_memory_mb: int = 512,
               max_time_sec: int = 15) -> Dict:
    times = []
    last_error = None

    for _ in range(TRIALS):
        stdin_data = format_input(input_type, n, data_type)
        result = compile_and_run_in_docker(source_code, stdin_data,
                                           max_memory_mb, max_time_sec)
        if result["status"] == "ok":
            times.append(result["time_ms"])
        else:
            last_error = result
            break

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
                max_memory_mb: int = 512, max_time_sec: int = 15) -> List[Dict]:
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
