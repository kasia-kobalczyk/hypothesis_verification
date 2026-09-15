# PROJECT_STATE

## Active phase
Freeze the benchmark schema and convert the first eight ACCEPT cases into structured dossiers compatible with the existing `kasia-kobalczyk/hypothesis_verification` repository and its consequence-graph experiment runner.

## Important execution architecture clarified from repository inspection
- Claude Code is the executor / technical research agent, not the scientific verifier model.
- The actual consequence-graph system is run through API-backed LLM agents/models inside the repository experiment harness.
- Temporal safety is enforced by `LiteratureSearchService` and `CutoffRegistry`, not by trusting the agent to obey a date instruction.
- Agents cannot choose or override cutoff dates through the literature-search API.
- Search, citation/reference expansion, metadata lookup, and prompt rendering all reapply temporal filtering; post-cutoff records are withheld from model context.
- The consequence-graph implementation already supports arbitrary k>=2 hypotheses conceptually, builds one shared proposition graph, cross-evaluates propositions against all hypotheses, retrieves proposition-level evidence, and performs Bayesian aggregation.
- Run artifacts already preserve prompts, graph, edge judgments, queries, retrieval, evidence, scores and reports.

## Frozen first tranche — ACCEPT
1. PFC working-memory storage vs top-down control.
2. Gcn4/Med15 soluble-complex vs transcriptional-condensate mechanisms.
3. Eukaryogenesis mitochondria-early vs mitochondria-intermediate/late.
4. Interhemispheric PFC specialized/lateralized vs redundant/shared storage.
5. GlnBP conformational selection vs induced fit.
6. Spider orb-web ancestral single origin/loss vs convergent independent origins.
7. Forest fragmentation edge-stress/degradation vs resource-release/productivity mechanisms.
8. Fly-wing developmental/genetic constraint vs correlational-selection explanation.

## Frozen benchmark-record schema
Each case should contain:
- case_id
- title
- domain
- phenomenon
- cutoff
- hypotheses[]
  - hypothesis_id
  - source_faithful_text
  - source_title
  - source_identifier / DOI / URL where available
  - source_public_date
  - articulation_type: explicit_in_source | reconstructed_from_pre_cutoff_sources
  - source_notes
- pre_cutoff_context
- consequence_matrix[]
  - observable_or_test
  - predictions_by_hypothesis
  - scientific_rationale
  - source_support
  - silence_as_null_check
- resolving_study
  - citation
  - DOI / preprint / repository identifiers
  - journal_public_date
  - earliest_public_date
  - earliest_public_channel
- resolving_observations[]
- resolution
  - type: favored | disfavored | mixed | regime_dependent | component_wise | unresolved
  - summary
- leakage_audit
  - channels_checked
  - pre_cutoff_equivalent_result_found
  - findings
  - remaining_uncertainty
- construction_status
- construction_rationale
- ambiguities_and_limitations
- benchmark_visibility
  - visible_to_verifier: phenomenon, cutoff, hypothesis texts, pre-cutoff context / literature as task design permits
  - hidden_annotations: consequence reference profile, resolving observations, resolution label, leakage notes

## Integration implication
The first experiment should adapt the eight accepted cases into the repository's existing benchmark input conventions rather than create a parallel execution stack. Claude should implement the adapter/dataset integration and run the existing API-agent consequence-graph method under the current temporal harness. Hidden benchmark annotations should remain evaluation-only and must not enter model prompts.

## Benchmark principles frozen with schema
- cutoff >= 2024-01-01
- phenomenon and hypotheses must predate cutoff
- resolving evidence must be post-cutoff
- alternatives must address the same phenomenon
- meaningful observable consequence differences are required
- silence is never converted into a null prediction
- no retrospective sharpening to manufacture contrast
- mixed/regime-dependent/component-wise resolutions are valid
- resolving evidence and hidden annotations are not exposed to the verifier by default
- reject rather than rescue structurally weak cases

## Current audited counts
- ACCEPT: 8
- BORDERLINE: 4
- REJECT: 5

## Construction conclusion so far
Recent explanatory-hypothesis benchmark construction is practically feasible, but the dominant cost is historical source auditing. The principal failure modes are pre-cutoff leakage, resolver-authored retrospective alternatives, hypotheses addressing different stages/aspects, asymmetric prediction structure, and disputes that were no longer genuinely live at the cutoff.

## Next execution target
Write full dossiers and a machine-readable repository-compatible dataset for the eight accepted cases, then issue a bounded Claude directive to integrate those records into the existing experiment runner and run the pre-existing consequence-graph system without tuning it on these eight cases.