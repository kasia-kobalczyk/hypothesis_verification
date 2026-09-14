# ResearchBench verification development slice — dev20-v1

> **DEVELOPMENT / DEBUGGING SET.** This slice is for building and debugging the
> method. Aggregate accuracy on it is not evidence for the method — see
> `STATUS.md`.

This directory contains a **frozen 20-row development slice** derived from the uploaded
ResearchBench ranking data.

## Selection protocol

The source contains 1,323 rows. Rows were grouped by DOI, leaving 962 unique source-paper
groups. One row per DOI was retained deterministically, and DOI groups were ordered by
SHA256(DOI). The previously frozen R1–R6 rubric was then applied conservatively.

A row was accepted only when:

1. the gold is an empirical or mechanistic scientific proposition;
2. at least one **raw, unmodified ResearchBench negative** addresses the same scientific
   target and disagrees with a substantive part of the gold;
3. the source target is presented as supported by the source study;
4. a temporal publication cutoff can be established;
5. no obvious row-level benchmark artifact invalidates the task; and
6. the target falls within the empirical-science scope.

No literature audit, consequence generation, graph quality, retrieval result, or expected
method performance was used to choose examples.

The 20th accepted item occurs at frozen screening rank **873**.

## Important policy

The hypotheses in `researchbench_dev20_v1.jsonl` are **verbatim ResearchBench text**.
They have not been rewritten to make consequence-based verification easier.

This is a development set, not a final held-out benchmark. The next required operation is
metadata verification: obtain each source paper's exact first-online date and set the
literature cutoff immediately before that date. Only after those dates are frozen should
we inspect pre-cutoff evidence.

## Files

- `researchbench_dev20_v1.jsonl` — the 20 frozen ResearchBench rows.
- `accepted_screening_decisions_v1.jsonl` — R1–R6 pass decisions and rationales.
- `manifest_v1.json` — sampling and anti-cherry-picking protocol.
