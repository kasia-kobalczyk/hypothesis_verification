# DIRECTIVE — BENCH-GRAPH-PILOT-001

## Objective
Integrate the frozen eight-case explanatory-hypothesis benchmark tranche below into the existing `kasia-kobalczyk/hypothesis_verification` experiment framework and run the existing agentic consequence-graph verifier as a diagnostic pilot.

Scientific question:

> Does the existing “what else should be true?” consequence-graph pipeline behave more appropriately on genuine competing explanations of the same phenomenon than it did on ResearchBench-style parallel research proposals?

This is a method-diagnosis experiment, not a tuning exercise and not a benchmark-scale performance claim.

---

# PART I — SOURCE-OF-TRUTH BENCHMARK MANIFEST

The eight items below are FROZEN. Do not rediscover, rename, sharpen, replace, or reformulate the scientific alternatives except for purely mechanical serialization. If a bibliographic field needs verification, verify the metadata but do not change the scientific meaning. If something appears inconsistent, report it as a blocker rather than silently repairing it.

For each case, fields under **VERIFIER-VISIBLE** may be materialized into the verifier input. Fields under **HIDDEN EVALUATION ANNOTATIONS** must be stored separately and must never enter graph generation, retrieval queries, evidence-assessment prompts, aggregation inputs, or any other verifier context.

## CASE 1 — `pfc_storage_vs_control`

### VERIFIER-VISIBLE
**Domain:** systems/cognitive neuroscience

**Phenomenon:** What causal role does lateral prefrontal cortex, particularly superior precentral sulcus (sPCS), play in visual working memory: direct storage of mnemonic content or top-down control/prioritization of representations stored elsewhere?

**Cutoff:** `2024-01-01`

**H1 — PFC storage account:**
Prefrontal persistent activity is itself a substrate for working-memory storage; disrupting the relevant PFC population therefore disrupts the stored mnemonic representation.

Pre-cutoff source anchors:
- Riley & Constantinidis (2016), review of PFC working-memory storage/persistent-activity accounts.
- Classical PFC persistent-activity/storage literature cited therein.

**H2 — PFC top-down control account:**
PFC primarily controls, prioritizes, or allocates resources to working-memory representations maintained in sensory/posterior regions rather than directly storing the mnemonic content itself.

Pre-cutoff source anchors:
- Curtis & D'Esposito (2003).
- D'Esposito & Postle (2015).
- Serences (2016) and related pre-cutoff control/resource-allocation literature.

### HIDDEN EVALUATION ANNOTATIONS
Reference discriminators:
- Perturbing a true storage substrate should ordinarily degrade the stored memory representation.
- Under the resource-control account, disrupting prioritization can counterintuitively improve low-priority items by redistributing limited mnemonic resources more evenly.
- Priority allocation itself should become more even after disrupting a control locus.

Resolver:
- Hallenbeck et al., bioRxiv v1 posted `2024-05-12`, DOI `10.1101/2024.05.11.593696`.
- Journal: Journal of Neuroscience 2025, DOI `10.1523/JNEUROSCI.1552-24.2025`.

Resolving observations:
- Retinotopically guided sPCS TMS selectively improved low-priority-item memory and reduced prioritization rather than causing a general degradation of mnemonic quality.
- IPS stimulation did not show the same pattern.

Reference resolution: `favored` — top-down resource-control account favored over a simple storage account.

Leakage note: no effectively equivalent pre-2024 public TMS result showing the counterintuitive low-priority improvement was located. A companion resource-allocation preprint was also first posted on 2024-05-12.

---

## CASE 2 — `gcn4_med15_complex_vs_condensate`

### VERIFIER-VISIBLE
**Domain:** molecular/cell biology; transcriptional regulation

**Phenomenon:** How does the Gcn4 activation domain engage Mediator subunit Med15 to drive transcriptional activation: through soluble dynamic/fuzzy complexes, transcriptional condensates/co-phase-separation, or some relationship between the two?

**Cutoff:** `2024-01-01`

**H1 — soluble-complex/fuzzy-binding mechanism:**
Gcn4 activation domains activate transcription through dynamic multivalent contacts with Med15 activation-binding domains in soluble complexes; transcriptional activity should therefore track productive Gcn4–Med15 molecular binding/affinity even outside a condensed phase.

