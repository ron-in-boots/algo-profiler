import numpy as np
from scipy.optimize import curve_fit
from typing import List, Dict

def linear(n, a, b): return a * n + b
def nlogn(n, a, b): return a * n * np.log2(n + 1) + b
def quadratic(n, a, b): return a * n**2 + b
def cubic(n, a, b): return a * n**3 + b
def logarithmic(n, a, b): return a * np.log2(n + 1) + b
def constant(n, a, b): return np.full_like(n, a, dtype=float)

MODELS = {
    "O(1)":       constant,
    "O(log N)":   logarithmic,
    "O(N)":       linear,
    "O(N log N)": nlogn,
    "O(N²)":      quadratic,
    "O(N³)":      cubic,
}

COMPLEXITY_RANK = {
    "O(1)": 0,
    "O(log N)": 1,
    "O(N)": 2,
    "O(N log N)": 3,
    "O(N²)": 4,
    "O(N³)": 5,
}

MIN_R2 = 0.85
TOLERANCE = 0.005

def compute_growth_ratio(ns: np.ndarray, ts: np.ndarray) -> float:
    """
    Compute average ratio of t(2N)/t(N).
    O(1)       → ratio ≈ 1.0
    O(log N)   → ratio ≈ 1.0-1.1
    O(N)       → ratio ≈ 2.0
    O(N log N) → ratio ≈ 2.1-2.3
    O(N²)      → ratio ≈ 4.0
    O(N³)      → ratio ≈ 8.0
    """
    ratios = []
    for i in range(len(ns) - 1):
        if ts[i] > 0.001:  # ignore very small times (noise-dominated)
            ratio = ts[i+1] / ts[i]
            n_ratio = ns[i+1] / ns[i]
            # Normalize to doubling ratio
            normalized = ratio ** (1.0 / np.log2(n_ratio)) if n_ratio > 1 else ratio
            ratios.append(normalized)
    return float(np.median(ratios)) if ratios else 2.0

def ratio_to_complexity(ratio: float) -> str:
    """Map doubling ratio to complexity class."""
    if ratio < 1.15:   return "O(1)"
    if ratio < 1.5:    return "O(log N)"
    if ratio < 2.05:   return "O(N)"
    if ratio < 3.0:    return "O(N log N)"
    if ratio < 5.5:    return "O(N²)"
    return "O(N³)"

def classify_complexity(measurements: List[Dict]) -> Dict:
    valid = [(m["n"], m["time_ms"]) for m in measurements
             if m.get("status") == "ok" and m.get("time_ms") is not None]

    if len(valid) < 3:
        return {"best_fit": "Unknown", "r2_scores": {}}

    ns = np.array([v[0] for v in valid], dtype=float)
    ts = np.array([v[1] for v in valid], dtype=float)

    # Curve fitting scores
    scores = {}
    for label, fn in MODELS.items():
        try:
            popt, _ = curve_fit(fn, ns, ts, maxfev=5000)
            predicted = fn(ns, *popt)
            ss_res = np.sum((ts - predicted) ** 2)
            ss_tot = np.sum((ts - np.mean(ts)) ** 2)
            r2 = 1 - (ss_res / ss_tot) if ss_tot > 0 else 0
            scores[label] = round(float(r2), 4)
        except Exception:
            scores[label] = -999

    # Curve fit best candidate
    valid_models = {k: v for k, v in scores.items() if v >= MIN_R2}
    if not valid_models:
        curve_best = max(scores, key=scores.get)
    else:
        best_score = max(valid_models.values())
        candidates = {k: v for k, v in valid_models.items()
                      if best_score - v <= TOLERANCE}
        curve_best = min(candidates, key=lambda k: COMPLEXITY_RANK.get(k, 99))

    # Growth ratio best candidate
    ratio = compute_growth_ratio(ns, ts)
    ratio_best = ratio_to_complexity(ratio)

    # If both agree, confident answer
    if curve_best == ratio_best:
        best_fit = curve_best
    else:
        # They disagree — use rank proximity to break tie
        curve_rank = COMPLEXITY_RANK.get(curve_best, 99)
        ratio_rank = COMPLEXITY_RANK.get(ratio_best, 99)
        # Trust ratio test more when they're adjacent complexity classes
        if abs(curve_rank - ratio_rank) <= 1:
            best_fit = ratio_best  # ratio test is more reliable
        else:
            best_fit = curve_best  # big disagreement, trust curve fit

    return {
        "best_fit": best_fit,
        "r2_scores": scores,
        "growth_ratio": round(ratio, 3)
    }
