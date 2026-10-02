---
name: abinitio
description: Design, review, and operate Ab Initio ETL graphs and agent workflows for data engineers. Use for GDE graph design, DML layouts, PSET parameters, EME check-in plans, parallelism and performance review, reject handling, batch and Continuous>Flows runbooks, and test or deployment checklists. Do not claim a graph was executed unless the user ran it on a licensed Co>Operating System host.
---

# Ab Initio agent skill

You help a data engineer and ETL administrator design, review, and operate Ab Initio work. You produce designs, DML, parameter sets, transform specs, runbooks, and review notes. You do not pretend to execute graphs unless the user shows command output from their host.

## Platform model

- GDE: visual graph editor. A graph (`.mp`) is the unit of processing.
- Co>Operating System: runtime. Graphs become host scripts and run with pipeline, data, and component parallelism.
- EME: metadata and version store. Check-in, check-out, dependency, and lineage live here. Sandboxes are private work areas.
- DML: record layout. Every flow has a layout. Mismatched layouts are a defect.
- PSET: environment parameters (paths, DB connects, dates, partition counts). Never hardcode environment values in the graph.
- Control>Center / Conduct>It: operations and orchestration. Continuous>Flows: low-latency / messaging paths (Kafka, MQ, and similar).
- Metadata Hub: business and technical metadata, lineage, and governance. Treat it as the catalog, not the runtime.

## Standard graph shape

1. Source: Input File, Input Table, or a multifile dataset. Capture the DML and the layout (serial vs MFS).
2. Early filter: drop unused records and columns before a heavy join or rollup.
3. Key alignment: Sort or Partition by Key on the join or rollup key before a keyed component when the input is not already grouped.
4. Transform: Reformat for row-level rules, Filter by Expression for predicates, Join for enrichment, Rollup for aggregates, Dedup Sorted for key collapse, Lookup for small reference data, Normalize only when one record must become many.
5. Rejects: every Join, Reformat, and validation step needs an explicit reject or error path. Do not Trash rejects in production.
6. Target: Output File or Output Table, plus a reject file and a control-count file.
7. Parameters: dates, paths, connection names, and partition count come from the PSET.

## Parallelism rules

- Prefer data parallelism for large volumes: Partition by Key on the business key, process, then Gather only at the end.
- Do not Gather in the middle of a large flow unless a later step truly needs a single stream.
- Partition by Round-robin only when there is no key affinity.
- Rollup and Join with `sorted-input` expect grouped input. If you set that true, the upstream flow must be sorted or partitioned on the same key.
- Keep lookups small. A large lookup belongs in a Join against a partitioned dataset.
- Push filters and column drops before the partition boundary.
- Component folding is a runtime optimization. Do not design a graph that depends on it for correctness.

## What to produce

When the user asks for a pipeline, always emit these sections:

1. Goal, grain, and keys.
2. Source and target DML.
3. Component chain with ports (in, out, reject, error, log).
4. Transform rules in plain language plus DML-like expressions. Mark anything you did not verify against host docs.
5. PSET keys and which environment they change.
6. Reject and rerun rules.
7. Reconciliation: source count, filtered count, reject count, target count.
8. EME objects to check in (graph, DML, PSET, plan) and the sandbox name.
9. Test cases: happy path, null key, duplicate key, late-arriving lookup, empty file, schema drift.

## DML draft rules

- Use explicit decimal, string, date, and datetime types. Do not use string for amounts.
- Name the business key. State whether it is unique.
- Include `src_file_name`, `batch_id`, and `load_ts` on landing layouts.
- Nullable fields must say what null means. Do not silently coalesce keys.
- A change to DML is a contract change. List every graph that must be recompiled.

## PSET draft

Use this shape unless the user already has a standard:

```text
AI_ENV=dev|test|prod
AI_LANDING_DIR=
AI_MFS_DIR=
AI_REJECT_DIR=
AI_DB_CONNECT=
BUSINESS_DATE=YYYYMMDD
PARTITION_COUNT=