Pre-cutoff source anchors:
- Tuttle et al., Cell Reports (2018), Gcn4/Med15 dynamic multivalent binding.
- Earlier and subsequent pre-2024 fuzzy-complex work on Gcn4–Med15.

**H2 — condensate/co-phase-separation mechanism:**
Gcn4 activation domains can activate transcription through phase-separation capacity and co-condensation with Mediator/Med15; transcriptional output should therefore track co-phase-separation/Med15 recruitment into condensates under the proposed condensate mechanism.

Pre-cutoff source anchors:
- Boija et al., Cell (2018), transcription-factor activation domains and phase separation/condensation with Mediator.
- Subsequent pre-2024 transcriptional-condensate literature involving Gcn4/Med15.

### HIDDEN EVALUATION ANNOTATIONS
Reference discriminators:
- Soluble-complex model: activity should track soluble Gcn4–Med15 binding/affinity under non-condensed conditions.
- Condensate model: activity should track co-condensation/Med15 recruitment; prevailing DNA-scaffolded condensate framing also expected multivalent DNA binding to facilitate condensation.
- Strong condensation need not monotonically enhance transcription if condensates and soluble complexes are coupled but functionally non-equivalent.

Resolver:
- Bremer et al., bioRxiv v1 posted `2024-11-22`, DOI `10.1101/2024.11.21.624739`.
- Molecular Cell 2025, DOI `10.1016/j.molcel.2025.06.008`.

Resolving observations:
- Homotypic Gcn4 condensation propensity alone poorly predicted activity.
- DNA binding suppressed Gcn4 phase separation.
- Soluble Med15 binding and co-condensation propensity largely covaried.
- At strongest affinities, excess condensation was associated with lower-than-expected activity.

Reference resolution: `mixed` / `reconciliatory` — soluble complexes and condensates are coupled routes; neither simple exclusive account is sufficient, and strong condensation can attenuate activity.

Leakage note: no effectively equivalent pre-2024 head-to-head Gcn4/Med15 result was located.

---

## CASE 3 — `eukaryogenesis_mito_timing`

### VERIFIER-VISIBLE
**Domain:** evolutionary cell biology / eukaryogenesis

**Phenomenon:** During the evolutionary assembly of the eukaryotic cell, did mitochondrial endosymbiosis occur early and enable most subsequent eukaryotic complexity, or did substantial cellular complexity evolve in the archaeal host before mitochondrial acquisition?

**Cutoff:** `2025-01-01`

**H1 — mitochondria-early scenarios:**
Mitochondrial acquisition was an initiating/foundational event that preceded or enabled much of later eukaryotic cellular complexity; major eukaryote-specific cellular systems should therefore largely elaborate after mitochondrial acquisition.

Pre-cutoff source anchors:
- Long-standing mitochondria-early eukaryogenesis models, including Martin-type syntrophic/hydrogen scenarios and reviews classifying mitochondria-early models.

**H2 — mitochondria-intermediate/late, complex-host scenarios:**
Substantial eukaryotic cellular machinery—including cytoskeletal, membrane-remodelling/trafficking, endomembrane, phagocytic, and nuclear-associated complexity—evolved before mitochondrial acquisition in an already complex archaeal host.

Pre-cutoff source anchors:
- Pre-2024/2025 reviews explicitly distinguishing mitochondria-early from mitochondria-late/intermediate models.
- 2015 review literature describing mitochondria-late hypotheses.

### HIDDEN EVALUATION ANNOTATIONS
Reference discriminators:
- Relative timing of pre-LECA duplications associated with cytoskeleton, membrane trafficking, endomembranes, phagocytosis, and nucleus versus mitochondrial acquisition.
- Mitochondria-early predicts these major elaborations should predominantly postdate mitochondrial acquisition.
- Complex-host/late-mitochondrion predicts substantial elaboration before mitochondrial acquisition.

Resolver:
- Nature article DOI `10.1038/s41586-025-09808-z`, first published online `2025-12-03`.
- Associated code/data publicly released `2025-10-21/22`; treat this as earliest located effective public release.

