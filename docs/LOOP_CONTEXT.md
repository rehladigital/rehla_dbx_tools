# Continuous Loop Context

## Instruction Snapshot

User instruction:

"There are more functions in the link i provided

https://github.com/rehladigital/rehla-aw-databricks-tools.git

create different

build , push,test, fix, plan , create new ,release version , repeat

keep on repeating till i interrupt and think how it can be improved, search online find pain points etc. Retain context in best way and pass this initial instruction as soon as context is about to be expired"

## Operating Contract

- Direct pushes to `main`.
- Version policy for 300-cycle campaign:
  - Start at `1.0.0`
  - Major release milestone every 50 cycles
  - Minor checkpoint every 100 cycles
- Continuous loop runs until user interrupts.
- Minimum team roles in each cycle:
  - planner/research
  - api builder
  - test engineer
  - bug hunter
  - release manager
  - docs/quality reviewer

## Context Preservation Rules

At end of every cycle:

1. Append cycle outcomes to `docs/CYCLE_LOG.md`.
2. Capture unresolved bugs and prioritized next batch.
3. Record pushed commit SHAs and released version.
4. If context window is close to limit, restate this instruction snapshot verbatim and summarize current queue in <=12 lines.

## Current Focus Queue

1. Continue from run 61 with round-robin cloud assignment (AWS -> Azure -> GCP).
2. Keep cycle logging strictly factual: list exact functionality added and changed each cycle.
3. Keep tests synchronized with each wrapper batch.
4. Keep release metadata/docs current for 50/100-cycle checkpoints.
5. Continue context snapshots for long-run continuity.
