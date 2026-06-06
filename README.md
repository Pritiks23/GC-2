TrajectoryBench
Measuring Latency Amplification in Agent-Style Workloads

Traditional LLM benchmarks emphasize throughput and long-form generation. Agent-style workloads invert those assumptions, repeatedly processing large contexts to produce short structured outputs. As context accumulates across a trajectory, workflow latency can grow substantially even when individual generations remain small. This benchmark explores that behavior by measuring latency across increasingly context-heavy sequential workflows.