Resolving observations:
- Relaxed-clock dating of pre-LECA duplications placed elaboration of cytoskeleton, membrane trafficking, endomembrane, phagocytic machinery, and nucleus before mitochondrial endosymbiosis.

Reference resolution: `favored` — rejects mitochondria-early scenarios and favors a complexified archaeal host with later mitochondrial acquisition, while not mapping perfectly onto every previously proposed late/intermediate scenario.

Leakage note:
- A Bristol MScR thesis awarded `2024-10-01` used related pre-LECA duplication timing but concluded in favor of a mitochondria-early scenario. Treat this as contrary pre-cutoff evidence demonstrating the dispute remained live, not leakage of the later result.
- No pre-2025 public preprint/abstract with the later CALM/complex-archaeon-late-mitochondrion result was located.

---

## CASE 4 — `pfc_interhemispheric_architecture`

### VERIFIER-VISIBLE
**Domain:** systems/cognitive neuroscience

**Phenomenon:** How do the two prefrontal hemispheres organize spatial working-memory representations across the visual field: as largely specialized/contralateral resources or as redundant/shared bilateral representations?

**Cutoff:** `2024-12-01`

**H1 — specialized/lateralized architecture:**
The hemispheres provide largely independent working-memory resources with a contralateral bias and selective interhemispheric transfer; bilateral-field advantages arise from partly separate capacity pools.

Pre-cutoff source anchors:
- Bilateral-field-advantage literature.
- Macaque electrophysiology showing stronger within-hemifield competition and contralateral organization.
- Pre-cutoff literature supporting hemisphere-specific storage.

**H2 — redundant/shared bilateral architecture:**
Working-memory representations can be carried by both hemispheres, providing robustness to unilateral disruption at some cost in duplicated capacity/precision.

Pre-cutoff source anchors:
- Unilateral-vs-bilateral perturbation results and shared-storage interpretations.
- A Cerebral Cortex paper published `2024-11-14` explicitly described the live uncertainty as hemisphere-specific versus shared internal memory storage.

### HIDDEN EVALUATION ANNOTATIONS
Reference discriminators:
- Specialized architecture: predominantly contralateral behavioral relevance; more independent hemisphere-specific storage; capacity advantage from separate pools.
- Redundant architecture: either hemisphere can carry behaviorally useful information about both visual fields; greater robustness to unilateral disruption; duplicated representations trade capacity for robustness/precision.
- Cross-hemisphere decoding-error correlations and hemisphere-local serial dependence distinguish aspects of redundancy versus independence.

Resolver:
- Tschiersch et al., bioRxiv first posted `2025-01-16`, DOI `10.1101/2025.01.15.633176`.
- Nature Communications, published `2026-07-20`, DOI `10.1038/s41467-026-75705-2`.

Resolving observations:
- Both hemispheres predicted behavioral imprecision across the visual field.
- Decoding errors were weakly correlated.
- Serial-dependence effects remained local within hemispheres.
- Network simulations showed redundancy can improve low-load robustness/precision, while lateralized inputs increase capacity under higher load.

Reference resolution: `regime_dependent` / `reconciliatory` — redundant weakly coupled architecture at low demand with specialization/capacity benefits emerging under greater demand.

Leakage note: no equivalent pre-cutoff simultaneous bilateral-PFC analysis with the later reconciliation was located.

---

## CASE 5 — `glnbp_induced_fit_vs_conformational_selection`

### VERIFIER-VISIBLE
**Domain:** molecular biophysics / protein-ligand binding

**Phenomenon:** How is glutamine binding coupled to the open-to-closed conformational transition of E. coli glutamine-binding protein (GlnBP)?

**Cutoff:** `2024-01-01`

**H1 — conformational selection:**
Apo-GlnBP samples a pre-existing binding-competent closed or semi-closed conformation; glutamine preferentially binds/captures that pre-existing conformation.

Pre-cutoff source anchors:
- Wang et al., Angewandte Chemie International Edition (2016), PMID `27730716`, combining NMR, MD, and smFRET and explicitly suggesting conformational selection from the apo ensemble.

