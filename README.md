TrajectoryBench: Measuring Latency Amplification in Multi-Step LLM Workflows
What Makes This Different

Most benchmarks measure:

Single Prompt
     ↓
Single Response

TrajectoryBench measures:

Prompt
   ↓
Response
   ↓
Refinement
   ↓
Response
   ↓
Refinement
   ↓
Response

and records:

per-step latency
cumulative latency
prompt token growth
completion token growth
latency amplification factor
