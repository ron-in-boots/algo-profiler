from groq import Groq
from app.config import settings
from typing import List, Dict

client = Groq(api_key=settings.GROQ_API_KEY)

def build_prompt(code: str, measurements: List[Dict], complexity: Dict) -> str:
    best_fit = complexity.get("best_fit", "Unknown")
    r2_scores = complexity.get("r2_scores", {})

    timing_table = "\n".join([
        f"  N={m['n']}: {m['time_ms']}ms ({m['status']})"
        for m in measurements
        if m.get("status") == "ok"
    ])

    scores_str = ", ".join([
        f"{k}: {v:.3f}" for k, v in
        sorted(r2_scores.items(), key=lambda x: -x[1])[:4]
    ])

    return f"""You are an expert C++ algorithms engineer and competitive programmer.
Analyze the following C++ algorithm function and its empirical profiling results.

## User's C++ Code:
```cpp
{code}
```

## Empirical Profiling Results:
- Detected Time Complexity: {best_fit}
- R² Scores (curve fit): {scores_str}
- Timing measurements:
{timing_table}

## Your Task:
Provide a concise, insightful analysis with these sections:

1. **Complexity Analysis**: Explain WHY this code has {best_fit} complexity. Point to specific lines.
2. **Bottlenecks**: Identify the most expensive operations.
3. **Optimizations**: Give 2-3 concrete, actionable suggestions with example code snippets where helpful.
4. **Best/Worst Case**: Note any differences between best, average, and worst case.

Be specific, technical, and practical. Keep response under 400 words."""

def analyze_code(code: str, measurements: List[Dict], complexity: Dict) -> str:
    """Call Groq API and return analysis as a string."""
    prompt = build_prompt(code, measurements, complexity)

    chat = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=600,
    )

    return chat.choices[0].message.content
