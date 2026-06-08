


# Project 1 Agent Trajectory Latency Benchmark : Cross-provider inference
<img width="2642" height="1582" alt="image" src="https://github.com/user-attachments/assets/26847b88-b9e4-4f68-b18a-aa5655bc150a" />

## Overview

Traditional LLM benchmarks primarily evaluate throughput, tokens/sec, or single-request latency. These metrics assume independent requests with bounded context.

Agent-style workloads
 repeatedly:
- ingest growing context
- maintain sequential dependency across steps
- generate short structured outputs under expanding prompt pressure

As a result, latency becomes a **trajectory-level property**, not a per-request constant.

This benchmark evaluates how inference systems behave under that regime by comparing:

- OpenAI (`gpt-4o-mini`)
- General Compute (`minimax-m2.7` via OpenAI-compatible API)

under identical structured agent workloads.

---
*** This benchmark compares latency behavior across two different inference providers under identical agent trajectory workloads; results are observational and not intended as causal or architectural comparisons. ***

## Experimental Design

Both systems execute the same deterministic agent loop:

- Fixed task: debugging a distributed training failure
- 6 sequential steps per trajectory
- Each step depends on prior outputs (state accumulation)
- Context size increases monotonically per step
- Outputs remain short and structured (bounded reasoning)

### Controlled Variable

The only scaling factor is:

> Increasing prompt/context size across steps

This isolates **context-driven inference behavior** from prompt semantics.

---

## Key Metrics

For each step:

- Step latency (end-to-end request time)
- Prompt tokens (context growth proxy)
- Completion tokens

And derived:

- trajectory latency curve
- cumulative latency
- context-to-latency sensitivity

---

# Results

After initial cold start run, 

✅ 1st run
OpenAI: 8.507960081100464
GC: 7.044839382171631

✅ 2nd run:
OpenAI: 8.503200054168701
GC: 6.81445574760437
✅ 3rd run:
OpenAI: 6.986875057220459
GC: 7.405105829238892

 ✅ 4th run:
OpenAI: 12.028305053710938
GC: 7.147117376327515

📊 Final comparison
Provider	Avg latency
OpenAI	9.01s
GC	7.10s
🧠 Interpretation (important)
Raw result:
GC is ~1.9s faster on average
~21% lower latency
​

## Scope Clarification:


This benchmark does not isolate model-level performance. Instead, it evaluates end-to-end inference latency as observed through two different API providers under identical agent-style workloads.

As a result, observed differences may reflect:

serving infrastructure differences
batching and request scheduling policies
context handling and KV-cache reuse behavior
network and routing variance

This work focuses on trajectory-level latency dynamics rather than causal attribution.


---
Experimental Findings:
<img width="2642" height="1582" alt="image" src="https://github.com/user-attachments/assets/26847b88-b9e4-4f68-b18a-aa5655bc150a" />


## 3. Key Finding
Across the trajectory, General Compute's MiniMax M2 consistently demonstrates lower cumulative execution time compared to GPT-4o-mini, finishing at ~6.8s versus ~8.5s by step 6. This gap is primarily driven by lower per-step latency in the early and middle stages, where GC MiniMax starts significantly faster (notably step 1) and maintains a more stable progression. GPT-4o-mini shows higher variance in per-step latency, with noticeable spikes (e.g., step 1 and step 4), which compounds into a steeper cumulative time curve. Overall, the system-level outcome is a ~1.25× speedup in favor of MiniMax in end-to-end trajectory execution.

The latency amplification plot highlights a key structural difference: General Compute MiniMax exhibits stronger step-to-step amplification (rising above ~2.2× by later steps), meaning later steps become progressively more expensive relative to the first. In contrast, GPT-4o-mini shows a dampened or even fluctuating amplification pattern, indicating less monotonic growth but higher instability. The latency difference plot reinforces this: GPT is sometimes slower by over 1s per step early on, but the gap narrows and occasionally reverses at later steps. Taken together, this suggests GC MiniMax is more efficient in absolute trajectory time, while GPT-4o-mini has more irregular per-step scaling behavior that smooths but does not outperform overall.



---

# Why This Matters

Agent systems are fundamentally constrained by:

- prefill cost (context ingestion)
- decode cost (step generation)
- sequential blocking (no parallelization across steps)

This benchmark shows that:

> systems differ not just in raw latency, but in how latency evolves under increasing context pressure.


---

# Final Takeaway

