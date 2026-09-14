"""Consequence graph — MILESTONE 2 (IMPLEMENTATION_SPEC.md §33).

Deliberately empty. The graph schema, generation and semantic merging are added
only once milestone 1 (benchmark, temporal safety, caching, baselines, runner,
tests) is complete and tested.

When implemented, note the invariants from §12 and §35:
  * proposition truth is `X_v`, retrieved literature evidence is `D_v`;
    there is no separate `C` variable or node type;
  * any node may be empirically assessable — there is no terminal
    "consequence" node type;
  * graph distance is not evidence strength;
  * the graph is frozen before any literature outcome is observed.
"""