**H2 — induced fit:**
Glutamine binds to open/binding-competent GlnBP before the major protein conformational rearrangement, after which GlnBP closes around the ligand.

Pre-cutoff source anchors:
- Classical interpretation of open apo versus closed holo structures.
- Chen et al., Communications Biology (2020), PMID `32747735`, proposing a hybrid pathway with initial conformational selection followed by induced fit, demonstrating that mechanism remained unsettled.

### HIDDEN EVALUATION ANNOTATIONS
Reference discriminators:
- Conformational selection requires apo-GlnBP to populate/exchange into a ligand-binding-competent closed/semi-closed state on a timescale compatible with binding.
- Induced fit does not require detectable pre-existing apo closed-state exchange; ligand binding can precede the major closure.
- Global relationships among conformational-exchange rates, ligand-association kinetics, and equilibrium populations differ between mechanisms.

Resolver:
- eLife reviewed preprint v1, DOI `10.7554/eLife.95304.1`, first public `2024-03-25`.
- Later revisions 2025-11-21; version of record 2026-06-02.

Resolving observations:
- No detectable apo or holo exchange between open and (semi-)closed conformations over roughly 100 ns–10 ms.
- Ligand binding tightly correlated with conformational change.
- Global analysis made conformational selection compatible only with an extreme unobserved exchange faster than ~100 ns, while induced fit remained compatible with all observations.

Reference resolution: `favored` — induced fit is the dominant mechanism over experimentally accessible timescales.

Leakage note: no effectively equivalent pre-2024 integrated kinetic/thermodynamic result ruling out conformational selection over the accessible timescale was located.

---

## CASE 6 — `spider_orb_web_origin`

### VERIFIER-VISIBLE
**Domain:** evolutionary biology / comparative genomics

**Phenomenon:** Why do distantly related cribellate and ecribellate spider lineages share orb-weaving behavior: inheritance from an ancient orb-weaving ancestor followed by repeated losses, or repeated independent/convergent origins?

**Cutoff:** `2026-01-01`

**H1 — ancient single origin with repeated losses:**
Orb-weaving evolved in an ancient common ancestor; descendant non-orb-weaving lineages repeatedly lost orb-associated traits and molecular functions.

Pre-cutoff source anchors:
- Coddington et al., PeerJ (2019), arguing that spiders repeatedly lost rather than repeatedly gained foraging webs and recovering an ancient orb-origin reconstruction under their preferred coding/model.

**H2 — repeated convergent/independent origins:**
Cribellate and ecribellate orb webs arose independently/repeatedly in separate lineages through convergent evolution.

Pre-cutoff source anchors:
- Fernández et al., Current Biology (2018), supporting repeated/convergent origins.
- Kallal et al., Cladistics, first online 2020 / issue 2021, rejecting a single origin and recovering multiple convergent orb origins.

### HIDDEN EVALUATION ANNOTATIONS
Reference discriminators:
- Ancient-origin/loss predicts orb-associated genes inherited from a common ancestor should show relaxed selection and/or gene loss in descendant lineages that lost orb-weaving.
- Convergent-origin predicts orb-associated genes should show convergent positive selection in independently orb-weaving lineages.

Resolver:
- Runnels, Miller & Gordus, bioRxiv posted `2026-04-01`, DOI `10.64898/2026.03.30.715290`.

Resolving observations:
- 491 genes showed relaxed selection in non-orb-weavers, consistent with ancestral orb-associated functions followed by loss.
- 96 genes showed positive selection associated with orb-weaving, consistent with convergent evolution.
- Additional orb-correlated gene loss/duplication patterns were found.

Reference resolution: `component_wise` / `mixed` — different components of modern orb-weaving likely have different evolutionary histories, some ancestral and lost, some convergent, others subsequently elaborated.

Leakage note: targeted searches found no pre-2026 conference abstract/preprint/indexed result from this study. A public GitHub analysis repository exists now; repository history should be rechecked before final release to ensure no pre-2026 discriminating result was publicly available.

---

## CASE 7 — `forest_fragmentation_resilience`

### VERIFIER-VISIBLE
**Domain:** forest ecology / global change biology

