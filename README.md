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



# Agent Trajectory Latency Benchmark : Cross-provider inference
<img width="2140" height="1502" alt="image" src="https://github.com/user-attachments/assets/b032432a-cd46-4cce-92e5-004a66396d38" />

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


## Scope Clarification:


This benchmark does not isolate model-level performance. Instead, it evaluates end-to-end inference latency as observed through two different API providers under identical agent-style workloads.

As a result, observed differences may reflect:

serving infrastructure differences
batching and request scheduling policies
context handling and KV-cache reuse behavior
network and routing variance

This work focuses on trajectory-level latency dynamics rather than causal attribution.
## 1. OpenAI (`gpt-4o-mini`)

### Latency Profile

- Step latency range: ~0.87s – 1.88s
- Non-monotonic behavior across trajectory
- Weak correlation between context growth and latency increase
- Presence of warmup / routing variance effects early in trajectory

### Total Trajectory Latency
- **7.80s**

### Interpretation

OpenAI shows:

- Strong overall stability in short structured generation
- Latency is relatively decoupled from context growth at this scale
- OpenAI appears closer to a relatively flat latency regime under this workload scale, with higher stochastic variance relative to observed context growth.

This results in:

> flat or weakly structured trajectory scaling behavior

---

## 2. General Compute (`minimax-m2.7`)

### Latency Profile

- Step latency range: ~0.66s → 1.65s
- Clear monotonic upward trend across trajectory
- Visually stronger coupling between prompt token growth and latency increase
- Consistent step-wise scaling behavior

### Total Trajectory Latency
- **7.02s**

### Prompt Scaling Signal

- ~1.6k → ~14k prompt tokens across trajectory
- Latency increases track context expansion more directly than in OpenAI

### Interpretation

General Compute exhibits:

- Notably, General Compute achieved lower total trajectory latency (7.02s versus 7.80s), suggesting that increasing context did not prevent competitive end-to-end performance.
- More predictable scaling with increasing trajectory depth
- Lower early-step latency combined with clearer structural growth behavior

This indicates:

> inference behavior that more directly reflects workload scaling characteristics

---

# Cross-System Comparison

## 1. Trajectory Scaling Behavior

| Property | OpenAI | General Compute |
|----------|--------|----------------|
| Context sensitivity | Weak | Strong |
| Latency scaling | Flat / noisy | Structured increase |
| Step stability | Moderate variance | More deterministic trend |

---

## 2. System-Level Behavior

### OpenAI
- Stable bounded latency
- Less sensitive to trajectory growth
- Behaves closer to constant-cost inference per request

### General Compute
- Clear latency growth with context accumulation
- More explicit prefill-driven scaling behavior
- Stronger coupling between workload size and latency

---

## 3. Key Finding

The most important observation is not absolute speed, but **scaling structure across agent trajectories**:

> A more structured latency–context relationship is observed in the General Compute run under this workload configuration.

This is critical for agent workloads where:
- context grows continuously
- steps are sequentially dependent
- cumulative latency determines usability

---

# Why This Matters

Agent systems are fundamentally constrained by:

- prefill cost (context ingestion)
- decode cost (step generation)
- sequential blocking (no parallelization across steps)

This benchmark shows that:

> systems differ not just in raw latency, but in how latency evolves under increasing context pressure.

General Compute demonstrates a clearer and more structured scaling response to this pressure.

---

# Final Takeaway

> Notably, General Compute  achieved lower total trajectory latency (7.02s versus 7.80s), suggesting that increasing context did not prevent competitive end-to-end performance.
> As prompt size expanded from approximately 1.6K to 14K tokens, latency increased in a consistent step-wise manner, indicating a stronger observed relationship between workload growth and inference behavior.

This makes it particularly informative for evaluating **agent-era inference workloads**, where trajectory-level performance matters more than isolated request latency.

---

# Next Work (Recommended)

To further strengthen this benchmark:

- Extend trajectory length (10–20 steps)
- Run multiple seeds for statistical confidence
- Normalize latency by prompt tokens (efficiency index)
- Separate prefill vs decode contributions explicitly
- Add tool-using agent workloads (real external calls)



