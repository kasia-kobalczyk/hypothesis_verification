# DIRECTIVE

Freeze the first benchmark-construction schema and convert the eight currently ACCEPTED explanatory-hypothesis cases into structured benchmark dossiers.

Accepted tranche:
1. PFC working-memory storage vs top-down control.
2. Gcn4/Med15 soluble-complex vs transcriptional-condensate mechanisms.
3. Eukaryogenesis mitochondria-early vs mitochondria-intermediate/late.
4. Interhemispheric PFC specialized/lateralized vs redundant/shared storage.
5. GlnBP conformational selection vs induced fit.
6. Spider orb-web ancestral single origin/loss vs convergent independent origins.
7. Forest fragmentation edge-stress/degradation vs resource-release/productivity mechanisms.
8. Fly-wing developmental/genetic constraint vs correlational-selection explanation.

Create a benchmark record schema that preserves:
- case_id
- title
- domain
- phenomenon
- cutoff
- hypotheses[] with source-faithful text, source identifiers, source dates, and whether explicitly named or reconstructed
- pre_cutoff_context
- consequence_matrix[] with observable/test, hypothesis-specific positive predictions, and rationale/source support
- resolving_study with all known identifiers and earliest_public_date
- resolving_observations[]
- resolution type (favored/disfavored/mixed/regime-dependent/component-wise/unresolved)
- leakage_audit with searched channels and findings
- construction_status
- construction_rationale
- ambiguities/limitations
- benchmark_visibility fields distinguishing verifier-visible inputs from hidden annotations

Do not expose resolving observations or hidden consequence annotations to a future verifier by default.

Also produce a summary report covering all eight cases, counts by resolution type/domain, common failure modes learned from rejected/borderline cases, and an assessment of scale-up to ~20 items.

Preserve the existing benchmark principles: no silence-as-null, no retrospective sharpening, no forced binary winners, cutoff >= 2024-01-01, hypotheses and phenomenon predate cutoff, and resolving evidence must be post-cutoff with no effective earlier leakage.