**Phenomenon:** How does forest fragmentation affect vegetation resilience to disturbance, and why can fragmented forests exhibit either degradation or enhanced growth/recovery depending on context?

**Cutoff:** `2024-01-01`

**H1 — edge-stress/degradation mechanism:**
Fragmentation increases exposure to heat, atmospheric dryness, wind, and drought stress, raising mortality and reducing ecosystem resilience, especially where water/heat stress dominates.

Pre-cutoff source anchors:
- Koelemeijer et al., Ecological Applications (2023), drought-amplified edge effects.
- Nunes et al., Nature Communications (2023), hotter/drier edge environments and biomass loss in Amazon fragments.

**H2 — resource-release/productivity mechanism:**
Edge formation can increase light availability and relax limiting-resource constraints, increasing growth, biomass, recovery capacity, and potentially resilience where climatic stress penalties are small enough.

Pre-cutoff source anchors:
- Morreale et al., Nature Communications (2021), reporting 36% higher growth and 24% higher biomass at temperate forest edges and attributing the effect largely to greater light availability/release from limiting constraints.
- Related pre-cutoff European temperate-edge work reporting increased carbon stocks near edges.

### HIDDEN EVALUATION ANNOTATIONS
Reference discriminators:
- Edge-stress account predicts fragmentation should covary with hotter/drier local microclimate and lower resilience where heat/water stress dominates.
- Resource-release account predicts fragmentation can increase light/resource availability and increase growth/recovery/resilience where stress penalties are weak.
- If both are real, the sign of fragmentation-resilience association should vary systematically by biome and covary with microclimate/resource differences.

Resolver:
- Nature Ecology & Evolution article DOI `10.1038/s41559-025-02776-7`, published `2025-07-08`.
- Earliest located study-specific public material: Zenodo code deposit `2025-05-22`, DOI `10.5281/zenodo.15488956`.
- Article received 2024-08-27; no preprint was located.

Resolving observations:
- Significant fragmentation-resilience relationship in ~77% of fragmented forests with opposite signs by biome.
- Tropical and temperate forests: fragmentation associated with increased local temperature/atmospheric dryness and lower resilience.
- Boreal forests: fragmentation associated with decreased atmospheric dryness, enhanced light resources, and higher resilience.

Reference resolution: `regime_dependent` — both mechanisms operate, with dominance depending on biome/environmental context.

Leakage note: no equivalent global biome-resolved fragmentation-resilience result was located before cutoff.

---

## CASE 8 — `fly_wing_constraint_vs_selection`

### VERIFIER-VISIBLE
**Domain:** evolutionary quantitative genetics / macroevolution

**Phenomenon:** Why does developmental/mutational/standing genetic variation in fly wing shape align strongly with macroevolutionary divergence over tens to hundreds of millions of years?

**Cutoff:** `2025-01-01`

**H1 — developmental/genetic constraint / line-of-least-resistance account:**
Macroevolution preferentially proceeds along directions of abundant developmental/genetic variation because the structure of available variation constrains which phenotypic directions can evolve readily.

Pre-cutoff source anchors:
- Houle et al., Nature (2017), explicitly discussing developmental/genetic constraint and lines of least resistance for fly-wing evolution.

**H2 — correlational-selection/common-fitness-surface account:**
Persistent correlational/stabilizing selection shapes developmental and mutational covariance; developmental bias and long-term divergence align because both are molded by the same fitness/allometric structure rather than because variation mechanically constrains evolutionary directions.

Pre-cutoff source anchors:
- Rohner & Berger, PNAS (2023), explicitly presenting correlational selection as an alternative explanation for the observed alignment.

### HIDDEN EVALUATION ANNOTATIONS
Reference discriminators:
- Simple constraint account predicts directions with little usable genetic/developmental variation should evolve more slowly.
- A constraint rescue based on hidden deleterious pleiotropy predicts apparent standing variation in disfavored directions should covary with fitness costs, making that variation effectively unusable.
- Correlational-selection account predicts substantial usable variation may exist without dictating evolutionary rates; alignment can instead track allometric/fitness structure shaped by selection.

