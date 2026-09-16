# Hidden benchmark context — POST-HOC ONLY

**Not verifier evidence.** These annotations were hidden from the verifier and postdate each case's cutoff. They are provided so a reviewer can, *after* forming an independent judgment of a proposition, compare it with how the dispute was later resolved. Reviewing implication validity blind to this file is recommended.

## eukaryogenesis_mito_timing

- resolution type: `favored`
- resolution summary: Rejects mitochondria-early scenarios and favors a complexified archaeal host with later mitochondrial acquisition, while not mapping perfectly onto every previously proposed late/intermediate scenario.
- reference discriminators:
  - Relative timing of pre-LECA duplications associated with cytoskeleton, membrane trafficking, endomembranes, phagocytosis, and nucleus versus mitochondrial acquisition.
  - Mitochondria-early predicts these major elaborations should predominantly postdate mitochondrial acquisition.
  - Complex-host/late-mitochondrion predicts substantial elaboration before mitochondrial acquisition.
- resolving observations:
  - Relaxed-clock dating of pre-LECA duplications placed elaboration of cytoskeleton, membrane trafficking, endomembrane, phagocytic machinery, and nucleus before mitochondrial endosymbiosis.
- resolver: `{"earliest_public": {"channel": "code/data release", "date": "2025-10-21"}, "journal": {"date": "2025-12-03", "doi": "10.1038/s41586-025-09808-z", "venue": "Nature"}}`

## fly_wing_constraint_vs_selection

- resolution type: `favored`
- resolution summary: Correlational-selection/common-cause explanation favored over a simple constraint interpretation.
- reference discriminators:
  - Simple constraint account predicts directions with little usable genetic/developmental variation should evolve more slowly.
  - A constraint rescue based on hidden deleterious pleiotropy predicts apparent standing variation in disfavored directions should covary with fitness costs, making that variation effectively unusable.
  - Correlational-selection account predicts substantial usable variation may exist without dictating evolutionary rates; alignment can instead track allometric/fitness structure shaped by selection.
- resolving observations:
  - Alignment of developmental/standing variation and divergence extends across >900 dipteran taxa and ~185 My.
  - No genetic covariation between wing shape and measured fitness components supporting the hidden-deleterious-pleiotropy rescue of simple constraint.
  - Little evidence that genetic constraint determines macroevolutionary rates.
  - Allometric correlational selection emerges as a plausible common cause of developmental bias and deep divergence.
- resolver: `{"dataset": {"date": "2025-01-15", "doi": "10.5061/dryad.08kprr599", "venue": "Dryad"}, "journal": {"date": "2025-02-07", "doi": "10.1038/s41559-025-02639-1", "venue": "Nature Ecology & Evolution"}, "preprint": {"date": "2025-01-14", "doi": "10.1101/2025.01.09.632237", "venue": "bioRxiv"}}`

## forest_fragmentation_resilience

- resolution type: `regime_dependent`
- resolution summary: Both mechanisms operate, with dominance depending on biome/environmental context.
- reference discriminators:
  - Edge-stress account predicts fragmentation should covary with hotter/drier local microclimate and lower resilience where heat/water stress dominates.
  - Resource-release account predicts fragmentation can increase light/resource availability and increase growth/recovery/resilience where stress penalties are weak.
  - If both are real, the sign of the fragmentation-resilience association should vary systematically by biome and covary with microclimate/resource differences.
- resolving observations:
  - Significant fragmentation-resilience relationship in ~77% of fragmented forests with opposite signs by biome.
  - Tropical and temperate forests: fragmentation associated with increased local temperature/atmospheric dryness and lower resilience.
  - Boreal forests: fragmentation associated with decreased atmospheric dryness, enhanced light resources, and higher resilience.
- resolver: `{"earliest_public": {"channel": "Zenodo code deposit", "date": "2025-05-22", "doi": "10.5281/zenodo.15488956"}, "journal": {"date": "2025-07-08", "doi": "10.1038/s41559-025-02776-7", "venue": "Nature Ecology & Evolution"}, "note": "article received 2024-08-27; no preprint located"}`

## gcn4_med15_complex_vs_condensate

- resolution type: `mixed`
- resolution summary: Reconciliatory: soluble complexes and condensates are coupled routes; neither simple exclusive account is sufficient, and strong condensation can attenuate activity.
- reference discriminators:
  - Soluble-complex model: activity should track soluble Gcn4-Med15 binding/affinity under non-condensed conditions.
  - Condensate model: activity should track co-condensation/Med15 recruitment; prevailing DNA-scaffolded condensate framing also expected multivalent DNA binding to facilitate condensation.
  - Strong condensation need not monotonically enhance transcription if condensates and soluble complexes are coupled but functionally non-equivalent.
