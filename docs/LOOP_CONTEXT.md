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

1. Expand Unity Catalog wrappers.
2. Expand Repos/Secrets/Tokens wrappers.
3. Keep tests synchronized with each wrapper batch.
4. Keep PyPI metadata/release docs current.
5. Execute continuous release cycles via loop maintainer process.
6. Expand account onboarding wrappers (credentials, storage configurations, networks).
7. Expand account private endpoint wrappers (VPC endpoints, customer-managed keys).