Resolver:
- bioRxiv DOI `10.1101/2025.01.09.632237`, first public `2025-01-14`.
- Dryad dataset DOI `10.5061/dryad.08kprr599`, published `2025-01-15`.
- Nature Ecology & Evolution article DOI `10.1038/s41559-025-02639-1`, published `2025-02-07`.

Resolving observations:
- Alignment of developmental/standing variation and divergence extends across >900 dipteran taxa and ~185 My.
- No genetic covariation between wing shape and measured fitness components supporting the hidden-deleterious-pleiotropy rescue of simple constraint.
- Little evidence that genetic constraint determines macroevolutionary rates.
- Allometric correlational selection emerges as a plausible common cause of developmental bias and deep divergence.

Reference resolution: `favored` — correlational-selection/common-cause explanation favored over a simple constraint interpretation.

Leakage note: no pre-2025 public version containing the 185-million-year analysis or fitness test was located.

---

# PART II — EXECUTION ARCHITECTURE

## Critical assumptions
- You are the implementation/execution agent, not the scientific verifier.
- The verifier consists of the repository's existing API-backed agents/models.
- Use the existing `LiteratureSearchService` / `CutoffRegistry` temporal controls. Do not replace them with prompt-only date instructions.
- Agents must not be able to choose, relax, or override benchmark cutoffs.
- Hidden annotations above must never enter verifier prompts, retrieval queries, graph generation, evidence assessment, or scoring inputs.

## Step 1 — Inspect and reuse existing repository conventions
Before changing code:
1. Inspect current benchmark/data schemas, experiment runner, cutoff registry, consequence-graph implementation, literature-search service, scoring/inference code, and run-artifact/report formats.
2. Reuse existing abstractions wherever possible.
3. Do not create a parallel benchmark framework if a small adapter/schema extension is sufficient.
4. Preserve compatibility with historical ResearchBench experiments and existing artifacts.
5. Document exact existing paths/components reused.

## Step 2 — Materialize the frozen manifest
Create repository-native machine-readable records from PART I.

Create two logically and physically separable datasets/artifacts:

### A. verifier-visible benchmark input
Only:
- `case_id`
- `domain` if useful to existing schema
- phenomenon/scientific question
- exact frozen hypothesis texts
- frozen cutoff
- only approved pre-cutoff context if the existing runner requires it

### B. hidden evaluation annotations
- source anchors and bibliographic audit metadata
- reference consequence/discriminator matrix
- resolver identifiers/dates
- resolving observations
- resolution type/summary
- leakage audit
- construction notes

If source anchors are needed for provenance in the visible file, they may be stored as metadata only, but must not be injected into verifier prompts unless that is already an explicit benchmark design choice. Post-cutoff resolver information must never be exposed.

Add a hard projection/test proving hidden fields cannot flow into verifier input.

## Step 3 — Register and test temporal cutoffs
Use the cutoffs frozen in PART I.

Before running the verifier, demonstrate that:
1. search is cutoff-filtered;
2. citation/reference expansion is cutoff-filtered;
3. metadata/title/abstract retrieval cannot reintroduce post-cutoff records;
4. prompt rendering contains no hidden annotations;
5. resolver DOI/title/identifiers from hidden annotations are absent from verifier context.

Do not weaken temporal controls to accommodate any item.

## Step 4 — Run existing consequence-graph verifier WITHOUT tuning
Run all eight items with the pre-existing method.

Do not change in response to pilot results:
- prompts;
- edge/evidence label mappings;
- priors;
- aggregation rules;
- graph depth;
- retrieval thresholds;
- proposition abstraction policy;
- stopping criteria.

Do not use hidden reference consequences before/during graph generation.
Do not reuse the spent ResearchBench reserve for tuning.
If only a minimal general code change is required for the new dataset/schema or k>=2 support, make the smallest possible change and document it.

## Step 5 — Preserve full forensic artifacts
For each case retain, where supported:
- exact rendered verifier input;
- generated propositions/consequence nodes;
- graph edges and implication judgments;
- cross-hypothesis evaluations;
- literature queries;
- retrieved papers and cutoff metadata;
- evidence spans/judgments;
- aggregation inputs;
- final scores/ranking/support summary;
- model/provider/configuration identifiers;
- errors/retries.