- resolving observations:
  - Homotypic Gcn4 condensation propensity alone poorly predicted activity.
  - DNA binding suppressed Gcn4 phase separation.
  - Soluble Med15 binding and co-condensation propensity largely covaried.
  - At strongest affinities, excess condensation was associated with lower-than-expected activity.
- resolver: `{"journal": {"doi": "10.1016/j.molcel.2025.06.008", "venue": "Molecular Cell 2025"}, "preprint": {"authors": "Bremer et al.", "date": "2024-11-22", "doi": "10.1101/2024.11.21.624739", "venue": "bioRxiv v1"}}`

## glnbp_induced_fit_vs_conformational_selection

- resolution type: `favored`
- resolution summary: Induced fit is the dominant mechanism over experimentally accessible timescales.
- reference discriminators:
  - Conformational selection requires apo-GlnBP to populate/exchange into a ligand-binding-competent closed/semi-closed state on a timescale compatible with binding.
  - Induced fit does not require detectable pre-existing apo closed-state exchange; ligand binding can precede the major closure.
  - Global relationships among conformational-exchange rates, ligand-association kinetics, and equilibrium populations differ between mechanisms.
- resolving observations:
  - No detectable apo or holo exchange between open and (semi-)closed conformations over roughly 100 ns-10 ms.
  - Ligand binding tightly correlated with conformational change.
  - Global analysis made conformational selection compatible only with an extreme unobserved exchange faster than ~100 ns, while induced fit remained compatible with all observations.
- resolver: `{"later": "revisions 2025-11-21; version of record 2026-06-02", "preprint": {"date": "2024-03-25", "doi": "10.7554/eLife.95304.1", "venue": "eLife reviewed preprint v1"}}`

## pfc_interhemispheric_architecture

- resolution type: `regime_dependent`
- resolution summary: Reconciliatory: redundant weakly coupled architecture at low demand with specialization/capacity benefits emerging under greater demand.
- reference discriminators:
  - Specialized architecture: predominantly contralateral behavioral relevance; more independent hemisphere-specific storage; capacity advantage from separate pools.
  - Redundant architecture: either hemisphere can carry behaviorally useful information about both visual fields; greater robustness to unilateral disruption; duplicated representations trade capacity for robustness/precision.
  - Cross-hemisphere decoding-error correlations and hemisphere-local serial dependence distinguish aspects of redundancy versus independence.
- resolving observations:
  - Both hemispheres predicted behavioral imprecision across the visual field.
  - Decoding errors were weakly correlated.
  - Serial-dependence effects remained local within hemispheres.
  - Network simulations showed redundancy can improve low-load robustness/precision, while lateralized inputs increase capacity under higher load.
- resolver: `{"journal": {"date": "2026-07-20", "doi": "10.1038/s41467-026-75705-2", "venue": "Nature Communications"}, "preprint": {"authors": "Tschiersch et al.", "date": "2025-01-16", "doi": "10.1101/2025.01.15.633176", "venue": "bioRxiv"}}`

## pfc_storage_vs_control

- resolution type: `favored`
- resolution summary: Top-down resource-control account favored over a simple storage account.
- reference discriminators:
  - Perturbing a true storage substrate should ordinarily degrade the stored memory representation.
  - Under the resource-control account, disrupting prioritization can counterintuitively improve low-priority items by redistributing limited mnemonic resources more evenly.
  - Priority allocation itself should become more even after disrupting a control locus.
- resolving observations:
  - Retinotopically guided sPCS TMS selectively improved low-priority-item memory and reduced prioritization rather than causing a general degradation of mnemonic quality.
  - IPS stimulation did not show the same pattern.
- resolver: `{"journal": {"doi": "10.1523/JNEUROSCI.1552-24.2025", "venue": "Journal of Neuroscience 2025"}, "preprint": {"authors": "Hallenbeck et al.", "date": "2024-05-12", "doi": "10.1101/2024.05.11.593696", "venue": "bioRxiv v1"}}`

## spider_orb_web_origin

- resolution type: `component_wise`
- resolution summary: Different components of modern orb-weaving likely have different evolutionary histories, some ancestral and lost, some convergent, others subsequently elaborated.
- reference discriminators:
  - Ancient-origin/loss predicts orb-associated genes inherited from a common ancestor should show relaxed selection and/or gene loss in descendant lineages that lost orb-weaving.
  - Convergent-origin predicts orb-associated genes should show convergent positive selection in independently orb-weaving lineages.
- resolving observations:
  - 491 genes showed relaxed selection in non-orb-weavers, consistent with ancestral orb-associated functions followed by loss.
  - 96 genes showed positive selection associated with orb-weaving, consistent with convergent evolution.
  - Additional orb-correlated gene loss/duplication patterns were found.
- resolver: `{"preprint": {"authors": "Runnels, Miller & Gordus", "date": "2026-04-01", "doi": "10.64898/2026.03.30.715290", "venue": "bioRxiv"}}`

