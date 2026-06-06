TrajectoryBench
Measuring Latency Amplification in Agent-Style Workloads
<img width="2782" height="1566" alt="image" src="https://github.com/user-attachments/assets/cbbfe4c8-a586-4632-90ce-342b66969751" />
```markdown
# Agent Trajectory Latency Benchmark — Mini Research Notes

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