## Step 6 — Post-hoc consequence-recovery evaluation
Only after each run is frozen, compare the generated graph with the hidden reference annotations.

Classify generated propositions at minimum as:
1. `reference_discriminator_recovered`
2. `novel_plausible_discriminator`
3. `compatible_non_discriminative`
4. `generic_component_fact`
5. `invalid_or_unsupported`
6. `silence_as_null_error`

Cross-evaluate every purported discriminator against all hypotheses. A proposition is not discriminative merely because it was generated from only one hypothesis.

If an automated matcher/judge is used, preserve raw judgments and enough evidence for manual review. Do not tune it on these eight cases.

## Step 7 — Analyze three capabilities separately
### A. Consequence discovery
Did the system independently recover scientifically discriminating consequences analogous to those later used by the resolving science?

Report per-case reference-discriminator coverage and examples of successes/failures.

### B. Historical evidence discovery
For useful discriminators, did the system find genuinely relevant pre-cutoff evidence?

Distinguish:
- no relevant historical evidence exists;
- retrieval failure;
- evidence-assessor failure;
- generic compatibility only;
- proposition/evidence construct mismatch.

### C. Hypothesis comparison
Given only pre-cutoff evidence, what did the system conclude?

Compare with hidden later resolution only after the run. Permit:
- one hypothesis favored;
- one disfavored;
- mixed support;
- regime/component dependence;
- insufficient evidence.

Do not force mixed benchmark cases into binary winner labels.

## Step 8 — Primary interpretation
Do NOT reduce the pilot to “accuracy out of 8.”

Primary questions:
1. Does the system generate genuinely discriminative consequence profiles more often than on ResearchBench?
2. Does it still drift toward generic assessable component facts?
3. Does it manufacture contrast through silence-as-null?
4. When the right discriminator is generated, can pre-cutoff retrieval find useful evidence?
5. When final assessment differs from later resolution, is failure attributable to consequence generation, retrieval, evidence relevance, aggregation, or genuinely insufficient historical evidence?

Simple case-level agreement counts may be reported descriptively only.

## Required outputs
1. Repository-native eight-case verifier-visible dataset.
2. Separate hidden annotation/evaluation dataset.
3. Minimal adapter/schema code if needed.
4. Tests for cutoff enforcement and hidden-field isolation.
5. One frozen run per case with the existing graph verifier.
6. Machine-readable post-hoc consequence-recovery analysis.
7. Human-readable pilot report.

Report must include:
- exact git commit/configuration;
- model/provider settings by API role;
- paths to benchmark/run artifacts;
- per-case cutoff;
- generated graph summary;
- consequence-recovery findings;
- evidence yield/relevance findings;
- final hypothesis assessment;
- comparison with hidden later resolution;
- failure attribution;
- descriptive aggregate summary;
- recommendation on whether graph architecture warrants evaluation on a ~20-case benchmark.

## Do not
- Do not modify/tune the verifier based on these eight outcomes.
- Do not expose post-cutoff resolver material to verifier context.
- Do not expose hidden reference consequences before runs are frozen.
- Do not reuse the spent ResearchBench reserve for tuning.
- Do not manufacture binary labels for mixed/regime-dependent cases.
- Do not treat silence as a null prediction.
- Do not create synthetic competing hypotheses.
- Do not rewrite the frozen hypotheses to make them easier to distinguish.
- Do not interpret perturbation stability as calibrated scientific truth probability.

## Acceptance criteria
Complete when:
1. all eight frozen cases from PART I are materialized exactly in repository-native form;
2. cutoff enforcement and hidden-annotation isolation are tested;
3. all eight are run through the pre-existing graph verifier without benchmark-specific tuning;
4. full forensic artifacts are preserved;
5. consequence recovery, historical evidence discovery, and final hypothesis comparison are evaluated separately;
6. the pilot report explains where the method succeeds/fails and whether scaling to the larger benchmark is justified.

A low final ranking agreement is not an execution failure. The experiment diagnoses whether correct task semantics change the behavior of the existing consequence-based verification architecture.