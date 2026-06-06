TrajectoryBench
Measuring Latency Amplification in Agent-Style Workloads
<img width="2782" height="1566" alt="image" src="https://github.com/user-attachments/assets/cbbfe4c8-a586-4632-90ce-342b66969751" />
```markdown
# # Project # 1 Agent Trajectory Latency Benchmark — Mini Research Notes

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
#Project #2 comparing General Compute versas OpenAI
<img width="2140" height="1502" alt="image" src="https://github.com/user-attachments/assets/b032432a-cd46-4cce-92e5-004a66396d38" />

# Agent Trajectory Latency Benchmark (OpenAI vs General Compute)

## Overview

Traditional LLM benchmarks emphasize throughput and long-form generation. Agent-style workloads invert these assumptions by repeatedly processing large and growing contexts while producing short, structured outputs. As context accumulates across a trajectory, workflow latency can increase even when individual generations remain small.

This project implements a **structured agent benchmark harness** to measure how inference latency evolves across sequential decision-making steps under increasing context pressure, and compares two inference backends under identical workloads:

- OpenAI (`gpt-4o-mini`)
- General Compute (`minimax-m2.7` via OpenAI-compatible API)

---

## Key Idea

The core idea is to isolate **trajectory-level inference behavior**:

- Each step depends on prior steps (agent memory accumulation)
- Prompt context increases deterministically per step
- Output remains short and structured (bounded JSON / constrained reasoning)
- Latency is measured per step and cumulatively

This enables observation of how inference systems behave under **agent-like workloads rather than single-shot prompts**.

---

## Experimental Design

### Agent Structure

Each system runs the same structured agent loop:

- Fixed task: *debug a distributed training failure*
- Sequential steps (6 per run)
- Each step:
  - Appends prior outputs to context
  - Expands total prompt size
  - Produces a short decision/action output

---

### Controlled Variable

The only intentionally varying factor is:

> **Prompt/context size increases monotonically across steps**

This creates a controlled proxy for agent memory growth.

---

### Measured Metrics

For each step:

- Latency (seconds)
- Prompt tokens
- Completion tokens

And derived metrics:

- Step latency curve
- Cumulative latency over trajectory
- Total trajectory cost

---

## Results

## 1. OpenAI (`gpt-4o-mini`)

### Observations

- Latency is relatively stable across steps (~0.87s–1.88s range)
- No strong monotonic increase with context size
- One early spike (step 0) likely due to warmup / routing variance
- Overall trajectory remains stable

### Key Metrics

- Total latency: **7.80s**
- Step behavior: non-monotonic but bounded variance
- Output format: consistently structured JSON

### Interpretation

OpenAI shows:
- Stable inference under increasing context
- Weak sensitivity to trajectory growth at this scale
- Likely strong optimization for short structured outputs

---

## 2. General Compute (`minimax-m2.7`)

### Observations

- Latency increases more consistently with context growth
- Clear upward trend from ~0.66s → ~1.65s
- Step-wise growth aligns more closely with prompt token expansion
- More pronounced trajectory-dependent latency behavior

### Key Metrics

- Total latency: **7.02s**
- Step latency trend: increasing with context size
- Prompt tokens grow from ~1.6k → ~14k

### Interpretation

General Compute shows:
- Stronger sensitivity to context accumulation
- More visible prefill-driven scaling effects
- Less stable per-step latency distribution compared to OpenAI

---

## Cross-System Comparison

### 1. Latency Stability

- OpenAI: higher variance, but bounded and non-trending
- General Compute: lower early latency, but stronger upward drift

---

### 2. Context Sensitivity

- OpenAI: weak coupling between context size and latency
- General Compute: clearer correlation between prompt growth and latency increase

---

### 3. Trajectory Behavior

Both systems exhibit:

- Non-linear latency behavior
- Early-step instability (warmup / routing effects)
- Increasing complexity under sequential dependency

However:

> General Compute shows stronger trajectory-dependent scaling behavior.

---

## Key Insight

The most important result is not absolute speed, but **latency structure across the trajectory**:

> Agent workloads do not behave like single-request benchmarks. They exhibit regime-dependent inference behavior driven by warmup effects, context accumulation, and system-level variance.

This experiment demonstrates that:

- Latency is not a single scalar property of a model
- It is a **trajectory-dependent function of context growth**

---

## Conclusion

This benchmark shows that inference systems behave differently under agent-style workloads compared to traditional LLM benchmarks.

We observe:

- Multi-step latency is not monotonic or purely random
- Context accumulation introduces measurable scaling effects
- Different inference backends exhibit distinct trajectory signatures

### Final takeaway:

> Agent performance is fundamentally a *sequential system property*, not a per-request metric.

---

## Next Steps (Future Work)

- Run multi-seed experiments (statistical confidence bands)
- Increase trajectory length (10–20 steps)
- Normalize latency by prompt tokens (efficiency score)
- Decompose prefill vs decode contributions more explicitly
- Extend to tool-using agents (real external calls)
