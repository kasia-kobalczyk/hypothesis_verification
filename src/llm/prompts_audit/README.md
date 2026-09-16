# Post-hoc audit prompts

These are NOT verifier prompts. They are used only by the post-hoc analysis
scripts (`scripts/analyze_pilot_*.py`), which run after a run is frozen and never
write back into anything the verifier can see.

They live in a separate directory rather than alongside the verifier prompts for
a specific reason: they are allowed to do things a verifier prompt must never do.

* **They may state the cutoff date.** `tests/test_invariants.py` forbids that in
  every verifier prompt, because the cutoff is enforced by the backend and must
  not be something a model is merely *asked* to respect. An auditor deciding
  whether relevant work existed by a given date genuinely needs the date.
* **They may show hidden benchmark annotations.** The reference discriminators
  and the resolving study are the answer key; showing them to the verifier would
  destroy the benchmark, and showing them to the auditor is the entire point.

Keeping them in a directory the verifier's `PromptLibrary` is never pointed at
makes the separation structural. A verifier run cannot render one of these by
accident, because it does not know they exist.