> Across the trajectory, MiniMax M2.7 consistently demonstrates lower cumulative execution time compared to GPT-4o-mini, finishing at ~6.8s versus ~8.5s by step 6. This gap is primarily driven by lower per-step latency in the early and middle stages, where MiniMax starts significantly faster (notably step 1) and maintains a more stable progression. GPT-4o-mini shows higher variance in per-step latency, with noticeable spikes (e.g., step 1 and step 4), which compounds into a steeper cumulative time curve. Overall, the system-level outcome is a ~1.25× speedup in favor of MiniMax in end-to-end trajectory execution.

The latency amplification plot highlights a key structural difference: MiniMax exhibits stronger step-to-step amplification (rising above ~2.2× by later steps), meaning later steps become progressively more expensive relative to the first. In contrast, GPT-4o-mini shows a dampened or even fluctuating amplification pattern, indicating less monotonic growth but higher instability. The latency difference plot reinforces this: GPT is sometimes slower by over 1s per step early on, but the gap narrows and occasionally reverses at later steps. Taken together, this suggests MiniMax is more efficient in absolute trajectory time, while GPT-4o-mini has more irregular per-step scaling behavior that smooths but does not outperform overall.


This makes it particularly informative for evaluating **agent-era inference workloads**, where trajectory-level performance matters more than isolated request latency.

---

# Next Work (Recommended)

To further strengthen this benchmark:

- Extend trajectory length (10–20 steps)
- Run multiple seeds for statistical confidence
- Normalize latency by prompt tokens (efficiency index)
- Separate prefill vs decode contributions explicitly
- Add tool-using agent workloads (real external calls)


TrajectoryBench
Measuring Latency Amplification in Agent-Style Workloads
<img width="2782" height="1566" alt="image" src="https://github.com/user-attachments/assets/cbbfe4c8-a586-4632-90ce-342b66969751" />
```markdown
# # Project # 2 Agent Trajectory Latency Benchmark — Mini Research Notes

I built this benchmark to study how inference latency behaves when LLMs are used in **agent-style sequential workflows**, rather than traditional single-turn or long-form generation benchmarks.

Traditional LLM benchmarks emphasize throughput and long-form generation. Agent-style workloads repeatedly process large and growing contexts while producing short, structured outputs. As context accumulates across a trajectory, workflow latency can grow substantially even when individual generations remain small. This benchmark explores that behavior by measuring latency across increasingly context-heavy sequential workflows.

---

## What I Observed

After instrumenting a structured agent loop with controlled context growth, the latency behavior did not follow a simple monotonic scaling pattern.

Instead, the per-step latency curve showed a combination of:

- structured early drop
- mid-trajectory stability
- late-stage increase

This immediately indicates that latency is not governed by a single smooth scaling law in agent workloads.

---

## Key Interpretation

The most important finding is that:

> latency is not simply a function of step index or trajectory depth.

Instead, observed latency is a combination of:

- system warmup effects (early-stage variability)
- context accumulation (prefill pressure increases over time)
- stochastic inference variance (server and decoding noise)

This explains why the curve does not behave linearly or monotonically, even under controlled agent execution.

---

## Multi-Regime Behavior in Inference

A more accurate interpretation of the system is that LLM inference exhibits **multiple operational regimes** rather than a single scaling relationship:

### 1. Cold Start Regime
- high variance in latency
- unstable execution behavior
- initialization and routing overhead dominates

### 2. Efficient Regime
- lowest observed latency region
- relatively stable inference path
- system operates near optimal throughput conditions

### 3. Context-Dominated Regime
- latency begins to increase again
- prefill cost grows with accumulated context
- sequential dependency amplifies workload per step

---

## Why This Matters

This experiment suggests that agent workloads should not be evaluated using traditional single-request benchmarks or throughput-only metrics.

Instead, they exhibit **trajectory-dependent performance behavior**, where:

- each step is conditioned on previous computation
- context accumulation becomes a primary cost driver
- latency dynamics emerge over sequences, not isolated calls

---

## Why My Agent Design Works

The structured agent loop used in this benchmark is not a simulation of conversational behavior. It is a controlled workload generator that enforces:

- sequential dependency between steps  
- increasing context size across trajectory  
- fixed output structure (short, bounded responses)  

This design allows inference behavior to be observed under realistic agent constraints while still maintaining measurable experimental control.

As a result, the system is no longer a toy simulation. It functions as:

> a multi-regime inference workload generator for agent-style execution paths

---

## Final Takeaway

The most accurate characterization of the observed behavior is:

> Agent trajectories exhibit non-monotonic latency behavior due to interaction between cold-start effects, context accumulation, and inference variance. After initial stabilization, latency begins to increase as accumulated context grows.

This indicates that inference latency in agent systems cannot be fully understood through single-request benchmarks. It is fundamentally a trajectory-level property shaped by evolving context and sequential computation structure.
```



