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
- Patch version bump each successful release cycle.
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

1. Expand Jobs wrappers.
2. Expand Clusters wrappers.
3. Expand Account workspace lifecycle wrappers.
4. Keep tests synchronized with new wrappers.
5. Add CI/release automation and release runbook/changelog.
