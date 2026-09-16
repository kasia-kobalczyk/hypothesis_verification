# Graph pilot review — priority packet

The 40 nodes that together account for 80.1% of all absolute score influence across the eight cases, ordered by descending influence. Selected from verifier score contributions only. Rubric: `RUBRIC.md` · machine-readable: `review_set_priority.jsonl`.

| rank | review id | influence | cumulative | favours | case ranking changes if withheld |
| --- | --- | --- | --- | --- | --- |
| 1 | `GP1-pfc_storage_vs_control-X2` | 0.885 | 5% | H1 | no |
| 2 | `GP1-glnbp_induced_fit_vs_conformational_selection-X4` | 0.876 | 10% | H2 | no |
| 3 | `GP1-eukaryogenesis_mito_timing-X7` | 0.845 | 14% | H2 | no |
| 4 | `GP1-glnbp_induced_fit_vs_conformational_selection-X11` | 0.755 | 19% | H2 | no |
| 5 | `GP1-gcn4_med15_complex_vs_condensate-X3` | 0.636 | 22% | H1 | no |
| 6 | `GP1-glnbp_induced_fit_vs_conformational_selection-X3` | 0.636 | 26% | H2 | no |
| 7 | `GP1-glnbp_induced_fit_vs_conformational_selection-X5` | 0.636 | 29% | H1 | no |
| 8 | `GP1-forest_fragmentation_resilience-X1` | 0.611 | 33% | H1 | no |
| 9 | `GP1-eukaryogenesis_mito_timing-X4` | 0.521 | 35% | H2 | no |
| 10 | `GP1-eukaryogenesis_mito_timing-X6` | 0.521 | 38% | H2 | no |
| 11 | `GP1-forest_fragmentation_resilience-X7` | 0.466 | 41% | H1 | no |
| 12 | `GP1-pfc_interhemispheric_architecture-X2` | 0.394 | 43% | H1 | no |
| 13 | `GP1-fly_wing_constraint_vs_selection-X2` | 0.302 | 45% | H2 | no |
| 14 | `GP1-pfc_storage_vs_control-X6` | 0.302 | 46% | H2 | no |
| 15 | `GP1-forest_fragmentation_resilience-X4` | 0.279 | 48% | H1 | no |
| 16 | `GP1-forest_fragmentation_resilience-X5` | 0.279 | 50% | H1 | no |
| 17 | `GP1-gcn4_med15_complex_vs_condensate-X5` | 0.279 | 51% | H2 | **yes** |
| 18 | `GP1-glnbp_induced_fit_vs_conformational_selection-X15` | 0.276 | 53% | H2 | no |
| 19 | `GP1-pfc_storage_vs_control-X15` | 0.276 | 54% | H1 | no |
| 20 | `GP1-pfc_storage_vs_control-X24` | 0.276 | 56% | H2 | no |
| 21 | `GP1-eukaryogenesis_mito_timing-X24` | 0.274 | 57% | H2 | no |
| 22 | `GP1-glnbp_induced_fit_vs_conformational_selection-X8` | 0.254 | 59% | H2 | no |
| 23 | `GP1-glnbp_induced_fit_vs_conformational_selection-X9` | 0.254 | 60% | H2 | no |
| 24 | `GP1-pfc_storage_vs_control-X14` | 0.247 | 61% | H1 | no |
| 25 | `GP1-glnbp_induced_fit_vs_conformational_selection-X6` | 0.245 | 63% | H1 | no |
| 26 | `GP1-pfc_storage_vs_control-X3` | 0.245 | 64% | H1 | no |
| 27 | `GP1-eukaryogenesis_mito_timing-X2` | 0.240 | 65% | H1 | no |
| 28 | `GP1-eukaryogenesis_mito_timing-X10` | 0.239 | 67% | H2 | no |
| 29 | `GP1-eukaryogenesis_mito_timing-X12` | 0.239 | 68% | H2 | no |
| 30 | `GP1-eukaryogenesis_mito_timing-X22` | 0.225 | 69% | H2 | no |
| 31 | `GP1-forest_fragmentation_resilience-X23` | 0.216 | 70% | H1 | no |
| 32 | `GP1-spider_orb_web_origin-X12` | 0.215 | 72% | H2 | no |
| 33 | `GP1-forest_fragmentation_resilience-X24` | 0.193 | 73% | H1 | no |
| 34 | `GP1-glnbp_induced_fit_vs_conformational_selection-X17` | 0.193 | 74% | H1 | no |
| 35 | `GP1-pfc_storage_vs_control-X13` | 0.193 | 75% | H1 | no |
| 36 | `GP1-forest_fragmentation_resilience-X15` | 0.192 | 76% | H2 | no |
| 37 | `GP1-gcn4_med15_complex_vs_condensate-X18` | 0.192 | 77% | H2 | **yes** |
| 38 | `GP1-gcn4_med15_complex_vs_condensate-X23` | 0.192 | 78% | H2 | **yes** |
| 39 | `GP1-gcn4_med15_complex_vs_condensate-X9` | 0.187 | 79% | H1 | no |
| 40 | `GP1-spider_orb_web_origin-X11` | 0.187 | 80% | H2 | no |

## #1 · `GP1-pfc_storage_vs_control-X2`

**GP1-pfc_storage_vs_control-X2** — case `pfc_storage_vs_control`, node `X2`

> Persistent neural activity in prefrontal cortex encodes the content of items maintained in working memory.

- generated from **H1** (Candidate A); abstraction: `mechanistic`
- generator's stated reason: If prefrontal persistent activity is a substrate for storage, then the content of working memory must be represented in that activity.
- influence: **0.885** (rank 1 in case, 1 overall; cumulative 5%) — favours **H1**
- log-likelihood contribution: H1 +1.956, H2 +1.070
- removing it alone: evidence withheld → case log-odds +0.329 (ranking unchanged); node deleted → +1.758 (ranking unchanged)

**Hypotheses (as shown to the verifier)**

- **H1** (Candidate A): Prefrontal persistent activity is itself a substrate for working-memory storage; disrupting the relevant PFC population therefore disrupts the stored mnemonic representation.
- **H2** (Candidate B): PFC primarily controls, prioritizes, or allocates resources to working-memory representations maintained in sensory/posterior regions rather than directly storing the mnemonic content itself.

**Verifier cross-hypothesis judgments** — P(X|H) combines these by noisy-OR

| hypothesis | origin? | direct edge | route via parent | P(X\|H) |
| --- | --- | --- | --- | --- |
| H1 | yes | `strongly_implied` | — | 0.950 |
| H2 | no | `unlikely` | — | 0.300 |

- edge rationale, **H1** → node: If prefrontal persistent activity is the substrate for working-memory storage, it follows directly that this activity encodes the content of items maintained in working memory.
- edge rationale, **H2** → node: If PFC primarily controls or allocates resources to representations stored elsewhere, it is less likely that persistent PFC activity itself encodes the mnemonic content.

**Verifier evidence** — label used in score: `strong_support` (log-LR +2.0)

- queries: `prefrontal cortex persistent activity`; `working memory item encoding`
- assessor rationale: Multiple records directly state that persistent activity in prefrontal cortex neurons encodes or maintains information about items in working memory. These include both empirical studies and reviews, with explicit mention of persistent activity representing or maintaining stimulus information during working memory tasks. The evidence spans primate and rodent studies, and includes both experimental and modeling work, all converging on the proposition as stated.
- supporting spans cited by the assessor:
  - "Neurons that generated persistent activity represented more information about the stimuli in both spatial and object working memory tasks."
  - "These results reveal that prefrontal neurons that generate persistent activity maintain information more reliably during working memory."
  - "Persistent activity of cue-representing neurons in the prefrontal cortex (PFC) is regarded as a neural basis for working memory."
  - "describe the effects of muscarinic M1 receptor stimulation and blockade on the generation and maintenance of persistent activity of prefrontal neurons encoding working memory representations."
  - "Persistent neuronal spiking has long been considered the mechanism underlying working memory"
  - "Persistent activity, the maintenance of neural activation over short periods of time in cortical networks, is widely thought to underlie the cognitive function of working memory."
  - "Nervous systems maintain information internally using persistent activity changes."
- 10 papers shown; key papers: `s2:3b03d751fc33823f163f06d345097e7c4bab1708`, `s2:59031196c9d4e166d206b87d4f61f487d140c373`, `s2:60a6bd5eb48146beb8281a643243ca7c63cbd0ea`, `s2:7d09f1318bb8aad56d476d5d2ca586e7e802a41d`, `s2:c20a74cc2800ea8aa66a9be003f9038527c088db`, `s2:d3038b219bf2a6c480211fada1dae89058000d62`
- _The evidence assessor returns ONE label for the node from all papers shown; the method has no per-paper contribution. Key papers and spans are those the assessor cited._

<details><summary>[1] Persistent activity in the prefrontal cortex during working memory. — C. Curtis, M. D’Esposito (2003); cutoff-filter date 2003-09-12; doi:10.1016/s1364-6613(03)00197-9</summary>

```text
[1] Persistent activity in the prefrontal cortex during working memory.
    id: s2:763be2b6f257f100e588bc8b41542d22c2c6d7ba
    date: 2003-09-01
    venue: Trends in Cognitive Sciences
    authors: C. Curtis, M. D’Esposito
    abstract: [no abstract available]
```
</details>

<details><summary>[2] **KEY** Interplay between persistent activity and activity-silent dynamics in prefrontal cortex underlies serial biases in working memory — Joao Barbosa, H. Stein, Rebecca L. Martinez, Adrià Galan-Gadea et al. (2020); cutoff-filter date 2020-06-22; doi:10.1038/s41593-020-0644-4</summary>

```text
[2] Interplay between persistent activity and activity-silent dynamics in prefrontal cortex underlies serial biases in working memory
    id: s2:d3038b219bf2a6c480211fada1dae89058000d62
    date: 2020-04-03
    venue: Nature Neuroscience
    authors: Joao Barbosa, H. Stein, Rebecca L. Martinez, Adrià Galan-Gadea, Sihai Li, J. Dalmau, Kirsten C. S. Adam, J. Valls-Solé
    abstract: Persistent neuronal spiking has long been considered the mechanism underlying working memory, but recent proposals argue for alternative ‘activity-silent’ substrates. Using monkey and human electrophysiology data, we show here that attractor dynamics that control neural spiking during mnemonic periods interact with activity-silent mechanisms in the prefrontal cortex (PFC). This interaction allows memory reactivations, which enhance serial biases in spatial working memory. Stimulus information was not decodable between trials, but remained present in activity-silent traces inferred from spiking synchrony in the PFC. Just before the new stimulus, this latent trace was reignited into activity that recapitulated the previous stimulus representation. Importantly, the reactivation strength correlated with the strength of serial biases in both monkeys and humans, as predicted by a computational model that integrates activity-based and activity-silent mechanisms. Finally, single-pulse transcranial magnetic stimulation applied to the human PFC between successive trials enhanced serial biases, thus demonstrating the causal role of prefrontal reactivations in determining working-memory behavior. Barbosa, Stein et al. show that rather than operating independently, PFC persistent activity and ‘activity-silent’ mechanisms interact dynamically to produce serial effects in working memory, consistent with attractor models with synaptic plasticity.
    note: possibly the same work as s2:e7000ee1f8eabf8922b0ccf1e6b56ba7d97ad9a5
```
</details>

<details><summary>[3] **KEY** Decoding working memory information from neurons with and without persistent activity in the primate prefrontal cortex. — Lilianna Thrower, Wen-Hao Dang, Rye G. Jaffe, Jasmine D. Sun et al. (2023); cutoff-filter date 2023-11-01; doi:10.1152/jn.00290.2023</summary>

```text
[3] Decoding working memory information from neurons with and without persistent activity in the primate prefrontal cortex.
    id: s2:59031196c9d4e166d206b87d4f61f487d140c373
    date: 2023-11-01
    venue: Journal of Neurophysiology
    authors: Lilianna Thrower, Wen-Hao Dang, Rye G. Jaffe, Jasmine D. Sun, Christos Constantinidis
    abstract: Persistent activity of neurons in the prefrontal cortex has been thought to represent the information maintained in working memory, though alternative models have challenged this idea. Theories that depend on the dynamic representation of information posit that stimulus information may be maintained by the activity pattern of neurons whose firing rate is not significantly elevated above their baseline during the delay period of working memory tasks. We thus tested the ability of neurons that do and do not generate persistent activity in the prefrontal cortex of monkeys to represent spatial and object information in working memory. Neurons that generated persistent activity represented more information about the stimuli in both spatial and object working memory tasks. The amount of information that could be decoded from neural activity depended on the choice of decoder and parameters used but neurons with persistent activity outperformed non-persistent neurons consistently. Although averaged across all neurons and stimuli, firing rate did not appear clearly elevated above baseline during the maintenance of neural activity particularly for object working memory, this grand average masked neurons that generated persistent activity selective for their preferred stimuli, which carried the majority of stimulus information. These results reveal that prefrontal neurons that generate persistent activity maintain information more reliably during working memory.
    note: possibly the same work as s2:9baaac246204af851f5ed535160cc131431eb3ac
```
</details>

<details><summary>[4] **KEY** Neuromodulation of Persistent Activity and Working Memory Circuitry in Primate Prefrontal Cortex by Muscarinic Receptors — S. Vijayraghavan, S. Everling (2021); cutoff-filter date 2021-03-15; doi:10.3389/fncir.2021.648624</summary>

```text
[4] Neuromodulation of Persistent Activity and Working Memory Circuitry in Primate Prefrontal Cortex by Muscarinic Receptors
    id: s2:3b03d751fc33823f163f06d345097e7c4bab1708
    date: 2021-03-15
    venue: Frontiers in Neural Circuits
    authors: S. Vijayraghavan, S. Everling
    abstract: Neuromodulation by acetylcholine plays a vital role in shaping the physiology and functions of cerebral cortex. Cholinergic neuromodulation influences brain-state transitions, controls the gating of cortical sensory stimulus responses, and has been shown to influence the generation and maintenance of persistent activity in prefrontal cortex. Here we review our current understanding of the role of muscarinic cholinergic receptors in primate prefrontal cortex during its engagement in the performance of working memory tasks. We summarize the localization of muscarinic receptors in prefrontal cortex, review the effects of muscarinic neuromodulation on arousal, working memory and cognitive control tasks, and describe the effects of muscarinic M1 receptor stimulation and blockade on the generation and maintenance of persistent activity of prefrontal neurons encoding working memory representations. Recent studies describing the pharmacological effects of M1 receptors on prefrontal persistent activity demonstrate the heterogeneity of muscarinic actions and delineate unexpected modulatory effects discovered in primate prefrontal cortex when compared with studies in rodents. Understanding the underlying mechanisms by which muscarinic receptors regulate prefrontal cognitive control circuitry will inform the search of muscarinic-based therapeutic targets in the treatment of neuropsychiatric disorders.
```
</details>

<details><summary>[5] **KEY** Subthreshold basis for reward-predictive persistent activity in mouse prefrontal cortex — Eunyoung Kim, Bilal A. Bari, Jeremiah Y. Cohen (2021); cutoff-filter date 2021-05-04; doi:10.1016/j.celrep.2021.109082</summary>

```text
[5] Subthreshold basis for reward-predictive persistent activity in mouse prefrontal cortex
    id: s2:7d09f1318bb8aad56d476d5d2ca586e7e802a41d
    date: 2021-05-01
    venue: Cell Reports
    authors: Eunyoung Kim, Bilal A. Bari, Jeremiah Y. Cohen
    abstract: SUMMARY Nervous systems maintain information internally using persistent activity changes. The mechanisms by which this activity arises are incompletely understood. We study prefrontal cortex (PFC) in mice performing behaviors in which stimuli predicted rewards at different delays with different probabilities. We measure membrane potential (Vm) from pyramidal neurons across layers. Reward-predictive persistent firing increases arise due to sustained increases in mean and variance of Vm and are terminated by reward or via centrally generated mechanisms based on reward expectation. Other neurons show persistent decreases in firing rates, maintained by persistent hyperpolarization that is robust to intracellular perturbation. Persistent activity is layer (L)- and cell-type-specific. Neurons with persistent depolarization are primarily located in upper L5, whereas those with persistent hyperpolarization are mostly found in lower L5. L2/3 neurons do not show persistent activity. Thus, reward-predictive persistent activity in PFC is spatially organized and conveys information about internal state via synaptic mechanisms.
```
</details>

<details><summary>[6] **KEY** Disparities in Short-Term Depression Among Prefrontal Cortex Synapses Sustain Persistent Activity in a Balanced Network. — J. Yoon, H. Lee, W. Ho, Suk-Ho Lee (2020); cutoff-filter date 2020-01-10; doi:10.1093/cercor/bhz076</summary>

```text
[6] Disparities in Short-Term Depression Among Prefrontal Cortex Synapses Sustain Persistent Activity in a Balanced Network.
    id: s2:c20a74cc2800ea8aa66a9be003f9038527c088db
    date: 2020-01-10
    venue: Cerebral Cortex
    authors: J. Yoon, H. Lee, W. Ho, Suk-Ho Lee
    abstract: Persistent activity of cue-representing neurons in the prefrontal cortex (PFC) is regarded as a neural basis for working memory. The contribution of short-term synaptic plasticity (STP) at different types of synapses comprising the cortical network to persistent activity, however, remains unclear. Characterizing STP at synapses of the rat PFC layer 5 network, we found that PFC synapses exhibit distinct STP patterns according to presynaptic and postsynaptic identities. Excitatory postsynaptic currents (EPSCs) from corticopontine (Cpn) neurons were well sustained throughout continued activity, with stronger depression at synapses onto fast-spiking interneurons than those onto pyramidal cells. Inhibitory postsynaptic currents (IPSCs) were sustained at a weaker level compared with EPSC from Cpn synapses. Computational modeling of a balanced network incorporating empirically observed STP revealed that little depression at recurrent excitatory synapses, combined with stronger depression at other synapses, could provide the PFC with a unique synaptic mechanism for the generation and maintenance of persistent activity.
```
</details>

<details><summary>[7] **KEY** Constraints on Persistent Activity in a Biologically Detailed Network Model of the Prefrontal Cortex with Heterogeneities — Joachim Hass, S. Ardid, Jason S. Sherfey, N. Kopell (2019); cutoff-filter date 2019-05-24; doi:10.1101/645663</summary>

```text
[7] Constraints on Persistent Activity in a Biologically Detailed Network Model of the Prefrontal Cortex with Heterogeneities
    id: s2:60a6bd5eb48146beb8281a643243ca7c63cbd0ea
    date: 2019-05-24
    venue: bioRxiv (preprint)
    authors: Joachim Hass, S. Ardid, Jason S. Sherfey, N. Kopell
    abstract: Persistent activity, the maintenance of neural activation over short periods of time in cortical networks, is widely thought to underlie the cognitive function of working memory. A large body of modeling studies has reproduced this kind of activity using cell assemblies with strengthened synaptic connections. However, almost all of these studies have considered persistent activity within networks with homogeneous neurons and synapses, making it difficult to judge the validity of such model results for cortical dynamics, which is based on highly heterogeneous neurons. Here, we consider persistent activity in a detailed, strongly data-driven network model of the prefrontal cortex with heterogeneous neuron and synapse parameters. Surprisingly, persistent activity could not be reproduced in this model without incorporating further constraints. We identified three factors that prevent successful persistent activity: heterogeneity in the cell parameters of interneurons, heterogeneity in the parameters of short-term synaptic plasticity and heterogeneity in the synaptic weights. Our model predicts that persistent activity is recovered if the heterogeneity in the activity of individual interneurons is diminished, which could be achieved by a homeostatic plasticity mechanism. Such a plasticity scheme could also compensate the heterogeneities in the synaptic weights and short-term plasticity when applied to the inhibitory synapses. Cell assemblies shaped in this way may be potentially targeted by distinct inputs or become more responsive to specific tuning or spectral properties. Furthermore, the model predicts that a network that exhibits persistent activity is not able to dynamically produce intrinsic in vivo-like irregular activity at the same time, because heterogeneous synaptic connections are required for these dynamics. Thus, the background noise in such a network must either be produced by external input or constitutes an entirely different state of the network, which [...]
```
</details>

<details><summary>[8] Interplay between persistent activity and activity-silent dynamics in prefrontal cortex during working memory — Joao Barbosa, H. Stein, Rebecca L. Martinez, A. Galán et al. (2019); cutoff-filter date 2019-09-12; doi:10.1101/763938</summary>

```text
[8] Interplay between persistent activity and activity-silent dynamics in prefrontal cortex during working memory
    id: s2:e7000ee1f8eabf8922b0ccf1e6b56ba7d97ad9a5
    date: 2019-09-12
    venue: bioRxiv (preprint)
    authors: Joao Barbosa, H. Stein, Rebecca L. Martinez, A. Galán, Kirsten C. S. Adam, Sihai Li, J. Valls-Solé, C. Constantinidis
    abstract: Persistent neuronal spiking has long been considered the mechanism underlying working memory, but recent proposals argue for alternative, “activity-silent” substrates for memory. Using monkey and human electrophysiology, we show here that attractor dynamics that control neural spiking during mnemonic periods interact with activity-silent mechanisms in PFC. This interaction allows memory reactivation, which enhance serial biases in spatial working memory. Stimulus information was not decodable between trials, but remained present in activity-silent traces inferred from spiking synchrony in PFC. Just prior to the new stimulus, this latent trace was reignited into activity that recapitulated the previous stimulus representation. Importantly, the reactivation strength correlated with the strength of serial biases in both monkeys and humans, as predicted by a computational model integrating activity-based and activity-silent mechanisms. Finally, single-pulse TMS applied to human prefrontal cortex prior to trial start enhanced serial biases, demonstrating the causal role of prefrontal reactivations in determining working memory behavior.
    note: possibly the same work as s2:d3038b219bf2a6c480211fada1dae89058000d62
```
</details>

<details><summary>[9] Decoding working memory information from persistent and activity-silent neurons in the primate prefrontal cortex — Lilianna Thrower, Wen-Hao Dang, Rye G. Jaffe, Jasmine D. Sun et al. (2023); cutoff-filter date 2023-07-28; doi:10.1101/2023.07.25.550371</summary>

```text
[9] Decoding working memory information from persistent and activity-silent neurons in the primate prefrontal cortex
    id: s2:9baaac246204af851f5ed535160cc131431eb3ac
    date: 2023-07-28
    venue: bioRxiv (preprint)
    authors: Lilianna Thrower, Wen-Hao Dang, Rye G. Jaffe, Jasmine D. Sun, C. Constantinidis
    abstract: [no abstract available]
    note: possibly the same work as s2:59031196c9d4e166d206b87d4f61f487d140c373
```
</details>

<details><summary>[10] The classic psychedelic DOI induces a persistent desynchronized state in medial prefrontal cortex — Randall J. Olson, Lowell Bartlett, Alex Sonneborn, Zachary Bretton-Granatoor et al. (2023); cutoff-filter date 2023-02-27; doi:10.1101/2023.02.26.529963</summary>

```text
[10] The classic psychedelic DOI induces a persistent desynchronized state in medial prefrontal cortex
    id: s2:5c4839ac4d4b6339a791c5a158f361d5851785f2
    date: 2023-02-27
    venue: bioRxiv (preprint)
    authors: Randall J. Olson, Lowell Bartlett, Alex Sonneborn, Zachary Bretton-Granatoor, Ayesha Firdous, Alexander Z. Harris, Atheir I. Abbas
    abstract: [no abstract available]
```
</details>

<details><summary>Post-hoc automated audit — NON-AUTHORITATIVE; uses hidden benchmark annotations</summary>

- primary auditor: `silence_as_null_error`; statuses {'H1': 'positive_or_present', 'H2': 'indeterminate'}; discriminative=False
- primary reasoning: H1 directly predicts that persistent neural activity in prefrontal cortex encodes working memory content, as it posits PFC as a storage substrate. H2, which posits PFC as a control locus, does not specify whether persistent activity encodes content or not; it is compatible with content being encoded elsewhere, so it is indeterminate.
- derived opposition call: `manufactured_from_silence`
- evidence attribution: `informative_evidence_found` — The retrieved papers directly address the proposition, with multiple studies explicitly stating that persistent neural activity in prefrontal cortex encodes or maintains the content of items in working memory. The assessor correctly identified strong support from empirical, modeling, and review papers spanning relevant species and methodologies. The process worked as intended.
- auditor retest: `silence_as_null_error`; discriminative=False
- disagreement flags: {'second_rater_vs_primary_discriminative': None, 'second_rater_vs_primary_status': None, 'retest_vs_primary_category': False, 'any': False}
</details>

**Human review** — `silence_as_null_error` · reviewer: Research Director · source: D045 · status: `first_pass_model_based_review` · genuinely discriminative: False · silence-as-null error: True · other fields not recorded

---

## #2 · `GP1-glnbp_induced_fit_vs_conformational_selection-X4`

**GP1-glnbp_induced_fit_vs_conformational_selection-X4** — case `glnbp_induced_fit_vs_conformational_selection`, node `X4`

> Apo-GlnBP adopts a closed or semi-closed conformation in the absence of glutamine.

- generated from **H1** (Candidate B); abstraction: `specific`
- influence: **0.876** (rank 1 in case, 2 overall; cumulative 10%) — favours **H2**
- log-likelihood contribution: H2 -0.300, H1 -1.177
- removing it alone: evidence withheld → case log-odds +0.965 (ranking unchanged); node deleted → +1.087 (ranking unchanged)

**Hypotheses (as shown to the verifier)**

- **H1** (Candidate B): Apo-GlnBP samples a pre-existing binding-competent closed or semi-closed conformation; glutamine preferentially binds/captures that pre-existing conformation.
- **H2** (Candidate A): Glutamine binds to open/binding-competent GlnBP before the major protein conformational rearrangement, after which GlnBP closes around the ligand.

**Verifier cross-hypothesis judgments** — P(X|H) combines these by noisy-OR

| hypothesis | origin? | direct edge | route via parent | P(X\|H) |
| --- | --- | --- | --- | --- |
| H2 | no | `unlikely` | — | 0.300 |
| H1 | yes | `implied` | — | 0.800 |

- edge rationale, **H2** → node: Candidate A states that GlnBP is open in the absence of glutamine and only closes after ligand binding, making a closed or semi-closed apo conformation less likely.
- edge rationale, **H1** → node: Candidate B asserts that apo-GlnBP samples closed or semi-closed conformations even without glutamine, making the proposition clearly expected.

**Verifier evidence** — label used in score: `strong_contradiction` (log-LR -2.0)

- queries: `Apo-GlnBP conformation`; `Apo-GlnBP glutamine binding structure`
- assessor rationale: Record [2] directly addresses the conformation of apo-GlnBP in the absence of glutamine, stating that the protein is crystallized in an open conformation and that NMR experiments show no evidence for a closed form. Furthermore, their paramagnetic NMR strategy finds that a major population of the closed apo species is highly improbable, and the average solution conformation matches the open crystal structure. This directly contradicts the proposition that apo-GlnBP adopts a closed or semi-closed conformation in the absence of glutamine.
- supporting spans cited by the assessor:
  - "Glutamine-binding protein (GlnBP) from Escherichia coli is a prototypical periplasmic binding protein that has been crystallized in an apo, “open” conformation, with its two domains far apart, and a holo, “closed” form, with proximal domains that engulf the cognate L-Gln ligand."
  - "A fundamental question about such large-scale conformational transitions—whether the closed state exists in the absence of ligand—is a matter of controversy in the case of GlnBP. Previously, NMR observations have indicated no evidence of the closed form, whereas experimentally validated computations have suggested a remarkable ~40% population. Here, a paramagnetic NMR strategy designed to specifically detect the putative apo-closed species shows that a major population of the latter is highly improbable. Further, NMR residual dipolar couplings collected under three anisotropic conditions fail to reveal differential domain alignment (which would otherwise signal interdomain dynamics) and establish that the average solution conformation is satisfied by the apo-open crystal structure. Our results indicate that the computational prediction of large-scale interdomain motions is far from trivial and may lead to grossly erroneous conclusions without proper experimental validation."
- 10 papers shown; key papers: `s2:eb71f0a80f7f2961fcf1898dd7951b1b511f449b`
- _The evidence assessor returns ONE label for the node from all papers shown; the method has no per-paper contribution. Key papers and spans are those the assessor cited._

<details><summary>[1] Conformational Dynamics of apo-GlnBP Revealed by Experimental and Computational Analysis. — Yitao Feng, Lu Zhang, Shaowen Wu, Zhijun Liu et al. (2016); cutoff-filter date 2016-11-02; doi:10.1002/anie.201606613</summary>

```text
[1] Conformational Dynamics of apo-GlnBP Revealed by Experimental and Computational Analysis.
    id: s2:011d4ac715a7d80122c2f1b0a60fcf0937ea6f2a
    date: 2016-11-02
    venue: Angewandte Chemie
    authors: Yitao Feng, Lu Zhang, Shaowen Wu, Zhijun Liu, Xin Gao, Xu Zhang, Maili Liu, Jianwei Liu
    abstract: [no abstract available]
    note: merged with 2 other version(s) of the same work
```
</details>

<details><summary>[2] **KEY** The Open Conformation Satisfies Multiple NMR Experiments on Apo Glutamine-Binding Protein: Overcoming Pitfalls in the Study of Interdomain Dynamics — H. Kooshapur, Junhe Ma, N. Tjandra, G. Bermejo (2019); cutoff-filter date 2019-09-13; doi:10.1002/anie.201911015</summary>

```text
[2] The Open Conformation Satisfies Multiple NMR Experiments on Apo Glutamine-Binding Protein: Overcoming Pitfalls in the Study of Interdomain Dynamics
    id: s2:eb71f0a80f7f2961fcf1898dd7951b1b511f449b
    date: 2019-09-13
    venue: Angewandte Chemie
    authors: H. Kooshapur, Junhe Ma, N. Tjandra, G. Bermejo
    abstract: Glutamine-binding protein (GlnBP) from Escherichia coli is a prototypical periplasmic binding protein that has been crystallized in an apo, “open” conformation, with its two domains far apart, and a holo, “closed” form, with proximal domains that engulf the cognate L-Gln ligand. A fundamental question about such large-scale conformational transitions—whether the closed state exists in the absence of ligand—is a matter of controversy in the case of GlnBP. Previously, NMR observations have indicated no evidence of the closed form, whereas experimentally validated computations have suggested a remarkable ~40% population. Here, a paramagnetic NMR strategy designed to specifically detect the putative apo-closed species shows that a major population of the latter is highly improbable. Further, NMR residual dipolar couplings collected under three anisotropic conditions fail to reveal differential domain alignment (which would otherwise signal interdomain dynamics) and establish that the average solution conformation is satisfied by the apo-open crystal structure. Our results indicate that the computational prediction of large-scale interdomain motions is far from trivial and may lead to grossly erroneous conclusions without proper experimental validation.
```
</details>

<details><summary>[3] Mechanisms for ligand binding to GluR0 ion channels: crystal structures of the glutamate and serine complexes and a closed apo state. — M. Mayer, R. Olson, E. Gouaux (2001); cutoff-filter date 2001-08-31; doi:10.1006/jmbi.2001.4884</summary>

```text
[3] Mechanisms for ligand binding to GluR0 ion channels: crystal structures of the glutamate and serine complexes and a closed apo state.
    id: s2:59d1f722a6654a45edca6cba29f1cf7a75711d63
    date: 2001-08-24
    venue: Journal of Molecular Biology
    authors: M. Mayer, R. Olson, E. Gouaux
    abstract: [no abstract available]
```
</details>

<details><summary>[4] Holo Protein Conformation Generation from Apo Structures by Ligand Binding Site Refinement — Jinze Zhang, Hao Li, Xuejun Zhao, Qi-Long Wu et al. (2022); cutoff-filter date 2022-11-07; doi:10.1021/acs.jcim.2c00895</summary>

```text
[4] Holo Protein Conformation Generation from Apo Structures by Ligand Binding Site Refinement
    id: s2:ba3a07e3ee7be450222f0258b68cad66e9524223
    date: 2022-11-07
    venue: Journal of Chemical Information and Modeling
    authors: Jinze Zhang, Hao Li, Xuejun Zhao, Qi-Long Wu, Shengqiang Huang
    abstract: An important part in structure-based drug design is the selection of an appropriate protein structure. It has been revealed that a holo protein structure that contains a well-defined binding site is a much better choice than an apo structure in structure-based drug discovery. Therefore, it is valuable to obtain a holo-like protein conformation from apo structures in the case where no holo structure is available. Meeting the need, we present a robust approach to generate reliable holo-like structures from apo structures by ligand binding site refinement with restraints derived from holo templates with low homology. Our method was tested on a test set of 32 proteins from the DUD-E data set and compared with other approaches. It was shown that our method successfully refined the apo structures toward the corresponding holo conformations for 23 of 32 proteins, reducing the average all-heavy-atom RMSD of binding site residues by 0.48 Å. In addition, when evaluated against all the holo structures in the protein data bank, our method can improve the binding site RMSD for 14 of 19 cases that experience significant conformational changes. Furthermore, our refined structures also demonstrate their advantages over the apo structures in ligand binding mode predictions by both rigid docking and flexible docking and in virtual screening on the database of active and decoy ligands from the DUD-E. These results indicate that our method is effective in recovering holo-like conformations and will be valuable in structure-based drug discovery.
```
</details>

<details><summary>[5] Effects of low temperatures on the conformation of apo-lactoferrin and its interactions with α-lactalbumin and β-lactoglobulin: Application of in silico approaches — Kevion K. Darmawan, T. Karagiannis, J. Hughes, D. Small et al. (2021); cutoff-filter date 2021-12-01; doi:10.1016/j.foodhyd.2021.107055</summary>

```text
[5] Effects of low temperatures on the conformation of apo-lactoferrin and its interactions with α-lactalbumin and β-lactoglobulin: Application of in silico approaches
    id: s2:af5e6fdb69b937c4549889050a10ff9515b54357
    date: 2021-12-01
    venue: Food Hydrocolloids
    authors: Kevion K. Darmawan, T. Karagiannis, J. Hughes, D. Small, A. Hung
    abstract: [no abstract available]
```
</details>

<details><summary>[6] Structural studies unravel the active conformation of apo RORγt nuclear receptor and a common inverse agonism of two diverse classes of RORγt inhibitors — Xiang Li, Marie D. Anderson, D. Collin, I. Muegge et al. (2017); cutoff-filter date 2017-05-26; doi:10.1074/jbc.m117.789024</summary>

```text
[6] Structural studies unravel the active conformation of apo RORγt nuclear receptor and a common inverse agonism of two diverse classes of RORγt inhibitors
    id: s2:dadbf63b3f146d848bdb2d3d7f3c49b703b7b15b
    date: 2017-05-25
    venue: Journal of Biological Chemistry
    authors: Xiang Li, Marie D. Anderson, D. Collin, I. Muegge, J. Wan, D. Brennan, Stanley Z Kugler, Donna Terenzio
    abstract: The nuclear receptor retinoid acid receptor-related orphan receptor γt (RORγt) is a master regulator of the Th17/IL-17 pathway that plays crucial roles in the pathogenesis of autoimmunity. RORγt has recently emerged as a highly promising target for treatment of a number of autoimmune diseases. Through high-throughput screening, we previously identified several classes of inverse agonists for RORγt. Here, we report the crystal structures for the ligand-binding domain of RORγt in both apo and ligand-bound states. We show that apo RORγt adopts an active conformation capable of recruiting coactivator peptides and present a detailed analysis of the structural determinants that stabilize helix 12 (H12) of RORγt in the active state in the absence of a ligand. The structures of ligand-bound RORγt reveal that binding of the inverse agonists disrupts critical interactions that stabilize H12. This destabilizing effect is supported by ab initio calculations and experimentally by a normalized crystallographic B-factor analysis. Of note, the H12 destabilization in the active state shifts the conformational equilibrium of RORγt toward an inactive state, which underlies the molecular mechanism of action for the inverse agonists reported here. Our findings highlight that nuclear receptor structure and function are dictated by a dynamic conformational equilibrium and that subtle changes in ligand structures can shift this equilibrium in opposite directions, leading to a functional switch from agonists to inverse agonists.
```
</details>

<details><summary>[7] Crystal structure of Zen4 in the apo state reveals a missing conformation of kinesin — Ruifang Guan, Lei Zhang, Q. Su, Keith J. Mickolajczyk et al. (2017); cutoff-filter date 2017-04-10; doi:10.1038/ncomms14951</summary>

```text
[7] Crystal structure of Zen4 in the apo state reveals a missing conformation of kinesin
    id: s2:499c567c7e48af3c53371f0052a34b2f585d820f
    date: 2017-04-10
    venue: Nature Communications
    authors: Ruifang Guan, Lei Zhang, Q. Su, Keith J. Mickolajczyk, Geng-Yuan Chen, W. Hancock, Yujie Sun, Yong-Fang Zhao
    abstract: Kinesins hydrolyse ATP to transport intracellular cargoes along microtubules. Kinesin neck linker (NL) functions as the central mechano-chemical coupling element by changing its conformation through the ATPase cycle. Here we report the crystal structure of kinesin-6 Zen4 in a nucleotide-free, apo state, with the NL initial segment (NIS) adopting a backward-docked conformation and the preceding α6 helix partially melted. Single-molecule fluorescence resonance energy transfer (smFRET) analyses indicate the NIS of kinesin-1 undergoes similar conformational changes under tension in the two-head bound (2HB) state, whereas it is largely disordered without tension. The backward-docked structure of NIS is essential for motility of the motor. Our findings reveal a key missing conformation of kinesins, which provides the structural basis of the stable 2HB state and offers a tension-based rationale for an optimal NL length to ensure processivity of the motor. Kinesins are molecular motors that travel along microtubules through a nucleotide-dependent stepping mechanism. Here the authors present the crystal structure of Zen4 (kinesin-6) in an apo state that sheds light on a key stepping intermediate of kinesin.
```
</details>

<details><summary>[8] The human mitochondrial Hsp60 in the APO conformation forms a stable tetradecameric complex — A. Enriquez, Humberto M Rojo, Jay M. Bhatt, S. Molugu et al. (2017); cutoff-filter date 2017-06-08; doi:10.1080/15384101.2017.1321180</summary>

```text
[8] The human mitochondrial Hsp60 in the APO conformation forms a stable tetradecameric complex
    id: s2:b0ba0d40c46b0f0b4b109feda79cfe412e6c4c0b
    date: 2017-06-08
    venue: Cell Cycle
    authors: A. Enriquez, Humberto M Rojo, Jay M. Bhatt, S. Molugu, Z. Hildenbrand, R. Bernal
    abstract: ABSTRACT The human mitochondrial chaperonin is a macromolecular machine that catalyzes the proper folding of mitochondrial proteins and is of vital importance to all cells. This chaperonin is composed of 2 distinct proteins, Hsp60 and Hsp10, that assemble into large oligomeric complexes that mediate the folding of non-native polypeptides in an ATP dependent manner. Here, we report the bacterial expression and purification of fully assembled human Hsp60 and Hsp10 recombinant proteins and that Hsp60 forms a stable tetradecameric double-ring conformation in the absence of co-chaperonin and nucleotide. Evidence of the stable double-ring conformation is illustrated by the 15 Å resolution electron microscopy reconstruction presented here. Furthermore, our biochemical analyses reveal that the presence of a non-native substrate initiates ATP-hydrolysis within the Hsp60/10 chaperonin to commence protein folding. Collectively, these data provide insight into the architecture of the intermediates used by the human mitochondrial chaperonin along its protein folding pathway and lay a foundation for subsequent high resolution structural investigations into the conformational changes of the mitochondrial chaperonin.
```
</details>

<details><summary>[9] Structures of apo Cas12a and its complex with crRNA and DNA reveal the dynamics of ternary complex formation and target DNA cleavage — Jianwei Li, C. Jobichen, S. Machida, Sun Meng et al. (2023); cutoff-filter date 2023-03-14; doi:10.1371/journal.pbio.3002023</summary>

```text
[9] Structures of apo Cas12a and its complex with crRNA and DNA reveal the dynamics of ternary complex formation and target DNA cleavage
    id: s2:a91c28f516ba093b06cef63b1e4a074dfabb60f7
    date: 2023-03-01
    venue: PLoS Biology
    authors: Jianwei Li, C. Jobichen, S. Machida, Sun Meng, Randy J. Read, Hongying Chen, Shi Jian, Yuren Adam Yuan
    abstract: Cas12a is a programmable nuclease for adaptive immunity against invading nucleic acids in CRISPR–Cas systems. Here, we report the crystal structures of apo Cas12a from Lachnospiraceae bacterium MA2020 (Lb2) and the Lb2Cas12a+crRNA complex, as well as the cryo-EM structure and functional studies of the Lb2Cas12a+crRNA+DNA complex. We demonstrate that apo Lb2Cas12a assumes a unique, elongated conformation, whereas the Lb2Cas12a+crRNA binary complex exhibits a compact conformation that subsequently rearranges to a semi-open conformation in the Lb2Cas12a+crRNA+DNA ternary complex. Notably, in solution, apo Lb2Cas12a is dynamic and can exist in both elongated and compact forms. Residues from Met493 to Leu523 of the WED domain undergo major conformational changes to facilitate the required structural rearrangements. The REC lobe of Lb2Cas12a rotates 103° concomitant with rearrangement of the hinge region close to the WED and RuvC II domains to position the RNA–DNA duplex near the catalytic site. Our findings provide insight into crRNA recognition and the mechanism of target DNA cleavage.
```
</details>

<details><summary>[10] Molecular glue CELMoD compounds are regulators of cereblon conformation — E. R. Watson, S. Novick, M. Matyskiela, P. Chamberlain et al. (2022); cutoff-filter date 2022-11-03; doi:10.1126/science.add7574</summary>

```text
[10] Molecular glue CELMoD compounds are regulators of cereblon conformation
    id: s2:0502a8068778f53b9cd3dabb60908f87dd99fa0a
    date: 2022-11-03
    venue: Science
    authors: E. R. Watson, S. Novick, M. Matyskiela, P. Chamberlain, A. H. de la Peña, Jinyi Zhu, Eileen Tran, P. Griffin
    abstract: Cereblon (CRBN) is a ubiquitin ligase (E3) substrate receptor protein co-opted by CRBN E3 ligase modulatory drug (CELMoD) agents that target therapeutically relevant proteins for degradation. Prior crystallographic studies defined the drug-binding site within CRBN’s thalidomide-binding domain (TBD), but the allostery of drug-induced neosubstrate binding remains unclear. We performed cryo–electron microscopy analyses of the DNA damage-binding protein 1 (DDB1)–CRBN apo complex and compared these structures with DDB1-CRBN in the presence of CELMoD compounds alone and complexed with neosubstrates. Association of CELMoD compounds to the TBD is necessary and sufficient for triggering CRBN allosteric rearrangement from an open conformation to the canonical closed conformation. The neosubstrate Ikaros only stably associates with the closed CRBN conformation, illustrating the importance of allostery for CELMoD compound efficacy and informing structure-guided design strategies to improve therapeutic efficacy. Description Closed complex for protein degradation The ability to target endogenous proteins for degradation with small molecules has opened up avenues for treating a wide range of diseases. Watson et al. investigated how a class of these molecules called CELMoDs (CRBN E3 ligase modulatory drugs) alter the conformational landscape of cereblon (CRBN), the enzyme that recognizes and marks substrates for degradation. The authors found that CELMoD compounds trigger a conformational rearrangement of CRBN from an entirely open and defunct form to an active closed form, but only for a subset of CRBN proteins. Next-generation CELMoDs, which are more effective therapies, appear to activate many more CRBN proteins by promoting closure much more efficiently, and future drug development may be able to harness this allosteric effect to improve efficacy. —MAF Cereblon modulatory drugs influence the conformational landscape of cereblon to induce neosubstrate binding and degradation.
```
</details>

<details><summary>Post-hoc automated audit — NON-AUTHORITATIVE; uses hidden benchmark annotations</summary>

- primary auditor: `silence_as_null_error`; statuses {'H2': 'indeterminate', 'H1': 'positive_or_present'}; discriminative=False
- primary reasoning: H1 (conformational selection) predicts that apo-GlnBP samples a closed or semi-closed conformation even without ligand, so the proposition is positive_or_present. H2 (induced fit) does not require or predict the presence of a closed or semi-closed conformation in the absence of ligand; it is silent on this, so indeterminate.
- derived opposition call: `manufactured_from_silence`
- evidence attribution: `informative_evidence_found` — The retrieval system surfaced a paper (record [2]) that directly addresses the conformation of apo-GlnBP in the absence of glutamine, providing clear experimental evidence that contradicts the proposition. The assessor correctly identified and used this evidence in their conclusion. The process worked as intended.
- disagreement flags: {'second_rater_vs_primary_discriminative': None, 'second_rater_vs_primary_status': None, 'retest_vs_primary_category': None, 'any': False}
</details>

**Human review** — `silence_as_null_error` · reviewer: Research Director · source: D045 · status: `first_pass_model_based_review` · genuinely discriminative: False · silence-as-null error: True · other fields not recorded

---

## #3 · `GP1-eukaryogenesis_mito_timing-X7`

**GP1-eukaryogenesis_mito_timing-X7** — case `eukaryogenesis_mito_timing`, node `X7`

> In eukaryotic lineages, the presence of a fully developed endomembrane system is observed only in cells that also contain mitochondria.

- generated from **H1** (Candidate A); abstraction: `specific`
- influence: **0.845** (rank 1 in case, 3 overall; cumulative 14%) — favours **H2**
- log-likelihood contribution: H1 -1.713, H2 -0.868
- removing it alone: evidence withheld → case log-odds -1.577 (ranking unchanged); node deleted → -1.577 (ranking unchanged)

**Hypotheses (as shown to the verifier)**

- **H1** (Candidate A): Mitochondrial acquisition was an initiating/foundational event that preceded or enabled much of later eukaryotic cellular complexity; major eukaryote-specific cellular systems should therefore largely elaborate after mitochondrial acquisition.
- **H2** (Candidate B): Substantial eukaryotic cellular machinery - including cytoskeletal, membrane-remodelling/trafficking, endomembrane, phagocytic, and nuclear-associated complexity - evolved before mitochondrial acquisition in an already complex archaeal host.

**Verifier cross-hypothesis judgments** — P(X|H) combines these by noisy-OR

| hypothesis | origin? | direct edge | route via parent | P(X\|H) |
| --- | --- | --- | --- | --- |
| H1 | yes | `implied` | X1 [H→parent `implied`, P=0.80] → `implied` | 0.948 |
| H2 | no | `unlikely` | X1 [H→parent `strongly_contradicted`, P=0.10] → `implied` | 0.671 |

- edge rationale, **H1** → node: If mitochondrial acquisition enabled later eukaryotic complexity, it is expected that a fully developed endomembrane system would only be present in cells with mitochondria.
- edge rationale, **H2** → node: If the endomembrane system evolved before mitochondria, it is less likely that its presence would be restricted to cells containing mitochondria.
- parent `X1`: Eukaryote-specific cellular structures such as the endomembrane system appear in lineages only after mitochondrial endosymbiosis.
- chain rationale, `X1` → node: If eukaryote-specific structures like the endomembrane system arise only after mitochondrial endosymbiosis, it is implied that fully developed endomembrane systems are found only in cells with mitochondria, though exceptions or partial developments are not ruled out.

**Verifier evidence** — label used in score: `strong_contradiction` (log-LR -2.0)

- queries: `eukaryotes endomembrane system mitochondria`; `mitochondria endomembrane system eukaryotic cells`
- assessor rationale: Record [9] directly states that Monocercomonoides exilis, a eukaryote lacking mitochondria, possesses a fully elaborated endomembrane system and canonical eukaryotic complexity. This contradicts the proposition that a fully developed endomembrane system is observed only in cells that also contain mitochondria. No other records directly address the proposition, but [9] provides clear, direct evidence against it.
- supporting spans cited by the assessor:
  - "Apart from the lack of mitochondria and peroxisomes, we show that M. exilis is a fully elaborated eukaryotic cell that is a promising model system in which eukaryotic cell biology can be investigated in the absence of mitochondria."
  - "the predicted cytoskeletal systems, the organization of endomembrane systems, and biosynthetic pathways also display canonical eukaryotic complexity."
- 10 papers shown; key papers: `s2:be8788b50047404bdd9f278ecf66e09de2584732`
- _The evidence assessor returns ONE label for the node from all papers shown; the method has no per-paper contribution. Key papers and spans are those the assessor cited._

<details><summary>[1] Bacterial Vesicle Secretion and the Evolutionary Origin of the Eukaryotic Endomembrane System. — S. Gould, S. Garg, W. Martin (2016); cutoff-filter date 2016-07-01; doi:10.1016/j.tim.2016.03.005</summary>

```text
[1] Bacterial Vesicle Secretion and the Evolutionary Origin of the Eukaryotic Endomembrane System.
    id: s2:abd443c19a1dc3f76c41f9008f6c83051e1090d3
    date: 2016-07-01
    venue: Trends in Microbiology
    authors: S. Gould, S. Garg, W. Martin
    abstract: [no abstract available]
```
</details>

<details><summary>[2] The phagotrophic origin of eukaryotes and phylogenetic classification of Protozoa. — T. Cavalier-Smith (2002); cutoff-filter date 2002-03-01; doi:10.1099/00207713-52-2-297</summary>

```text
[2] The phagotrophic origin of eukaryotes and phylogenetic classification of Protozoa.
    id: s2:86f68d207d34235eaed77f7cbc1ebb7f1dac4829
    date: 2002-03-01
    venue: International Journal of Systematic and Evolutionary Microbiology
    authors: T. Cavalier-Smith
    abstract: [no abstract available]
```
</details>

<details><summary>[3] Gene Duplications Trace Mitochondria to the Onset of Eukaryote Complexity — F. D. K. Tria, Julia Brueckner, Josip Skejo, Joana C. Xavier et al. (2019); cutoff-filter date 2021-03-16; doi:10.1093/gbe/evab055</summary>

```text
[3] Gene Duplications Trace Mitochondria to the Onset of Eukaryote Complexity
    id: s2:0060881fe926a598ffc25d72e8cedaa8147d9b22
    date: 2019-09-25
    venue: bioRxiv (preprint)
    authors: F. D. K. Tria, Julia Brueckner, Josip Skejo, Joana C. Xavier, Nils Kapust, Michael Knopp, Jessica L. E. Wimmer, Falk S. P. Nagies
    abstract: The last eukaryote common ancestor (LECA) lived 1.6 billion years ago1,2. It possessed nuclei, sex, an endomembrane system, mitochondria, and all key traits that make eukaryotic cells more complex than their prokaryotic ancestors2–6. The closest known relatives of the host lineage that acquired the mitochondrion are, however, small obligately symbiotic archaea that lack any semblance of eukaryotic cell complexity7. Although the steep evolutionary grade separating prokaryotes from eukaryotes increasingly implicates mitochondrial symbiosis at eukaryote origin4,7, the timing and evolutionary significance of mitochondrial origin remains debated. Gradualist theories contend that eukaryotes arose from archaea by slow accumulation of eukaryotic traits8–10 with mitochondria arriving late11, while symbiotic theories have it that mitochondria initiated the onset of eukaryote complexity in a non-nucleated archaeal host7 by gene transfers from the organelle4,12–14. The evolutionary process leading to LECA should be recorded in its gene duplications. Among 163,545 duplications in 24,571 gene trees spanning 150 sequenced eukaryotic genomes we identified 713 gene duplication events that occurred in LECA. LECA’s bacterially derived genes were duplicated more frequently than archaeal derived or eukaryote specific genes, reflecting the serial copying15,16 of genes from the mitochondrial endosymbiont to the archaeal host’s chromosomes prior to the onset of eukaryote genome complexity. Bacterial derived genes for mitochondrial functions, lipid synthesis, biosynthesis, as well as core carbon and energy metabolism in LECA were duplicated more often than archaeal derived genes and even more often than eukaryote-specific inventions for endomembrane, cytoskeletal or cell cycle functions. Gene duplications record the sequence of events at LECA’s origin and indicate that recurrent gene transfer from a resident mitochondrial endosymbiont preceded the onset of eukaryotic cellular complexity.
```
</details>

<details><summary>[4] Origin of eukaryotes from within archaea, archaeal eukaryome and bursts of gene gain: eukaryogenesis just made easier? — E. Koonin (2015); cutoff-filter date 2015-09-26; doi:10.1098/rstb.2014.0333</summary>

```text
[4] Origin of eukaryotes from within archaea, archaeal eukaryome and bursts of gene gain: eukaryogenesis just made easier?
    id: s2:a05e691c970394fb7fb46c1451a1528e81a94afd
    date: 2015-09-26
    venue: Philosophical Transactions of the Royal Society B: Biological Sciences
    authors: E. Koonin
    abstract: The origin of eukaryotes is a fundamental, forbidding evolutionary puzzle. Comparative genomic analysis clearly shows that the last eukaryotic common ancestor (LECA) possessed most of the signature complex features of modern eukaryotic cells, in particular the mitochondria, the endomembrane system including the nucleus, an advanced cytoskeleton and the ubiquitin network. Numerous duplications of ancestral genes, e.g. DNA polymerases, RNA polymerases and proteasome subunits, also can be traced back to the LECA. Thus, the LECA was not a primitive organism and its emergence must have resulted from extensive evolution towards cellular complexity. However, the scenario of eukaryogenesis, and in particular the relationship between endosymbiosis and the origin of eukaryotes, is far from being clear. Four recent developments provide new clues to the likely routes of eukaryogenesis. First, evolutionary reconstructions suggest complex ancestors for most of the major groups of archaea, with the subsequent evolution dominated by gene loss. Second, homologues of signature eukaryotic proteins, such as actin and tubulin that form the core of the cytoskeleton or the ubiquitin system, have been detected in diverse archaea. The discovery of this ‘dispersed eukaryome’ implies that the archaeal ancestor of eukaryotes was a complex cell that might have been capable of a primitive form of phagocytosis and thus conducive to endosymbiont capture. Third, phylogenomic analyses converge on the origin of most eukaryotic genes of archaeal descent from within the archaeal evolutionary tree, specifically, the TACK superphylum. Fourth, evidence has been presented that the origin of the major archaeal phyla involved massive acquisition of bacterial genes. Taken together, these findings make the symbiogenetic scenario for the origin of eukaryotes considerably more plausible and the origin of the organizational complexity of eukaryotic cells more readily explainable than they appeared until recently.
```
</details>

<details><summary>[5] Biology of Giardia lamblia — R. Adam (2001); cutoff-filter date 2001-07-31; doi:10.1128/cmr.14.3.447-475.2001</summary>

```text
[5] Biology of Giardia lamblia
    id: s2:8723012b4a1aae8e61fea9ee43703c299615afb3
    date: 2001-07-01
    venue: Clinical Microbiology Reviews
    authors: R. Adam
    abstract: [no abstract available]
```
</details>

<details><summary>[6] The Puzzling Conservation and Diversification of Lipid Droplets from Bacteria to Eukaryotes. — Josselin Lupette, E. Maréchal (2020); cutoff-filter date 2020-12-31; doi:10.1007/978-3-030-51849-3_11</summary>

```text
[6] The Puzzling Conservation and Diversification of Lipid Droplets from Bacteria to Eukaryotes.
    id: s2:20c8b2b850ee96f3b9c6861951258fab8397321e
    date: 2020
    venue: Results and problems in cell differentiation
    authors: Josselin Lupette, E. Maréchal
    abstract: [no abstract available]
```
</details>

<details><summary>[7] The symbiotic origin of the eukaryotic cell. — P. López-García, D. Moreira (2023); cutoff-filter date 2023-05-30; doi:10.5802/crbiol.118</summary>

```text
[7] The symbiotic origin of the eukaryotic cell.
    id: s2:bfbb10e2d371e78eb6ab4b8fd3818a598b4c8413
    date: 2023-05-30
    venue: Comptes rendus. Biologies
    authors: P. López-García, D. Moreira
    abstract: Eukaryogenesis represented a major evolutionary transition that led to the emergence of complex cells from simpler ancestors. For several decades, the most accepted scenario involved the evolution of an independent lineage of proto-eukaryotes endowed with an endomembrane system, including a nuclear compartment, a developed cytoskeleton and phagocytosis, which engulfed the alphaproteobacterial ancestor of mitochondria. However, the recent discovery by metagenomic and cultural approaches of Asgard archaea, which harbour many genes in common with eukaryotes and are their closest relatives in phylogenomic trees, rather supports scenarios based on the symbiosis of one Asgard-like archaeon and one or more bacteria at the origin of the eukaryotic cell. Here, we review the recent discoveries that led to this conceptual shift, briefly evoking current models of eukaryogenesis and the challenges ahead to discriminate between them and to establish a detailed, plausible scenario that accounts for the evolution of eukaryotic traits from those of their prokaryotic ancestors.
```
</details>

<details><summary>[8] A New Aspect to the Origin and Evolution of Eukaryotes — T. Vellai, K. Takács, G. Vida (1998); cutoff-filter date 1998-05-31; doi:10.1007/pl00006331</summary>

```text
[8] A New Aspect to the Origin and Evolution of Eukaryotes
    id: s2:bbae06b9bc6fb1e7b027e81e07f56468e85554c9
    date: 1998-05-01
    venue: Journal of Molecular Evolution
    authors: T. Vellai, K. Takács, G. Vida
    abstract: [no abstract available]
```
</details>

<details><summary>[9] **KEY** The Oxymonad Genome Displays Canonical Eukaryotic Complexity in the Absence of a Mitochondrion — Anna Karnkowska, S. C. Treitli, Ondřej Brzoň, L. Novak et al. (2019); cutoff-filter date 2019-08-06; doi:10.1093/molbev/msz147</summary>

```text
[9] The Oxymonad Genome Displays Canonical Eukaryotic Complexity in the Absence of a Mitochondrion
    id: s2:be8788b50047404bdd9f278ecf66e09de2584732
    date: 2019-08-06
    venue: Molecular biology and evolution
    authors: Anna Karnkowska, S. C. Treitli, Ondřej Brzoň, L. Novak, Vojtěch Vacek, Petr Soukal, Lael D. Barlow, Emily K. Herman
    abstract: Abstract The discovery that the protist Monocercomonoides exilis completely lacks mitochondria demonstrates that these organelles are not absolutely essential to eukaryotic cells. However, the degree to which the metabolism and cellular systems of this organism have adapted to the loss of mitochondria is unknown. Here, we report an extensive analysis of the M. exilis genome to address this question. Unexpectedly, we find that M. exilis genome structure and content is similar in complexity to other eukaryotes and less “reduced” than genomes of some other protists from the Metamonada group to which it belongs. Furthermore, the predicted cytoskeletal systems, the organization of endomembrane systems, and biosynthetic pathways also display canonical eukaryotic complexity. The only apparent preadaptation that permitted the loss of mitochondria was the acquisition of the SUF system for Fe–S cluster assembly and the loss of glycine cleavage system. Changes in other systems, including in amino acid metabolism and oxidative stress response, were coincident with the loss of mitochondria but are likely adaptations to the microaerophilic and endobiotic niche rather than the mitochondrial loss per se. Apart from the lack of mitochondria and peroxisomes, we show that M. exilis is a fully elaborated eukaryotic cell that is a promising model system in which eukaryotic cell biology can be investigated in the absence of mitochondria.
```
</details>

<details><summary>[10] Understanding protein translocation across chloroplast membranes: translocons and motor proteins. — Da Been Kim, Changhee Na, Inhwan Hwang, Dong Wook Lee (2022); cutoff-filter date 2022-10-12; doi:10.1111/jipb.13385</summary>

```text
[10] Understanding protein translocation across chloroplast membranes: translocons and motor proteins.
    id: s2:c3b6d59e074ede7956f9717f4a7c7228207d3eac
    date: 2022-10-12
    venue: Journal of Integrative Plant Biology
    authors: Da Been Kim, Changhee Na, Inhwan Hwang, Dong Wook Lee
    abstract: Subcellular organelles in eukaryotes are surrounded by lipid membranes. In an endomembrane system, vesicle trafficking is the primary mechanism for the delivery of organellar proteins to specific organelles. However, organellar proteins for chloroplasts, mitochondria, the nucleus, and peroxisomes that are translated in the cytosol are directly imported into their target organelles. Chloroplasts are a plant-specific organelle with outer and inner envelope membranes, a dual-membrane structure that is similar to mitochondria. Interior chloroplast proteins translated by cytosolic ribosomes are thus translocated through TOC and TIC complexes (translocons in the outer and inner envelope of chloroplasts, respectively), with stromal ATPase motor proteins playing a critical role in pulling preproteins through these import channels. Over the last three decades, the identity and function of TOC/TIC components and stromal motor proteins have been actively investigated, which has shed light on the action mechanisms at a molecular level. However, there remains some disagreement over the exact composition of TIC complexes and genuine stromal motor proteins. In this review, we discuss recent findings on the mechanisms by which proteins are translocated through TOC/TIC complexes and discuss future prospects for this field of research. This article is protected by copyright. All rights reserved.
```
</details>

<details><summary>Post-hoc automated audit — NON-AUTHORITATIVE; uses hidden benchmark annotations</summary>

- primary auditor: `silence_as_null_error`; statuses {'H1': 'positive_or_present', 'H2': 'indeterminate'}; discriminative=False
- primary reasoning: H1 predicts that major eukaryotic cellular systems like the endomembrane system should arise after mitochondrial acquisition, so only cells with mitochondria should have them. H2 does not specify whether the endomembrane system must be restricted to cells with mitochondria, as it allows for such complexity to arise before mitochondrial acquisition.
- derived opposition call: `manufactured_from_silence`
- evidence attribution: `informative_evidence_found` — The retrieval surfaced a paper (record [9]) that directly addresses and contradicts the proposition, providing clear evidence that a eukaryote without mitochondria can possess a fully developed endomembrane system. The assessor correctly identified and used this evidence. The process worked as intended.
- disagreement flags: {'second_rater_vs_primary_discriminative': None, 'second_rater_vs_primary_status': None, 'retest_vs_primary_category': None, 'any': False}
</details>

**Human review** — `invalid_or_weak_implication` · reviewer: Research Director · source: D045 · status: `first_pass_model_based_review` · genuinely discriminative: False · silence-as-null error: False · other fields not recorded

---

## #4 · `GP1-glnbp_induced_fit_vs_conformational_selection-X11`

**GP1-glnbp_induced_fit_vs_conformational_selection-X11** — case `glnbp_induced_fit_vs_conformational_selection`, node `X11`

> Glutamine binding is not required for GlnBP to adopt a closed conformation.

- generated from **H1** (Candidate B); abstraction: `mechanistic`
- generator's stated reason: If apo-GlnBP can be closed without glutamine, then the mechanism of closure does not strictly depend on ligand binding.
- influence: **0.755** (rank 2 in case, 4 overall; cumulative 19%) — favours **H2**
- log-likelihood contribution: H2 -0.958, H1 -1.713
- removing it alone: evidence withheld → case log-odds +1.087 (ranking unchanged); node deleted → +1.087 (ranking unchanged)

**Hypotheses (as shown to the verifier)**

- **H1** (Candidate B): Apo-GlnBP samples a pre-existing binding-competent closed or semi-closed conformation; glutamine preferentially binds/captures that pre-existing conformation.
- **H2** (Candidate A): Glutamine binds to open/binding-competent GlnBP before the major protein conformational rearrangement, after which GlnBP closes around the ligand.

**Verifier cross-hypothesis judgments** — P(X|H) combines these by noisy-OR

| hypothesis | origin? | direct edge | route via parent | P(X\|H) |
| --- | --- | --- | --- | --- |
| H2 | no | `unlikely` | X4 [H→parent `unlikely`, P=0.30] → `implied` | 0.713 |
| H1 | yes | `implied` | X4 [H→parent `implied`, P=0.80] → `implied` | 0.948 |

- edge rationale, **H2** → node: Candidate A implies that glutamine binding is necessary to induce the closed conformation, making the proposition less likely.
- edge rationale, **H1** → node: Candidate B suggests that GlnBP can adopt a closed conformation without glutamine, so the proposition is clearly expected.
- parent `X4`: Apo-GlnBP adopts a closed or semi-closed conformation in the absence of glutamine.
- chain rationale, `X4` → node: If Apo-GlnBP can adopt a closed or semi-closed conformation without glutamine, it suggests that glutamine binding is not strictly required for GlnBP to be in a closed conformation.

**Verifier evidence** — label used in score: `strong_contradiction` (log-LR -2.0)

- queries: `GlnBP closed conformation glutamine`; `GlnBP ligand-free closed structure`
- assessor rationale: Record [1] directly addresses whether GlnBP adopts a closed conformation in the absence of glutamine, reporting that a major population of the apo-closed species is highly improbable and that the average solution conformation matches the open form. Record [4] further states that the likelihood of a ligand-free closed conformation diminishes with temperature and supports the induced-fit model, implying closure is induced by ligand binding. Both records directly contradict the proposition that glutamine binding is not required for GlnBP to adopt a closed conformation.
- supporting spans cited by the assessor:
  - "A fundamental question about such large-scale conformational transitions—whether the closed state exists in the absence of ligand—is a matter of controversy in the case of GlnBP. Previously, NMR observations have indicated no evidence of the closed form, whereas experimentally validated computations have suggested a remarkable ~40% population. Here, a paramagnetic NMR strategy designed to specifically detect the putative apo-closed species shows that a major population of the latter is highly improbable. Further, NMR residual dipolar couplings collected under three anisotropic conditions fail to reveal differential domain alignment (which would otherwise signal interdomain dynamics) and establish that the average solution conformation is satisfied by the apo-open crystal structure."
  - "the likelihood that GlnBP can adopt a ligand free closed conformation in solution diminishes at higher temperatures. Our results support the induced-fit model as mode of action for GlnBP."
- 10 papers shown; key papers: `s2:eb71f0a80f7f2961fcf1898dd7951b1b511f449b`, `s2:f1114e0bbb4513350290b5e28bdf86aa47a1c0c7`
- _The evidence assessor returns ONE label for the node from all papers shown; the method has no per-paper contribution. Key papers and spans are those the assessor cited._

<details><summary>[1] **KEY** The Open Conformation Satisfies Multiple NMR Experiments on Apo Glutamine-Binding Protein: Overcoming Pitfalls in the Study of Interdomain Dynamics — H. Kooshapur, Junhe Ma, N. Tjandra, G. Bermejo (2019); cutoff-filter date 2019-09-13; doi:10.1002/anie.201911015</summary>

```text
[1] The Open Conformation Satisfies Multiple NMR Experiments on Apo Glutamine-Binding Protein: Overcoming Pitfalls in the Study of Interdomain Dynamics
    id: s2:eb71f0a80f7f2961fcf1898dd7951b1b511f449b
    date: 2019-09-13
    venue: Angewandte Chemie
    authors: H. Kooshapur, Junhe Ma, N. Tjandra, G. Bermejo
    abstract: Glutamine-binding protein (GlnBP) from Escherichia coli is a prototypical periplasmic binding protein that has been crystallized in an apo, “open” conformation, with its two domains far apart, and a holo, “closed” form, with proximal domains that engulf the cognate L-Gln ligand. A fundamental question about such large-scale conformational transitions—whether the closed state exists in the absence of ligand—is a matter of controversy in the case of GlnBP. Previously, NMR observations have indicated no evidence of the closed form, whereas experimentally validated computations have suggested a remarkable ~40% population. Here, a paramagnetic NMR strategy designed to specifically detect the putative apo-closed species shows that a major population of the latter is highly improbable. Further, NMR residual dipolar couplings collected under three anisotropic conditions fail to reveal differential domain alignment (which would otherwise signal interdomain dynamics) and establish that the average solution conformation is satisfied by the apo-open crystal structure. Our results indicate that the computational prediction of large-scale interdomain motions is far from trivial and may lead to grossly erroneous conclusions without proper experimental validation.
```
</details>

<details><summary>[2] Conformational Dynamics of apo-GlnBP Revealed by Experimental and Computational Analysis. — Yitao Feng, Lu Zhang, Shaowen Wu, Zhijun Liu et al. (2016); cutoff-filter date 2016-11-02; doi:10.1002/anie.201606613</summary>

```text
[2] Conformational Dynamics of apo-GlnBP Revealed by Experimental and Computational Analysis.
    id: s2:011d4ac715a7d80122c2f1b0a60fcf0937ea6f2a
    date: 2016-11-02
    venue: Angewandte Chemie
    authors: Yitao Feng, Lu Zhang, Shaowen Wu, Zhijun Liu, Xin Gao, Xu Zhang, Maili Liu, Jianwei Liu
    abstract: [no abstract available]
```
</details>

<details><summary>[3] Mechanisms for ligand binding to GluR0 ion channels: crystal structures of the glutamate and serine complexes and a closed apo state. — M. Mayer, R. Olson, E. Gouaux (2001); cutoff-filter date 2001-08-31; doi:10.1006/jmbi.2001.4884</summary>

```text
[3] Mechanisms for ligand binding to GluR0 ion channels: crystal structures of the glutamate and serine complexes and a closed apo state.
    id: s2:59d1f722a6654a45edca6cba29f1cf7a75711d63
    date: 2001-08-24
    venue: Journal of Molecular Biology
    authors: M. Mayer, R. Olson, E. Gouaux
    abstract: [no abstract available]
```
</details>

<details><summary>[4] **KEY** Temperature dependence of molecular interactions involved in defining stability of Glutamine Binding Protein and its complex with L-Glutamine — S. Pistolesi, N. Tjandra (2012); cutoff-filter date 2012-01-06; doi:10.1021/bi201494h</summary>

```text
[4] Temperature dependence of molecular interactions involved in defining stability of Glutamine Binding Protein and its complex with L-Glutamine
    id: s2:f1114e0bbb4513350290b5e28bdf86aa47a1c0c7
    date: 2012-01-06
    venue: Biochemistry
    authors: S. Pistolesi, N. Tjandra
    abstract: Temperature dependence of dynamic parameters derived from nuclear magnetic resonance (NMR) relaxation data are related to conformational entropy of the system under study. This provides information such as macromolecules stability and thermodynamics of ligand binding. We studied the temperature dependence of NMR order parameter of Glutamine binding protein (GlnBP), a periplasmic binding protein (PBP) highly specific to L-glutamine associated with its ABC transporter, with the goal of elucidating the dynamical differences between the respective ligand bound and free forms. We found that the protein-ligand interaction, which is stabilized at higher temperature, has a striking effect on the stability of the hydrophobic core of the large domain of GlnBP. Moreover, in contrast to what was found for less specific PBPs the decreasing backbone motion of the hinge region at increasing temperature supports the idea that the likelihood that GlnBP can adopt a ligand free closed conformation in solution diminishes at higher temperatures. Our results support the induced-fit model as mode of action for GlnBP. In addition, we found that the backbones of residues involved in a salt bridge do not necessarily become more rigid as the temperature rises as it was previously suggested [Vinther, J.M. et. al. (2011) J. Am. Chem. Soc., 271–278]. Our results show that for this to happen, these residues have to also directly interact with a region of the protein that is becoming more rigid as the temperature increases.
```
</details>

<details><summary>[5] Determination of the Solution Bound Conformation of an Amino-acid Binding Protein by NMR Paramagnetic Relaxation Enhancement: Use of a Single Flexible Paramagnetic Probe with Improved Estimation of Its Sampling Space — G. Bermejo, M. Strub, C. Ho, N. Tjandra (2009); cutoff-filter date 2009-07-15; doi:10.1021/ja902436g</summary>

```text
[5] Determination of the Solution Bound Conformation of an Amino-acid Binding Protein by NMR Paramagnetic Relaxation Enhancement: Use of a Single Flexible Paramagnetic Probe with Improved Estimation of Its Sampling Space
    id: s2:1cbc73facc1f2878f174180c43b8dddfc23c2c61
    date: 2009-07-15
    venue: Journal of the American Chemical Society
    authors: G. Bermejo, M. Strub, C. Ho, N. Tjandra
    abstract: We demonstrate the feasibility of elucidating the bound (“closed”) conformation of a periplasmic binding protein, the glutamine-binding protein (GlnBP), in solution, using paramagnetic relaxation enhancements (PREs) arising from a single paramagnetic group. GlnBP consists of two globular domains connected by a hinge. Using the ligand-free (“open”) conformation as a starting point, conjoined rigid-body/torsion-angle simulated annealing calculations were performed using backbone 1HN-PREs as a major source of distance information. Paramagnetic probe flexibility was accounted for via a multiple-conformer representation. A conventional approach where the entire PRE data set is enforced at once during simulated annealing yielded poor results due to inappropriate conformational sampling of the probe. On the other hand, significant improvements in coordinate accuracy were obtained by estimating the probe sampling space prior to structure calculation. Such sampling is achieved by refining the ensemble of probe conformers with intra-domain PREs only, keeping the protein backbone fixed in the open form. Subsequently, while constraining the probe to the previously found conformations, the domains are allowed to move relative to each other under the influence of the non-intra-domain PREs, giving the hinge region torsional degrees of freedom. Thus, by partitioning the protocol into a “probe sampling” and a “backbone sampling” stage, structures significantly closer to the X-ray structure of ligand-bound GlnBP were obtained.
```
</details>

<details><summary>[6] The differential ability of asparagine and glutamine in promoting the closed/active enzyme conformation rationalizes the Wolinella succinogenes L-asparaginase substrate specificity — H. Nguyen, D. Durden, A. Lavie (2017); cutoff-filter date 2017-01-31; doi:10.1038/srep41643</summary>

```text
[6] The differential ability of asparagine and glutamine in promoting the closed/active enzyme conformation rationalizes the Wolinella succinogenes L-asparaginase substrate specificity
    id: s2:645aed4778ea17272ee2b7abb2e03592750aee9e
    date: 2017-01-31
    venue: Scientific Reports
    authors: H. Nguyen, D. Durden, A. Lavie
    abstract: Many side effects of current FDA-approved L-asparaginases have been related to their secondary L-glutaminase activity. The Wolinella succinogenes L-asparaginase (WoA) has been reported to be L-glutaminase free, suggesting it would have fewer side effects. Unexpectedly, the WoA variant with a proline at position 121 (WoA-P121) was found to have L-glutaminase activity in contrast to Uniprot entry P50286 (WoA-S121) that has a serine residue at this position. Towards understanding how this residue impacts the L-glutaminase property, kinetic analysis was coupled with crystal structure determination of these WoA variants. WoA-S121 was confirmed to have much lower L-glutaminase activity than WoA-P121, yet both showed comparable L-asparaginase activity. Structures of the WoA variants in complex with L-aspartic acid versus L-glutamic acid provide insights into their differential substrate selectivity. Structural analysis suggests a mechanism by which residue 121 impacts the conformation of the conserved tyrosine 27, a component of the catalytically-important flexible N-terminal loop. Surprisingly, we could fully model this loop in either its open or closed conformations, revealing the roles of specific residues of an evolutionary conserved motif among this L-asparaginase family. Together, this work showcases critical residues that influence the ability of the flexible N-terminal loop for adopting its active conformation, thereby effecting substrate specificity.
```
</details>

<details><summary>[7] A coarse-grained method to predict the open-to-closed behavior of glutamine binding protein — Da-Shuai Lv, Weikang Gong, Yue Zhang, Yang Liu et al. (2017); cutoff-filter date 2017-08-17; doi:10.1016/j.chemphys.2017.05.019</summary>

```text
[7] A coarse-grained method to predict the open-to-closed behavior of glutamine binding protein
    id: s2:f4dd3b815162f85f7a8c5669e472c671e15cb8f2
    date: 2017-08-17
    venue: Chemical Physics
    authors: Da-Shuai Lv, Weikang Gong, Yue Zhang, Yang Liu, Chunhua Li
    abstract: [no abstract available]
```
</details>

<details><summary>[8] A L-glutamine binding protein modified MNM structured optical fiber biosensor based on surface plasmon resonance sensing for detection of L-glutamine metabolism in vitro embryo culture. — Jianfeng Chen, Liyun Ding, Jue Zhao, Xing-Dong Jiang et al. (2023); cutoff-filter date 2023-07-16; doi:10.2139/ssrn.4327577</summary>

```text
[8] A L-glutamine binding protein modified MNM structured optical fiber biosensor based on surface plasmon resonance sensing for detection of L-glutamine metabolism in vitro embryo culture.
    id: s2:6766c35f686e47e89d88b269e20bb2827f091f31
    date: 2023-07-16
    venue: Biosensors & bioelectronics
    authors: Jianfeng Chen, Liyun Ding, Jue Zhao, Xing-Dong Jiang, Fei Ma, Hai-Bing Li, Yumei Zhang
    abstract: A surface plasmon resonance (SPR) optical fiber sensor with multimode-coreless-multimode (MNM) structure was developed, which modified by L-glutamine-binding protein (QBP) for detection of L-glutamine (Gln). The QBP was immobilized on the surface of gold films by chemical cross-linking and exhibited a binding affinity for L-glutamine. The conformation of QBP can be changed from the "open" to the "closed", which led to a red-shift of the SPR peak when QBP bounded to L-glutamine. There was a good linear correlation between is a dependence of the SPR peak on and the concentration of L-glutamine concentration in the range 10-100 μM, with a sensitivity of 10.797nm/log10[Gln] for L-glutamine in the in vitro embryo culture (IVC) medium environment, and the limit of detection (LOD) is 1.187 μM. This QBP-modified MNM structure optical fiber SPR sensor provides a new idea for the developmental potential assessment of embryos in the process of in vitro embryo culture.
```
</details>

<details><summary>[9] Ion binding induces closed conformation in Pseudomonas 7A glutaminase-asparaginase (PGA): crystal structure of the PGA-SO4(2-)-NH4+ complex at 1.7 A resolution. — C. Jakob, Krzysztof Lewiński, M. W. LaCount, J. Roberts et al. (1997); cutoff-filter date 1997-01-28; doi:10.1021/bi961979x</summary>

```text
[9] Ion binding induces closed conformation in Pseudomonas 7A glutaminase-asparaginase (PGA): crystal structure of the PGA-SO4(2-)-NH4+ complex at 1.7 A resolution.
    id: s2:cb962c702b4fe2433997ba75bb5be323122be959
    date: 1997-01-28
    venue: Biochemistry
    authors: C. Jakob, Krzysztof Lewiński, M. W. LaCount, J. Roberts, Lukasz Lebioda
    abstract: [no abstract available]
```
</details>

<details><summary>[10] Revealing Allosteric Mechanism of Amino Acid Binding Proteins from Open to Closed State — Quanshan Shi, Ling Liu, Huaichuan Duan, Yu Jiang et al. (2023); cutoff-filter date 2023-10-17; doi:10.3390/molecules28207139</summary>

```text
[10] Revealing Allosteric Mechanism of Amino Acid Binding Proteins from Open to Closed State
    id: s2:d2e8b7984115311248318e8753264fccf34a20a5
    date: 2023-10-01
    venue: Molecules
    authors: Quanshan Shi, Ling Liu, Huaichuan Duan, Yu Jiang, Wenqin Luo, Guangzhou Sun, Yutong Ge, Li Liang
    abstract: Amino acid binding proteins (AABPs) undergo significant conformational closure in the periplasmic space of Gram-negative bacteria, tightly binding specific amino acid substrates and then initiating transmembrane transport of nutrients. Nevertheless, the possible closure mechanisms after substrate binding, especially long-range signaling, remain unknown. Taking three typical AABPs—glutamine binding protein (GlnBP), histidine binding protein (HisJ) and lysine/arginine/ornithine binding protein (LAOBP) in Escherichia coli (E. coli)—as research subjects, a series of theoretical studies including sequence alignment, Gaussian network model (GNM), anisotropic network model (ANM), conventional molecular dynamics (cMD) and neural relational inference molecular dynamics (NRI-MD) simulations were carried out. Sequence alignment showed that GlnBP, HisJ and LAOBP have high structural similarity. According to the results of the GNM and ANM, AABPs’ Index Finger and Thumb domains exhibit closed motion tendencies that contribute to substrate capture and stable binding. Based on cMD trajectories, the Index Finger domain, especially the I-Loop region, exhibits high molecular flexibility, with residues 11 and 117 both being potentially key residues for receptor–ligand recognition and initiation of receptor allostery. Finally, the signaling pathway of AABPs’ conformational closure was revealed by NRI-MD training and trajectory reconstruction. This work not only provides a complete picture of AABPs’ recognition mechanism and possible conformational closure, but also aids subsequent structure-based design of small-molecule oncology drugs.
```
</details>

<details><summary>Post-hoc automated audit — NON-AUTHORITATIVE; uses hidden benchmark annotations</summary>

- primary auditor: `reference_discriminator_recovered`; statuses {'H2': 'negative_or_absent', 'H1': 'positive_or_present'}; discriminative=True
- primary reasoning: H2 (induced fit) predicts that GlnBP only closes after glutamine binds, so closure without glutamine should not occur. H1 (conformational selection) predicts that apo-GlnBP can adopt a closed conformation even without glutamine, so closure without ligand is possible.
- matched hidden reference discriminator: Conformational selection requires apo-GlnBP to populate/exchange into a ligand-binding-competent closed/semi-closed state on a timescale compatible with binding.
- derived opposition call: `genuine`
- evidence attribution: `informative_evidence_found` — The retrieved literature directly addresses the proposition: multiple papers, especially records [1] and [4], provide experimental evidence that GlnBP does not adopt a closed conformation in the absence of glutamine, thus contradicting the proposition. The assessor correctly identified and interpreted this evidence. The process worked as intended.
- disagreement flags: {'second_rater_vs_primary_discriminative': None, 'second_rater_vs_primary_status': None, 'retest_vs_primary_category': None, 'any': False}
</details>

**Human review** — `silence_as_null_error` · reviewer: Research Director · source: D045 · status: `first_pass_model_based_review` · genuinely discriminative: False · silence-as-null error: True · other fields not recorded

---

## #5 · `GP1-gcn4_med15_complex_vs_condensate-X3`

**GP1-gcn4_med15_complex_vs_condensate-X3** — case `gcn4_med15_complex_vs_condensate`, node `X3`

> Soluble multivalent interactions between transcription factor activation domains and Mediator subunits can drive transcriptional activation in the absence of phase-separated condensates.

- generated from **H1** (Candidate A); abstraction: `class`
- generator's stated reason: If Gcn4 activates transcription through soluble multivalent contacts with Med15, it implies that this mechanism is possible for other transcription factors and Mediator subunits of the same class.
- influence: **0.636** (rank 1 in case, 5 overall; cumulative 22%) — favours **H1**
- log-likelihood contribution: H1 +1.164, H2 +0.528
- removing it alone: evidence withheld → case log-odds -0.641 (ranking unchanged); node deleted → -0.641 (ranking unchanged)

**Hypotheses (as shown to the verifier)**

- **H1** (Candidate A): Gcn4 activation domains activate transcription through dynamic multivalent contacts with Med15 activation-binding domains in soluble complexes; transcriptional activity should therefore track productive Gcn4-Med15 molecular binding/affinity even outside a condensed phase.
- **H2** (Candidate B): Gcn4 activation domains can activate transcription through phase-separation capacity and co-condensation with Mediator/Med15; transcriptional output should therefore track co-phase-separation/Med15 recruitment into condensates under the proposed condensate mechanism.

**Verifier cross-hypothesis judgments** — P(X|H) combines these by noisy-OR

| hypothesis | origin? | direct edge | route via parent | P(X\|H) |
| --- | --- | --- | --- | --- |
| H1 | yes | `strongly_implied` | — | 0.950 |
| H2 | no | `unlikely` | — | 0.300 |

- edge rationale, **H1** → node: Candidate A explicitly states that transcriptional activation is driven by soluble multivalent interactions between activation domains and Mediator subunits, even outside of condensed phases, which directly supports the proposition.
- edge rationale, **H2** → node: Candidate B posits that transcriptional activation depends on phase separation and co-condensation, making it less likely that soluble multivalent interactions alone can drive activation in the absence of condensates.

**Verifier evidence** — label used in score: `support` (log-LR +1.2)

- queries: `transcription factor activation domain Mediator`; `multivalent interaction transcription activation assay`
- assessor rationale: Record [3] directly states that transcription factor activation domains (Gal4 and Gcn4) interact with Mediator subunit Med15 via a 'fuzzy' (i.e., multivalent and dynamic) protein interface, and that this interaction drives transcriptional activation. The abstract does not mention phase-separated condensates, but it describes a soluble, sequence-independent mechanism for activation via AD-Mediator binding. No records directly address the necessity or absence of phase separation, but the described mechanism is consistent with soluble multivalent interactions driving activation.
- supporting spans cited by the assessor:
  - "The acidic activation domain (AD) of yeast transcription factor Gal4 plays a dual role in transcription repression and activation through binding to Gal80 repressor and Mediator subunit Med15."
  - "We show by NMR that each AD region binds the Mediator subunit Med15 using a “fuzzy” protein interface."
  - "The intrinsically disordered acidic activation domain (AD) of the yeast transcription factor Gal4 acts through binding to the Med15 subunit of the Mediator complex."
  - "Here, the authors show that Gal4 interacts with Med15 through an identical fuzzy binding mechanism as Gcn4 AD, which has a different sequence, revealing a common sequence-independent mechanism for AD-Mediator binding."
- 10 papers shown; key papers: `s2:115f993f3732be21d562cfa449172c05b7c2918f`
- _The evidence assessor returns ONE label for the node from all papers shown; the method has no per-paper contribution. Key papers and spans are those the assessor cited._

<details><summary>[1] Activation domain–mediator interactions promote transcription preinitiation complex assembly on promoter DNA — Greg T. Cantin, Jennitte L. Stevens, A. Berk (2003); cutoff-filter date 2003-09-23; doi:10.1073/pnas.2035253100</summary>

```text
[1] Activation domain–mediator interactions promote transcription preinitiation complex assembly on promoter DNA
    id: s2:36c9df41ab7825d0270badacf6714babcfa75124
    date: 2003-09-23
    venue: Proceedings of the National Academy of Sciences of the United States of America
    authors: Greg T. Cantin, Jennitte L. Stevens, A. Berk
    abstract: [no abstract available]
```
</details>

<details><summary>[2] Transformation suppressor activity of a Jun transcription factor lacking its activation domain — A. Lloyd, N. Yancheva, B. Wasylyk (1991); cutoff-filter date 1991-08-31; doi:10.1038/352635a0</summary>

```text
[2] Transformation suppressor activity of a Jun transcription factor lacking its activation domain
    id: s2:2793564faa1a795f7fd2034990d7d9d5dd690627
    date: 1991-08-15
    venue: Nature
    authors: A. Lloyd, N. Yancheva, B. Wasylyk
    abstract: [no abstract available]
```
</details>

<details><summary>[3] **KEY** Mediator subunit Med15 dictates the conserved “fuzzy” binding mechanism of yeast transcription activators Gal4 and Gcn4 — L. M. Tuttle, Derek Pacheco, Linda Warfield, D. Wilburn et al. (2021); cutoff-filter date 2021-04-13; doi:10.1038/s41467-021-22441-4</summary>

```text
[3] Mediator subunit Med15 dictates the conserved “fuzzy” binding mechanism of yeast transcription activators Gal4 and Gcn4
    id: s2:115f993f3732be21d562cfa449172c05b7c2918f
    date: 2021-04-13
    venue: Nature Communications
    authors: L. M. Tuttle, Derek Pacheco, Linda Warfield, D. Wilburn, S. Hahn, R. Klevit
    abstract: The acidic activation domain (AD) of yeast transcription factor Gal4 plays a dual role in transcription repression and activation through binding to Gal80 repressor and Mediator subunit Med15. The activation function of Gal4 arises from two hydrophobic regions within the 40-residue AD. We show by NMR that each AD region binds the Mediator subunit Med15 using a “fuzzy” protein interface. Remarkably, comparison of chemical shift perturbations shows that Gal4 and Gcn4, two intrinsically disordered ADs of different sequence, interact nearly identically with Med15. The finding that two ADs of different sequence use an identical fuzzy binding mechanism shows a common sequence-independent mechanism for AD-Mediator binding, similar to interactions within a hydrophobic cloud. In contrast, the same region of Gal4 AD interacts strongly with Gal80 via a distinct structured complex, implying that the structured binding partner of an intrinsically disordered protein dictates the type of protein–protein interaction. The intrinsically disordered acidic activation domain (AD) of the yeast transcription factor Gal4 acts through binding to the Med15 subunit of the Mediator complex. Here, the authors show that Gal4 interacts with Med15 through an identical fuzzy binding mechanism as Gcn4 AD, which has a different sequence, revealing a common sequence-independent mechanism for AD-Mediator binding. In contrast, Gal4 AD binds to the Gal80 repressor as a structured polypeptide, which strongly suggests that the structured binding partner dictates the type of protein–protein interaction for an intrinsically disordered protein.
```
</details>

<details><summary>[4] Mediator Subunit Gal11p/MED15 Is Required for Fatty Acid-dependent Gene Activation by Yeast Transcription Factor Oaf1p* — J. Thakur, H. Arthanari, Fa-Jun Yang, Katherine Chau et al. (2009); cutoff-filter date 2009-02-13; doi:10.1074/jbc.m808263200</summary>

```text
[4] Mediator Subunit Gal11p/MED15 Is Required for Fatty Acid-dependent Gene Activation by Yeast Transcription Factor Oaf1p*
    id: s2:0f3908dda63c5ba99ea31a36f113556bd31929cc
    date: 2009-02-13
    venue: Journal of Biological Chemistry
    authors: J. Thakur, H. Arthanari, Fa-Jun Yang, Katherine Chau, G. Wagner, A. Näär
    abstract: The yeast zinc cluster transcription factor Oaf1p activates transcription of target genes in response to direct binding of fatty acids in a manner analogous to the vertebrate nuclear receptor peroxisome proliferator-activated receptorα (PPARα). PPARs and other metazoan nuclear receptors productively engage several distinct LXXLL motif-containing co-activators, including p160 family members and the TRAP220/MED1 subunit of the Mediator co-activator, to promote ligand-dependent gene activation. Yeast, however, does not appear to harbor LXXLL motif co-activators, and the mechanism of fatty acid-dependent gene activation by the yeast PPARα analog Oaf1p is unknown. Here we show that the yeast Mediator subunit Gal11p/MED15 and its activator-targeted KIX domain plays a critical role in fatty acid-dependent transcriptional regulation of fatty acid β-oxidation and peroxisomal genes by Oaf1p and for the ability of yeast to utilize fatty acids as a sole carbon source. Moreover, structural studies by NMR spectroscopy reveal that the Oaf1p activation domain interacts with the Gal11p/MED15 KIX domain in a manner similar to the yeast zinc cluster family member and xenobiotic receptor Pdr1p, revealing that the Gal11p/MED15 KIX domain is a key target of several ligand-dependent transcription factors in yeast. Together with previous work showing that the Caenorhabditis elegans Gal11p/MED15 homolog MDT-15 plays a critical role in regulation of fatty acid metabolism by the nematode PPAR-like nuclear receptor NHR-49, the findings presented here provide evidence for an ancient and essential role of a Mediator co-activator subunit in regulation of fatty acid metabolism by nuclear receptor-like transcription factors in eukaryotes.
```
</details>

<details><summary>[5] A sequence-specific transcription activator motif and powerful synthetic variants that bind Mediator using a fuzzy protein interface — Linda Warfield, L. M. Tuttle, Derek Pacheco, R. Klevit et al. (2014); cutoff-filter date 2014-08-13; doi:10.1073/pnas.1412088111</summary>

```text
[5] A sequence-specific transcription activator motif and powerful synthetic variants that bind Mediator using a fuzzy protein interface
    id: s2:b991ecabf5e6aa3c9884d9bc9b4b5df0485349ef
    date: 2014-08-13
    venue: Proceedings of the National Academy of Sciences of the United States of America
    authors: Linda Warfield, L. M. Tuttle, Derek Pacheco, R. Klevit, S. Hahn
    abstract: [no abstract available]
```
</details>

<details><summary>[6] Human Mediator Subunit Med26 Functions As A Docking Site For Transcription Elongation Factors — Hidehisa Takahashi, T. Parmely, S. Sato, C. Tomomori-Sato et al. (2011); cutoff-filter date 2011-07-08; doi:10.1016/j.cell.2011.06.005</summary>

```text
[6] Human Mediator Subunit Med26 Functions As A Docking Site For Transcription Elongation Factors
    id: s2:a90c5c61dc4c25ac3cb26e06a2830abb94396398
    date: 2011-07-08
    venue: Cell
    authors: Hidehisa Takahashi, T. Parmely, S. Sato, C. Tomomori-Sato, C. A. Banks, Stephanie E. Kong, Henrietta Szutorisz, S. Swanson
    abstract: Summary Promoter proximal pausing by initiated RNA polymerase II (Pol II) and regulated release of paused polymerase into productive elongation has emerged as a major mechanism of transcription activation. Reactivation of paused Pol II correlates with recruitment of SuperElongationComplexes (SECs) containing ELL/EAF family members, P-TEFb, and other proteins, but the mechanism of their recruitment is currently a major unanswered question. Here, we present evidence for a role of human Mediator subunit Med26 in this process. We identify in the conserved N-terminal domain of Med26 overlapping docking sites for SEC and a second ELL/EAF-containing complex, as well as general initiation factor TFIID. In addition, we present evidence consistent with the model that Med26 can function as a molecular switch that interacts first with TFIID in the Pol II initiation complex and then exchanges TFIID for complexes containing ELL/EAF and P-TEFb to facilitate transition of Pol II into the elongation stage of transcription.
```
</details>

<details><summary>[7] Nuclear Factor E2-related Factor-2 (Nrf2) Is Required for NLRP3 and AIM2 Inflammasome Activation* — Changcheng Zhao, Devyn D. Gillette, Xinghui Li, Zhi-Bin Zhang et al. (2014); cutoff-filter date 2014-05-05; doi:10.1074/jbc.m114.563114</summary>

```text
[7] Nuclear Factor E2-related Factor-2 (Nrf2) Is Required for NLRP3 and AIM2 Inflammasome Activation*
    id: s2:7c15e66f90d135b936f3f7f3c1558fa1bf75debf
    date: 2014-05-05
    venue: Journal of Biological Chemistry
    authors: Changcheng Zhao, Devyn D. Gillette, Xinghui Li, Zhi-Bin Zhang, Haitao Wen
    abstract: Background: A subgroup of the NLR (nucleotide binding domain, leucine-rich repeat-containing) proteins and a non-NLR protein AIM2 are key mediators of the inflammasome. Results: Cells lacking Nrf2 are defective in the activation of the NLRP3 and AIM2 inflammasome but not the NLRC4 inflammasome. Conclusion: Nrf2 is an essential mediator of NLRP3 and AIM2 inflammasome activation. Significance: Nrf2 plays a proinflammatory role by enhancing inflammasome activation. Despite the number of extensive studies on the immune function and signaling of inflammasomes in various diseases, the activating mechanism of inflammasome, especially the NLRP3 inflammasome, is not fully understood. Nuclear factor E2-related Factor-2 (Nrf2), a key transcription factor that regulates cellular redox homeostasis, has been reported to play both protective and pathogenic roles depending on the disease conditions through undefined mechanism. This study reveals an essential role of Nrf2 in inflammasome activation. LPS stimulation increased Nrf2 protein levels in a Myd88-dependent manner. When compared with wild-type controls, Nrf2-deficient (Nrf2−/−) macrophages showed decreased maturation and secretion of caspase-1 and IL-1β and reduced apoptosis-associated speck-like protein containing CARD (ASC) speck formation in response to various NLRP3 and AIM2 inflammasome stimuli. In contrast, NLRC4 inflammasome activation was not controlled by Nrf2. Biochemical analysis revealed that Nrf2 appeared in the ASC-enriched cytosolic compartment after NLRP3 inflammasome activation. Furthermore, mitochondrial reactive oxygen species-induced NLRP3 activation also required Nrf2. Nrf2−/− mice showed a dramatic decrease in immune cell recruitment and IL-1β generation in alum-induced peritonitis, which is a typical IL-1 signaling-dependent inflammation animal model. This work discovered a critical proinflammatory effect of Nrf2 by mediating inflammasome activation.
```
</details>

<details><summary>[8] The Gcn4p Activation Domain Interacts Specifically In Vitro with RNA Polymerase II Holoenzyme, TFIID, and the Adap-Gcn5p Coactivator Complex — C. Drysdale, B. M. Jackson, R. McVeigh, E. Klebanow et al. (1998); cutoff-filter date 1998-03-01; doi:10.1128/mcb.18.3.1711</summary>

```text
[8] The Gcn4p Activation Domain Interacts Specifically In Vitro with RNA Polymerase II Holoenzyme, TFIID, and the Adap-Gcn5p Coactivator Complex
    id: s2:2db5fc47fe41257fe0cd5c56c49d060ac1e4f72c
    date: 1998-03-01
    venue: Molecular and Cellular Biology
    authors: C. Drysdale, B. M. Jackson, R. McVeigh, E. Klebanow, Y. Bai, T. Kokubo, M. Swanson, Y. Nakatani
    abstract: [no abstract available]
```
</details>

<details><summary>[9] RIP1 is an essential mediator of Toll-like receptor 3–induced NF-κB activation — E. Meylan, K. Burns, K. Hofmann, V. Blancheteau et al. (2004); cutoff-filter date 2004-05-01; doi:10.1038/ni1061</summary>

```text
[9] RIP1 is an essential mediator of Toll-like receptor 3–induced NF-κB activation
    id: s2:8730f1ac730fceaf8ed7a2cb9e364e371b5bf7f8
    date: 2004-05-01
    venue: Nature Immunology
    authors: E. Meylan, K. Burns, K. Hofmann, V. Blancheteau, F. Martinon, M. Kelliher, J. Tschopp
    abstract: [no abstract available]
    note: merged with 1 other version(s) of the same work
```
</details>

<details><summary>[10] Inhibiting Fungal Multidrug Resistance by Disrupting an Activator-Mediator Interaction — Joy L. Nishikawa, A. Boeszoermenyi, L. Vale-Silva, R. Torelli et al. (2016); cutoff-filter date 2016-02-17; doi:10.1038/nature16963</summary>

```text
[10] Inhibiting Fungal Multidrug Resistance by Disrupting an Activator-Mediator Interaction
    id: s2:1c00e7c3a6c85b9dcf38ff8159948ca215ca368f
    date: 2016-02-17
    venue: Nature
    authors: Joy L. Nishikawa, A. Boeszoermenyi, L. Vale-Silva, R. Torelli, B. Posteraro, Y. Sohn, Fei Ji, V. Gelev
    abstract: Eukaryotic transcription activators stimulate the expression of specific sets of target genes through recruitment of co-activators such as the RNA polymerase II-interacting Mediator complex. Aberrant function of transcription activators has been implicated in several diseases. However, therapeutic targeting efforts have been hampered by a lack of detailed molecular knowledge of the mechanisms of gene activation by disease-associated transcription activators. We previously identified an activator-targeted three-helix bundle KIX domain in the human MED15 Mediator subunit that is structurally conserved in Gal11/Med15 Mediator subunits in fungi. The Gal11/Med15 KIX domain engages pleiotropic drug resistance transcription factor (Pdr1) orthologues, which are key regulators of the multidrug resistance pathway in Saccharomyces cerevisiae and in the clinically important human pathogen Candida glabrata. The prevalence of C. glabrata is rising, partly owing to its low intrinsic susceptibility to azoles, the most widely used antifungal agent. Drug-resistant clinical isolates of C. glabrata most commonly contain point mutations in Pdr1 that render it constitutively active, suggesting that this transcriptional activation pathway represents a linchpin in C. glabrata multidrug resistance. Here we perform sequential biochemical and in vivo high-throughput screens to identify small-molecule inhibitors of the interaction of the C. glabrata Pdr1 activation domain with the C. glabrata Gal11A KIX domain. The lead compound (iKIX1) inhibits Pdr1-dependent gene activation and re-sensitizes drug-resistant C. glabrata to azole antifungals in vitro and in animal models for disseminated and urinary tract C. glabrata infection. Determining the NMR structure of the C. glabrata Gal11A KIX domain provides a detailed understanding of the molecular mechanism of Pdr1 gene activation and multidrug resistance inhibition by iKIX1. We have demonstrated the feasibility of small-molecule targeting of a tra [...]
```
</details>

<details><summary>Post-hoc automated audit — NON-AUTHORITATIVE; uses hidden benchmark annotations</summary>

- primary auditor: `silence_as_null_error`; statuses {'H1': 'positive_or_present', 'H2': 'indeterminate'}; discriminative=False
- primary reasoning: H1 directly predicts that soluble multivalent interactions between activation domains and Mediator subunits can drive transcriptional activation without phase-separated condensates. H2 is silent on whether activation can occur in the absence of condensates, as it only specifies activation via co-condensation.
- derived opposition call: `manufactured_from_silence`
- evidence attribution: `informative_evidence_found` — The retrieved literature includes a paper (record [3]) that directly addresses the core of the proposition: it describes multivalent, soluble interactions between transcription factor activation domains and Mediator subunits driving transcriptional activation, and the assessor correctly recognized this as relevant evidence. While the papers do not explicitly rule out phase separation, they provide mechanistic support for activation via soluble interactions, which is the main claim. The process worked as intended.
- disagreement flags: {'second_rater_vs_primary_discriminative': None, 'second_rater_vs_primary_status': None, 'retest_vs_primary_category': None, 'any': False}
</details>

**Human review** — `generic_component_fact` · reviewer: Research Director · source: D045 · status: `first_pass_model_based_review` · genuinely discriminative: False · silence-as-null error: False · other fields not recorded

---

## #6 · `GP1-glnbp_induced_fit_vs_conformational_selection-X3`

**GP1-glnbp_induced_fit_vs_conformational_selection-X3** — case `glnbp_induced_fit_vs_conformational_selection`, node `X3`

> Substrate-binding proteins in the periplasmic binding protein family can bind their ligand in an open, binding-competent state.

- generated from **H2** (Candidate A); abstraction: `class`
- generator's stated reason: The claim about GlnBP, a member of this family, increases the likelihood that other periplasmic binding proteins also bind ligands in an open conformation.
- influence: **0.636** (rank 3 in case, 6 overall; cumulative 26%) — favours **H2**
- log-likelihood contribution: H2 +1.164, H1 +0.528
- removing it alone: evidence withheld → case log-odds +1.205 (ranking unchanged); node deleted → +1.205 (ranking unchanged)

**Hypotheses (as shown to the verifier)**

- **H1** (Candidate B): Apo-GlnBP samples a pre-existing binding-competent closed or semi-closed conformation; glutamine preferentially binds/captures that pre-existing conformation.
- **H2** (Candidate A): Glutamine binds to open/binding-competent GlnBP before the major protein conformational rearrangement, after which GlnBP closes around the ligand.

**Verifier cross-hypothesis judgments** — P(X|H) combines these by noisy-OR

| hypothesis | origin? | direct edge | route via parent | P(X\|H) |
| --- | --- | --- | --- | --- |
| H2 | yes | `strongly_implied` | — | 0.950 |
| H1 | no | `unlikely` | — | 0.300 |

- edge rationale, **H2** → node: Candidate A explicitly states that the ligand binds to the protein in an open, binding-competent state, which directly supports the proposition.
- edge rationale, **H1** → node: Candidate B suggests that ligand binding occurs to a closed or semi-closed conformation, making binding in an open state less likely.

**Verifier evidence** — label used in score: `support` (log-LR +1.2)

- queries: `periplasmic binding protein open conformation`; `substrate-binding protein ligand binding state`
- assessor rationale: Record [10] directly states that the periplasmic C4-dicarboxylate binding protein (DctP) has an open-liganded conformation, which is consistent with substrate-binding proteins in the periplasmic binding protein family binding their ligand in an open, binding-competent state. This is a direct report of the proposition as written, rather than an inference. No other records directly state ligand binding in the open conformation.
- supporting spans cited by the assessor:
  - "In the absence of ligand, the protein is in equilibrium between an essentially nonbinding form, BP1, and the binding form, BP2. Ligands bind to the BP2 form, shifting the equilibrium toward the BP2-L conformation, and also inducing a further isomerization of the protein, to the BP3-L form. The kinetic properties of the four different conformational states of the DctP protein identified in this study would be consistent with their identification as the closed-conformation, the open-conformation, an open-liganded conformation, and a closed-liganded conformation."
- 10 papers shown; key papers: `s2:eed159a6397468593a7f59bff05e8ddfca83e770`
- _The evidence assessor returns ONE label for the node from all papers shown; the method has no per-paper contribution. Key papers and spans are those the assessor cited._

<details><summary>[1] Open Conformation of the Escherichia coli Periplasmic Murein Tripeptide Binding Protein, MppA, at High Resolution — F. Bhatt, V. Patel, C. Jeffery (2018); cutoff-filter date 2018-05-19; doi:10.3390/biology7020030</summary>

```text
[1] Open Conformation of the Escherichia coli Periplasmic Murein Tripeptide Binding Protein, MppA, at High Resolution
    id: s2:5a47e8bc5487d7f664fdf14bd73afa31c6dd440f
    date: 2018-05-19
    venue: Biology
    authors: F. Bhatt, V. Patel, C. Jeffery
    abstract: Periplasmic ligand-binding proteins (PBPs) bind ligands with a high affinity and specificity. They undergo a large conformational change upon ligand binding, and they have a robust protein fold. These physical features have made them ideal candidates for use in protein engineering projects to develop novel biosensors and signaling molecules. The Escherichia coli MppA (murein peptide permease A) PBP binds the murein tripeptide, l-alanyl-γ-d-glutamyl-meso-diaminopimelate, (l-Ala-γ-d-Glu-meso-Dap), which contains both a D-amino acid and a gamma linkage between two of the amino acids. We have solved a high-resolution X-ray crystal structure of E. coli MppA at 1.5 Å resolution in the unliganded, open conformation. Now, structures are available for this member of the PBP protein family in both the liganded/closed form and the unliganded/open form.
```
</details>

<details><summary>[2] The Open Conformation Satisfies Multiple NMR Experiments on Apo Glutamine-Binding Protein: Overcoming Pitfalls in the Study of Interdomain Dynamics — H. Kooshapur, Junhe Ma, N. Tjandra, G. Bermejo (2019); cutoff-filter date 2019-09-13; doi:10.1002/anie.201911015</summary>

```text
[2] The Open Conformation Satisfies Multiple NMR Experiments on Apo Glutamine-Binding Protein: Overcoming Pitfalls in the Study of Interdomain Dynamics
    id: s2:eb71f0a80f7f2961fcf1898dd7951b1b511f449b
    date: 2019-09-13
    venue: Angewandte Chemie
    authors: H. Kooshapur, Junhe Ma, N. Tjandra, G. Bermejo
    abstract: Glutamine-binding protein (GlnBP) from Escherichia coli is a prototypical periplasmic binding protein that has been crystallized in an apo, “open” conformation, with its two domains far apart, and a holo, “closed” form, with proximal domains that engulf the cognate L-Gln ligand. A fundamental question about such large-scale conformational transitions—whether the closed state exists in the absence of ligand—is a matter of controversy in the case of GlnBP. Previously, NMR observations have indicated no evidence of the closed form, whereas experimentally validated computations have suggested a remarkable ~40% population. Here, a paramagnetic NMR strategy designed to specifically detect the putative apo-closed species shows that a major population of the latter is highly improbable. Further, NMR residual dipolar couplings collected under three anisotropic conditions fail to reveal differential domain alignment (which would otherwise signal interdomain dynamics) and establish that the average solution conformation is satisfied by the apo-open crystal structure. Our results indicate that the computational prediction of large-scale interdomain motions is far from trivial and may lead to grossly erroneous conclusions without proper experimental validation.
```
</details>

<details><summary>[3] A structural model for (GlcNAc)2 translocation via a periplasmic chitooligosaccharide-binding protein from marine Vibrio bacteria — Y. Kitaoku, T. Fukamizo, Sawitree Kumsaoad, P. Ubonbal et al. (2021); cutoff-filter date 2021-08-13; doi:10.1016/j.jbc.2021.101071</summary>

```text
[3] A structural model for (GlcNAc)2 translocation via a periplasmic chitooligosaccharide-binding protein from marine Vibrio bacteria
    id: s2:217bab073df03bde42f55f8caa3b033a837ad888
    date: 2021-08-01
    venue: Journal of Biological Chemistry
    authors: Y. Kitaoku, T. Fukamizo, Sawitree Kumsaoad, P. Ubonbal, R. Robinson, W. Suginta
    abstract: VhCBP is a periplasmic chitooligosaccharide-binding protein mainly responsible for translocation of the chitooligosaccharide (GlcNAc)2 across the double membranes of marine bacteria. However, structural and thermodynamic understanding of the sugar-binding/-release processes of VhCBP is relatively less. VhCBP displayed the greatest affinity toward (GlcNAc)2, with lower affinity for longer-chain chitooligosaccharides [(GlcNAc)3–4]. (GlcNAc)4 partially occupied the closed sugar-binding groove, with two reducing-end GlcNAc units extending beyond the sugar-binding groove and barely characterized by weak electron density. Mutation of three conserved residues (Trp363, Asp365, and Trp513) to Ala resulted in drastic decreases in the binding affinity toward the preferred substrate (GlcNAc)2, indicating their significant contributions to sugar binding. The structure of the W513A–(GlcNAc)2 complex in a ‘half-open’ conformation unveiled the intermediary step of the (GlcNAc)2 translocation from the soluble CBP in the periplasm to the inner membrane–transporting components. Isothermal calorimetry data suggested that VhCBP adopts the high-affinity conformation to bind (GlcNAc)2, while its low-affinity conformation facilitated sugar release. Thus, chitooligosaccharide translocation, conferred by periplasmic VhCBP, is a crucial step in the chitin catabolic pathway, allowing Vibrio bacteria to thrive in oceans where chitin is their major source of nutrients.
```
</details>

<details><summary>[4] Crystal structure of a LacY–nanobody complex in a periplasmic-open conformation — Xin Jiang, I. Smirnova, V. Kasho, Jianping Wu et al. (2016); cutoff-filter date 2016-10-19; doi:10.1073/pnas.1615414113</summary>

```text
[4] Crystal structure of a LacY–nanobody complex in a periplasmic-open conformation
    id: s2:510d3aa9493c0013229bafe212f9b20b663f07f6
    date: 2016-10-19
    venue: Proceedings of the National Academy of Sciences of the United States of America
    authors: Xin Jiang, I. Smirnova, V. Kasho, Jianping Wu, K. Hirata, M. Ke, E. Pardon, J. Steyaert
    abstract: [no abstract available]
```
</details>

<details><summary>[5] Ligand-induced structural changes analysis of ribose-binding protein as studied by molecular dynamics simulations — Hai-Yan Li, Zanxia Cao, Guodong Hu, Li-Ling Zhao et al. (2021); cutoff-filter date 2021-03-02; doi:10.3233/thc-218011</summary>

```text
[5] Ligand-induced structural changes analysis of ribose-binding protein as studied by molecular dynamics simulations
    id: s2:b407302d7c1be527f2abbdc5b5075a4a215f7ec3
    date: 2021-01-01
    venue: Technology and Health Care
    authors: Hai-Yan Li, Zanxia Cao, Guodong Hu, Li-Ling Zhao, Chun-Ling Wang, Jihua Wang
    abstract: BACKGROUND: The ribose-binding protein (RBP) from Escherichia coli is one of the representative structures of periplasmic binding proteins. Binding of ribose at the cleft between two domains causes a conformational change corresponding to a closure of two domains around the ligand. The RBP has been crystallized in the open and closed conformations. OBJECTIVE: With the complex trajectory as a control, our goal was to study the conformation changes induced by the detachment of the ligand, and the results have been revealed from two computational tools, MD simulations and elastic network models. METHODS: Molecular dynamics (MD) simulations were performed to study the conformation changes of RBP starting from the open-apo, closed-holo and closed-apo conformations. RESULTS: The evolution of the domain opening angle θ clearly indicates large structural changes. The simulations indicate that the closed states in the absence of ribose are inclined to transition to the open states and that ribose-free RBP exists in a wide range of conformations. The first three dominant principal motions derived from the closed-apo trajectories, consisting of rotating, bending and twisting motions, account for the major rearrangement of the domains from the closed to the open conformation. CONCLUSIONS: The motions showed a strong one-to-one correspondence with the slowest modes from our previous study of RBP with the anisotropic network model (ANM). The results obtained for RBP contribute to the generalization of robustness for protein domain motion studies using either the ANM or PCA for trajectories obtained from MD.
```
</details>

<details><summary>[6] Crystal structure of a putative oligopeptide-binding periplasmic protein from a hyperthermophile — H. Yoon, Hee Jung Kim, B. Mikami, Y. Yu et al. (2016); cutoff-filter date 2016-07-05; doi:10.1007/s00792-016-0861-7</summary>

```text
[6] Crystal structure of a putative oligopeptide-binding periplasmic protein from a hyperthermophile
    id: s2:e9c338de66a7a7217823f67e127c98641e8d2e32
    date: 2016-07-05
    venue: Extremophiles
    authors: H. Yoon, Hee Jung Kim, B. Mikami, Y. Yu, H. Lee
    abstract: [no abstract available]
```
</details>

<details><summary>[7] Accessing a Hidden Conformation of the Maltose Binding Protein Using Accelerated Molecular Dynamics — Denis Bucher, Barry J. Grant, P. Markwick, J. McCammon (2011); cutoff-filter date 2011-04-21; doi:10.1371/journal.pcbi.1002034</summary>

```text
[7] Accessing a Hidden Conformation of the Maltose Binding Protein Using Accelerated Molecular Dynamics
    id: s2:4bd83fb543e1b02d0746b468bd934d5d23db3848
    date: 2011-04-01
    venue: PLoS Comput. Biol.
    authors: Denis Bucher, Barry J. Grant, P. Markwick, J. McCammon
    abstract: Periplasmic binding proteins (PBPs) are a large family of molecular transporters that play a key role in nutrient uptake and chemotaxis in Gram-negative bacteria. All PBPs have characteristic two-domain architecture with a central interdomain ligand-binding cleft. Upon binding to their respective ligands, PBPs undergo a large conformational change that effectively closes the binding cleft. This conformational change is traditionally viewed as a ligand induced-fit process; however, the intrinsic dynamics of the protein may also be crucial for ligand recognition. Recent NMR paramagnetic relaxation enhancement (PRE) experiments have shown that the maltose binding protein (MBP) - a prototypical member of the PBP superfamily - exists in a rapidly exchanging (ns to µs regime) mixture comprising an open state (approx 95%), and a minor partially closed state (approx 5%). Here we describe accelerated MD simulations that provide a detailed picture of the transition between the open and partially closed states, and confirm the existence of a dynamical equilibrium between these two states in apo MBP. We find that a flexible part of the protein called the balancing interface motif (residues 175–184) is displaced during the transformation. Continuum electrostatic calculations indicate that the repacking of non-polar residues near the hinge region plays an important role in driving the conformational change. Oscillations between open and partially closed states create variations in the shape and size of the binding site. The study provides a detailed description of the conformational space available to ligand-free MBP, and has implications for understanding ligand recognition and allostery in related proteins.
```
</details>

<details><summary>[8] Opening and closing motions in the periplasmic vitamin B12 binding protein BtuF. — Christian Kandt, Zhi-Tao Xu, D. Tieleman (2006); cutoff-filter date 2006-10-13; doi:10.1021/bi061280j</summary>

```text
[8] Opening and closing motions in the periplasmic vitamin B12 binding protein BtuF.
    id: s2:079537c6be5248ab15869c8af132fead69a0473a
    date: 2006-10-13
    venue: Biochemistry
    authors: Christian Kandt, Zhi-Tao Xu, D. Tieleman
    abstract: [no abstract available]
```
</details>

<details><summary>[9] Determination of the Solution Bound Conformation of an Amino-acid Binding Protein by NMR Paramagnetic Relaxation Enhancement: Use of a Single Flexible Paramagnetic Probe with Improved Estimation of Its Sampling Space — G. Bermejo, M. Strub, C. Ho, N. Tjandra (2009); cutoff-filter date 2009-07-15; doi:10.1021/ja902436g</summary>

```text
[9] Determination of the Solution Bound Conformation of an Amino-acid Binding Protein by NMR Paramagnetic Relaxation Enhancement: Use of a Single Flexible Paramagnetic Probe with Improved Estimation of Its Sampling Space
    id: s2:1cbc73facc1f2878f174180c43b8dddfc23c2c61
    date: 2009-07-15
    venue: Journal of the American Chemical Society
    authors: G. Bermejo, M. Strub, C. Ho, N. Tjandra
    abstract: We demonstrate the feasibility of elucidating the bound (“closed”) conformation of a periplasmic binding protein, the glutamine-binding protein (GlnBP), in solution, using paramagnetic relaxation enhancements (PREs) arising from a single paramagnetic group. GlnBP consists of two globular domains connected by a hinge. Using the ligand-free (“open”) conformation as a starting point, conjoined rigid-body/torsion-angle simulated annealing calculations were performed using backbone 1HN-PREs as a major source of distance information. Paramagnetic probe flexibility was accounted for via a multiple-conformer representation. A conventional approach where the entire PRE data set is enforced at once during simulated annealing yielded poor results due to inappropriate conformational sampling of the probe. On the other hand, significant improvements in coordinate accuracy were obtained by estimating the probe sampling space prior to structure calculation. Such sampling is achieved by refining the ensemble of probe conformers with intra-domain PREs only, keeping the protein backbone fixed in the open form. Subsequently, while constraining the probe to the previously found conformations, the domains are allowed to move relative to each other under the influence of the non-intra-domain PREs, giving the hinge region torsional degrees of freedom. Thus, by partitioning the protocol into a “probe sampling” and a “backbone sampling” stage, structures significantly closer to the X-ray structure of ligand-bound GlnBP were obtained.
```
</details>

<details><summary>[10] **KEY** The mechanism of ligand binding to the periplasmic C4-dicarboxylate binding protein (DctP) from Rhodobacter capsulatus. — A. Walmsley, Jonathan G. Shaw, David J. Kelly (1992); cutoff-filter date 1992-04-30; doi:10.1016/s0021-9258(18)42408-8</summary>

```text
[10] The mechanism of ligand binding to the periplasmic C4-dicarboxylate binding protein (DctP) from Rhodobacter capsulatus.
    id: s2:eed159a6397468593a7f59bff05e8ddfca83e770
    date: 1992-04-25
    venue: Journal of Biological Chemistry
    authors: A. Walmsley, Jonathan G. Shaw, David J. Kelly
    abstract: The kinetics of ligand binding to the periplasmic C4-dicarboxylate binding protein (DctP) from Rhodobacter capsulatus were investigated by exploiting the changes in the intrinsic fluorescence of the protein upon binding ligands. Steady state measurements have shown that L-malate, succinate, and fumarate are all bound with sub-micromolar Kd values, whereas D-malate is bound 2 orders of magnitude more weakly. Stopped-flow studies have revealed that the binding process involves at least three steps. In the absence of ligand, the protein is in equilibrium between an essentially nonbinding form, BP1, and the binding form, BP2. Ligands bind to the BP2 form, shifting the equilibrium toward the BP2-L conformation, and also inducing a further isomerization of the protein, to the BP3-L form. The kinetic properties of the four different conformational states of the DctP protein identified in this study would be consistent with their identification as the closed-conformation, the open-conformation, an open-liganded conformation, and a closed-liganded conformation. The latter three states have been identified by x-ray crystallographic studies of binding proteins, but no kinetic or structural data have been presented previously to support the possibility of a closed but unliganded conformation.
```
</details>

<details><summary>Post-hoc automated audit — NON-AUTHORITATIVE; uses hidden benchmark annotations</summary>

- primary auditor: `silence_as_null_error`; statuses {'H2': 'positive_or_present', 'H1': 'indeterminate'}; discriminative=False
- primary reasoning: H2 (induced fit) implies that ligand binding can occur to an open, binding-competent state, so it predicts this proposition. H1 (conformational selection) is silent about whether other periplasmic binding proteins bind ligands in an open state; it only requires that the closed/semi-closed state is binding-competent and populated, so it makes no commitment about the open state.
- derived opposition call: `manufactured_from_silence`
- evidence attribution: `informative_evidence_found` — The retrieval system surfaced a paper (record [10]) that directly addresses the proposition, reporting that a periplasmic binding protein binds its ligand in an open, binding-competent state. The queries were appropriate and the assessor correctly identified relevant evidence. The process worked as intended.
- disagreement flags: {'second_rater_vs_primary_discriminative': None, 'second_rater_vs_primary_status': None, 'retest_vs_primary_category': None, 'any': False}
</details>

**Human review** — `generic_component_fact` · reviewer: Research Director · source: D045 · status: `first_pass_model_based_review` · genuinely discriminative: False · silence-as-null error: False · other fields not recorded

---

## #7 · `GP1-glnbp_induced_fit_vs_conformational_selection-X5`

**GP1-glnbp_induced_fit_vs_conformational_selection-X5** — case `glnbp_induced_fit_vs_conformational_selection`, node `X5`

> Glutamine binding to GlnBP occurs preferentially when the protein is in a closed or semi-closed conformation.

- generated from **H1** (Candidate B); abstraction: `mechanistic`
- generator's stated reason: The claim asserts that glutamine captures a pre-existing closed or semi-closed conformation, so binding is mechanistically coupled to the presence of that conformation.
- influence: **0.636** (rank 4 in case, 7 overall; cumulative 29%) — favours **H1**
- log-likelihood contribution: H2 +0.528, H1 +1.164
- removing it alone: evidence withheld → case log-odds +2.477 (ranking unchanged); node deleted → +2.410 (ranking unchanged)

**Hypotheses (as shown to the verifier)**

- **H1** (Candidate B): Apo-GlnBP samples a pre-existing binding-competent closed or semi-closed conformation; glutamine preferentially binds/captures that pre-existing conformation.
- **H2** (Candidate A): Glutamine binds to open/binding-competent GlnBP before the major protein conformational rearrangement, after which GlnBP closes around the ligand.

**Verifier cross-hypothesis judgments** — P(X|H) combines these by noisy-OR

| hypothesis | origin? | direct edge | route via parent | P(X\|H) |
| --- | --- | --- | --- | --- |
| H2 | no | `unlikely` | — | 0.300 |
| H1 | yes | `strongly_implied` | — | 0.950 |

- edge rationale, **H2** → node: Candidate A states that glutamine binds to the open conformation before the protein closes, which suggests binding does not preferentially occur in the closed or semi-closed state.
- edge rationale, **H1** → node: Candidate B explicitly claims that glutamine preferentially binds to a pre-existing closed or semi-closed conformation, making the proposition nearly certain if B is true.

**Verifier evidence** — label used in score: `support` (log-LR +1.2)

- queries: `GlnBP glutamine binding conformation`; `GlnBP closed state ligand affinity`
- assessor rationale: Record [6] directly states that glutamine binding to QBP induces a conformational change from open to closed, implying preferential binding in the closed state. Record [8] reports that domain closure propensity determines ligand binding affinity, and that ligand binding triggers conformational change, supporting the idea that binding occurs preferentially in closed or semi-closed conformations. Both records directly address the relationship between glutamine binding and protein conformation.
- supporting spans cited by the assessor:
  - "The QBP was immobilized on the surface of gold films by chemical cross-linking and exhibited a binding affinity for L-glutamine. The conformation of QBP can be changed from the "open" to the "closed", which led to a red-shift of the SPR peak when QBP bounded to L-glutamine."
  - "We propose that the freedome of closure movement is also vital for ligand binding. In order to approve this hypothesis, we generate a series of mutants with different linker length that has different magnitude of domain closure. Mutants show different ligand binding affinity, which indicates that the propensity of domain closure determines the ligand binding affinity. Ligand binding triggers gradual ensemble conformational change."
- 10 papers shown; key papers: `s2:6766c35f686e47e89d88b269e20bb2827f091f31`, `s2:9abdfb5efd6c7a7ec50fb901f5b87db3380cdc1c`
- _The evidence assessor returns ONE label for the node from all papers shown; the method has no per-paper contribution. Key papers and spans are those the assessor cited._

<details><summary>[1] The Open Conformation Satisfies Multiple NMR Experiments on Apo Glutamine-Binding Protein: Overcoming Pitfalls in the Study of Interdomain Dynamics — H. Kooshapur, Junhe Ma, N. Tjandra, G. Bermejo (2019); cutoff-filter date 2019-09-13; doi:10.1002/anie.201911015</summary>

```text
[1] The Open Conformation Satisfies Multiple NMR Experiments on Apo Glutamine-Binding Protein: Overcoming Pitfalls in the Study of Interdomain Dynamics
    id: s2:eb71f0a80f7f2961fcf1898dd7951b1b511f449b
    date: 2019-09-13
    venue: Angewandte Chemie
    authors: H. Kooshapur, Junhe Ma, N. Tjandra, G. Bermejo
    abstract: Glutamine-binding protein (GlnBP) from Escherichia coli is a prototypical periplasmic binding protein that has been crystallized in an apo, “open” conformation, with its two domains far apart, and a holo, “closed” form, with proximal domains that engulf the cognate L-Gln ligand. A fundamental question about such large-scale conformational transitions—whether the closed state exists in the absence of ligand—is a matter of controversy in the case of GlnBP. Previously, NMR observations have indicated no evidence of the closed form, whereas experimentally validated computations have suggested a remarkable ~40% population. Here, a paramagnetic NMR strategy designed to specifically detect the putative apo-closed species shows that a major population of the latter is highly improbable. Further, NMR residual dipolar couplings collected under three anisotropic conditions fail to reveal differential domain alignment (which would otherwise signal interdomain dynamics) and establish that the average solution conformation is satisfied by the apo-open crystal structure. Our results indicate that the computational prediction of large-scale interdomain motions is far from trivial and may lead to grossly erroneous conclusions without proper experimental validation.
```
</details>

<details><summary>[2] Temperature dependence of molecular interactions involved in defining stability of Glutamine Binding Protein and its complex with L-Glutamine — S. Pistolesi, N. Tjandra (2012); cutoff-filter date 2012-01-06; doi:10.1021/bi201494h</summary>

```text
[2] Temperature dependence of molecular interactions involved in defining stability of Glutamine Binding Protein and its complex with L-Glutamine
    id: s2:f1114e0bbb4513350290b5e28bdf86aa47a1c0c7
    date: 2012-01-06
    venue: Biochemistry
    authors: S. Pistolesi, N. Tjandra
    abstract: Temperature dependence of dynamic parameters derived from nuclear magnetic resonance (NMR) relaxation data are related to conformational entropy of the system under study. This provides information such as macromolecules stability and thermodynamics of ligand binding. We studied the temperature dependence of NMR order parameter of Glutamine binding protein (GlnBP), a periplasmic binding protein (PBP) highly specific to L-glutamine associated with its ABC transporter, with the goal of elucidating the dynamical differences between the respective ligand bound and free forms. We found that the protein-ligand interaction, which is stabilized at higher temperature, has a striking effect on the stability of the hydrophobic core of the large domain of GlnBP. Moreover, in contrast to what was found for less specific PBPs the decreasing backbone motion of the hinge region at increasing temperature supports the idea that the likelihood that GlnBP can adopt a ligand free closed conformation in solution diminishes at higher temperatures. Our results support the induced-fit model as mode of action for GlnBP. In addition, we found that the backbones of residues involved in a salt bridge do not necessarily become more rigid as the temperature rises as it was previously suggested [Vinther, J.M. et. al. (2011) J. Am. Chem. Soc., 271–278]. Our results show that for this to happen, these residues have to also directly interact with a region of the protein that is becoming more rigid as the temperature increases.
```
</details>

<details><summary>[3] Conformational Dynamics of apo-GlnBP Revealed by Experimental and Computational Analysis. — Yitao Feng, Lu Zhang, Shaowen Wu, Zhijun Liu et al. (2016); cutoff-filter date 2016-11-02; doi:10.1002/anie.201606613</summary>

```text
[3] Conformational Dynamics of apo-GlnBP Revealed by Experimental and Computational Analysis.
    id: s2:011d4ac715a7d80122c2f1b0a60fcf0937ea6f2a
    date: 2016-11-02
    venue: Angewandte Chemie
    authors: Yitao Feng, Lu Zhang, Shaowen Wu, Zhijun Liu, Xin Gao, Xu Zhang, Maili Liu, Jianwei Liu
    abstract: [no abstract available]
```
</details>

<details><summary>[4] Determination of the Solution Bound Conformation of an Amino-acid Binding Protein by NMR Paramagnetic Relaxation Enhancement: Use of a Single Flexible Paramagnetic Probe with Improved Estimation of Its Sampling Space — G. Bermejo, M. Strub, C. Ho, N. Tjandra (2009); cutoff-filter date 2009-07-15; doi:10.1021/ja902436g</summary>

```text
[4] Determination of the Solution Bound Conformation of an Amino-acid Binding Protein by NMR Paramagnetic Relaxation Enhancement: Use of a Single Flexible Paramagnetic Probe with Improved Estimation of Its Sampling Space
    id: s2:1cbc73facc1f2878f174180c43b8dddfc23c2c61
    date: 2009-07-15
    venue: Journal of the American Chemical Society
    authors: G. Bermejo, M. Strub, C. Ho, N. Tjandra
    abstract: We demonstrate the feasibility of elucidating the bound (“closed”) conformation of a periplasmic binding protein, the glutamine-binding protein (GlnBP), in solution, using paramagnetic relaxation enhancements (PREs) arising from a single paramagnetic group. GlnBP consists of two globular domains connected by a hinge. Using the ligand-free (“open”) conformation as a starting point, conjoined rigid-body/torsion-angle simulated annealing calculations were performed using backbone 1HN-PREs as a major source of distance information. Paramagnetic probe flexibility was accounted for via a multiple-conformer representation. A conventional approach where the entire PRE data set is enforced at once during simulated annealing yielded poor results due to inappropriate conformational sampling of the probe. On the other hand, significant improvements in coordinate accuracy were obtained by estimating the probe sampling space prior to structure calculation. Such sampling is achieved by refining the ensemble of probe conformers with intra-domain PREs only, keeping the protein backbone fixed in the open form. Subsequently, while constraining the probe to the previously found conformations, the domains are allowed to move relative to each other under the influence of the non-intra-domain PREs, giving the hinge region torsional degrees of freedom. Thus, by partitioning the protocol into a “probe sampling” and a “backbone sampling” stage, structures significantly closer to the X-ray structure of ligand-bound GlnBP were obtained.
```
</details>

<details><summary>[5] Mechanisms for ligand binding to GluR0 ion channels: crystal structures of the glutamate and serine complexes and a closed apo state. — M. Mayer, R. Olson, E. Gouaux (2001); cutoff-filter date 2001-08-31; doi:10.1006/jmbi.2001.4884</summary>

```text
[5] Mechanisms for ligand binding to GluR0 ion channels: crystal structures of the glutamate and serine complexes and a closed apo state.
    id: s2:59d1f722a6654a45edca6cba29f1cf7a75711d63
    date: 2001-08-24
    venue: Journal of Molecular Biology
    authors: M. Mayer, R. Olson, E. Gouaux
    abstract: [no abstract available]
```
</details>

<details><summary>[6] **KEY** A L-glutamine binding protein modified MNM structured optical fiber biosensor based on surface plasmon resonance sensing for detection of L-glutamine metabolism in vitro embryo culture. — Jianfeng Chen, Liyun Ding, Jue Zhao, Xing-Dong Jiang et al. (2023); cutoff-filter date 2023-07-16; doi:10.2139/ssrn.4327577</summary>

```text
[6] A L-glutamine binding protein modified MNM structured optical fiber biosensor based on surface plasmon resonance sensing for detection of L-glutamine metabolism in vitro embryo culture.
    id: s2:6766c35f686e47e89d88b269e20bb2827f091f31
    date: 2023-07-16
    venue: Biosensors & bioelectronics
    authors: Jianfeng Chen, Liyun Ding, Jue Zhao, Xing-Dong Jiang, Fei Ma, Hai-Bing Li, Yumei Zhang
    abstract: A surface plasmon resonance (SPR) optical fiber sensor with multimode-coreless-multimode (MNM) structure was developed, which modified by L-glutamine-binding protein (QBP) for detection of L-glutamine (Gln). The QBP was immobilized on the surface of gold films by chemical cross-linking and exhibited a binding affinity for L-glutamine. The conformation of QBP can be changed from the "open" to the "closed", which led to a red-shift of the SPR peak when QBP bounded to L-glutamine. There was a good linear correlation between is a dependence of the SPR peak on and the concentration of L-glutamine concentration in the range 10-100 μM, with a sensitivity of 10.797nm/log10[Gln] for L-glutamine in the in vitro embryo culture (IVC) medium environment, and the limit of detection (LOD) is 1.187 μM. This QBP-modified MNM structure optical fiber SPR sensor provides a new idea for the developmental potential assessment of embryos in the process of in vitro embryo culture.
```
</details>

<details><summary>[7] Autoantibody binding and unique enzyme-substrate intermediate conformation of human transglutaminase 3 — J. Heggelund, Saykat Das, J. Stamnaes, R. Iversen et al. (2023); cutoff-filter date 2023-10-05; doi:10.1038/s41467-023-42004-z</summary>

```text
[7] Autoantibody binding and unique enzyme-substrate intermediate conformation of human transglutaminase 3
    id: s2:82414eed3c54b6adafadd571b038d2cd1421da4d
    date: 2023-10-05
    venue: Nature Communications
    authors: J. Heggelund, Saykat Das, J. Stamnaes, R. Iversen, L. Sollid
    abstract: Transglutaminase 3 (TG3), the autoantigen of dermatitis herpetiformis (DH), is a calcium dependent enzyme that targets glutamine residues in polypeptides for either transamidation or deamidation modifications. To become catalytically active TG3 requires proteolytic cleavage between the core domain and two C-terminal β-barrels (C1C2). Here, we report four X-ray crystal structures representing inactive and active conformations of human TG3 in complex with a TG3-specific Fab fragment of a DH patient derived antibody. We demonstrate that cleaved TG3, upon binding of a substrate-mimicking inhibitor, undergoes a large conformational change as a β-sheet in the catalytic core domain moves and C1C2 detaches. The unique enzyme-substrate conformation of TG3 without C1C2 is recognized by DH autoantibodies. The findings support a model where B-cell receptors of TG3-specific B cells bind and internalize TG3-gluten enzyme-substrate complexes thereby facilitating gluten-antigen presentation, T-cell help and autoantibody production.
```
</details>

<details><summary>[8] **KEY** Reversible domain closure modulates GlnBP ligand binding affinity — Qun Chen, Fang Li, X. Zuo, J. Chen et al. (2022); cutoff-filter date 2022-04-21; doi:10.1371/journal.pone.0263102</summary>

```text
[8] Reversible domain closure modulates GlnBP ligand binding affinity
    id: s2:9abdfb5efd6c7a7ec50fb901f5b87db3380cdc1c
    date: 2022-04-21
    venue: PLoS ONE
    authors: Qun Chen, Fang Li, X. Zuo, J. Chen, Peiwu Qin, Chu-Hui Wang, Jin Xu, Dan Yang
    abstract: Glutamine binding protein (GlnBP) is an Escherichia Coli periplasmic binding protein, which binds and carries glutamine to the inner membrane ATP-binding cassette (ABC) transporter. GlnBP binds the ligand with affinity around 0.1μM measured by isothermal titration calorimetry (ITC) and ligand binding stabilizes protein structure shown by its increase in thermodynamic stability. However, the molecular determinant of GlnBP ligand binding is not known. Electrostatic and hydrophobic interaction between GlnBP and glutamine are critical factors. We propose that the freedome of closure movement is also vital for ligand binding. In order to approve this hypothesis, we generate a series of mutants with different linker length that has different magnitude of domain closure. Mutants show different ligand binding affinity, which indicates that the propensity of domain closure determines the ligand binding affinity. Ligand binding triggers gradual ensemble conformational change. Structural changes upon ligand binding are monitored by combination of small angle x-ray scattering (SAXS) and NMR spectroscopy. Detailed structure characterization of GlnBP contributes to a better understanding of ligand binding and provides the structural basis for biosensor design.
```
</details>

<details><summary>[9] Ligand-bound glutamine binding protein assumes multiple metastable binding sites with different binding affinities — Lu Zhang, Shaowen Wu, Yitao Feng, Dan Wang et al. (2020); cutoff-filter date 2020-08-03; doi:10.1038/s42003-020-01149-z</summary>

```text
[9] Ligand-bound glutamine binding protein assumes multiple metastable binding sites with different binding affinities
    id: s2:a669bf843aba225e0dd842ff1272c07a33e56434
    date: 2020-08-03
    venue: Communications Biology
    authors: Lu Zhang, Shaowen Wu, Yitao Feng, Dan Wang, Xilin Jia, Zhijun Liu, Jianwei Liu, Wen-Ning Wang
    abstract: Protein dynamics plays key roles in ligand binding. However, the microscopic description of conformational dynamics-coupled ligand binding remains a challenge. In this study, we integrate molecular dynamics simulations, Markov state model (MSM) analysis and experimental methods to characterize the conformational dynamics of ligand-bound glutamine binding protein (GlnBP). We show that ligand-bound GlnBP has high conformational flexibility and additional metastable binding sites, presenting a more complex energy landscape than the scenario in the absence of ligand. The diverse conformations of GlnBP demonstrate different binding affinities and entail complex transition kinetics, implicating a concerted ligand binding mechanism. Single molecule fluorescence resonance energy transfer measurements and mutagenesis experiments are performed to validate our MSM-derived structure ensemble as well as the binding mechanism. Collectively, our study provides deeper insights into the protein dynamics-coupled ligand binding, revealing an intricate regulatory network underlying the apparent binding affinity. Zhang, Wu, Feng et al. show that ligand-bound glutamine binding protein assumes multiple metastable binding sites, presenting a more dynamic energy landscape than its ligand-free form. This study provides insights into the ligand-binding mechanisms coupled with protein dynamics that underly the apparent binding affinity.
```
</details>

<details><summary>[10] Continuous electrochemical monitoring of L-glutamine using redox-probe-modified L-glutamine-binding protein based on intermittent pulse amperometry — Shouhei Takamatsu, Jinhee Lee, R. Asano, W. Tsugawa et al. (2021); cutoff-filter date 2021-11-01; doi:10.1016/j.snb.2021.130554</summary>

```text
[10] Continuous electrochemical monitoring of L-glutamine using redox-probe-modified L-glutamine-binding protein based on intermittent pulse amperometry
    id: s2:03cc71a412a845e4ac90fd10028ac55062264f36
    date: 2021-11-01
    venue: Sensors and Actuators B-chemical
    authors: Shouhei Takamatsu, Jinhee Lee, R. Asano, W. Tsugawa, K. Ikebukuro, K. Sode
    abstract: Abstract The development of a continuous electrochemical monitoring system using a periplasmic binding protein (PBP), which changes its conformational dynamics upon ligand binding, is promising for in situ, real-time, continuous measurement technologies for use in effective biological production processes. This study focuses on a continuous L -glutamine biosensor based on　Escherichia coli-derived L -glutamine-binding protein (QBP), a PBP that can speficically bind to L -glutamine. In this sensor, QBP was modified with a redox probe, amine-reactive phenazine ethosulfate (PES), and the conformational change in QBP through the recognition of L -glutamine was monitored electrochemically by intermittent pulse amperometry (IPA) based on the change in the access of QBP-modified PES to the electrode. This sensor exhibited a change in the current against logarithmic L -glutamine concentrations between 0.2–50 μM. Continuous monitoring of L -glutamine, based on IPA measurements, revealed that continuous changes in L -glutamine concentration were observed for both increasing and decreasing concentrations. During continuous monitoring, L -glutamine concentration was monitored between 50 and 500 μM, with a limit of detection of 50 μM. This result is expected to address the future development of an electrochemical biosensor for in situ, real-time, continuous monitoring of various metabolites based on PBPs.
```
</details>

<details><summary>Post-hoc automated audit — NON-AUTHORITATIVE; uses hidden benchmark annotations</summary>

- primary auditor: `silence_as_null_error`; statuses {'H1': 'positive_or_present', 'H2': 'indeterminate'}; discriminative=False
- primary reasoning: H1 (conformational selection) predicts that glutamine binds preferentially to a pre-existing closed or semi-closed conformation, so the proposition is positive_or_present. H2 (induced fit) does not require or predict preferential binding to the closed/semi-closed state; it is silent on this, so indeterminate.
- derived opposition call: `manufactured_from_silence`
- evidence attribution: `informative_evidence_found` — The retrieved literature includes papers that directly address the relationship between glutamine binding and GlnBP conformation, specifically noting that binding induces or is associated with a closed or semi-closed state. The assessor correctly identified and used this evidence to support the proposition. The process worked as intended.
- disagreement flags: {'second_rater_vs_primary_discriminative': None, 'second_rater_vs_primary_status': None, 'retest_vs_primary_category': None, 'any': False}
</details>

**Human review** — `genuine_discriminator` · reviewer: Research Director · source: D045 · status: `first_pass_model_based_review` · genuinely discriminative: True · silence-as-null error: False · other fields not recorded

---

## #8 · `GP1-forest_fragmentation_resilience-X1`

**GP1-forest_fragmentation_resilience-X1** — case `forest_fragmentation_resilience`, node `X1`

> In fragmented forests with newly formed edges, aboveground biomass increases in edge zones compared to interior zones when climatic stress is low.

- generated from **H2** (Candidate A); abstraction: `specific`
- influence: **0.611** (rank 1 in case, 8 overall; cumulative 33%) — favours **H1**
- log-likelihood contribution: H2 -1.177, H1 -0.566
- removing it alone: evidence withheld → case log-odds -1.021 (ranking unchanged); node deleted → -0.979 (ranking unchanged)

**Hypotheses (as shown to the verifier)**

- **H1** (Candidate B): Fragmentation increases exposure to heat, atmospheric dryness, wind, and drought stress, raising mortality and reducing ecosystem resilience, especially where water/heat stress dominates.
- **H2** (Candidate A): Edge formation can increase light availability and relax limiting-resource constraints, increasing growth, biomass, recovery capacity, and potentially resilience where climatic stress penalties are small enough.

**Verifier cross-hypothesis judgments** — P(X|H) combines these by noisy-OR

| hypothesis | origin? | direct edge | route via parent | P(X\|H) |
| --- | --- | --- | --- | --- |
| H2 | yes | `implied` | — | 0.800 |
| H1 | no | `neutral` | — | 0.500 |

- edge rationale, **H2** → node: Candidate A states that edge formation can increase growth and biomass where climatic stress is low, which clearly supports the proposition.
- edge rationale, **H1** → node: Candidate B focuses on increased stress and mortality at edges under high climatic stress, but does not address what happens when climatic stress is low.

**Verifier evidence** — label used in score: `strong_contradiction` (log-LR -2.0)

- queries: `forest edge aboveground biomass`; `forest interior aboveground biomass`
- assessor rationale: Multiple independent studies directly compare aboveground biomass in edge and interior zones of fragmented forests. They consistently report that aboveground biomass is significantly lower at the edges than in the interior, contradicting the proposition. No record states or measures an increase in edge zone biomass under low climatic stress; instead, the evidence points to a decrease.
- supporting spans cited by the assessor:
  - "AGB was significantly higher in plots in the forest interior than in those at the edge of forests."
  - "The AGB in the fragments’ edges were significantly lower than in the fragments’ cores."
  - "the lower height of some large trees has resulted in a net loss of 6.0 Mg ha−1 of aboveground biomass – representing 2.3% of the aboveground biomass of edge forests."
- 10 papers shown; key papers: `s2:0ca959ab67ae82a9e0950ed681ba48f234731177`, `s2:447646f5a65281858a0607a61c9b401865a0876e`, `s2:6e638cdba421a400b68e9980fb765c9d8c015c45`
- _The evidence assessor returns ONE label for the node from all papers shown; the method has no per-paper contribution. Key papers and spans are those the assessor cited._

<details><summary>[1] Automated Machine Learning Driven Stacked Ensemble Modeling for Forest Aboveground Biomass Prediction Using Multitemporal Sentinel-2 Data — Parth Naik, M. Dalponte, L. Bruzzone (2023); cutoff-filter date 2023-12-31; doi:10.1109/jstars.2022.3232583</summary>

```text
[1] Automated Machine Learning Driven Stacked Ensemble Modeling for Forest Aboveground Biomass Prediction Using Multitemporal Sentinel-2 Data
    id: s2:dc10dffdb0b4c1f6f17c418e93779081863be483
    date: 2023
    venue: IEEE Journal of Selected Topics in Applied Earth Observations and Remote Sensing
    authors: Parth Naik, M. Dalponte, L. Bruzzone
    abstract: Modeling and large-scale mapping of forest aboveground biomass (AGB) is a complicated, challenging, and expensive task. There are considerable variations in forest characteristics that create functional disparity for different models and needs comprehensive evaluation. Moreover, the human-bias involved in the process of modeling and evaluation affects the generalization of models at larger scales. In this article, we present an automated machine learning framework for modeling, evaluation, and stacking of multiple base models for AGB prediction. We incorporate a hyperparameter optimization procedure for automatic extraction of targeted features from multitemporal Sentinel-2 data that minimizes human-bias in the proposed modeling pipeline. We integrate the two independent frameworks for automatic feature extraction and automatic model ensembling and evaluation. The results suggest that the extracted target-oriented features have an excessive contribution of red-edge and short-wave infrared spectrum. The feature importance scale indicates a dominant role of summer-based features as compared to other seasons. The automated ensembling and evaluation framework produced a stacked ensemble of base models that outperformed individual base models in accurately predicting forest AGB. The stacked ensemble model delivered the best scores of R2cv = 0.71 and RMSE = 74.44 Mgha−1. The other base models delivered R2cv and RMSE ranging between 0.38–0.66 and 81.27–109.44 Mg ha−1, respectively. The model evaluation metrics indicated that the stacked ensemble model was more resistant to outliers and achieved a better generalization. Thus, the proposed study demonstrated an effective automated modeling pipeline for predicting AGB by minimizing human-bias and deployable over large and diverse forest areas.
```
</details>

<details><summary>[2] **KEY** Aboveground Biomass and Endogenous Hormones in Sub-Tropical Forest Fragments — Chang Liu, Wen-Zhi Du, Hong-Lin Cao, Chunyu Shen et al. (2023); cutoff-filter date 2023-03-23; doi:10.3390/f14040661</summary>

```text
[2] Aboveground Biomass and Endogenous Hormones in Sub-Tropical Forest Fragments
    id: s2:6e638cdba421a400b68e9980fb765c9d8c015c45
    date: 2023-03-23
    venue: Forests
    authors: Chang Liu, Wen-Zhi Du, Hong-Lin Cao, Chunyu Shen, Lei Ma
    abstract: Associated endogenous hormones were affected by forest fragmentation and significantly correlated with aboveground biomass storage. Forest fragmentation threatens aboveground biomass (AGB) and affects biodiversity and ecosystem functioning in multiple ways. We ask whether and how forest fragmentation influences AGB in forest fragments. We investigated differences in AGB between forest edges and interiors, and how plant community characteristics and endogenous hormones influenced AGB. In six 40 m × 40 m plots spread across three forest fragments, AGB was significantly higher in plots in the forest interior than in those at the edge of forests. The proportion of individuals with a large diameter at breast height (DBH > 40 cm) in the forest edges is higher than that in the forest interiors. Further, trees within a 15–40 cm DBH range had the highest contribution to AGB in all plots. Trees in interior plots had higher abscisic acid (ABA) and lower indole-3-acetic acid (IAA) concentrations than those in edge plots. In addition, AGB was significantly positively and negatively correlated with ABA and IAA concentrations at the community scale. In this study, we provide an account of endogenous hormones’ role as an integrator of environmental signals and, in particular, we highlight the correlation of these endogenous hormone levels with vegetation patterns. Edge effects strongly influenced AGB. In the future, more endogenous hormones and complex interactions should be better explored and understood to support consistent forest conservation and management actions.
```
</details>

<details><summary>[3] Retrieving the forest aboveground biomass by combining the red edge bands of Sentinel-2 and GF-6 — 蒋馥根，孙华，李成杰，马开森，陈松，龙江平，任蓝翔 JIANG Fugen (2021); cutoff-filter date 2021-12-31; doi:10.5846/stxb202012173204</summary>

```text
[3] Retrieving the forest aboveground biomass by combining the red edge bands of Sentinel-2 and GF-6
    id: s2:fc5c1378b2a10d0d3d520d5157e37e8009e9338a
    date: 2021
    venue: Acta Ecologica Sinica
    authors: 蒋馥根，孙华，李成杰，马开森，陈松，龙江平，任蓝翔 JIANG Fugen
    abstract: [no abstract available]
```
</details>

<details><summary>[4] Multi-Sensor Aboveground Biomass Estimation in the Broadleaved Hyrcanian Forest of Iran — Ghasem Ronoud, P. Fatehi, A. Darvishsefat, E. Tomppo et al. (2021); cutoff-filter date 2021-09-07; doi:10.1080/07038992.2021.1968811</summary>

```text
[4] Multi-Sensor Aboveground Biomass Estimation in the Broadleaved Hyrcanian Forest of Iran
    id: s2:4f93064bf7fcf0ce25fe02a4c3315bba841e0f25
    date: 2021-09-06
    venue: Canadian journal of remote sensing
    authors: Ghasem Ronoud, P. Fatehi, A. Darvishsefat, E. Tomppo, J. Praks, M. Schaepman
    abstract: Abstract In this study, the capability of Landsat-8 (L8), Sentinel-2 (S2), Sentinel-1 (S1), and their combination was investigated for estimating aboveground biomass (AGB). A pure stand of Fagus Orientalis located in the Hyrcanian forest of Iran was selected as the study area. The performance of a parametric approach, i.e., Multiple Linear Regression (MLR) model and non-parametric approaches, i.e., k-Nearest Neighbor (k-NN), Random Forest (RF), and Support Vector Regression (SVR), were also evaluated for AGB estimations. Our results indicated that among S2 metrics, the FAPAR canopy biophysical index and NDVI index based on the red-edge band (NIR-b8a) have the highest correlation coefficient (r) of 0.420 and 0.417, respectively. The results of AGB estimation showed that a combination of S2 and S1 datasets using the k-NN algorithm had the best accuracy (R 2 of 0.57 and rRMSE of 14.68%). The best rRMSE using L8, S2, and S1 datasets was 18.95, 16.99, and 19.17% using k-NN, k-NN, and MLR algorithms, respectively. The combination of L8 with S1 dataset also improved the rRMSE relative to L8 and S1 separately by 0.96 and 1.18%, respectively. We concluded that the combination of optical data (L8 or S2) with SAR data (S1) improves the broadleaved Hyrcanian AGB estimation.
```
</details>

<details><summary>[5] Exploring the potential of Sentinel-2A satellite data for aboveground biomass estimation in fragmented Himalayan subtropical pine forest — Mobiishir Riaz Khan, I. Khan, M. H. A. Baig, Zhengjia Liu et al. (2020); cutoff-filter date 2020-12-23; doi:10.1007/s11629-019-5968-8</summary>

```text
[5] Exploring the potential of Sentinel-2A satellite data for aboveground biomass estimation in fragmented Himalayan subtropical pine forest
    id: s2:33c656e15bfa1e0ee03cc6d574dbd572db49bb80
    date: 2020-12-01
    venue: Journal of Mountain Science
    authors: Mobiishir Riaz Khan, I. Khan, M. H. A. Baig, Zhengjia Liu, M. Ashraf
    abstract: [no abstract available]
```
</details>

<details><summary>[6] Machine learning-based grassland aboveground biomass estimation and its response to climate variation in Southwest China — Wenjun Liu, Cong Xu, Zhi-Ming Zhang, H. D. De Boeck et al. (2023); cutoff-filter date 2023-03-09; doi:10.3389/fevo.2023.1146850</summary>

```text
[6] Machine learning-based grassland aboveground biomass estimation and its response to climate variation in Southwest China
    id: s2:00406f733b576374de13d2b7d242a4a0976264b9
    date: 2023-03-09
    venue: Frontiers in Ecology and Evolution
    authors: Wenjun Liu, Cong Xu, Zhi-Ming Zhang, H. D. De Boeck, Yanfen Wang, Liankai Zhang, Xiongwei Xu, Chen Zhang
    abstract: The demand for accurate estimation of aboveground biomass (AGB) at high spatial resolution is increasing in grassland-related research and management, especially for those regions with complex topography and fragmented landscapes, where grass and shrub are interspersed. In this study, based on 519 field AGB observations, integrating Synthetic Aperture Radar (SAR; Sentinel-1) and high-resolution (Sentinel-2) remote sensing images, environmental and topographical data, we estimated the AGB of mountain grassland in Southwest China (Yunnan Province and Guizhou Province) by using remote sensing algorithms ranging from traditional regression to cutting edge machine learning (ML) and deep learning (DL) models. Four models (i.e., multiple stepwise regression (MSR), random forest (RF), support vector machine (SVM) and convolutional neural network (CNN)) were developed and compared for AGB simulation purposes. The results indicated that the RF model performed the best among the four models (testing dataset: decision co-efficient (R2) was 0.80 for shrubland and 0.75 for grassland, respectively). Among all input variables in the RF model, the vegetation indices played the most important role in grassland AGB estimation, with 6 vegetation indices (EVI, EVI2, NDVI, NIRv, MSR and DVI) in the top 10 of input variables. For shrubland, however, topographical factors (elevation, 12.7% IncMSE (increase in mean squared error)) and SAR data (VH band, 11.3% IncMSE) were the variables which contributed the most in the AGB estimation model. By comparing the input variables to the RF model, we found that integrating SAR data has the potential to improve grassland AGB estimation, especially for shrubland (26.7% improvement in the estimation of shrubland AGB). Regional grassland AGB estimation showed a lower mean AGB in Yunnan Province (443.6 g/m2) than that in Guizhou Province (687.6 g/m2) in 2021. Moreover, the correlation between five consecutive years (2018–2022) of AGB data and climatic f [...]
```
</details>

<details><summary>[7] Argentinian Yungas Forest Fragmentation: Effects on Aboveground Biomass, Microclimate and Carbon Storage — Silvina M. Manrique, P. Vacaflor, Norma Cruz (2018); cutoff-filter date 2018-01-25; doi:10.4236/ojf.2018.81009</summary>

```text
[7] Argentinian Yungas Forest Fragmentation: Effects on Aboveground Biomass, Microclimate and Carbon Storage
    id: s2:6f00d01d6b257935664064c5a342726e1dda3bd5
    date: 2018-01-25
    venue: Open Journal of Forestry
    authors: Silvina M. Manrique, P. Vacaflor, Norma Cruz
    abstract: The Argentinian Yungas ecosystem, the more extensive of the two richest biodiversity ecoregions of the country, is subject to rapid deforestation and fragmentation. Because these fragments are the future biodiversity reserves of this ecosystem, it was interesting to know if they constitute small-scale replicas of the forest from which they were detached. Our objective was to characterise the fragments and compare them with sectors of continuous forest by studying the aboveground tree biomass (for the five most representative forest species), microclimate (three variables) and edaphic factors (three) as a function of distance from forest edge at 15, 25, 50, 100 and 200 meters. We selected two size categories for fragments: 5 - 10 ha and 100 - 150 ha, located in the lower Yungas forest (LYF). We did sampling during the dry and wet seasons. As a result, in the larger fragments, the distance exerts a significant effect on the records of the microclimate and edaphic variables, gradually modifying them from the edge to the interior (up to at least 100 meters). The variations are more evident in the wet season. Solar radiation and relative humidity were two of the factors with greater response (Spearman r= -0.89; p p ·ha-1, for small and big fragments, respectively). The five species studied show less density and trees of reduced dimensions (lower dbh and height). Fast-growing pioneer plant species and disturbance-loving lianas accompany them. Edge plant composition presents notorious changes in the bigger fragments. Biomass and ecosystem processes such as carbon cycling, which have been modified into fragments, both are directly associated with the structure and functioning in LYF remnants. The human and animal intervention detected in the area could be interacting synergistically with the microclimate and biological changes observed and potentiate the effects of degradation in the fragments, creating conditions of greater threat to LYF’s biodiversity. However, the manage [...]
```
</details>

<details><summary>[8] Estimation Model of Rice Aboveground Dry Biomass Based on the Machine Learning and Hyperspectral Characteristic Parameters of the Canopy — Xiaoke Wang, Guiling Xu, Yue-Hua Feng, Jinfeng Peng et al. (2023); cutoff-filter date 2023-07-22; doi:10.3390/agronomy13071940</summary>

```text
[8] Estimation Model of Rice Aboveground Dry Biomass Based on the Machine Learning and Hyperspectral Characteristic Parameters of the Canopy
    id: s2:02fcf2f8a1135c77d06af96901d510adedb25ea5
    date: 2023-07-22
    venue: Agronomy
    authors: Xiaoke Wang, Guiling Xu, Yue-Hua Feng, Jinfeng Peng, Yu-Qi Gao, Jie Li, Zhili Han, Qiangxin Luo
    abstract: Accurately estimating aboveground dry biomass (ADB) is crucial. The ADB of rice has primarily been estimated using vegetation indices with several discrete bands; nevertheless, these indices cannot take advantage of continuous bands available with hyperspectral remote sensing. This study analyzed the quantitative relationship between canopy hyperspectral characteristic parameters (HCPs) and the ADB of rice. Twenty HCPs were used, including red edge area (SDr), blue edge area (SDb), and others. The variable-screening methods involved stepwise regression (SR), a regression coefficient (RC), variable importance in projection (vip), and random forest (RF). Stepwise and partial least squares regression methods were employed with traditional linear regression as well as machine learning methods including random forest (RF), a support vector machine (SVM), a BP artificial neural network (BPNN), and an extreme learning machine. Whole- and screening-variable models were constructed to estimate rice ADB at jointing, booting, heading, and maturing stages and across growth stages. Screening-variable models include SVM models based on SR (SVM-sr), RF models based on vip (RF-vip), and others. The results show that the HCPs had a significant correlation with ADB containing elements in the red edge region, namely SDr, SDr/SDb, and (SDr − SDb)/(SDr + SDb) at each growth stage. In addition, the screening performance of vip and SR was better than that of RC and RF, and fewer variables were screened. Moreover, the HCPs of the red edge region were screened using different screening methods at each growth stage. Among them, SDr/SDb and (SDr − SDb)/(SDr + SDb) appeared frequently, indicating they are important. Furthermore, at each growth stage, ADB could be well-estimated using diverse models with the RF modeling method based on vip screening variables found to be the best modeling method for ADB estimation; the independent variables of the RF-vip model involved the (SDr − SDb)/(SDr + SD [...]
```
</details>

<details><summary>[9] **KEY** Edge effects on tree architecture exacerbate biomass loss of fragmented Amazonian forests — Matheus Henrique Nunes, M. Vaz, J. Camargo, W. Laurance et al. (2023); cutoff-filter date 2023-12-14; doi:10.1038/s41467-023-44004-5</summary>

```text
[9] Edge effects on tree architecture exacerbate biomass loss of fragmented Amazonian forests
    id: s2:447646f5a65281858a0607a61c9b401865a0876e
    date: 2023-12-14
    venue: Nature Communications
    authors: Matheus Henrique Nunes, M. Vaz, J. Camargo, W. Laurance, A. D. de Andrade, A. Vicentini, S. Laurance, P. Raumonen
    abstract: Habitat fragmentation could potentially affect tree architecture and allometry. Here, we use ground surveys of terrestrial LiDAR in Central Amazonia to explore the influence of forest edge effects on tree architecture and allometry, as well as forest biomass, 40 years after fragmentation. We find that young trees colonising the forest fragments have thicker branches and architectural traits that optimise for light capture, which result in 50% more woody volume than their counterparts of similar stem size and height in the forest interior. However, we observe a disproportionately lower height in some large trees, leading to a 30% decline in their woody volume. Despite the substantial wood production of colonising trees, the lower height of some large trees has resulted in a net loss of 6.0 Mg ha−1 of aboveground biomass – representing 2.3% of the aboveground biomass of edge forests. Our findings indicate a strong influence of edge effects on tree architecture and allometry, and uncover an overlooked factor that likely exacerbates carbon losses in fragmented forests.
```
</details>

<details><summary>[10] **KEY** Integrating Spaceborne Lidar Nasa’s Gedi With Imaging Sensors To Map Aboveground Biomass In Fragmented Tropical Forests — R. Leite, C. Silva, C. H. do Amaral, D. N. Cosenza et al. (2023); cutoff-filter date 2023-07-16; doi:10.1109/igarss52108.2023.10282548</summary>

```text
[10] Integrating Spaceborne Lidar Nasa’s Gedi With Imaging Sensors To Map Aboveground Biomass In Fragmented Tropical Forests
    id: s2:0ca959ab67ae82a9e0950ed681ba48f234731177
    date: 2023-07-16
    venue: IEEE International Geoscience and Remote Sensing Symposium
    authors: R. Leite, C. Silva, C. H. do Amaral, D. N. Cosenza, M. Schlickmann, Kleydson Diego Da Rocha, J. Xia, M. Mohan
    abstract: Human induced forest degradation can reduce aboveground biomass (AGB) and carbon stock of forest fragments. Developing approaches to assess these effects in highly-degraded tropical forests is necessary, especially at large scales. In this study, we developed a framework to upscale NASA’s GEDI spaceborne lidar AGB products using data from imaging sensors in the Brazilian Atlantic Forest – one of the most degraded and fragmented ecosystems in the world. A Random Forest model was trained using GEDI footprint level AGB as response and vegetation indices from Landsat 8/OLI and ALOS/PALSAR-2 images as predictors. The models were used to map and assess the AGB at the core and edge of 8783 fragments. The model had r = 0.83 and RMSE = 34.06 Mg/ha. The AGB in the fragments’ edges were significantly lower than in the fragments’ cores. The results demonstrated the potential of the developed framework to assess fragmentation effects on highly degraded tropical forest ecosystems.
```
</details>

<details><summary>Post-hoc automated audit — NON-AUTHORITATIVE; uses hidden benchmark annotations</summary>

- primary auditor: `silence_as_null_error`; statuses {'H2': 'positive_or_present', 'H1': 'indeterminate'}; discriminative=False
- primary reasoning: H2 predicts that edge formation in fragmented forests can increase growth and biomass when climatic stress is low, so it implies the proposition should be observed. H1 focuses on increased stress and reduced resilience under fragmentation, but only where heat/water stress dominates; it is silent about what happens when climatic stress is low.
- derived opposition call: `one_sided_silence_labelled_neutral`
- evidence attribution: `informative_evidence_found` — The retrieved literature directly addresses the proposition, with multiple studies comparing aboveground biomass in edge and interior zones of fragmented forests. The assessor correctly identified that the evidence consistently contradicts the proposition, showing lower biomass at edges. The process worked as intended, surfacing relevant, informative evidence.
- disagreement flags: {'second_rater_vs_primary_discriminative': None, 'second_rater_vs_primary_status': None, 'retest_vs_primary_category': None, 'any': False}
</details>

**Human review** — `compatible_non_discriminative` · reviewer: Research Director · source: D045 · status: `first_pass_model_based_review` · genuinely discriminative: False · silence-as-null error: False · other fields not recorded

---

## #9 · `GP1-eukaryogenesis_mito_timing-X4`

**GP1-eukaryogenesis_mito_timing-X4** — case `eukaryogenesis_mito_timing`, node `X4`

> Archaeal lineages closely related to eukaryotes possess genes encoding cytoskeletal proteins such as actin and tubulin homologs.

- generated from **H2** (Candidate B); abstraction: `specific`
- influence: **0.521** (rank 2 in case, 9 overall; cumulative 35%) — favours **H2**
- log-likelihood contribution: H1 +0.528, H2 +1.049
- removing it alone: evidence withheld → case log-odds -1.901 (ranking unchanged); node deleted → -3.129 (ranking unchanged)

**Hypotheses (as shown to the verifier)**

- **H1** (Candidate A): Mitochondrial acquisition was an initiating/foundational event that preceded or enabled much of later eukaryotic cellular complexity; major eukaryote-specific cellular systems should therefore largely elaborate after mitochondrial acquisition.
- **H2** (Candidate B): Substantial eukaryotic cellular machinery - including cytoskeletal, membrane-remodelling/trafficking, endomembrane, phagocytic, and nuclear-associated complexity - evolved before mitochondrial acquisition in an already complex archaeal host.

**Verifier cross-hypothesis judgments** — P(X|H) combines these by noisy-OR

| hypothesis | origin? | direct edge | route via parent | P(X\|H) |
| --- | --- | --- | --- | --- |
| H1 | no | `unlikely` | — | 0.300 |
| H2 | yes | `implied` | — | 0.800 |

- edge rationale, **H1** → node: If mitochondrial acquisition was foundational and most eukaryotic cellular systems arose after it, then closely related archaeal lineages would be less likely to possess genes for cytoskeletal proteins like actin and tubulin homologs.
- edge rationale, **H2** → node: If substantial eukaryotic cellular machinery, including cytoskeletal components, evolved before mitochondrial acquisition in a complex archaeal host, then archaeal lineages closely related to eukaryotes would be expected to possess genes encoding cytoskeletal proteins such as actin and tubulin homologs.

**Verifier evidence** — label used in score: `support` (log-LR +1.2)

- queries: `archaea actin tubulin homologs`; `asgard archaea cytoskeletal protein genes`
- assessor rationale: Record [9] directly states that Asgard archaea, which are closely related to eukaryotes, possess genes encoding actin-regulating proteins and eukaryotic-like genes, supporting the proposition. Record [10] provides direct evidence that archaea possess a gene encoding FtsZ2, a putative tubulin homolog, and that this gene is highly conserved across the archaeal domain. Both records directly address the presence of actin and tubulin homologs in archaeal lineages related to eukaryotes.
- supporting spans cited by the assessor:
  - "Thor gelsolins are functional in regulating rabbit actin in in vitro assays, showing a range of activities including actin filament severing and bundling."
  - "Asgard archaea genomes contain potential eukaryotic-like genes that provide intriguing insight for the evolution of eukaryotes."
  - "In general, Asgard genomes encode two classes of actin-regulating proteins from sequence analysis, profilins and gelsolins."
  - "Here, we use genetics, functional genomics, and quantitative imaging to identify and characterize the novel CdrSL gene regulatory network in a model species of archaea."
  - "We demonstrate the central role of these ribbon-helix-helix family transcription factors in the regulation of cell division through specific transcriptional control of the gene encoding FtsZ2, a putative tubulin homolog."
  - "The cdrS-ftsZ2 locus is highly conserved throughout the archaeal domain, and the central function of CdrS in regulating cell division is conserved across hypersaline adapted archaea."
- 10 papers shown; key papers: `s2:40322deb03a84073a09ca822e015247f284e0577`, `s2:4cc65d91f1d8c6dcdb247b349e1d5a7c3b7859d8`
- _The evidence assessor returns ONE label for the node from all papers shown; the method has no per-paper contribution. Key papers and spans are those the assessor cited._

<details><summary>[1] Prefoldin, a chaperone that delivers unfolded proteins to cytosolic chaperonin. — Irina E. Vainberg, S. A. Lewis, H. Rommelaere, C. Ampe et al. (1998); cutoff-filter date 1998-05-31; doi:10.1016/s0092-8674(00)81446-4</summary>

```text
[1] Prefoldin, a chaperone that delivers unfolded proteins to cytosolic chaperonin.
    id: s2:ee3c7bc5c7934d7f416591654923227cd1317ac1
    date: 1998-05-29
    venue: Cell
    authors: Irina E. Vainberg, S. A. Lewis, H. Rommelaere, C. Ampe, Joël Vandekerckhove, H. Klein, N. Cowan
    abstract: We describe the discovery of a heterohexameric chaperone protein, prefoldin, based on its ability to capture unfolded actin. Prefoldin binds specifically to cytosolic chaperonin (c-cpn) and transfers target proteins to it. Deletion of the gene encoding a prefoldin subunit in S. cerevisiae results in a phenotype similar to those found when c-cpn is mutated, namely impaired functions of the actin and tubulin-based cytoskeleton. Consistent with prefoldin having a general role in chaperonin-mediated folding, we identify homologs in archaea, which have a class II chaperonin but contain neither actin nor tubulin. We show that by directing target proteins to chaperonin, prefoldin promotes folding in an environment in which there are many competing pathways for nonnative proteins.
```
</details>

<details><summary>[2] World War II, Sex and Antibiotics - II — Dipika Mishra, Irene Aniyan Puthethu, Nivedita Mitra, R. Srinivasan (2023); cutoff-filter date 2023-08-16; doi:10.1007/s12045-023-1657-6</summary>

```text
[2] World War II, Sex and Antibiotics - II
    id: s2:75a97e33474129acf4af3b391a4fced4242414be
    date: 2023-08-01
    venue: Resonance
    authors: Dipika Mishra, Irene Aniyan Puthethu, Nivedita Mitra, R. Srinivasan
    abstract: [no abstract available]
```
</details>

<details><summary>[3] Prokaryotic cytoskeletons: in situ and ex situ structures and cellular locations — Ki Woo Kim (2018); cutoff-filter date 2018-08-20; doi:10.1007/s10482-018-1142-5</summary>

```text
[3] Prokaryotic cytoskeletons: in situ and ex situ structures and cellular locations
    id: s2:b02cc3a654c8573f7cb1e3dc628cbdb87fe28d43
    date: 2018-08-20
    venue: Antonie van Leeuwenhoek
    authors: Ki Woo Kim
    abstract: [no abstract available]
```
</details>

<details><summary>[4] Tubulin Homologs in Bacteria and Archaea — N. Rumyantseva, D. M. Golofeeva, A. A. Khasanova, A. D. Vedyaykin (2024); cutoff-filter date 2024-05-14; doi:10.1134/s002626172460469x</summary>

```text
[4] Tubulin Homologs in Bacteria and Archaea
    id: s2:fe140c433d63a131e79d1a0b498b116b783f0d74
    date: 2024-05-14
    venue: Microbiology
    authors: N. Rumyantseva, D. M. Golofeeva, A. A. Khasanova, A. D. Vedyaykin
    abstract: [no abstract available]
```
</details>

<details><summary>[5] Phylogeny of actin and tubulin gene homologs in diverse eukaryotic species — P. Jayaswal, A. Shanker, N. Singh (2019); cutoff-filter date 2019-01-16; doi:10.31742/ijgpb.79s.1.20</summary>

```text
[5] Phylogeny of actin and tubulin gene homologs in diverse eukaryotic species
    id: s2:64ac873ebec556f478c902d1dae2f578931b2924
    date: 2019-01-16
    venue: Indian Journal of Genetics and Plant Breeding (The)
    authors: P. Jayaswal, A. Shanker, N. Singh
    abstract: Actin and tubulin are cytoskeleton proteins, which are
important components of the celland are conserved across
species. Despite their crucial significance in cell motility
and cell division the distribution and phylogeny of actin
and tubulin genes across taxa is poorly understood. Here
we used publicly available genomic data of 49 model species
of plants, animals, fungi and Protista for further
understanding the distribution of these genes among
diverse eukaryotic species using rice as reference. The
highest numbers of rice actin and tubulin gene homologs
were present in plants followed by animals, fungi and
Protista species, whereas ten actin and nine tubulin genes
were conserved in all 49 species. Phylogenetic analysis of
19 actin and 18 tubulin genes clustered them into four
major groups each. One each of the actin and tubulin gene
clusters was conserved across eukaryotic species. Species
trees based on the conserved actin and tubulin genes
showed evolutionary relationship of 49 different taxa
clustered into plants, animals, fungi and Protista. This study
provides a phylogenetic insight into the evolution of actin
and tubulin genes in diverse eukaryotic species.
```
</details>

<details><summary>[6] Unite to divide: Oligomerization of tubulin and actin homologs regulates initiation of bacterial cell division — M. Krupka, W. Margolin (2018); cutoff-filter date 2018-02-28; doi:10.12688/f1000research.13504.1</summary>

```text
[6] Unite to divide: Oligomerization of tubulin and actin homologs regulates initiation of bacterial cell division
    id: s2:d591224f066afd0429c0a8de93bfca2e070502db
    date: 2018-02-28
    venue: F1000Research
    authors: M. Krupka, W. Margolin
    abstract: To generate two cells from one, bacteria such as Escherichia coli use a complex of membrane-embedded proteins called the divisome that synthesize the division septum. The initial stage of cytokinesis requires a tubulin homolog, FtsZ, which forms polymers that treadmill around the cell circumference. The attachment of these polymers to the cytoplasmic membrane requires an actin homolog, FtsA, which also forms dynamic polymers that directly bind to FtsZ. Recent evidence indicates that FtsA and FtsZ regulate each other’s oligomeric state in E. coli to control the progression of cytokinesis, including the recruitment of septum synthesis proteins. In this review, we focus on recent advances in our understanding of protein-protein association between FtsZ and FtsA in the initial stages of divisome function, mainly in the well-characterized E. coli system.
```
</details>

<details><summary>[7] Bacterial Actin and Tubulin Homologs in Cell Growth and Division — Kimberly K. Busiek, W. Margolin (2015); cutoff-filter date 2015-03-16; doi:10.1016/j.cub.2015.01.030</summary>

```text
[7] Bacterial Actin and Tubulin Homologs in Cell Growth and Division
    id: s2:2629a59ed965373b7029e6ae94ad310b87f5daed
    date: 2015-03-16
    venue: Current Biology
    authors: Kimberly K. Busiek, W. Margolin
    abstract: In contrast to the elaborate cytoskeletal machines harbored by eukaryotic cells, such as mitotic spindles, cytoskeletal structures detectable by typical negative stain electron microscopy are generally absent from bacterial cells. As a result, for decades it was thought that bacteria lacked cytoskeletal machines. Revolutions in genomics and fluorescence microscopy have confirmed the existence not only of smaller-scale cytoskeletal structures in bacteria, but also of widespread functional homologs of eukaryotic cytoskeletal proteins. The presence of actin, tubulin, and intermediate filament homologs in these relatively simple cells suggests that primitive cytoskeletons first arose in bacteria. In bacteria such as Escherichia coli, homologs of tubulin and actin directly interact with each other and are crucial for coordinating cell growth and division. The function and direct interactions between these proteins will be the focus of this review.
```
</details>

<details><summary>[8] The Chloroplast Tubulin Homologs FtsZA and FtsZB from the Red Alga Galdieria sulphuraria Co-assemble into Dynamic Filaments* — Yao-Dong Chen, Katie J. Porter, M. Osawa, Anne Marie Augustus et al. (2017); cutoff-filter date 2017-02-08; doi:10.1074/jbc.m116.767715</summary>

```text
[8] The Chloroplast Tubulin Homologs FtsZA and FtsZB from the Red Alga Galdieria sulphuraria Co-assemble into Dynamic Filaments*
    id: s2:963fc1054760e76b7f9067534ce48710bb1f1cb2
    date: 2017-02-07
    venue: Journal of Biological Chemistry
    authors: Yao-Dong Chen, Katie J. Porter, M. Osawa, Anne Marie Augustus, Sara L. Milam, Chandra P. Joshi, K. Osteryoung, H. Erickson
    abstract: FtsZ is a homolog of eukaryotic tubulin and is present in almost all bacteria and many archaea, where it is the major cytoskeletal protein in the Z ring, required for cell division. Unlike some other cell organelles of prokaryotic origin, chloroplasts have retained FtsZ as an essential component of the division machinery. However, chloroplast FtsZs have been challenging to study because they are difficult to express and purify. To this end, we have used a FATT tag expression system to produce as soluble proteins the two chloroplast FtsZs from Galdieria sulphuraria, a thermophilic red alga. GsFtsZA and GsFtsZB assembled individually in the presence of GTP, forming large bundles of protofilaments. GsFtsZA also assembled in the presence of GDP, the first member of the FtsZ/tubulin superfamily to do so. Mixtures of GsFtsZA and GsFtsZB assembled protofilament bundles and hydrolyzed GTP at a rate approximately equal to the sum of their individual rates, suggesting a random co-assembly. GsFtsZA assembly by itself in limiting GTP gave polymers that remained stable for a prolonged time. However, when GsFtsZB was added, the co-polymers disassembled with enhanced kinetics, suggesting that the GsFtsZB regulates and enhances disassembly dynamics. GsFtsZA-mts (where mts is a membrane-targeting amphipathic helix) formed Z ring-like helices when expressed in Escherichia coli. Co-expression of GsFtsZB (without an mts) gave co-assembly of both into similar helices. In summary, we provide biochemical evidence that GsFtsZA assembles as the primary scaffold of the chloroplast Z ring and that GsFtsZB co-assembly enhances polymer disassembly and dynamics.
```
</details>

<details><summary>[9] **KEY** Insights into the evolution of regulated actin dynamics via characterization of primitive gelsolin/cofilin proteins from Asgard archaea — C. Akıl, L. Tran, Magali Orhant-Prioux, Yohendran Baskaran et al. (2020); cutoff-filter date 2020-08-03; doi:10.1073/pnas.2009167117</summary>

```text
[9] Insights into the evolution of regulated actin dynamics via characterization of primitive gelsolin/cofilin proteins from Asgard archaea
    id: s2:4cc65d91f1d8c6dcdb247b349e1d5a7c3b7859d8
    date: 2020-08-03
    venue: Proceedings of the National Academy of Sciences of the United States of America
    authors: C. Akıl, L. Tran, Magali Orhant-Prioux, Yohendran Baskaran, E. Manser, L. Blanchoin, R. Robinson
    abstract: Significance Eukaryotic gelsolin superfamily proteins generally comprise three or more related domains. Here we characterize single- and double-domain gelsolins from Thorarchaeota (Thor). Similar domain architectures are present in Heimdall-, Loki-, and Odinarchaeota. Thor gelsolins are functional in regulating rabbit actin in in vitro assays, showing a range of activities including actin filament severing and bundling. These gelsolins bind to the eukaryotic gelsolin/cofilin-binding site on actin. Two-domain, but not one-domain, gelsolins are calcium regulated. Thor gelsolins appear to have the characteristics and structure consistent with primitive gelsolins/cofilins, suggesting that these single- and double-domain gelsolins are a record of a nascent preeukaryotic actin-regulation machinery. Asgard archaea genomes contain potential eukaryotic-like genes that provide intriguing insight for the evolution of eukaryotes. The eukaryotic actin polymerization/depolymerization cycle is critical for providing force and structure in many processes, including membrane remodeling. In general, Asgard genomes encode two classes of actin-regulating proteins from sequence analysis, profilins and gelsolins. Asgard profilins were demonstrated to regulate actin filament nucleation. Here, we identify actin filament severing, capping, annealing and bundling, and monomer sequestration activities by gelsolin proteins from Thorarchaeota (Thor), which complete a eukaryotic-like actin depolymerization cycle, and indicate complex actin cytoskeleton regulation in Asgard organisms. Thor gelsolins have homologs in other Asgard archaea and comprise one or two copies of the prototypical gelsolin domain. This appears to be a record of an initial preeukaryotic gene duplication event, since eukaryotic gelsolins are generally comprise three to six domains. X-ray structures of these proteins in complex with mammalian actin revealed similar interactions to the first domain of human gelsolin or cofilin [...]
```
</details>

<details><summary>[10] **KEY** The Ribbon-Helix-Helix Domain Protein CdrS Regulates the Tubulin Homolog ftsZ2 To Control Cell Division in Archaea — Cynthia L. Darnell, Jenny Zheng, Sean Wilson, Ryan M Bertoli et al. (2020); cutoff-filter date 2020-08-11; doi:10.1128/mbio.01007-20</summary>

```text
[10] The Ribbon-Helix-Helix Domain Protein CdrS Regulates the Tubulin Homolog ftsZ2 To Control Cell Division in Archaea
    id: s2:40322deb03a84073a09ca822e015247f284e0577
    date: 2020-08-11
    venue: mBio
    authors: Cynthia L. Darnell, Jenny Zheng, Sean Wilson, Ryan M Bertoli, Alexandre W. Bisson-Filho, Ethan C. Garner, Amy K. Schmid
    abstract: Healthy cell growth and division are critical for individual organism survival and species long-term viability. However, it remains unknown how cells of the domain Archaea maintain a healthy cell cycle. Understanding the archaeal cell cycle is of paramount evolutionary importance given that an archaeal cell was the host of the endosymbiotic event that gave rise to eukaryotes. Here, we identify and characterize novel molecular players needed for regulating cell division in archaea. These molecules dictate the timing of cell septation but are dispensable for growth between divisions. Timing is accomplished through transcriptional control of the cell division ring. Our results shed light on mechanisms underlying the archaeal cell cycle, which has thus far remained elusive. ABSTRACT Precise control of the cell cycle is central to the physiology of all cells. In prior work we demonstrated that archaeal cells maintain a constant size; however, the regulatory mechanisms underlying the cell cycle remain unexplored in this domain of life. Here, we use genetics, functional genomics, and quantitative imaging to identify and characterize the novel CdrSL gene regulatory network in a model species of archaea. We demonstrate the central role of these ribbon-helix-helix family transcription factors in the regulation of cell division through specific transcriptional control of the gene encoding FtsZ2, a putative tubulin homolog. Using time-lapse fluorescence microscopy in live cells cultivated in microfluidics devices, we further demonstrate that FtsZ2 is required for cell division but not elongation. The cdrS-ftsZ2 locus is highly conserved throughout the archaeal domain, and the central function of CdrS in regulating cell division is conserved across hypersaline adapted archaea. We propose that the CdrSL-FtsZ2 transcriptional network coordinates cell division timing with cell growth in archaea. IMPORTANCE Healthy cell growth and division are critical for individual organism surviv [...]
```
</details>

<details><summary>Post-hoc automated audit — NON-AUTHORITATIVE; uses hidden benchmark annotations</summary>

- primary auditor: `silence_as_null_error`; statuses {'H1': 'indeterminate', 'H2': 'positive_or_present'}; discriminative=False
- primary reasoning: H1 (mitochondria-early) does not specifically predict whether closely related archaeal lineages should possess cytoskeletal genes; it is compatible with either presence or absence. H2 (complex-host/late-mitochondrion) predicts that substantial cellular complexity, including cytoskeletal genes, should be present in the archaeal host and its close relatives prior to mitochondrial acquisition.
- derived opposition call: `manufactured_from_silence`
- evidence attribution: `informative_evidence_found` — The retrieved literature includes papers that directly address the presence of actin-regulating and tubulin homolog genes in Asgard archaea, which are closely related to eukaryotes. The assessor correctly identified and used these papers to support the proposition, indicating that the retrieval and assessment process worked as intended.
- disagreement flags: {'second_rater_vs_primary_discriminative': None, 'second_rater_vs_primary_status': None, 'retest_vs_primary_category': None, 'any': False}
</details>

**Human review** — `generic_component_fact` · reviewer: Research Director · source: D045 · status: `first_pass_model_based_review` · genuinely discriminative: False · silence-as-null error: False · other fields not recorded

---

## #10 · `GP1-eukaryogenesis_mito_timing-X6`

**GP1-eukaryogenesis_mito_timing-X6** — case `eukaryogenesis_mito_timing`, node `X6`

> Members of the Asgard archaeal superphylum exhibit eukaryote-like cellular complexity, including genes for endomembrane and phagocytic functions.

- generated from **H2** (Candidate B); abstraction: `class`
- generator's stated reason: The claim posits that substantial complexity evolved in the archaeal host, making it more likely that Asgard archaea as a group show these features.
- influence: **0.521** (rank 3 in case, 10 overall; cumulative 38%) — favours **H2**
- log-likelihood contribution: H1 +0.528, H2 +1.049
- removing it alone: evidence withheld → case log-odds -1.901 (ranking unchanged); node deleted → -3.027 (ranking unchanged)

**Hypotheses (as shown to the verifier)**

- **H1** (Candidate A): Mitochondrial acquisition was an initiating/foundational event that preceded or enabled much of later eukaryotic cellular complexity; major eukaryote-specific cellular systems should therefore largely elaborate after mitochondrial acquisition.
- **H2** (Candidate B): Substantial eukaryotic cellular machinery - including cytoskeletal, membrane-remodelling/trafficking, endomembrane, phagocytic, and nuclear-associated complexity - evolved before mitochondrial acquisition in an already complex archaeal host.

**Verifier cross-hypothesis judgments** — P(X|H) combines these by noisy-OR

| hypothesis | origin? | direct edge | route via parent | P(X\|H) |
| --- | --- | --- | --- | --- |
| H1 | no | `unlikely` | — | 0.300 |
| H2 | yes | `implied` | — | 0.800 |

- edge rationale, **H1** → node: If eukaryote-like cellular complexity arose only after mitochondrial acquisition, Asgard archaea (which lack mitochondria) would be unlikely to exhibit such complexity.
- edge rationale, **H2** → node: If substantial eukaryotic cellular machinery evolved before mitochondrial acquisition in a complex archaeal host, it is clearly expected that Asgard archaea could exhibit eukaryote-like cellular complexity.

**Verifier evidence** — label used in score: `support` (log-LR +1.2)

- queries: `Asgard archaea endomembrane genes`; `Asgard archaea phagocytosis genes`
- assessor rationale: Multiple records directly state that Asgard archaea possess genes encoding eukaryote-like components involved in endomembrane system functions, such as ESCRT complexes and Arf family GTPases. These genes are described as structurally and functionally similar to their eukaryotic counterparts, and are implicated in membrane remodeling and cargo sorting. However, while these records provide direct evidence for the presence of eukaryote-like genes related to endomembrane and phagocytic functions, they do not report direct observation of cellular complexity or phagocytosis itself, so the support is not 'strong'.
- supporting spans cited by the assessor:
  - "Recently, genes encoding eukaryote-like ESCRT protein components have been identified in the genomes of Asgard archaea, a newly proposed archaeal superphylum that is thought to include the closest extant prokaryotic relatives of eukaryotes."
  - "Here we show that Vps4, Vps2/24/46, and Vps20/32/60, the core functional components of the Asgard ESCRT, co-evolved eukaryote-like structural and functional features."
  - "Molecular dynamic simulation and biochemical assays indicate that Asgard Vps4 contains a eukaryote-like Microtubule Interacting and Transport (MIT) domain that binds the distinct type-1 MIT Interacting Motif and type-2 MIT Interacting Motif in Vps2/24/46, and Vps20/32/60, respectively."
  - "Thus, this work provides evidence that the ESCRT complexes from Asgard archaea and eukaryotes are evolutionarily related and functionally similar."
  - "Here, we show that a UEV-Vps23 protein family, which contains UEV and Vps23 domains, mediates an ancient ESCRT and ubiquitin system interplay in Asgard archaea."
  - "The UEV binds ubiquitin with high affinity, making the UEV-Vps23 a sensor for sorting ubiquitinated cargo."
  - "Our results show that Arf family GTPases are present in Asgardarchaeota, and strongly suggest that they originated in the archaeal contributor to eukaryogenesis, providing support for nascent endomembrane system capacity evolving early in eukaryogenesis."
- 10 papers shown; key papers: `s2:2bab312eb5127c5b3aceac1ba0f8a69b7ff7fb3c`, `s2:3fd208ebadff884b05d9062d422bc38fea999d8e`, `s2:55a43731cbbe21dd1a001b68bb552cca6ab3f7e3`
- _The evidence assessor returns ONE label for the node from all papers shown; the method has no per-paper contribution. Key papers and spans are those the assessor cited._

<details><summary>[1] **KEY** Co-evolution of Eukaryotic-like Vps4 and ESCRT-III Subunits in the Asgard Archaea — Zhongyi Lu, Ting Fu, Tianyi Li, Yang Liu et al. (2020); cutoff-filter date 2020-05-06; doi:10.1101/2020.05.05.080093</summary>

```text
[1] Co-evolution of Eukaryotic-like Vps4 and ESCRT-III Subunits in the Asgard Archaea
    id: s2:2bab312eb5127c5b3aceac1ba0f8a69b7ff7fb3c
    date: 2020-05-06
    venue: bioRxiv (preprint)
    authors: Zhongyi Lu, Ting Fu, Tianyi Li, Yang Liu, Siyu Zhang, Jinquan Li, Junbiao Dai, E. Koonin
    abstract: The emergence of the endomembrane system is a key step in the evolution of cellular complexity during eukaryogenesis. The Endosomal Sorting Complex Required for Transport (ESCRT) machinery is essential and required for the endomembrane system functions in eukaryotic cells. Recently, genes encoding eukaryote-like ESCRT protein components have been identified in the genomes of Asgard archaea, a newly proposed archaeal superphylum that is thought to include the closest extant prokaryotic relatives of eukaryotes. However, structural and functional features of Asgard ESCRT remain uncharacterized. Here we show that Vps4, Vps2/24/46, and Vps20/32/60, the core functional components of the Asgard ESCRT, co-evolved eukaryote-like structural and functional features. Phylogenetic analysis shows that Asgard Vps4, Vps2/24/46, and Vps20/32/60 are closely related to their eukaryotic counterparts. Molecular dynamic simulation and biochemical assays indicate that Asgard Vps4 contains a eukaryote-like Microtubule Interacting and Transport (MIT) domain that binds the distinct type-1 MIT Interacting Motif and type-2 MIT Interacting Motif in Vps2/24/46, and Vps20/32/60, respectively. The Asgard Vps4 partly, but much more efficiently than homologs from other archaea, complements the vps4 null mutant of Saccharomyces cerevisiae, further supporting the functional similarity between the membrane remodeling machineries of Asgard archaea and eukaryotes. Thus, this work provides evidence that the ESCRT complexes from Asgard archaea and eukaryotes are evolutionarily related and functionally similar. Thus, despite the apparent absence of endomembranes in Asgard archaea, the eukaryotic ESCRT seems to have been directly inherited from an Asgard ancestor, to become a key component of the emerging endomembrane system. IMPORTANCE The discovery of Asgard archaea has changed the exiting ideas on the origins of Eukaryotes. Researchers propose that eukaryotic cells evolve from Asgard archaea. This hypothe [...]
    note: merged with 1 other version(s) of the same work
```
</details>

<details><summary>[2] The symbiotic origin of the eukaryotic cell. — P. López-García, D. Moreira (2023); cutoff-filter date 2023-05-30; doi:10.5802/crbiol.118</summary>

```text
[2] The symbiotic origin of the eukaryotic cell.
    id: s2:bfbb10e2d371e78eb6ab4b8fd3818a598b4c8413
    date: 2023-05-30
    venue: Comptes rendus. Biologies
    authors: P. López-García, D. Moreira
    abstract: Eukaryogenesis represented a major evolutionary transition that led to the emergence of complex cells from simpler ancestors. For several decades, the most accepted scenario involved the evolution of an independent lineage of proto-eukaryotes endowed with an endomembrane system, including a nuclear compartment, a developed cytoskeleton and phagocytosis, which engulfed the alphaproteobacterial ancestor of mitochondria. However, the recent discovery by metagenomic and cultural approaches of Asgard archaea, which harbour many genes in common with eukaryotes and are their closest relatives in phylogenomic trees, rather supports scenarios based on the symbiosis of one Asgard-like archaeon and one or more bacteria at the origin of the eukaryotic cell. Here, we review the recent discoveries that led to this conceptual shift, briefly evoking current models of eukaryogenesis and the challenges ahead to discriminate between them and to establish a detailed, plausible scenario that accounts for the evolution of eukaryotic traits from those of their prokaryotic ancestors.
```
</details>

<details><summary>[3] **KEY** Origin of eukaryotic-like Vps23 shapes an ancient functional interplay between ESCRT and ubiquitin system in Asgard archaea. — Zhongyi Lu, Siyu Zhang, Yang Liu, Runyue Xia et al. (2024); cutoff-filter date 2024-02-14; doi:10.1016/j.celrep.2024.113781</summary>

```text
[3] Origin of eukaryotic-like Vps23 shapes an ancient functional interplay between ESCRT and ubiquitin system in Asgard archaea.
    id: s2:55a43731cbbe21dd1a001b68bb552cca6ab3f7e3
    date: 2024-02-01
    venue: Cell Reports
    authors: Zhongyi Lu, Siyu Zhang, Yang Liu, Runyue Xia, Meng Li
    abstract: Functional interplay between the endosomal sorting complexes required for transport (ESCRT) and the ubiquitin system underlies the ubiquitin-dependent cargo-sorting pathway of the eukaryotic endomembrane system, yet its evolutionary origin remains unclear. Here, we show that a UEV-Vps23 protein family, which contains UEV and Vps23 domains, mediates an ancient ESCRT and ubiquitin system interplay in Asgard archaea. The UEV binds ubiquitin with high affinity, making the UEV-Vps23 a sensor for sorting ubiquitinated cargo. A steadiness box in the Vps23 domain undergoes ubiquitination through an Asgard E1, E2, and RING E3 cascade. The UEV-Vps23 switches between autoinhibited and active forms, regulating the ESCRT and ubiquitin system interplay. Furthermore, the shared sequence and structural homology among the UEV-Vps23, eukaryotic Vps23, and archaeal CdvA suggest a common evolutionary origin. Together, this work expands our understanding of the ancient ESCRT and ubiquitin system interplay that likely arose antedating divergent evolution between Asgard archaea and eukaryotes.
    note: merged with 1 other version(s) of the same work
```
</details>

<details><summary>[4] **KEY** Arf family GTPases are present in Asgard archaea — Romana Vargová, Roxanne Chevreau, M. Alves, Camille Courbin et al. (2024); cutoff-filter date 2024-03-01; doi:10.1101/2024.02.28.582541</summary>

```text
[4] Arf family GTPases are present in Asgard archaea
    id: s2:3fd208ebadff884b05d9062d422bc38fea999d8e
    date: 2024-03-01
    venue: bioRxiv (preprint)
    authors: Romana Vargová, Roxanne Chevreau, M. Alves, Camille Courbin, Kara Terry, Pierre Legrand, Marek Eliáš, Julie Ménétrey
    abstract: The emergence of eukaryotes from their prokaryotic ancestors is one of the most fundamental evolutionary events in the history of life. Little is robustly known about how eukaryogenesis occurred, but a major breakthrough came with the identification of the Asgardarchaeota, the closest prokaryotic lineage to eukaryotes yet discovered. Endomembrane organelles, and the capacity to transport material between them, are major hallmarks of eukaryotic cells. The Arf family GTPases are crucial regulators of organelle dynamics in eukaryotes, functioning in vesicle budding, membrane tethering and membrane-cytoskeleton interactions. Although an expanded GTPase complement has been reported in the Asgardarchaeota, the specific origins of the Arf family remain elusive. Here we report a new group of prokaryotic GTPases, the ArfRs. Widely present in Asgardarchaeota and almost exclusive to them, it is the clade from which all eukaryotic Arf family proteins are derived. Heterologous expression of representative Asgardarchaeota ArfR proteins in the model eukaryote Saccharomyces cerevisiae and X-ray crystallographic studies demonstrate that ArfR GTPases possess the mechanism of membrane binding and structural features unique to Arf family proteins. Our results show that Arf family GTPases are present in Asgardarchaeota, and strongly suggest that they originated in the archaeal contributor to eukaryogenesis, providing support for nascent endomembrane system capacity evolving early in eukaryogenesis.
```
</details>

<details><summary>[5] Complete genomes of Asgard archaea reveal diverse integrated and mobile genetic elements — L. Valentin-Alvarado, Ling-Dong Shi, K. Appler, Alexander Crits-Christoph et al. (2024); cutoff-filter date 2024-10-15; doi:10.1101/gr.279480.124</summary>

```text
[5] Complete genomes of Asgard archaea reveal diverse integrated and mobile genetic elements
    id: s2:e6c1517d25f3fd63fe8c18daea997d100398e2d3
    date: 2024-10-01
    venue: Genome Research (preprint)
    authors: L. Valentin-Alvarado, Ling-Dong Shi, K. Appler, Alexander Crits-Christoph, V. de Anda, Benjamin A. Adler, Michael L. Cui, Lynn Ly
    abstract: Asgard archaea are of great interest as the progenitors of Eukaryotes, but little is known about the mobile genetic elements (MGEs) that may shape their ongoing evolution. Here, we describe MGEs that replicate in Atabeyarchaeia, a wetland Asgard archaea lineage represented by two complete genomes. We used soil depth–resolved population metagenomic data sets to track 18 MGEs for which genome structures were defined and precise chromosome integration sites could be identified for confident host linkage. Additionally, we identified a complete 20.67 kbp circular plasmid and two family-level groups of viruses linked to Atabeyarchaeia, via CRISPR spacer targeting. Closely related 40 kbp viruses possess a hypervariable genomic region encoding combinations of specific genes for small cysteine-rich proteins structurally similar to restriction-homing endonucleases. One 10.9 kbp integrative conjugative element (ICE) integrates genomically into the Atabeyarchaeum deiterrae-1 chromosome and has a 2.5 kbp circularizable element integrated within it. The 10.9 kbp ICE encodes an expressed Type IIG restriction-modification system with a sequence specificity matching an active methylation motif identified by Pacific Biosciences (PacBio) high-accuracy long-read (HiFi) metagenomic sequencing. Restriction-modification of Atabeyarchaeia differs from that of another coexisting Asgard archaea, Freyarchaeia, which has few identified MGEs but possesses diverse defense mechanisms, including DISARM and Hachiman, not found in Atabeyarchaeia. Overall, defense systems and methylation mechanisms of Asgard archaea likely modulate their interactions with MGEs, and integration/excision and copy number variation of MGEs in turn enable host genetic versatility.
```
</details>

<details><summary>[6] Genetic elements and defense systems drive diversification and evolution in Asgard archaea — L. Valentin-Alvarado, Ling-Dong Shi, K. Appler, Alexander Crits-Christoph et al. (2024); cutoff-filter date 2024-03-23; doi:10.1101/2024.03.22.586370</summary>

```text
[6] Genetic elements and defense systems drive diversification and evolution in Asgard archaea
    id: s2:703b9d3f624e80434597ed11069c47cdaf2dad25
    date: 2024-03-23
    venue: bioRxiv (preprint)
    authors: L. Valentin-Alvarado, Ling-Dong Shi, K. Appler, Alexander Crits-Christoph, Michael L. Cui, V. de Anda, Pedro Leão, Benjamin A. Adler
    abstract: [no abstract available]
```
</details>

<details><summary>[7] Potential for mercury methylation by Asgard archaea in mangrove sediments — Cuijing Zhang, Yu-Rong Liu, G. Cha, Yang Liu et al. (2023); cutoff-filter date 2023-01-13; doi:10.1038/s41396-023-01360-w</summary>

```text
[7] Potential for mercury methylation by Asgard archaea in mangrove sediments
    id: s2:30c1ff357052476c09b0ce28df3a76bd73c186c9
    date: 2023-01-13
    venue: The ISME Journal
    authors: Cuijing Zhang, Yu-Rong Liu, G. Cha, Yang Liu, Xin-Quan Zhou, Zhongyi Lu, Jie Pan, Mingwei Cai
    abstract: [no abstract available]
```
</details>

<details><summary>[8] Asgard archaea modulate potential methanogenesis substrates in wetland soil — L. Valentin-Alvarado, K. Appler, V. de Anda, M. C. Schoelmerich et al. (2023); cutoff-filter date 2024-07-31; doi:10.1038/s41467-024-49872-z</summary>

```text
[8] Asgard archaea modulate potential methanogenesis substrates in wetland soil
    id: s2:fe1d4f8116010838a66644fefd1a3aa3517e8126
    date: 2023-11-22
    venue: bioRxiv (preprint)
    authors: L. Valentin-Alvarado, K. Appler, V. de Anda, M. C. Schoelmerich, Jacob West-Roberts, Veronika Kivenson, A. Crits-Christoph, Lynn Ly
    abstract: The roles of Asgard archaea in eukaryogenesis and marine biogeochemical cycles are well studied, yet their contributions in soil ecosystems are unknown. Of particular interest are Asgard archaeal contributions to methane cycling in wetland soils. To investigate this, we reconstructed two complete genomes for soil-associated Atabeyarchaeia, a new Asgard lineage, and the first complete genome of Freyarchaeia, and defined their metabolism in situ. Metatranscriptomics highlights high expression of [NiFe]-hydrogenases, pyruvate oxidation and carbon fixation via the Wood-Ljungdahl pathway genes. Also highly expressed are genes encoding enzymes for amino acid metabolism, anaerobic aldehyde oxidation, hydrogen peroxide detoxification and glycerol and carbohydrate breakdown to acetate and formate. Overall, soil-associated Asgard archaea are predicted to be non-methanogenic acetogens, likely impacting reservoirs of substrates for methane production in terrestrial ecosystems. One-Sentence Summary Complete genomes of Asgard archaea, coupled with metatranscriptomic data, indicate roles in production and consumption of carbon compounds that are known to serve as substrates for methane production in wetlands.
```
</details>

<details><summary>[9] Ribosomal Protein Cluster Organization in Asgard Archaea — M. Tirumalai, R. Sivaraman, Layla A. Kutty, Eric L Song et al. (2023); cutoff-filter date 2023-09-29; doi:10.1155/2023/5512414</summary>

```text
[9] Ribosomal Protein Cluster Organization in Asgard Archaea
    id: s2:69d7c8666f34b698cdd937c6af0d0a34372ba5bc
    date: 2023-09-29
    venue: Archaea
    authors: M. Tirumalai, R. Sivaraman, Layla A. Kutty, Eric L Song, George E. Fox
    abstract: It has been proposed that the superphylum of Asgard Archaea may represent a historical link between the Archaea and Eukarya. Following the discovery of the Archaea, it was soon appreciated that archaeal ribosomes were more similar to those of Eukarya rather than Bacteria. Coupled with other eukaryotic-like features, it has been suggested that the Asgard Archaea may be directly linked to eukaryotes. However, the genomes of Bacteria and non-Asgard Archaea generally organize ribosome-related genes into clusters that likely function as operons. In contrast, eukaryotes typically do not employ an operon strategy. To gain further insight into conservation of the r-protein genes, the genome order of conserved ribosomal protein (r-protein) coding genes was identified in 17 Asgard genomes (thirteen complete genomes and four genomes with less than 20 contigs) and compared with those found previously in non-Asgard archaeal and bacterial genomes. A universal core of two clusters of 14 and 4 cooccurring r-proteins, respectively, was identified in both the Asgard and non-Asgard Archaea. The equivalent genes in the E. coli version of the cluster are found in the S10 and spc operons. The large cluster of 14 r-protein genes (uS19-uL22-uS3-uL29-uS17 from the S10 operon and uL14-uL24-uL5-uS14-uS8-uL6-uL18-uS5-uL30-uL15 from the spc operon) occurs as a complete set in the genomes of thirteen Asgard genomes (five Lokiarchaeotes, three Heimdallarchaeotes, one Odinarchaeote, and four Thorarchaeotes). Four less conserved clusters with partial bacterial equivalents were found in the Asgard. These were the L30e (str operon in Bacteria) cluster, the L18e (alpha operon in Bacteria) cluster, the S24e-S27ae-rpoE1 cluster, and the L31e, L12..L1 cluster. Finally, a new cluster referred to as L7ae was identified. In many cases, r-protein gene clusters/operons are less conserved in their organization in the Asgard group than in other Archaea. If this is generally true for nonribosomal gene clusters, [...]
```
</details>

<details><summary>[10] Promethearchaeum syntrophicum gen. nov., sp. nov., an anaerobic, obligately syntrophic archaeon, the first isolate of the lineage ‘Asgard’ archaea, and proposal of the new archaeal phylum Promethearchaeota phyl. nov. and kingdom Promethearchaeati regn. nov. — H. Imachi, M. Nobu, Shingo Kato, Y. Takaki et al. (2024); cutoff-filter date 2024-07-05; doi:10.1099/ijsem.0.006435</summary>

```text
[10] Promethearchaeum syntrophicum gen. nov., sp. nov., an anaerobic, obligately syntrophic archaeon, the first isolate of the lineage ‘Asgard’ archaea, and proposal of the new archaeal phylum Promethearchaeota phyl. nov. and kingdom Promethearchaeati regn. nov.
    id: s2:547db19c1375763548b72637119b8e49b9ca4323
    date: 2024-07-01
    venue: International Journal of Systematic and Evolutionary Microbiology
    authors: H. Imachi, M. Nobu, Shingo Kato, Y. Takaki, M. Miyazaki, Makoto Miyata, Miyuki Ogawara, Yumi Saito
    abstract: Abstract An anaerobic, mesophilic, syntrophic, archaeon strain MK-D1T, was isolated as a pure co-culture with Methanogenium sp. strain MK-MG from deep-sea methane seep sediment. This organism is, to our knowledge, the first cultured representative of ‘Asgard’ archaea, an archaeal group closely related to eukaryotes. Here, we describe the detailed physiology and phylogeny of MK-D1T and propose Promethearchaeum syntrophicum gen. nov., sp. nov. to accommodate this strain. Cells were non-motile, small cocci, approximately 300–750 nm in diameter and produced membrane vesicles, chains of blebs and membrane-based protrusions. MK-D1T grew at 4–30 °C with optimum growth at 20 °C. The strain grew chemoorganotrophically with amino acids, peptides and yeast extract with obligate dependence on syntrophy with H2-/formate-utilizing organisms. MK-D1T showed the fastest growth and highest maximum cell yield when grown with yeast extract as the substrate: approximately 3 months to full growth, reaching up to 6.7×106 16S rRNA gene copies ml−1. MK-D1T had a circular 4.32 Mb chromosome with a DNA G+C content of 31.1 mol%. The results of phylogenetic analyses of the 16S rRNA gene and conserved marker proteins indicated that the strain is affiliated with ‘Asgard’ archaea and more specifically DHVC1/DSAG/MBG-B and ‘Lokiarchaeota’/‘Lokiarchaeia’. On the basis of the results of 16S rRNA gene sequence analysis, the most closely related isolated relatives were Infirmifilum lucidum 3507LTT (76.09 %) and Methanothermobacter tenebrarum RMAST (77.45 %) and the closest relative in enrichment culture was Candidatus ‘Lokiarchaeum ossiferum’ (95.39 %). The type strain of the type species is MK-D1T (JCM 39240T and JAMSTEC no. 115508). We propose the associated family, order, class, phylum, and kingdom as Promethearchaeaceae fam. nov., Promethearchaeales ord. nov., Promethearchaeia class. nov., Promethearchaeota phyl. nov., and Promethearchaeati regn. nov., respectively. These are in accordance with ICN [...]
```
</details>

<details><summary>Post-hoc automated audit — NON-AUTHORITATIVE; uses hidden benchmark annotations</summary>

- primary auditor: `silence_as_null_error`; statuses {'H1': 'indeterminate', 'H2': 'positive_or_present'}; discriminative=False
- primary reasoning: H2 predicts that substantial eukaryote-like complexity, including endomembrane and phagocytic functions, should be present in the archaeal host, so Asgard archaea exhibiting these features is expected. H1 is silent on the complexity of extant or ancestral archaea, making no commitment about Asgard archaea's features.
- derived opposition call: `manufactured_from_silence`
- evidence attribution: `informative_evidence_found` — The retrieved literature directly addresses the proposition by documenting the presence of eukaryote-like genes in Asgard archaea, specifically those involved in endomembrane and phagocytic functions (e.g., ESCRT complexes, Arf GTPases). The assessor correctly noted that while direct cellular observations are lacking, the genetic evidence is relevant and informative for the claim as stated. The process worked as intended.
- disagreement flags: {'second_rater_vs_primary_discriminative': None, 'second_rater_vs_primary_status': None, 'retest_vs_primary_category': None, 'any': False}
</details>

**Human review** — `generic_component_fact` · reviewer: Research Director · source: D045 · status: `first_pass_model_based_review` · genuinely discriminative: False · silence-as-null error: False · other fields not recorded

---

## #11 · `GP1-forest_fragmentation_resilience-X7`

**GP1-forest_fragmentation_resilience-X7** — case `forest_fragmentation_resilience`, node `X7`

> Aboveground biomass is higher at forest edges than in interior zones in recently fragmented forests under low climatic stress.

- generated from **H2** (Candidate A); abstraction: `specific`
- influence: **0.466** (rank 2 in case, 11 overall; cumulative 41%) — favours **H1**
- log-likelihood contribution: H2 -1.835, H1 -1.370
- removing it alone: evidence withheld → case log-odds -1.165 (ranking unchanged); node deleted → -1.165 (ranking unchanged)

**Hypotheses (as shown to the verifier)**

- **H1** (Candidate B): Fragmentation increases exposure to heat, atmospheric dryness, wind, and drought stress, raising mortality and reducing ecosystem resilience, especially where water/heat stress dominates.
- **H2** (Candidate A): Edge formation can increase light availability and relax limiting-resource constraints, increasing growth, biomass, recovery capacity, and potentially resilience where climatic stress penalties are small enough.

**Verifier cross-hypothesis judgments** — P(X|H) combines these by noisy-OR

| hypothesis | origin? | direct edge | route via parent | P(X\|H) |
| --- | --- | --- | --- | --- |
| H2 | yes | `implied` | X1 [H→parent `implied`, P=0.80] → `strongly_implied` | 0.972 |
| H1 | no | `neutral` | X1 [H→parent `neutral`, P=0.50] → `strongly_implied` | 0.863 |

- edge rationale, **H2** → node: Candidate A states that edge formation can increase growth and biomass where climatic stress is low, which clearly supports higher aboveground biomass at edges under these conditions.
- edge rationale, **H1** → node: Candidate B focuses on increased stress and mortality due to fragmentation, but specifies this is especially where water/heat stress dominates, not addressing the low climatic stress scenario in the proposition.
- parent `X1`: In fragmented forests with newly formed edges, aboveground biomass increases in edge zones compared to interior zones when climatic stress is low.
- chain rationale, `X1` → node: The parent proposition directly states that aboveground biomass increases at edges compared to interiors in recently fragmented forests under low climatic stress, which matches the child proposition almost exactly.

**Verifier evidence** — label used in score: `strong_contradiction` (log-LR -2.0)

- queries: `forest edge aboveground biomass`; `forest interior aboveground biomass`
- assessor rationale: Multiple studies directly compare aboveground biomass at forest edges and interiors in fragmented forests. Record [2] reports that aboveground biomass is significantly higher in interior plots than at edges. Record [10] finds that edge fragments have significantly lower aboveground biomass than cores. Record [9] describes a net loss of aboveground biomass at edges due to architectural changes, despite some increased wood production in colonizing trees. These findings directly contradict the proposition as written.
- supporting spans cited by the assessor:
  - "AGB was significantly higher in plots in the forest interior than in those at the edge of forests."
  - "The AGB in the fragments’ edges were significantly lower than in the fragments’ cores."
  - "Despite the substantial wood production of colonising trees, the lower height of some large trees has resulted in a net loss of 6.0 Mg ha−1 of aboveground biomass – representing 2.3% of the aboveground biomass of edge forests."
- 10 papers shown; key papers: `s2:0ca959ab67ae82a9e0950ed681ba48f234731177`, `s2:447646f5a65281858a0607a61c9b401865a0876e`, `s2:6e638cdba421a400b68e9980fb765c9d8c015c45`
- _The evidence assessor returns ONE label for the node from all papers shown; the method has no per-paper contribution. Key papers and spans are those the assessor cited._

<details><summary>[1] Automated Machine Learning Driven Stacked Ensemble Modeling for Forest Aboveground Biomass Prediction Using Multitemporal Sentinel-2 Data — Parth Naik, M. Dalponte, L. Bruzzone (2023); cutoff-filter date 2023-12-31; doi:10.1109/jstars.2022.3232583</summary>

```text
[1] Automated Machine Learning Driven Stacked Ensemble Modeling for Forest Aboveground Biomass Prediction Using Multitemporal Sentinel-2 Data
    id: s2:dc10dffdb0b4c1f6f17c418e93779081863be483
    date: 2023
    venue: IEEE Journal of Selected Topics in Applied Earth Observations and Remote Sensing
    authors: Parth Naik, M. Dalponte, L. Bruzzone
    abstract: Modeling and large-scale mapping of forest aboveground biomass (AGB) is a complicated, challenging, and expensive task. There are considerable variations in forest characteristics that create functional disparity for different models and needs comprehensive evaluation. Moreover, the human-bias involved in the process of modeling and evaluation affects the generalization of models at larger scales. In this article, we present an automated machine learning framework for modeling, evaluation, and stacking of multiple base models for AGB prediction. We incorporate a hyperparameter optimization procedure for automatic extraction of targeted features from multitemporal Sentinel-2 data that minimizes human-bias in the proposed modeling pipeline. We integrate the two independent frameworks for automatic feature extraction and automatic model ensembling and evaluation. The results suggest that the extracted target-oriented features have an excessive contribution of red-edge and short-wave infrared spectrum. The feature importance scale indicates a dominant role of summer-based features as compared to other seasons. The automated ensembling and evaluation framework produced a stacked ensemble of base models that outperformed individual base models in accurately predicting forest AGB. The stacked ensemble model delivered the best scores of R2cv = 0.71 and RMSE = 74.44 Mgha−1. The other base models delivered R2cv and RMSE ranging between 0.38–0.66 and 81.27–109.44 Mg ha−1, respectively. The model evaluation metrics indicated that the stacked ensemble model was more resistant to outliers and achieved a better generalization. Thus, the proposed study demonstrated an effective automated modeling pipeline for predicting AGB by minimizing human-bias and deployable over large and diverse forest areas.
```
</details>

<details><summary>[2] **KEY** Aboveground Biomass and Endogenous Hormones in Sub-Tropical Forest Fragments — Chang Liu, Wen-Zhi Du, Hong-Lin Cao, Chunyu Shen et al. (2023); cutoff-filter date 2023-03-23; doi:10.3390/f14040661</summary>

```text
[2] Aboveground Biomass and Endogenous Hormones in Sub-Tropical Forest Fragments
    id: s2:6e638cdba421a400b68e9980fb765c9d8c015c45
    date: 2023-03-23
    venue: Forests
    authors: Chang Liu, Wen-Zhi Du, Hong-Lin Cao, Chunyu Shen, Lei Ma
    abstract: Associated endogenous hormones were affected by forest fragmentation and significantly correlated with aboveground biomass storage. Forest fragmentation threatens aboveground biomass (AGB) and affects biodiversity and ecosystem functioning in multiple ways. We ask whether and how forest fragmentation influences AGB in forest fragments. We investigated differences in AGB between forest edges and interiors, and how plant community characteristics and endogenous hormones influenced AGB. In six 40 m × 40 m plots spread across three forest fragments, AGB was significantly higher in plots in the forest interior than in those at the edge of forests. The proportion of individuals with a large diameter at breast height (DBH > 40 cm) in the forest edges is higher than that in the forest interiors. Further, trees within a 15–40 cm DBH range had the highest contribution to AGB in all plots. Trees in interior plots had higher abscisic acid (ABA) and lower indole-3-acetic acid (IAA) concentrations than those in edge plots. In addition, AGB was significantly positively and negatively correlated with ABA and IAA concentrations at the community scale. In this study, we provide an account of endogenous hormones’ role as an integrator of environmental signals and, in particular, we highlight the correlation of these endogenous hormone levels with vegetation patterns. Edge effects strongly influenced AGB. In the future, more endogenous hormones and complex interactions should be better explored and understood to support consistent forest conservation and management actions.
```
</details>

<details><summary>[3] Retrieving the forest aboveground biomass by combining the red edge bands of Sentinel-2 and GF-6 — 蒋馥根，孙华，李成杰，马开森，陈松，龙江平，任蓝翔 JIANG Fugen (2021); cutoff-filter date 2021-12-31; doi:10.5846/stxb202012173204</summary>

```text
[3] Retrieving the forest aboveground biomass by combining the red edge bands of Sentinel-2 and GF-6
    id: s2:fc5c1378b2a10d0d3d520d5157e37e8009e9338a
    date: 2021
    venue: Acta Ecologica Sinica
    authors: 蒋馥根，孙华，李成杰，马开森，陈松，龙江平，任蓝翔 JIANG Fugen
    abstract: [no abstract available]
```
</details>

<details><summary>[4] Multi-Sensor Aboveground Biomass Estimation in the Broadleaved Hyrcanian Forest of Iran — Ghasem Ronoud, P. Fatehi, A. Darvishsefat, E. Tomppo et al. (2021); cutoff-filter date 2021-09-07; doi:10.1080/07038992.2021.1968811</summary>

```text
[4] Multi-Sensor Aboveground Biomass Estimation in the Broadleaved Hyrcanian Forest of Iran
    id: s2:4f93064bf7fcf0ce25fe02a4c3315bba841e0f25
    date: 2021-09-06
    venue: Canadian journal of remote sensing
    authors: Ghasem Ronoud, P. Fatehi, A. Darvishsefat, E. Tomppo, J. Praks, M. Schaepman
    abstract: Abstract In this study, the capability of Landsat-8 (L8), Sentinel-2 (S2), Sentinel-1 (S1), and their combination was investigated for estimating aboveground biomass (AGB). A pure stand of Fagus Orientalis located in the Hyrcanian forest of Iran was selected as the study area. The performance of a parametric approach, i.e., Multiple Linear Regression (MLR) model and non-parametric approaches, i.e., k-Nearest Neighbor (k-NN), Random Forest (RF), and Support Vector Regression (SVR), were also evaluated for AGB estimations. Our results indicated that among S2 metrics, the FAPAR canopy biophysical index and NDVI index based on the red-edge band (NIR-b8a) have the highest correlation coefficient (r) of 0.420 and 0.417, respectively. The results of AGB estimation showed that a combination of S2 and S1 datasets using the k-NN algorithm had the best accuracy (R 2 of 0.57 and rRMSE of 14.68%). The best rRMSE using L8, S2, and S1 datasets was 18.95, 16.99, and 19.17% using k-NN, k-NN, and MLR algorithms, respectively. The combination of L8 with S1 dataset also improved the rRMSE relative to L8 and S1 separately by 0.96 and 1.18%, respectively. We concluded that the combination of optical data (L8 or S2) with SAR data (S1) improves the broadleaved Hyrcanian AGB estimation.
```
</details>

<details><summary>[5] Exploring the potential of Sentinel-2A satellite data for aboveground biomass estimation in fragmented Himalayan subtropical pine forest — Mobiishir Riaz Khan, I. Khan, M. H. A. Baig, Zhengjia Liu et al. (2020); cutoff-filter date 2020-12-23; doi:10.1007/s11629-019-5968-8</summary>

```text
[5] Exploring the potential of Sentinel-2A satellite data for aboveground biomass estimation in fragmented Himalayan subtropical pine forest
    id: s2:33c656e15bfa1e0ee03cc6d574dbd572db49bb80
    date: 2020-12-01
    venue: Journal of Mountain Science
    authors: Mobiishir Riaz Khan, I. Khan, M. H. A. Baig, Zhengjia Liu, M. Ashraf
    abstract: [no abstract available]
```
</details>

<details><summary>[6] Machine learning-based grassland aboveground biomass estimation and its response to climate variation in Southwest China — Wenjun Liu, Cong Xu, Zhi-Ming Zhang, H. D. De Boeck et al. (2023); cutoff-filter date 2023-03-09; doi:10.3389/fevo.2023.1146850</summary>

```text
[6] Machine learning-based grassland aboveground biomass estimation and its response to climate variation in Southwest China
    id: s2:00406f733b576374de13d2b7d242a4a0976264b9
    date: 2023-03-09
    venue: Frontiers in Ecology and Evolution
    authors: Wenjun Liu, Cong Xu, Zhi-Ming Zhang, H. D. De Boeck, Yanfen Wang, Liankai Zhang, Xiongwei Xu, Chen Zhang
    abstract: The demand for accurate estimation of aboveground biomass (AGB) at high spatial resolution is increasing in grassland-related research and management, especially for those regions with complex topography and fragmented landscapes, where grass and shrub are interspersed. In this study, based on 519 field AGB observations, integrating Synthetic Aperture Radar (SAR; Sentinel-1) and high-resolution (Sentinel-2) remote sensing images, environmental and topographical data, we estimated the AGB of mountain grassland in Southwest China (Yunnan Province and Guizhou Province) by using remote sensing algorithms ranging from traditional regression to cutting edge machine learning (ML) and deep learning (DL) models. Four models (i.e., multiple stepwise regression (MSR), random forest (RF), support vector machine (SVM) and convolutional neural network (CNN)) were developed and compared for AGB simulation purposes. The results indicated that the RF model performed the best among the four models (testing dataset: decision co-efficient (R2) was 0.80 for shrubland and 0.75 for grassland, respectively). Among all input variables in the RF model, the vegetation indices played the most important role in grassland AGB estimation, with 6 vegetation indices (EVI, EVI2, NDVI, NIRv, MSR and DVI) in the top 10 of input variables. For shrubland, however, topographical factors (elevation, 12.7% IncMSE (increase in mean squared error)) and SAR data (VH band, 11.3% IncMSE) were the variables which contributed the most in the AGB estimation model. By comparing the input variables to the RF model, we found that integrating SAR data has the potential to improve grassland AGB estimation, especially for shrubland (26.7% improvement in the estimation of shrubland AGB). Regional grassland AGB estimation showed a lower mean AGB in Yunnan Province (443.6 g/m2) than that in Guizhou Province (687.6 g/m2) in 2021. Moreover, the correlation between five consecutive years (2018–2022) of AGB data and climatic f [...]
```
</details>

<details><summary>[7] Argentinian Yungas Forest Fragmentation: Effects on Aboveground Biomass, Microclimate and Carbon Storage — Silvina M. Manrique, P. Vacaflor, Norma Cruz (2018); cutoff-filter date 2018-01-25; doi:10.4236/ojf.2018.81009</summary>

```text
[7] Argentinian Yungas Forest Fragmentation: Effects on Aboveground Biomass, Microclimate and Carbon Storage
    id: s2:6f00d01d6b257935664064c5a342726e1dda3bd5
    date: 2018-01-25
    venue: Open Journal of Forestry
    authors: Silvina M. Manrique, P. Vacaflor, Norma Cruz
    abstract: The Argentinian Yungas ecosystem, the more extensive of the two richest biodiversity ecoregions of the country, is subject to rapid deforestation and fragmentation. Because these fragments are the future biodiversity reserves of this ecosystem, it was interesting to know if they constitute small-scale replicas of the forest from which they were detached. Our objective was to characterise the fragments and compare them with sectors of continuous forest by studying the aboveground tree biomass (for the five most representative forest species), microclimate (three variables) and edaphic factors (three) as a function of distance from forest edge at 15, 25, 50, 100 and 200 meters. We selected two size categories for fragments: 5 - 10 ha and 100 - 150 ha, located in the lower Yungas forest (LYF). We did sampling during the dry and wet seasons. As a result, in the larger fragments, the distance exerts a significant effect on the records of the microclimate and edaphic variables, gradually modifying them from the edge to the interior (up to at least 100 meters). The variations are more evident in the wet season. Solar radiation and relative humidity were two of the factors with greater response (Spearman r= -0.89; p p ·ha-1, for small and big fragments, respectively). The five species studied show less density and trees of reduced dimensions (lower dbh and height). Fast-growing pioneer plant species and disturbance-loving lianas accompany them. Edge plant composition presents notorious changes in the bigger fragments. Biomass and ecosystem processes such as carbon cycling, which have been modified into fragments, both are directly associated with the structure and functioning in LYF remnants. The human and animal intervention detected in the area could be interacting synergistically with the microclimate and biological changes observed and potentiate the effects of degradation in the fragments, creating conditions of greater threat to LYF’s biodiversity. However, the manage [...]
```
</details>

<details><summary>[8] Estimation Model of Rice Aboveground Dry Biomass Based on the Machine Learning and Hyperspectral Characteristic Parameters of the Canopy — Xiaoke Wang, Guiling Xu, Yue-Hua Feng, Jinfeng Peng et al. (2023); cutoff-filter date 2023-07-22; doi:10.3390/agronomy13071940</summary>

```text
[8] Estimation Model of Rice Aboveground Dry Biomass Based on the Machine Learning and Hyperspectral Characteristic Parameters of the Canopy
    id: s2:02fcf2f8a1135c77d06af96901d510adedb25ea5
    date: 2023-07-22
    venue: Agronomy
    authors: Xiaoke Wang, Guiling Xu, Yue-Hua Feng, Jinfeng Peng, Yu-Qi Gao, Jie Li, Zhili Han, Qiangxin Luo
    abstract: Accurately estimating aboveground dry biomass (ADB) is crucial. The ADB of rice has primarily been estimated using vegetation indices with several discrete bands; nevertheless, these indices cannot take advantage of continuous bands available with hyperspectral remote sensing. This study analyzed the quantitative relationship between canopy hyperspectral characteristic parameters (HCPs) and the ADB of rice. Twenty HCPs were used, including red edge area (SDr), blue edge area (SDb), and others. The variable-screening methods involved stepwise regression (SR), a regression coefficient (RC), variable importance in projection (vip), and random forest (RF). Stepwise and partial least squares regression methods were employed with traditional linear regression as well as machine learning methods including random forest (RF), a support vector machine (SVM), a BP artificial neural network (BPNN), and an extreme learning machine. Whole- and screening-variable models were constructed to estimate rice ADB at jointing, booting, heading, and maturing stages and across growth stages. Screening-variable models include SVM models based on SR (SVM-sr), RF models based on vip (RF-vip), and others. The results show that the HCPs had a significant correlation with ADB containing elements in the red edge region, namely SDr, SDr/SDb, and (SDr − SDb)/(SDr + SDb) at each growth stage. In addition, the screening performance of vip and SR was better than that of RC and RF, and fewer variables were screened. Moreover, the HCPs of the red edge region were screened using different screening methods at each growth stage. Among them, SDr/SDb and (SDr − SDb)/(SDr + SDb) appeared frequently, indicating they are important. Furthermore, at each growth stage, ADB could be well-estimated using diverse models with the RF modeling method based on vip screening variables found to be the best modeling method for ADB estimation; the independent variables of the RF-vip model involved the (SDr − SDb)/(SDr + SD [...]
```
</details>

<details><summary>[9] **KEY** Edge effects on tree architecture exacerbate biomass loss of fragmented Amazonian forests — Matheus Henrique Nunes, M. Vaz, J. Camargo, W. Laurance et al. (2023); cutoff-filter date 2023-12-14; doi:10.1038/s41467-023-44004-5</summary>

```text
[9] Edge effects on tree architecture exacerbate biomass loss of fragmented Amazonian forests
    id: s2:447646f5a65281858a0607a61c9b401865a0876e
    date: 2023-12-14
    venue: Nature Communications
    authors: Matheus Henrique Nunes, M. Vaz, J. Camargo, W. Laurance, A. D. de Andrade, A. Vicentini, S. Laurance, P. Raumonen
    abstract: Habitat fragmentation could potentially affect tree architecture and allometry. Here, we use ground surveys of terrestrial LiDAR in Central Amazonia to explore the influence of forest edge effects on tree architecture and allometry, as well as forest biomass, 40 years after fragmentation. We find that young trees colonising the forest fragments have thicker branches and architectural traits that optimise for light capture, which result in 50% more woody volume than their counterparts of similar stem size and height in the forest interior. However, we observe a disproportionately lower height in some large trees, leading to a 30% decline in their woody volume. Despite the substantial wood production of colonising trees, the lower height of some large trees has resulted in a net loss of 6.0 Mg ha−1 of aboveground biomass – representing 2.3% of the aboveground biomass of edge forests. Our findings indicate a strong influence of edge effects on tree architecture and allometry, and uncover an overlooked factor that likely exacerbates carbon losses in fragmented forests.
```
</details>

<details><summary>[10] **KEY** Integrating Spaceborne Lidar Nasa’s Gedi With Imaging Sensors To Map Aboveground Biomass In Fragmented Tropical Forests — R. Leite, C. Silva, C. H. do Amaral, D. N. Cosenza et al. (2023); cutoff-filter date 2023-07-16; doi:10.1109/igarss52108.2023.10282548</summary>

```text
[10] Integrating Spaceborne Lidar Nasa’s Gedi With Imaging Sensors To Map Aboveground Biomass In Fragmented Tropical Forests
    id: s2:0ca959ab67ae82a9e0950ed681ba48f234731177
    date: 2023-07-16
    venue: IEEE International Geoscience and Remote Sensing Symposium
    authors: R. Leite, C. Silva, C. H. do Amaral, D. N. Cosenza, M. Schlickmann, Kleydson Diego Da Rocha, J. Xia, M. Mohan
    abstract: Human induced forest degradation can reduce aboveground biomass (AGB) and carbon stock of forest fragments. Developing approaches to assess these effects in highly-degraded tropical forests is necessary, especially at large scales. In this study, we developed a framework to upscale NASA’s GEDI spaceborne lidar AGB products using data from imaging sensors in the Brazilian Atlantic Forest – one of the most degraded and fragmented ecosystems in the world. A Random Forest model was trained using GEDI footprint level AGB as response and vegetation indices from Landsat 8/OLI and ALOS/PALSAR-2 images as predictors. The models were used to map and assess the AGB at the core and edge of 8783 fragments. The model had r = 0.83 and RMSE = 34.06 Mg/ha. The AGB in the fragments’ edges were significantly lower than in the fragments’ cores. The results demonstrated the potential of the developed framework to assess fragmentation effects on highly degraded tropical forest ecosystems.
```
</details>

<details><summary>Post-hoc automated audit — NON-AUTHORITATIVE; uses hidden benchmark annotations</summary>

- primary auditor: `reference_discriminator_recovered`; statuses {'H2': 'positive_or_present', 'H1': 'negative_or_absent'}; discriminative=True
- primary reasoning: H2 predicts that edge formation increases light and relaxes resource constraints, leading to higher aboveground biomass at edges under low climatic stress. H1 predicts that fragmentation increases stress and reduces resilience, so aboveground biomass should not be higher at edges, even under low stress.
- matched hidden reference discriminator: Resource-release account predicts fragmentation can increase light/resource availability and increase growth/recovery/resilience where stress penalties are weak.
- derived opposition call: `genuine`
- evidence attribution: `informative_evidence_found` — The retrieved literature directly addresses the proposition, with multiple papers comparing aboveground biomass at forest edges and interiors in fragmented forests. The assessor correctly identified strong contradiction based on explicit findings in the papers, showing the process worked as intended.
- disagreement flags: {'second_rater_vs_primary_discriminative': None, 'second_rater_vs_primary_status': None, 'retest_vs_primary_category': None, 'any': False}
</details>

**Human review** — `compatible_non_discriminative` · reviewer: Research Director · source: D045 · status: `first_pass_model_based_review` · genuinely discriminative: False · silence-as-null error: False · other fields not recorded

---

## #12 · `GP1-pfc_interhemispheric_architecture-X2`

**GP1-pfc_interhemispheric_architecture-X2** — case `pfc_interhemispheric_architecture`, node `X2`

> Interhemispheric transfer of spatial working-memory representations occurs selectively, rather than continuously, between the prefrontal cortices.

- generated from **H1** (Candidate A); abstraction: `mechanistic`
- generator's stated reason: The claim asserts selective interhemispheric transfer, so it implies that transfer is not constant but occurs under specific conditions.
- influence: **0.394** (rank 1 in case, 12 overall; cumulative 43%) — favours **H1**
- log-likelihood contribution: H1 +1.164, H2 +0.770
- removing it alone: evidence withheld → case log-odds +0.086 (ranking unchanged); node deleted → +0.086 (ranking unchanged)

**Hypotheses (as shown to the verifier)**

- **H1** (Candidate A): The hemispheres provide largely independent working-memory resources with a contralateral bias and selective interhemispheric transfer; bilateral-field advantages arise from partly separate capacity pools.
- **H2** (Candidate B): Working-memory representations can be carried by both hemispheres, providing robustness to unilateral disruption at some cost in duplicated capacity/precision.

**Verifier cross-hypothesis judgments** — P(X|H) combines these by noisy-OR

| hypothesis | origin? | direct edge | route via parent | P(X\|H) |
| --- | --- | --- | --- | --- |
| H1 | yes | `strongly_implied` | — | 0.950 |
| H2 | no | `neutral` | — | 0.500 |

- edge rationale, **H1** → node: Candidate A explicitly states that interhemispheric transfer is selective, matching the proposition directly.
- edge rationale, **H2** → node: Candidate B discusses bilateral representation and robustness but does not specify whether interhemispheric transfer is selective or continuous.

**Verifier evidence** — label used in score: `support` (log-LR +1.2)

- queries: `prefrontal cortex interhemispheric transfer`; `spatial working memory prefrontal cortex`
- assessor rationale: Record [1] directly reports that interhemispheric transfer of working memory traces occurs at specific times, associated with a shift in remembered location, rather than continuously. The evidence describes neural signatures and synchrony peaking around the time of transfer, supporting the proposition that transfer is selective. No other records provide direct evidence for or against the proposition.
- supporting spans cited by the assessor:
  - "Before the shift, spike rates and oscillatory power showed clear signatures of memory laterality. After the shift, the lateralization inverted, consistent with transfer of the memory trace from one hemisphere to the other."
  - "Around the time of transfer, synchrony between the two prefrontal hemispheres peaked in theta and low-gamma frequencies, with a directionality consistent with memory trace transfer."
- 10 papers shown; key papers: `s2:e79920699778f01e9beda8c051e9efad60f6d7cc`
- _The evidence assessor returns ONE label for the node from all papers shown; the method has no per-paper contribution. Key papers and spans are those the assessor cited._

<details><summary>[1] **KEY** Interhemispheric transfer of working memories — S. Brincat, Jacob A. Donoghue, Meredith K. Mahnke, Simon Kornblith et al. (2020); cutoff-filter date 2021-02-08; doi:10.1016/j.neuron.2021.01.016</summary>

```text
[1] Interhemispheric transfer of working memories
    id: s2:e79920699778f01e9beda8c051e9efad60f6d7cc
    date: 2020-08-12
    venue: bioRxiv (preprint)
    authors: S. Brincat, Jacob A. Donoghue, Meredith K. Mahnke, Simon Kornblith, Mikael Lundqvist, E. Miller
    abstract: Visual working memory (WM) storage is largely independent between the left and right visual hemifields/cerebral hemispheres, yet somehow WM feels seamless. We studied how WM is integrated across hemifields by recording neural activity bilaterally from lateral prefrontal cortex. An instructed saccade during the WM delay shifted the remembered location from one hemifield to the other. Before the shift, spike rates and oscillatory power showed clear signatures of memory laterality. After the shift, the lateralization inverted, consistent with transfer of the memory trace from one hemisphere to the other. Transferred traces initially used different neural ensembles from feedforward-induced ones but they converged at the end of the delay. Around the time of transfer, synchrony between the two prefrontal hemispheres peaked in theta and low-gamma frequencies, with a directionality consistent with memory trace transfer. This illustrates how dynamics between the two cortical hemispheres can stitch together WM traces across visual hemifields.
```
</details>

<details><summary>[2] Interhemispheric functional differences in prefrontal cortex of monkeys. — J. S. Stamm, A. Gadotti, Steven C. Rosen (1975); cutoff-filter date 1975-12-31; doi:10.1002/neu.480060108</summary>

```text
[2] Interhemispheric functional differences in prefrontal cortex of monkeys.
    id: s2:c4e6812cafb174ca165eb0144cb31a158ebfbb90
    date: 1975
    venue: Journal of Neurobiology
    authors: J. S. Stamm, A. Gadotti, Steven C. Rosen
    abstract: [no abstract available]
```
</details>

<details><summary>[3] A Selective Interhemispheric Transfer Callosal Deficit in Autism — J. Gruzelier, S. Stevens, K. Lewis (1996); cutoff-filter date 1996-12-31; doi:10.1016/0924-9338(96)88781-5</summary>

```text
[3] A Selective Interhemispheric Transfer Callosal Deficit in Autism
    id: s2:b056959a750e068764e6bb9c4a0ab663e9f55ac4
    date: 1996
    venue: European psychiatry
    authors: J. Gruzelier, S. Stevens, K. Lewis
    abstract: [no abstract available]
```
</details>

<details><summary>[4] Interhemispheric visuo-motor integration in humans: the role of the superior parietal cortex. — M. Iacoboni, E. Zaidel (2004); cutoff-filter date 2004-12-31; doi:10.1016/j.neuropsychologia.2003.10.007</summary>

```text
[4] Interhemispheric visuo-motor integration in humans: the role of the superior parietal cortex.
    id: s2:ab0bcc9369f101e5b51dc7cc2c6504ac0da902f5
    date: 2004
    venue: Neuropsychologia
    authors: M. Iacoboni, E. Zaidel
    abstract: [no abstract available]
```
</details>

<details><summary>[5] Cortical regions contributing to the anterior commissure in man — Gabriella Di Virgilio, Stephanie Clarke, G. Pizzolato, T. Schaffner (1999); cutoff-filter date 1999-12-31; doi:10.1007/s002210050593</summary>

```text
[5] Cortical regions contributing to the anterior commissure in man
    id: s2:2d5909a1d89b5a7f5261b4207c7a83a2a6eb0542
    date: 1999
    venue: Experimental Brain Research
    authors: Gabriella Di Virgilio, Stephanie Clarke, G. Pizzolato, T. Schaffner
    abstract: [no abstract available]
```
</details>

<details><summary>[6] Frontal-striatal disconnection disrupts cognitive performance of the frontal-type in the rat. — S. Dunnett, A. Meldrum, J. Muir (2005); cutoff-filter date 2005-12-31; doi:10.1016/j.neuroscience.2005.07.033</summary>

```text
[6] Frontal-striatal disconnection disrupts cognitive performance of the frontal-type in the rat.
    id: s2:effb84bab05e6da21de63f8f49f26458a8122899
    date: 2005
    venue: Neuroscience
    authors: S. Dunnett, A. Meldrum, J. Muir
    abstract: [no abstract available]
```
</details>

<details><summary>[7] Dissociation apraxia secondary to right premotor stroke. — S. Luzzi, M. Piccirilli, Martina Pesallaccia, Katia Fabi et al. (2010); cutoff-filter date 2010-12-31; doi:10.1016/j.neuropsychologia.2009.08.010</summary>

```text
[7] Dissociation apraxia secondary to right premotor stroke.
    id: s2:4cb61662ed8f86495876f1d624ac58ffd4b1a5bc
    date: 2010
    venue: Neuropsychologia
    authors: S. Luzzi, M. Piccirilli, Martina Pesallaccia, Katia Fabi, L. Provinciali
    abstract: [no abstract available]
```
</details>

<details><summary>[8] Skeletomotor subsystems. — R. Sieb (1987); cutoff-filter date 1987-12-31; doi:10.1016/0306-9877(87)90207-6</summary>

```text
[8] Skeletomotor subsystems.
    id: s2:d97ab306ce6c78c972977e1d40fc438188df598d
    date: 1987
    venue: Medical Hypotheses
    authors: R. Sieb
    abstract: [no abstract available]
```
</details>

<details><summary>[9] Electroconvulsive Therapy Regulates the Interhemispheric Functional Connectivity of the Dorsomedial Prefrontal Cortex in Depressive Patients: Evidence from 2 Independent Samples — Lou-feng Zhang, Yuan-Yuan Guo, Tong-Jian Bai, Mei-Dan Zu et al. (2024); cutoff-filter date 2024-10-05; doi:10.62641/aep.v52i5.1675</summary>

```text
[9] Electroconvulsive Therapy Regulates the Interhemispheric Functional Connectivity of the Dorsomedial Prefrontal Cortex in Depressive Patients: Evidence from 2 Independent Samples
    id: s2:a568c7ddd016fb721d7ef25df87d784dc2fbd16f
    date: 2024-10-01
    venue: Actas espanolas de psiquiatria
    authors: Lou-feng Zhang, Yuan-Yuan Guo, Tong-Jian Bai, Mei-Dan Zu, Qiang Wei, Yue Wu, G. Ji, Huaming Lv
    abstract: Background: The dorsomedial prefrontal cortex (dmPFC) is considered a crucial node in emotional and cognitive processes. Voxel-mirrored homotopic connectivity (VMHC) is a validated methodology for investigating interhemispheric coordination. This study aims to elucidate the effects of electroconvulsive therapy (ECT) on the interhemispheric connectivity of the dmPFC in patients with depression, using VMHC as a measure of bilateral neural coordination. Methods: Thirty-three patients with depression, screened at the University of Science and Technology of China (USTC), and thirty-five patients with depression, screened at Anhui Medical University (AHMU), were selected as the subjects of this study. VMHC was employed to investigate the effects of ECT on bilateral hemispheric functional connectivity. The Hamilton Depression Rating Scale (HAMD) was used to assess depressive symptoms, and the relationships between changes in HAMD scores and VMHC values were examined. Results: Following ECT, the depressive symptoms of all participants decreased (p < 0.001). The VMHC values in the dmPFC were significantly increased in both groups after ECT (p < 0.01). No significant correlation was found between the increasing VMHC values in the dmPFC and the changes in HAMD scores in depressed patients (p > 0.05). Conclusion: These results show that ECT regulates interhemispheric functional connectivity in depressed patients, and significantly increases the VMHC values in the dmPFC. Our findings may provide a useful method for optimizing the treatment of depression.
```
</details>

<details><summary>[10] Online stimulation of the prefrontal cortex during practice increases motor variability and modulates later cognitive transfer: a randomized, double-blinded and sham-controlled tDCS study — Nisha Maria Prabhu, Nico Lehmann, E. Kaminski, Notger G. Müller et al. (2024); cutoff-filter date 2024-08-29; doi:10.1038/s41598-024-70857-x</summary>

```text
[10] Online stimulation of the prefrontal cortex during practice increases motor variability and modulates later cognitive transfer: a randomized, double-blinded and sham-controlled tDCS study
    id: s2:e67e8221f2ffc26c852b1bbc2aabd06a20fc4bda
    date: 2024-08-29
    venue: Scientific Reports
    authors: Nisha Maria Prabhu, Nico Lehmann, E. Kaminski, Notger G. Müller, Marco Taubert
    abstract: The benefits of learning a motor skill extend to improved task-specific cognitive abilities. The mechanistic underpinnings of this motor-cognition relationship potentially rely on overlapping neural resources involved in both processes, an assumption lacking causal evidence. We hypothesize that interfering with prefrontal networks would inhibit concurrent motor skill performance, long-term learning and associated cognitive functions dependent on similar networks (transfer). We conducted a randomised, double-blinded, sham-controlled brain stimulation study using transcranial direct current stimulation (tDCS) in young adults spanning over three weeks to assess the role of the prefrontal regions in learning a complex balance task and long-term cognitive performance. Balance training combined with active tDCS led to higher performance variability in the trained task as compared to the sham group, impacting the process of learning a complex task without affecting the learning rate. Furthermore, active tDCS also positively influenced performance in untrained motor and cognitive tasks. The findings of this study help ascertaining the networks directly involved in learning a complex motor task and its implications on cognitive function. Hence, opening up the possibility of harnessing the observed frontal networks involved in resource mobilization in instances of aging, brain lesion/injury or dysfunction.
```
</details>

<details><summary>Post-hoc automated audit — NON-AUTHORITATIVE; uses hidden benchmark annotations</summary>

- primary auditor: `silence_as_null_error`; statuses {'H1': 'positive_or_present', 'H2': 'indeterminate'}; discriminative=False
- primary reasoning: H1 explicitly posits selective (not continuous) interhemispheric transfer, so it predicts this proposition should hold. H2 is silent on the nature or selectivity of interhemispheric transfer, focusing instead on redundancy and robustness, so it makes no commitment either way.
- derived opposition call: `one_sided_silence_labelled_neutral`
- evidence attribution: `informative_evidence_found` — The retrieval system surfaced a paper (Record [1]) that directly addresses the proposition, providing evidence that interhemispheric transfer of spatial working memory in the prefrontal cortex occurs selectively rather than continuously. The assessor correctly identified and used this evidence. The queries were appropriate and the process worked as intended.
- disagreement flags: {'second_rater_vs_primary_discriminative': None, 'second_rater_vs_primary_status': None, 'retest_vs_primary_category': None, 'any': False}
</details>

**Human review** — `compatible_non_discriminative` · reviewer: Research Director · source: D045 · status: `first_pass_model_based_review` · genuinely discriminative: False · silence-as-null error: False · other fields not recorded

---

## #13 · `GP1-fly_wing_constraint_vs_selection-X2`

**GP1-fly_wing_constraint_vs_selection-X2** — case `fly_wing_constraint_vs_selection`, node `X2`

> Correlational or stabilizing selection on wing shape generates covariance in developmental and mutational variation along the same axes favored by long-term evolutionary divergence.

- generated from **H2** (Candidate A); abstraction: `mechanistic`
- generator's stated reason: The claim asserts that selection molds both developmental bias and divergence, so selection-driven covariance should align with evolutionary axes.
- influence: **0.302** (rank 1 in case, 13 overall; cumulative 45%) — favours **H2**
- log-likelihood contribution: H2 +0.480, H1 +0.178
- removing it alone: evidence withheld → case log-odds +0.007 (ranking unchanged); node deleted → +0.007 (ranking unchanged)

**Hypotheses (as shown to the verifier)**

- **H1** (Candidate B): Macroevolution preferentially proceeds along directions of abundant developmental/genetic variation because the structure of available variation constrains which phenotypic directions can evolve readily.
- **H2** (Candidate A): Persistent correlational/stabilizing selection shapes developmental and mutational covariance; developmental bias and long-term divergence align because both are molded by the same fitness/allometric structure rather than because variation mechanically constrains evolutionary directions.

**Verifier cross-hypothesis judgments** — P(X|H) combines these by noisy-OR

| hypothesis | origin? | direct edge | route via parent | P(X\|H) |
| --- | --- | --- | --- | --- |
| H2 | yes | `strongly_implied` | — | 0.950 |
| H1 | no | `unlikely` | — | 0.300 |

- edge rationale, **H2** → node: If persistent correlational/stabilizing selection shapes both developmental/mutational covariance and long-term divergence, then covariance in variation should align with the axes favored by selection, as the proposition states.
- edge rationale, **H1** → node: If macroevolution proceeds along directions of abundant variation due to developmental constraints, then covariance in variation is expected to precede and constrain divergence, not be generated by selection along the axes of divergence as the proposition claims.

**Verifier evidence** — label used in score: `weak_support` (log-LR +0.5)

- queries: `wing shape developmental covariance`; `wing shape mutational variation divergence`
- assessor rationale: Record [2] shows that developmental bias in wing shape predicts both mutational and individual variation, as well as macroevolutionary divergence, which is consistent with the proposition but does not explicitly link selection to covariance generation. Record [9] demonstrates that artificial selection on wing shape vectors aligns genetic and phenotypic variation along major axes, suggesting that selection can generate covariance in developmental and mutational variation along axes favored by divergence. However, neither record directly states that correlational or stabilizing selection is the causal mechanism, so the support is weak.
- supporting spans cited by the assessor:
  - "Here, we estimate developmental bias in insect wings and show that it predicts variation among individuals, the effects of mutation, as well as deep macroevolutionary divergence that unfolded over ~60 My. This suggests that developmental biases can be strong predictors of diversification on both short and long evolutionary timescales but also challenges the classic view of strong relationships between genetic variation and divergence as solely reflecting constraints on adaptation."
  - "We demonstrate that multivariate wing shape changes associated with these genes are aligned with major axes of phenotypic and genetic variation in natural populations. Following seven generations of artificial selection along the ds shape change vector, we observe genetic differentiation of variants in ds and genomic regions containing other genes in the hippo signaling pathway. This suggests a shared direction of effects within a developmental network. We also performed artificial selection with the emc shape change vector, which is not a part of the hippo signaling network, but showed a largely shared direction of effects. The response to selection along the emc vector was similar to that of ds, suggesting that the available genetic diversity of a population, summarized by the genetic (co)variance matrix (G), influenced alleles captured by selection."
- 10 papers shown; key papers: `s2:113b6ffdac2e15b1687d3dd611c685b731e353fc`, `s2:a08442400ce65647ef6c048a5c24bafcb8192676`
- _The evidence assessor returns ONE label for the node from all papers shown; the method has no per-paper contribution. Key papers and spans are those the assessor cited._

<details><summary>[1] Describing compartmentalization in the hind wing of the hispid beetle Brontispa longissima — Bryan George D. Belleza, C. Demayo (2014); cutoff-filter date 2014-12-31; https://www.semanticscholar.org/paper/9bb41cb4d32b55ffdce8fbad8f0023bea43eb2e1</summary>

```text
[1] Describing compartmentalization in the hind wing of the hispid beetle Brontispa longissima
    id: s2:9bb41cb4d32b55ffdce8fbad8f0023bea43eb2e1
    date: 2014
    venue: European Journal of Zoological Research
    authors: Bryan George D. Belleza, C. Demayo
    abstract: [no abstract available]
```
</details>

<details><summary>[2] **KEY** Developmental bias predicts 60 million years of wing shape evolution — P. Rohner, D. Berger (2023); cutoff-filter date 2023-05-01; doi:10.1073/pnas.2211210120</summary>

```text
[2] Developmental bias predicts 60 million years of wing shape evolution
    id: s2:113b6ffdac2e15b1687d3dd611c685b731e353fc
    date: 2023-05-01
    venue: Proceedings of the National Academy of Sciences of the United States of America
    authors: P. Rohner, D. Berger
    abstract: Significance Perturbation of development often has nonrandom effects on trait expression. Such developmental bias is thought to constrain adaptation by making evolution more likely to proceed in certain directions. Developmental biases can evolve, but what role natural selection plays in this process remains highly controversial. Here, we estimate developmental bias in insect wings and show that it predicts variation among individuals, the effects of mutation, as well as deep macroevolutionary divergence that unfolded over ~60 My. This suggests that developmental biases can be strong predictors of diversification on both short and long evolutionary timescales but also challenges the classic view of strong relationships between genetic variation and divergence as solely reflecting constraints on adaptation.
```
</details>

<details><summary>[3] Melanic morphs of Bactrocera dorsalis possess distinct developmental time, weight, and wing size and shape — Nelson L. Mwando, S. B. S. Baleba, S. Ndlela, S. A. Mohamed (2023); cutoff-filter date 2023-04-18; doi:10.1111/eea.13303</summary>

```text
[3] Melanic morphs of Bactrocera dorsalis possess distinct developmental time, weight, and wing size and shape
    id: s2:dc17eaba4e91467a4cad0fb6407eeb8756103dda
    date: 2023-04-18
    venue: Entomologia Experimentalis et Applicata
    authors: Nelson L. Mwando, S. B. S. Baleba, S. Ndlela, S. A. Mohamed
    abstract: The scutum of oriental fruit fly, Bactrocera dorsalis (Hendel) (Diptera: Tephritidae), shows a high degree of variability in its colouration, which goes from black to red‐brown. Such variation depicts different levels of melanin production in these individuals. In insects, melanization can have an effect on their fitness parameters, which could consequently impact the insect's adaptive responses. Here, we asked whether the progeny produced by B. dorsalis individuals with different scutum colouration (melanic morphs) would differ in their developmental time, weight, and wing size and shape. To address this, we followed eggs produced by each B. dorsalis melanic morph by recording their pupation time, emergence time, and larval (second instar), pupal, and adult weights. Also, using landmark‐based geometric morphometric analysis, we assessed the variation in wing size and shape of the adults obtained from each parental melanic morphs of B. dorsalis. We found that larvae produced by adults with the darkest scutum exhibited faster development and weighed more than those produced by adults with brown scutum. At the adult stage, individuals from parents with darker and brown scutum had a reduced weight and wing size (length, width, area, and centroid size) than those from parents with moderate melanin production. We also found significant wing shape variation across the four melanic morphs. Our study suggests that melanisation in the scutum of B. dorsalis has a fitness gain in the preimaginal stages of this fly. In the adult stage, however, the amount of melanin in the scutum has a fitness cost. This suggests that in B. dorsalis, there is a potential trade‐off between melanin production and fitness parameters, which could have implications for adaptive responses such as thermoregulation, flight, and dispersal, and consequently for its management.
```
</details>

<details><summary>[4] Codivergence but Limited Covariance of Wing Shape and Calling Song Structure in Field Crickets (Gryllus) — Thomas Blankers, R. Block, R. M. Hennig (2018); cutoff-filter date 2018-06-01; doi:10.1007/s11692-017-9439-2</summary>

```text
[4] Codivergence but Limited Covariance of Wing Shape and Calling Song Structure in Field Crickets (Gryllus)
    id: s2:c01419c8f667daa96711dbd3ab06a1107dad5d1a
    date: 2018-06-01
    venue: Evolutionary biology
    authors: Thomas Blankers, R. Block, R. M. Hennig
    abstract: [no abstract available]
    note: merged with 1 other version(s) of the same work
```
</details>

<details><summary>[5] Review of: Wing shape evolution is not constrained by ancestral genetic covariances in the invasive Drosophila suzukii. Round#1/Reviewer#1 — authors n/a (2024); cutoff-filter date 2024-03-26; doi:10.24072/pci.evolbiol.100789.rev11</summary>

```text
[5] Review of: Wing shape evolution is not constrained by ancestral genetic covariances in the invasive Drosophila suzukii. Round#1/Reviewer#1
    id: s2:61a379c432fe5a252deac4c153178752bc613e34
    date: 2024-03-26
    venue: Peer Community in Evolutionary Biology
    authors: unknown
    abstract: [no abstract available]
    note: possibly the same work as s2:25428bd4865ef532b52129e25bbbfb23a3b1c95f, s2:849f6528fc158675ed38f7bf82a6323f03aa80c9
```
</details>

<details><summary>[6] Review of: Wing shape evolution is not constrained by ancestral genetic covariances in the invasive Drosophila suzukii. Round#1/Reviewer#2 — authors n/a (2024); cutoff-filter date 2024-03-26; doi:10.24072/pci.evolbiol.100789.rev12</summary>

```text
[6] Review of: Wing shape evolution is not constrained by ancestral genetic covariances in the invasive Drosophila suzukii. Round#1/Reviewer#2
    id: s2:25428bd4865ef532b52129e25bbbfb23a3b1c95f
    date: 2024-03-26
    venue: Peer Community in Evolutionary Biology
    authors: unknown
    abstract: [no abstract available]
    note: possibly the same work as s2:61a379c432fe5a252deac4c153178752bc613e34, s2:849f6528fc158675ed38f7bf82a6323f03aa80c9
```
</details>

<details><summary>[7] Decision Revise: Wing shape evolution is not constrained by ancestral genetic covariances in the invasive Drosophila suzukii. Round#1 — authors n/a (2024); cutoff-filter date 2024-05-27; doi:10.24072/pci.evolbiol.100789.d1</summary>

```text
[7] Decision Revise: Wing shape evolution is not constrained by ancestral genetic covariances in the invasive Drosophila suzukii. Round#1
    id: s2:849f6528fc158675ed38f7bf82a6323f03aa80c9
    date: 2024-05-27
    venue: Peer Community in Evolutionary Biology
    authors: unknown
    abstract: [no abstract available]
    note: possibly the same work as s2:61a379c432fe5a252deac4c153178752bc613e34, s2:25428bd4865ef532b52129e25bbbfb23a3b1c95f
```
</details>

<details><summary>[8] Lack of response to artificial selection on developmental stability of partial wing shape components in Drosophila melanogaster — Masahiro Tsujino, Kazuo H. Takahashi (2014); cutoff-filter date 2014-04-18; doi:10.1007/s10709-014-9765-6</summary>

```text
[8] Lack of response to artificial selection on developmental stability of partial wing shape components in Drosophila melanogaster
    id: s2:4bf5310c8b2d3796aadb4609194adff19d196b09
    date: 2014-04-18
    venue: Genetica
    authors: Masahiro Tsujino, Kazuo H. Takahashi
    abstract: [no abstract available]
    note: merged with 1 other version(s) of the same work
```
</details>

<details><summary>[9] **KEY** Complexities of recapitulating polygenic effects in natural populations: replication of genetic effects on wing shape in artificially selected and wild caught populations of Drosophila melanogaster — Katie Pelletier, William R. Pitchers, Anna E Mammel, Emmalee J. Northrop-Albrecht et al. (2023); cutoff-filter date 2023-03-18; doi:10.1101/2022.05.12.491649</summary>

```text
[9] Complexities of recapitulating polygenic effects in natural populations: replication of genetic effects on wing shape in artificially selected and wild caught populations of Drosophila melanogaster
    id: s2:a08442400ce65647ef6c048a5c24bafcb8192676
    date: 2023-03-18
    venue: bioRxiv (preprint)
    authors: Katie Pelletier, William R. Pitchers, Anna E Mammel, Emmalee J. Northrop-Albrecht, E. Márquez, R. Moscarella, D. Houle, I. Dworkin
    abstract: Identifying the genetic architecture of complex traits is important to many geneticists, including those interested in human disease, plant and animal breeding, and evolutionary genetics. Advances in sequencing technology and statistical methods for genome-wide association studies (GWAS) have allowed for the identification of more variants with smaller effect sizes, however, many of these identified polymorphisms fail to be replicated in subsequent studies. In addition to sampling variation, this failure to replicate reflects the complexities introduced by factors including environmental variation, genetic background, and differences in allele frequencies among populations. Using Drosophila melanogaster wing shape, we ask if we can replicate allelic effects of polymorphisms first identified in a GWAS (Pitchers et al. 2019) in three genes: dachsous (ds), extra-macrochaete (emc) and neuralized (neur), using artificial selection in the lab, and bulk segregant mapping in natural populations. We demonstrate that multivariate wing shape changes associated with these genes are aligned with major axes of phenotypic and genetic variation in natural populations. Following seven generations of artificial selection along the ds shape change vector, we observe genetic differentiation of variants in ds and genomic regions containing other genes in the hippo signaling pathway. This suggests a shared direction of effects within a developmental network. We also performed artificial selection with the emc shape change vector, which is not a part of the hippo signaling network, but showed a largely shared direction of effects. The response to selection along the emc vector was similar to that of ds, suggesting that the available genetic diversity of a population, summarized by the genetic (co)variance matrix (G), influenced alleles captured by selection. Despite the success with artificial selection, bulk segregant analysis using natural populations did not detect these same variants, [...]
```
</details>

<details><summary>[10] Wing Shape Variation between Terrestrial and Coastal Populations of the Invasive Box Tree Moth, Cydalima perspectalis, in Croatia — D. Lemić, Helena Viric Gasparic, Patricija Majcenic, Ivana Pajač Živković et al. (2023); cutoff-filter date 2023-09-28; doi:10.3390/ani13193044</summary>

```text
[10] Wing Shape Variation between Terrestrial and Coastal Populations of the Invasive Box Tree Moth, Cydalima perspectalis, in Croatia
    id: s2:da64b635ebd970a2a922d22bb35d398a1a387627
    date: 2023-09-28
    venue: Animals
    authors: D. Lemić, Helena Viric Gasparic, Patricija Majcenic, Ivana Pajač Živković, Mario Bjeliš, Manuel J. Suazo, Margarita Correa, Jordan Hernández
    abstract: Featured Application Use of Geometric morphometrics tools to understand invasiveness patterns of invasive species. Simple Summary The box tree moth is an invasive species that originated in Asia. Its presence causes damage by defoliating plants, to the point of causing their death. The presence of silk barriers and threads, covering plants during intense attacks, allows for species recognition. Cydalima perspectalis was first detected in 2007 in Germany and the Netherlands, after which it spread widely to other regions of Europe. In Croatia, its presence was first recorded in 2012 and it caused notable damage in 2013. This study analyzed the wing morphological variability of C. perspectalis in Croatia and its invasive character. This technique uses a mathematical approach in which the combination of geometry and statistics is essential to understand the morphology of invasive organisms; principally, how the wings adapt to allow the moth to colonize new environments. To achieve this, 269 moths from different areas were collected, and the wings of both males and females were evaluated. Significant differences in wing shape were found between terrestrial and coastal populations, with no sexual dimorphism established. The implications of this variability with regard to the invasive capacity and spread of the species are discussed. Abstract The box tree moth (Cydalima perspectalis Walker, 1859; Lepidoptera: Crambidae) is an invasive species naturally distributed in Asia. The caterpillars in all developmental stages cause damage through defoliation of plants, and ultimately the death of the plant itself may occur. It is possible to recognize this species by its silk barriers and threads, and in the case of an intense attack, the entire plant will be covered with them. In Europe, this species’ presence was first recorded in 2007 in Germany and the Netherlands, and it is now widely distributed. In Croatia, its existence was first recorded in 2012, in Istria, while substanti [...]
```
</details>

<details><summary>Post-hoc automated audit — NON-AUTHORITATIVE; uses hidden benchmark annotations</summary>

- primary auditor: `silence_as_null_error`; statuses {'H2': 'positive_or_present', 'H1': 'indeterminate'}; discriminative=False
- primary reasoning: H2 directly predicts that correlational/stabilizing selection molds developmental and mutational covariance to align with axes favored by divergence. H1 is silent on whether selection shapes covariance; it only posits that available variation constrains evolution, not that selection generates covariance along favored axes.
- derived opposition call: `manufactured_from_silence`
- evidence attribution: `generic_compatibility_only` — The retrieved papers are topically relevant and discuss developmental bias, mutational variation, and evolutionary divergence in wing shape, but they do not directly test or demonstrate that correlational or stabilizing selection generates covariance along axes favored by long-term divergence. The assessor treated these as weak support, but the evidence is only generically compatible with the proposition, not specific to its causal claim.
- disagreement flags: {'second_rater_vs_primary_discriminative': None, 'second_rater_vs_primary_status': None, 'retest_vs_primary_category': None, 'any': False}
</details>

**Human review** — `silence_as_null_error` · reviewer: Research Director · source: D045 · status: `first_pass_model_based_review` · genuinely discriminative: False · silence-as-null error: True · other fields not recorded

---

## #14 · `GP1-pfc_storage_vs_control-X6`

**GP1-pfc_storage_vs_control-X6** — case `pfc_storage_vs_control`, node `X6`

> Regions of prefrontal cortex are more likely to show signals related to attentional control or prioritization than to the specific content of visual working memory representations.

- generated from **H2** (Candidate B); abstraction: `class`
- generator's stated reason: If the claim is true for PFC in general, then across studies, PFC regions should more often reflect control processes than direct storage of mnemonic content.
- influence: **0.302** (rank 2 in case, 14 overall; cumulative 46%) — favours **H2**
- log-likelihood contribution: H1 +0.178, H2 +0.480
- removing it alone: evidence withheld → case log-odds +1.516 (ranking unchanged); node deleted → +0.837 (ranking unchanged)

**Hypotheses (as shown to the verifier)**

- **H1** (Candidate A): Prefrontal persistent activity is itself a substrate for working-memory storage; disrupting the relevant PFC population therefore disrupts the stored mnemonic representation.
- **H2** (Candidate B): PFC primarily controls, prioritizes, or allocates resources to working-memory representations maintained in sensory/posterior regions rather than directly storing the mnemonic content itself.

**Verifier cross-hypothesis judgments** — P(X|H) combines these by noisy-OR

| hypothesis | origin? | direct edge | route via parent | P(X\|H) |
| --- | --- | --- | --- | --- |
| H1 | no | `unlikely` | — | 0.300 |
| H2 | yes | `strongly_implied` | — | 0.950 |

- edge rationale, **H1** → node: If PFC persistent activity directly stores mnemonic content, it is less likely that PFC signals are primarily related to attentional control or prioritization rather than content.
- edge rationale, **H2** → node: If PFC's main role is to control or prioritize representations stored elsewhere, it is nearly certain that PFC signals will reflect attentional control or prioritization rather than specific content.

**Verifier evidence** — label used in score: `weak_support` (log-LR +0.5)

- queries: `prefrontal cortex attentional control signals`; `prefrontal cortex visual working memory`
- assessor rationale: Several records directly state that prefrontal cortex regions are involved in attentional control, top-down regulation, and goal-directed behavior, supporting the proposition that PFC is more likely to show signals related to attentional control or prioritization. However, only one record (6) directly addresses the encoding of specific content in PFC, and it reports that feature-selective representations are present in prefrontal areas, challenging a strict segregation. Thus, while most records support the attentional control aspect, evidence for the relative likelihood compared to content signals is weak and not comprehensive.
- supporting spans cited by the assessor:
  - "We review how PFC-connected thalamic nuclei likely contribute to all aspects of cognitive control: from the processing of information on internal states and goals, facilitating its interactions with mnemonic information and learned values of stimuli and actions, to their influence on high-level cognitive processes, attentional allocation and goal-directed behavior."
  - "The prefrontal cortex (PFC) governs top–down control of attention and is known to be vulnerable in aging."
  - "Whole-brain voxel-wise analyses showed that symptom improvement was predicted by enhanced pre-treatment activity in the presence of emotional face distractors in the dorsal anterior cingulate cortex and dorsal medial prefrontal cortex."
  - "Recent studies suggest that attention samples space rhythmically through oscillatory interactions in the frontoparietal network. However, the precise mechanism through which the prefrontal cortex, at the source of attention control signals, organizes this rhythmic exploration of space remains unknown."
  - "These results are discussed in the context of exploration and exploitation strategies and prefrontal top-down attentional control."
- 10 papers shown; key papers: `s2:101ee9d1f637a879d2a13f764d079dffce256d36`, `s2:2759af28ca1fe466a7f8d66ef11f3a3ef89ea47a`, `s2:4beafdc6d162b7db26e1adf8d008dd95a3490c3d`, `s2:8e0f5181bf64bcfb66b09186cb2482d1365fc18c`
- _The evidence assessor returns ONE label for the node from all papers shown; the method has no per-paper contribution. Key papers and spans are those the assessor cited._

<details><summary>[1] **KEY** Disentangling the influences of multiple thalamic nuclei on prefrontal cortex and cognitive control — Jessica M. Phillips, Niranjan A. Kambi, Michelle J. Redinbaugh, S. Mohanta et al. (2021); cutoff-filter date 2021-06-30; doi:10.1016/j.neubiorev.2021.06.042</summary>

```text
[1] Disentangling the influences of multiple thalamic nuclei on prefrontal cortex and cognitive control
    id: s2:8e0f5181bf64bcfb66b09186cb2482d1365fc18c
    date: 2021-06-30
    venue: Neuroscience and Biobehavioral Reviews
    authors: Jessica M. Phillips, Niranjan A. Kambi, Michelle J. Redinbaugh, S. Mohanta, Y. Saalmann
    abstract: The prefrontal cortex (PFC) has a complex relationship with the thalamus, involving many nuclei which occupy predominantly medial zones along its anterior-to-posterior extent. Thalamocortical neurons in most of these nuclei are modulated by the affective and cognitive signals which funnel through the basal ganglia. We review how PFC-connected thalamic nuclei likely contribute to all aspects of cognitive control: from the processing of information on internal states and goals, facilitating its interactions with mnemonic information and learned values of stimuli and actions, to their influence on high-level cognitive processes, attentional allocation and goal-directed behavior. This includes contributions to transformations such as rule-to-choice (parvocellular mediodorsal nucleus), value-to-choice (magnocellular mediodorsal nucleus), mnemonic-to-choice (anteromedial nucleus) and sensory-to-choice (medial pulvinar). Common mechanisms appear to be thalamic modulation of cortical gain and cortico-cortical functional connectivity. The anatomy also implies a unique role for medial PFC in modulating processing in thalamocortical circuits involving other orbital and lateral PFC regions. We further discuss how cortico-basal ganglia circuits may provide a mechanism through which PFC controls cortico-cortical functional connectivity.
```
</details>

<details><summary>[2] Anterior Cingulate Cortex Cells Identify Process-Specific Errors of Attentional Control Prior to Transient Prefrontal-Cingulate Inhibition. — Chen Shen, S. Ardid, Daniel Kaping, S. Westendorff et al. (2015); cutoff-filter date 2015-08-01; doi:10.1093/cercor/bhu028</summary>

```text
[2] Anterior Cingulate Cortex Cells Identify Process-Specific Errors of Attentional Control Prior to Transient Prefrontal-Cingulate Inhibition.
    id: s2:56b22b61adeacbab5a5278d1edf5181386008859
    date: 2015-08-01
    venue: Cerebral Cortex
    authors: Chen Shen, S. Ardid, Daniel Kaping, S. Westendorff, S. Everling, T. Womelsdorf
    abstract: [no abstract available]
```
</details>

<details><summary>[3] Lesions of prefrontal cortex reduce attentional modulation of neuronal responses and synchrony in V4 — G. Gregoriou, A. Rossi, Leslie G. Ungerleider, R. Desimone (2014); cutoff-filter date 2014-06-15; doi:10.1038/nn.3742</summary>

```text
[3] Lesions of prefrontal cortex reduce attentional modulation of neuronal responses and synchrony in V4
    id: s2:61fd55edad2ba939f6795b99db3a621cecf281a1
    date: 2014-06-01
    venue: Nature Neuroscience
    authors: G. Gregoriou, A. Rossi, Leslie G. Ungerleider, R. Desimone
    abstract: It is widely held that the frontal eye field (FEF) in prefrontal cortex (PFC) modulates processing in visual cortex with attention, although the evidence that it is necessary is equivocal. To help identify critical sources of attentional feedback to area V4, we surgically removed the entire lateral PFC, including the FEF, in one hemisphere and transected the corpus callosum and anterior commissure in two macaques. This deprived V4 of PFC input in one hemisphere while keeping the other hemisphere intact. In the absence of PFC, attentional effects on neuronal responses and synchrony in V4 were substantially reduced and the remaining effects of attention were delayed in time, indicating a critical role for PFC. Conversely, distracters captured attention and influenced V4 responses. However, because the effects of attention in V4 were not eliminated by PFC lesions, other sources of top-down attentional control signals to visual cortex must exist outside of PFC.
```
</details>

<details><summary>[4] Triple Dissociation of Attention and Decision Computations across Prefrontal Cortex — L. Hunt, W. M. Nishantha Malalasekera, Archy O. de Berker, B. Miranda et al. (2017); cutoff-filter date 2018-09-19; doi:10.1038/s41593-018-0239-5</summary>

```text
[4] Triple Dissociation of Attention and Decision Computations across Prefrontal Cortex
    id: s2:53410f3ff2dd23a945267bed48000e08a33983f1
    date: 2017-08-01
    venue: Nature Neuroscience
    authors: L. Hunt, W. M. Nishantha Malalasekera, Archy O. de Berker, B. Miranda, S. Farmer, T. Behrens, S. Kennerley
    abstract: Naturalistic decision-making typically involves sequential deployment of attention to choice alternatives to gather information before a decision is made. Attention filters how information enters decision circuits, thus implying that attentional control may shape how decision computations unfold. We recorded neuronal activity from three subregions of the prefrontal cortex (PFC) while monkeys performed an attention-guided decision-making task. From the first saccade to decision-relevant information, a triple dissociation of decision- and attention-related computations emerged in parallel across PFC subregions. During subsequent saccades, orbitofrontal cortex activity reflected the value comparison between currently and previously attended information. In contrast, the anterior cingulate cortex carried several signals reflecting belief updating in light of newly attended information, the integration of evidence to a decision bound and an emerging plan for what action to choose. Our findings show how anatomically dissociable PFC representations evolve during attention-guided information search, supporting computations critical for value-guided choice. Hunt, Malalasekera et al. recorded populations of prefrontal neurons from monkeys performing a visual attention-guided-choice task. The results revealed that distinct computations in three PFC subregions as information was sampled guided the eventual decision.
```
</details>

<details><summary>[5] **KEY** Chemogenetic inhibition of prefrontal projection neurons constrain top-down control of attention in young but not aged rats — Michael R. Duggan, Surbhi Joshi, J. Strupp, V. Parikh (2021); cutoff-filter date 2021-07-10; doi:10.1007/s00429-021-02336-2</summary>

```text
[5] Chemogenetic inhibition of prefrontal projection neurons constrain top-down control of attention in young but not aged rats
    id: s2:101ee9d1f637a879d2a13f764d079dffce256d36
    date: 2021-07-10
    venue: Brain Structure and Function
    authors: Michael R. Duggan, Surbhi Joshi, J. Strupp, V. Parikh
    abstract: The prefrontal cortex (PFC) governs top–down control of attention and is known to be vulnerable in aging. Cortical reorganization with increased PFC recruitment is suggested to account for functional compensation. Here, we hypothesized that reduced PFC output would exert differential effects on attentional capacities in young and aged rats, with the latter exhibiting a more robust decline in performance. A chemogenetic approach involving designer receptors exclusively activated by designer drugs was utilized to determine the impact of silencing PFC projection neurons in rats performing an operant attention task. Visual distractors were presented in all behavioral testing sessions to tax attentional resources. Under control conditions, aged rats exhibited impairments in discriminating signals with the shortest duration from non-signal events. Surprisingly, chemogenetic inhibition of PFC output neurons did not worsen performance amongst aged animals. Conversely, significant impairments in attentional capacities were observed in young subjects following such manipulation. Given the involvement of PFC-projecting basal forebrain cholinergic neurons in top–down regulation of attention, amperometric recordings were conducted to measure alterations in prefrontal cholinergic transmission in a separate cohort of young and aged rats. While PFC silencing resulted in a robust attenuation of tonic cholinergic signaling across age groups, the capacity to generate phasic cholinergic transients was impaired only amongst young animals. Collectively, our findings suggest a reduced efficiency of PFC-mediated top–down control of attention and cholinergic system in aging, and that activity of PFC output neurons does not reflect compensation in aged rats, at least in the attention domain.
```
</details>

<details><summary>[6] Feature-Selective Attentional Modulations in Human Frontoparietal Cortex — Edward F. Ester, David W. Sutterer, J. Serences, Edward Awh (2016); cutoff-filter date 2016-08-03; doi:10.1523/jneurosci.3935-15.2016</summary>

```text
[6] Feature-Selective Attentional Modulations in Human Frontoparietal Cortex
    id: s2:3cd77b4d2a88f441f048faf1b47f34424f0c500c
    date: 2016-08-03
    venue: Journal of Neuroscience
    authors: Edward F. Ester, David W. Sutterer, J. Serences, Edward Awh
    abstract: Control over visual selection has long been framed in terms of a dichotomy between “source” and “site,” where top-down feedback signals originating in frontoparietal cortical areas modulate or bias sensory processing in posterior visual areas. This distinction is motivated in part by observations that frontoparietal cortical areas encode task-level variables (e.g., what stimulus is currently relevant or what motor outputs are appropriate), while posterior sensory areas encode continuous or analog feature representations. Here, we present evidence that challenges this distinction. We used fMRI, a roving searchlight analysis, and an inverted encoding model to examine representations of an elementary feature property (orientation) across the entire human cortical sheet while participants attended either the orientation or luminance of a peripheral grating. Orientation-selective representations were present in a multitude of visual, parietal, and prefrontal cortical areas, including portions of the medial occipital cortex, the lateral parietal cortex, and the superior precentral sulcus (thought to contain the human homolog of the macaque frontal eye fields). Additionally, representations in many—but not all—of these regions were stronger when participants were instructed to attend orientation relative to luminance. Collectively, these findings challenge models that posit a strict segregation between sources and sites of attentional control on the basis of representational properties by demonstrating that simple feature values are encoded by cortical regions throughout the visual processing hierarchy, and that representations in many of these areas are modulated by attention. SIGNIFICANCE STATEMENT Influential models of visual attention posit a distinction between top-down control and bottom-up sensory processing networks. These models are motivated in part by demonstrations showing that frontoparietal cortical areas associated with top-down control represent abstract or [...]
```
</details>

<details><summary>[7] Directional Signals in the Prefrontal Cortex and in Area MT during a Working Memory for Visual Motion Task — D. Zaksas, T. Pasternak (2006); cutoff-filter date 2006-11-08; doi:10.1523/jneurosci.3420-06.2006</summary>

```text
[7] Directional Signals in the Prefrontal Cortex and in Area MT during a Working Memory for Visual Motion Task
    id: s2:1df921838b07daacd457a2d4cfa6be400c2ed91d
    date: 2006-11-08
    venue: Journal of Neuroscience
    authors: D. Zaksas, T. Pasternak
    abstract: Neurons in the middle temporal visual area (MT) have been implicated in the perception of visual motion, whereas prefrontal cortex (PFC) neurons have been linked to temporary storage of sensory signals, attentional and executive control of behavior. Using a task that placed demands on both sets of neurons, we investigated their contribution to working memory for visual motion. Monkeys compared the direction of two moving random-dot stimuli, sample and test, separated by a brief memory delay. Neurons in both areas showed robust direction-selective activity during all phases of the task. During the sample, ∼60% of task-related PFC neurons were direction selective, and this selectivity emerged 40 ms later than in MT. Unlike MT, the PFC responses to sample did not correlate with behavioral choices, but their selectivity was modulated by task demands and diminished on error trials. Reliable directional signals were found in both areas during the memory delay, but these signals were transient rather than sustained by neurons of either area. Responses to the test in both areas were modulated by the remembered sample direction, decreasing when the test direction matched the sample. This decrease arose in the PFC 100 ms later than in MT and was predictive of the forthcoming decision. Our data suggest that neurons in the two regions are functionally connected and make unique contributions to different task components. PFC neurons reflect task-related information about visual motion and represent decisions that may be based, in part, on the comparison in MT between the remembered sample and test.
```
</details>

<details><summary>[8] **KEY** Prefrontal attentional saccades explore space rhythmically — C. Gaillard, Sameh Ben Hadj Hassen, F. Di Bello, Yann Bihan-Poudec et al. (2019); cutoff-filter date 2019-05-16; doi:10.1101/637975</summary>

```text
[8] Prefrontal attentional saccades explore space rhythmically
    id: s2:2759af28ca1fe466a7f8d66ef11f3a3ef89ea47a
    date: 2019-05-16
    venue: bioRxiv (preprint)
    authors: C. Gaillard, Sameh Ben Hadj Hassen, F. Di Bello, Yann Bihan-Poudec, Rufin VanRullen, S. Ben Hamed
    abstract: Recent studies suggest that attention samples space rhythmically through oscillatory interactions in the frontoparietal network. However, the precise mechanism through which the prefrontal cortex, at the source of attention control signals, organizes this rhythmic exploration of space remains unknown. We show that, when decoded at a high spatial (0.1°) and temporal resolution (50ms), the prefrontal covert attentional spotlight, aka the mind’s eye, continuously explores space at an alpha 7-12 Hz rhythm. When sensory events are presented at a specific optimal phase (resp. anti-phase) with respect to this rhythm, sensory encoding and behavioral report are accurate (resp. poor). We propose that this rhythmic prefrontal attentional spotlight dynamics corresponds to a continuous overt exploration of space via alpha-clocked attentional saccades. These attentional saccades are highly flexible, their pattern of space exploration depending both on within-trial and across-task contingencies. These results are discussed in the context of exploration and exploitation strategies and prefrontal top-down attentional control. Highlights The decoded prefrontal attentional spotlight samples visual space in rhythmic cycles This rhythmic attentional exploration predicts neuronal sensory processing accuracy This rhythmic attentional exploration predicts overt behavioral accuracy These rhythmic cycles define alpha-clocked attentional saccades Space exploration by attentional saccades is highly flexible and under top-down control
```
</details>

<details><summary>[9] **KEY** Neural response during attentional control and emotion processing predicts improvement after cognitive behavioral therapy in generalized social anxiety disorder — H. Klumpp, D. Fitzgerald, M. Angstadt, David Post et al. (2014); cutoff-filter date 2014-03-21; doi:10.1017/s0033291714000567</summary>

```text
[9] Neural response during attentional control and emotion processing predicts improvement after cognitive behavioral therapy in generalized social anxiety disorder
    id: s2:4beafdc6d162b7db26e1adf8d008dd95a3490c3d
    date: 2014-03-21
    venue: Psychological Medicine
    authors: H. Klumpp, D. Fitzgerald, M. Angstadt, David Post, K. Phan
    abstract: Background Individuals with generalized social anxiety disorder (gSAD) exhibit attentional bias to salient stimuli, which is reduced in patients whose symptoms improve after treatment, indicating that mechanisms of bias mediate treatment success. Therefore, pre-treatment activity in regions implicated in attentional control over socio-emotional signals (e.g. anterior cingulate cortex, dorsolateral prefrontal cortex) may predict response to cognitive behavioral therapy (CBT), evidence-based psychotherapy for gSAD. Method During functional magnetic resonance imaging, 21 participants with gSAD viewed images comprising a trio of geometric shapes (circles, rectangles or triangles) alongside a trio of faces (angry, fearful or happy) within the same field of view. Attentional control was evaluated with the instruction to ‘match shapes’, directing attention away from faces, which was contrasted with ‘match faces’, whereby attention was directed to emotional faces. Results Whole-brain voxel-wise analyses showed that symptom improvement was predicted by enhanced pre-treatment activity in the presence of emotional face distractors in the dorsal anterior cingulate cortex and dorsal medial prefrontal cortex. Additionally, CBT success was foretold by less activity in the amygdala and/or increased activity in the medial orbitofrontal gyrus during emotion processing. Conclusions CBT response was predicted by pre-treatment activity in prefrontal regions and the amygdala. The direction of activity suggests that individuals with intact attentional control in the presence of emotional distractors, regulatory capacity over emotional faces and/or less reactivity to such faces are more likely to benefit from CBT. Findings indicate that baseline neural activity in the context of attentional control and emotion processing may serve as a step towards delineating mechanisms by which CBT exerts its effects.
```
</details>

<details><summary>[10] Threat prompts defensive brain responses independently of attentional control. — S. Pichon, B. de Gelder, J. Grèzes (2012); cutoff-filter date 2012-02-01; doi:10.1093/cercor/bhr060</summary>

```text
[10] Threat prompts defensive brain responses independently of attentional control.
    id: s2:31a861b69be95dd4b8500822d1cfd1aa9d653574
    date: 2012-02-01
    venue: Cerebral Cortex
    authors: S. Pichon, B. de Gelder, J. Grèzes
    abstract: [no abstract available]
```
</details>

<details><summary>Post-hoc automated audit — NON-AUTHORITATIVE; uses hidden benchmark annotations</summary>

- primary auditor: `novel_plausible_discriminator`; statuses {'H1': 'negative_or_absent', 'H2': 'positive_or_present'}; discriminative=True
- primary reasoning: H1 predicts that prefrontal cortex should show signals related to the specific content of visual working memory, not just control/prioritization, so the proposition should NOT hold. H2 predicts that PFC is involved in control/prioritization rather than direct storage, so the proposition should hold.
- derived opposition call: `genuine`
- evidence attribution: `generic_compatibility_only` — The retrieved papers establish that the prefrontal cortex is involved in attentional control and, to a lesser extent, in representing specific content, but they do not directly test or compare the relative likelihood of attentional control signals versus content signals in PFC. The evidence is generic and compatible with the proposition, but does not specifically address the comparative claim at its core.
- second rater (LLM, blind): statuses {'H1': 'negative_or_absent', 'H2': 'positive_or_present'}; discriminative=True (medium confidence) — content vs control signals in PFC
- auditor retest: `compatible_non_discriminative`; discriminative=True
- disagreement flags: {'second_rater_vs_primary_discriminative': False, 'second_rater_vs_primary_status': False, 'retest_vs_primary_category': True, 'any': True}
</details>

**Human review** — `genuine_discriminator` · reviewer: Research Director · source: D045 · status: `first_pass_model_based_review` · genuinely discriminative: True · silence-as-null error: False · other fields not recorded

---

## #15 · `GP1-forest_fragmentation_resilience-X4`

**GP1-forest_fragmentation_resilience-X4** — case `forest_fragmentation_resilience`, node `X4`

> Fragmented forests with high edge-to-area ratios exhibit increased tree mortality rates during drought events.

- generated from **H1** (Candidate B); abstraction: `specific`
- influence: **0.279** (rank 3 in case, 15 overall; cumulative 48%) — favours **H1**
- log-likelihood contribution: H2 +0.770, H1 +1.049
- removing it alone: evidence withheld → case log-odds -1.352 (ranking unchanged); node deleted → -1.959 (ranking unchanged)

**Hypotheses (as shown to the verifier)**

- **H1** (Candidate B): Fragmentation increases exposure to heat, atmospheric dryness, wind, and drought stress, raising mortality and reducing ecosystem resilience, especially where water/heat stress dominates.
- **H2** (Candidate A): Edge formation can increase light availability and relax limiting-resource constraints, increasing growth, biomass, recovery capacity, and potentially resilience where climatic stress penalties are small enough.

**Verifier cross-hypothesis judgments** — P(X|H) combines these by noisy-OR

| hypothesis | origin? | direct edge | route via parent | P(X\|H) |
| --- | --- | --- | --- | --- |
| H2 | no | `neutral` | — | 0.500 |
| H1 | yes | `implied` | — | 0.800 |

- edge rationale, **H2** → node: Candidate A suggests edge formation can increase growth and resilience under mild stress but does not address mortality rates during drought events or predict increased mortality.
- edge rationale, **H1** → node: Candidate B explicitly states that fragmentation increases exposure to drought stress and raises mortality, directly supporting the proposition.

**Verifier evidence** — label used in score: `support` (log-LR +1.2)

- queries: `forest edge area tree mortality`; `forest fragmentation drought tree mortality`
- assessor rationale: Several records directly state that fragmented forests and their edges exhibit elevated tree mortality rates compared to non-edge or intact forests. Record [7] specifically notes higher mortality at edges in fragmented regions, and [1] and [4] report increased tree mortality and disturbance at fragment edges. However, none of the records explicitly link these mortality rates to drought events, so the evidence is supportive but not strong for the proposition as written.
- supporting spans cited by the assessor:
  - "Empirical studies on severely fragmented regions suggest that decades after fragmentation, forest edges located near human-modified areas exhibit the structure of early successional states, with lower biomass per area and higher mortality compared to non-edge areas."
  - "These effects can include reduced tree growth and fecundity, elevated tree mortality, alterations in tree‐species composition, degradation of forest succession, and a substantial decline in forest carbon storage."
  - "We found an EE on tree density (SF), and on mortality, total basal area and basal area of dead (CE), although do not so notorious on a short-term scale."
  - "Fragmented forests experienced considerable disturbance‐induced degradation at their edges, resulting in a significant increase in liana abundance. This effect penetrated to significantly greater depths in forest fragments than in intact forests."
- 10 papers shown; key papers: `s2:4c50ba9eab320d4c0ac4c26aaba2c31dc202d85e`, `s2:516fcb38070aa0d042c900d7ddbfecff19c36d40`, `s2:c73fc64bb305df66fde7d2888fc6031b0e8607b1`
- _The evidence assessor returns ONE label for the node from all papers shown; the method has no per-paper contribution. Key papers and spans are those the assessor cited._

<details><summary>[1] **KEY** Edge disturbance drives liana abundance increase and alteration of liana–host tree interactions in tropical forest fragments — M. Campbell, W. Edwards, Ainhoa Magrach, M. Alamgir et al. (2018); cutoff-filter date 2018-04-02; doi:10.1002/ece3.3959</summary>

```text
[1] Edge disturbance drives liana abundance increase and alteration of liana–host tree interactions in tropical forest fragments
    id: s2:c73fc64bb305df66fde7d2888fc6031b0e8607b1
    date: 2018-04-01
    venue: Ecology and Evolution
    authors: M. Campbell, W. Edwards, Ainhoa Magrach, M. Alamgir, Gabriel Porolak, D. Mohandass, W. Laurance
    abstract: Abstract Closed‐canopy forests are being rapidly fragmented across much of the tropical world. Determining the impacts of fragmentation on ecological processes enables better forest management and improves species‐conservation outcomes. Lianas are an integral part of tropical forests but can have detrimental and potentially complex interactions with their host trees. These effects can include reduced tree growth and fecundity, elevated tree mortality, alterations in tree‐species composition, degradation of forest succession, and a substantial decline in forest carbon storage. We examined the individual impacts of fragmentation and edge effects (0–100‐m transect from edge to forest interior) on the liana community and liana–host tree interactions in rainforests of the Atherton Tableland in north Queensland, Australia. We compared the liana and tree community, the traits of liana‐infested trees, and determinants of the rates of tree infestation within five forest fragments (23–58 ha in area) and five nearby intact‐forest sites. Fragmented forests experienced considerable disturbance‐induced degradation at their edges, resulting in a significant increase in liana abundance. This effect penetrated to significantly greater depths in forest fragments than in intact forests. The composition of the liana community in terms of climbing guilds was significantly different between fragmented and intact forests, likely because forest edges had more small‐sized trees favoring particular liana guilds which preferentially use these for climbing trellises. Sites that had higher liana abundances also exhibited higher infestation rates of trees, as did sites with the largest lianas. However, large lianas were associated with low‐disturbance forest sites. Our study shows that edge disturbance of forest fragments significantly altered the abundance and community composition of lianas and their ecological relationships with trees, with liana impacts on trees being elevated in fragments r [...]
```
</details>

<details><summary>[2] Tree mortality in a natural mixed forest affected by stand fragmentation and by a strong typhoon in northern Japan — T. Yoshida, M. Noguchi, S. Uemura, Satoshi Yanaba et al. (2011); cutoff-filter date 2011-05-15; doi:10.1007/s10310-011-0274-5</summary>

```text
[2] Tree mortality in a natural mixed forest affected by stand fragmentation and by a strong typhoon in northern Japan
    id: s2:9e0f56deb430b065c842e5215692332adb5be7a6
    date: 2011-05-15
    venue: Journal of Forest Research
    authors: T. Yoshida, M. Noguchi, S. Uemura, Satoshi Yanaba, Hisashi Miya, T. Hiura
    abstract: [no abstract available]
```
</details>

<details><summary>[3] Tree mortality patterns after experimental fragmentation of an old-growth conifer forest — Per‐Anders Esseen (1994); cutoff-filter date 1994-12-31; doi:10.1016/0006-3207(94)90542-8</summary>

```text
[3] Tree mortality patterns after experimental fragmentation of an old-growth conifer forest
    id: s2:135d42039e78f069f8e0190eb8555273925be28a
    date: 1994
    venue: Biological Conservation
    authors: Per‐Anders Esseen
    abstract: [no abstract available]
```
</details>

<details><summary>[4] **KEY** Edge Effects on Successional Dynamics of Forest Fragments in the Brazilian Cerrado — Firmino Cardoso Pereira, F. Guilherme, B. Marimon (2021); cutoff-filter date 2021-12-31; doi:10.1590/2179-8087-floram-2020-0063</summary>

```text
[4] Edge Effects on Successional Dynamics of Forest Fragments in the Brazilian Cerrado
    id: s2:516fcb38070aa0d042c900d7ddbfecff19c36d40
    date: 2021
    venue: Floresta e Ambiente
    authors: Firmino Cardoso Pereira, F. Guilherme, B. Marimon
    abstract: Comparative studies of tree dynamics can be useful for the conservation of forest fragments in the Cerrado. We tested if the successional dynamics in fragments of semideciduous forest (SF) and cerradão (CE) are influenced by edge effects (EE). Two surveys were carried out with plots allocation in both physiognomies, from the edge towards the interior of the fragments. All trees with diameter at breast height ≥ 5cm were measured, identified and classified (ecological groups). Both physiognomies showed high recruitment and mortality rates when compared with other forests in Cerrado. We found an EE on tree density (SF), and on mortality, total basal area and basal area of dead (CE), although do not so notorious on a short-term scale. Probably because EE did not influence the ecological groups and canopy cover. Our results suggest that the forest fragmentation can act as a disturbance agent, causing changes in the tree dynamics of the Cerrado forests.
```
</details>

<details><summary>[5] Massive mortality of aspen following severe drought along the southern edge of the Canadian boreal forest — M. Michaelian, E. Hogg, R. Hall, E. Arsenault (2011); cutoff-filter date 2011-06-01; doi:10.1111/j.1365-2486.2010.02357.x</summary>

```text
[5] Massive mortality of aspen following severe drought along the southern edge of the Canadian boreal forest
    id: s2:8cd408dedb2d686380d4ff262cf0c43517dc3d28
    date: 2011-06-01
    venue: Global Change Biology
    authors: M. Michaelian, E. Hogg, R. Hall, E. Arsenault
    abstract: Drought‐induced, regional‐scale dieback of forests has emerged as a global concern that is expected to escalate under model projections of climate change. Since 2000, drought of unusual severity, extent, and duration has affected large areas of western North America, leading to regional‐scale dieback of forests in the southwestern US. We report on drought impacts on forests in a region farther north, encompassing the transition between boreal forest and prairie in western Canada. A central question is the significance of drought as an agent of large‐scale tree mortality and its potential future impact on carbon cycling in this cold region. We used a combination of plot‐based, meteorological, and remote sensing measures to map and quantify aboveground, dead biomass of trembling aspen (Populus tremuloides Michx.) across an 11.5 Mha survey area where drought was exceptionally severe during 2001–2002. Within this area, a satellite‐based land cover map showed that aspen‐dominated broadleaf forests occupied 2.3 Mha. Aerial surveys revealed extensive patches of severe mortality (>55%) resembling the impacts of fire. Dead aboveground biomass was estimated at 45 Mt, representing 20% of the total aboveground biomass, based on a spatial interpolation of plot‐based measurements. Spatial variation in percentage dead biomass showed a moderately strong correlation with drought severity. In the prairie‐like, southern half of the study area where the drought was most severe, 35% of aspen biomass was dead, compared with an estimated 7% dead biomass in the absence of drought. Drought led to an estimated 29 Mt increase in dead biomass across the survey area, corresponding to 14 Mt of potential future carbon emissions following decomposition. Many recent, comparable episodes of drought‐induced forest dieback have been reported from around the world, which points to an emerging need for multiscale monitoring approaches to quantify drought effects on woody biomass and carbon cycling acros [...]
```
</details>

<details><summary>[6] Effects of Topography and Tree Structure on the Distribution Patterns of Understory Plants in the Transitional Area between China’s Southern Subtropical Zone and the Northern Edge of the Tropical Zone — Na Fan (2012); cutoff-filter date 2012-12-31; https://www.semanticscholar.org/paper/d8bccd7261ef72b2d20a88403d7388922bb58821</summary>

```text
[6] Effects of Topography and Tree Structure on the Distribution Patterns of Understory Plants in the Transitional Area between China’s Southern Subtropical Zone and the Northern Edge of the Tropical Zone
    id: s2:d8bccd7261ef72b2d20a88403d7388922bb58821
    date: 2012
    venue: Resources Science
    authors: Na Fan
    abstract: [no abstract available]
```
</details>

<details><summary>[7] **KEY** Tropical forest degradation and recovery in fragmented landscapes — Simulating changes in tree community, forest hydrology and carbon balance — M. D. de Paula, J. Groeneveld, A. Huth (2015); cutoff-filter date 2015-12-31; doi:10.1016/j.gecco.2015.03.004</summary>

```text
[7] Tropical forest degradation and recovery in fragmented landscapes — Simulating changes in tree community, forest hydrology and carbon balance
    id: s2:4c50ba9eab320d4c0ac4c26aaba2c31dc202d85e
    date: 2015
    venue: Global Ecology and Conservation
    authors: M. D. de Paula, J. Groeneveld, A. Huth
    abstract: Abstract Empirical studies on severely fragmented regions suggest that decades after fragmentation, forest edges located near human-modified areas exhibit the structure of early successional states, with lower biomass per area and higher mortality compared to non-edge areas. These habitat changes (edge effects) can also have a considerable impact on ecosystem processes such as carbon and water balance, which in turn have a major impact on human activities. Using field data from a long-term fragmented landscape in the Brazilian Northeastern Atlantic Forest, and the Forest Model FORMIND, we were able to visualize the time scale in which edge effects influence tropical forests by performing 500-year simulations. We observed changes in community composition, aboveground biomass, total evapotranspiration and total runoff. Averages from ten four-hectare simulations show forest biomass degradation lasting around 100 years. If edge effects cease, recovery of biomass lasts around 150 years. Carbon loss is especially intense during the first five years after fragmentation, resulting in a decline of over 5 Mg ha −1 y −1 C. Finally, edges of large fragments face an evapotranspiration loss of 43% and total runoff gains of 57% in relation to core areas of large fragments, suggesting that fragmented landscapes can be of significantly lower value in terms of ecosystem services.
```
</details>

<details><summary>[8] The fate of Amazonian forest fragments: A 32-year investigation — W. Laurance, J. Camargo, R. Luizão, S. Laurance et al. (2011); cutoff-filter date 2011-12-31; doi:10.1016/j.biocon.2010.09.021</summary>

```text
[8] The fate of Amazonian forest fragments: A 32-year investigation
    id: s2:f01561d301d6610e845abaa446b854ed990aaea4
    date: 2011
    venue: Biological Conservation
    authors: W. Laurance, J. Camargo, R. Luizão, S. Laurance, S. Pimm, E. Bruna, P. Stouffer, G. Williamson
    abstract: [no abstract available]
```
</details>

<details><summary>[9] Elevated growth and biomass along temperate forest edges — L. Morreale, Jonathan R. Thompson, Xiao-Jing Tang, A. Reinmann et al. (2021); cutoff-filter date 2021-12-10; doi:10.1038/s41467-021-27373-7</summary>

```text
[9] Elevated growth and biomass along temperate forest edges
    id: s2:2a84b020530b9f3ab9daff49f479a8b1669a20f0
    date: 2021-12-01
    venue: Nature Communications
    authors: L. Morreale, Jonathan R. Thompson, Xiao-Jing Tang, A. Reinmann, L. Hutyra
    abstract: Fragmentation transforms the environment along forest edges. The prevailing narrative, driven by research in tropical systems, suggests that edge environments increase tree mortality and structural degradation resulting in net decreases in ecosystem productivity. We show that, in contrast to tropical systems, temperate forest edges exhibit increased forest growth and biomass with no change in total mortality relative to the forest interior. We analyze >48,000 forest inventory plots across the north-eastern US using a quasi-experimental matching design. At forest edges adjacent to anthropogenic land covers, we report increases of 36.3% and 24.1% in forest growth and biomass, respectively. Inclusion of edge impacts increases estimates of forest productivity by up to 23% in agriculture-dominated areas, 15% in the metropolitan coast, and +2% in the least-fragmented regions. We also quantify forest fragmentation globally, at 30-m resolution, showing that temperate forests contain 52% more edge forest area than tropical forests. Our analyses upend the conventional wisdom of forest edges as less productive than intact forest and call for a reassessment of the conservation value of forest fragments. Studies from tropical regions indicate that fragmented forests are less productive. Here, the authors report higher growth and biomass in temperate forest edges in North America, and show that temperate forests are more fragmented than tropical forests globally.
```
</details>

<details><summary>[10] Tree Responses to Edge Effects and Canopy Openness in a Tropical Montane Forest Fragment in Southern Costa Rica — L. Cayuela, C. Murcia, A. Hawk, J. Fernandez-Vega et al. (2009); cutoff-filter date 2009-12-01; doi:10.1177/194008290900200404</summary>

```text
[10] Tree Responses to Edge Effects and Canopy Openness in a Tropical Montane Forest Fragment in Southern Costa Rica
    id: s2:ee8a0c4e7dd320dbc114a510711c6a11df6a2bbc
    date: 2009-12-01
    venue: Tropical Conservation Science
    authors: L. Cayuela, C. Murcia, A. Hawk, J. Fernandez-Vega, Federico Oviedo‐Brenes
    abstract: Tropical forests frequently experience the opening and closing of canopy gaps as part of their natural dynamics. When fragmented, the forests are also exposed to edges, which (at least in the lowlands) cause increased mortality on the fragment's periphery and—depending on the fragment size—also on the forest interior. Here we explore if the presence of edges increase the rate at which the canopy opens in a montane forest and if and how that interaction affects the vegetation composition and structure. At Las Cruces Biological Station (SW Costa Rica), we surveyed four 150 m edge-to-interior transects to evaluate changes in vegetation structure (stem density and basal area for all plants with DBH > 5 cm) and species richness and composition as a function of both distance to the edge and canopy openness. Edge proximity did not increase canopy openness. Canopy openness, however, did affect stem density, species richness, and composition. Consequently, heterogeneity in forest structure, diversity, or composition could not be attributed to indirect edge effects. Forest edges, however, had a direct effect on species composition, but with a negligible effect on species diversity and forest structure. Overall, these results reveal that the structure, diversity, and composition of tree communities in this tropical premontane forest fragment are more strongly influenced by canopy openness than by the proximity of edges.
```
</details>

<details><summary>Post-hoc automated audit — NON-AUTHORITATIVE; uses hidden benchmark annotations</summary>

- primary auditor: `silence_as_null_error`; statuses {'H2': 'indeterminate', 'H1': 'positive_or_present'}; discriminative=False
- primary reasoning: H1 predicts that fragmentation increases exposure to drought stress and thus should increase tree mortality during droughts. H2 focuses on increased resource availability and growth but does not specifically address mortality during drought events, so it is silent on this proposition.
- derived opposition call: `one_sided_silence_labelled_neutral`
- evidence attribution: `generic_compatibility_only` — The retrieved papers and the assessor's rationale show that the literature supports increased tree mortality at forest edges and in fragmented forests, but they do not specifically address the interaction with drought events as required by the proposition. The evidence is thus only generically compatible: it supports the plausibility of the mechanism but does not test the full proposition. The process did not surface direct evidence for the specific claim.
- disagreement flags: {'second_rater_vs_primary_discriminative': None, 'second_rater_vs_primary_status': None, 'retest_vs_primary_category': None, 'any': False}
</details>

**Human review** — `compatible_non_discriminative` · reviewer: Research Director · source: D045 · status: `first_pass_model_based_review` · genuinely discriminative: False · silence-as-null error: False · other fields not recorded

---

## #16 · `GP1-forest_fragmentation_resilience-X5`

**GP1-forest_fragmentation_resilience-X5** — case `forest_fragmentation_resilience`, node `X5`

> Increased exposure to wind and atmospheric dryness at forest edges leads to reduced vegetation resilience to environmental disturbances.

- generated from **H1** (Candidate B); abstraction: `mechanistic`
- generator's stated reason: The claim states that fragmentation increases exposure to these stressors, which in turn reduces resilience, so the mechanism of edge exposure causing lower resilience is more likely.
- influence: **0.279** (rank 4 in case, 16 overall; cumulative 50%) — favours **H1**
- log-likelihood contribution: H2 +0.770, H1 +1.049
- removing it alone: evidence withheld → case log-odds -1.352 (ranking unchanged); node deleted → -1.624 (ranking unchanged)

**Hypotheses (as shown to the verifier)**

- **H1** (Candidate B): Fragmentation increases exposure to heat, atmospheric dryness, wind, and drought stress, raising mortality and reducing ecosystem resilience, especially where water/heat stress dominates.
- **H2** (Candidate A): Edge formation can increase light availability and relax limiting-resource constraints, increasing growth, biomass, recovery capacity, and potentially resilience where climatic stress penalties are small enough.

**Verifier cross-hypothesis judgments** — P(X|H) combines these by noisy-OR

| hypothesis | origin? | direct edge | route via parent | P(X\|H) |
| --- | --- | --- | --- | --- |
| H2 | no | `neutral` | — | 0.500 |
| H1 | yes | `implied` | — | 0.800 |

- edge rationale, **H2** → node: Candidate A suggests that edge effects can increase resilience unless climatic stress is significant, but does not directly address the effect of wind and atmospheric dryness on resilience.
- edge rationale, **H1** → node: Candidate B explicitly states that increased exposure to wind and atmospheric dryness at edges reduces ecosystem resilience, which aligns with the proposition.

**Verifier evidence** — label used in score: `support` (log-LR +1.2)

- queries: `forest edge wind vegetation resilience`; `atmospheric dryness forest edge disturbance`
- assessor rationale: Record [3] directly addresses the proposition, showing that increased exposure to wind and atmospheric dryness at forest edges amplifies edge effects, which are associated with negative impacts on vegetation resilience during environmental disturbances such as drought. The study demonstrates that these effects are stronger in drought years and in areas with less rain, supporting the proposition that such exposure reduces resilience. Other records do not directly state the proposition as written.
- supporting spans cited by the assessor:
  - "Differences in wind, radiation and vegetation structure create edge-to-interior gradients in forest microclimate, and these gradients are likely to be more pronounced during droughts and heatwaves."
  - "Edge effects were almost twice as strong in the drought year as in the non-drought years, but we did not find clear evidence that they penetrated deeper into the forest in the drought year."
  - "Edge influences were also greater in areas that had fewer days with rain during the drought year."
  - "Our results demonstrate that edge effects are amplified by drought, suggesting that fragmentation effects are aggravated when droughts become more frequent and severe."
  - "Our results suggest that dense edges and buffer zones with high canopy cover can be important ways to mitigate negative drought impacts in forest edges."
- 10 papers shown; key papers: `s2:75b80df6a3a8ff0572c9cf488abaf3ac2f3de1bb`
- _The evidence assessor returns ONE label for the node from all papers shown; the method has no per-paper contribution. Key papers and spans are those the assessor cited._

<details><summary>[1] Resilient Restoration of Power Distribution System Based on Minimum Spanning Forest — Shiva Poudel, Hongbo Sun, D. Nikovski, Jinyun Zhang (2019); cutoff-filter date 2019-08-31; doi:10.1109/pesgm40551.2019.8973730</summary>

```text
[1] Resilient Restoration of Power Distribution System Based on Minimum Spanning Forest
    id: s2:9e4709d02c4075cf3928a50f489d415cad16904f
    date: 2019-08-01
    venue: IEEE Power & Energy Society General Meeting
    authors: Shiva Poudel, Hongbo Sun, D. Nikovski, Jinyun Zhang
    abstract: In this paper, the concept of minimum spanning forest (MSF) is utilized to formulate the restoration problem where each spanning tree in a forest is a self-sustained islanded grid (SSIG). Specifically, a weight is assigned to each edge in a distribution system based on several factors such as their exposure to vegetation, span length, location and structures supporting them. Then, a MSF is obtained for the given network by switching off the edges with higher weights to form several SSIGs each energized by a master unit (micro-turbine) in coordination with several intermittent DGs (wind, solar) and energy storage system (ESS) while achieving the resilience objectives. Numerical results based on a modified IEEE 123-node test case validates the effectiveness of the proposed approach.
```
</details>

<details><summary>[2] Not every high‐latitude or high‐elevation forest edge is a treeline — C. Körner, G. Hoch (2023); cutoff-filter date 2023-03-14; doi:10.1111/jbi.14593</summary>

```text
[2] Not every high‐latitude or high‐elevation forest edge is a treeline
    id: s2:298dda25f80e4f3839a8740d0fc9776278059b5b
    date: 2023-03-14
    venue: Journal of Biogeography
    authors: C. Körner, G. Hoch
    abstract: Attempts at identifying climate warming effects on mountain and arctic vegetation caused a recent hype in treeline studies. In this perspectives article, we recall the need of clear‐cut definitions, a consistent terminology and a theoretical framework that permits hypothesis testing. Founded in the ecological niche concept, the application of the fundamental niche edge to treeline permits defining the potential climatic limit of tree growth, while the realized niche edge captures all deviations for reasons related to other, more local, abiotic factors, biotic interactions, disturbances and human interventions. An important point is that a globally common phenomenon calls for a common abiotic driver which is the temperature at the low temperature edge of the niche of the life form tree. We explain why other abiotic factors that may affect the local range limits, such as microclimate, moisture and wind do not devaluate the classical isotherm concept. Our key message is that applying a clearly defined concept of potential treeline, also allows defining deviations from it and explaining the deviations within a reproducible theoretical framework.
```
</details>

<details><summary>[3] **KEY** Forest edge effects on moss growth are amplified by drought. — Irena A. Koelemeijer, J. Ehrlén, P. De Frenne, Mari Jönsson et al. (2023); cutoff-filter date 2023-03-20; doi:10.1002/eap.2851</summary>

```text
[3] Forest edge effects on moss growth are amplified by drought.
    id: s2:75b80df6a3a8ff0572c9cf488abaf3ac2f3de1bb
    date: 2023-03-20
    venue: Ecological Applications
    authors: Irena A. Koelemeijer, J. Ehrlén, P. De Frenne, Mari Jönsson, P. Berg, K. Hylander
    abstract: Forest fragmentation increases the amount of edges in the landscape. Differences in wind, radiation and vegetation structure create edge-to-interior gradients in forest microclimate, and these gradients are likely to be more pronounced during droughts and heatwaves. Although the effects of climate extremes on edge influences have potentially strong and long-lasting impacts on forest understory biodiversity, they are not well understood and are not often considered in management and landscape planning. Here we used a novel method of retrospectively quantifying growth to assess biologically relevant edge influences likely caused by microclimate using Hylocomium splendens, a moss with annual segments. We examined how spatio-temporal variation in drought across three years and 46 sites in central Sweden, affected the depth and magnitude of edge influences. We also investigated whether edge effects during drought are influenced by differences in forest structure. Edge effects were almost twice as strong in the drought year as in the non-drought years, but we did not find clear evidence that they penetrated deeper into the forest in the drought year. Edge influences were also greater in areas that had fewer days with rain during the drought year. Higher levels of forest canopy cover and tree height buffered the magnitude of edge influence in times of drought. Our results demonstrate that edge effects are amplified by drought, suggesting that fragmentation effects are aggravated when droughts become more frequent and severe. Our results suggest that dense edges and buffer zones with high canopy cover can be important ways to mitigate negative drought impacts in forest edges.
```
</details>

<details><summary>[4] Old‐growth forests show low canopy resilience to droughts at the southern edge of the taiga — Feng Liu, Hongyan Liu, Chong-Yang Xu, Liang Shi et al. (2021); cutoff-filter date 2021-03-19; doi:10.1111/gcb.15605</summary>

```text
[4] Old‐growth forests show low canopy resilience to droughts at the southern edge of the taiga
    id: s2:9bb8bdd57dbbf3721b5236b222ae4654fbd6458b
    date: 2021-03-19
    venue: Global Change Biology
    authors: Feng Liu, Hongyan Liu, Chong-Yang Xu, Liang Shi, Xin-Rong Zhu, Yang Qi, Wenqi He
    abstract: Forest mortality and resilience driven by drought disturbances have attracted tons of attention. However, the acquisition of continuous spatial–temporal data is generally enslaved to the conventional field investigations. In this study, the resilience of semiarid forest was characterized with canopy dynamics from remote sensing observations, combining the variations in canopy greenness and water content. We integrated dense normalized difference vegetation index (NDVI) and normalized difference infrared index (NDII) time series from Landsat datasets, intending to assess the canopy resilience in 24 conifer patches along a climatic aridity gradient at the southern edge of the taiga in northern Mongolia and southern Siberia of Russia. The results exhibited four patterns of coordinated NDVI–NDII variation trends, indicating that the canopy water content of coniferous forests may decrease at first during a drought period, and sustained water loss may, in turn, induce an accompanying reduction in canopy greenness. Meanwhile, the patches with canopy recovery growth after initial declines were considered to have resilience to climate change. We further observed the combined effects of aridity degree and tree age on canopy resilience, and all seven patches with no resilience corresponded to the old‐tree group (the oldest trees reached or exceeded the age of 90). The observations indicated that the old‐growth forests in semiarid regions were less likely to show canopy resilience, which corresponded to a higher risk of sustained decline.
```
</details>

<details><summary>[5] Norway spruce at the trailing edge: the effect of landscape configuration and composition on climate resilience — Juha Honkaniemi, W. Rammer, R. Seidl (2020); cutoff-filter date 2020-01-11; doi:10.1007/s10980-019-00964-y</summary>

```text
[5] Norway spruce at the trailing edge: the effect of landscape configuration and composition on climate resilience
    id: s2:8133b3c309f8db3abb7353a6ce6be785f8623237
    date: 2020-01-11
    venue: Landscape Ecology
    authors: Juha Honkaniemi, W. Rammer, R. Seidl
    abstract: Norway spruce (Picea abies) is one of the most widespread tree species in Europe’s forests. Due to its high economic value it has been strongly favored by management, especially at the trailing edge of its natural distribution. However, disturbances from wind and bark beetles are increasingly impacting these forests, and their resilience under climate change has been called into question recently. We quantified the effects of landscape configuration and composition on (1) the risk from natural disturbances, and (2) on the overall resilience of Norway spruce to changing climate at the trailing edge. We simulated the dynamics of a 9183 ha forest landscape in Eastern Austria over 190 years. We used the simulation model iLand to experimentally study a wide range of landscape compositions and configurations under five different climate scenarios. Natural disturbances increased considerably under all future climate scenarios. Dispersing Norway spruce throughout the landscape in mixed stands resulted in the highest levels of climate resilience. Reducing the percentage of Norway spruce on the landscape increased the resilience of the remaining Norway spruce trees, yet landscape configuration generally had a stronger effect on resilience than composition. The resilience of Norway spruce at the trailing edge of its distribution is challenged by climate change, and considerable efforts are needed to sustain these ecosystems. While currently discussed adaptation measures focus largely on the stand level, we show that modifying landscape composition and configuration can be used to foster Norway spruce resilience while maintaining socio-economically relevant proportions of Norway spruce.
```
</details>

<details><summary>[6] Resilience of a Fire-Maintained Pinus palustris Woodland to Catastrophic Wind Disturbance: 10 Year Results — J. D. Goode, J. Kleinman, J. Hart (2021); cutoff-filter date 2021-08-07; doi:10.3390/f12081051</summary>

```text
[6] Resilience of a Fire-Maintained Pinus palustris Woodland to Catastrophic Wind Disturbance: 10 Year Results
    id: s2:9d1b04a022a7296d36a03beefc47c2a8afd9cdfa
    date: 2021-08-07
    venue: Forests
    authors: J. D. Goode, J. Kleinman, J. Hart
    abstract: Increased interest in ecosystem recovery and resilience has been driven by concerns over global change-induced shifts in forest disturbance regimes. In frequent-fire forests, catastrophic wind disturbances modify vegetation-fuels-fire feedbacks, and these alterations may shift species composition and stand structure to alternative states relative to pre-disturbance conditions. We established permanent inventory plots in a catastrophically wind-disturbed and fire-maintained Pinus palustris woodland in the Alabama Fall Line Hills to examine ecosystem recovery and model the successional and developmental trajectory of the stand through age 50 years. We found that sapling height was best explained by species. Species with the greatest mean heights likely utilized different regeneration mechanisms. The simulation model projected that at age 50 years, the stand would transition to be mixedwood and dominated by Quercus species, Pinus taeda, and P. palustris. The projected successional pathway is likely a function of residual stems that survived the catastrophic wind disturbance and modification of vegetation-fuels-fire feedbacks. Although silvicultural interventions will be required for this system to exhibit pre-disturbance species composition and structure, we contend that the ecosystem was still resilient to the catastrophic disturbance because similar silvicultural treatments were required to create and maintain the P. palustris woodland prior to the disturbance event.
```
</details>

<details><summary>[7] Not gone with the wind: Vegetation complexity increases seed retention during windy periods in the Argentine Semiarid Chaco — M. L. Lipoma, A. Cuchietti, Lucas D. Gorné, S. Díaz (2019); cutoff-filter date 2019-05-01; doi:10.1111/jvs.12747</summary>

```text
[7] Not gone with the wind: Vegetation complexity increases seed retention during windy periods in the Argentine Semiarid Chaco
    id: s2:cea28a09549f9462297a6dd008a107a30a0cde57
    date: 2019-05-01
    venue: Journal of Vegetation Science
    authors: M. L. Lipoma, A. Cuchietti, Lucas D. Gorné, S. Díaz
    abstract: QUESTIONS: We experimentally studied whether different degrees of vegetation structural complexity, developed under different land‐use regimes, affected the retention of seeds in situ in the semiarid Chaco forest. We sought to answer the following questions: (a) Does vegetation complexity in interaction with climatic conditions affect seed retention on the soil surface? (b) Do seeds with contrasting traits show the same retention pattern? LOCATION: Chancani, Northwestern Cordoba, Argentina. METHODS: We run a field experiment to test seed retention across 16 field sites differing in physiognomy and land‐use regime. We used artificial seeds with contrasting traits to simulate extreme morphologies found among dominant species of the Chaco forest (large‐flattened and small‐spherical seed types). We placed artificial seeds in 10 quadrats along a transect at each site and recorded the number of seeds retained after 25 days. We performed the experiment in the same season in two consecutive years. Through a Principal Component Analysis of a matrix of 320 survey plots by 6 structural variables, we extracted two major multivariate axes summarizing vegetation complexity. RESULTS: Vegetation complexity was strongly related to land‐use regimes, and a more complex vegetation structure increased seed retention, particularly in the first year of the experiment, when wind velocity was twice the value of the historical mean. The same general retention pattern was observed for different seed types with contrasting size and shape, but the absolute amount of retention was lower for large‐flattened than small‐spherical seeds. CONCLUSION: Vegetation complexity interacting with variable climatic conditions ‐especially wind velocity‐ and seed morphology increased seed retention on the soil surface. Because seed dynamics is known to play an essential role in vegetation recovery, manipulation of soil cover should be a key factor in vegetation resilience in these systems.
```
</details>

<details><summary>[8] Forest-edge effects on sea-salt aerosol deposition: a wind-tunnel study using living oak leaves — A. Reinap, B. Wiman, B. Svenningsson, Sara Gunnarsson (2012); cutoff-filter date 2012-12-31; https://www.semanticscholar.org/paper/b5342619a166d31f2b19010cbbef730cf1c18249</summary>

```text
[8] Forest-edge effects on sea-salt aerosol deposition: a wind-tunnel study using living oak leaves
    id: s2:b5342619a166d31f2b19010cbbef730cf1c18249
    date: 2012
    venue: Boreal Environment Research
    authors: A. Reinap, B. Wiman, B. Svenningsson, Sara Gunnarsson
    abstract: [no abstract available]
```
</details>

<details><summary>[9] Tropical Cyclone Impact and Forest Resilience in the Southwestern Pacific — Baptiste Delaporte, T. Ibanez, M. Despinoy, M. Mangeas et al. (2022); cutoff-filter date 2022-03-03; doi:10.3390/rs14051245</summary>

```text
[9] Tropical Cyclone Impact and Forest Resilience in the Southwestern Pacific
    id: s2:385e040fee4ab83ea4a24a82779f15ee37fbcaa7
    date: 2022-03-03
    venue: Remote Sensing
    authors: Baptiste Delaporte, T. Ibanez, M. Despinoy, M. Mangeas, C. Menkes
    abstract: Tropical cyclones (TCs) can have profound effects on the dynamics of forest vegetation that need to be better understood. Here, we analysed changes in forest vegetation induced by TCs using the normalized difference vegetation index (NDVI). We used an accurate historical database of TC tracks and intensities, together with the Willoughby cyclone model to reconstruct the 2D surface wind speed structure of TCs and analyse how TCs affect forest vegetation. We used segmented linear models to identify significant breakpoints in the relationship between the reconstructed maximum sustained wind speed (Wmax) and the observed changes in NDVI. We tested the hypothesis that the rate of change in damage caused by TCs to forest and recovery time would increase according to Wmax thresholds as defined in the widely used Saffir–Simpson hurricane wind scale (SSHWS). We showed that the most significant breakpoint was located at 50 m/s. This breakpoint corresponds to the transition between categories 2 and 3 TCs in the SSHWS. Below this breakpoint, damages caused to forest vegetation and the time needed to recover from these damages were negligable. We found a second breakpoint, with a sharp increase in damages for winds >75 m/s. This suggested that extremely intense tropical cyclones, which might be more frequent in the future, can cause extreme damages to forest vegetation. Nevertheless, we found high variation in the observed damages and time needed to recover for a given Wmax. Further studies are needed to integrate other factors that might affect the exposure and resistance to TCs as well as forests’ capacity to recover from these disturbances.
```
</details>

<details><summary>[10] Early arboreal colonization, postglacial resilience of deciduous Nothofagus forests, and the Southern Westerly Wind influence in central-east Andean Patagonia — P. I. Moreno, E. Simi, R. Villa-Martínez, I. Vilanova (2019); cutoff-filter date 2019-08-15; doi:10.1016/j.quascirev.2019.06.004</summary>

```text
[10] Early arboreal colonization, postglacial resilience of deciduous Nothofagus forests, and the Southern Westerly Wind influence in central-east Andean Patagonia
    id: s2:2e9002ffb56564e46e40054f9a7fa06954f2df0f
    date: 2019-08-15
    venue: Quaternary Science Reviews
    authors: P. I. Moreno, E. Simi, R. Villa-Martínez, I. Vilanova
    abstract: Abstract The history and dynamics of deciduous Nothofagus forests along the eastern slopes of the central Patagonian Andes (44°-49°S) remain insufficiently studied and understood, particularly at timescales ranging from centuries to millennia. Available fossil pollen records point to time-transgressive responses of the arboreal vegetation to climatic changes during the Last Glacial Termination (T1) and early Holocene, and spatial heterogeneity since then along north-south, east-west, and elevation transects. The degree to which these results represent biogeographic and climatic trends, varying environmental gradients, or site-specific phenomena has not been assessed in detail. Here we present a fossil pollen and macroscopic charcoal record from Lago Churrasco (45°41′S, 71°49′W), a small closed-basin lake located in the deciduous Nothofagus forest zone of the central-east Andes of Chilean Patagonia. Our results suggest that Nothofagus trees colonized newly deglaciated terrains at ∼16,000 cal yr BP and formed scrublands/woodlands several millennia earlier than reported by previous studies east of the Andes. This suggests expansion and local densification of tree populations sourced from the eastern margin of the Patagonian Ice Sheet during the Last Glacial Maximum, with the additional implication that temperature and precipitation conditions favorable for tree survival and reproduction developed early during T1. We posit that the amount of moisture delivered by the Southern Westerly Winds was not a limiting factor for arboreal expansion during T1 in this sector of the central Patagonian Andes. Closed-canopy Nothofagus forests established at ∼10,000 cal yr BP and have remained essentially invariant despite climate change and natural disturbance regimes. This resilience was challenged and exceeded by human disturbance during the 20th century through the use of fire, leading to deforestation and spread of invasive exotic species in an extraordinarily rapid event. Our rec [...]
```
</details>

<details><summary>Post-hoc automated audit — NON-AUTHORITATIVE; uses hidden benchmark annotations</summary>

- primary auditor: `silence_as_null_error`; statuses {'H1': 'positive_or_present', 'H2': 'indeterminate'}; discriminative=False
- primary reasoning: H1 explicitly predicts that increased exposure to wind and atmospheric dryness at edges reduces resilience. H2 does not address edge-induced wind or dryness or their effects on resilience, so it is silent on this proposition.
- derived opposition call: `one_sided_silence_labelled_neutral`
- evidence attribution: `informative_evidence_found` — The retrieval system surfaced a paper (record 3) that directly addresses the proposition, showing that increased wind and atmospheric dryness at forest edges reduce vegetation resilience to disturbance. The assessor correctly identified and used this evidence. The process worked as intended.
- disagreement flags: {'second_rater_vs_primary_discriminative': None, 'second_rater_vs_primary_status': None, 'retest_vs_primary_category': None, 'any': False}
</details>

**Human review** — `compatible_non_discriminative` · reviewer: Research Director · source: D045 · status: `first_pass_model_based_review` · genuinely discriminative: False · silence-as-null error: False · other fields not recorded

---

## #17 · `GP1-gcn4_med15_complex_vs_condensate-X5`

**GP1-gcn4_med15_complex_vs_condensate-X5** — case `gcn4_med15_complex_vs_condensate`, node `X5`

> Phase separation between transcription factor activation domains and Mediator subunits facilitates recruitment of Mediator to active gene loci.

- generated from **H2** (Candidate B); abstraction: `mechanistic`
- generator's stated reason: The claim asserts that Gcn4 activates transcription via co-phase-separation with Med15, implying that phase separation is a mechanism for Mediator recruitment.
- influence: **0.279** (rank 2 in case, 17 overall; cumulative 51%) — favours **H2**
- log-likelihood contribution: H1 +0.770, H2 +1.049
- removing it alone: evidence withheld → case log-odds +0.274 (ranking CHANGES); node deleted → -0.459 (ranking unchanged)

**Hypotheses (as shown to the verifier)**

- **H1** (Candidate A): Gcn4 activation domains activate transcription through dynamic multivalent contacts with Med15 activation-binding domains in soluble complexes; transcriptional activity should therefore track productive Gcn4-Med15 molecular binding/affinity even outside a condensed phase.
- **H2** (Candidate B): Gcn4 activation domains can activate transcription through phase-separation capacity and co-condensation with Mediator/Med15; transcriptional output should therefore track co-phase-separation/Med15 recruitment into condensates under the proposed condensate mechanism.

**Verifier cross-hypothesis judgments** — P(X|H) combines these by noisy-OR

| hypothesis | origin? | direct edge | route via parent | P(X\|H) |
| --- | --- | --- | --- | --- |
| H1 | no | `neutral` | — | 0.500 |
| H2 | yes | `implied` | — | 0.800 |

- edge rationale, **H1** → node: Candidate A posits that transcriptional activation depends on soluble molecular interactions rather than phase separation, and thus does not imply that phase separation facilitates Mediator recruitment.
- edge rationale, **H2** → node: Candidate B suggests that phase separation and co-condensation with Mediator are mechanisms for transcriptional activation, making it clearly expected that phase separation facilitates Mediator recruitment.

**Verifier evidence** — label used in score: `support` (log-LR +1.2)

- queries: `transcription factor Mediator phase separation`; `Mediator recruitment gene loci phase separation`
- assessor rationale: Record [7] directly states that transcription factor activation domains form phase-separated condensates with Mediator, and that this interaction is linked to gene activation. It also notes that the same residues are required for both phase separation with Mediator and gene activation, supporting the proposition that phase separation facilitates Mediator recruitment to active gene loci. No other records directly address the specific mechanism between TF ADs and Mediator subunits in recruitment.
- supporting spans cited by the assessor:
  - "Here we report that diverse ADs form phase-separated condensates with the Mediator coactivator. For the OCT4 and GCN4 TFs, we show that the ability to form phase-separated droplets with Mediator in vitro and the ability to activate genes in vivo are dependent on the same amino acid residues."
  - "These results suggest that diverse TFs can interact with Mediator through the phase-separating capacity of their ADs and that formation of condensates with Mediator is involved in gene activation."
- 10 papers shown; key papers: `s2:e4f0debfff8b369862f80cc3adec3518a77760c0`
- _The evidence assessor returns ONE label for the node from all papers shown; the method has no per-paper contribution. Key papers and spans are those the assessor cited._

<details><summary>[1] Phase separation in transcription factor dynamics and chromatin organization — Kaustubh Wagh, David A. Garcia, A. Upadhyaya (2021); cutoff-filter date 2021-07-22; doi:10.1016/j.sbi.2021.06.009</summary>

```text
[1] Phase separation in transcription factor dynamics and chromatin organization
    id: s2:f51971ef0c59aa1d5b52ee24002c90cad98a808d
    date: 2021-07-22
    venue: Current Opinion in Structural Biology
    authors: Kaustubh Wagh, David A. Garcia, A. Upadhyaya
    abstract: Studies over the past decade have highlighted the key role of liquid-liquid phase separation in cellular organization and function. Dynamic compartmentalization of transcription factors and co-activators by such phase-separated condensates regulates the assembly of transcriptional machinery at genomic loci. While rapid advances in microscopy have demonstrated the ubiquity of such condensates, a rigorous characterization of the physics of phase separation in transcription remains to be done. In this review, we discuss theoretical and experimental evidence for biomolecular condensates as dynamic regulators of transcription. Looking beyond, we highlight functional consequences for transcription factor dynamics and gene expression and discuss potential pitfalls of misclassifying biomolecular condensates as liquid droplets in the absence of a rigorous physical description.
```
</details>

<details><summary>[2] Targeting phase separation on enhancers induced by transcription factor complex formations as a new strategy for treating drug-resistant cancers — K. Takayama, S. Inoue (2022); cutoff-filter date 2022-10-03; doi:10.3389/fonc.2022.1024600</summary>

```text
[2] Targeting phase separation on enhancers induced by transcription factor complex formations as a new strategy for treating drug-resistant cancers
    id: s2:66ab67f8ce18e050e89663dc3f7d5f8e2ecf0401
    date: 2022-10-03
    venue: Frontiers in Oncology
    authors: K. Takayama, S. Inoue
    abstract: The limited options for treating patients with drug-resistant cancers have emphasized the need to identify alternative treatment targets. Tumor cells have large super-enhancers (SEs) in the vicinity of important oncogenes for activation. The physical process of liquid-liquid phase separation (LLPS) contributes to the assembly of several membrane-less organelles in mammalian cells. Intrinsically disordered regions (IDRs) of proteins induce LLPS formation by developing condensates. It was discovered that key transcription factors (TFs) undergo LLPS in SEs. In addition, TFs play critical roles in the epigenetic and genetic regulation of cancer progression. Recently, we revealed the essential role of disease-specific TF collaboration changes in advanced prostate cancer (PC). OCT4 confers epigenetic changes by promoting complex formation with TFs, such as Forkhead box protein A1 (FOXA1), androgen receptor (AR) and Nuclear respiratory factor 1 (NRF1), inducing PC progression. It was demonstrated that TF collaboration through LLPS underlying transcriptional activation contributes to cancer aggressiveness and drug resistance. Moreover, the disruption of TF-mediated LLPS inhibited treatment-resistant PC tumor growth. Therefore, we propose that repression of TF collaborations involved in the LLPS of SEs could be a promising strategy for advanced cancer therapy. In this article, we summarize recent evidence highlighting the formation of LLPS on enhancers as a potent therapeutic target in advanced cancers.
```
</details>

<details><summary>[3] The oncogenic transcription factor FUS-CHOP can undergo nuclear liquid-liquid phase separation — Izzy Owen, Debra S. Yee, Hala Wyne, T. M. Perdikari et al. (2021); cutoff-filter date 2021-02-24; doi:10.1101/2021.02.24.432743</summary>

```text
[3] The oncogenic transcription factor FUS-CHOP can undergo nuclear liquid-liquid phase separation
    id: s2:9bbea21b2282d4b162b230e38471bac0535cef25
    date: 2021-02-24
    venue: bioRxiv (preprint)
    authors: Izzy Owen, Debra S. Yee, Hala Wyne, T. M. Perdikari, Victoria Johnson, Jeremy T. Smyth, Robert L. Kortum, N. Fawzi
    abstract: Myxoid liposarcoma is caused by a chromosomal translocation resulting in a fusion protein comprised of the N-terminus of FUS (fused in sarcoma) and the full-length transcription factor CHOP (CCAAT/Enhancer Binding Protein Homologous Protein). FUS functions in RNA metabolism and CHOP is a stress-induced transcription factor. The FUS-CHOP fusion protein causes unique gene expression and oncogenic transformation. The FUS segment is required for oncogenic transformation, but the mechanism of FUS-CHOP-induced transcriptional activation is unknown. Recently, some transcription factors and super enhancers were proposed to undergo liquid-liquid phase separation and form membraneless compartments that recruit transcription machinery to gene promoters. Since phase separation of FUS depends on its N-terminus, transcriptional activation by FUS-CHOP could result from the N-terminus driving nuclear phase transitions. Here, we characterized FUS-CHOP in cells and in vitro, and observed novel phase-separating properties relative to unmodified CHOP. Our data indicate FUS-CHOP forms phase-separated condensates at super enhancer transcriptional sites. We provide strong evidence that the FUS-CHOP phase transition is a novel oncogenic mechanism and potential therapeutic target for treatment of myxoid liposarcoma.
```
</details>

<details><summary>[4] A Prion-like Domain in Transcription Factor EBF1 Promotes Phase Separation and Enables B Cell Programming of Progenitor Chromatin. — Yuanting Wang, N. Zolotarev, Cheng-Yuan Yang, Angelika S. Rambold et al. (2020); cutoff-filter date 2020-11-06; doi:10.1016/j.immuni.2020.10.009</summary>

```text
[4] A Prion-like Domain in Transcription Factor EBF1 Promotes Phase Separation and Enables B Cell Programming of Progenitor Chromatin.
    id: s2:168c8eb18b786567aecc04cd906b9ffbb0f2d475
    date: 2020-10-30
    venue: Immunity
    authors: Yuanting Wang, N. Zolotarev, Cheng-Yuan Yang, Angelika S. Rambold, Gerhard Mittler, R. Grosschedl
    abstract: Establishment of B-lineage-specific gene expression requires the binding of transcription factors to inaccessible chromatin of progenitors. The transcription factor EBF1 can bind genomic regions prior to the detection of chromatin accessibility in a manner dependent on EBF1's C-terminal domain (CTD) and independent of cooperating transcription factors. Here, we studied the mechanism whereby the CTD enables this pioneering function. The CTD of EBF1 was dispensable for initial chromatin targeting but stabilized occupancy via recruitment of the chromatin remodeler Brg1. We found that the CTD harbors a prion-like domain (PLD) with an ability of liquid-liquid phase separation, which was enhanced by interaction of EBF1 with the RNA-binding protein FUS. Brg1 also partitioned into phase-separated FUS condensates and coincided with EBF1 and FUS foci in pro-B cells. Heterologous PLDs conferred pioneering function on EBF1ΔCTD. Thus, the phase separation ability of EBF1 facilitates Brg1-mediated chromatin opening and the transition of naive progenitor chromatin to B-lineage-committed chromatin.
```
</details>

<details><summary>[5] Mitotic Implantation of the Transcription Factor Prospero via Phase Separation Drives Terminal Neuronal Differentiation. — Xiaodan Liu, Jingwen Shen, Leiming Xie, Zelin Wei et al. (2019); cutoff-filter date 2019-12-19; doi:10.1016/j.devcel.2019.11.019</summary>

```text
[5] Mitotic Implantation of the Transcription Factor Prospero via Phase Separation Drives Terminal Neuronal Differentiation.
    id: s2:b3ec93881f818c30d2ba287f541ef367abc85663
    date: 2019-12-11
    venue: Developmental Cell
    authors: Xiaodan Liu, Jingwen Shen, Leiming Xie, Zelin Wei, Chouin Wong, Yiyao Li, Xinhe Zheng, Pilong Li
    abstract: Compacted heterochromatin blocks are prevalent in differentiated cells and present a barrier to cellular reprogramming. It remains obscure how heterochromatin remodeling is orchestrated during cell differentiation. Here we find that the evolutionarily conserved homeodomain transcription factor Prospero (Pros)/Prox1 ensures neuronal differentiation by driving heterochromatin domain condensation and expansion. Intriguingly, in mitotically dividing Drosophila neural precursors, Pros is retained at H3K9me3+ pericentromeric heterochromatin regions of chromosomes via liquid-liquid phase separation (LLPS). During mitotic exit of neural precursors, mitotically retained Pros recruits and concentrates heterochromatin protein 1 (HP1) into phase-separated condensates and drives heterochromatin compaction. This establishes a transcriptionally repressive chromatin environment that guarantees cell-cycle exit and terminal neuronal differentiation. Importantly, mammalian Prox1 employs a similar "mitotic-implantation-ensured heterochromatin condensation" strategy to reinforce neuronal differentiation. Together, our results unveiled a new paradigm whereby mitotic implantation of a transcription factor via LLPS remodels H3K9me3+ heterochromatin and drives timely and irreversible terminal differentiation.
```
</details>

<details><summary>[6] Phytochrome B inhibits the activity of phytochrome-interacting factor 7 involving phase separation. — Yu Xie, Wenbo Liu, Wenjing Liang, Xiaobin Ling et al. (2023); cutoff-filter date 2023-12-09; doi:10.1016/j.celrep.2023.113562</summary>

```text
[6] Phytochrome B inhibits the activity of phytochrome-interacting factor 7 involving phase separation.
    id: s2:3045bdaf216ad76b5678b5bba4ea5c52153b7a39
    date: 2023-12-01
    venue: Cell Reports
    authors: Yu Xie, Wenbo Liu, Wenjing Liang, Xiaobin Ling, Jinbiao Ma, Chuanwei Yang, Lin Li
    abstract: Shade-intolerant plants sense changes in the light environment and trigger shade-avoidance syndrome in the presence of neighboring vegetation. Phytochrome-interacting factor 7 (PIF7) is an essential regulator that integrates shade signals into plant transcriptional networks. While the regulation of PIF7 under shade conditions has been well studied, the mechanism that represses PIF7 activity under white light remains ambiguous. Here, we report that PIF7 forms nuclear puncta containing phase-separated liquid-like condensates. Phytochrome B (phyB) then binds to dephosphorylated PIF7 and promotes its condensed phase of PIF7 under white light. The phyB-PIF7 condensate subsequently inhibits the DNA-binding activity of PIF7. However, shade inactivation of phyB causes the dissociation of phyB-PIF7 condensates and allows unbound PIF7 to promote the transcription of shade-induced genes. This reversible transcriptional condensation via phase separation provides sessile organisms with the flexibility of gene control to adapt to their surrounding environment.
```
</details>

<details><summary>[7] **KEY** Transcription factors activate genes through the phase separation capacity of their activation domains — Ann Boija, Isaac A. Klein, Benjamin R. Sabari, Alessandra Dall’Agnese et al. (2018); cutoff-filter date 2018-11-15; doi:10.1016/j.cell.2018.10.042</summary>

```text
[7] Transcription factors activate genes through the phase separation capacity of their activation domains
    id: s2:e4f0debfff8b369862f80cc3adec3518a77760c0
    date: 2018-11-15
    venue: Cell
    authors: Ann Boija, Isaac A. Klein, Benjamin R. Sabari, Alessandra Dall’Agnese, Eliot L. Coffey, A. V. Zamudio, Charles H. Li, K. Shrinivas
    abstract: Gene expression is controlled by transcription factors (TFs) that consist of DNA-binding domains (DBDs) and activation domains (ADs). The DBDs have been well-characterized, but little is known about the mechanisms by which ADs effect gene activation. Here we report that diverse ADs form phase-separated condensates with the Mediator coactivator. For the OCT4 and GCN4 TFs, we show that the ability to form phase-separated droplets with Mediator in vitro and the ability to activate genes in vivo are dependent on the same amino acid residues. For the estrogen receptor (ER), a ligand-dependent activator, we show that estrogen enhances phase separation with Mediator, again linking phase separation with gene activation. These results suggest that diverse TFs can interact with Mediator through the phase-separating capacity of their ADs and that formation of condensates with Mediator is involved in gene activation.
```
</details>

<details><summary>[8] Poly(ADP-ribosylation) of P-TEFb by PARP1 disrupts phase separation to inhibit global transcription upon DNA damage — Huanyi Fu, Rongdiao Liu, Zixuan Jia, Ran Li et al. (2022); cutoff-filter date 2022-04-07; doi:10.1038/s41556-022-00872-5</summary>

```text
[8] Poly(ADP-ribosylation) of P-TEFb by PARP1 disrupts phase separation to inhibit global transcription upon DNA damage
    id: s2:269ade24b176156a20409508034bd3dd0cf94171
    date: 2022-04-01
    venue: Nature Cell Biology
    authors: Huanyi Fu, Rongdiao Liu, Zixuan Jia, Ran Li, Feifeng Zhu, Wenxuan Zhu, Yangqing Shao, Yiyang Jin
    abstract: DNA damage shuts down genome-wide transcription to prevent transcriptional mutagenesis and to initiate repair signalling, but the mechanism to stall elongating RNA polymerase II (Pol II) is not fully understood. Central to the DNA damage response, poly(ADP-ribose) polymerase 1 (PARP1) initiates DNA repair by translocating to the lesions where it catalyses protein poly(ADP-ribosylation). Here we report that PARP1 inhibits Pol II elongation by inactivating the transcription elongation factor P-TEFb, a CDK9–cyclin T1 (CycT1) heterodimer. After sensing damage, the activated PARP1 binds to transcriptionally engaged P-TEFb and modifies CycT1 at multiple positions, including histidine residues that are rarely used as an acceptor site. This prevents CycT1 from undergoing liquid–liquid phase separation that is required for CDK9 to hyperphosphorylate Pol II and to stimulate elongation. Functionally, poly(ADP-ribosylation) of CycT1 promotes DNA repair and cell survival. Thus, the P-TEFb–PARP1 signalling plays a protective role in transcription quality control and genomic stability maintenance after DNA damage. Fu, et al. report that PARP1-dependent poly(ADP-ribsoyl)ation of the P-TEFb subunit CycT1 suppresses its phase separation, which prevents its interaction partner CDK9 from hyperphosphorylating RNA polymerase II and thereby blocks transcription.
```
</details>

<details><summary>[9] Liquid-liquid phase separation of light-inducible transcription factors increases transcription activation in mammalian cells and mice — Nils Schneider, Franz-Georg Wieland, Deqiang Kong, A. Fischer et al. (2021); cutoff-filter date 2021-01-01; doi:10.1126/sciadv.abd3568</summary>

```text
[9] Liquid-liquid phase separation of light-inducible transcription factors increases transcription activation in mammalian cells and mice
    id: s2:3df6dcfd2196421468c12488b5b545dee5817682
    date: 2021-01-01
    venue: Science Advances
    authors: Nils Schneider, Franz-Georg Wieland, Deqiang Kong, A. Fischer, M. Hörner, J. Timmer, Haifeng Ye, W. Weber
    abstract: Engineering liquid-liquid phase separation into synthetic and optogenetic transcription factors increases gene expression. Light-inducible gene switches represent a key strategy for the precise manipulation of cellular events in fundamental and applied research. However, the performance of widely used gene switches is limited due to low tissue penetrance and possible phototoxicity of the light stimulus. To overcome these limitations, we engineer optogenetic synthetic transcription factors to undergo liquid-liquid phase separation in close spatial proximity to promoters. Phase separation of constitutive and optogenetic synthetic transcription factors was achieved by incorporation of intrinsically disordered regions. Supported by a quantitative mathematical model, we demonstrate that engineered transcription factor droplets form at target promoters and increase gene expression up to fivefold. This increase in performance was observed in multiple mammalian cells lines as well as in mice following in situ transfection. The results of this work suggest that the introduction of intrinsically disordered domains is a simple yet effective means to boost synthetic transcription factor activity.
```
</details>

<details><summary>[10] Regulated splicing of large exons is linked to phase‐separation of vertebrate transcription factors — Toshihiko Kawachi, A. Masuda, Y. Yamashita, Jun-ichi Takeda et al. (2021); cutoff-filter date 2021-10-04; doi:10.15252/embj.2020107485</summary>

```text
[10] Regulated splicing of large exons is linked to phase‐separation of vertebrate transcription factors
    id: s2:4ca78a852bca09a32a1a4751af0b05de664720f1
    date: 2021-10-04
    venue: EMBO Journal
    authors: Toshihiko Kawachi, A. Masuda, Y. Yamashita, Jun-ichi Takeda, B. Ohkawara, Mikako Ito, K. Ohno
    abstract: Although large exons cannot be readily recognized by the spliceosome, many are evolutionarily conserved and constitutively spliced for inclusion in the processed transcript. Furthermore, whether large exons may be enriched in a certain subset of proteins, or mediate specific functions, has remained unclear. Here, we identify a set of nearly 3,000 SRSF3‐dependent large constitutive exons (S3‐LCEs) in human and mouse cells. These exons are enriched for cytidine‐rich sequence motifs, which bind and recruit the splicing factors hnRNP K and SRSF3. We find that hnRNP K suppresses S3‐LCE splicing, an effect that is mitigated by SRSF3 to thus achieve constitutive splicing of S3‐LCEs. S3‐LCEs are enriched in genes for components of transcription machineries, including mediator and BAF complexes, and frequently contain intrinsically disordered regions (IDRs). In a subset of analyzed S3‐LCE‐containing transcription factors, SRSF3 depletion leads to deletion of the IDRs due to S3‐LCE exon skipping, thereby disrupting phase‐separated assemblies of these factors. Cytidine enrichment in large exons introduces proline/serine codon bias in intrinsically disordered regions and appears to have been evolutionarily acquired in vertebrates. We propose that layered splicing regulation by hnRNP K and SRSF3 ensures proper phase‐separation of these S3‐LCE‐containing transcription factors in vertebrates.
```
</details>

<details><summary>Post-hoc automated audit — NON-AUTHORITATIVE; uses hidden benchmark annotations</summary>

- primary auditor: `silence_as_null_error`; statuses {'H1': 'indeterminate', 'H2': 'positive_or_present'}; discriminative=False
- primary reasoning: H2 explicitly predicts that phase separation facilitates Mediator recruitment to active gene loci, as it posits co-condensation as a mechanism for transcriptional activation. H1, which centers on soluble complexes, does not address phase separation or its role in Mediator recruitment, so it is indeterminate regarding this proposition.
- derived opposition call: `one_sided_silence_labelled_neutral`
- evidence attribution: `informative_evidence_found` — The retrieval system surfaced a paper (Record [7]) that directly addresses the proposition, showing that transcription factor activation domains form phase-separated condensates with Mediator and that this interaction is linked to gene activation. The assessor correctly identified this as supporting evidence. The process worked as intended, with relevant evidence found and used.
- disagreement flags: {'second_rater_vs_primary_discriminative': None, 'second_rater_vs_primary_status': None, 'retest_vs_primary_category': None, 'any': False}
</details>

**Human review** — `compatible_non_discriminative` · reviewer: Research Director · source: D045 · status: `first_pass_model_based_review` · genuinely discriminative: False · silence-as-null error: False · other fields not recorded

---

## #18 · `GP1-glnbp_induced_fit_vs_conformational_selection-X15`

**GP1-glnbp_induced_fit_vs_conformational_selection-X15** — case `glnbp_induced_fit_vs_conformational_selection`, node `X15`

> Ligand binding induces a conformational change from open to closed in substrate-binding proteins.

- generated from **H2** (Candidate A); abstraction: `mechanistic`
- generator's stated reason: The claim describes ligand binding as the event that triggers the conformational change, implying a mechanistic coupling between binding and structural transition.
- influence: **0.276** (rank 5 in case, 18 overall; cumulative 53%) — favours **H2**
- log-likelihood contribution: H2 +1.991, H1 +1.715
- removing it alone: evidence withheld → case log-odds +1.565 (ranking unchanged); node deleted → +1.565 (ranking unchanged)

**Hypotheses (as shown to the verifier)**

- **H1** (Candidate B): Apo-GlnBP samples a pre-existing binding-competent closed or semi-closed conformation; glutamine preferentially binds/captures that pre-existing conformation.
- **H2** (Candidate A): Glutamine binds to open/binding-competent GlnBP before the major protein conformational rearrangement, after which GlnBP closes around the ligand.

**Verifier cross-hypothesis judgments** — P(X|H) combines these by noisy-OR

| hypothesis | origin? | direct edge | route via parent | P(X\|H) |
| --- | --- | --- | --- | --- |
| H2 | yes | `strongly_implied` | X2 [H→parent `strongly_implied`, P=0.95] → `implied` | 0.989 |
| H1 | no | `unlikely` | X2 [H→parent `unlikely`, P=0.30] → `implied` | 0.713 |

- edge rationale, **H2** → node: Candidate A explicitly states that ligand binding is followed by a major conformational rearrangement from open to closed, directly supporting the proposition.
- edge rationale, **H1** → node: Candidate B suggests that the protein already samples closed conformations before ligand binding, implying that ligand binding does not induce the conformational change but rather selects for it.
- parent `X2`: Ligand binding to a substrate-binding protein occurs before the major conformational change that closes the protein around the ligand.
- chain rationale, `X2` → node: The parent proposition establishes that ligand binding precedes a conformational change, which suggests but does not guarantee that binding induces the change.

**Verifier evidence** — label used in score: `strong_support` (log-LR +2.0)

- queries: `ligand substrate-binding protein conformation`; `substrate-binding protein open closed structure`
- assessor rationale: Multiple records directly state that ligand binding induces a conformational change from open to closed in substrate-binding proteins. Record [6] explicitly describes the open-to-closed transition upon ligand binding. Record [4] details the open conformation in the absence of ligand and closed conformation when ligand is bound. Record [10] discusses structural rearrangement between open and closed conformations dependent on substrate binding. These are independent studies using structural and simulation methods, directly supporting the proposition.
- supporting spans cited by the assessor:
  - "The open state switches to the closed one upon the binding of ligands, brought about by the two critical helices."
  - "The SBD2 domain of the glutamine (GLN) transporter from bacteria consists of two domains D1 and D2 that bind GLN in the space between the domains in a closed conformation. In the absence of ligand, SBD2 adopts an open conformation with increased domain distance."
  - "Comparison with the previously reported crystal structure indicates that the a′ domain partially masks the binding surface of the b′ domain, causing steric hindrance against the peptide in the reduced form of the b′–a′ domains that exhibits a closed conformation. These findings provide a structural basis for the mechanism underlying the redox-dependent substrate binding of PDI."
- 10 papers shown; key papers: `s2:6d0a309f616b17b23689f21fd6e38c0c745969d8`, `s2:a6d9e182bdaf8f0592a90085680292608a95f2ec`, `s2:e858b1b4acb255474166ef197359666f99ab289a`
- _The evidence assessor returns ONE label for the node from all papers shown; the method has no per-paper contribution. Key papers and spans are those the assessor cited._

<details><summary>[1] Resolving Protein Conformational Plasticity and Substrate Binding via Machine Learning. — N. Ahalawat, Mohammad Sahil, Jagannath Mondal (2023); cutoff-filter date 2023-04-17; doi:10.1021/acs.jctc.2c00932</summary>

```text
[1] Resolving Protein Conformational Plasticity and Substrate Binding via Machine Learning.
    id: s2:a2bfba9f1cf4c8e1ebe66bd74deb5ac5c0254612
    date: 2023-04-17
    venue: Journal of Chemical Theory and Computation
    authors: N. Ahalawat, Mohammad Sahil, Jagannath Mondal
    abstract: A long-standing target in elucidating the biomolecular recognition process is the identification of binding-competent conformations of the receptor protein. However, protein conformational plasticity and the stochastic nature of the recognition processes often preclude the assignment of a specific protein conformation to an individual ligand-bound pose. Here, we demonstrate that a computational framework coined as RF-TICA-MD, which integrates an ensemble decision-tree-based Random Forest (RF) machine learning (ML) technique with an unsupervised dimension reduction approach time-structured independent component analysis (TICA), provides an efficient and unambiguous solution toward resolving protein conformational plasticity and the substrate binding process. In particular, we consider multimicrosecond-long molecular dynamics (MD) simulation trajectories of a ligand recognition process in solvent-inaccessible cavities of archetypal proteins T4 lysozyme and cytochrome P450cam. We show that in a scenario in which clear correspondence between protein conformation and binding-competent macrostates could not be obtained via an unsupervised dimension reduction approach, an a priori decision-tree-based supervised classification of the simulated recognition trajectories via RF would help characterize key amino acid residue pairs of the protein that are deemed sensitive for ligand binding. A subsequent unsupervised dimensional reduction of the selected residue pairs via TICA would then delineate a conformational landscape of protein which is able to demarcate ligand-bound poses from unbound ones. The proposed RF-TICA-MD approach is shown to be data agnostic and found to be robust when using other ML-based classification methods such as XGBoost. As a promising spinoff of the protocol, the framework is found to be capable of identifying distal protein locations which would be allosterically important for ligand binding and would characterize their roles in recognition pathways. [...]
```
</details>

<details><summary>[2] Structural characterization of the Streptococcus pneumoniae carbohydrate substrate-binding protein SP0092 — S. Culurgioni, M. Tang, M. Walsh (2017); cutoff-filter date 2017-01-01; doi:10.1107/s2053230x16020252</summary>

```text
[2] Structural characterization of the Streptococcus pneumoniae carbohydrate substrate-binding protein SP0092
    id: s2:b8a555bfe35e295c82eb9b86a3df4f4f1657280d
    date: 2017-01-01
    venue: Acta Crystallographica Section F Structural Biology Communications
    authors: S. Culurgioni, M. Tang, M. Walsh
    abstract: The crystal structure of SP0092 was determined at 1.61 Å resolution and reveals a domain-swapped dimer with the monomer subunit in a closed conformation in the absence of ligand.
```
</details>

<details><summary>[3] Identification of multiple substrate binding sites in SLC4 transporters in the outward-facing conformation: Insights into the transport mechanism — Hristina R. Zhekova, A. Pushkin, Gülru Kayık, Liyo Kao et al. (2021); cutoff-filter date 2021-01-31; doi:10.1016/j.jbc.2021.100724</summary>

```text
[3] Identification of multiple substrate binding sites in SLC4 transporters in the outward-facing conformation: Insights into the transport mechanism
    id: s2:94ac44053f4f8c09844ae616a13316ee6fae0082
    date: 2021-01-01
    venue: Journal of Biological Chemistry
    authors: Hristina R. Zhekova, A. Pushkin, Gülru Kayık, Liyo Kao, R. Azimov, N. Abuladze, D. Kurtz, Mirna Damergi
    abstract: Solute carrier family 4 (SLC4) transporters mediate the transmembrane transport of HCO3−, CO32−, and Cl− necessary for pH regulation, transepithelial H+/base transport, and ion homeostasis. Substrate transport with varying stoichiometry and specificity is achieved through an exchange mechanism and/or through coupling of the uptake of anionic substrates to typically co-transported Na+. Recently solved outward-facing structures of two SLC4 members (human anion exchanger 1 [hAE1] and human electrogenic sodium bicarbonate cotransporter 1 [hNBCe1]) with different transport modes (Cl−/HCO3− exchange versus Na+-CO32− symport) revealed highly conserved three-dimensional organization of their transmembrane domains. However, the exact location of the ion binding sites and their protein–ion coordination motifs are still unclear. In the present work, we combined site identification by ligand competitive saturation mapping and extensive molecular dynamics sampling with functional mutagenesis studies which led to the identification of two substrate binding sites (entry and central) in the outward-facing states of hAE1 and hNBCe1. Mutation of residues in the identified binding sites led to impaired transport in both proteins. We also showed that R730 in hAE1 is crucial for anion binding in both entry and central sites, whereas in hNBCe1, a Na+ acts as an anchor for CO32− binding to the central site. Additionally, protonation of the central acidic residues (E681 in hAE1 and D754 in hNBCe1) alters the ion dynamics in the permeation cavity and may contribute to the transport mode differences in SLC4 proteins. These results provide a basis for understanding the functional differences between hAE1 and hNBCe1 and may facilitate potential drug development for diseases such as proximal and distal renal tubular acidosis.
```
</details>

<details><summary>[4] **KEY** Ligand binding and global adaptation of the GlnPQ substrate binding domain 2 revealed by molecular dynamics simulations — Maximilian Kienlein, M. Zacharias (2020); cutoff-filter date 2020-10-18; doi:10.1002/pro.3981</summary>

```text
[4] Ligand binding and global adaptation of the GlnPQ substrate binding domain 2 revealed by molecular dynamics simulations
    id: s2:a6d9e182bdaf8f0592a90085680292608a95f2ec
    date: 2020-10-18
    venue: Protein Science
    authors: Maximilian Kienlein, M. Zacharias
    abstract: Substrate‐binding domains (SBD) are important structural elements of substrate transporters mediating the transport of essential molecules across the cell membrane. The SBD2 domain of the glutamine (GLN) transporter from bacteria consists of two domains D1 and D2 that bind GLN in the space between the domains in a closed conformation. In the absence of ligand, SBD2 adopts an open conformation with increased domain distance. In molecular dynamics (MD) simulations in the absence of ligands, no closing of the open conformation was observed on the MD time scale. Addition of GLN resulted in several reversible binding and unbinding events of GLN at the binding site on the D1 domain but did not induce domain closing indicating that binding and global domain closing do not occur simultaneously. The SBD2 structure remained in a closed state when starting from the GLN‐bound closed crystal structure and opened quickly to reach the open state upon removal of the GLN ligand. Free energy simulations to induce opening to closing indicated a barrier for closing in the absence and presence of ligand and a significant penalty for closing without GLN in the binding pocket. Simulations of a Leu480Ala mutation also indicate that an interaction of a C‐terminal D1‐tail471‐484 with a D2‐helix418‐427 (not contacting the substrate‐binding region) plays a decisive role for controlling the barrier of conformational switching in the SBD2 protein. The results allow us to derive a model of the molecular mechanism of substrate binding to SBD2 and associated conformational changes.
```
</details>

<details><summary>[5] Noncanonical role for the binding protein in substrate uptake by the MetNI methionine ATP Binding Cassette (ABC) transporter — P. Nguyễn, J. Y. Lai, A. T. Lee, J. Kaiser et al. (2018); cutoff-filter date 2018-10-23; doi:10.1073/pnas.1811003115</summary>

```text
[5] Noncanonical role for the binding protein in substrate uptake by the MetNI methionine ATP Binding Cassette (ABC) transporter
    id: s2:8620a0ad659143ca35b6176d50b5322b27c42853
    date: 2018-10-23
    venue: Proceedings of the National Academy of Sciences of the United States of America
    authors: P. Nguyễn, J. Y. Lai, A. T. Lee, J. Kaiser, D. Rees
    abstract: Significance The high-affinity methionine importer MetNI belongs to the ATP Binding Cassette (ABC) family of transporters that carry out the ATP-dependent uptake of substrates into cells. As with other ABC importers, MetNI requires a soluble binding protein (MetQ) that in the canonical mechanistic model delivers substrates to the transporter. We made the unexpected observation that a MetQ variant with significantly impaired ligand-binding properties supports d-selenomethionine uptake at a higher rate than wild-type MetQ. A crystal structure of MetNIQ in the outward-facing conformation reveals access channels through the binding protein to the transmembrane translocation pathway. These studies support a noncanonical role for the binding protein in facilitating the uptake of certain substrates directly through the transporter–binding protein complex. The Escherichia coli methionine ABC transporter MetNI exhibits both high-affinity transport toward l-methionine and broad specificity toward methionine derivatives, including d-methionine. In this work, we characterize the transport of d-methionine derivatives by the MetNI transporter. Unexpectedly, the N229A substrate-binding deficient variant of the cognate binding protein MetQ was found to support high MetNI transport activity toward d-selenomethionine. We determined the crystal structure at 2.95 Å resolution of the ATPγS-bound MetNIQ complex in the outward-facing conformation with the N229A apo MetQ variant. This structure revealed conformational changes in MetQ providing substrate access through the binding protein to the transmembrane translocation pathway. MetQ likely mediates uptake of methionine derivatives through two mechanisms: in the methionine-bound form delivering substrate from the periplasm to the transporter (the canonical mechanism) and in the apo form by facilitating ligand binding when complexed to the transporter (the noncanonical mechanism). This dual role for substrate-binding proteins is proposed [...]
```
</details>

<details><summary>[6] **KEY** Alternative conformation induced by substrate binding for Arabidopsis thalianaN6-methyl-AMP deaminase — Q. Jia, W. Xie (2019); cutoff-filter date 2019-02-05; doi:10.1093/nar/gkz070</summary>

```text
[6] Alternative conformation induced by substrate binding for Arabidopsis thalianaN6-methyl-AMP deaminase
    id: s2:6d0a309f616b17b23689f21fd6e38c0c745969d8
    date: 2019-02-05
    venue: Nucleic Acids Research
    authors: Q. Jia, W. Xie
    abstract: Abstract Adenosine deaminase is involved in adenosine degradation and salvage pathway, and plays important physiological roles in purine metabolism. Recently, a novel type of adenosine deaminase-like protein has been identified, which displays deamination activity toward N6-methyl-adenosine monophosphate but not adenosine or AMP, and was consequently named N6-methyl-AMP deaminase (MAPDA). The underlying structural basis of MAPDA recognition and catalysis is poorly understood. Here, we present the crystal structures of MAPDA from Arabidopsis thaliana in the free and in the ligand-bound forms. The protein contains a conserved (β/α)8 Tim-barrel domain and a typical zinc-binding site, but it also exhibits idiosyncratic local differences for two flexible helices important for substrate binding. The extensive interactions between the N6-methyl-AMP substrate or the inosine monophosphate product and the enzyme were identified, and subsequently evaluated by the deamination activity assays. Importantly, each structure reported here represents a different stage of the catalytic pathway and their structural differences suggested that the enzyme can exist in two distinct conformational states. The open state switches to the closed one upon the binding of ligands, brought about by the two critical helices. Our structural studies provide the first look of this important metabolic enzyme and shed lights on its catalytic pathway, which holds promise for the structure-based drug design for MAPDA-related diseases.
```
</details>

<details><summary>[7] Crystal Structures of the Choline/Acetylcholine Substrate-binding Protein ChoX from Sinorhizobium meliloti in the Liganded and Unliganded-Closed States* — C. Oswald, S. Smits, Marina Höing, Linda Sohn-Bösser et al. (2008); cutoff-filter date 2008-11-21; doi:10.1074/jbc.m806021200</summary>

```text
[7] Crystal Structures of the Choline/Acetylcholine Substrate-binding Protein ChoX from Sinorhizobium meliloti in the Liganded and Unliganded-Closed States*
    id: s2:a49bb0ba969d90a0daa80d930119c57b37631cb4
    date: 2008-11-21
    venue: Journal of Biological Chemistry
    authors: C. Oswald, S. Smits, Marina Höing, Linda Sohn-Bösser, Laurence Dupont, Daniel Le Rudulier, L. Schmitt, E. Bremer
    abstract: The ATP-binding cassette transporter ChoVWX is one of several choline import systems operating in Sinorhizobium meliloti. Here fluorescence-based ligand binding assays were used to quantitate substrate binding by the periplasmic ligand-binding protein ChoX. These data confirmed that ChoX recognizes choline and acetylcholine with high and medium affinity, respectively. We also report the crystal structures of ChoX in complex with either choline or acetylcholine. These structural investigations revealed an architecture of the ChoX binding pocket and mode of substrate binding similar to that reported previously for several compatible solute-binding proteins. Additionally the ChoX-acetylcholine complex permitted a detailed structural comparison with the carbamylcholine-binding site of the acetylcholine-binding protein from the mollusc Lymnaea stagnalis. In addition to the two liganded structures of ChoX, we were also able to solve the crystal structure of ChoX in a closed, substrate-free conformation that revealed an architecture of the ligand-binding site that is superimposable to the closed, ligand-bound form of ChoX. This structure is only the second of its kind and raises the important question of how ATP-binding cassette transporters are capable of distinguishing liganded and unliganded-closed states of the binding protein.
```
</details>

<details><summary>[8] Free-Energy Landscape Analysis of Protein-Ligand Binding: The Case of Human Glutathione Transferase A1 — Adrien Nicolaï, Nicolas Petiot, Paul Grassein, P. Delarue et al. (2022); cutoff-filter date 2022-08-16; doi:10.3390/app12168196</summary>

```text
[8] Free-Energy Landscape Analysis of Protein-Ligand Binding: The Case of Human Glutathione Transferase A1
    id: s2:55b9b8c9620fbb5d8bc45a66d5f543ba31f6aa1e
    date: 2022-08-16
    venue: Applied Sciences
    authors: Adrien Nicolaï, Nicolas Petiot, Paul Grassein, P. Delarue, F. Neiers, P. Senet
    abstract: Glutathione transferases (GSTs) are a superfamily of enzymes which have in common the ability to catalyze the nucleophilic addition of the thiol group of reduced glutathione (GSH) onto electrophilic and hydrophobic substrates. This conjugation reaction, which occurs spontaneously but is dramatically accelerated by the enzyme, protects cells against damages caused by harmful molecules. With some exceptions, GSTs are catalytically active as homodimers, with monomers generally constituted of 200 to 250 residues organized into two subdomains. The first is the N-terminal subdomain, which contains an active site named G site, where GSH is hosted in catalytic conformation and which is generally highly conserved among GSTs. The second subdomain, hydrophobic, which binds the substrate counterpart (H site), can vary from one GST to another, resulting in structures able to recognize different substrates. In the present work, we performed all-atom molecular dynamics simulations in explicit solvent of human GSTA1 in its APO form, bound to GSH ligand and bound to GS-conjugated ligand. From MD, two probes were analyzed to (i) decipher the local conformational changes induced by the presence of the ligand and (ii) map the communication pathways involved in the ligand-binding process. These two local probes are, first, coarse-grained angles (θ,γ), representing the local conformation of the protein main chain and, second, dihedral angles χ representing the local conformation of the amino-acid side chains. From the local probes time series, effective free-energy landscapes along the amino-acid sequence were analyzed and compared between the three different forms of GSTA1. This methodology allowed us to extract a network of 33 key residues, some of them being located in the experimentally well-known binding sites G and H of GSTA1 and others being located as far as 30Å from the original binding sites. Finally, the collective motions associated with the network of key residues were estab [...]
```
</details>

<details><summary>[9] Hijacking of a substrate-binding protein scaffold for use in mycobacterial cell wall biosynthesis. — Z. Marland, T. Beddoe, L. Zaker-Tabrizi, I. Lucet et al. (2006); cutoff-filter date 2006-06-16; doi:10.1016/j.jmb.2006.04.012</summary>

```text
[9] Hijacking of a substrate-binding protein scaffold for use in mycobacterial cell wall biosynthesis.
    id: s2:feb0c25b01c22232dac3bed2b68d7fcde54991cb
    date: 2006-06-16
    venue: Journal of Molecular Biology
    authors: Z. Marland, T. Beddoe, L. Zaker-Tabrizi, I. Lucet, Rajini Brammananth, J. Whisstock, M. Wilce, R. Coppel
    abstract: [no abstract available]
```
</details>

<details><summary>[10] **KEY** Structural basis of redox-dependent substrate binding of protein disulfide isomerase — M. Yagi-Utsumi, T. Satoh, Koichi Kato (2015); cutoff-filter date 2015-09-09; doi:10.1038/srep13909</summary>

```text
[10] Structural basis of redox-dependent substrate binding of protein disulfide isomerase
    id: s2:e858b1b4acb255474166ef197359666f99ab289a
    date: 2015-09-09
    venue: Scientific Reports
    authors: M. Yagi-Utsumi, T. Satoh, Koichi Kato
    abstract: Protein disulfide isomerase (PDI) is a multidomain enzyme, operating as an essential folding catalyst, in which the b′ and a′ domains provide substrate binding sites and undergo an open–closed domain rearrangement depending on the redox states of the a′ domain. Despite the long research history of this enzyme, three-dimensional structural data remain unavailable for its ligand-binding mode. Here we characterize PDI substrate recognition using α-synuclein (αSN) as the model ligand. Our nuclear magnetic resonance (NMR) data revealed that the substrate-binding domains of PDI captured the αSN segment Val37–Val40 only in the oxidized form. Furthermore, we determined the crystal structure of an oxidized form of the b′–a′ domains in complex with an undecapeptide corresponding to this segment. The peptide-binding mode observed in the crystal structure with NMR validation, was characterized by hydrophobic interactions on the b′ domain in an open conformation. Comparison with the previously reported crystal structure indicates that the a′ domain partially masks the binding surface of the b′ domain, causing steric hindrance against the peptide in the reduced form of the b′–a′ domains that exhibits a closed conformation. These findings provide a structural basis for the mechanism underlying the redox-dependent substrate binding of PDI.
```
</details>

<details><summary>Post-hoc automated audit — NON-AUTHORITATIVE; uses hidden benchmark annotations</summary>

- primary auditor: `generic_component_fact`; statuses {'H2': 'positive_or_present', 'H1': 'positive_or_present'}; discriminative=False
- primary reasoning: Both H2 (induced fit) and H1 (conformational selection) ultimately result in a conformational change from open to closed upon ligand binding, though the sequence of events differs. The proposition simply states that ligand binding induces a conformational change, which is consistent with both mechanisms.
- derived opposition call: `both_predict_same`
- evidence attribution: `informative_evidence_found` — The retrieved literature directly addresses the proposition, with multiple papers describing ligand-induced open-to-closed conformational changes in substrate-binding proteins. The assessor correctly identified and used this evidence. The process worked as intended.
- disagreement flags: {'second_rater_vs_primary_discriminative': None, 'second_rater_vs_primary_status': None, 'retest_vs_primary_category': None, 'any': False}
</details>

**Human review** — `generic_component_fact` · reviewer: Research Director · source: D045 · status: `first_pass_model_based_review` · genuinely discriminative: False · silence-as-null error: False · other fields not recorded

---

## #19 · `GP1-pfc_storage_vs_control-X15`

**GP1-pfc_storage_vs_control-X15** — case `pfc_storage_vs_control`, node `X15`

> Regions of the prefrontal cortex can directly store and represent information about items maintained in working memory.

- generated from **H1** (Candidate A); abstraction: `class`
- generator's stated reason: If persistent activity in prefrontal cortex encodes working memory content, then prefrontal regions generally have the capacity to store mnemonic representations.
- influence: **0.276** (rank 3 in case, 19 overall; cumulative 54%) — favours **H1**
- log-likelihood contribution: H1 +1.991, H2 +1.715
- removing it alone: evidence withheld → case log-odds +0.938 (ranking unchanged); node deleted → +0.938 (ranking unchanged)

**Hypotheses (as shown to the verifier)**

- **H1** (Candidate A): Prefrontal persistent activity is itself a substrate for working-memory storage; disrupting the relevant PFC population therefore disrupts the stored mnemonic representation.
- **H2** (Candidate B): PFC primarily controls, prioritizes, or allocates resources to working-memory representations maintained in sensory/posterior regions rather than directly storing the mnemonic content itself.

**Verifier cross-hypothesis judgments** — P(X|H) combines these by noisy-OR

| hypothesis | origin? | direct edge | route via parent | P(X\|H) |
| --- | --- | --- | --- | --- |
| H1 | yes | `strongly_implied` | X2 [H→parent `strongly_implied`, P=0.95] → `implied` | 0.989 |
| H2 | no | `unlikely` | X2 [H→parent `unlikely`, P=0.30] → `implied` | 0.713 |

- edge rationale, **H1** → node: If prefrontal persistent activity is the substrate for working-memory storage, then regions of the prefrontal cortex must directly store and represent information about items in working memory.
- edge rationale, **H2** → node: If PFC only controls or allocates resources to representations stored elsewhere, it is less likely that PFC regions directly store and represent working-memory content.
- parent `X2`: Persistent neural activity in prefrontal cortex encodes the content of items maintained in working memory.
- chain rationale, `X2` → node: If persistent neural activity in prefrontal cortex encodes working memory content, it suggests that prefrontal regions can represent and store such information, though it does not guarantee direct storage as opposed to encoding or processing.

**Verifier evidence** — label used in score: `strong_support` (log-LR +2.0)

- queries: `prefrontal cortex working memory representation`; `prefrontal cortex item storage`
- assessor rationale: Multiple independent studies directly report that neurons in regions of the prefrontal cortex actively encode, store, and represent information about items maintained in working memory. This is shown through persistent activity, sequential activation, and causal manipulations in both primate and rodent models, as well as in human studies using stimulation. The evidence spans spatial, object, and emotional working memory, and includes both behavioral and neurophysiological measures.
- supporting spans cited by the assessor:
  - "We thus tested the ability of neurons that do and do not generate persistent activity in the prefrontal cortex of monkeys to represent spatial and object information in working memory. Neurons that generated persistent activity represented more information about the stimuli in both spatial and object working memory tasks."
  - "These results reveal that prefrontal neurons that generate persistent activity maintain information more reliably during working memory."
  - "Here we demonstrate that microcircuits in layers 2/3 of the primate lateral prefrontal cortex dynamically represent memory content in a naturalistic task through sequential activation of single neurons."
  - "We found that the sequential activation of single neurons encoded trajectories to target locations held in working memory."
  - "Single neurons in PFC, and to a lesser extent neurons in VIP, actively encoded empty sets during the delay period."
  - "Moreover, PFC activity correlated better with behavioral performance in empty set trials."
  - "These findings suggest that the representation of null quantity in working memory relies more on prefrontal and less on parietal processing."
  - "Overall, our results show that empty sets are dynamically and distinctly represented in working memory."
  - "The findings indicate that anodal HD-tDCS over the L-DLPFC can effectively enhance the ability of memory representation towards threat information in highly avoidant individuals."
  - "This study extends causal research by showing that the L-DLPFC is an important brain region for hot WM representations."
  - "Our results indicate that neurons in the lateral prefrontal cortex causally encode working memory in naturalistic conditions via complex and temporally precise activation patterns."
  - "The present results suggest that mPFC neurons in rats are involved in encoding working memory, via increasing firing frequency or synchronization."
- 10 papers shown; key papers: `s2:0879bfe55c6d3e5f185431699966213d09a4a9b1`, `s2:1701014a2d3b0475328d8d6773c29a4cc1cdcdc5`, `s2:41340092edd6af4f43668284ddf61fe5e18bb1f3`, `s2:59031196c9d4e166d206b87d4f61f487d140c373`, `s2:8384a74f73349b764266c422767af534ef3da9ba`
- _The evidence assessor returns ONE label for the node from all papers shown; the method has no per-paper contribution. Key papers and spans are those the assessor cited._

<details><summary>[1] Parietal-driven visual working memory representation in occipito-temporal cortex — Yao-Da Xu (2023); cutoff-filter date 2023-09-22; doi:10.1016/j.cub.2023.08.080</summary>

```text
[1] Parietal-driven visual working memory representation in occipito-temporal cortex
    id: s2:565e1aa52cf942ae362e593afcbbbec7ea140ce1
    date: 2023-09-01
    venue: Current Biology
    authors: Yao-Da Xu
    abstract: Summary Human fMRI studies have documented extensively that the content of visual working memory (VWM) can be reliably decoded from fMRI voxel response patterns during the delay period in both the occipito-temporal cortex (OTC), including early visual areas (EVC), and posterior parietal cortex (PPC)1–4. Further work has revealed that VWM signal in OTC is largely sustained by feedback from associative areas such as prefrontal cortex and PPC4–9. It is unclear, however, if feedback during VWM simply restores sensory representations initially formed in OTC or if it can reshape the representational content of OTC during VWM delay. Taking advantage of a recent finding showing that object representational geometry differs between OTC and PPC in perception10, here we find that, during VWM delay, the object representational geometry in OTC becomes more aligned with that of PPC during perception than with itself during perception. This finding supports the role of feedback in shaping the content of VWM in OTC, with the VWM content of OTC more determined by information retained in PPC than by the sensory information initially encoded in OTC.
```
</details>

<details><summary>[2] Task-specific oscillatory synchronization of prefrontal cortex, nucleus reuniens, and hippocampus during working memory — J. G. de Mooij-van Malsen, Niels Röhrdanz, Anna-Sophia Buschhoff, T. Schiffelholz et al. (2023); cutoff-filter date 2023-08-02; doi:10.1016/j.isci.2023.107532</summary>

```text
[2] Task-specific oscillatory synchronization of prefrontal cortex, nucleus reuniens, and hippocampus during working memory
    id: s2:62eeab7e04d0fd25f850a4d7784063c0e5989916
    date: 2023-08-01
    venue: iScience
    authors: J. G. de Mooij-van Malsen, Niels Röhrdanz, Anna-Sophia Buschhoff, T. Schiffelholz, Torfi Sigurdsson, P. Wulff
    abstract: Summary Working memory requires maintenance of and executive control over task-relevant information on a timescale of seconds. Spatial working memory depends on interactions between hippocampus, for the representation of space, and prefrontal cortex, for executive control. A monosynaptic hippocampal projection to the prefrontal cortex has been proposed to serve this interaction. However, connectivity and inactivation experiments indicate a critical role of the nucleus reuniens in hippocampal-prefrontal communication. We have investigated the dynamics of oscillatory coherence throughout the prefrontal-hippocampal-reuniens network in a touchscreen-based working memory task. We found that coherence at distinct frequencies evolved depending on phase and difficulty of the task. During choice, the reuniens did not participate in enhanced prefrontal-hippocampal theta but in gamma coherence. Strikingly, the reuniens was strongly embedded in performance-related increases in beta coherence, suggesting the execution of top-down control. In addition, we show that during working memory maintenance the prefrontal-hippocampal-reuniens network displays performance-related delay activity.
```
</details>

<details><summary>[3] **KEY** Decoding working memory information from neurons with and without persistent activity in the primate prefrontal cortex. — Lilianna Thrower, Wen-Hao Dang, Rye G. Jaffe, Jasmine D. Sun et al. (2023); cutoff-filter date 2023-11-01; doi:10.1152/jn.00290.2023</summary>

```text
[3] Decoding working memory information from neurons with and without persistent activity in the primate prefrontal cortex.
    id: s2:59031196c9d4e166d206b87d4f61f487d140c373
    date: 2023-11-01
    venue: Journal of Neurophysiology
    authors: Lilianna Thrower, Wen-Hao Dang, Rye G. Jaffe, Jasmine D. Sun, Christos Constantinidis
    abstract: Persistent activity of neurons in the prefrontal cortex has been thought to represent the information maintained in working memory, though alternative models have challenged this idea. Theories that depend on the dynamic representation of information posit that stimulus information may be maintained by the activity pattern of neurons whose firing rate is not significantly elevated above their baseline during the delay period of working memory tasks. We thus tested the ability of neurons that do and do not generate persistent activity in the prefrontal cortex of monkeys to represent spatial and object information in working memory. Neurons that generated persistent activity represented more information about the stimuli in both spatial and object working memory tasks. The amount of information that could be decoded from neural activity depended on the choice of decoder and parameters used but neurons with persistent activity outperformed non-persistent neurons consistently. Although averaged across all neurons and stimuli, firing rate did not appear clearly elevated above baseline during the maintenance of neural activity particularly for object working memory, this grand average masked neurons that generated persistent activity selective for their preferred stimuli, which carried the majority of stimulus information. These results reveal that prefrontal neurons that generate persistent activity maintain information more reliably during working memory.
```
</details>

<details><summary>[4] Interplay between persistent activity and activity-silent dynamics in prefrontal cortex underlies serial biases in working memory — Joao Barbosa, H. Stein, Rebecca L. Martinez, Adrià Galan-Gadea et al. (2020); cutoff-filter date 2020-06-22; doi:10.1038/s41593-020-0644-4</summary>

```text
[4] Interplay between persistent activity and activity-silent dynamics in prefrontal cortex underlies serial biases in working memory
    id: s2:d3038b219bf2a6c480211fada1dae89058000d62
    date: 2020-04-03
    venue: Nature Neuroscience
    authors: Joao Barbosa, H. Stein, Rebecca L. Martinez, Adrià Galan-Gadea, Sihai Li, J. Dalmau, Kirsten C. S. Adam, J. Valls-Solé
    abstract: Persistent neuronal spiking has long been considered the mechanism underlying working memory, but recent proposals argue for alternative ‘activity-silent’ substrates. Using monkey and human electrophysiology data, we show here that attractor dynamics that control neural spiking during mnemonic periods interact with activity-silent mechanisms in the prefrontal cortex (PFC). This interaction allows memory reactivations, which enhance serial biases in spatial working memory. Stimulus information was not decodable between trials, but remained present in activity-silent traces inferred from spiking synchrony in the PFC. Just before the new stimulus, this latent trace was reignited into activity that recapitulated the previous stimulus representation. Importantly, the reactivation strength correlated with the strength of serial biases in both monkeys and humans, as predicted by a computational model that integrates activity-based and activity-silent mechanisms. Finally, single-pulse transcranial magnetic stimulation applied to the human PFC between successive trials enhanced serial biases, thus demonstrating the causal role of prefrontal reactivations in determining working-memory behavior. Barbosa, Stein et al. show that rather than operating independently, PFC persistent activity and ‘activity-silent’ mechanisms interact dynamically to produce serial effects in working memory, consistent with attractor models with synaptic plasticity.
    note: possibly the same work as s2:e7000ee1f8eabf8922b0ccf1e6b56ba7d97ad9a5
```
</details>

<details><summary>[5] A ventral stream-prefrontal cortex processing cascade enables working memory gating dynamics — Shi-Jing Yu, Sarah Rempel, Negin Gholamipourbarogh, C. Beste (2022); cutoff-filter date 2022-10-12; doi:10.1038/s42003-022-04048-7</summary>

```text
[5] A ventral stream-prefrontal cortex processing cascade enables working memory gating dynamics
    id: s2:5d8c81ec02237567a8f140241f755aa97f3170ec
    date: 2022-10-12
    venue: Communications Biology
    authors: Shi-Jing Yu, Sarah Rempel, Negin Gholamipourbarogh, C. Beste
    abstract: The representation of incoming information, goals and the flexible processing of these are required for cognitive control. Efficient mechanisms are needed to decide when it is important that novel information enters working memory (WM) and when these WM ‘gates’ have to be closed. Compared to neural foundations of maintaining information in WM, considerably less is known about what neural mechanisms underlie the representational dynamics during WM gating. Using different EEG analysis methods, we trace the path of mental representations along the human cortex during WM gate opening and closing. We show temporally nested representational dynamics during WM gate opening and closing depending on multiple independent neural activity profiles. These activity profiles are attributable to a ventral stream-prefrontal cortex processing cascade. The representational dynamics start in the ventral stream during WM gate opening and WM gate closing before prefrontal cortical regions are modulated. A regional specific activity profile is shown within the prefrontal cortex depending on whether WM gates are opened or closed, matching overarching concepts of prefrontal cortex functions. The study closes an essential conceptual gap detailing the neural dynamics underlying how mental representations drive the WM gate to open or close to enable WM functions such as updating and maintenance. Analysis of representational dynamics during working memory gating suggests that distinct opening and closing gating activity profiles are attributable to a ventral stream-prefrontal cortex processing cascade.
```
</details>

<details><summary>[6] Decision Making in Mice During an Optimized Touchscreen Spatial Working Memory Task Sensitive to Medial Prefrontal Cortex Inactivation and NMDA Receptor Hypofunction — Tyler D Dexter, Daniel Palmer, A. Hashad, L. Saksida et al. (2022); cutoff-filter date 2022-05-17; doi:10.3389/fnins.2022.905736</summary>

```text
[6] Decision Making in Mice During an Optimized Touchscreen Spatial Working Memory Task Sensitive to Medial Prefrontal Cortex Inactivation and NMDA Receptor Hypofunction
    id: s2:4db213cc2b43cd750c47c2c83e1a81c76e274543
    date: 2022-05-17
    venue: Frontiers in Neuroscience
    authors: Tyler D Dexter, Daniel Palmer, A. Hashad, L. Saksida, T. Bussey
    abstract: Working memory is a fundamental cognitive process for decision-making and is a hallmark impairment in a variety of neuropsychiatric and neurodegenerative diseases. Spatial working memory paradigms are a valuable tool to assess these processes in rodents and dissect the neurobiology underlying working memory. The trial unique non-match to location (TUNL) task is an automated touchscreen paradigm used to study spatial working memory and pattern separation processes in rodents. Here, animals must remember the spatial location of a stimulus presented on the screen over a delay period; and use this representation to respond to the novel location when the two are presented together. Because stimuli can be presented in a variety of spatial configurations, TUNL offers a trial-unique paradigm, which can aid in combating the development of unwanted mediating strategies. Here, we have optimized the TUNL protocol for mice to reduce training time and further reduce the potential development of mediating strategies. As a result, mice are able to accurately perform an enhanced trial-unique paradigm, where the locations of the sample and choice stimuli can be presented in any configuration on the screen during a single session. We also aimed to pharmacologically characterize this updated protocol, by assessing the roles of the medial prefrontal cortex (mPFC) and N-methyl-D-aspartate (NMDA) receptor (NMDAr) functioning during TUNL. Temporary inactivation of the medial prefrontal cortex (mPFC) was accomplished by directly infusing a mixture of GABA agonists muscimol and baclofen into the mPFC. We found that mPFC inactivation significantly impaired TUNL performance in a delay-dependent manner. In addition, mPFC inactivation significantly increased the susceptibility of mice to proactive interference. Mice were then challenged with acute systemic injections of the NMDAr antagonist ketamine, which resulted in a dose-dependent, delay-dependent working memory impairment. Together, we desc [...]
```
</details>

<details><summary>[7] **KEY** Neural sequences in primate prefrontal cortex encode working memory in naturalistic environments — M. Roussy, Alexandra N. Busch, R. Luna, Matthew L. Leavitt et al. (2022); cutoff-filter date 2022-08-18; doi:10.1101/2022.08.18.504406</summary>

```text
[7] Neural sequences in primate prefrontal cortex encode working memory in naturalistic environments
    id: s2:1701014a2d3b0475328d8d6773c29a4cc1cdcdc5
    date: 2022-08-18
    venue: bioRxiv (preprint)
    authors: M. Roussy, Alexandra N. Busch, R. Luna, Matthew L. Leavitt, M. Mofrad, Roberto A. Gulli, B. Corrigan, J. Mináč
    abstract: Working memory is the ability to briefly remember and manipulate information after it becomes unavailable to the senses. The mechanisms supporting working memory coding in the primate brain remain controversial. Here we demonstrate that microcircuits in layers 2/3 of the primate lateral prefrontal cortex dynamically represent memory content in a naturalistic task through sequential activation of single neurons. We simultaneously recorded the activity of hundreds of neurons in the lateral prefrontal cortex of macaque monkeys during a naturalistic visuospatial working memory task set in a virtual environment. We found that the sequential activation of single neurons encoded trajectories to target locations held in working memory. Neural sequences were not a mere successive activation of cells with memory fields at specific spatial locations, but an abstract representation of the subject’s trajectory to the target. Neural sequences were less correlated to target trajectories during perception and were not found during working memory tasks lacking the spatiotemporal structure of the naturalistic task. Finally, ketamine administration distorted neural sequences, selectively decreasing working memory performance. Our results indicate that neurons in the lateral prefrontal cortex causally encode working memory in naturalistic conditions via complex and temporally precise activation patterns.
```
</details>

<details><summary>[8] **KEY** Neuronal representation of working memory in the medial prefrontal cortex of rats — Sheng-Tao Yang, Yi Shi, Qi Wang, Jiyun Peng et al. (2014); cutoff-filter date 2014-08-28; doi:10.1186/s13041-014-0061-2</summary>

```text
[8] Neuronal representation of working memory in the medial prefrontal cortex of rats
    id: s2:0879bfe55c6d3e5f185431699966213d09a4a9b1
    date: 2014-08-28
    venue: Molecular Brain
    authors: Sheng-Tao Yang, Yi Shi, Qi Wang, Jiyun Peng, Bao-Ming Li
    abstract: Working memory is a process for short-term active maintenance of information. Behavioral neurophysiological studies in monkeys have demonstrated that the dorsolateral prefrontal cortex (dlPFC) is a key cortical region for working memory. The medial prefrontal cortex (mPFC) in rats is a cortical area similar to the dlPFC in monkeys in terms of anatomical connections, and is also required for behavioral performance on working-memory tasks. However, it is still controversial regarding whether and how mPFC neurons encode working memory. In the present study, we trained rats on a two-choice spatial delayed alternation task in Y maze, a typical working memory task for rodents, and investigated neuronal activities in the mPFC when rats performed the task. Our results show that, (1) inactivation of the mPFC severely impaired the performance of rats on the task, consistent with previous studies showing the importance of the mPFC for working-memory tasks; (2) 93.7% mPFC cells (449 in 479) exhibited changes in spiking frequency that were temporally locked with the task events, some of which, including delay-related cells, were tuned by spatial information; (3) differential delay activities in individual mPFC cells appeared transiently and sequentially along the delay, especially during the early phase of the delay; (4) some mPFC cells showed no change in discharge frequency but exhibited differential synchronization in firing during the delay. The present results suggest that mPFC neurons in rats are involved in encoding working memory, via increasing firing frequency or synchronization.
    note: merged with 1 other version(s) of the same work
```
</details>

<details><summary>[9] **KEY** Working memory representation of empty sets in the primate parietal and prefrontal cortices. — Araceli Ramirez-Cardenas, Andreas Nieder (2019); cutoff-filter date 2019-05-01; doi:10.1016/j.cortex.2019.02.028</summary>

```text
[9] Working memory representation of empty sets in the primate parietal and prefrontal cortices.
    id: s2:41340092edd6af4f43668284ddf61fe5e18bb1f3
    date: 2019-05-01
    venue: Cortex; a journal devoted to the study of the nervous system and behavior
    authors: Araceli Ramirez-Cardenas, Andreas Nieder
    abstract: For the brain, representing empty sets as a precursor to zero is a challenge because it requires the active coding of a quantitative category that, by definition, contains no items. Recent neurophysiological recordings show that empty sets are distinctively encoded by neurons in the primate ventral intraparietal area (VIP) and the prefrontal cortex (PFC). However, how empty sets are represented in working memory is unknown. We simultaneously recorded from VIP and PFC while rhesus monkeys performed a delayed numerosity matching task that required the maintenance of numerosities in memory for a brief period. Countable numerosities (1-4) and empty sets ('numerosity 0') were included as stimuli. Single neurons in PFC, and to a lesser extent neurons in VIP, actively encoded empty sets during the delay period. In both cortical areas, empty sets were progressively differentiated from countable numerosities with time during the ongoing trial. Moreover, the tuning of neuron populations in VIP and PFC shifted dynamically towards empty sets so that they became increasingly overrepresented in working memory. Compared to VIP, the prefrontal representation of empty sets was more stable in time and more independent of low level visual features. Moreover, PFC activity correlated better with behavioral performance in empty set trials. These findings suggest that the representation of null quantity in working memory relies more on prefrontal and less on parietal processing. Overall, our results show that empty sets are dynamically and distinctly represented in working memory.
```
</details>

<details><summary>[10] **KEY** Stimulating the Left Dorsolateral Prefrontal Cortex Improves the Memory Representation of Threats among Individuals with High Avoidant Attachment. — Mi Zhou, Xu Chen, Wanting Chen, Xujia Bai (2019); cutoff-filter date 2019-11-01; doi:10.1016/j.bbr.2019.112073</summary>

```text
[10] Stimulating the Left Dorsolateral Prefrontal Cortex Improves the Memory Representation of Threats among Individuals with High Avoidant Attachment.
    id: s2:8384a74f73349b764266c422767af534ef3da9ba
    date: 2019-11-01
    venue: Behavioural Brain Research
    authors: Mi Zhou, Xu Chen, Wanting Chen, Xujia Bai
    abstract: Prior research has suggested that individuals with high avoidant attachment may demonstrate a vigilant attentional bias and selective attentional avoidance towards attachment-related negative information (threat information). Similarly, some evidence suggests that impairment of hot working memory (WM) or emotional-related WM occurs in highly avoidant individuals. Moreover, functional MRI studies have demonstrated that the less-activated left dorsolateral prefrontal cortex (L-DLPFC) is related to the impairment of cognitive control for threat stimuli in individuals with high avoidant attachment. Therefore, in the present study, the causal role of the L-DLPFC on hot WM presentation was investigated by the high-definition transcranial direct current stimulation (HD-tDCS) technique, and cognitive control for internal mental representations in WM was measured by the Internal Shift Task (IST). The results showed that the highly avoidant participants performed faster on the emotional IST than low avoidant participants in the sham condition. In the emotional IST, highly avoidant participants were slower after receiving anodal HD-tDCS than in the sham condition. Moreover, the switching cost of the emotional IST was significantly smaller in the highly avoidant group than low avoidant group under the sham HD-tDCS condition. Interestingly, in the emotional IST, the switching cost of highly avoidant individuals was significantly greater in the anodal stimulation group than the sham stimulation group. Conversely, the switching cost of low avoidant individuals was significantly smaller with anodal stimulation than for sham stimulation. The findings indicate that anodal HD-tDCS over the L-DLPFC can effectively enhance the ability of memory representation towards threat information in highly avoidant individuals. This study extends causal research by showing that the L-DLPFC is an important brain region for hot WM representations.
```
</details>

<details><summary>Post-hoc automated audit — NON-AUTHORITATIVE; uses hidden benchmark annotations</summary>

- primary auditor: `silence_as_null_error`; statuses {'H1': 'positive_or_present', 'H2': 'indeterminate'}; discriminative=False
- primary reasoning: H1 directly predicts that prefrontal regions can store mnemonic representations, as it posits PFC persistent activity as a storage substrate. H2 is silent on whether PFC can store information, as it only claims PFC controls or prioritizes representations stored elsewhere, without specifying PFC's own storage capacity.
- derived opposition call: `manufactured_from_silence`
- evidence attribution: `informative_evidence_found` — The retrieved literature includes multiple studies that directly address the proposition, showing that regions of the prefrontal cortex can store and represent information about items maintained in working memory. The assessor correctly identified and synthesized this evidence, which includes neurophysiological, behavioral, and stimulation studies across species. The process worked as intended.
- auditor retest: `silence_as_null_error`; discriminative=False
- disagreement flags: {'second_rater_vs_primary_discriminative': None, 'second_rater_vs_primary_status': None, 'retest_vs_primary_category': False, 'any': False}
</details>

**Human review** — `evidence_construct_mismatch` · reviewer: Research Director · source: D045 · status: `first_pass_model_based_review` · genuinely discriminative: False · silence-as-null error: False · other fields not recorded

---

## #20 · `GP1-pfc_storage_vs_control-X24`

**GP1-pfc_storage_vs_control-X24** — case `pfc_storage_vs_control`, node `X24`

> Lateral prefrontal cortex is more likely to encode signals related to task demands or control processes than to the specific sensory features of memorized visual stimuli.

- generated from **H2** (Candidate B); abstraction: `class`
- generator's stated reason: The claim asserts that prefrontal regions generally reflect control or prioritization, so this should apply to the broader class of lateral prefrontal cortex functions.
- influence: **0.276** (rank 4 in case, 20 overall; cumulative 56%) — favours **H2**
- log-likelihood contribution: H1 +1.715, H2 +1.991
- removing it alone: evidence withheld → case log-odds +1.490 (ranking unchanged); node deleted → +1.490 (ranking unchanged)

**Hypotheses (as shown to the verifier)**

- **H1** (Candidate A): Prefrontal persistent activity is itself a substrate for working-memory storage; disrupting the relevant PFC population therefore disrupts the stored mnemonic representation.
- **H2** (Candidate B): PFC primarily controls, prioritizes, or allocates resources to working-memory representations maintained in sensory/posterior regions rather than directly storing the mnemonic content itself.

**Verifier cross-hypothesis judgments** — P(X|H) combines these by noisy-OR

| hypothesis | origin? | direct edge | route via parent | P(X\|H) |
| --- | --- | --- | --- | --- |
| H1 | no | `unlikely` | X6 [H→parent `unlikely`, P=0.30] → `implied` | 0.713 |
| H2 | yes | `strongly_implied` | X6 [H→parent `strongly_implied`, P=0.95] → `implied` | 0.989 |

- edge rationale, **H1** → node: If prefrontal persistent activity directly stores mnemonic representations, it is more likely to encode the specific sensory features of memorized stimuli rather than primarily signals related to task demands or control processes.
- edge rationale, **H2** → node: If PFC's main role is to control or allocate resources to working-memory representations stored elsewhere, it is nearly certain that PFC encodes signals related to task demands or control processes rather than the sensory features themselves.
- parent `X6`: Regions of prefrontal cortex are more likely to show signals related to attentional control or prioritization than to the specific content of visual working memory representations.
- chain rationale, `X6` → node: The parent proposition suggests that prefrontal cortex regions, which include lateral prefrontal cortex, are more involved in control processes than in encoding specific sensory content, supporting the child proposition but not specifying lateral prefrontal cortex exclusively.

**Verifier evidence** — label used in score: `strong_support` (log-LR +2.0)

- queries: `lateral prefrontal cortex task demands`; `lateral prefrontal cortex sensory features`
- assessor rationale: Multiple records directly state that the lateral prefrontal cortex is involved in encoding signals related to task demands, control processes, and goal representations, rather than specific sensory features of memorized visual stimuli. The evidence includes causal studies, fMRI, and theoretical models, all consistently describing the LPFC's role in cognitive control, task-order coordination, and context-dependent prioritization. No records directly contradict this proposition, and the studies are methodologically strong and independent.
- supporting spans cited by the assessor:
  - "Results of this study indicate that the lPFC, but not the preSMA, is causally involved in implementing task-order coordination processes in dual-task situations."
  - "These results suggest that the fundamental control architecture of the LPFC is relatively fixed, and that different demands are accommodated through modulations of this fixed architecture."
  - "Overall, we demonstrate how cognitive control mechanisms may inhibit novel idea generation."
  - "Together, our findings indicate that in effort‐based decisions DLPFC represents the capacity to exert mental effort and the updating of this information with enduring time‐on‐task, informing theoretical accounts on the role of DLPFC in the motivation to exert mental effort and the fatigue arising from it."
  - "We measured High-Frequency Activity [50-150 Hz] as a proxy of population-level spiking activity and we identified a crucial component of a Gate-Keeping Mechanism bilateral in the mid-Ventro-Lateral Prefrontal Cortex (VLPFC), at the interplay of the Ventral and Dorsal Attention Networks, that selectively reacts before domain specialized cortical regions that engage in full stimulus analysis according to task demands."
  - "Dorsolateral prefrontal cortex (DLPFC) maintains goal representations in a context-dependent manner. Here, we show this region is involved in prioritising off-task thought in an analogous way."
  - "Cognitive control refers to the intentional selection of thoughts, emotions, and behaviors based on current task demands and social context, and the concomitant suppression of inappropriate habitual actions (Miller and Cohen, 2001)."
  - "An influential model suggests that the lateral prefrontal cortex (LPFC) represents rules or instructions in working memory and that this information adaptively guides perceptual and motor processing in posterior brain regions, thus resulting in the selection of appropriate behaviors, and the suppression of maladaptive habitual actions (Miller and Cohen, 2001; Bunge, 2004)."
- 10 papers shown; key papers: `s2:4fab206eee09b4729f4920142b8e3c75d1e4d59d`, `s2:55fb5dd8f620c0bd876bf610bb04342bdbd65da7`, `s2:58a935709080fa92d1a9bbab12b2e2fe543bbc5d`, `s2:9fa82bafe8efc6b3bab14f5fd99a4336953de001`, `s2:a928c0c9e1144350038e7144778efca73dcc3e84`, `s2:cb75f4db6a12a419ce2959b924bf73ea239f5765`, `s2:dbd377f2ee64101b4ed25cd78a2c17d1cfc523b1`
- _The evidence assessor returns ONE label for the node from all papers shown; the method has no per-paper contribution. Key papers and spans are those the assessor cited._

<details><summary>[1] **KEY** The Causal Role of the Lateral Prefrontal Cortex for Task-order Coordination in Dual-task Situations: A Study with Transcranial Magnetic Stimulation — Sebastian Kübler, Alexander Soutschek, T. Schubert (2019); cutoff-filter date 2019-09-03; doi:10.1162/jocn_a_01466</summary>

```text
[1] The Causal Role of the Lateral Prefrontal Cortex for Task-order Coordination in Dual-task Situations: A Study with Transcranial Magnetic Stimulation
    id: s2:dbd377f2ee64101b4ed25cd78a2c17d1cfc523b1
    date: 2019-09-03
    venue: Journal of Cognitive Neuroscience
    authors: Sebastian Kübler, Alexander Soutschek, T. Schubert
    abstract: Dual tasks are characterized by the requirement for additional task-order coordination processes that schedule the processing order of two temporally overlapping tasks. Preliminary evidence from functional imaging studies suggests that lateral pFC (lPFC) activation correlates with implementing these task-order coordination processes. However, so far, it is unclear whether the lPFC is also causally involved in coordinating task order during dual-task performance and which exact mechanisms are implemented by this brain region. In this study, we addressed these open issues by applying online TMS during a dual-task situation. For this purpose, participants performed a dual task in fixed-order blocks with a constant order of tasks and in random-order block, in which the order of tasks varied randomly and thus demands on task-order coordination were increased. In Experiment 1, TMS of the lPFC compared with control TMS conditions impaired dual-task performance in random-order blocks, whereas performance in fixed-order blocks was unaffected by TMS. In Experiment 2, we tested for the specificity of the lPFC TMS effect on task-order coordination by applying TMS over the preSMA. We showed that preSMA TMS did not affect dual-task performance, neither in fixed-order nor in random-order blocks. Results of this study indicate that the lPFC, but not the preSMA, is causally involved in implementing task-order coordination processes in dual-task situations.
```
</details>

<details><summary>[2] **KEY** Generalizing the Control Architecture of the Lateral Prefrontal Cortex — McKinney Pitts, Derek Evan Nee (2022); cutoff-filter date 2022-10-18; doi:10.1016/j.nlm.2022.107688</summary>

```text
[2] Generalizing the Control Architecture of the Lateral Prefrontal Cortex
    id: s2:55fb5dd8f620c0bd876bf610bb04342bdbd65da7
    date: 2022-10-01
    venue: Neurobiology of Learning and Memory
    authors: McKinney Pitts, Derek Evan Nee
    abstract: Cognitive control guides non-habitual, goal directed behaviors allowing us to flexibly adapt to ongoing demands. Previous work has suggested that multiple cognitive control processes exist that can be classed according to their action on present-oriented/external information versus future-oriented/internal information. These processes can be mapped onto the lateral prefrontal cortex (LPFC) such that increasingly rostral areas are involved in increasingly future-oriented/internal control processes. Whether and how such processes are organized to support goal-directed behavior remains unclear. On the one hand, the LPFC may flexibly adapt based upon demands. On the other hand, there may be a consistent control architecture such as a control hierarchy that generalizes across demands. Previous work using fMRI in humans during a comprehensive control task that engaged several control processes at once found that an area in mid-LPFC consistently exerted widespread influence throughout the LPFC. These data suggested that the mid-LPFC forms an apex of a putative control hierarchy. However, whether such an architecture generalizes across tasks remains to be tested. Here, we utilized a modified comprehensive control task designed to alter how control processes influence one another to test the generalizability of the LPFC control architecture. Univariate fMRI activations revealed distinct control-related activations relative to past work. Despite these changes, effective connectivity modeling revealed a directed architecture similar to previous findings with the mid-LPFC exerting the most widespread influences throughout LPFC. These results suggest that the fundamental control architecture of the LPFC is relatively fixed, and that different demands are accommodated through modulations of this fixed architecture.
```
</details>

<details><summary>[3] **KEY** Noninvasive brain stimulation to lateral prefrontal cortex alters the novelty of creative idea generation — Yoed N. Kenett, David S. Rosen, Emilio R. Tamez, S. Thompson-Schill (2021); cutoff-filter date 2021-02-23; doi:10.3758/s13415-021-00869-x</summary>

```text
[3] Noninvasive brain stimulation to lateral prefrontal cortex alters the novelty of creative idea generation
    id: s2:9fa82bafe8efc6b3bab14f5fd99a4336953de001
    date: 2021-02-23
    venue: Cognitive, Affective, & Behavioral Neuroscience
    authors: Yoed N. Kenett, David S. Rosen, Emilio R. Tamez, S. Thompson-Schill
    abstract: Theories of the processes involved in creative cognition posit that cognitive control has a negative effect on creative idea generation but a positive effect on creative idea evaluation. Brain stimulation research has started to examine empirically the effects of cognitive control, with several reports of decreased cognitive control facilitating creative ideation. Such studies have shown how decreased cognitive control mechanisms facilitate creative idea generation, potentially by allowing participants access to less inhibited weaker-related associations, thereby increasing novelty. In the current study, we advance this line of work by investigating how cognitive control affects creative thinking, potentially inhibiting or facilitating novel idea generation based on task demands. Participants read sentences with the final word missing and were instructed to complete the sentence with an uncommon (but appropriate) ending. Participants performed this task while undergoing either anodal (excitatory), cathodal (inhibitory), or sham (control) transcranial direct current stimulation over their left prefrontal cortex. These responses were then rated for their novelty and appropriateness by an independent sample of raters. We found that anodal stimulation increased the appropriateness and decreased the novelty of participants’ responses. Contrary to previous studies, we did not find that cathodal stimulation increased the novelty of participants’ responses, which may be due to the nature of our task. Overall, we demonstrate how cognitive control mechanisms may inhibit novel idea generation.
```
</details>

<details><summary>[4] **KEY** Causal role of lateral prefrontal cortex in mental effort and fatigue — Alexander Soutschek, P. Tobler (2020); cutoff-filter date 2020-07-25; doi:10.1002/hbm.25146</summary>

```text
[4] Causal role of lateral prefrontal cortex in mental effort and fatigue
    id: s2:4fab206eee09b4729f4920142b8e3c75d1e4d59d
    date: 2020-07-25
    venue: Human Brain Mapping
    authors: Alexander Soutschek, P. Tobler
    abstract: Dorsolateral prefrontal cortex (DLPFC) is well‐known for its role in exerting mental work, however the contribution of DLPFC for deciding whether or not to engage in effort remains unknown. Here, we assessed the causal role of DLPFC in effort‐based decision making. We disrupted functioning of DLPFC with noninvasive brain stimulation before participants repeatedly decided whether to exert mental effort in a working memory task. We found the same DLPFC subregion involved in mental effort exertion to influence also effort‐based decisions: First, it enhanced effort discounting, suggesting that DLPFC may signal the capacity to successfully deal with effort demands. Second, a novel computational model integrating the costs of enduring effort into the effort‐based decision process revealed that DLPFC disruption reduced fatigue after accumulated effort exertion, linking DLPFC activation with fatigue. Together, our findings indicate that in effort‐based decisions DLPFC represents the capacity to exert mental effort and the updating of this information with enduring time‐on‐task, informing theoretical accounts on the role of DLPFC in the motivation to exert mental effort and the fatigue arising from it.
```
</details>

<details><summary>[5] **KEY** A real-time marker of object-based attention in the human brain. A possible component of a "gate-keeping mechanism" performing late attentional selection in the Ventro-Lateral Prefrontal Cortex — M. Perrone‐Bertolotti, S. El Bouzaïdi Tiali, Juan R. Vidal, Mathilde Petton et al. (2020); cutoff-filter date 2020-01-22; doi:10.1016/j.neuroimage.2020.116574</summary>

```text
[5] A real-time marker of object-based attention in the human brain. A possible component of a "gate-keeping mechanism" performing late attentional selection in the Ventro-Lateral Prefrontal Cortex
    id: s2:58a935709080fa92d1a9bbab12b2e2fe543bbc5d
    date: 2020-01-22
    venue: NeuroImage
    authors: M. Perrone‐Bertolotti, S. El Bouzaïdi Tiali, Juan R. Vidal, Mathilde Petton, A. Croize, P. Deman, S. Rheims, L. Minotti
    abstract: The decision to process an incoming stimulus attentively - and to trigger a follow-up cascade of high-level processes - is strategic for the human brain as it becomes transiently unavailable to subsequent stimulus processing. In this study, we set to identify brain networks that carry out such evaluations. We therefore assessed the time-course of neural responses with intracerebral EEG in human patients during an attentional reading task, contrasting to-be-attended vs. to-be-ignored items. We measured High-Frequency Activity [50-150 Hz] as a proxy of population-level spiking activity and we identified a crucial component of a Gate-Keeping Mechanism bilateral in the mid-Ventro-Lateral Prefrontal Cortex (VLPFC), at the interplay of the Ventral and Dorsal Attention Networks, that selectively reacts before domain specialized cortical regions that engage in full stimulus analysis according to task demands.
```
</details>

<details><summary>[6] **KEY** Left dorsolateral prefrontal cortex supports context-dependent prioritisation of off-task thought — Adam Turnbull, Hao-Ting Wang, Charlotte Murphy, N. Ho et al. (2019); cutoff-filter date 2019-08-23; doi:10.1038/s41467-019-11764-y</summary>

```text
[6] Left dorsolateral prefrontal cortex supports context-dependent prioritisation of off-task thought
    id: s2:a928c0c9e1144350038e7144778efca73dcc3e84
    date: 2019-08-23
    venue: Nature Communications
    authors: Adam Turnbull, Hao-Ting Wang, Charlotte Murphy, N. Ho, Xiuyi Wang, Mladen Sormaz, Theodoros Karapanagiotidis, R. Leech
    abstract: When environments lack compelling goals, humans often let their minds wander to thoughts with greater personal relevance; however, we currently do not understand how this context-dependent prioritisation process operates. Dorsolateral prefrontal cortex (DLPFC) maintains goal representations in a context-dependent manner. Here, we show this region is involved in prioritising off-task thought in an analogous way. In a whole brain analysis we established that neural activity in DLPFC is high both when ‘on-task’ under demanding conditions and ‘off-task’ in a non-demanding task. Furthermore, individuals who increase off-task thought when external demands decrease, show lower correlation between neural signals linked to external tasks and lateral regions of the DMN within DLPFC, as well as less cortical grey matter in regions sensitive to these external task relevant signals. We conclude humans prioritise daydreaming when environmental demands decrease by aligning cognition with their personal goals using DLPFC. The authors show that the dorsolateral prefrontal cortex (DLPFC) is involved in both on-task thought during increased environmental demands, and off-task thought during decreased demand–suggesting a role for the DLPFC in prioritising goals in a context-dependent manner.
```
</details>

<details><summary>[7] Task-order coordination in dual-task performance and the lateral prefrontal cortex: an event-related fMRI study — André J. Szameitat, J. Lepsien, D. V. von Cramon, A. Sterr et al. (2006); cutoff-filter date 2006-10-10; doi:10.1007/s00426-005-0015-5</summary>

```text
[7] Task-order coordination in dual-task performance and the lateral prefrontal cortex: an event-related fMRI study
    id: s2:222be43e0a4d4d70b69e9b33682c21676d25b966
    date: 2006-10-10
    venue: Psychological Research
    authors: André J. Szameitat, J. Lepsien, D. V. von Cramon, A. Sterr, T. Schubert
    abstract: [no abstract available]
```
</details>

<details><summary>[8] A Sensitive Indicator of Hemodynamic Changes in The Lateral Prefrontal Cortex Using a Modified Version of "Rock, Paper, Scissors" as a Task Load — Kenji Matsumoto, Senichiro Kikuchi, F. Miwakeichi, Y. Yamauchi et al. (2013); cutoff-filter date 2013-02-01; https://www.semanticscholar.org/paper/6ec2c45515192da6c72621f68d8d7483d6b702ab</summary>

```text
[8] A Sensitive Indicator of Hemodynamic Changes in The Lateral Prefrontal Cortex Using a Modified Version of "Rock, Paper, Scissors" as a Task Load
    id: s2:6ec2c45515192da6c72621f68d8d7483d6b702ab
    date: 2013-02-01
    venue: Journal of Medical and Biological Engineering
    authors: Kenji Matsumoto, Senichiro Kikuchi, F. Miwakeichi, Y. Yamauchi, Makio Ishiguro, Eiju Watanabe, S. Kato
    abstract: [no abstract available]
```
</details>

<details><summary>[9] Bilateral recruitment of prefrontal cortex in working memory is associated with task demand but not with age — Melanie S. Höller-Wallscheid, P. Thier, J. K. Pomper, A. Lindner (2017); cutoff-filter date 2017-01-17; doi:10.1073/pnas.1601983114</summary>

```text
[9] Bilateral recruitment of prefrontal cortex in working memory is associated with task demand but not with age
    id: s2:38ac9b1e6c1f9fe43ad69ec8dca2c6744f7e18ff
    date: 2017-01-17
    venue: Proceedings of the National Academy of Sciences of the United States of America
    authors: Melanie S. Höller-Wallscheid, P. Thier, J. K. Pomper, A. Lindner
    abstract: [no abstract available]
```
</details>

<details><summary>[10] **KEY** Cognitive control, emotional value, and the lateral prefrontal cortex — Matthew L. Dixon (2015); cutoff-filter date 2015-06-02; doi:10.3389/fpsyg.2015.00758</summary>

```text
[10] Cognitive control, emotional value, and the lateral prefrontal cortex
    id: s2:cb75f4db6a12a419ce2959b924bf73ea239f5765
    date: 2015-06-02
    venue: Frontiers in Psychology
    authors: Matthew L. Dixon
    abstract: Cognitive control refers to the intentional selection of thoughts, emotions, and behaviors based on current task demands and social context, and the concomitant suppression of inappropriate habitual actions (Miller and Cohen, 2001). Common situations that require cognitive control include: studying for an exam while resisting the impulse to check Facebook; having fruit instead of dessert when on a diet; and being patient with one's kids instead of yelling at them for spilling juice on the carpet. Historically, there has been preferential interest in how cognitive control operates. An influential model suggests that the lateral prefrontal cortex (LPFC) represents rules or instructions in working memory and that this information adaptively guides perceptual and motor processing in posterior brain regions, thus resulting in the selection of appropriate behaviors, and the suppression of maladaptive habitual actions (Miller and Cohen, 2001; Bunge, 2004). Surprisingly, there has been less focus on why individuals choose to engage cognitive control in the first place (Dixon and Christoff, 2012; Botvinick and Braver, 2015). In this article, I outline a value-based framework of cognitive control which suggests that: (1) individuals choose to engage cognitive control when they expect that it will produce an emotionally valued outcome (i.e., a reward or the avoidance of punishment); (2) the LPFC is a critical neural substrate involved in representing the value of engaging cognitive control; and (3) the LPFC is organized along a rostro-caudal axis, with different sub-regions contributing to different elements of the decision to employ cognitive control.
```
</details>

<details><summary>Post-hoc automated audit — NON-AUTHORITATIVE; uses hidden benchmark annotations</summary>

- primary auditor: `silence_as_null_error`; statuses {'H1': 'indeterminate', 'H2': 'positive_or_present'}; discriminative=False
- primary reasoning: H2 predicts that lateral prefrontal cortex activity should reflect control or prioritization signals rather than sensory mnemonic content, so the proposition is positive under H2. H1, which posits PFC as a storage substrate, does not specifically predict whether lateral PFC encodes control signals or sensory features, so it is indeterminate.
- derived opposition call: `manufactured_from_silence`
- evidence attribution: `informative_evidence_found` — The retrieved papers directly address the proposition, providing strong evidence that the lateral prefrontal cortex encodes signals related to task demands and control processes rather than specific sensory features. The assessor correctly interpreted the literature, which includes causal, fMRI, and theoretical studies, all supporting the proposition. The process worked as intended.
- auditor retest: `novel_plausible_discriminator`; discriminative=True
- disagreement flags: {'second_rater_vs_primary_discriminative': None, 'second_rater_vs_primary_status': None, 'retest_vs_primary_category': True, 'any': True}
</details>

**Human review** — `genuine_discriminator` · reviewer: Research Director · source: D045 · status: `first_pass_model_based_review` · genuinely discriminative: True · silence-as-null error: False · other fields not recorded

---

## #21 · `GP1-eukaryogenesis_mito_timing-X24`

**GP1-eukaryogenesis_mito_timing-X24** — case `eukaryogenesis_mito_timing`, node `X24`

> Complex cellular traits associated with eukaryotes can arise in archaeal lineages prior to endosymbiosis.

- generated from **H2** (Candidate B); abstraction: `class`
- generator's stated reason: If Asgard archaea show eukaryote-like complexity, it increases the likelihood that such traits can evolve in archaeal superphyla before mitochondrial acquisition.
- influence: **0.274** (rank 4 in case, 21 overall; cumulative 57%) — favours **H2**
- log-likelihood contribution: H1 +1.715, H2 +1.989
- removing it alone: evidence withheld → case log-odds -2.148 (ranking unchanged); node deleted → -2.148 (ranking unchanged)

**Hypotheses (as shown to the verifier)**

- **H1** (Candidate A): Mitochondrial acquisition was an initiating/foundational event that preceded or enabled much of later eukaryotic cellular complexity; major eukaryote-specific cellular systems should therefore largely elaborate after mitochondrial acquisition.
- **H2** (Candidate B): Substantial eukaryotic cellular machinery - including cytoskeletal, membrane-remodelling/trafficking, endomembrane, phagocytic, and nuclear-associated complexity - evolved before mitochondrial acquisition in an already complex archaeal host.

**Verifier cross-hypothesis judgments** — P(X|H) combines these by noisy-OR

| hypothesis | origin? | direct edge | route via parent | P(X\|H) |
| --- | --- | --- | --- | --- |
| H1 | no | `unlikely` | X6 [H→parent `unlikely`, P=0.30] → `implied` | 0.713 |
| H2 | yes | `strongly_implied` | X6 [H→parent `implied`, P=0.80] → `implied` | 0.987 |

- edge rationale, **H1** → node: If mitochondrial acquisition was foundational and most eukaryotic complexity arose after it, then complex cellular traits in archaea prior to endosymbiosis would be less likely.
- edge rationale, **H2** → node: If substantial eukaryotic cellular complexity evolved before mitochondrial acquisition in an archaeal host, then complex cellular traits arising in archaea prior to endosymbiosis is nearly certain.
- parent `X6`: Members of the Asgard archaeal superphylum exhibit eukaryote-like cellular complexity, including genes for endomembrane and phagocytic functions.
- chain rationale, `X6` → node: If Asgard archaea possess eukaryote-like complexity, it suggests that such traits can develop in archaeal lineages before endosymbiosis occurs.

**Verifier evidence** — label used in score: `strong_support` (log-LR +2.0)

- queries: `archaea complex cellular traits`; `archaea eukaryotic features endosymbiosis`
- assessor rationale: Record [5] directly reports that several halophilic archaea display complex cellular traits, specifically cellular differentiation into mycelia and spores, which are typically associated with eukaryotes. This demonstrates that such traits can arise in archaeal lineages prior to endosymbiosis, as stated in the proposition. No other records directly address this proposition.
- supporting spans cited by the assessor:
  - "Here, we show that several haloarchaea of the family Halobacteriaceae display a life cycle resembling that of Streptomyces bacteria. Strain YIM 93972 (isolated from a salt marsh) undergoes cellular differentiation into mycelia and spores."
  - "Bacteria of the genus Streptomyces have complex life cycles involving cellular differentiation and multicellular structures that have never been observed in archaea. Here, the authors show that several halophilic archaea display a life cycle resembling that of Streptomyces bacteria, undergoing cellular differentiation into mycelia and spores."
- 10 papers shown; key papers: `s2:dcb912939f8cefc5bf05967565ffd9cdf63d96c4`
- _The evidence assessor returns ONE label for the node from all papers shown; the method has no per-paper contribution. Key papers and spans are those the assessor cited._

<details><summary>[1] The emergence of major cellular processes in evolution — C. Ouzounis, N. Kyrpides (1996); cutoff-filter date 1996-07-22; doi:10.1016/0014-5793(96)00631-x</summary>

```text
[1] The emergence of major cellular processes in evolution
    id: s2:6151324fe98a609a8bc96cf62b7c6820589fe425
    date: 1996-07-22
    venue: FEBS Letters
    authors: C. Ouzounis, N. Kyrpides
    abstract: [no abstract available]
```
</details>

<details><summary>[2] The last universal common ancestor (LUCA), simple or complex? — Patrick Forterre, Hervé Philippe (1999); cutoff-filter date 1999-06-30; doi:10.2307/1542973</summary>

```text
[2] The last universal common ancestor (LUCA), simple or complex?
    id: s2:a660d11227593ac180ce355b4ec8b9dc02ea7280
    date: 1999-06-01
    venue: The Biological Bulletin
    authors: Patrick Forterre, Hervé Philippe
    abstract: [no abstract available]
```
</details>

<details><summary>[3] Helq acts in parallel to Fancc to suppress replication-associated genome instability — Spencer W. Luebben, Tsuyoshi Kawabata, Monica K. Akre, Wai L. Lee et al. (2013); cutoff-filter date 2013-08-21; doi:10.1093/nar/gkt676</summary>

```text
[3] Helq acts in parallel to Fancc to suppress replication-associated genome instability
    id: s2:fd1628c2773b29af1d93ba82d00bb533366c2c1a
    date: 2013-08-21
    venue: Nucleic Acids Research
    authors: Spencer W. Luebben, Tsuyoshi Kawabata, Monica K. Akre, Wai L. Lee, Charles S. Johnson, M. O'Sullivan, N. Shima
    abstract: HELQ is a superfamily 2 DNA helicase found in archaea and metazoans. It has been implicated in processing stalled replication forks and in repairing DNA double-strand breaks and inter-strand crosslinks. Though previous studies have suggested the possibility that HELQ is involved in the Fanconi anemia (FA) pathway, a dominant mechanism for inter-strand crosslink repair in vertebrates, this connection remains elusive. Here, we investigated this question in mice using the Helqgt and Fancc− strains. Compared with Fancc−/− mice lacking FANCC, a component of the FA core complex, Helqgt/gt mice exhibited a mild of form of FA-like phenotypes including hypogonadism and cellular sensitivity to the crosslinker mitomycin C. However, unlike Fancc−/− primary fibroblasts, Helqgt/gt cells had intact FANCD2 mono-ubiquitination and focus formation. Notably, for all traits examined, Helq was non-epistatic with Fancc, as Helqgt/gt;Fancc−/− double mutants displayed significantly worsened phenotypes than either single mutant. Importantly, this was most noticeable for the suppression of spontaneous chromosome instability such as micronuclei and 53BP1 nuclear bodies, known consequences of persistently stalled replication forks. These findings suggest that mammalian HELQ contributes to genome stability in unchallenged conditions through a mechanism distinct from the function of FANCC.
```
</details>

<details><summary>[4] Genetic and molecular architecture of complex traits — T. Lappalainen, Yang I Li, Sohini Ramachandran, Alexander Gusev (2024); cutoff-filter date 2024-02-29; doi:10.1016/j.cell.2024.01.023</summary>

```text
[4] Genetic and molecular architecture of complex traits
    id: s2:415a4d8b8610b0e035f4ca6e4a9bc2a76cc89cfe
    date: 2024-02-01
    venue: Cell
    authors: T. Lappalainen, Yang I Li, Sohini Ramachandran, Alexander Gusev
    abstract: Human genetics has emerged as one of the most dynamic areas of biology, with a broadening societal impact. In this review, we discuss recent achievements, ongoing efforts and future challenges in the field. Advances in technology, statistical methods and the growing scale of research efforts have all provided many insights into the processes that have given rise to the current patterns of genetic variation. Vast maps of genetic associations with human traits and diseases have allowed characterization of their genetic architecture. Finally, studies of molecular and cellular effects of genetic variants have provided insights into biological processes underlying disease. Many outstanding questions remain, but the field is well poised for groundbreaking discoveries as it increases the use of genetic data to understand both the history of our species and its applications to improve human health.
```
</details>

<details><summary>[5] **KEY** Cellular differentiation into hyphae and spores in halophilic archaea — Shu-Kun Tang, Xiao-Yang Zhi, Yao Zhang, K. Makarova et al. (2023); cutoff-filter date 2023-04-01; doi:10.1038/s41467-023-37389-w</summary>

```text
[5] Cellular differentiation into hyphae and spores in halophilic archaea
    id: s2:dcb912939f8cefc5bf05967565ffd9cdf63d96c4
    date: 2023-04-01
    venue: Nature Communications
    authors: Shu-Kun Tang, Xiao-Yang Zhi, Yao Zhang, K. Makarova, Bing-Bing Liu, Guo-Song Zheng, Zhen-Peng Zhang, Hua-Jun Zheng
    abstract: Several groups of bacteria have complex life cycles involving cellular differentiation and multicellular structures. For example, actinobacteria of the genus Streptomyces form multicellular vegetative hyphae, aerial hyphae, and spores. However, similar life cycles have not yet been described for archaea. Here, we show that several haloarchaea of the family Halobacteriaceae display a life cycle resembling that of Streptomyces bacteria. Strain YIM 93972 (isolated from a salt marsh) undergoes cellular differentiation into mycelia and spores. Other closely related strains are also able to form mycelia, and comparative genomic analyses point to gene signatures (apparent gain or loss of certain genes) that are shared by members of this clade within the Halobacteriaceae . Genomic, transcriptomic and proteomic analyses of non-differentiating mutants suggest that a Cdc48-family ATPase might be involved in cellular differentiation in strain YIM 93972. Additionally, a gene encoding a putative oligopeptide transporter from YIM 93972 can restore the ability to form hyphae in a Streptomyces coelicolor mutant that carries a deletion in a homologous gene cluster ( bldKA-bldKE ), suggesting functional equivalence. We propose strain YIM 93972 as representative of a new species in a new genus within the family Halobacteriaceae , for which the name Actinoarchaeum halophilum gen. nov., sp. nov. is herewith proposed. Our demonstration of a complex life cycle in a group of haloarchaea adds a new dimension to our understanding of the biological diversity and environmental adaptation of archaea. Bacteria of the genus Streptomyces have complex life cycles involving cellular differentiation and multicellular structures that have never been observed in archaea. Here, the authors show that several halophilic archaea display a life cycle resembling that of Streptomyces bacteria, undergoing cellular differentiation into mycelia and spores.
```
</details>

<details><summary>[6] PigBiobank: a valuable resource for understanding genetic and biological mechanisms of diverse complex traits in pigs — Haonan Zeng, Wenjing Zhang, Qing Lin, Yahui Gao et al. (2023); cutoff-filter date 2023-11-13; doi:10.1093/nar/gkad1080</summary>

```text
[6] PigBiobank: a valuable resource for understanding genetic and biological mechanisms of diverse complex traits in pigs
    id: s2:782174efef99c4fbf4c6d53e95bab0ef15cc6d85
    date: 2023-11-13
    venue: Nucleic Acids Research
    authors: Haonan Zeng, Wenjing Zhang, Qing Lin, Yahui Gao, J. Teng, Zhiting Xu, Xiaodian Cai, Zhanming Zhong
    abstract: Abstract To fully unlock the potential of pigs as both agricultural species for animal-based protein food and biomedical models for human biology and disease, a comprehensive understanding of molecular and cellular mechanisms underlying various complex phenotypes in pigs and how the findings can be translated to other species, especially humans, are urgently needed. Here, within the Farm animal Genotype-Tissue Expression (FarmGTEx) project, we build the PigBiobank (http://pigbiobank.farmgtex.org) to systematically investigate the relationships among genomic variants, regulatory elements, genes, molecular networks, tissues and complex traits in pigs. This first version of the PigBiobank curates 71 885 pigs with both genotypes and phenotypes from over 100 pig breeds worldwide, covering 264 distinct complex traits. The PigBiobank has the following functions: (i) imputed sequence-based genotype-phenotype associations via a standardized and uniform pipeline, (ii) molecular and cellular mechanisms underlying trait-associations via integrating multi-omics data, (iii) cross-species gene mapping of complex traits via transcriptome-wide association studies, and (iv) high-quality results display and visualization. The PigBiobank will be updated timely with the development of the FarmGTEx-PigGTEx project, serving as an open-access and easy-to-use resource for genetically and biologically dissecting complex traits in pigs and translating the findings to other species.
```
</details>

<details><summary>[7] Genetic effects on molecular network states explain complex traits — Matthias Weith, J. Grossbach, M. Clément-Ziza, Ludovic C. Gillet et al. (2023); cutoff-filter date 2023-07-24; doi:10.15252/msb.202211493</summary>

```text
[7] Genetic effects on molecular network states explain complex traits
    id: s2:f6c8e9789d8201914dd27b0c925968cd0a1a440c
    date: 2023-07-24
    venue: Molecular Systems Biology
    authors: Matthias Weith, J. Grossbach, M. Clément-Ziza, Ludovic C. Gillet, María Rodríguez-López, S. Marguerat, C. Workman, P. Picotti
    abstract: The complexity of many cellular and organismal traits results from the integration of genetic and environmental factors via molecular networks. Network structure and effect propagation are best understood at the level of functional modules, but so far, no concept has been established to include the global network state. Here, we show when and how genetic perturbations lead to molecular changes that are confined to small parts of a network versus when they lead to modulation of network states. Integrating multi‐omics profiling of genetically heterogeneous budding and fission yeast strains with an array of cellular traits identified a central state transition of the yeast molecular network that is related to PKA and TOR (PT) signaling. Genetic variants affecting this PT state globally shifted the molecular network along a single‐dimensional axis, thereby modulating processes including energy and amino acid metabolism, transcription, translation, cell cycle control, and cellular stress response. We propose that genetic effects can propagate through large parts of molecular networks because of the functional requirement to centrally coordinate the activity of fundamental cellular processes.
```
</details>

<details><summary>[8] Archaea, specific genetic traits, and development of improved bacterial live biotherapeutic products: another face of next-generation probiotics — Khaled Fadhlaoui, M. Arnal, Matthieu Martineau, P. Camponova et al. (2020); cutoff-filter date 2020-04-12; doi:10.1007/s00253-020-10599-8</summary>

```text
[8] Archaea, specific genetic traits, and development of improved bacterial live biotherapeutic products: another face of next-generation probiotics
    id: s2:9e0c5116fc0c5ae157400e0354432f4d1de904c5
    date: 2020-04-12
    venue: Applied Microbiology and Biotechnology
    authors: Khaled Fadhlaoui, M. Arnal, Matthieu Martineau, P. Camponova, B. Ollivier, P. O’Toole, J. Brugère
    abstract: [no abstract available]
```
</details>

<details><summary>[9] Archaea Are Interactive Components of Complex Microbiomes. — C. Moissl-Eichinger, Manuela R. Pausan, Julian Taffner, G. Berg et al. (2018); cutoff-filter date 2018-12-31; doi:10.1016/j.tim.2017.07.004</summary>

```text
[9] Archaea Are Interactive Components of Complex Microbiomes.
    id: s2:2dad0f246fe6615befe80f98ae9d943c3431c8fc
    date: 2018
    venue: Trends in Microbiology
    authors: C. Moissl-Eichinger, Manuela R. Pausan, Julian Taffner, G. Berg, C. Bang, R. Schmitz
    abstract: [no abstract available]
```
</details>

<details><summary>[10] Genetic Identification of Cell Types Underlying Brain Complex Traits Yields Insights Into the Etiology of Parkinson’s Disease — Julien Bryois, N. Skene, T. Hansen, L. Kogelman et al. (2020); cutoff-filter date 2020-04-27; doi:10.1038/s41588-020-0610-9</summary>

```text
[10] Genetic Identification of Cell Types Underlying Brain Complex Traits Yields Insights Into the Etiology of Parkinson’s Disease
    id: s2:deda10df1744057a16da9859aba1cf654a74f9d1
    date: 2020-04-27
    venue: Nature Genetics
    authors: Julien Bryois, N. Skene, T. Hansen, L. Kogelman, Hunna J. Watson, Leo Brueggeman, G. Breen, C. Bulik
    abstract: Genome-wide association studies have discovered hundreds of loci associated with complex brain disorders, but it remains unclear in which cell types these loci are active. Here we integrate genome-wide association study results with single-cell transcriptomic data from the entire mouse nervous system to systematically identify cell types underlying brain complex traits. We show that psychiatric disorders are predominantly associated with projecting excitatory and inhibitory neurons. Neurological diseases were associated with different cell types, which is consistent with other lines of evidence. Notably, Parkinson’s disease was genetically associated not only with cholinergic and monoaminergic neurons (which include dopaminergic neurons) but also with enteric neurons and oligodendrocytes. Using post-mortem brain transcriptomic data, we confirmed alterations in these cells, even at the earliest stages of disease progression. Our study provides an important framework for understanding the cellular basis of complex brain maladies, and reveals an unexpected role of oligodendrocytes in Parkinson’s disease. Integration of GWAS and single-cell transcriptomic data from the entire nervous system systematically identifies cell types underlying brain complex traits and provides insights into the etiology of Parkinson’s disease.
```
</details>

<details><summary>Post-hoc automated audit — NON-AUTHORITATIVE; uses hidden benchmark annotations</summary>

- primary auditor: `reference_discriminator_recovered`; statuses {'H1': 'negative_or_absent', 'H2': 'positive_or_present'}; discriminative=True
- primary reasoning: H1 (mitochondria-early) predicts that complex eukaryotic traits should not arise in archaeal lineages prior to endosymbiosis, as such complexity is enabled by mitochondria; H2 (complex-host) predicts that such traits can and should arise before mitochondrial acquisition.
- matched hidden reference discriminator: Relative timing of pre-LECA duplications associated with cytoskeleton, membrane trafficking, endomembranes, phagocytosis, and nucleus versus mitochondrial acquisition.
- derived opposition call: `genuine`
- evidence attribution: `informative_evidence_found` — The retrieved literature included a paper (record [5]) that directly reports complex cellular traits in halophilic archaea, specifically cellular differentiation into mycelia and spores, which are typically associated with eukaryotes. This provides strong support for the proposition, and the assessor correctly identified and used this evidence.
- disagreement flags: {'second_rater_vs_primary_discriminative': None, 'second_rater_vs_primary_status': None, 'retest_vs_primary_category': None, 'any': False}
</details>

**Human review** — `generic_component_fact` · reviewer: Research Director · source: D045 · status: `first_pass_model_based_review` · genuinely discriminative: False · silence-as-null error: False · other fields not recorded

---

## #22 · `GP1-glnbp_induced_fit_vs_conformational_selection-X8`

**GP1-glnbp_induced_fit_vs_conformational_selection-X8** — case `glnbp_induced_fit_vs_conformational_selection`, node `X8`

> Ligand binding can occur to the open conformation of periplasmic binding proteins before a conformational change to the closed state.

- generated from **H2** (Candidate A); abstraction: `class`
- generator's stated reason: The claim asserts that glutamine binds to the open form of GlnBP, which is a periplasmic binding protein, implying that ligand binding to the open state is possible in this protein family.
- influence: **0.254** (rank 6 in case, 22 overall; cumulative 59%) — favours **H2**
- log-likelihood contribution: H2 +1.192, H1 +0.939
- removing it alone: evidence withheld → case log-odds +1.588 (ranking unchanged); node deleted → +1.588 (ranking unchanged)

**Hypotheses (as shown to the verifier)**

- **H1** (Candidate B): Apo-GlnBP samples a pre-existing binding-competent closed or semi-closed conformation; glutamine preferentially binds/captures that pre-existing conformation.
- **H2** (Candidate A): Glutamine binds to open/binding-competent GlnBP before the major protein conformational rearrangement, after which GlnBP closes around the ligand.

**Verifier cross-hypothesis judgments** — P(X|H) combines these by noisy-OR

| hypothesis | origin? | direct edge | route via parent | P(X\|H) |
| --- | --- | --- | --- | --- |
| H2 | yes | `strongly_implied` | X1 [H→parent `strongly_implied`, P=0.95] → `implied` | 0.989 |
| H1 | no | `unlikely` | X1 [H→parent `strongly_contradicted`, P=0.10] → `implied` | 0.671 |

- edge rationale, **H2** → node: Candidate A explicitly states that ligand binding occurs to the open conformation before the protein closes, making the proposition nearly certain if A is true.
- edge rationale, **H1** → node: Candidate B asserts that ligand binding occurs to a pre-existing closed or semi-closed conformation, making binding to the open state less likely if B is true.
- parent `X1`: Glutamine is bound to the open conformation of E. coli GlnBP prior to the protein's transition to the closed state.
- chain rationale, `X1` → node: The parent describes ligand binding to the open conformation in a specific periplasmic binding protein, which suggests this mechanism can occur in the broader class but does not guarantee it for all members.

**Verifier evidence** — label used in score: `support` (log-LR +1.2)

- queries: `periplasmic binding protein open conformation ligand`; `periplasmic binding protein ligand binding kinetics`
- assessor rationale: Record [10] directly states that the S72P mutant of the periplasmic histidine-binding protein binds ligand to the open form, without transitioning to a closed conformation. This is direct evidence that ligand binding can occur to the open conformation before any conformational change to the closed state. No other records directly address ligand binding to the open conformation, though several discuss conformational changes and ligand binding in general.
- supporting spans cited by the assessor:
  - "S72P binds the ligand to the open form, but does not assume a recognizable closed form."
- 10 papers shown; key papers: `s2:5161ab94b09b87a1591e6e301e322ee81ff08dde`
- _The evidence assessor returns ONE label for the node from all papers shown; the method has no per-paper contribution. Key papers and spans are those the assessor cited._

<details><summary>[1] Open Conformation of the Escherichia coli Periplasmic Murein Tripeptide Binding Protein, MppA, at High Resolution — F. Bhatt, V. Patel, C. Jeffery (2018); cutoff-filter date 2018-05-19; doi:10.3390/biology7020030</summary>

```text
[1] Open Conformation of the Escherichia coli Periplasmic Murein Tripeptide Binding Protein, MppA, at High Resolution
    id: s2:5a47e8bc5487d7f664fdf14bd73afa31c6dd440f
    date: 2018-05-19
    venue: Biology
    authors: F. Bhatt, V. Patel, C. Jeffery
    abstract: Periplasmic ligand-binding proteins (PBPs) bind ligands with a high affinity and specificity. They undergo a large conformational change upon ligand binding, and they have a robust protein fold. These physical features have made them ideal candidates for use in protein engineering projects to develop novel biosensors and signaling molecules. The Escherichia coli MppA (murein peptide permease A) PBP binds the murein tripeptide, l-alanyl-γ-d-glutamyl-meso-diaminopimelate, (l-Ala-γ-d-Glu-meso-Dap), which contains both a D-amino acid and a gamma linkage between two of the amino acids. We have solved a high-resolution X-ray crystal structure of E. coli MppA at 1.5 Å resolution in the unliganded, open conformation. Now, structures are available for this member of the PBP protein family in both the liganded/closed form and the unliganded/open form.
```
</details>

<details><summary>[2] The Open Conformation Satisfies Multiple NMR Experiments on Apo Glutamine-Binding Protein: Overcoming Pitfalls in the Study of Interdomain Dynamics — H. Kooshapur, Junhe Ma, N. Tjandra, G. Bermejo (2019); cutoff-filter date 2019-09-13; doi:10.1002/anie.201911015</summary>

```text
[2] The Open Conformation Satisfies Multiple NMR Experiments on Apo Glutamine-Binding Protein: Overcoming Pitfalls in the Study of Interdomain Dynamics
    id: s2:eb71f0a80f7f2961fcf1898dd7951b1b511f449b
    date: 2019-09-13
    venue: Angewandte Chemie
    authors: H. Kooshapur, Junhe Ma, N. Tjandra, G. Bermejo
    abstract: Glutamine-binding protein (GlnBP) from Escherichia coli is a prototypical periplasmic binding protein that has been crystallized in an apo, “open” conformation, with its two domains far apart, and a holo, “closed” form, with proximal domains that engulf the cognate L-Gln ligand. A fundamental question about such large-scale conformational transitions—whether the closed state exists in the absence of ligand—is a matter of controversy in the case of GlnBP. Previously, NMR observations have indicated no evidence of the closed form, whereas experimentally validated computations have suggested a remarkable ~40% population. Here, a paramagnetic NMR strategy designed to specifically detect the putative apo-closed species shows that a major population of the latter is highly improbable. Further, NMR residual dipolar couplings collected under three anisotropic conditions fail to reveal differential domain alignment (which would otherwise signal interdomain dynamics) and establish that the average solution conformation is satisfied by the apo-open crystal structure. Our results indicate that the computational prediction of large-scale interdomain motions is far from trivial and may lead to grossly erroneous conclusions without proper experimental validation.
```
</details>

<details><summary>[3] Ligand-induced structural changes analysis of ribose-binding protein as studied by molecular dynamics simulations — Hai-Yan Li, Zanxia Cao, Guodong Hu, Li-Ling Zhao et al. (2021); cutoff-filter date 2021-03-02; doi:10.3233/thc-218011</summary>

```text
[3] Ligand-induced structural changes analysis of ribose-binding protein as studied by molecular dynamics simulations
    id: s2:b407302d7c1be527f2abbdc5b5075a4a215f7ec3
    date: 2021-01-01
    venue: Technology and Health Care
    authors: Hai-Yan Li, Zanxia Cao, Guodong Hu, Li-Ling Zhao, Chun-Ling Wang, Jihua Wang
    abstract: BACKGROUND: The ribose-binding protein (RBP) from Escherichia coli is one of the representative structures of periplasmic binding proteins. Binding of ribose at the cleft between two domains causes a conformational change corresponding to a closure of two domains around the ligand. The RBP has been crystallized in the open and closed conformations. OBJECTIVE: With the complex trajectory as a control, our goal was to study the conformation changes induced by the detachment of the ligand, and the results have been revealed from two computational tools, MD simulations and elastic network models. METHODS: Molecular dynamics (MD) simulations were performed to study the conformation changes of RBP starting from the open-apo, closed-holo and closed-apo conformations. RESULTS: The evolution of the domain opening angle θ clearly indicates large structural changes. The simulations indicate that the closed states in the absence of ribose are inclined to transition to the open states and that ribose-free RBP exists in a wide range of conformations. The first three dominant principal motions derived from the closed-apo trajectories, consisting of rotating, bending and twisting motions, account for the major rearrangement of the domains from the closed to the open conformation. CONCLUSIONS: The motions showed a strong one-to-one correspondence with the slowest modes from our previous study of RBP with the anisotropic network model (ANM). The results obtained for RBP contribute to the generalization of robustness for protein domain motion studies using either the ANM or PCA for trajectories obtained from MD.
```
</details>

<details><summary>[4] The mechanism of ligand binding to the periplasmic C4-dicarboxylate binding protein (DctP) from Rhodobacter capsulatus. — A. Walmsley, Jonathan G. Shaw, David J. Kelly (1992); cutoff-filter date 1992-04-30; doi:10.1016/s0021-9258(18)42408-8</summary>

```text
[4] The mechanism of ligand binding to the periplasmic C4-dicarboxylate binding protein (DctP) from Rhodobacter capsulatus.
    id: s2:eed159a6397468593a7f59bff05e8ddfca83e770
    date: 1992-04-25
    venue: Journal of Biological Chemistry
    authors: A. Walmsley, Jonathan G. Shaw, David J. Kelly
    abstract: The kinetics of ligand binding to the periplasmic C4-dicarboxylate binding protein (DctP) from Rhodobacter capsulatus were investigated by exploiting the changes in the intrinsic fluorescence of the protein upon binding ligands. Steady state measurements have shown that L-malate, succinate, and fumarate are all bound with sub-micromolar Kd values, whereas D-malate is bound 2 orders of magnitude more weakly. Stopped-flow studies have revealed that the binding process involves at least three steps. In the absence of ligand, the protein is in equilibrium between an essentially nonbinding form, BP1, and the binding form, BP2. Ligands bind to the BP2 form, shifting the equilibrium toward the BP2-L conformation, and also inducing a further isomerization of the protein, to the BP3-L form. The kinetic properties of the four different conformational states of the DctP protein identified in this study would be consistent with their identification as the closed-conformation, the open-conformation, an open-liganded conformation, and a closed-liganded conformation. The latter three states have been identified by x-ray crystallographic studies of binding proteins, but no kinetic or structural data have been presented previously to support the possibility of a closed but unliganded conformation.
```
</details>

<details><summary>[5] The histidine-binding protein undergoes conformational changes in the absence of ligand as analyzed with conformation-specific monoclonal antibodies. — Amnon Wolf, Eudean Shaw, K. Nikaido, G. Ames (1994); cutoff-filter date 1994-09-16; https://www.semanticscholar.org/paper/3b0dd1ee3b724effc5b9f352cc2cb5c8162af718</summary>

```text
[5] The histidine-binding protein undergoes conformational changes in the absence of ligand as analyzed with conformation-specific monoclonal antibodies.
    id: s2:3b0dd1ee3b724effc5b9f352cc2cb5c8162af718
    date: 1994-09-16
    venue: Journal of Biological Chemistry
    authors: Amnon Wolf, Eudean Shaw, K. Nikaido, G. Ames
    abstract: [no abstract available]
```
</details>

<details><summary>[6] Molecular dynamics simulations of ligand-induced backbone conformational changes in the binding site of the periplasmic lysine-, arginine-, ornithine-binding protein — Ami C. C. Yang, R. L. Mancera (2008); cutoff-filter date 2008-04-15; doi:10.1007/s10822-008-9215-6</summary>

```text
[6] Molecular dynamics simulations of ligand-induced backbone conformational changes in the binding site of the periplasmic lysine-, arginine-, ornithine-binding protein
    id: s2:deb7e3db9243189002027cb47e49f07860ecb85b
    date: 2008-04-15
    venue: J. Comput. Aided Mol. Des.
    authors: Ami C. C. Yang, R. L. Mancera
    abstract: [no abstract available]
```
</details>

<details><summary>[7] Accessing a Hidden Conformation of the Maltose Binding Protein Using Accelerated Molecular Dynamics — Denis Bucher, Barry J. Grant, P. Markwick, J. McCammon (2011); cutoff-filter date 2011-04-21; doi:10.1371/journal.pcbi.1002034</summary>

```text
[7] Accessing a Hidden Conformation of the Maltose Binding Protein Using Accelerated Molecular Dynamics
    id: s2:4bd83fb543e1b02d0746b468bd934d5d23db3848
    date: 2011-04-01
    venue: PLoS Comput. Biol.
    authors: Denis Bucher, Barry J. Grant, P. Markwick, J. McCammon
    abstract: Periplasmic binding proteins (PBPs) are a large family of molecular transporters that play a key role in nutrient uptake and chemotaxis in Gram-negative bacteria. All PBPs have characteristic two-domain architecture with a central interdomain ligand-binding cleft. Upon binding to their respective ligands, PBPs undergo a large conformational change that effectively closes the binding cleft. This conformational change is traditionally viewed as a ligand induced-fit process; however, the intrinsic dynamics of the protein may also be crucial for ligand recognition. Recent NMR paramagnetic relaxation enhancement (PRE) experiments have shown that the maltose binding protein (MBP) - a prototypical member of the PBP superfamily - exists in a rapidly exchanging (ns to µs regime) mixture comprising an open state (approx 95%), and a minor partially closed state (approx 5%). Here we describe accelerated MD simulations that provide a detailed picture of the transition between the open and partially closed states, and confirm the existence of a dynamical equilibrium between these two states in apo MBP. We find that a flexible part of the protein called the balancing interface motif (residues 175–184) is displaced during the transformation. Continuum electrostatic calculations indicate that the repacking of non-polar residues near the hinge region plays an important role in driving the conformational change. Oscillations between open and partially closed states create variations in the shape and size of the binding site. The study provides a detailed description of the conformational space available to ligand-free MBP, and has implications for understanding ligand recognition and allostery in related proteins.
```
</details>

<details><summary>[8] Opening and closing motions in the periplasmic vitamin B12 binding protein BtuF. — Christian Kandt, Zhi-Tao Xu, D. Tieleman (2006); cutoff-filter date 2006-10-13; doi:10.1021/bi061280j</summary>

```text
[8] Opening and closing motions in the periplasmic vitamin B12 binding protein BtuF.
    id: s2:079537c6be5248ab15869c8af132fead69a0473a
    date: 2006-10-13
    venue: Biochemistry
    authors: Christian Kandt, Zhi-Tao Xu, D. Tieleman
    abstract: [no abstract available]
```
</details>

<details><summary>[9] Determination of the Solution Bound Conformation of an Amino-acid Binding Protein by NMR Paramagnetic Relaxation Enhancement: Use of a Single Flexible Paramagnetic Probe with Improved Estimation of Its Sampling Space — G. Bermejo, M. Strub, C. Ho, N. Tjandra (2009); cutoff-filter date 2009-07-15; doi:10.1021/ja902436g</summary>

```text
[9] Determination of the Solution Bound Conformation of an Amino-acid Binding Protein by NMR Paramagnetic Relaxation Enhancement: Use of a Single Flexible Paramagnetic Probe with Improved Estimation of Its Sampling Space
    id: s2:1cbc73facc1f2878f174180c43b8dddfc23c2c61
    date: 2009-07-15
    venue: Journal of the American Chemical Society
    authors: G. Bermejo, M. Strub, C. Ho, N. Tjandra
    abstract: We demonstrate the feasibility of elucidating the bound (“closed”) conformation of a periplasmic binding protein, the glutamine-binding protein (GlnBP), in solution, using paramagnetic relaxation enhancements (PREs) arising from a single paramagnetic group. GlnBP consists of two globular domains connected by a hinge. Using the ligand-free (“open”) conformation as a starting point, conjoined rigid-body/torsion-angle simulated annealing calculations were performed using backbone 1HN-PREs as a major source of distance information. Paramagnetic probe flexibility was accounted for via a multiple-conformer representation. A conventional approach where the entire PRE data set is enforced at once during simulated annealing yielded poor results due to inappropriate conformational sampling of the probe. On the other hand, significant improvements in coordinate accuracy were obtained by estimating the probe sampling space prior to structure calculation. Such sampling is achieved by refining the ensemble of probe conformers with intra-domain PREs only, keeping the protein backbone fixed in the open form. Subsequently, while constraining the probe to the previously found conformations, the domains are allowed to move relative to each other under the influence of the non-intra-domain PREs, giving the hinge region torsional degrees of freedom. Thus, by partitioning the protocol into a “probe sampling” and a “backbone sampling” stage, structures significantly closer to the X-ray structure of ligand-bound GlnBP were obtained.
```
</details>

<details><summary>[10] **KEY** Structure/Function Analysis of the Periplasmic Histidine-binding Protein — Amnon Wolf, Eudean Shaw, B. Oh, H. D. De Bondt et al. (1995); cutoff-filter date 1995-07-31; doi:10.1074/jbc.270.27.16097</summary>

```text
[10] Structure/Function Analysis of the Periplasmic Histidine-binding Protein
    id: s2:5161ab94b09b87a1591e6e301e322ee81ff08dde
    date: 1995-07-07
    venue: Journal of Biological Chemistry
    authors: Amnon Wolf, Eudean Shaw, B. Oh, H. D. De Bondt, A. Joshi, G. Ames
    abstract: The periplasmic histidine-binding protein, HisJ, is a receptor for the histidine permease of Salmonella typhimurium. Receptors of this type are composed of two lobes that are far apart in the unliganded structure (open conformation) and drawn close together in the liganded structure (closed conformation). The binding of the ligand, in a cleft between the lobes, stabilizes the closed conformation. Such receptors have several functions in transport: interaction with the membrane-bound complex, transmission of a transmembrane signal to hydrolyze ATP, and receiving a signal to open the lobes and release the ligand. In this study the mechanism of action of HisJ was further investigated using mutant proteins defective in ligand binding activity and closed form-specific monoclonal antibodies (Wolf, A., Shaw, E. W., Nikaido, K., and Ames G. F.-L.(1994) J. Biol. Chem. 269, 23051-23058). Y14H is defective in stabilization of the closed form, does not assume the closed empty form, and assumes an altered closed liganded form. T121A and G119R are similar to Y14H, but assume a normal closed liganded form. S72P binds the ligand to the open form, but does not assume a recognizable closed form. S92F is defective in the ability to undergo conformational change and to stabilize the closed form. All other mutant proteins appear to fall within one of these four categories. The biochemical characterization of these mutant proteins agrees with the structural analysis of the protein. We suggest that mutant proteins that do not assume the normal closed form, in addition to their defect in ligand binding, fail to interact with the membrane-bound complex and/or to transmit transmembrane signals.
```
</details>

<details><summary>Post-hoc automated audit — NON-AUTHORITATIVE; uses hidden benchmark annotations</summary>

- primary auditor: `reference_discriminator_recovered`; statuses {'H2': 'positive_or_present', 'H1': 'negative_or_absent'}; discriminative=True
- primary reasoning: H2 (induced fit) predicts that ligand binding can occur to the open conformation before closure, so the proposition is positive under H2. H1 (conformational selection) predicts that ligand binding occurs to a pre-existing closed or semi-closed state, so binding to the open state should not occur, making the proposition negative under H1.
- matched hidden reference discriminator: Induced fit does not require detectable pre-existing apo closed-state exchange; ligand binding can precede the major closure.
- derived opposition call: `genuine`
- evidence attribution: `informative_evidence_found` — The retrieval system surfaced a paper (record [10]) that directly addresses the proposition by describing a mutant periplasmic binding protein that binds ligand in the open conformation without transitioning to the closed state. The assessor correctly identified and used this as direct evidence. The process worked as intended.
- disagreement flags: {'second_rater_vs_primary_discriminative': None, 'second_rater_vs_primary_status': None, 'retest_vs_primary_category': None, 'any': False}
</details>

**Human review** — `generic_component_fact` · reviewer: Research Director · source: D045 · status: `first_pass_model_based_review` · genuinely discriminative: False · silence-as-null error: False · other fields not recorded

---

## #23 · `GP1-glnbp_induced_fit_vs_conformational_selection-X9`

**GP1-glnbp_induced_fit_vs_conformational_selection-X9** — case `glnbp_induced_fit_vs_conformational_selection`, node `X9`

> The transition from open to closed conformation in E. coli GlnBP is triggered by glutamine binding.

- generated from **H2** (Candidate A); abstraction: `mechanistic`
- generator's stated reason: The claim states that glutamine binds before the conformational change, implying that ligand binding initiates the transition.
- influence: **0.254** (rank 7 in case, 23 overall; cumulative 60%) — favours **H2**
- log-likelihood contribution: H2 +1.192, H1 +0.939
- removing it alone: evidence withheld → case log-odds +1.588 (ranking unchanged); node deleted → +1.588 (ranking unchanged)

**Hypotheses (as shown to the verifier)**

- **H1** (Candidate B): Apo-GlnBP samples a pre-existing binding-competent closed or semi-closed conformation; glutamine preferentially binds/captures that pre-existing conformation.
- **H2** (Candidate A): Glutamine binds to open/binding-competent GlnBP before the major protein conformational rearrangement, after which GlnBP closes around the ligand.

**Verifier cross-hypothesis judgments** — P(X|H) combines these by noisy-OR

| hypothesis | origin? | direct edge | route via parent | P(X\|H) |
| --- | --- | --- | --- | --- |
| H2 | yes | `strongly_implied` | X1 [H→parent `strongly_implied`, P=0.95] → `implied` | 0.989 |
| H1 | no | `unlikely` | X1 [H→parent `strongly_contradicted`, P=0.10] → `implied` | 0.671 |

- edge rationale, **H2** → node: Candidate A states that glutamine binding occurs before and triggers the conformational change to the closed state, directly supporting the proposition.
- edge rationale, **H1** → node: Candidate B suggests that the closed conformation exists prior to glutamine binding and that glutamine binds to this pre-existing state, making it unlikely that binding triggers the transition.
- parent `X1`: Glutamine is bound to the open conformation of E. coli GlnBP prior to the protein's transition to the closed state.
- chain rationale, `X1` → node: If glutamine is bound before the protein transitions to the closed state, it suggests that glutamine binding is associated with or may trigger the conformational change, though it does not definitively establish causality.

**Verifier evidence** — label used in score: `support` (log-LR +1.2)

- queries: `E. coli GlnBP glutamine binding`; `GlnBP conformational change glutamine`
- assessor rationale: Record [1] directly states that E. coli GlnBP is crystallized in an open conformation when apo and in a closed conformation when bound to glutamine, indicating that glutamine binding triggers the transition. No other records provide direct evidence, as their abstracts are unavailable. The statement in [1] is clear and directly addresses the proposition.
- supporting spans cited by the assessor:
  - "Glutamine-binding protein (GlnBP) from Escherichia coli is a prototypical periplasmic binding protein that has been crystallized in an apo, “open” conformation, with its two domains far apart, and a holo, “closed” form, with proximal domains that engulf the cognate L-Gln ligand."
- 10 papers shown; key papers: `s2:eb71f0a80f7f2961fcf1898dd7951b1b511f449b`
- _The evidence assessor returns ONE label for the node from all papers shown; the method has no per-paper contribution. Key papers and spans are those the assessor cited._

<details><summary>[1] **KEY** The Open Conformation Satisfies Multiple NMR Experiments on Apo Glutamine-Binding Protein: Overcoming Pitfalls in the Study of Interdomain Dynamics — H. Kooshapur, Junhe Ma, N. Tjandra, G. Bermejo (2019); cutoff-filter date 2019-09-13; doi:10.1002/anie.201911015</summary>

```text
[1] The Open Conformation Satisfies Multiple NMR Experiments on Apo Glutamine-Binding Protein: Overcoming Pitfalls in the Study of Interdomain Dynamics
    id: s2:eb71f0a80f7f2961fcf1898dd7951b1b511f449b
    date: 2019-09-13
    venue: Angewandte Chemie
    authors: H. Kooshapur, Junhe Ma, N. Tjandra, G. Bermejo
    abstract: Glutamine-binding protein (GlnBP) from Escherichia coli is a prototypical periplasmic binding protein that has been crystallized in an apo, “open” conformation, with its two domains far apart, and a holo, “closed” form, with proximal domains that engulf the cognate L-Gln ligand. A fundamental question about such large-scale conformational transitions—whether the closed state exists in the absence of ligand—is a matter of controversy in the case of GlnBP. Previously, NMR observations have indicated no evidence of the closed form, whereas experimentally validated computations have suggested a remarkable ~40% population. Here, a paramagnetic NMR strategy designed to specifically detect the putative apo-closed species shows that a major population of the latter is highly improbable. Further, NMR residual dipolar couplings collected under three anisotropic conditions fail to reveal differential domain alignment (which would otherwise signal interdomain dynamics) and establish that the average solution conformation is satisfied by the apo-open crystal structure. Our results indicate that the computational prediction of large-scale interdomain motions is far from trivial and may lead to grossly erroneous conclusions without proper experimental validation.
```
</details>

<details><summary>[2] Resolution of fluorescence intensity decays of the two tryptophan residues in glutamine-binding protein from Escherichia coli using single tryptophan mutants. — Paul H. Axelsen, Z. Bajzer, Franklyn G. Prendergast, P. F. Cottam et al. (1991); cutoff-filter date 1991-09-30; doi:10.1016/s0006-3495(91)82094-x</summary>

```text
[2] Resolution of fluorescence intensity decays of the two tryptophan residues in glutamine-binding protein from Escherichia coli using single tryptophan mutants.
    id: s2:1da6922ec288625ed013e6f584a07f3658c5c203
    date: 1991-09-01
    venue: Biophysical Journal
    authors: Paul H. Axelsen, Z. Bajzer, Franklyn G. Prendergast, P. F. Cottam, C. Ho
    abstract: [no abstract available]
```
</details>

<details><summary>[3] A Recombinant Glutamine‐Binding Protein from Escherichia coli: Effect of Ligand‐Binding on Protein Conformational Dynamics — P. Heřman, J. Večeř, V. Scognamiglio, M. Staiano et al. (2004); cutoff-filter date 2004-12-31; doi:10.1021/bp049956u</summary>

```text
[3] A Recombinant Glutamine‐Binding Protein from Escherichia coli: Effect of Ligand‐Binding on Protein Conformational Dynamics
    id: s2:ea760e1a1e5ac6db1e812e374853333e2c600945
    date: 2004
    venue: Biotechnology progress (Print)
    authors: P. Heřman, J. Večeř, V. Scognamiglio, M. Staiano, M. Rossi, S. d'Auria
    abstract: [no abstract available]
```
</details>

<details><summary>[4] Glutamine-binding protein from Escherichia coli specifically binds a wheat gliadin peptide allowing the design of a new porous silicon-based optical biosensor. — L. de Stefano, M. Rossi, M. Staiano, G. Mamone et al. (2006); cutoff-filter date 2006-03-21; doi:10.1021/pr0600226</summary>

```text
[4] Glutamine-binding protein from Escherichia coli specifically binds a wheat gliadin peptide allowing the design of a new porous silicon-based optical biosensor.
    id: s2:bba7d9831daa36326559df0c14c36d6a3f9ff3d5
    date: 2006-03-21
    venue: Journal of Proteome Research
    authors: L. de Stefano, M. Rossi, M. Staiano, G. Mamone, Antonoietta Parracino, L. Rotiroti, I. Rendina, M. Rossi
    abstract: [no abstract available]
```
</details>

<details><summary>[5] [The structure and stability of the glutamine-binding protein from Escherichia coli and its complex with glutamine]. — O. Stepanenko, I. Kuznetsova, K. K. Turoverov, V. Scognamiglio et al. (2005); cutoff-filter date 2005-12-31; https://www.semanticscholar.org/paper/1e4abe5ff5247346bfd64a67b7db462222bdc417</summary>

```text
[5] [The structure and stability of the glutamine-binding protein from Escherichia coli and its complex with glutamine].
    id: s2:1e4abe5ff5247346bfd64a67b7db462222bdc417
    date: 2005
    venue: Tsitologiya
    authors: O. Stepanenko, I. Kuznetsova, K. K. Turoverov, V. Scognamiglio, M. Staiano, S. D'Auria
    abstract: [no abstract available]
    note: possibly the same work as s2:3e30d9038418fe0db4f748c0133ac87451eaa72b
```
</details>

<details><summary>[6] An investigation of the ligand-binding site of the glutamine-binding protein of Escherichia coli using rotational-echo double-resonance NMR. — Andrew W. Hing, N. Tjandra, Patricia F. Cottam, Jacob Schaefer et al. (1994); cutoff-filter date 1994-07-26; doi:10.1021/bi00195a005</summary>

```text
[6] An investigation of the ligand-binding site of the glutamine-binding protein of Escherichia coli using rotational-echo double-resonance NMR.
    id: s2:4705c9080232bf4fbf728f7aad8f86b6a6d024ea
    date: 1994-07-26
    venue: Biochemistry
    authors: Andrew W. Hing, N. Tjandra, Patricia F. Cottam, Jacob Schaefer, Chien Ho
    abstract: [no abstract available]
```
</details>

<details><summary>[7] Binding of glutamine to glutamine‐binding protein from Escherichia coli induces changes in protein structure and increases protein stability — S. d'Auria, Andrea Scirè, A. Varriale, V. Scognamiglio et al. (2004); cutoff-filter date 2004-10-29; doi:10.1002/prot.20289</summary>

```text
[7] Binding of glutamine to glutamine‐binding protein from Escherichia coli induces changes in protein structure and increases protein stability
    id: s2:6fb71d8a4338cc017f7aa99b5d224eb52cdcf051
    date: 2004-10-29
    venue: Proteins: Structure, Function, and Bioinformatics
    authors: S. d'Auria, Andrea Scirè, A. Varriale, V. Scognamiglio, M. Staiano, A. Ausili, A. Marabotti, M. Rossi
    abstract: [no abstract available]
```
</details>

<details><summary>[8] Unfolding and refolding of the glutamine-binding protein from Escherichia coli and its complex with glutamine induced by guanidine hydrochloride. — M. Staiano, V. Scognamiglio, M. Rossi, S. d'Auria et al. (2005); cutoff-filter date 2005-03-25; doi:10.1021/bi0478300</summary>

```text
[8] Unfolding and refolding of the glutamine-binding protein from Escherichia coli and its complex with glutamine induced by guanidine hydrochloride.
    id: s2:41ad542985767d9a9bcc6542828182df8103f413
    date: 2005-03-25
    venue: Biochemistry
    authors: M. Staiano, V. Scognamiglio, M. Rossi, S. d'Auria, O. Stepanenko, I. Kuznetsova, K. K. Turoverov
    abstract: [no abstract available]
```
</details>

<details><summary>[9] Fluorescence properties of glutamine-binding protein from Escherichia coli and its complex with glutamine. — I. Kuznetsova, O. Stepanenko, K. K. Turoverov, M. Staiano et al. (2005); cutoff-filter date 2005-02-08; doi:10.1021/pr0498077</summary>

```text
[9] Fluorescence properties of glutamine-binding protein from Escherichia coli and its complex with glutamine.
    id: s2:3e30d9038418fe0db4f748c0133ac87451eaa72b
    date: 2005-02-08
    venue: Journal of Proteome Research
    authors: I. Kuznetsova, O. Stepanenko, K. K. Turoverov, M. Staiano, V. Scognamiglio, M. Rossi, S. d'Auria
    abstract: [no abstract available]
    note: possibly the same work as s2:1e4abe5ff5247346bfd64a67b7db462222bdc417
```
</details>

<details><summary>[10] The differences in the microenvironment of the two tryptophan residues of the glutamine‐binding protein from Escherichia coli shed light on the binding properties and the structural dynamics of the protein — S. d'Auria, M. Staiano, A. Varriale, M. Gonnelli et al. (2008); cutoff-filter date 2008-05-01; doi:10.1002/prot.21748</summary>

```text
[10] The differences in the microenvironment of the two tryptophan residues of the glutamine‐binding protein from Escherichia coli shed light on the binding properties and the structural dynamics of the protein
    id: s2:89830a1784ec7a7de86860e55291c55823676f53
    date: 2008-05-01
    venue: Proteins: Structure, Function, and Bioinformatics
    authors: S. d'Auria, M. Staiano, A. Varriale, M. Gonnelli, A. Marabotti, M. Rossi, Giovanni B. Strambini
    abstract: [no abstract available]
```
</details>

<details><summary>Post-hoc automated audit — NON-AUTHORITATIVE; uses hidden benchmark annotations</summary>

- primary auditor: `silence_as_null_error`; statuses {'H2': 'positive_or_present', 'H1': 'indeterminate'}; discriminative=False
- primary reasoning: H2 (induced fit) predicts that glutamine binding triggers the open-to-closed transition, so the proposition is positive under H2. H1 (conformational selection) is silent on whether glutamine binding triggers the transition, as it posits that the closed state pre-exists and glutamine binds to it, so the proposition is indeterminate under H1.
- derived opposition call: `manufactured_from_silence`
- evidence attribution: `informative_evidence_found` — The retrieval system surfaced a paper ([1]) that directly addresses the proposition, stating that E. coli GlnBP transitions from open to closed conformation upon glutamine binding. The assessor correctly identified this as support. The queries were appropriate and the process worked as intended.
- disagreement flags: {'second_rater_vs_primary_discriminative': None, 'second_rater_vs_primary_status': None, 'retest_vs_primary_category': None, 'any': False}
</details>

**Human review** — `genuine_discriminator` · reviewer: Research Director · source: D045 · status: `first_pass_model_based_review` · genuinely discriminative: True · silence-as-null error: False · other fields not recorded

---

## #24 · `GP1-pfc_storage_vs_control-X14`

**GP1-pfc_storage_vs_control-X14** — case `pfc_storage_vs_control`, node `X14`

> Neural firing rates in prefrontal cortex encode the specific features of memorized stimuli during the delay period of a visual working memory task.

- generated from **H1** (Candidate A); abstraction: `mechanistic`
- generator's stated reason: If persistent activity in prefrontal cortex encodes mnemonic content, then neural firing rates should reflect the features of memorized items during maintenance.
- influence: **0.247** (rank 5 in case, 24 overall; cumulative 61%) — favours **H1**
- log-likelihood contribution: H1 +1.962, H2 +1.715
- removing it alone: evidence withheld → case log-odds +0.967 (ranking unchanged); node deleted → +0.967 (ranking unchanged)

**Hypotheses (as shown to the verifier)**

- **H1** (Candidate A): Prefrontal persistent activity is itself a substrate for working-memory storage; disrupting the relevant PFC population therefore disrupts the stored mnemonic representation.
- **H2** (Candidate B): PFC primarily controls, prioritizes, or allocates resources to working-memory representations maintained in sensory/posterior regions rather than directly storing the mnemonic content itself.

**Verifier cross-hypothesis judgments** — P(X|H) combines these by noisy-OR

| hypothesis | origin? | direct edge | route via parent | P(X\|H) |
| --- | --- | --- | --- | --- |
| H1 | yes | `implied` | X2 [H→parent `strongly_implied`, P=0.95] → `implied` | 0.957 |
| H2 | no | `unlikely` | X2 [H→parent `unlikely`, P=0.30] → `implied` | 0.713 |

- edge rationale, **H1** → node: If persistent activity in PFC is the substrate for working-memory storage, it is clearly expected that PFC firing rates would encode the specific features of memorized stimuli during the delay period.
- edge rationale, **H2** → node: If PFC mainly controls or allocates resources to representations stored elsewhere, it is less likely that PFC firing rates themselves encode the specific features of memorized stimuli during the delay period.
- parent `X2`: Persistent neural activity in prefrontal cortex encodes the content of items maintained in working memory.
- chain rationale, `X2` → node: If persistent neural activity in prefrontal cortex encodes working memory content, it is implied that neural firing rates could encode specific features of memorized stimuli during the delay period, though the parent does not specify modality or timing.

**Verifier evidence** — label used in score: `strong_support` (log-LR +2.0)

- queries: `prefrontal cortex firing rate delay`; `visual working memory stimulus encoding`
- assessor rationale: Multiple records directly state that prefrontal cortex neurons exhibit stimulus-selective firing rates during the delay period of working memory tasks, encoding specific features of memorized stimuli. These include both spatial and object information, and the selectivity is observed in persistent activity. The evidence is consistent across independent primate studies, and the findings are explicitly reported rather than inferred.
- supporting spans cited by the assessor:
  - "Neurons that generated persistent activity represented more information about the stimuli in both spatial and object working memory tasks."
  - "Although averaged across all neurons and stimuli, firing rate did not appear clearly elevated above baseline during the maintenance of neural activity particularly for object working memory, this grand average masked neurons that generated persistent activity selective for their preferred stimuli, which carried the majority of stimulus information."
  - "This training induces more pronounced changes in anterior prefrontal regions, including increased firing rate during the delay period, selectivity, reliability, information for stimuli, representation of whether a test stimulus matched the remembered cue or not, and variability and correlation between neurons."
  - "In prefrontal cortex (PFC), a neuronal correlate of WM is stimulus-selective persistent activity during the delay."
- 10 papers shown; key papers: `s2:59031196c9d4e166d206b87d4f61f487d140c373`, `s2:5ddd5110a9050cb7760a0058c9e4b94df6b428fd`, `s2:6fe4eca3f9f95977e371eccfccbefa7bf52887b3`
- _The evidence assessor returns ONE label for the node from all papers shown; the method has no per-paper contribution. Key papers and spans are those the assessor cited._

<details><summary>[1] Representations of On-Going Behavior and Future Actions During a Spatial Working Memory Task by a High Firing-Rate Population of Medial Prefrontal Cortex Neurons — J. J. Stout, Amy L. Griffin (2020); cutoff-filter date 2020-08-31; doi:10.3389/fnbeh.2020.00151</summary>

```text
[1] Representations of On-Going Behavior and Future Actions During a Spatial Working Memory Task by a High Firing-Rate Population of Medial Prefrontal Cortex Neurons
    id: s2:234ebf0e8ceab3787e4f78bde2e6b7b20107c75d
    date: 2020-08-31
    venue: Frontiers in Behavioral Neuroscience
    authors: J. J. Stout, Amy L. Griffin
    abstract: Spatial working memory (SWM) requires the encoding, maintenance, and retrieval of spatially relevant information to guide decision-making. The medial prefrontal cortex (mPFC) has long been implicated in the ability of rodents to perform SWM tasks. While past studies have demonstrated that mPFC ensembles reflect past and future experiences, most findings are derived from tasks that have an experimental overlap between the encoding and retrieval of trajectory specific information. In this study, we recorded single units from the mPFC of rats as they performed a T-maze delayed non-match to position (DNMP) task. This task consists of an encoding dominant sample phase, a memory maintenance delay period, and retrieval dominant choice phase. Using a linear classifier, we investigated whether distinct ensembles collectively reflect various trajectory-dependent experiences. We find that a population of high-firing rate mPFC neurons both predict a future choice and reflect changes in trajectory-dependent behaviors. We then developed a modeling procedure that estimated the number of high and low-firing rate units required to dissociate between various experiences. We find that low firing rate ensembles weakly reflect the direction that rats were forced to turn on the sample phase. This was in contrast to the highly active population that could effectively predict both future decision-making on early stem traversals and trajectory-divergences at T-junction. Finally, we compared the ensemble size necessary to code a forced trajectory to the size required to predict a decision. We provide evidence to suggest that a larger number of highly active neurons are employed during decision-making processes when compared to rewarded forced behaviors. Together, our study provides important insight into how specific ensembles of mPFC units support upcoming choices and ongoing behavior during SWM.
```
</details>

<details><summary>[2] Unexpected Rule-Changes in a Working Memory Task Shape the Firing of Histologically Identified Delay-Tuned Neurons in the Prefrontal Cortex. — A. T. Ozdemir, Michael Lagler, Sabria Lagoun, Hugo Malagon-Vina et al. (2020); cutoff-filter date 2020-02-11; doi:10.1016/j.celrep.2019.12.102</summary>

```text
[2] Unexpected Rule-Changes in a Working Memory Task Shape the Firing of Histologically Identified Delay-Tuned Neurons in the Prefrontal Cortex.
    id: s2:83ceb95758d2ba4f71d58508d38241d9c5ac96a2
    date: 2020-02-04
    venue: Cell Reports
    authors: A. T. Ozdemir, Michael Lagler, Sabria Lagoun, Hugo Malagon-Vina, B. Lasztóczi, T. Klausberger
    abstract: Working memory-guided behaviors require memory retention during delay periods, when subsets of prefrontal neurons have been reported to exhibit persistently elevated firing. What happens to delay activity when information stored in working memory is no longer relevant for guiding behavior? In this study, we perform juxtacellular recording and labeling of delay-tuned (-elevated or -suppressed) neurons in the prelimbic cortex of freely moving rats, performing a familiar delayed cue-matching-to-place task. Unexpectedly, novel task-rules are introduced, rendering information held in working memory irrelevant. Following successful strategy switching within one session, delay-tuned neurons are filled with neurobiotin for histological analysis. Delay-elevated neurons include pyramidal cells with large heterogeneity of soma-dendritic distribution, molecular expression profiles, and task-relevant activity. Rule change induces heterogenous adjustments on individual neurons and ensembles' activity but cumulates in balanced firing rate reorganizations across cortical layers. Our results demonstrate divergent cellular and network dynamics when an abrupt change in task rules interferes with working memory.
```
</details>

<details><summary>[3] **KEY** Decoding working memory information from neurons with and without persistent activity in the primate prefrontal cortex. — Lilianna Thrower, Wen-Hao Dang, Rye G. Jaffe, Jasmine D. Sun et al. (2023); cutoff-filter date 2023-11-01; doi:10.1152/jn.00290.2023</summary>

```text
[3] Decoding working memory information from neurons with and without persistent activity in the primate prefrontal cortex.
    id: s2:59031196c9d4e166d206b87d4f61f487d140c373
    date: 2023-11-01
    venue: Journal of Neurophysiology
    authors: Lilianna Thrower, Wen-Hao Dang, Rye G. Jaffe, Jasmine D. Sun, Christos Constantinidis
    abstract: Persistent activity of neurons in the prefrontal cortex has been thought to represent the information maintained in working memory, though alternative models have challenged this idea. Theories that depend on the dynamic representation of information posit that stimulus information may be maintained by the activity pattern of neurons whose firing rate is not significantly elevated above their baseline during the delay period of working memory tasks. We thus tested the ability of neurons that do and do not generate persistent activity in the prefrontal cortex of monkeys to represent spatial and object information in working memory. Neurons that generated persistent activity represented more information about the stimuli in both spatial and object working memory tasks. The amount of information that could be decoded from neural activity depended on the choice of decoder and parameters used but neurons with persistent activity outperformed non-persistent neurons consistently. Although averaged across all neurons and stimuli, firing rate did not appear clearly elevated above baseline during the maintenance of neural activity particularly for object working memory, this grand average masked neurons that generated persistent activity selective for their preferred stimuli, which carried the majority of stimulus information. These results reveal that prefrontal neurons that generate persistent activity maintain information more reliably during working memory.
    note: possibly the same work as s2:9baaac246204af851f5ed535160cc131431eb3ac
```
</details>

<details><summary>[4] Decoding working memory information from persistent and activity-silent neurons in the primate prefrontal cortex — Lilianna Thrower, Wen-Hao Dang, Rye G. Jaffe, Jasmine D. Sun et al. (2023); cutoff-filter date 2023-07-28; doi:10.1101/2023.07.25.550371</summary>

```text
[4] Decoding working memory information from persistent and activity-silent neurons in the primate prefrontal cortex
    id: s2:9baaac246204af851f5ed535160cc131431eb3ac
    date: 2023-07-28
    venue: bioRxiv (preprint)
    authors: Lilianna Thrower, Wen-Hao Dang, Rye G. Jaffe, Jasmine D. Sun, C. Constantinidis
    abstract: [no abstract available]
    note: possibly the same work as s2:59031196c9d4e166d206b87d4f61f487d140c373
```
</details>

<details><summary>[5] Strong Gamma Frequency Oscillations in the Adolescent Prefrontal Cortex — Zhengyang Wang, Balbir Singh, X. Zhou, C. Constantinidis (2021); cutoff-filter date 2021-08-22; doi:10.1101/2021.08.20.455686</summary>

```text
[5] Strong Gamma Frequency Oscillations in the Adolescent Prefrontal Cortex
    id: s2:9e2c84f07ca3583a7957218eaf8ba3475f261f4a
    date: 2021-08-22
    venue: Journal of Neuroscience (preprint)
    authors: Zhengyang Wang, Balbir Singh, X. Zhou, C. Constantinidis
    abstract: Working memory ability continues to mature into adulthood in humans and nonhuman primates. At the single-neuron level, adolescent development is characterized by increased prefrontal firing rate in the delay period, but less is known about how coordinated activity between neurons is altered. Local field potentials (LFPs) provide a window into the computations conducted by the local network. To address the effects of adolescent development on LFP activity, three male rhesus monkeys were trained to perform an oculomotor delayed response task and tested at both the adolescent and adult stages. Simultaneous single-unit and LFP signals were recorded from areas 8a and 46 of the dorsolateral prefrontal cortex. In both the cue and delay period, power relative to baseline in the gamma frequency range (32–128 Hz) was higher in the adolescent than the adult stage. The changes between developmental stages could not be accounted for by differences in performance and were observed in more posterior as well as more anterior recording sites. In the adult stage, high-firing neurons were also more likely to reside at sites with strong gamma power increase from baseline. For both stages, the gamma power increase in the delay was selective for sites with neuron-encoding stimulus information in their spiking. Our results establish gamma power decrease to be a feature of prefrontal cortical maturation. SIGNIFICANCE STATEMENT Gamma-frequency oscillations in extracellular field recordings (e.g., local field potential or EEG) are a marker of normal interactions between excitatory and inhibitory neurons in neural circuits. Abnormally low gamma power during working memory is seen in conditions such as schizophrenia. We sought to examine whether the immature prefrontal cortex similarly exhibits lower power in the gamma-frequency range during working memory, in a nonhuman primate model of adolescence. Contrary to this expectation, the adolescent PFC exhibited stronger gamma power during the mai [...]
```
</details>

<details><summary>[6] Canonical goal-selective representations are absent from prefrontal cortex in a spatial working memory task requiring behavioral flexibility — C. Böhm, Albert K. Lee (2020); cutoff-filter date 2020-12-24; doi:10.7554/elife.63035</summary>

```text
[6] Canonical goal-selective representations are absent from prefrontal cortex in a spatial working memory task requiring behavioral flexibility
    id: s2:efc5a8c62ef741f8cb33ce54a6e8f2f03ceff75c
    date: 2020-09-11
    venue: bioRxiv (preprint)
    authors: C. Böhm, Albert K. Lee
    abstract: The prefrontal cortex (PFC)’s functions are thought to include working memory, as its activity can reflect information that must be temporarily maintained to realize the current goal. We designed a flexible spatial working memory task that required rats to navigate - after distractions and a delay - to multiple possible goal locations from different starting points and via multiple routes. This made the current goal location the key variable to remember, instead of a particular direction or route to the goal. However, across a broad population of PFC neurons, we found no evidence of current-goal-specific memory in any previously reported form - i.e. differences in the rate, sequence, phase or covariance of firing. This suggests such patterns do not hold working memory in the PFC when information must be employed flexibly. Instead, the PFC grouped locations representing behaviorally equivalent task features together, consistent with a role in encoding long-term knowledge of task structure.
```
</details>

<details><summary>[7] Active avoidance requires inhibitory signaling in the rodent prelimbic prefrontal cortex — Maria M. Diehl, Christian Bravo-Rivera, Jose Rodríguez-Romaguera, Pablo A Pagan-Rivera et al. (2018); cutoff-filter date 2018-05-31; doi:10.7554/elife.34657</summary>

```text
[7] Active avoidance requires inhibitory signaling in the rodent prelimbic prefrontal cortex
    id: s2:a5bd4dc9df756a133f46859bda11512d2e8555cd
    date: 2018-01-02
    venue: bioRxiv (preprint)
    authors: Maria M. Diehl, Christian Bravo-Rivera, Jose Rodríguez-Romaguera, Pablo A Pagan-Rivera, Anthony Burgos-Robles, Ciorana Roman-Ortiz, G. Quirk
    abstract: Much is known about the neural circuits of conditioned fear and its relevance to understanding anxiety disorders, but less is known about other anxiety-related behaviors such as active avoidance. Using a tone-signaled, platform-mediated active avoidance task, we observed that pharmacological inactivation of the prelimbic prefrontal cortex (PL) delayed initiation of avoidance. However, optogenetic silencing of PL neurons did not delay avoidance. Consistent with this finding, inhibitory, but not excitatory, responses of rostral PL neurons to the tone were correlated with initiation of avoidance. To oppose inhibitory responses, we photoactivated rostral PL neurons during the tone to maintain pre-tone firing rate. Photoactivation of rostral PL (but not caudal PL) neurons at 4 Hz (but not 2 Hz) delayed or prevented avoidance. These findings suggest that the initiation of active avoidance requires inhibitory neuronal responses in rostral PL, and underscores the importance of designing behavioral optogenetic studies based on neuronal firing patterns.
```
</details>

<details><summary>[8] **KEY** Anterior-posterior gradient of plasticity in primate prefrontal cortex — M. R. Riley, Xue-Lian Qi, X. Zhou, C. Constantinidis (2018); cutoff-filter date 2018-09-17; doi:10.1038/s41467-018-06226-w</summary>

```text
[8] Anterior-posterior gradient of plasticity in primate prefrontal cortex
    id: s2:6fe4eca3f9f95977e371eccfccbefa7bf52887b3
    date: 2018-09-17
    venue: Nature Communications
    authors: M. R. Riley, Xue-Lian Qi, X. Zhou, C. Constantinidis
    abstract: The functional organization of the primate prefrontal cortex has been a matter of debate with some models speculating dorso-ventral and rostro-caudal specialization while others suggesting that information is represented dynamically by virtue of plasticity across the entire prefrontal cortex. To address functional properties and capacity for plasticity, we recorded from different prefrontal sub-regions and analyzed changes in responses following training in a spatial working memory task. This training induces more pronounced changes in anterior prefrontal regions, including increased firing rate during the delay period, selectivity, reliability, information for stimuli, representation of whether a test stimulus matched the remembered cue or not, and variability and correlation between neurons. Similar results are obtained for discrete subdivisions or when treating position along the anterior-posterior axis as a continuous variable. Our results reveal that anterior aspects of the lateral prefrontal cortex of non-human primates possess greater plasticity based on task demands. Studies of the functional organization of the prefrontal cortex have produced contradicting results depending on the task used. Here, Riley and colleagues demonstrate that prefrontal areas are specialized across the anterior posterior axis and that the effects of the task themselves impact more the anterior areas.
```
</details>

<details><summary>[9] **KEY** Testing burst coding models of working memory with spike trains from primate prefrontal cortex — Daming Li, Christos Contantidinis, J. Murray (2019); cutoff-filter date 2019-12-31; doi:10.32470/ccn.2019.1262-0</summary>

```text
[9] Testing burst coding models of working memory with spike trains from primate prefrontal cortex
    id: s2:5ddd5110a9050cb7760a0058c9e4b94df6b428fd
    date: 2019
    venue: 2019 Conference on Cognitive Computational Neuroscience
    authors: Daming Li, Christos Contantidinis, J. Murray
    abstract: Working memory (WM) requires the brain’s ability to convert a brief stimulus-driven signal into an internal representation that can then be maintained across a mnemonic delay of several seconds. In prefrontal cortex (PFC), a neuronal correlate of WM is stimulus-selective persistent activity during the delay. This hallmark persistent activity is typically measured by the elevated mean firing rate, averaged across trials for a stimulus condition, and therefore may obscure more complex patterns of spiking on individual trials. It was recently proposed that observed persistent activity in WM may be an artifact of trial averaging, and that WM is instead subserved by sparse intermittent bursts of neural activity (Lundqvist et al. (2016)). However, that study was done with local field potential (LFP) data, while the predictions of this alternative burst-coding WM proposal for single neuron spiking activity have not been characterized or tested. To investigate this debated issue, we applied the theory of stochastic processes and analysis of single-neuron recordings from PFC during WM tasks, focusing on measures of across-trial variability such as Fano factor (FF). We first mathematically formalized the burst-coding proposal through a doubly-stochastic inhomogeneous Poisson process model, in which the underlying firing rate transitions follow a two-level telegraph process (Figure 1). This model admits an analytical expression for the FF. We demonstrated that under the burstcoding model, as opposed to the persistent-activity model, elevated WM activity should exhibit an increase in FF. These conclusions are robust under the introduction of refractoriness. Based on these model predictions, we next tested the plausibility of the burst coding mechanism by analyzing spike train data of many single neurons in monkey PFC during two classic WM tasks used in primate electrophysiology: the oculomotor delayed response task (Constantinidis, Franowicz, and Goldman-Rakic (2001)) and the v [...]
```
</details>

<details><summary>[10] Increased action potential firing rates of layer 2/3 pyramidal cells in the prefrontal cortex are significantly related to cognitive performance in aged monkeys. — Yu-Ming Chang, D. Rosene, R. Killiany, L. Mangiamele et al. (2005); cutoff-filter date 2005-04-01; doi:10.1093/cercor/bhh144</summary>

```text
[10] Increased action potential firing rates of layer 2/3 pyramidal cells in the prefrontal cortex are significantly related to cognitive performance in aged monkeys.
    id: s2:5f28e49d76c51e7e710797cbc93bd287cbd0ca8e
    date: 2005-04-01
    venue: Cerebral Cortex
    authors: Yu-Ming Chang, D. Rosene, R. Killiany, L. Mangiamele, J. Luebke
    abstract: [no abstract available]
```
</details>

<details><summary>Post-hoc automated audit — NON-AUTHORITATIVE; uses hidden benchmark annotations</summary>

- primary auditor: `silence_as_null_error`; statuses {'H1': 'positive_or_present', 'H2': 'indeterminate'}; discriminative=False
- primary reasoning: H1 predicts that prefrontal cortex persistent activity encodes mnemonic content, so neural firing rates should reflect memorized features. H2, which posits PFC as a control locus rather than a storage substrate, does not commit to whether PFC firing rates encode specific mnemonic features; it is compatible with either possibility.
- derived opposition call: `manufactured_from_silence`
- evidence attribution: `informative_evidence_found` — The retrieved papers directly address the proposition, with multiple studies reporting stimulus-selective persistent firing rates in prefrontal cortex neurons during the delay period of visual working memory tasks. The assessor correctly identified and used this evidence, and the queries were appropriate for surfacing relevant literature. The process worked as intended.
- auditor retest: `silence_as_null_error`; discriminative=False
- disagreement flags: {'second_rater_vs_primary_discriminative': None, 'second_rater_vs_primary_status': None, 'retest_vs_primary_category': False, 'any': False}
</details>

**Human review** — `evidence_construct_mismatch` · reviewer: Research Director · source: D045 · status: `first_pass_model_based_review` · genuinely discriminative: False · silence-as-null error: False · other fields not recorded

---

## #25 · `GP1-glnbp_induced_fit_vs_conformational_selection-X6`

**GP1-glnbp_induced_fit_vs_conformational_selection-X6** — case `glnbp_induced_fit_vs_conformational_selection`, node `X6`

> Ligand binding to periplasmic binding proteins can select for pre-existing conformational states rather than induce new ones.

- generated from **H1** (Candidate B); abstraction: `class`
- generator's stated reason: If GlnBP, a periplasmic binding protein, uses a conformational selection mechanism, it increases the likelihood that other proteins in this class may also employ conformational selection.
- influence: **0.245** (rank 8 in case, 25 overall; cumulative 63%) — favours **H1**
- log-likelihood contribution: H2 +0.920, H1 +1.164
- removing it alone: evidence withheld → case log-odds +2.086 (ranking unchanged); node deleted → +1.604 (ranking unchanged)

**Hypotheses (as shown to the verifier)**

- **H1** (Candidate B): Apo-GlnBP samples a pre-existing binding-competent closed or semi-closed conformation; glutamine preferentially binds/captures that pre-existing conformation.
- **H2** (Candidate A): Glutamine binds to open/binding-competent GlnBP before the major protein conformational rearrangement, after which GlnBP closes around the ligand.

**Verifier cross-hypothesis judgments** — P(X|H) combines these by noisy-OR

| hypothesis | origin? | direct edge | route via parent | P(X\|H) |
| --- | --- | --- | --- | --- |
| H2 | no | `weakly_implied` | — | 0.650 |
| H1 | yes | `strongly_implied` | — | 0.950 |

- edge rationale, **H2** → node: Candidate A suggests that the ligand binds before a major conformational change, which is somewhat consistent with selection of a pre-existing state but does not explicitly state that the binding-competent conformation exists prior to ligand binding.
- edge rationale, **H1** → node: Candidate B directly states that the protein samples pre-existing conformations and that the ligand preferentially binds to one of these, which matches the proposition that ligand binding selects for pre-existing states.

**Verifier evidence** — label used in score: `support` (log-LR +1.2)

- queries: `periplasmic binding protein conformational states`; `ligand binding protein conformational selection`
- assessor rationale: Record [6] directly states that the periplasmic C4-dicarboxylate binding protein exists in equilibrium between different conformational states in the absence of ligand, and that ligand binding selects for the binding form (BP2), rather than inducing it de novo. This is direct evidence for the proposition that ligand binding can select for pre-existing conformational states. No other records directly address this mechanism.
- supporting spans cited by the assessor:
  - "In the absence of ligand, the protein is in equilibrium between an essentially nonbinding form, BP1, and the binding form, BP2. Ligands bind to the BP2 form, shifting the equilibrium toward the BP2-L conformation, and also inducing a further isomerization of the protein, to the BP3-L form."
- 10 papers shown; key papers: `s2:eed159a6397468593a7f59bff05e8ddfca83e770`
- _The evidence assessor returns ONE label for the node from all papers shown; the method has no per-paper contribution. Key papers and spans are those the assessor cited._

<details><summary>[1] Ligand-induced structural changes analysis of ribose-binding protein as studied by molecular dynamics simulations — Hai-Yan Li, Zanxia Cao, Guodong Hu, Li-Ling Zhao et al. (2021); cutoff-filter date 2021-03-02; doi:10.3233/thc-218011</summary>

```text
[1] Ligand-induced structural changes analysis of ribose-binding protein as studied by molecular dynamics simulations
    id: s2:b407302d7c1be527f2abbdc5b5075a4a215f7ec3
    date: 2021-01-01
    venue: Technology and Health Care
    authors: Hai-Yan Li, Zanxia Cao, Guodong Hu, Li-Ling Zhao, Chun-Ling Wang, Jihua Wang
    abstract: BACKGROUND: The ribose-binding protein (RBP) from Escherichia coli is one of the representative structures of periplasmic binding proteins. Binding of ribose at the cleft between two domains causes a conformational change corresponding to a closure of two domains around the ligand. The RBP has been crystallized in the open and closed conformations. OBJECTIVE: With the complex trajectory as a control, our goal was to study the conformation changes induced by the detachment of the ligand, and the results have been revealed from two computational tools, MD simulations and elastic network models. METHODS: Molecular dynamics (MD) simulations were performed to study the conformation changes of RBP starting from the open-apo, closed-holo and closed-apo conformations. RESULTS: The evolution of the domain opening angle θ clearly indicates large structural changes. The simulations indicate that the closed states in the absence of ribose are inclined to transition to the open states and that ribose-free RBP exists in a wide range of conformations. The first three dominant principal motions derived from the closed-apo trajectories, consisting of rotating, bending and twisting motions, account for the major rearrangement of the domains from the closed to the open conformation. CONCLUSIONS: The motions showed a strong one-to-one correspondence with the slowest modes from our previous study of RBP with the anisotropic network model (ANM). The results obtained for RBP contribute to the generalization of robustness for protein domain motion studies using either the ANM or PCA for trajectories obtained from MD.
```
</details>

<details><summary>[2] Structures of the Neisseria meningitides methionine‐binding protein MetQ in substrate‐free form and bound to l‐ and d‐methionine isomers — P. Nguyễn, J. Y. Lai, J. Kaiser, D. Rees (2019); cutoff-filter date 2019-07-26; doi:10.1002/pro.3694</summary>

```text
[2] Structures of the Neisseria meningitides methionine‐binding protein MetQ in substrate‐free form and bound to l‐ and d‐methionine isomers
    id: s2:c1acc5c3c623a87a4889c62efe25b0516575d4bb
    date: 2019-07-26
    venue: Protein Science
    authors: P. Nguyễn, J. Y. Lai, J. Kaiser, D. Rees
    abstract: The bacterial periplasmic methionine‐binding protein MetQ is involved in the import of methionine by the cognate MetNI methionine ATP binding cassette (ABC) transporter. The MetNIQ system is one of the few members of the ABC importer family that has been structurally characterized in multiple conformational states. Critical missing elements in the structural analysis of MetNIQ are the structure of the substrate‐free form of MetQ, and detailing how MetQ binds multiple methionine derivatives, including both l‐ and d‐methionine isomers. In this study, we report the structures of the Neisseria meningitides MetQ in substrate‐free form and in complexes with l‐methionine and with d‐methionine, along with the associated binding constants determined by isothermal titration calorimetry. Structures of the substrate‐free (N238A) and substrate‐bound N. meningitides MetQ are related by a “Venus‐fly trap” hinge‐type movement of the two domains accompanying methionine binding and dissociation. l‐ and d‐methionine bind to the same site on MetQ, and this study emphasizes the important role of asparagine 238 in ligand binding and affinity. A thermodynamic analysis demonstrates that ligand‐free MetQ associates with the ATP‐bound form of MetNI ∼40 times more tightly than does liganded MetQ, consistent with the necessity of dissociating methionine from MetQ for transport to occur.
```
</details>

<details><summary>[3] In Situ Conformational Changes of the Escherichia coli Serine Chemoreceptor in Different Signaling States — Wen Yang, C. K. Cassidy, P. Ames, C. Diebolder et al. (2019); cutoff-filter date 2019-07-02; doi:10.1128/mbio.00973-19</summary>

```text
[3] In Situ Conformational Changes of the Escherichia coli Serine Chemoreceptor in Different Signaling States
    id: s2:300135c7e88a38d044edba196fe97d0a1fdd832b
    date: 2019-07-02
    venue: mBio
    authors: Wen Yang, C. K. Cassidy, P. Ames, C. Diebolder, K. Schulten, Z. Luthey-Schulten, J. Parkinson, A. Briegel
    abstract: In Escherichia coli, membrane-bound chemoreceptors, the histidine kinase CheA, and coupling protein CheW form highly ordered chemosensory arrays. In core signaling complexes, chemoreceptor trimers of dimers undergo conformational changes, induced by ligand binding and sensory adaptation, which regulate kinase activation. Here, we characterize by cryo-electron tomography the kinase-ON and kinase-OFF conformations of the E. coli serine receptor in its native array context. We found distinctive structural differences between the members of a receptor trimer, which contact different partners in the signaling unit, and structural differences between the ON and OFF signaling complexes. Our results provide new insights into the signaling mechanism of chemoreceptor arrays and suggest an important functional role for a previously postulated flexible region and glycine hinge in the receptor molecule. ABSTRACT Tsr, the serine chemoreceptor in Escherichia coli, transduces signals from a periplasmic ligand-binding site to its cytoplasmic tip, where it controls the activity of the CheA kinase. To function, Tsr forms trimers of homodimers (TODs), which associate in vivo with the CheA kinase and CheW coupling protein. Together, these proteins assemble into extended hexagonal arrays. Here, we use cryo-electron tomography and molecular dynamics simulation to study Tsr in the context of a near-native array, characterizing its signaling-related conformational changes at both the individual dimer and the trimer level. In particular, we show that individual Tsr dimers within a trimer exhibit asymmetric flexibilities that are a function of the signaling state, highlighting the effect of their different protein interactions at the receptor tips. We further reveal that the dimer compactness of the Tsr trimer changes between signaling states, transitioning at the glycine hinge from a compact conformation in the kinase-OFF state to an expanded conformation in the kinase-ON state. Hence, our r [...]
```
</details>

<details><summary>[4] Structural Analysis of ABC-family Periplasmic Zinc Binding Protein Provides New Insights Into Mechanism of Ligand Uptake and Release — B. R. Chandra, M. Yogavel, Amit Sharma (2007); cutoff-filter date 2007-01-24; doi:10.1016/j.jmb.2007.01.041</summary>

```text
[4] Structural Analysis of ABC-family Periplasmic Zinc Binding Protein Provides New Insights Into Mechanism of Ligand Uptake and Release
    id: s2:6e0f562cb566a66bc1cac2bc0ce1dba19f31fbb4
    date: 2007-01-23
    venue: Journal of Molecular Biology
    authors: B. R. Chandra, M. Yogavel, Amit Sharma
    abstract: ATP-binding cassette superfamily of periplasmic metal transporters are known to be vital for maintaining ion homeostasis in several pathogenic and non-pathogenic bacteria. We have determined crystal structure of the high-affinity zinc transporter ZnuA from Escherichia coli at 1.8 Å resolution. This structure represents the first native (non-recombinant) protein structure of a periplasmic metal binding protein. ZnuA reveals numerous conformational features, which occur either in Zn2+ or in Mn2+ transporters, and presents a unique conformational state. A comprehensive comparison of ZnuA with other periplasmic ligand binding protein structures suggests vital mechanistic differences between bound and release states of metal transporters. The key new attributes in ZnuA include a C-domain disulfide bond, an extra α-helix proximal to the highly charged metal chelating mobile loop region, alternate conformations of secondary shell stabilizing residues at the metal binding site, and domain movements potentially controlled by salt bridges. Based on in-depth structural analyses of five metal binding transporters, we present here a mechanistic model termed as “partial domain slippage” for binding and release of Zn2+.
```
</details>

<details><summary>[5] Conformational changes of glucose/galactose‐binding protein illuminated by open, unliganded, and ultra‐high‐resolution ligand‐bound structures — M. Jack Borrok, L. Kiessling, K. Forest (2007); cutoff-filter date 2007-06-01; doi:10.1110/ps.062707807</summary>

```text
[5] Conformational changes of glucose/galactose‐binding protein illuminated by open, unliganded, and ultra‐high‐resolution ligand‐bound structures
    id: s2:6f7eebb5b63e76f292b41d0ca5ea561d97cb7500
    date: 2007-06-01
    venue: Protein Science
    authors: M. Jack Borrok, L. Kiessling, K. Forest
    abstract: [no abstract available]
```
</details>

<details><summary>[6] **KEY** The mechanism of ligand binding to the periplasmic C4-dicarboxylate binding protein (DctP) from Rhodobacter capsulatus. — A. Walmsley, Jonathan G. Shaw, David J. Kelly (1992); cutoff-filter date 1992-04-30; doi:10.1016/s0021-9258(18)42408-8</summary>

```text
[6] The mechanism of ligand binding to the periplasmic C4-dicarboxylate binding protein (DctP) from Rhodobacter capsulatus.
    id: s2:eed159a6397468593a7f59bff05e8ddfca83e770
    date: 1992-04-25
    venue: Journal of Biological Chemistry
    authors: A. Walmsley, Jonathan G. Shaw, David J. Kelly
    abstract: The kinetics of ligand binding to the periplasmic C4-dicarboxylate binding protein (DctP) from Rhodobacter capsulatus were investigated by exploiting the changes in the intrinsic fluorescence of the protein upon binding ligands. Steady state measurements have shown that L-malate, succinate, and fumarate are all bound with sub-micromolar Kd values, whereas D-malate is bound 2 orders of magnitude more weakly. Stopped-flow studies have revealed that the binding process involves at least three steps. In the absence of ligand, the protein is in equilibrium between an essentially nonbinding form, BP1, and the binding form, BP2. Ligands bind to the BP2 form, shifting the equilibrium toward the BP2-L conformation, and also inducing a further isomerization of the protein, to the BP3-L form. The kinetic properties of the four different conformational states of the DctP protein identified in this study would be consistent with their identification as the closed-conformation, the open-conformation, an open-liganded conformation, and a closed-liganded conformation. The latter three states have been identified by x-ray crystallographic studies of binding proteins, but no kinetic or structural data have been presented previously to support the possibility of a closed but unliganded conformation.
```
</details>

<details><summary>[7] Conformational changes of ribose-binding protein and two related repressors are tailored to fit the functional need. — Sherry L. Mowbray, A. Björkman (1999); cutoff-filter date 1999-11-30; doi:10.1006/jmbi.1999.3271</summary>

```text
[7] Conformational changes of ribose-binding protein and two related repressors are tailored to fit the functional need.
    id: s2:bf075ed133dd66c7f752ff13ee6174eabd9ab3cd
    date: 1999-11-26
    venue: Journal of Molecular Biology
    authors: Sherry L. Mowbray, A. Björkman
    abstract: [no abstract available]
```
</details>

<details><summary>[8] Calculation of Relative Binding Free Energy in the Water-Filled Active Site of Oligopeptide-Binding Protein A — M. Maurer, S. D. de Beer, C. Oostenbrink (2016); cutoff-filter date 2016-04-15; doi:10.3390/molecules21040499</summary>

```text
[8] Calculation of Relative Binding Free Energy in the Water-Filled Active Site of Oligopeptide-Binding Protein A
    id: s2:06d53fc175796c4abe54c812fc6e927e53d64baf
    date: 2016-04-15
    venue: Molecules
    authors: M. Maurer, S. D. de Beer, C. Oostenbrink
    abstract: The periplasmic oligopeptide binding protein A (OppA) represents a well-known example of water-mediated protein-ligand interactions. Here, we perform free-energy calculations for three different ligands binding to OppA, using a thermodynamic integration approach. The tripeptide ligands share a high structural similarity (all have the sequence KXK), but their experimentally-determined binding free energies differ remarkably. Thermodynamic cycles were constructed for the ligands, and simulations conducted in the bound and (freely solvated) unbound states. In the unbound state, it was observed that the difference in conformational freedom between alanine and glycine leads to a surprisingly slow convergence, despite their chemical similarity. This could be overcome by increasing the softness parameter during alchemical transformations. Discrepancies remained in the bound state however, when comparing independent simulations of the three ligands. These difficulties could be traced to a slow relaxation of the water network within the active site. Fluctuations in the number of water molecules residing in the binding cavity occur mostly on a timescale larger than the simulation time along the alchemical path. After extensive simulations, relative binding free energies that were converged to within thermal noise could be obtained, which agree well with available experimental data.
```
</details>

<details><summary>[9] Kinetics of transport systems dependent on periplasmic binding proteins. — R. M. Krupka (1992); cutoff-filter date 1992-09-30; doi:10.1016/0005-2736(92)90287-v</summary>

```text
[9] Kinetics of transport systems dependent on periplasmic binding proteins.
    id: s2:b117f3f1ffb785fba0a4cf797f10f0c2830fcc2c
    date: 1992-09-21
    venue: Biochimica et Biophysica Acta
    authors: R. M. Krupka
    abstract: [no abstract available]
    note: possibly the same work as s2:272fb167ec9b19c2f442ff9c0279343d933c4426
```
</details>

<details><summary>[10] Testing models for transport systems dependent on periplasmic binding proteins. — R. M. Krupka (1992); cutoff-filter date 1992-09-30; doi:10.1016/0005-2736(92)90288-w</summary>

```text
[10] Testing models for transport systems dependent on periplasmic binding proteins.
    id: s2:272fb167ec9b19c2f442ff9c0279343d933c4426
    date: 1992-09-21
    venue: Biochimica et Biophysica Acta
    authors: R. M. Krupka
    abstract: [no abstract available]
    note: possibly the same work as s2:b117f3f1ffb785fba0a4cf797f10f0c2830fcc2c
```
</details>

<details><summary>Post-hoc automated audit — NON-AUTHORITATIVE; uses hidden benchmark annotations</summary>

- primary auditor: `silence_as_null_error`; statuses {'H2': 'indeterminate', 'H1': 'positive_or_present'}; discriminative=False
- primary reasoning: H1 (conformational selection) implies that ligand binding can select for pre-existing conformational states, so the proposition is a direct consequence. H2 (induced fit) does not speak to what other periplasmic binding proteins do, nor does it require or preclude conformational selection in general, so it is indeterminate.
- derived opposition call: `silence_given_directional_label`
- evidence attribution: `informative_evidence_found` — The retrieved literature included a paper (record [6]) that directly addressed the proposition, providing evidence that ligand binding to a periplasmic binding protein can select for a pre-existing conformational state. The assessor correctly identified and used this evidence. The process worked as intended.
- disagreement flags: {'second_rater_vs_primary_discriminative': None, 'second_rater_vs_primary_status': None, 'retest_vs_primary_category': None, 'any': False}
</details>

**Human review** — `generic_component_fact` · reviewer: Research Director · source: D045 · status: `first_pass_model_based_review` · genuinely discriminative: False · silence-as-null error: False · other fields not recorded

---

## #26 · `GP1-pfc_storage_vs_control-X3`

**GP1-pfc_storage_vs_control-X3** — case `pfc_storage_vs_control`, node `X3`

> Disruption of persistent activity in lateral prefrontal cortex leads to degradation of working memory representations.

- generated from **H1** (Candidate A); abstraction: `class`
- generator's stated reason: If disrupting the relevant PFC population disrupts the stored representation, then this should generalize to the class of lateral prefrontal cortex regions involved in working memory.
- influence: **0.245** (rank 6 in case, 26 overall; cumulative 64%) — favours **H1**
- log-likelihood contribution: H1 +1.164, H2 +0.920
- removing it alone: evidence withheld → case log-odds +0.969 (ranking unchanged); node deleted → +1.070 (ranking unchanged)

**Hypotheses (as shown to the verifier)**

- **H1** (Candidate A): Prefrontal persistent activity is itself a substrate for working-memory storage; disrupting the relevant PFC population therefore disrupts the stored mnemonic representation.
- **H2** (Candidate B): PFC primarily controls, prioritizes, or allocates resources to working-memory representations maintained in sensory/posterior regions rather than directly storing the mnemonic content itself.

**Verifier cross-hypothesis judgments** — P(X|H) combines these by noisy-OR

| hypothesis | origin? | direct edge | route via parent | P(X\|H) |
| --- | --- | --- | --- | --- |
| H1 | yes | `strongly_implied` | — | 0.950 |
| H2 | no | `weakly_implied` | — | 0.650 |

- edge rationale, **H1** → node: If persistent activity in lateral prefrontal cortex is the substrate for working-memory storage, then disrupting it would almost certainly degrade working memory representations.
- edge rationale, **H2** → node: If PFC controls or allocates resources to working-memory representations stored elsewhere, disrupting its persistent activity might somewhat degrade those representations, but not as directly or necessarily as if it stored them itself.

**Verifier evidence** — label used in score: `support` (log-LR +1.2)

- queries: `lateral prefrontal cortex working memory`; `persistent activity working memory representations`
- assessor rationale: Record [2] directly reports that ketamine disrupts neuronal activity in the lateral prefrontal cortex, resulting in degraded working memory representations, as evidenced by decreased neuronal tuning and information about remembered locations. This matches the proposition that disruption of persistent activity in lateral prefrontal cortex leads to degradation of working memory representations. No other records directly address the causal relationship as stated.
- supporting spans cited by the assessor:
  - "Ketamine induced transient working memory deficits while sparing perceptual and motor skills. Working memory deficits were accompanied by decreased responses of fast spiking inhibitory interneurons and increased responses of broad spiking excitatory neurons in the lateral prefrontal cortex. This translated into a decrease in neuronal tuning and information encoded by neuronal populations about remembered locations. Our results demonstrate that ketamine differentially affects neuronal types in the neocortex; thus, it perturbs the excitation inhibition balance within prefrontal microcircuits and ultimately leads to selective working memory deficits."
- 10 papers shown; key papers: `s2:62550df868e0d543d778099ea3cbae0e351b9164`
- _The evidence assessor returns ONE label for the node from all papers shown; the method has no per-paper contribution. Key papers and spans are those the assessor cited._

<details><summary>[1] Neuronal properties of pyramidal cells in lateral prefrontal cortex of the aging rhesus monkey brain are associated with performance deficits on spatial working memory but not executive function — T. Moore, M. Medalla, Sara Ibañez, K. Wimmer et al. (2023); cutoff-filter date 2023-04-27; doi:10.1007/s11357-023-00798-2</summary>

```text
[1] Neuronal properties of pyramidal cells in lateral prefrontal cortex of the aging rhesus monkey brain are associated with performance deficits on spatial working memory but not executive function
    id: s2:7ec8c10f4684693b427cb70e278f6866f68fc764
    date: 2023-02-08
    venue: bioRxiv (preprint)
    authors: T. Moore, M. Medalla, Sara Ibañez, K. Wimmer, Chromewell A. Mojica, R. Killiany, M. Moss, J. Luebke
    abstract: [no abstract available]
```
</details>

<details><summary>[2] **KEY** Ketamine disrupts naturalistic coding of working memory in primate lateral prefrontal cortex networks — M. Roussy, R. Luna, Lyndon Duong, B. Corrigan et al. (2021); cutoff-filter date 2021-05-12; doi:10.1038/s41380-021-01082-5</summary>

```text
[2] Ketamine disrupts naturalistic coding of working memory in primate lateral prefrontal cortex networks
    id: s2:62550df868e0d543d778099ea3cbae0e351b9164
    date: 2021-05-12
    venue: Molecular Psychiatry
    authors: M. Roussy, R. Luna, Lyndon Duong, B. Corrigan, Roberto A. Gulli, Ramon Nogueira, R. Moreno-Bote, A. Sachs
    abstract: Ketamine is a dissociative anesthetic drug, which has more recently emerged as a rapid-acting antidepressant. When acutely administered at subanesthetic doses, ketamine causes cognitive deficits like those observed in patients with schizophrenia, including impaired working memory. Although these effects have been linked to ketamine’s action as an N-methyl-D-aspartate receptor antagonist, it is unclear how synaptic alterations translate into changes in brain microcircuit function that ultimately influence cognition. Here, we administered ketamine to rhesus monkeys during a spatial working memory task set in a naturalistic virtual environment. Ketamine induced transient working memory deficits while sparing perceptual and motor skills. Working memory deficits were accompanied by decreased responses of fast spiking inhibitory interneurons and increased responses of broad spiking excitatory neurons in the lateral prefrontal cortex. This translated into a decrease in neuronal tuning and information encoded by neuronal populations about remembered locations. Our results demonstrate that ketamine differentially affects neuronal types in the neocortex; thus, it perturbs the excitation inhibition balance within prefrontal microcircuits and ultimately leads to selective working memory deficits.
```
</details>

<details><summary>[3] Stable Working Memory and Perceptual Representations in Macaque Lateral Prefrontal Cortex during Naturalistic Vision — M. Roussy, B. Corrigan, R. Luna, Roberto A. Gulli et al. (2022); cutoff-filter date 2022-03-27; doi:10.1101/2022.03.24.485710</summary>

```text
[3] Stable Working Memory and Perceptual Representations in Macaque Lateral Prefrontal Cortex during Naturalistic Vision
    id: s2:785ccec056a4bbdc45ead2b21d84eb4e3754af6c
    date: 2022-03-27
    venue: Journal of Neuroscience (preprint)
    authors: M. Roussy, B. Corrigan, R. Luna, Roberto A. Gulli, A. Sachs, L. Palaniyappan, J. Martinez-Trujillo
    abstract: Primates use perceptual and mnemonic visuospatial representations to perform everyday functions. Neurons in the lateral prefrontal cortex (LPFC) have been shown to encode both of these representations during tasks where eye movements are strictly controlled and visual stimuli are reduced in complexity. This raises the question of whether perceptual and mnemonic representations encoded by LPFC neurons remain robust during naturalistic vision—in the presence of a rich visual scenery and during eye movements. Here we investigate this issue by training macaque monkeys to perform working memory and perception tasks in a visually complex virtual environment that requires navigation using a joystick and allows for free visual exploration of the scene. We recorded the activity of 3950 neurons in the LPFC (areas 8a and 9/46) of two male rhesus macaques using multielectrode arrays, and measured eye movements using video tracking. We found that navigation trajectories to target locations and eye movement behavior differed between the perception and working memory tasks, suggesting that animals used different behavioral strategies. Single neurons were tuned to target location during cue encoding and working memory delay, and neural ensemble activity was predictive of the behavior of the animals. Neural decoding of the target location was stable throughout the working memory delay epoch. However, neural representations of similar target locations differed between the working memory and perception tasks. These findings indicate that during naturalistic vision, LPFC neurons maintain robust and distinct neural codes for mnemonic and perceptual visuospatial representations. SIGNIFICANCE STATEMENT We show that lateral prefrontal cortex neurons encode working memory and perceptual representations during a naturalistic task set in a virtual environment. We show that despite eye movement and complex visual input, neurons maintain robust working memory representations of space, which are [...]
```
</details>

<details><summary>[4] Minimally dependent activity subspaces for working memory and motor preparation in the lateral prefrontal cortex — Cheng Tang, R. Herikstad, Aishwarya Parthasarathy, C. Libedinsky et al. (2020); cutoff-filter date 2020-09-09; doi:10.7554/elife.58154</summary>

```text
[4] Minimally dependent activity subspaces for working memory and motor preparation in the lateral prefrontal cortex
    id: s2:fe9cfbae06e4ee67db4b2fad220b9c63a1326c12
    date: 2020-09-09
    venue: eLife
    authors: Cheng Tang, R. Herikstad, Aishwarya Parthasarathy, C. Libedinsky, S. Yen
    abstract: The lateral prefrontal cortex is involved in the integration of multiple types of information, including working memory and motor preparation. However, it is not known how downstream regions can extract one type of information without interference from the others present in the network. Here, we show that the lateral prefrontal cortex of non-human primates contains two minimally dependent low-dimensional subspaces: one that encodes working memory information, and another that encodes motor preparation information. These subspaces capture all the information about the target in the delay periods, and the information in both subspaces is reduced in error trials. A single population of neurons with mixed selectivity forms both subspaces, but the information is kept largely independent from each other. A bump attractor model with divisive normalization replicates the properties of the neural data. These results provide new insights into neural processing in prefrontal regions.
    note: merged with 1 other version(s) of the same work
```
</details>

<details><summary>[5] Time-invariant working memory representations in the presence of code-morphing in the lateral prefrontal cortex — Aishwarya Parthasarathy, Cheng Tang, R. Herikstad, L. Cheong et al. (2019); cutoff-filter date 2019-11-01; doi:10.1038/s41467-019-12841-y</summary>

```text
[5] Time-invariant working memory representations in the presence of code-morphing in the lateral prefrontal cortex
    id: s2:79966af72116d4f476cae0d39ab18823a420a72f
    date: 2019-02-28
    venue: Nature Communications
    authors: Aishwarya Parthasarathy, Cheng Tang, R. Herikstad, L. Cheong, S. Yen, C. Libedinsky
    abstract: Maintenance of working memory is thought to involve the activity of prefrontal neuronal populations with strong recurrent connections. However, it was recently shown that distractors evoke a morphing of the prefrontal population code, even when memories are maintained throughout the delay. How can a morphing code maintain time-invariant memory information? We hypothesized that dynamic prefrontal activity contains time-invariant memory information within a subspace of neural activity. Using an optimization algorithm, we found a low-dimensional subspace that contains time-invariant memory information. This information was reduced in trials where the animals made errors in the task, and was also found in periods of the trial not used to find the subspace. A bump attractor model replicated these properties, and provided predictions that were confirmed in the neural data. Our results suggest that the high-dimensional responses of prefrontal cortex contain subspaces where different types of information can be simultaneously encoded with minimal interference. Working memory is maintained in the recurrent connectivity of prefrontal neurons; however, distractors lead to a morphing of the population code. Here, the authors show that a low dimensional subspace of activity maintains memory information even with a distractor and can be modeled as a bump attractor.
```
</details>

<details><summary>[6] Small neuronal ensembles of primate lateral prefrontal cortex encode spatial working memory in two reference frames — R. Luna, M. Roussy, B. Corrigan, A. Sachs et al. (2021); cutoff-filter date 2021-09-27; doi:10.1167/jov.21.9.2858</summary>

```text
[6] Small neuronal ensembles of primate lateral prefrontal cortex encode spatial working memory in two reference frames
    id: s2:ce3144b4492b7f0d5056bfcee0f7214fbc3ccd86
    date: 2021-09-27
    venue: Journal of Vision
    authors: R. Luna, M. Roussy, B. Corrigan, A. Sachs, S. Treue, J. Martinez-Trujillo
    abstract: [no abstract available]
    note: possibly the same work as s2:db8e777535e54e689b30b5f050e7fd915f35cd69
```
</details>

<details><summary>[7] Sulcal Depth in Lateral Prefrontal Cortex Predicts Working Memory in Childhood — Jewelia K. Yao, Willa Voorhies, Jacob A. Miller, S. Bunge et al. (2020); cutoff-filter date 2020-04-18; doi:10.1096/fasebj.2020.34.s1.04640</summary>

```text
[7] Sulcal Depth in Lateral Prefrontal Cortex Predicts Working Memory in Childhood
    id: s2:f6efafd0accf623449c7241ecd8f8e7cde5297a7
    date: 2020-04-01
    venue: The FASEB Journal
    authors: Jewelia K. Yao, Willa Voorhies, Jacob A. Miller, S. Bunge, K. Weiner
    abstract: Sulci, the indentations in the brain, develop over childhood (Zilles et al., 1988; Alemán‐Gómez et al., 2013), and demonstrate individual differences linked to cognition (Cachia et al., 2018; Im et al., 2011). Previous neuroimaging work implicates prefrontal cortex (PFC) in working memory, a key facet of cognition. In particular, maintaining items in working memory (e.g., keeping a series of digits in mind) engages ventrolateral prefrontal cortex (VLPFC), whereas maintaining items in working memory (e.g., reversing a series of digits) engages both VLPFC and dorsolateral prefrontal cortex (DLPFC; Crone et. al, 2006). We propose to examine the relationship between sulcal depth in these regions and working memory for two tasks: Digit Span Forwards, which taxes maintenance, and Digit Span Backwards, which taxes manipulation and maintenance. Sulcal morphology of the PFC has been classically proposed to be functionally relevant to cognition that engages this region (Sanides, 1964). Thus, we hypothesized that there would be a relationship between sulcal depth and behavioral performance, whereby greater sulcal depth would predict better working memory. Cortical morphometric analyses were performed on high resolution T1‐weighted MPRAGE anatomical scans in 60 participants ages 6–18, from a previously published dataset (Wendelken et al., 2017). Cortical surface reconstructions were generated using Freesurfer. Sulci in lateral PFC were manually defined based on recently proposed definitions (Petrides & Pandya, 2012; Petrides, 2019), resulting in 2,157 labels (~18 labels per hemisphere, per subject). Mean sulcal depth was extracted for each sulcus. Relevant sulci for task performance were determined using a least absolute shrinkage and selection operator (LASSO) regression, fit separately for each hemisphere with each task condition using leave‐one‐out cross‐validation. Our analysis approach revealed four main findings. First, there is a relationship between PFC sulcal depth and [...]
```
</details>

<details><summary>[8] Neuronal ensembles of primate Lateral Prefrontal Cortex encode spatial working memory in different frames of reference — Rogelio Luna Almeida, M. Roussy, A. Sachs, S. Treue et al. (2020); cutoff-filter date 2020-10-20; doi:10.1167/jov.20.11.1753</summary>

```text
[8] Neuronal ensembles of primate Lateral Prefrontal Cortex encode spatial working memory in different frames of reference
    id: s2:db8e777535e54e689b30b5f050e7fd915f35cd69
    date: 2020-10-20
    venue: Journal of Vision
    authors: Rogelio Luna Almeida, M. Roussy, A. Sachs, S. Treue, J. Martinez-Trujillo
    abstract: [no abstract available]
    note: possibly the same work as s2:ce3144b4492b7f0d5056bfcee0f7214fbc3ccd86
```
</details>

<details><summary>[9] Reference Frames for Spatial Working Memory in the Lateral Prefrontal Cortex of primates — R. Luna, M. Roussy, S. Treue, J. Martinez-Trujillo (2019); cutoff-filter date 2019-09-06; doi:10.1167/19.10.206</summary>

```text
[9] Reference Frames for Spatial Working Memory in the Lateral Prefrontal Cortex of primates
    id: s2:434265b64f694dbb46a6494298823f6fb9825f85
    date: 2019-09-06
    venue: Journal of Vision
    authors: R. Luna, M. Roussy, S. Treue, J. Martinez-Trujillo
    abstract: [no abstract available]
```
</details>

<details><summary>[10] Resting-State Anticorrelations Between Medial and Lateral Prefrontal Cortex: Association with Working Memory, Aging, and Individual Differences — Joseph B. Keller, T. Hedden, Todd W. Thompson, S. Anteraper et al. (2014); cutoff-filter date 2014-12-13; doi:10.1016/j.cortex.2014.12.001</summary>

```text
[10] Resting-State Anticorrelations Between Medial and Lateral Prefrontal Cortex: Association with Working Memory, Aging, and Individual Differences
    id: s2:1ed0d088c91e14f2c7bf71a74db33837fbcfb3ad
    date: 2014-12-01
    venue: Cortex; a journal devoted to the study of the nervous system and behavior
    authors: Joseph B. Keller, T. Hedden, Todd W. Thompson, S. Anteraper, J. Gabrieli, S. Whitfield-Gabrieli
    abstract: We examined how variation in working memory (WM) capacity due to aging or individual differences among young adults is associated with intrinsic or resting-state anticorrelations, particularly between (1) the medial prefrontal cortex (MPFC), a component of the default-mode network (DMN) that typically decreases in activation during external, attention-demanding tasks, and (2) the dorsolateral prefrontal cortex (DLPFC), a component of the fronto-parietal control network that supports executive functions and WM and typically increases in activation during attention-demanding tasks. We compared the magnitudes of MPFC-DLPFC anticorrelations between healthy younger and older participants (Experiment 1) and related the magnitudes of these anticorrelations to individual differences on two behavioral measures of working memory capacity in two independent groups of young adults (Experiments 1 and 2). Relative to younger adults, older adults exhibited reductions in working memory capacity and in MPFC-DLPFC anticorrelations. Within younger adults, greater MPFC-DLPFC anticorrelation at rest correlated with greater working memory capacity. These findings show that variation in MPFC-DLPFC anticorrelations, whether related to aging or to individual differences, may reflect an intrinsic functional brain architecture supportive of working memory capacity.
```
</details>

<details><summary>Post-hoc automated audit — NON-AUTHORITATIVE; uses hidden benchmark annotations</summary>

- primary auditor: `silence_as_null_error`; statuses {'H1': 'positive_or_present', 'H2': 'indeterminate'}; discriminative=False
- primary reasoning: H1 predicts that disrupting persistent activity in lateral prefrontal cortex should degrade working memory representations, as it is posited to be the storage substrate. H2, which posits PFC as a control locus rather than a storage substrate, does not make a specific prediction about whether disruption would degrade memory representations; it is silent on this point.
- derived opposition call: `silence_given_directional_label`
- evidence attribution: `informative_evidence_found` — The retrieval system surfaced a paper (record [2]) that directly addresses the proposition, showing that disruption of persistent activity in the lateral prefrontal cortex (via ketamine) leads to degraded working memory representations. The assessor correctly identified and used this evidence. The process worked as intended.
- auditor retest: `silence_as_null_error`; discriminative=False
- disagreement flags: {'second_rater_vs_primary_discriminative': None, 'second_rater_vs_primary_status': None, 'retest_vs_primary_category': False, 'any': False}
</details>

**Human review** — `compatible_non_discriminative` · reviewer: Research Director · source: D045 · status: `first_pass_model_based_review` · genuinely discriminative: False · silence-as-null error: False · other fields not recorded

---

## #27 · `GP1-eukaryogenesis_mito_timing-X2`

**GP1-eukaryogenesis_mito_timing-X2** — case `eukaryogenesis_mito_timing`, node `X2`

> Acquisition of an energy-generating endosymbiont enables the evolution of increased cellular complexity in the host.

- generated from **H1** (Candidate A); abstraction: `mechanistic`
- generator's stated reason: The claim asserts that mitochondrial acquisition provided the energetic foundation necessary for subsequent elaboration of complex cellular systems.
- influence: **0.240** (rank 5 in case, 27 overall; cumulative 65%) — favours **H1**
- log-likelihood contribution: H1 +0.418, H2 +0.178
- removing it alone: evidence withheld → case log-odds -2.662 (ranking unchanged); node deleted → -2.374 (ranking unchanged)

**Hypotheses (as shown to the verifier)**

- **H1** (Candidate A): Mitochondrial acquisition was an initiating/foundational event that preceded or enabled much of later eukaryotic cellular complexity; major eukaryote-specific cellular systems should therefore largely elaborate after mitochondrial acquisition.
- **H2** (Candidate B): Substantial eukaryotic cellular machinery - including cytoskeletal, membrane-remodelling/trafficking, endomembrane, phagocytic, and nuclear-associated complexity - evolved before mitochondrial acquisition in an already complex archaeal host.

**Verifier cross-hypothesis judgments** — P(X|H) combines these by noisy-OR

| hypothesis | origin? | direct edge | route via parent | P(X\|H) |
| --- | --- | --- | --- | --- |
| H1 | yes | `implied` | — | 0.800 |
| H2 | no | `unlikely` | — | 0.300 |

- edge rationale, **H1** → node: If mitochondrial acquisition enabled later eukaryotic complexity, it is clearly expected that acquiring an energy-generating endosymbiont allows increased cellular complexity in the host.
- edge rationale, **H2** → node: If substantial cellular complexity evolved before mitochondrial acquisition, then acquiring an energy-generating endosymbiont is not expected to enable increased complexity and may even be less likely to do so.

**Verifier evidence** — label used in score: `weak_support` (log-LR +0.5)

- queries: `endosymbiont cellular complexity`; `energy-generating endosymbiont host evolution`
- assessor rationale: Record [2] explicitly argues that the acquisition of a proto-mitochondrial endosymbiont removed limitations on cellular complexity in the host, and links endosymbiont energy generation to increased complexity. Record [4] states that endosymbiosis was a key factor in the evolution of eukaryotic cellular complexity, which is consistent with the proposition but does not specify the energy-generating aspect. Both records directly address the relationship between endosymbiont acquisition and increased cellular complexity, though only one mentions energy generation. The evidence is therefore weak but direct.
- supporting spans cited by the assessor:
  - "Eukaryotic cells are characterized by a considerable increase in subcellular compartmentalization when compared to prokaryotes. Most evidence suggests that the earliest eukaryotes consisted of mitochondria derived from an α-proteobacterial ancestor enclosed within an archaeal host cell. However, what benefits the archaeal host and the proto-mitochondrial endosymbiont might have obtained at the beginning of this endosymbiotic relationship remains unclear. In this work, I argue that heat generated by the proto-mitochondrion initially permitted an archaeon living at high temperatures to colonize a cooler environment, thereby removing apparent limitations on cellular complexity. Furthermore, heat generation by the endosymbiont would have provided phenotypic flexibility not available through fixed alleles selected for fitness at specific temperatures. Finally, a role for heat production by the proto-mitochondrion bridges a conceptual gap between initial endosymbiont entry to the archaeal host and a later role for mitochondrial ATP production in permitting increased cellular complexity."
  - "Endosymbiosis was a key factor in the evolution of eukaryotic cellular complexity."
- 10 papers shown; key papers: `s2:0c1df5318536d6f6bf7678e581dfd7dc8a72ce60`, `s2:e087083291c2c7b6a9771e2370c9709a06375292`
- _The evidence assessor returns ONE label for the node from all papers shown; the method has no per-paper contribution. Key papers and spans are those the assessor cited._

<details><summary>[1] Asgard archaea illuminate the origin of eukaryotic cellular complexity — Katarzyna Zaremba-Niedźwiedzka, Eva F. Caceres, Jimmy H. W. Saw, Disa Bäckström et al. (2017); cutoff-filter date 2017-01-11; doi:10.1038/nature21031</summary>

```text
[1] Asgard archaea illuminate the origin of eukaryotic cellular complexity
    id: s2:2800ff203b3ac5ee457d9ab5acf432dd87c8fe93
    date: 2017-01-11
    venue: Nature
    authors: Katarzyna Zaremba-Niedźwiedzka, Eva F. Caceres, Jimmy H. W. Saw, Disa Bäckström, L. Juzokaite, Emmelien Vancaester, K. Seitz, Karthik Anantharaman
    abstract: [no abstract available]
```
</details>

<details><summary>[2] **KEY** Some Liked It Hot: A Hypothesis Regarding Establishment of the Proto-Mitochondrial Endosymbiont During Eukaryogenesis — Cory D. Dunn (2017); cutoff-filter date 2017-09-15; doi:10.1007/s00239-017-9809-5</summary>

```text
[2] Some Liked It Hot: A Hypothesis Regarding Establishment of the Proto-Mitochondrial Endosymbiont During Eukaryogenesis
    id: s2:0c1df5318536d6f6bf7678e581dfd7dc8a72ce60
    date: 2017-07-14
    venue: Journal of Molecular Evolution
    authors: Cory D. Dunn
    abstract: Eukaryotic cells are characterized by a considerable increase in subcellular compartmentalization when compared to prokaryotes. Most evidence suggests that the earliest eukaryotes consisted of mitochondria derived from an α-proteobacterial ancestor enclosed within an archaeal host cell. However, what benefits the archaeal host and the proto-mitochondrial endosymbiont might have obtained at the beginning of this endosymbiotic relationship remains unclear. In this work, I argue that heat generated by the proto-mitochondrion initially permitted an archaeon living at high temperatures to colonize a cooler environment, thereby removing apparent limitations on cellular complexity. Furthermore, heat generation by the endosymbiont would have provided phenotypic flexibility not available through fixed alleles selected for fitness at specific temperatures. Finally, a role for heat production by the proto-mitochondrion bridges a conceptual gap between initial endosymbiont entry to the archaeal host and a later role for mitochondrial ATP production in permitting increased cellular complexity.
```
</details>

<details><summary>[3] Endosymbiosis and Eukaryotic Cell Evolution. — J. Archibald (2015); cutoff-filter date 2015-10-05; doi:10.1016/j.cub.2015.07.055</summary>

```text
[3] Endosymbiosis and Eukaryotic Cell Evolution.
    id: s2:04cc476ca8429f3c792d6bfada89d660dc44f6ff
    date: 2015-10-05
    venue: Current Biology
    authors: J. Archibald
    abstract: [no abstract available]
```
</details>

<details><summary>[4] **KEY** Immune-like glycan-sensing and horizontally-acquired glycan-processing orchestrate host control in a microbial endosymbiosis — Benjamin H. Jenkins, Estelle S. Kilias, Fiona R. Savory, Megan E. S. Sørensen et al. (2024); cutoff-filter date 2024-10-24; doi:10.1101/2024.09.14.613017</summary>

```text
[4] Immune-like glycan-sensing and horizontally-acquired glycan-processing orchestrate host control in a microbial endosymbiosis
    id: s2:e087083291c2c7b6a9771e2370c9709a06375292
    date: 2024-10-24
    venue: bioRxiv (preprint)
    authors: Benjamin H. Jenkins, Estelle S. Kilias, Fiona R. Savory, Megan E. S. Sørensen, Camille Poirier, V. Attah, G. C. Drew, L. J. Galindo
    abstract: Endosymbiosis was a key factor in the evolution of eukaryotic cellular complexity. Yet the mechanisms that allow host regulation of intracellular symbionts, a pre-requisite for stable endosymbiosis and subsequent organelle evolution, are largely unknown. Here, we describe an immune-like glycan-sensing/processing network, partly assembled through horizontal gene-transfers (HGTs), that enables Paramecium bursaria to control its algal endosymbionts. Using phylogenetics, RNA-interference (RNAi), and metabolite exposure experiments, we show that P. bursaria regulates endosymbiont destruction using glycan-sensing/processing – a system that includes a eukaryotic-wide chitin-binding chitinase-like protein (CLP) localized to the host phago-lysosome. RNAi of CLP alters expression of eight glycan-processing genes, including two prokaryote-derived HGTs, during endosymbiont destruction. Furthermore, glycan-sensing/processing dynamically regulates endosymbiont number in P. bursaria, plasticity crucial to maximize host fitness across ecological conditions. CLP is homologous to a human phagocyte-associated innate immune factor, revealing how immune functions can be alternatively adapted and expanded, partly through HGT, enabling endosymbiotic control. Graphical Abstract
```
</details>

<details><summary>[5] The reducible complexity of a mitochondrial molecular machine — Abigail Clements, D. Bursać, X. Gatsos, A. Perry et al. (2009); cutoff-filter date 2009-09-15; doi:10.1073/pnas.0908264106</summary>

```text
[5] The reducible complexity of a mitochondrial molecular machine
    id: s2:e2717373c9eb30a77ec7e0716a2a82bf8cb7baa2
    date: 2009-09-15
    venue: Proceedings of the National Academy of Sciences of the United States of America
    authors: Abigail Clements, D. Bursać, X. Gatsos, A. Perry, Srgjan Civciristov, N. Celik, V. Likic, S. Poggio
    abstract: [no abstract available]
```
</details>

<details><summary>[6] The Role of Small Extracellular Vesicles in Viral-Protozoan Symbiosis: Lessons From Trichomonasvirus in an Isogenic Host Parasite Model — Yashini Govender, Tiffany Chan, H. Yamamoto, B. Budnik et al. (2020); cutoff-filter date 2020-11-05; doi:10.3389/fcimb.2020.591172</summary>

```text
[6] The Role of Small Extracellular Vesicles in Viral-Protozoan Symbiosis: Lessons From Trichomonasvirus in an Isogenic Host Parasite Model
    id: s2:5de045a0a32d6d1c467e11cbb0dc4236f4ffe22d
    date: 2020-11-05
    venue: Frontiers in Cellular and Infection Microbiology
    authors: Yashini Govender, Tiffany Chan, H. Yamamoto, B. Budnik, R. Fichorova
    abstract: The protozoan parasite Trichomonas vaginalis (TV), exclusively adapted to the human genital tract, is one of the most common sexually transmitted pathogens. Adding to the complexity of the host-pathogen interactions, the parasite harbors TV-specific endosymbiont viruses (Trichomonasvirus, TVV). It was reported that small extracellular vesicles (sEVs) released by TV play a role in host immunity; however, the role of the viral endosymbiosis in this process remained unknown. We hypothesized that the virus may offer evolutionary benefit to its protozoan host at least in part by altering the immunomodulatory properties of sEVs spreading from the site of infection to non-infected immune effector cells. We infected human vaginal epithelial cells, the natural host of the parasite, with TV natively harboring TVV and an isogenic derivative of the parasite cured from the viral infection. sEVs were isolated from vaginal cell culture 24 h post TV infection and from medium where the isogenic TV strains were cultured in the absence of the human host. sEVs from TVV-negative but not TVV-positive parasites cultured alone caused NF-κB activation and increase of IL-8 and RANTES expression by uterine endocervical cells, which provide innate immune defense at the gate to the upper reproductive tract. Similarly, mononuclear leukocytes increased their IL-8, IL-6 and TNF-α output in response to sEVs from virus-negative, but not isogenic virus-positive parasites, the latter exosomes being immunosuppressive in comparison to TV medium control. The same phenomenon of suppressed immunity induced by the TVV-positive compared to TVV-negative phenotype was seen when stimulating the leukocytes with sEVs originating from infected vaginal cultures. In addition, the sEVs from the TVV-positive infection phenotype suppressed immune signaling of a toll-like receptor ligand derived from mycoplasma, another frequent TV symbiont. Quantitative comparative proteome analysis of the secreted sEVs from virus-posi [...]
```
</details>

<details><summary>[7] Eukarya the chimera: eukaryotes, a secondary innovation of the two domains of life? — Stephanie-Jane Nobs, Fraser I. MacLeod, Hon-Lun Wong, B. P. Burns (2021); cutoff-filter date 2021-12-01; doi:10.1016/j.tim.2021.11.003</summary>

```text
[7] Eukarya the chimera: eukaryotes, a secondary innovation of the two domains of life?
    id: s2:b998914a68c1015d58b6804fcf962837b08578e2
    date: 2021-12-01
    venue: Trends in Microbiology
    authors: Stephanie-Jane Nobs, Fraser I. MacLeod, Hon-Lun Wong, B. P. Burns
    abstract: One of the most significant events in the evolution of life is the origin of the eukaryotic cell, an increase in cellular complexity that occurred approximately 2 billion years ago. Ground-breaking research has centered around unraveling the characteristics of the Last Eukaryotic Common Ancestor (LECA) and the nuanced archaeal and bacterial contributions in eukaryogenesis, resulting in fundamental changes in our understanding of the Tree of Life. The archaeal and bacterial roles are covered by theories of endosymbiogenesis wherein an ancestral host archaeon and a bacterial endosymbiont merged to create a new complex cell type - Eukarya - and its mitochondrion. Eukarya is often regarded as a unique and distinct domain due to complex innovations not found in archaea or bacteria, despite housing a chimeric genome containing genes of both archaeal and bacterial origin. However, the discovery of complex cell machineries in recently described Asgard archaeal lineages, and the growing support for diverse bacterial gene transfers prior to and during the time of LECA, is redefining our understanding of eukaryogenesis. Indeed, the uniqueness of Eukarya, as a domain, is challenged. It is likely that many microbial syntrophies, encompassing a 'microbial village', were required to 'raise' a eukaryote during the process of eukaryogenesis.
```
</details>

<details><summary>[8] Emergent RNA–RNA interactions can promote stability in a facultative phototrophic endosymbiosis — Benjamin H. Jenkins, F. Maguire, G. Leonard, Joshua D. Eaton et al. (2021); cutoff-filter date 2021-09-14; doi:10.1073/pnas.2108874118</summary>

```text
[8] Emergent RNA–RNA interactions can promote stability in a facultative phototrophic endosymbiosis
    id: s2:265422f97aa3b2c0de5e6c6c23f4234a3b25c2be
    date: 2021-09-14
    venue: Proceedings of the National Academy of Sciences of the United States of America
    authors: Benjamin H. Jenkins, F. Maguire, G. Leonard, Joshua D. Eaton, Steven West, B. Housden, David S. Milner, T. Richards
    abstract: Significance Stable endosymbiosis between eukaryotic microbes has driven the evolution of further cellular complexity. Yet the mechanisms that can act to stabilize an emergent eukaryote–eukaryote endosymbiosis are unclear. Using the model facultative endosymbiotic system, Paramecium bursaria, we demonstrate that endosymbiont–host RNA–RNA interactions can drive a cost to host growth upon endosymbiont digestion. These RNA–RNA interactions are facilitated by the host RNA-interference system. For endosymbiont messenger RNA sharing a high level of sequence identity with host transcripts, this process can result in host gene knockdown. We propose that these endosymbiont–host RNA–RNA interactions—“RNA-interference collisions”—represent an emergent mechanism to sanction the host for breakdown of the endosymbiosis, promoting the stability of the facultative endosymbiotic interaction. Eukaryote–eukaryote endosymbiosis was responsible for the spread of chloroplast (plastid) organelles. Stability is required for the metabolic and genetic integration that drives the establishment of new organelles, yet the mechanisms that act to stabilize emergent endosymbioses—between two fundamentally selfish biological organisms—are unclear. Theory suggests that enforcement mechanisms, which punish misbehavior, may act to stabilize such interactions by resolving conflict. However, how such mechanisms can emerge in a facultative endosymbiosis has yet to be explored. Here, we propose that endosymbiont–host RNA–RNA interactions, arising from digestion of the endosymbiont population, can result in a cost to host growth for breakdown of the endosymbiosis. Using the model facultative endosymbiosis between Paramecium bursaria and Chlorella spp., we demonstrate that this mechanism is dependent on the host RNA-interference (RNAi) system. We reveal through small RNA (sRNA) sequencing that endosymbiont-derived messenger RNA (mRNA) released upon endosymbiont digestion can be processed by the host RNAi sy [...]
```
</details>

<details><summary>[9] Chromerids and Their Plastids — Z. Füssy, M. Oborník (2017); cutoff-filter date 2017-12-31; doi:10.1016/bs.abr.2017.07.001</summary>

```text
[9] Chromerids and Their Plastids
    id: s2:90e5f454be6706cadf312ee5c2601b44db751762
    date: 2017
    venue: unknown
    authors: Z. Füssy, M. Oborník
    abstract: [no abstract available]
```
</details>

<details><summary>[10] Nitric Oxide Regulation of Mitochondrial Processes: Commonality in Medical Disorders. — G. Stefano, R. Kream (2015); cutoff-filter date 2015-07-16; doi:10.12659/aot.894289</summary>

```text
[10] Nitric Oxide Regulation of Mitochondrial Processes: Commonality in Medical Disorders.
    id: s2:f98440100d277166aeb44462de2e52860a11772b
    date: 2015-07-16
    venue: Annals of Transplantation
    authors: G. Stefano, R. Kream
    abstract: The vital status of diverse classes of eukaryotic mitochondria is reflected by the high degree of evolutionary modification functionally linked to ongoing multifaceted organelle development. From this teleological perspective, a logistical enhancement of eukaryotic cellular energy requirements indicates a convergence of metabolic processes within the mitochondrial matrix for optimal synthesis of ATP from ADP and inorganic phosphate and necessitates an evolutionarily driven retrofit of the primordial endosymbiont bacterial plasma membrane into the inner mitochondrial membrane. The biochemical complexity of eukaryotic inner membrane electron transport complexes linked to temporally-defined, state-dependent, fluctuations in mitochondrial oxygen utilization is capable of generating deleterious reactive oxygen species. Within this functional context, an extensive neurochemical literature supports the role of the free radical gas nitric oxide (NO) as a key signaling molecule involved in the regulation of multiple aspects of mitochondrial respiration/oxidative phosphorylation. Importantly, the unique chemical properties of NO underlie its rapid metabolism in vivo within a mechanistic spectrum of small oxidative molecules, free and protein-bound thiol adducts, and reversible binding to ferrous heme iron centers. Recent compelling work has identified a medically relevant dual regulation pathway for mitochondrial NO expression mediated by traditionally characterized NO synthases (NOS) and by enzymatic reduction of available cellular nitrite pools by a diverse class of cytosolic and mitochondrial nitrite reductases. Accordingly, our short review presents selected medically-based discussion topics relating to multi-faceted NO regulation of mitochondrial functions in human health and disease states.
```
</details>

<details><summary>Post-hoc automated audit — NON-AUTHORITATIVE; uses hidden benchmark annotations</summary>

- primary auditor: `silence_as_null_error`; statuses {'H1': 'positive_or_present', 'H2': 'indeterminate'}; discriminative=False
- primary reasoning: H1 explicitly predicts that mitochondrial acquisition enabled subsequent cellular complexity, so the proposition is positive under H1. H2 does not speak to whether mitochondrial acquisition enabled complexity; it posits complexity arose before mitochondria, so it is indeterminate regarding this proposition.
- derived opposition call: `manufactured_from_silence`
- evidence attribution: `informative_evidence_found` — The retrieved papers directly address the relationship between acquisition of an energy-generating endosymbiont and increased cellular complexity in the host, with at least one paper explicitly linking energy generation to complexity. The assessor correctly identified weak but direct support for the proposition from the literature. The process worked as intended.
- second rater (LLM, blind): statuses {'H1': 'positive_or_present', 'H2': 'indeterminate'}; discriminative=False (None confidence) — H2 does not deny mito enabled further complexity
- disagreement flags: {'second_rater_vs_primary_discriminative': False, 'second_rater_vs_primary_status': False, 'retest_vs_primary_category': None, 'any': False}
</details>

**Human review** — `silence_as_null_error` · reviewer: Research Director · source: D045 · status: `first_pass_model_based_review` · genuinely discriminative: False · silence-as-null error: True · other fields not recorded

---

## #28 · `GP1-eukaryogenesis_mito_timing-X10`

**GP1-eukaryogenesis_mito_timing-X10** — case `eukaryogenesis_mito_timing`, node `X10`

> Genes encoding actin and tubulin homologs are present in genomes of Asgard archaeal lineages closely related to eukaryotes.

- generated from **H2** (Candidate B); abstraction: `specific`
- influence: **0.239** (rank 6 in case, 28 overall; cumulative 67%) — favours **H2**
- log-likelihood contribution: H1 +1.715, H2 +1.954
- removing it alone: evidence withheld → case log-odds -2.183 (ranking unchanged); node deleted → -2.183 (ranking unchanged)

**Hypotheses (as shown to the verifier)**

- **H1** (Candidate A): Mitochondrial acquisition was an initiating/foundational event that preceded or enabled much of later eukaryotic cellular complexity; major eukaryote-specific cellular systems should therefore largely elaborate after mitochondrial acquisition.
- **H2** (Candidate B): Substantial eukaryotic cellular machinery - including cytoskeletal, membrane-remodelling/trafficking, endomembrane, phagocytic, and nuclear-associated complexity - evolved before mitochondrial acquisition in an already complex archaeal host.

**Verifier cross-hypothesis judgments** — P(X|H) combines these by noisy-OR

| hypothesis | origin? | direct edge | route via parent | P(X\|H) |
| --- | --- | --- | --- | --- |
| H1 | no | `unlikely` | X4 [H→parent `unlikely`, P=0.30] → `implied` | 0.713 |
| H2 | yes | `implied` | X4 [H→parent `implied`, P=0.80] → `implied` | 0.948 |

- edge rationale, **H1** → node: If mitochondrial acquisition was required for later eukaryotic complexity, it is less likely that genes for actin and tubulin homologs would be present in Asgard archaea predating this event.
- edge rationale, **H2** → node: If substantial eukaryotic cellular machinery evolved before mitochondrial acquisition, it is expected that Asgard archaea closely related to eukaryotes would possess genes encoding actin and tubulin homologs.
- parent `X4`: Archaeal lineages closely related to eukaryotes possess genes encoding cytoskeletal proteins such as actin and tubulin homologs.
- chain rationale, `X4` → node: The parent proposition states that archaeal lineages closely related to eukaryotes possess these genes, which implies their presence in the genomes of Asgard archaeal lineages if they are considered closely related to eukaryotes.

**Verifier evidence** — label used in score: `strong_support` (log-LR +2.0)

- queries: `Asgard archaea actin genes`; `Asgard archaea tubulin homologs genomes`
- assessor rationale: Multiple records directly state that Asgard archaeal genomes contain genes encoding actin homologs, and at least one record explicitly mentions tubulin as well. These statements are made in the context of Asgard lineages closely related to eukaryotes, and are not merely inferential. The evidence is consistent and comes from both primary research and review articles, including direct genomic analysis and protein characterization.
- supporting spans cited by the assessor:
  - "ESPs represent 5% of its protein-coding genes, including four actin homologues."
  - "identifying groups of archaeal species, such as the superphylum TACK and the Asgard archaea, has shown that primitive genes for eukaryotic signature proteins （ ESP ） already existed in the genomes of these archaeal species. Some ESPs are especially important, including actin and tubulin in the cytoskeleton"
  - "Asgard archaea genomes contain potential eukaryotic-like genes that provide intriguing insight for the evolution of eukaryotes."
  - "These prokaryotes seem to encode an unprecedented number of genes related to features typically descriptive of eukaryotes, including intracellular trafficking, vesicular transport and a dynamic actin-based cytoskeleton."
  - "sequencing of anaerobic sediments identified a group of uncultured organisms, Asgard archaea, which contain genes with homology to eukaryotic signature genes."
- 10 papers shown; key papers: `s2:4cc65d91f1d8c6dcdb247b349e1d5a7c3b7859d8`, `s2:71fc837544469150ef20e05f1cc00075c0765b05`, `s2:ca5c456f1359cb5a65fb0571e72d3c74ee4d6168`, `s2:dd9fc09b6726d7b226c7cf679dc896c71e8a9f4c`, `s2:df4680129acc8a7a82b5c8d382db89e8541c40f7`
- _The evidence assessor returns ONE label for the node from all papers shown; the method has no per-paper contribution. Key papers and spans are those the assessor cited._

<details><summary>[1] **KEY** Insights into the evolution of regulated actin dynamics via characterization of primitive gelsolin/cofilin proteins from Asgard archaea — C. Akıl, L. Tran, Magali Orhant-Prioux, Yohendran Baskaran et al. (2020); cutoff-filter date 2020-08-03; doi:10.1073/pnas.2009167117</summary>

```text
[1] Insights into the evolution of regulated actin dynamics via characterization of primitive gelsolin/cofilin proteins from Asgard archaea
    id: s2:4cc65d91f1d8c6dcdb247b349e1d5a7c3b7859d8
    date: 2020-08-03
    venue: Proceedings of the National Academy of Sciences of the United States of America
    authors: C. Akıl, L. Tran, Magali Orhant-Prioux, Yohendran Baskaran, E. Manser, L. Blanchoin, R. Robinson
    abstract: Significance Eukaryotic gelsolin superfamily proteins generally comprise three or more related domains. Here we characterize single- and double-domain gelsolins from Thorarchaeota (Thor). Similar domain architectures are present in Heimdall-, Loki-, and Odinarchaeota. Thor gelsolins are functional in regulating rabbit actin in in vitro assays, showing a range of activities including actin filament severing and bundling. These gelsolins bind to the eukaryotic gelsolin/cofilin-binding site on actin. Two-domain, but not one-domain, gelsolins are calcium regulated. Thor gelsolins appear to have the characteristics and structure consistent with primitive gelsolins/cofilins, suggesting that these single- and double-domain gelsolins are a record of a nascent preeukaryotic actin-regulation machinery. Asgard archaea genomes contain potential eukaryotic-like genes that provide intriguing insight for the evolution of eukaryotes. The eukaryotic actin polymerization/depolymerization cycle is critical for providing force and structure in many processes, including membrane remodeling. In general, Asgard genomes encode two classes of actin-regulating proteins from sequence analysis, profilins and gelsolins. Asgard profilins were demonstrated to regulate actin filament nucleation. Here, we identify actin filament severing, capping, annealing and bundling, and monomer sequestration activities by gelsolin proteins from Thorarchaeota (Thor), which complete a eukaryotic-like actin depolymerization cycle, and indicate complex actin cytoskeleton regulation in Asgard organisms. Thor gelsolins have homologs in other Asgard archaea and comprise one or two copies of the prototypical gelsolin domain. This appears to be a record of an initial preeukaryotic gene duplication event, since eukaryotic gelsolins are generally comprise three to six domains. X-ray structures of these proteins in complex with mammalian actin revealed similar interactions to the first domain of human gelsolin or cofilin [...]
    note: possibly the same work as s2:ace8ff0946dfd3dc93709b91142a8d7c6a2fc69f
```
</details>

<details><summary>[2] Complex eukaryotic-like actin regulation systems from Asgard archaea — C. Akıl, L. Tran, Magali Orhant-Prioux, Yohendran Baskaran et al. (2019); cutoff-filter date 2019-09-14; doi:10.1101/768580</summary>

```text
[2] Complex eukaryotic-like actin regulation systems from Asgard archaea
    id: s2:21c7caf9b26ef1b41098a8fcdc3cf907beccd6c1
    date: 2019-09-14
    venue: bioRxiv (preprint)
    authors: C. Akıl, L. Tran, Magali Orhant-Prioux, Yohendran Baskaran, E. Manser, L. Blanchoin, R. Robinson
    abstract: Asgard archaea genomes contain potential eukaryotic-like genes that provide intriguing insight for the evolution of eukaryotes. The actin polymerization/depolymerization cycle is critical for providing force and structure for a variety of processes in eukaryotes, including membrane remodelling. Here, we identify actin filament severing, capping, annealing and bundling, and monomer sequestration activities by gelsolin proteins from Thorarchaeota (Thor), which complete a eukaryote-like actin depolymerization cycle. Thor gelsolins are comprised of one or two copies of the prototypical gelsolin domain and appear to be a record of an initial pre-eukaryotic gene duplication event, since eukaryotic gelsolins are generally comprised of three to six domains. X-ray crystal structure determination of these proteins in complex with mammalian actin revealed similar interactions to the first domain of human gelsolin. Asgard two-domain, but not one-domain, gelsolins contain calcium-binding sites, which is manifested in calcium-controlled activities. Expression of two-domain gelsolins in mammalian cells led to enhanced actin filament disassembly on ionomycin-triggered calcium release. This functional demonstration, at the cellular level, provides evidence for calcium-regulated actin cytoskeleton in Asgard archaea, and indicates that the calcium-regulated actin cytoskeleton predates eukaryotes. In eukaryotes, dynamic bundled filaments are responsible for shaping filopodia and microvilli. By correlation, the formation of the protrusions observed from Lokiarchaeota cell bodies may involve gelsolin-regulated actin structures.
```
</details>

<details><summary>[3] **KEY** Actin cytoskeleton and complex cell architecture in an Asgard archaeon — Thiago Rodrigues-Oliveira, F. Wollweber, Rafael I. Ponce-Toledo, Jing-Wei Xu et al. (2022); cutoff-filter date 2022-12-21; doi:10.1038/s41586-022-05550-y</summary>

```text
[3] Actin cytoskeleton and complex cell architecture in an Asgard archaeon
    id: s2:dd9fc09b6726d7b226c7cf679dc896c71e8a9f4c
    date: 2022-12-21
    venue: Nature
    authors: Thiago Rodrigues-Oliveira, F. Wollweber, Rafael I. Ponce-Toledo, Jing-Wei Xu, S. Rittmann, A. Klingl, M. Pilhofer, Christa Schleper
    abstract: Culture and analysis of ‘ Candidatus  Lokiarchaeum ossiferum’—a member of the Asgard phylum—reveals an elaborate cell architecture with extensive membranous protrusions. Asgard archaea are considered to be the closest known relatives of eukaryotes. Their genomes contain hundreds of eukaryotic signature proteins (ESPs), which inspired hypotheses on the evolution of the eukaryotic cell^ 1 – 3 . A role of ESPs in the formation of an elaborate cytoskeleton and complex cellular structures has been postulated^ 4 – 6 , but never visualized. Here we describe a highly enriched culture of ‘ Candidatus Lokiarchaeum ossiferum’, a member of the Asgard phylum, which thrives anaerobically at 20 °C on organic carbon sources. It divides every 7–14 days, reaches cell densities of up to 5 × 10^7 cells per ml and has a significantly larger genome compared with the single previously cultivated Asgard strain^ 7 . ESPs represent 5% of its protein-coding genes, including four actin homologues. We imaged the enrichment culture using cryo-electron tomography, identifying ‘ Ca . L. ossiferum’ cells on the basis of characteristic expansion segments of their ribosomes. Cells exhibited coccoid cell bodies and a network of branched protrusions with frequent constrictions. The cell envelope consists of a single membrane and complex surface structures. A long-range cytoskeleton extends throughout the cell bodies, protrusions and constrictions. The twisted double-stranded architecture of the filaments is consistent with F-actin. Immunostaining indicates that the filaments comprise Lokiactin—one of the most highly conserved ESPs in Asgard archaea. We propose that a complex actin-based cytoskeleton predated the emergence of the first eukaryotes and was a crucial feature in the evolution of the Asgard phylum by scaffolding elaborate cellular structures.
```
</details>

<details><summary>[4] **KEY** The Archaeal Roots of the Eukaryotic Dynamic Actin Cytoskeleton. — Courtney W. Stairs, Thijs J. G. Ettema (2020); cutoff-filter date 2020-05-18; doi:10.1016/j.cub.2020.02.074</summary>

```text
[4] The Archaeal Roots of the Eukaryotic Dynamic Actin Cytoskeleton.
    id: s2:df4680129acc8a7a82b5c8d382db89e8541c40f7
    date: 2020-05-01
    venue: Current Biology
    authors: Courtney W. Stairs, Thijs J. G. Ettema
    abstract: It is generally well accepted that eukaryotes evolved from the symbiosis of an archaeal host cell and an alphaproteobacterium, a union that ultimately gave rise to the complex, eukaryotic cells we see today. However, the catalyst of this merger, the exact nature of the cellular biology of either partner, or how this event spawned the vast majority of complex life on Earth remains enigmatic. In recent years, the discovery of the Asgard archaea, the closest known prokaryotic relatives of eukaryotes, has been monumental for addressing these unanswered questions. These prokaryotes seem to encode an unprecedented number of genes related to features typically descriptive of eukaryotes, including intracellular trafficking, vesicular transport and a dynamic actin-based cytoskeleton. Collectively, these features imply that the Asgard archaea have the potential for cellular complexity previously thought to be unique to eukaryotes. Here, we review the most recent advances in our understanding of the archaeal cytoskeleton and its implications for determining the origin of eukaryotic cellular complexity.
```
</details>

<details><summary>[5] **KEY** Mythical origins of the actin cytoskeleton. — C. Akıl, Y. Kitaoku, L. Tran, D. Liebl et al. (2020); cutoff-filter date 2020-10-10; doi:10.1016/j.ceb.2020.08.011</summary>

```text
[5] Mythical origins of the actin cytoskeleton.
    id: s2:ca5c456f1359cb5a65fb0571e72d3c74ee4d6168
    date: 2020-10-09
    venue: Current Opinion in Cell Biology
    authors: C. Akıl, Y. Kitaoku, L. Tran, D. Liebl, H. Choe, Duangkamon Muengsaen, W. Suginta, A. Schulte
    abstract: The origin of the eukaryotic cell is one of the greatest mysteries in modern biology. Eukaryotic-wide specific biological processes arose in the lost ancestors of eukaryotes. These distinctive features, such as the actin cytoskeleton, define what it is to be a eukaryote. Recent sequencing, characterization, and isolation of Asgard archaea have opened an intriguing window into the pre-eukaryotic cell. Firstly, sequencing of anaerobic sediments identified a group of uncultured organisms, Asgard archaea, which contain genes with homology to eukaryotic signature genes. Secondly, characterization of the products of these genes at the protein level demonstrated that Asgard archaea have related biological processes to eukaryotes. Finally, the isolation of an Asgard archaeon has produced a model organism in which the morphological consequences of the eukaryotic-like processes can be studied. Here, we consider the consequences for the Asgard actin cytoskeleton and for the evolution of a regulated actin system in the archaea-to-eukaryotic transition.
```
</details>

<details><summary>[6] Giant viruses encode novel types of actins possibly related to the origin of eukaryotic actin: the viractins — Violette Da Cunha, Morgan Gaia, H. Ogata, O. Jaillon et al. (2020); cutoff-filter date 2020-06-16; doi:10.1101/2020.06.16.150565</summary>

```text
[6] Giant viruses encode novel types of actins possibly related to the origin of eukaryotic actin: the viractins
    id: s2:cc2500dd56d0b65a7f4d17db1e70954df23ffbd8
    date: 2020-06-16
    venue: bioRxiv (preprint)
    authors: Violette Da Cunha, Morgan Gaia, H. Ogata, O. Jaillon, Tom O. Delmont, P. Forterre
    abstract: Actin is a major component of the eukaryotic cytoskeleton. Many related actin homologues can be found in eukaryotes1, some of them being present in most or all eukaryotic lineages. The gene repertoire of the Last Eukaryotic Common Ancestor (LECA) therefore would have harbored both actin and various actin-related proteins (ARPs). A current hypothesis is that the different ARPs originated by gene duplication in the proto-eukaryotic lineage from an actin gene that was inherited from Asgard archaea. Here, we report the first detection of actin-related genes in viruses (viractins), encoded by 19 genomes belonging to the Imitervirales, a viral order encompassing the giant Mimiviridae. Most viractins were closely related to the actin, contrasting with actin-related genes of Asgard archaea and Bathyarchaea (a newly discovered clade). Our phylogenetic analysis suggests viractins could have been acquired from proto-eukaryotes and possibly gave rise to the conventional eukaryotic actin after being reintroduced into the pre-LECA eukaryotic lineage.
```
</details>

<details><summary>[7] **KEY** Importance of Prokaryotes for the Origin of Eukaryotes and the Global Environment at 2.4-2.0 Ga — Naota Takeyama, Yuka Takahashi, Shohei Nagata, Y. Sawaki et al. (2020); cutoff-filter date 2020-12-25; doi:10.5026/jgeography.129.899</summary>

```text
[7] Importance of Prokaryotes for the Origin of Eukaryotes and the Global Environment at 2.4-2.0 Ga
    id: s2:71fc837544469150ef20e05f1cc00075c0765b05
    date: 2020-12-25
    venue: Journal of Geography (Chigaku Zasshi)
    authors: Naota Takeyama, Yuka Takahashi, Shohei Nagata, Y. Sawaki, Tomohiko Sato, S. Maruyama, A. Kanai
    abstract: ― Abstract The origin of eukaryotic organisms is one of the most important questions in biology. So far, it has been suggested that eukaryotes are phylogenetically related to Archaea. Indeed, recent progress in archaeal genomic biology seems to have accurately determined the exact position of Archaea in the birth of the Eukaryota. In particular, identifying groups of archaeal species, such as the superphylum TACK and the Asgard archaea, has shown that primitive genes for eukaryotic signature proteins （ ESP ） already existed in the genomes of these archaeal species. Some ESPs are especially important, including actin and tubulin in the cytoskeleton and the ESCRT complex, which is involved in nuclear membrane formation. There have been many reports that eukaryotic intracellular organelles, such as mitochondria and chloroplasts, evolved from speciﬁc symbiotic bacteria. Moreover, eukaryotic genes are disrupted by intronic sequences, which must be removed or “spliced” and the exons connected after the primary transcript is generated, to make a mature functional mRNA. Recently, it has been suggested that the self-splicing
```
</details>

<details><summary>[8] Complete genomes of Asgard archaea reveal diverse integrated and mobile genetic elements — L. Valentin-Alvarado, Ling-Dong Shi, K. Appler, Alexander Crits-Christoph et al. (2024); cutoff-filter date 2024-10-15; doi:10.1101/gr.279480.124</summary>

```text
[8] Complete genomes of Asgard archaea reveal diverse integrated and mobile genetic elements
    id: s2:e6c1517d25f3fd63fe8c18daea997d100398e2d3
    date: 2024-10-01
    venue: Genome Research (preprint)
    authors: L. Valentin-Alvarado, Ling-Dong Shi, K. Appler, Alexander Crits-Christoph, V. de Anda, Benjamin A. Adler, Michael L. Cui, Lynn Ly
    abstract: Asgard archaea are of great interest as the progenitors of Eukaryotes, but little is known about the mobile genetic elements (MGEs) that may shape their ongoing evolution. Here, we describe MGEs that replicate in Atabeyarchaeia, a wetland Asgard archaea lineage represented by two complete genomes. We used soil depth–resolved population metagenomic data sets to track 18 MGEs for which genome structures were defined and precise chromosome integration sites could be identified for confident host linkage. Additionally, we identified a complete 20.67 kbp circular plasmid and two family-level groups of viruses linked to Atabeyarchaeia, via CRISPR spacer targeting. Closely related 40 kbp viruses possess a hypervariable genomic region encoding combinations of specific genes for small cysteine-rich proteins structurally similar to restriction-homing endonucleases. One 10.9 kbp integrative conjugative element (ICE) integrates genomically into the Atabeyarchaeum deiterrae-1 chromosome and has a 2.5 kbp circularizable element integrated within it. The 10.9 kbp ICE encodes an expressed Type IIG restriction-modification system with a sequence specificity matching an active methylation motif identified by Pacific Biosciences (PacBio) high-accuracy long-read (HiFi) metagenomic sequencing. Restriction-modification of Atabeyarchaeia differs from that of another coexisting Asgard archaea, Freyarchaeia, which has few identified MGEs but possesses diverse defense mechanisms, including DISARM and Hachiman, not found in Atabeyarchaeia. Overall, defense systems and methylation mechanisms of Asgard archaea likely modulate their interactions with MGEs, and integration/excision and copy number variation of MGEs in turn enable host genetic versatility.
```
</details>

<details><summary>[9] Genomes of Asgard archaea encode profilins that regulate actin — C. Akıl, R. Robinson (2018); cutoff-filter date 2018-10-02; doi:10.1038/s41586-018-0548-6</summary>

```text
[9] Genomes of Asgard archaea encode profilins that regulate actin
    id: s2:d30a56d30b134fc3b0859fa8f3968b6f8290d3aa
    date: 2018-10-01
    venue: Nature
    authors: C. Akıl, R. Robinson
    abstract: [no abstract available]
```
</details>

<details><summary>[10] Genetic elements and defense systems drive diversification and evolution in Asgard archaea — L. Valentin-Alvarado, Ling-Dong Shi, K. Appler, Alexander Crits-Christoph et al. (2024); cutoff-filter date 2024-03-23; doi:10.1101/2024.03.22.586370</summary>

```text
[10] Genetic elements and defense systems drive diversification and evolution in Asgard archaea
    id: s2:703b9d3f624e80434597ed11069c47cdaf2dad25
    date: 2024-03-23
    venue: bioRxiv (preprint)
    authors: L. Valentin-Alvarado, Ling-Dong Shi, K. Appler, Alexander Crits-Christoph, Michael L. Cui, V. de Anda, Pedro Leão, Benjamin A. Adler
    abstract: [no abstract available]
```
</details>

<details><summary>Post-hoc automated audit — NON-AUTHORITATIVE; uses hidden benchmark annotations</summary>

- primary auditor: `silence_as_null_error`; statuses {'H1': 'indeterminate', 'H2': 'positive_or_present'}; discriminative=False
- primary reasoning: H2 predicts that substantial eukaryotic cellular machinery, including cytoskeletal components like actin and tubulin, evolved before mitochondrial acquisition, so their presence in Asgard archaea is expected. H1 is silent on whether actin and tubulin homologs should be present in archaeal relatives, as it focuses on elaboration after mitochondrial acquisition, not on their presence in the host lineage.
- derived opposition call: `manufactured_from_silence`
- evidence attribution: `informative_evidence_found` — The retrieved papers directly address the proposition, with multiple sources confirming the presence of actin and tubulin homolog genes in Asgard archaeal genomes closely related to eukaryotes. The assessor correctly interpreted the evidence, which includes primary genomic analyses and protein characterization. The process worked as intended.
- disagreement flags: {'second_rater_vs_primary_discriminative': None, 'second_rater_vs_primary_status': None, 'retest_vs_primary_category': None, 'any': False}
</details>

**Human review** — `generic_component_fact` · reviewer: Research Director · source: D045 · status: `first_pass_model_based_review` · genuinely discriminative: False · silence-as-null error: False · other fields not recorded

---

## #29 · `GP1-eukaryogenesis_mito_timing-X12`

**GP1-eukaryogenesis_mito_timing-X12** — case `eukaryogenesis_mito_timing`, node `X12`

> Members of the Asgard archaea family encode cytoskeletal protein homologs in their genomes.

- generated from **H2** (Candidate B); abstraction: `class`
- generator's stated reason: The claim about closely related lineages implies that the broader Asgard archaea family, to which they belong, is more likely to encode cytoskeletal protein homologs.
- influence: **0.239** (rank 7 in case, 29 overall; cumulative 68%) — favours **H2**
- log-likelihood contribution: H1 +1.715, H2 +1.954
- removing it alone: evidence withheld → case log-odds -2.183 (ranking unchanged); node deleted → -2.183 (ranking unchanged)

**Hypotheses (as shown to the verifier)**

- **H1** (Candidate A): Mitochondrial acquisition was an initiating/foundational event that preceded or enabled much of later eukaryotic cellular complexity; major eukaryote-specific cellular systems should therefore largely elaborate after mitochondrial acquisition.
- **H2** (Candidate B): Substantial eukaryotic cellular machinery - including cytoskeletal, membrane-remodelling/trafficking, endomembrane, phagocytic, and nuclear-associated complexity - evolved before mitochondrial acquisition in an already complex archaeal host.

**Verifier cross-hypothesis judgments** — P(X|H) combines these by noisy-OR

| hypothesis | origin? | direct edge | route via parent | P(X\|H) |
| --- | --- | --- | --- | --- |
| H1 | no | `unlikely` | X4 [H→parent `unlikely`, P=0.30] → `implied` | 0.713 |
| H2 | yes | `implied` | X4 [H→parent `implied`, P=0.80] → `implied` | 0.948 |

- edge rationale, **H1** → node: If major eukaryotic cellular systems largely elaborated after mitochondrial acquisition, it is less likely that Asgard archaea (which predate this event) would encode cytoskeletal protein homologs.
- edge rationale, **H2** → node: If substantial eukaryotic cellular machinery, including cytoskeletal complexity, evolved before mitochondrial acquisition in an archaeal host, it is clearly expected that Asgard archaea would encode cytoskeletal protein homologs.
- parent `X4`: Archaeal lineages closely related to eukaryotes possess genes encoding cytoskeletal proteins such as actin and tubulin homologs.
- chain rationale, `X4` → node: If archaeal lineages closely related to eukaryotes possess cytoskeletal protein homologs, it is likely but not certain that Asgard archaea, which are considered closely related to eukaryotes, also encode such homologs.

**Verifier evidence** — label used in score: `strong_support` (log-LR +2.0)

- queries: `Asgard archaea cytoskeletal protein homologs`; `Asgard archaea genome cytoskeleton genes`
- assessor rationale: Multiple records directly state that Asgard archaea genomes encode homologs of cytoskeletal proteins, including actin-regulating proteins (profilins, gelsolins) and ESCRT components, which are key cytoskeletal and membrane remodeling proteins in eukaryotes. These homologs are described as present in several Asgard lineages and are explicitly identified in their genomes. The evidence is consistent and comes from independent studies, including structural and functional characterization.
- supporting spans cited by the assessor:
  - "Asgard genomes encode diverse eukaryotic signature proteins (ESPs), representing homologs of proteins that play important roles in the complex organization of eukaryotic cells"
  - "Thor gelsolins have homologs in other Asgard archaea and comprise one or two copies of the prototypical gelsolin domain."
  - "In general, Asgard genomes encode two classes of actin-regulating proteins from sequence analysis, profilins and gelsolins."
  - "Recently, genes encoding eukaryote-like ESCRT protein components have been identified in the genomes of Asgard archaea, a newly proposed archaeal superphylum that is thought to include the closest extant prokaryotic relatives of eukaryotes."
  - "Genes encoding for ESCRT proteins have been identified in Asgard archaea, a newly discovered superphylum, currently recognized as the ancestor of all eukaryotes."
- 10 papers shown; key papers: `s2:4cc65d91f1d8c6dcdb247b349e1d5a7c3b7859d8`, `s2:6495ecb5d13c094fdb512d34476ec035b78334f7`, `s2:94ff780009ab792c0a9351b388cbce3eca8ddf7`, `s2:aa4014b6a7933eeb353390f858585e570b642338`
- _The evidence assessor returns ONE label for the node from all papers shown; the method has no per-paper contribution. Key papers and spans are those the assessor cited._

<details><summary>[1] **KEY** Structure-based inference of eukaryotic complexity in Asgard archaea — Stephan Köstlbacher, J. V. van Hooff, Kassiani Panagiotou, Daniel Tamarit et al. (2024); cutoff-filter date 2024-07-05; doi:10.1101/2024.07.03.601958</summary>

```text
[1] Structure-based inference of eukaryotic complexity in Asgard archaea
    id: s2:6495ecb5d13c094fdb512d34476ec035b78334f7
    date: 2024-07-05
    venue: bioRxiv (preprint)
    authors: Stephan Köstlbacher, J. V. van Hooff, Kassiani Panagiotou, Daniel Tamarit, V. de Anda, K. Appler, Brett J. Baker, T. Ettema
    abstract: Asgard archaea played a key role in the origin of the eukaryotic cell. While previous studies found that Asgard genomes encode diverse eukaryotic signature proteins (ESPs), representing homologs of proteins that play important roles in the complex organization of eukaryotic cells, the cellular characteristics and complexity of the Asgard archaeal ancestor of eukaryotes remain unclear. Here, we used de novo protein structure modeling and sensitive sequence similarity detection algorithms within an expanded Asgard archaeal genomic dataset to build a structural catalogue of the Asgard archaeal pangenome and identify 908 new ‘isomorphic’ ESPs (iESPs), representing clusters of protein structures most similar to eukaryotic proteins and that likely underwent extensive sequence divergence. While most previously identified ESPs were involved in cellular processes and signaling, iESPs are enriched in information storage and processing functions, with several being potentially implicated in facilitating cellular complexity. By expanding the complement of eukaryotic proteins in Asgard archaea, this study indicates that the archaeal ancestor of eukaryotes was more complex than previously assumed.
```
</details>

<details><summary>[2] Tubulin Homologs in Bacteria and Archaea — N. Rumyantseva, D. M. Golofeeva, A. A. Khasanova, A. D. Vedyaykin (2024); cutoff-filter date 2024-05-14; doi:10.1134/s002626172460469x</summary>

```text
[2] Tubulin Homologs in Bacteria and Archaea
    id: s2:fe140c433d63a131e79d1a0b498b116b783f0d74
    date: 2024-05-14
    venue: Microbiology
    authors: N. Rumyantseva, D. M. Golofeeva, A. A. Khasanova, A. D. Vedyaykin
    abstract: [no abstract available]
```
</details>

<details><summary>[3] Unprecedented Diversity of Unique CRISPR-Cas-Related Systems and Cas1 Homologs in Asgard Archaea — K. Makarova, Y. Wolf, Sergey A. Shmakov, Yang Liu et al. (2020); cutoff-filter date 2020-06-01; doi:10.1089/crispr.2020.0012</summary>

```text
[3] Unprecedented Diversity of Unique CRISPR-Cas-Related Systems and Cas1 Homologs in Asgard Archaea
    id: s2:1356aab49d466415f29c2d6c6603b2f07e8a71c1
    date: 2020-06-01
    venue: The CRISPR Journal
    authors: K. Makarova, Y. Wolf, Sergey A. Shmakov, Yang Liu, Meng Li, E. Koonin
    abstract: The principal function of archaeal and bacterial CRISPR-Cas systems is antivirus adaptive immunity. However, recent genome analyses identified a variety of derived CRISPR-Cas variants at least some of which appear to perform different functions. Here, we describe a unique repertoire of CRISPR-Cas-related systems that we discovered by searching archaeal metagenome-assemble genomes of the Asgard superphylum. Several of these variants contain extremely diverged homologs of Cas1, the integrase involved in CRISPR adaptation as well as casposon transposition. Strikingly, the diversity of Cas1 in Asgard archaea alone is greater than that detected so far among the rest of archaea and bacteria. The Asgard CRISPR-Cas derivatives also encode distinct forms of Cas4, Cas5, and Cas7 proteins, and/or additional nucleases. Some of these systems are predicted to perform defense functions, but possibly not programmable ones, whereas others are likely to represent previously unknown mobile genetic elements.
```
</details>

<details><summary>[4] **KEY** Coevolution of Eukaryote-like Vps4 and ESCRT-III Subunits in the Asgard Archaea — Zhongyi Lu, Ting Fu, Tianyi Li, Yang Liu et al. (2020); cutoff-filter date 2020-05-19; doi:10.1128/mbio.00417-20</summary>

```text
[4] Coevolution of Eukaryote-like Vps4 and ESCRT-III Subunits in the Asgard Archaea
    id: s2:aa4014b6a7933eeb353390f858585e570b642338
    date: 2020-05-19
    venue: mBio
    authors: Zhongyi Lu, Ting Fu, Tianyi Li, Yang Liu, Siyu Zhang, Jinquan Li, Junbiao Dai, E. Koonin
    abstract: The discovery of Asgard archaea has changed the existing ideas on the origins of eukaryotes. Researchers propose that eukaryotic cells evolved from Asgard archaea. This hypothesis partly stems from the presence of multiple eukaryotic signature proteins in Asgard archaea, including homologs of ESCRT proteins that are essential components of the endomembrane system in eukaryotes. However, structural and functional features of Asgard ESCRT remain unknown. Our study provides evidence that Asgard ESCRT is functionally comparable to the eukaryotic counterparts, suggesting that despite the apparent absence of endomembranes in archaea, eukaryotic ESCRT was inherited from an Asgard archaeal ancestor, alongside the emergence of endomembrane system during eukaryogenesis. ABSTRACT The emergence of the endomembrane system is a key step in the evolution of cellular complexity during eukaryogenesis. The endosomal sorting complex required for transport (ESCRT) machinery is essential and required for the endomembrane system functions in eukaryotic cells. Recently, genes encoding eukaryote-like ESCRT protein components have been identified in the genomes of Asgard archaea, a newly proposed archaeal superphylum that is thought to include the closest extant prokaryotic relatives of eukaryotes. However, structural and functional features of Asgard ESCRT remain uncharacterized. Here, we show that Vps4, Vps2/24/46, and Vps20/32/60, the core functional components of the Asgard ESCRT, coevolved eukaryote-like structural and functional features. Phylogenetic analysis shows that Asgard Vps4, Vps2/24/46, and Vps20/32/60 are closely related to their eukaryotic counterparts. Molecular dynamics simulation and biochemical assays indicate that Asgard Vps4 contains a eukaryote-like microtubule-interacting and transport (MIT) domain that binds the distinct type 1 MIT-interacting motif and type 2 MIT-interacting motif in Vps2/24/46 and Vps20/32/60, respectively. The Asgard Vps4 partly, but much more e [...]
    note: merged with 1 other version(s) of the same work
```
</details>

<details><summary>[5] **KEY** Insights into the evolution of regulated actin dynamics via characterization of primitive gelsolin/cofilin proteins from Asgard archaea — C. Akıl, L. Tran, Magali Orhant-Prioux, Yohendran Baskaran et al. (2020); cutoff-filter date 2020-08-03; doi:10.1073/pnas.2009167117</summary>

```text
[5] Insights into the evolution of regulated actin dynamics via characterization of primitive gelsolin/cofilin proteins from Asgard archaea
    id: s2:4cc65d91f1d8c6dcdb247b349e1d5a7c3b7859d8
    date: 2020-08-03
    venue: Proceedings of the National Academy of Sciences of the United States of America
    authors: C. Akıl, L. Tran, Magali Orhant-Prioux, Yohendran Baskaran, E. Manser, L. Blanchoin, R. Robinson
    abstract: Significance Eukaryotic gelsolin superfamily proteins generally comprise three or more related domains. Here we characterize single- and double-domain gelsolins from Thorarchaeota (Thor). Similar domain architectures are present in Heimdall-, Loki-, and Odinarchaeota. Thor gelsolins are functional in regulating rabbit actin in in vitro assays, showing a range of activities including actin filament severing and bundling. These gelsolins bind to the eukaryotic gelsolin/cofilin-binding site on actin. Two-domain, but not one-domain, gelsolins are calcium regulated. Thor gelsolins appear to have the characteristics and structure consistent with primitive gelsolins/cofilins, suggesting that these single- and double-domain gelsolins are a record of a nascent preeukaryotic actin-regulation machinery. Asgard archaea genomes contain potential eukaryotic-like genes that provide intriguing insight for the evolution of eukaryotes. The eukaryotic actin polymerization/depolymerization cycle is critical for providing force and structure in many processes, including membrane remodeling. In general, Asgard genomes encode two classes of actin-regulating proteins from sequence analysis, profilins and gelsolins. Asgard profilins were demonstrated to regulate actin filament nucleation. Here, we identify actin filament severing, capping, annealing and bundling, and monomer sequestration activities by gelsolin proteins from Thorarchaeota (Thor), which complete a eukaryotic-like actin depolymerization cycle, and indicate complex actin cytoskeleton regulation in Asgard organisms. Thor gelsolins have homologs in other Asgard archaea and comprise one or two copies of the prototypical gelsolin domain. This appears to be a record of an initial preeukaryotic gene duplication event, since eukaryotic gelsolins are generally comprise three to six domains. X-ray structures of these proteins in complex with mammalian actin revealed similar interactions to the first domain of human gelsolin or cofilin [...]
```
</details>

<details><summary>[6] The Asgard Archaeal-Unique Contribution to Protein Families of the Eukaryotic Common Ancestor Was 0.3% — Michael Knopp, Simon Stockhorst, M. van der Giezen, S. Garg et al. (2021); cutoff-filter date 2021-04-21; doi:10.1093/gbe/evab085</summary>

```text
[6] The Asgard Archaeal-Unique Contribution to Protein Families of the Eukaryotic Common Ancestor Was 0.3%
    id: s2:84926b2cd2c00281c2d0f9312ffbb313c7ec596b
    date: 2021-02-10
    venue: bioRxiv (preprint)
    authors: Michael Knopp, Simon Stockhorst, M. van der Giezen, S. Garg, S. Gould
    abstract: Ever since the first report of a new archaeal lineage, the asgardarchaea, their metagenome analyses have encouraged continued speculations on a type of cell biology ranging between that of prokaryotes and eukaryotes. While it appears a tempting notion, recent microscopic images of an asgardarchaeon suggest otherwise. We inspected the origin of eukaryotic protein families with respect to their distribution across bacteria and archaea. This reveals that the protein families shared exclusively between asgardarchaea and eukaryotes amounts to only 0.3% of the protein families conserved across all eukaryotes. Asgardarchaeal diversity is likely unrivaled across archaea, but their cell biology remains prokaryotic in nature and lends support for the importance of endosymbiosis in evolving eukaryotic traits. Summary The difference between pro- and eukaryotic biology is evident in their genomes, cell biology, and evolution of complex and macroscopic body plans. The lack of intermediates between the two types of cells places the endosymbiotic acquisition of the mitochondrion through an archaeal host at the event horizon of eukaryote origin. The identification of eukaryote specific proteins in a new archaeal phylum, the asgardarchaea, has fueled speculations about their cellular complexity, suggesting they could be eukaryote-like. Here we analyzed the coding capacity of 150 eukaryotes, 1000 bacteria, and 226 archaea, including the only cultured member of the asgardarchaea, Candidatus Prometheoarchaeon syntrophicum MK-D1. Established clustering methods that recover endosymbiotic contributions to eukaryotic genomes, recover an asgardarchaeal-unique contribution of a mere 0.3% to protein families present in the last eukaryotic common ancestor, while simultaneously suggesting that asgardarchaeal diversity rivals that of all other archaea combined. Furthermore, we show that the number of homologs shared exclusively between asgardarchaea and eukaryotes is only 27 on average. Genomic a [...]
```
</details>

<details><summary>[7] The Asgard archaeal ESCRT-III system forms helical filaments and remodels eukaryotic membranes, shedding light on the emergence of eukaryogenesis — Nataly Melnikov, B. Junglas, G. Halbi, Dikla Nachmias et al. (2024); cutoff-filter date 2024-07-04; doi:10.1101/2022.09.07.506706</summary>

```text
[7] The Asgard archaeal ESCRT-III system forms helical filaments and remodels eukaryotic membranes, shedding light on the emergence of eukaryogenesis
    id: s2:d13e708d742c916411dc1ddb38870c1e98dd4241
    date: 2024-07-04
    venue: bioRxiv (preprint)
    authors: Nataly Melnikov, B. Junglas, G. Halbi, Dikla Nachmias, Erez Zerbib, Alexander Upcher, R. Zalk, C. Sachse
    abstract: [no abstract available]
```
</details>

<details><summary>[8] Diversity and Potential Multifunctionality of Archaeal CetZ Tubulin-like Cytoskeletal Proteins — Hannah J. Brown, I. Duggin (2023); cutoff-filter date 2023-01-09; doi:10.3390/biom13010134</summary>

```text
[8] Diversity and Potential Multifunctionality of Archaeal CetZ Tubulin-like Cytoskeletal Proteins
    id: s2:959b19ba95bf4667cfa91a33ec832bac783078cb
    date: 2023-01-01
    venue: Biomolecules
    authors: Hannah J. Brown, I. Duggin
    abstract: Tubulin superfamily (TSF) proteins are widespread, and are known for their multifaceted roles as cytoskeletal proteins underpinning many basic cellular functions, including morphogenesis, division, and motility. In eukaryotes, tubulin assembles into microtubules, a major component of the dynamic cytoskeletal network of fibres, whereas the bacterial homolog FtsZ assembles the division ring at midcell. The functions of the lesser-known archaeal TSF proteins are beginning to be identified and show surprising diversity, including homologs of tubulin and FtsZ as well as a third archaea-specific family, CetZ, implicated in the regulation of cell shape and possibly other unknown functions. In this study, we define sequence and structural characteristics of the CetZ family and CetZ1 and CetZ2 subfamilies, identify CetZ groups and diversity amongst archaea, and identify potential functional relationships through analysis of the genomic neighbourhoods of cetZ genes. We identified at least three subfamilies of orthologous CetZ proteins in the archaeal class Halobacteria, including CetZ1 and CetZ2 as well as a novel uncharacterized subfamily. CetZ1 and CetZ2 were correlated to one another as well as to cell shape and motility phenotypes across diverse Halobacteria. Among other known CetZ clusters in orders Archaeoglobales, Methanomicrobiales, Methanosarcinales, and Thermococcales, an additional uncharacterized group from Archaeoglobales and Methanomicrobiales is affiliated strongly with Halobacteria CetZs, suggesting that they originated via horizontal transfer. Subgroups of Halobacteria CetZ2 and Thermococcales CetZ genes were found adjacent to different type IV pili regulons, suggesting potential utilization of CetZs by type IV systems. More broadly conserved cetZ gene neighbourhoods include nucleotide and cofactor biosynthesis (e.g., F420) and predicted cell surface sugar epimerase genes. These findings imply that CetZ subfamilies are involved in multiple functions linked to [...]
```
</details>

<details><summary>[9] RNA-Dependent Cysteine Biosynthesis in Bacteria and Archaea — T. Mukai, A. Crnković, T. Umehara, Natalia N. Ivanova et al. (2017); cutoff-filter date 2017-05-10; doi:10.1128/mbio.00561-17</summary>

```text
[9] RNA-Dependent Cysteine Biosynthesis in Bacteria and Archaea
    id: s2:22425eda95c879f3c5112edead6a2bc809666687
    date: 2017-05-09
    venue: mBio
    authors: T. Mukai, A. Crnković, T. Umehara, Natalia N. Ivanova, N. Kyrpides, D. Söll
    abstract: ABSTRACT The diversity of the genetic code systems used by microbes on earth is yet to be elucidated. It is known that certain methanogenic archaea employ an alternative system for cysteine (Cys) biosynthesis and encoding; tRNACys is first acylated with phosphoserine (Sep) by O-phosphoseryl-tRNA synthetase (SepRS) and then converted to Cys-tRNACys by Sep-tRNA:Cys-tRNA synthase (SepCysS). In this study, we searched all genomic and metagenomic protein sequence data in the Integrated Microbial Genomes (IMG) system and at the NCBI to reveal new clades of SepRS and SepCysS proteins belonging to diverse archaea in the four major groups (DPANN, Euryarchaeota, TACK, and Asgard) and two groups of bacteria (“Candidatus Parcubacteria” and Chloroflexi). Bacterial SepRS and SepCysS charged bacterial tRNACys species with cysteine in vitro. Homologs of SepCysE, a scaffold protein facilitating SepRS⋅SepCysS complex assembly in Euryarchaeota class I methanogens, are found in a few groups of TACK and Asgard archaea, whereas the C-terminally truncated homologs exist fused or genetically coupled with diverse SepCysS species. Investigation of the selenocysteine (Sec)- and pyrrolysine (Pyl)-utilizing traits in SepRS-utilizing archaea and bacteria revealed that the archaea carrying full-length SepCysE employ Sec and that SepRS is often found in Pyl-utilizing archaea and Chloroflexi bacteria. We discuss possible contributions of the SepRS-SepCysS system for sulfur assimilation, methanogenesis, and other metabolic processes requiring large amounts of iron-sulfur enzymes or Pyl-containing enzymes. IMPORTANCE Comprehensive analyses of all genomic and metagenomic protein sequence data in public databases revealed the distribution and evolution of an alternative cysteine-encoding system in diverse archaea and bacteria. The finding that the SepRS-SepCysS-SepCysE- and the selenocysteine-encoding systems are shared by the Euryarchaeota class I methanogens, the Crenarchaeota AK8/W8A-19 group, and a [...]
```
</details>

<details><summary>[10] Asgard ESCRT-III and VPS4 reveal evolutionary conserved chromatin binding properties of the ESCRT machinery — Dikla Nachmias, Nataly Melnikov, Alvah Zorea, Yasmin De-picchoto et al. (2021); cutoff-filter date 2021-11-29; doi:10.1101/2021.11.29.470303</summary>

```text
[10] Asgard ESCRT-III and VPS4 reveal evolutionary conserved chromatin binding properties of the ESCRT machinery
    id: s2:94ff780009ab792c0a9351b388cbce3eca8ddf7d
    date: 2021-11-29
    venue: bioRxiv (preprint)
    authors: Dikla Nachmias, Nataly Melnikov, Alvah Zorea, Yasmin De-picchoto, R. Zarivach, I. Mizrahi, Natalie Elia
    abstract: The ESCRT machinery drive membrane remodeling in numerous processes in eukaryotes. Genes encoding for ESCRT proteins have been identified in Asgard archaea, a newly discovered superphylum, currently recognized as the ancestor of all eukaryotes. This begs the question of the functional evolutionary origin of this machinery and its conservation across lineages. Here, we find that Asgard-ESCRT’s exhibit conserved DNA-binding properties, which is derived from recruitment of specific members. We show that Asgard-ESCRT-III/VPS4 homologs interact with one another inside mammalian cells, associate with chromatin, and recruit their counterparts to organize in discrete foci in the mammalian nucleus. This is congruent with human-ESCRT-III homologs. We find that human- and Asgard-ESCRT-IIIs associate with chromatin via the same N terminal domain, and that human-ESCRT-III can recruit Asgard-VPS4 to the nucleus to form foci. Therefore, ESCRTs possess chromatin binding properties that were preserved through the billion years of evolution that separate Asgard and human cells.
```
</details>

<details><summary>Post-hoc automated audit — NON-AUTHORITATIVE; uses hidden benchmark annotations</summary>

- primary auditor: `silence_as_null_error`; statuses {'H1': 'indeterminate', 'H2': 'positive_or_present'}; discriminative=False
- primary reasoning: H2 predicts that substantial eukaryotic cellular machinery, such as cytoskeletal proteins, evolved before mitochondrial acquisition, so their presence in Asgard archaea is expected. H1 is silent on the presence of such homologs in Asgard archaea, as it focuses on elaboration after mitochondrial acquisition and does not predict their absence or presence in the archaeal relatives.
- derived opposition call: `manufactured_from_silence`
- evidence attribution: `informative_evidence_found` — The retrieved literature directly addresses the proposition, with multiple papers providing explicit evidence that Asgard archaea genomes encode homologs of cytoskeletal proteins, including actin regulators and ESCRT components. The assessor correctly identified and used this evidence to support the proposition, indicating the retrieval and assessment process worked as intended.
- disagreement flags: {'second_rater_vs_primary_discriminative': None, 'second_rater_vs_primary_status': None, 'retest_vs_primary_category': None, 'any': False}
</details>

**Human review** — `generic_component_fact` · reviewer: Research Director · source: D045 · status: `first_pass_model_based_review` · genuinely discriminative: False · silence-as-null error: False · other fields not recorded

---

## #30 · `GP1-eukaryogenesis_mito_timing-X22`

**GP1-eukaryogenesis_mito_timing-X22** — case `eukaryogenesis_mito_timing`, node `X22`

> Asgard archaeal genomes contain homologs of eukaryotic endomembrane system genes.

- generated from **H2** (Candidate B); abstraction: `specific`
- influence: **0.225** (rank 8 in case, 30 overall; cumulative 69%) — favours **H2**
- log-likelihood contribution: H1 +1.750, H2 +1.975
- removing it alone: evidence withheld → case log-odds -2.197 (ranking unchanged); node deleted → -2.197 (ranking unchanged)

**Hypotheses (as shown to the verifier)**

- **H1** (Candidate A): Mitochondrial acquisition was an initiating/foundational event that preceded or enabled much of later eukaryotic cellular complexity; major eukaryote-specific cellular systems should therefore largely elaborate after mitochondrial acquisition.
- **H2** (Candidate B): Substantial eukaryotic cellular machinery - including cytoskeletal, membrane-remodelling/trafficking, endomembrane, phagocytic, and nuclear-associated complexity - evolved before mitochondrial acquisition in an already complex archaeal host.

**Verifier cross-hypothesis judgments** — P(X|H) combines these by noisy-OR

| hypothesis | origin? | direct edge | route via parent | P(X\|H) |
| --- | --- | --- | --- | --- |
| H1 | no | `unlikely` | X6 [H→parent `unlikely`, P=0.30] → `strongly_implied` | 0.744 |
| H2 | yes | `implied` | X6 [H→parent `implied`, P=0.80] → `strongly_implied` | 0.972 |

- edge rationale, **H1** → node: If major eukaryote-specific cellular systems largely elaborated after mitochondrial acquisition, Asgard archaeal genomes (which predate mitochondria) would be less likely to contain homologs of eukaryotic endomembrane system genes.
- edge rationale, **H2** → node: If substantial eukaryotic cellular machinery, including endomembrane systems, evolved before mitochondrial acquisition in an archaeal host, it is clearly expected that Asgard archaeal genomes would contain homologs of these genes.
- parent `X6`: Members of the Asgard archaeal superphylum exhibit eukaryote-like cellular complexity, including genes for endomembrane and phagocytic functions.
- chain rationale, `X6` → node: If Asgard archaea exhibit eukaryote-like complexity including genes for endomembrane functions, it is strongly implied that their genomes contain homologs of eukaryotic endomembrane system genes.

**Verifier evidence** — label used in score: `strong_support` (log-LR +2.0)

- queries: `Asgard archaea endomembrane genes`; `Asgard archaeal eukaryotic homologs`
- assessor rationale: Multiple records directly state that Asgard archaeal genomes contain homologs of eukaryotic endomembrane system genes, including ESCRT components and Arf family GTPases. These findings are based on genomic identification and functional characterization, and are reported as direct evidence for the presence of eukaryote-like genes in Asgard archaea. The studies are independent and use different gene families to support the proposition.
- supporting spans cited by the assessor:
  - "Recently, genes encoding eukaryote-like ESCRT protein components have been identified in the genomes of Asgard archaea, a newly proposed archaeal superphylum that is thought to include the closest extant prokaryotic relatives of eukaryotes."
  - "Here, we show that a UEV-Vps23 protein family, which contains UEV and Vps23 domains, mediates an ancient ESCRT and ubiquitin system interplay in Asgard archaea."
  - "Our results show that Arf family GTPases are present in Asgardarchaeota, and strongly suggest that they originated in the archaeal contributor to eukaryogenesis, providing support for nascent endomembrane system capacity evolving early in eukaryogenesis."
- 10 papers shown; key papers: `s2:2bab312eb5127c5b3aceac1ba0f8a69b7ff7fb3c`, `s2:3fd208ebadff884b05d9062d422bc38fea999d8e`, `s2:55a43731cbbe21dd1a001b68bb552cca6ab3f7e3`
- _The evidence assessor returns ONE label for the node from all papers shown; the method has no per-paper contribution. Key papers and spans are those the assessor cited._

<details><summary>[1] **KEY** Co-evolution of Eukaryotic-like Vps4 and ESCRT-III Subunits in the Asgard Archaea — Zhongyi Lu, Ting Fu, Tianyi Li, Yang Liu et al. (2020); cutoff-filter date 2020-05-06; doi:10.1101/2020.05.05.080093</summary>

```text
[1] Co-evolution of Eukaryotic-like Vps4 and ESCRT-III Subunits in the Asgard Archaea
    id: s2:2bab312eb5127c5b3aceac1ba0f8a69b7ff7fb3c
    date: 2020-05-06
    venue: bioRxiv (preprint)
    authors: Zhongyi Lu, Ting Fu, Tianyi Li, Yang Liu, Siyu Zhang, Jinquan Li, Junbiao Dai, E. Koonin
    abstract: The emergence of the endomembrane system is a key step in the evolution of cellular complexity during eukaryogenesis. The Endosomal Sorting Complex Required for Transport (ESCRT) machinery is essential and required for the endomembrane system functions in eukaryotic cells. Recently, genes encoding eukaryote-like ESCRT protein components have been identified in the genomes of Asgard archaea, a newly proposed archaeal superphylum that is thought to include the closest extant prokaryotic relatives of eukaryotes. However, structural and functional features of Asgard ESCRT remain uncharacterized. Here we show that Vps4, Vps2/24/46, and Vps20/32/60, the core functional components of the Asgard ESCRT, co-evolved eukaryote-like structural and functional features. Phylogenetic analysis shows that Asgard Vps4, Vps2/24/46, and Vps20/32/60 are closely related to their eukaryotic counterparts. Molecular dynamic simulation and biochemical assays indicate that Asgard Vps4 contains a eukaryote-like Microtubule Interacting and Transport (MIT) domain that binds the distinct type-1 MIT Interacting Motif and type-2 MIT Interacting Motif in Vps2/24/46, and Vps20/32/60, respectively. The Asgard Vps4 partly, but much more efficiently than homologs from other archaea, complements the vps4 null mutant of Saccharomyces cerevisiae, further supporting the functional similarity between the membrane remodeling machineries of Asgard archaea and eukaryotes. Thus, this work provides evidence that the ESCRT complexes from Asgard archaea and eukaryotes are evolutionarily related and functionally similar. Thus, despite the apparent absence of endomembranes in Asgard archaea, the eukaryotic ESCRT seems to have been directly inherited from an Asgard ancestor, to become a key component of the emerging endomembrane system. IMPORTANCE The discovery of Asgard archaea has changed the exiting ideas on the origins of Eukaryotes. Researchers propose that eukaryotic cells evolve from Asgard archaea. This hypothe [...]
    note: merged with 1 other version(s) of the same work
```
</details>

<details><summary>[2] The symbiotic origin of the eukaryotic cell. — P. López-García, D. Moreira (2023); cutoff-filter date 2023-05-30; doi:10.5802/crbiol.118</summary>

```text
[2] The symbiotic origin of the eukaryotic cell.
    id: s2:bfbb10e2d371e78eb6ab4b8fd3818a598b4c8413
    date: 2023-05-30
    venue: Comptes rendus. Biologies
    authors: P. López-García, D. Moreira
    abstract: Eukaryogenesis represented a major evolutionary transition that led to the emergence of complex cells from simpler ancestors. For several decades, the most accepted scenario involved the evolution of an independent lineage of proto-eukaryotes endowed with an endomembrane system, including a nuclear compartment, a developed cytoskeleton and phagocytosis, which engulfed the alphaproteobacterial ancestor of mitochondria. However, the recent discovery by metagenomic and cultural approaches of Asgard archaea, which harbour many genes in common with eukaryotes and are their closest relatives in phylogenomic trees, rather supports scenarios based on the symbiosis of one Asgard-like archaeon and one or more bacteria at the origin of the eukaryotic cell. Here, we review the recent discoveries that led to this conceptual shift, briefly evoking current models of eukaryogenesis and the challenges ahead to discriminate between them and to establish a detailed, plausible scenario that accounts for the evolution of eukaryotic traits from those of their prokaryotic ancestors.
```
</details>

<details><summary>[3] **KEY** Origin of eukaryotic-like Vps23 shapes an ancient functional interplay between ESCRT and ubiquitin system in Asgard archaea. — Zhongyi Lu, Siyu Zhang, Yang Liu, Runyue Xia et al. (2024); cutoff-filter date 2024-02-14; doi:10.1016/j.celrep.2024.113781</summary>

```text
[3] Origin of eukaryotic-like Vps23 shapes an ancient functional interplay between ESCRT and ubiquitin system in Asgard archaea.
    id: s2:55a43731cbbe21dd1a001b68bb552cca6ab3f7e3
    date: 2024-02-01
    venue: Cell Reports
    authors: Zhongyi Lu, Siyu Zhang, Yang Liu, Runyue Xia, Meng Li
    abstract: Functional interplay between the endosomal sorting complexes required for transport (ESCRT) and the ubiquitin system underlies the ubiquitin-dependent cargo-sorting pathway of the eukaryotic endomembrane system, yet its evolutionary origin remains unclear. Here, we show that a UEV-Vps23 protein family, which contains UEV and Vps23 domains, mediates an ancient ESCRT and ubiquitin system interplay in Asgard archaea. The UEV binds ubiquitin with high affinity, making the UEV-Vps23 a sensor for sorting ubiquitinated cargo. A steadiness box in the Vps23 domain undergoes ubiquitination through an Asgard E1, E2, and RING E3 cascade. The UEV-Vps23 switches between autoinhibited and active forms, regulating the ESCRT and ubiquitin system interplay. Furthermore, the shared sequence and structural homology among the UEV-Vps23, eukaryotic Vps23, and archaeal CdvA suggest a common evolutionary origin. Together, this work expands our understanding of the ancient ESCRT and ubiquitin system interplay that likely arose antedating divergent evolution between Asgard archaea and eukaryotes.
    note: merged with 1 other version(s) of the same work
```
</details>

<details><summary>[4] **KEY** Arf family GTPases are present in Asgard archaea — Romana Vargová, Roxanne Chevreau, M. Alves, Camille Courbin et al. (2024); cutoff-filter date 2024-03-01; doi:10.1101/2024.02.28.582541</summary>

```text
[4] Arf family GTPases are present in Asgard archaea
    id: s2:3fd208ebadff884b05d9062d422bc38fea999d8e
    date: 2024-03-01
    venue: bioRxiv (preprint)
    authors: Romana Vargová, Roxanne Chevreau, M. Alves, Camille Courbin, Kara Terry, Pierre Legrand, Marek Eliáš, Julie Ménétrey
    abstract: The emergence of eukaryotes from their prokaryotic ancestors is one of the most fundamental evolutionary events in the history of life. Little is robustly known about how eukaryogenesis occurred, but a major breakthrough came with the identification of the Asgardarchaeota, the closest prokaryotic lineage to eukaryotes yet discovered. Endomembrane organelles, and the capacity to transport material between them, are major hallmarks of eukaryotic cells. The Arf family GTPases are crucial regulators of organelle dynamics in eukaryotes, functioning in vesicle budding, membrane tethering and membrane-cytoskeleton interactions. Although an expanded GTPase complement has been reported in the Asgardarchaeota, the specific origins of the Arf family remain elusive. Here we report a new group of prokaryotic GTPases, the ArfRs. Widely present in Asgardarchaeota and almost exclusive to them, it is the clade from which all eukaryotic Arf family proteins are derived. Heterologous expression of representative Asgardarchaeota ArfR proteins in the model eukaryote Saccharomyces cerevisiae and X-ray crystallographic studies demonstrate that ArfR GTPases possess the mechanism of membrane binding and structural features unique to Arf family proteins. Our results show that Arf family GTPases are present in Asgardarchaeota, and strongly suggest that they originated in the archaeal contributor to eukaryogenesis, providing support for nascent endomembrane system capacity evolving early in eukaryogenesis.
```
</details>

<details><summary>[5] Complete genomes of Asgard archaea reveal diverse integrated and mobile genetic elements — L. Valentin-Alvarado, Ling-Dong Shi, K. Appler, Alexander Crits-Christoph et al. (2024); cutoff-filter date 2024-10-15; doi:10.1101/gr.279480.124</summary>

```text
[5] Complete genomes of Asgard archaea reveal diverse integrated and mobile genetic elements
    id: s2:e6c1517d25f3fd63fe8c18daea997d100398e2d3
    date: 2024-10-01
    venue: Genome Research (preprint)
    authors: L. Valentin-Alvarado, Ling-Dong Shi, K. Appler, Alexander Crits-Christoph, V. de Anda, Benjamin A. Adler, Michael L. Cui, Lynn Ly
    abstract: Asgard archaea are of great interest as the progenitors of Eukaryotes, but little is known about the mobile genetic elements (MGEs) that may shape their ongoing evolution. Here, we describe MGEs that replicate in Atabeyarchaeia, a wetland Asgard archaea lineage represented by two complete genomes. We used soil depth–resolved population metagenomic data sets to track 18 MGEs for which genome structures were defined and precise chromosome integration sites could be identified for confident host linkage. Additionally, we identified a complete 20.67 kbp circular plasmid and two family-level groups of viruses linked to Atabeyarchaeia, via CRISPR spacer targeting. Closely related 40 kbp viruses possess a hypervariable genomic region encoding combinations of specific genes for small cysteine-rich proteins structurally similar to restriction-homing endonucleases. One 10.9 kbp integrative conjugative element (ICE) integrates genomically into the Atabeyarchaeum deiterrae-1 chromosome and has a 2.5 kbp circularizable element integrated within it. The 10.9 kbp ICE encodes an expressed Type IIG restriction-modification system with a sequence specificity matching an active methylation motif identified by Pacific Biosciences (PacBio) high-accuracy long-read (HiFi) metagenomic sequencing. Restriction-modification of Atabeyarchaeia differs from that of another coexisting Asgard archaea, Freyarchaeia, which has few identified MGEs but possesses diverse defense mechanisms, including DISARM and Hachiman, not found in Atabeyarchaeia. Overall, defense systems and methylation mechanisms of Asgard archaea likely modulate their interactions with MGEs, and integration/excision and copy number variation of MGEs in turn enable host genetic versatility.
```
</details>

<details><summary>[6] Genetic elements and defense systems drive diversification and evolution in Asgard archaea — L. Valentin-Alvarado, Ling-Dong Shi, K. Appler, Alexander Crits-Christoph et al. (2024); cutoff-filter date 2024-03-23; doi:10.1101/2024.03.22.586370</summary>

```text
[6] Genetic elements and defense systems drive diversification and evolution in Asgard archaea
    id: s2:703b9d3f624e80434597ed11069c47cdaf2dad25
    date: 2024-03-23
    venue: bioRxiv (preprint)
    authors: L. Valentin-Alvarado, Ling-Dong Shi, K. Appler, Alexander Crits-Christoph, Michael L. Cui, V. de Anda, Pedro Leão, Benjamin A. Adler
    abstract: [no abstract available]
```
</details>

<details><summary>[7] Potential for mercury methylation by Asgard archaea in mangrove sediments — Cuijing Zhang, Yu-Rong Liu, G. Cha, Yang Liu et al. (2023); cutoff-filter date 2023-01-13; doi:10.1038/s41396-023-01360-w</summary>

```text
[7] Potential for mercury methylation by Asgard archaea in mangrove sediments
    id: s2:30c1ff357052476c09b0ce28df3a76bd73c186c9
    date: 2023-01-13
    venue: The ISME Journal
    authors: Cuijing Zhang, Yu-Rong Liu, G. Cha, Yang Liu, Xin-Quan Zhou, Zhongyi Lu, Jie Pan, Mingwei Cai
    abstract: [no abstract available]
```
</details>

<details><summary>[8] Asgard archaea modulate potential methanogenesis substrates in wetland soil — L. Valentin-Alvarado, K. Appler, V. de Anda, M. C. Schoelmerich et al. (2023); cutoff-filter date 2024-07-31; doi:10.1038/s41467-024-49872-z</summary>

```text
[8] Asgard archaea modulate potential methanogenesis substrates in wetland soil
    id: s2:fe1d4f8116010838a66644fefd1a3aa3517e8126
    date: 2023-11-22
    venue: bioRxiv (preprint)
    authors: L. Valentin-Alvarado, K. Appler, V. de Anda, M. C. Schoelmerich, Jacob West-Roberts, Veronika Kivenson, A. Crits-Christoph, Lynn Ly
    abstract: The roles of Asgard archaea in eukaryogenesis and marine biogeochemical cycles are well studied, yet their contributions in soil ecosystems are unknown. Of particular interest are Asgard archaeal contributions to methane cycling in wetland soils. To investigate this, we reconstructed two complete genomes for soil-associated Atabeyarchaeia, a new Asgard lineage, and the first complete genome of Freyarchaeia, and defined their metabolism in situ. Metatranscriptomics highlights high expression of [NiFe]-hydrogenases, pyruvate oxidation and carbon fixation via the Wood-Ljungdahl pathway genes. Also highly expressed are genes encoding enzymes for amino acid metabolism, anaerobic aldehyde oxidation, hydrogen peroxide detoxification and glycerol and carbohydrate breakdown to acetate and formate. Overall, soil-associated Asgard archaea are predicted to be non-methanogenic acetogens, likely impacting reservoirs of substrates for methane production in terrestrial ecosystems. One-Sentence Summary Complete genomes of Asgard archaea, coupled with metatranscriptomic data, indicate roles in production and consumption of carbon compounds that are known to serve as substrates for methane production in wetlands.
```
</details>

<details><summary>[9] Ribosomal Protein Cluster Organization in Asgard Archaea — M. Tirumalai, R. Sivaraman, Layla A. Kutty, Eric L Song et al. (2023); cutoff-filter date 2023-09-29; doi:10.1155/2023/5512414</summary>

```text
[9] Ribosomal Protein Cluster Organization in Asgard Archaea
    id: s2:69d7c8666f34b698cdd937c6af0d0a34372ba5bc
    date: 2023-09-29
    venue: Archaea
    authors: M. Tirumalai, R. Sivaraman, Layla A. Kutty, Eric L Song, George E. Fox
    abstract: It has been proposed that the superphylum of Asgard Archaea may represent a historical link between the Archaea and Eukarya. Following the discovery of the Archaea, it was soon appreciated that archaeal ribosomes were more similar to those of Eukarya rather than Bacteria. Coupled with other eukaryotic-like features, it has been suggested that the Asgard Archaea may be directly linked to eukaryotes. However, the genomes of Bacteria and non-Asgard Archaea generally organize ribosome-related genes into clusters that likely function as operons. In contrast, eukaryotes typically do not employ an operon strategy. To gain further insight into conservation of the r-protein genes, the genome order of conserved ribosomal protein (r-protein) coding genes was identified in 17 Asgard genomes (thirteen complete genomes and four genomes with less than 20 contigs) and compared with those found previously in non-Asgard archaeal and bacterial genomes. A universal core of two clusters of 14 and 4 cooccurring r-proteins, respectively, was identified in both the Asgard and non-Asgard Archaea. The equivalent genes in the E. coli version of the cluster are found in the S10 and spc operons. The large cluster of 14 r-protein genes (uS19-uL22-uS3-uL29-uS17 from the S10 operon and uL14-uL24-uL5-uS14-uS8-uL6-uL18-uS5-uL30-uL15 from the spc operon) occurs as a complete set in the genomes of thirteen Asgard genomes (five Lokiarchaeotes, three Heimdallarchaeotes, one Odinarchaeote, and four Thorarchaeotes). Four less conserved clusters with partial bacterial equivalents were found in the Asgard. These were the L30e (str operon in Bacteria) cluster, the L18e (alpha operon in Bacteria) cluster, the S24e-S27ae-rpoE1 cluster, and the L31e, L12..L1 cluster. Finally, a new cluster referred to as L7ae was identified. In many cases, r-protein gene clusters/operons are less conserved in their organization in the Asgard group than in other Archaea. If this is generally true for nonribosomal gene clusters, [...]
```
</details>

<details><summary>[10] Promethearchaeum syntrophicum gen. nov., sp. nov., an anaerobic, obligately syntrophic archaeon, the first isolate of the lineage ‘Asgard’ archaea, and proposal of the new archaeal phylum Promethearchaeota phyl. nov. and kingdom Promethearchaeati regn. nov. — H. Imachi, M. Nobu, Shingo Kato, Y. Takaki et al. (2024); cutoff-filter date 2024-07-05; doi:10.1099/ijsem.0.006435</summary>

```text
[10] Promethearchaeum syntrophicum gen. nov., sp. nov., an anaerobic, obligately syntrophic archaeon, the first isolate of the lineage ‘Asgard’ archaea, and proposal of the new archaeal phylum Promethearchaeota phyl. nov. and kingdom Promethearchaeati regn. nov.
    id: s2:547db19c1375763548b72637119b8e49b9ca4323
    date: 2024-07-01
    venue: International Journal of Systematic and Evolutionary Microbiology
    authors: H. Imachi, M. Nobu, Shingo Kato, Y. Takaki, M. Miyazaki, Makoto Miyata, Miyuki Ogawara, Yumi Saito
    abstract: Abstract An anaerobic, mesophilic, syntrophic, archaeon strain MK-D1T, was isolated as a pure co-culture with Methanogenium sp. strain MK-MG from deep-sea methane seep sediment. This organism is, to our knowledge, the first cultured representative of ‘Asgard’ archaea, an archaeal group closely related to eukaryotes. Here, we describe the detailed physiology and phylogeny of MK-D1T and propose Promethearchaeum syntrophicum gen. nov., sp. nov. to accommodate this strain. Cells were non-motile, small cocci, approximately 300–750 nm in diameter and produced membrane vesicles, chains of blebs and membrane-based protrusions. MK-D1T grew at 4–30 °C with optimum growth at 20 °C. The strain grew chemoorganotrophically with amino acids, peptides and yeast extract with obligate dependence on syntrophy with H2-/formate-utilizing organisms. MK-D1T showed the fastest growth and highest maximum cell yield when grown with yeast extract as the substrate: approximately 3 months to full growth, reaching up to 6.7×106 16S rRNA gene copies ml−1. MK-D1T had a circular 4.32 Mb chromosome with a DNA G+C content of 31.1 mol%. The results of phylogenetic analyses of the 16S rRNA gene and conserved marker proteins indicated that the strain is affiliated with ‘Asgard’ archaea and more specifically DHVC1/DSAG/MBG-B and ‘Lokiarchaeota’/‘Lokiarchaeia’. On the basis of the results of 16S rRNA gene sequence analysis, the most closely related isolated relatives were Infirmifilum lucidum 3507LTT (76.09 %) and Methanothermobacter tenebrarum RMAST (77.45 %) and the closest relative in enrichment culture was Candidatus ‘Lokiarchaeum ossiferum’ (95.39 %). The type strain of the type species is MK-D1T (JCM 39240T and JAMSTEC no. 115508). We propose the associated family, order, class, phylum, and kingdom as Promethearchaeaceae fam. nov., Promethearchaeales ord. nov., Promethearchaeia class. nov., Promethearchaeota phyl. nov., and Promethearchaeati regn. nov., respectively. These are in accordance with ICN [...]
```
</details>

<details><summary>Post-hoc automated audit — NON-AUTHORITATIVE; uses hidden benchmark annotations</summary>

- primary auditor: `reference_discriminator_recovered`; statuses {'H1': 'negative_or_absent', 'H2': 'positive_or_present'}; discriminative=True
- primary reasoning: H1 predicts that major eukaryote-specific systems, including endomembrane complexity, should arise after mitochondrial acquisition, so Asgard archaea (pre-mitochondrial) should lack these homologs. H2 predicts substantial cellular complexity, including endomembrane systems, evolved before mitochondrial acquisition, so Asgard archaea should contain these homologs.
- matched hidden reference discriminator: Relative timing of pre-LECA duplications associated with cytoskeleton, membrane trafficking, endomembranes, phagocytosis, and nucleus versus mitochondrial acquisition.
- derived opposition call: `genuine`
- evidence attribution: `informative_evidence_found` — The retrieved papers directly address the proposition, with multiple studies reporting the presence of eukaryotic endomembrane system gene homologs (e.g., ESCRT components, Arf GTPases) in Asgard archaeal genomes. The assessor correctly identified and used this evidence, and the queries were appropriate for surfacing such literature. The process worked as intended.
- second rater (LLM, blind): statuses {'H1': 'indeterminate', 'H2': 'positive_or_present'}; discriminative=False (None confidence) — Asgard ESP homologs: H2 predicts; mito-early is compatible with archaeal precursor genes
- disagreement flags: {'second_rater_vs_primary_discriminative': True, 'second_rater_vs_primary_status': True, 'retest_vs_primary_category': None, 'any': True}
</details>

**Human review** — `generic_component_fact` · reviewer: Research Director · source: D045 · status: `first_pass_model_based_review` · genuinely discriminative: False · silence-as-null error: False · other fields not recorded

---

## #31 · `GP1-forest_fragmentation_resilience-X23`

**GP1-forest_fragmentation_resilience-X23** — case `forest_fragmentation_resilience`, node `X23`

> Fragmentation reduces the ability of forest vegetation to maintain physiological function under drought conditions.

- generated from **H1** (Candidate B); abstraction: `mechanistic`
- generator's stated reason: If fragmented forests are less resistant to heat and drought, then the mechanism underlying this is impaired physiological resilience in vegetation due to fragmentation.
- influence: **0.216** (rank 5 in case, 31 overall; cumulative 70%) — favours **H1**
- log-likelihood contribution: H2 +0.976, H1 +1.192
- removing it alone: evidence withheld → case log-odds -1.415 (ranking unchanged); node deleted → -1.415 (ranking unchanged)

**Hypotheses (as shown to the verifier)**

- **H1** (Candidate B): Fragmentation increases exposure to heat, atmospheric dryness, wind, and drought stress, raising mortality and reducing ecosystem resilience, especially where water/heat stress dominates.
- **H2** (Candidate A): Edge formation can increase light availability and relax limiting-resource constraints, increasing growth, biomass, recovery capacity, and potentially resilience where climatic stress penalties are small enough.

**Verifier cross-hypothesis judgments** — P(X|H) combines these by noisy-OR

| hypothesis | origin? | direct edge | route via parent | P(X\|H) |
| --- | --- | --- | --- | --- |
| H2 | no | `unlikely` | X6 [H→parent `unlikely`, P=0.30] → `implied` | 0.713 |
| H1 | yes | `strongly_implied` | X6 [H→parent `strongly_implied`, P=0.95] → `implied` | 0.989 |

- edge rationale, **H2** → node: Candidate A suggests that fragmentation can increase growth, recovery, and resilience under certain conditions, implying that fragmentation does not generally reduce physiological function under drought.
- edge rationale, **H1** → node: Candidate B directly states that fragmentation increases drought stress and reduces ecosystem resilience, making it nearly certain that fragmentation reduces physiological function under drought.
- parent `X6`: Forests experiencing fragmentation are more likely to show decreased resistance to heat and drought stress compared to contiguous forests.
- chain rationale, `X6` → node: The parent proposition suggests that fragmentation decreases resistance to drought stress, which implies reduced physiological function under such conditions, though it does not state this mechanism explicitly.

**Verifier evidence** — label used in score: `support` (log-LR +1.2)

- queries: `forest fragmentation vegetation physiological function`; `forest drought fragmentation plant water stress`
- assessor rationale: Record [2] directly states that fragmentation reduces ecosystem resistance and resilience, and that less fragmented forests have higher vitality under extreme heat, which is consistent with reduced physiological function under drought. Record [10] also directly links fragmentation to negative effects on rare forest communities, including their ability to recover in specific ecological conditions. These statements bear directly on the proposition, though they do not provide detailed physiological measurements, so the support is not strong.
- supporting spans cited by the assessor:
  - "Forest fragmentation not only poses a threat to many organisms but also reduces the resistance and resilience of the ecosystem, which is especially relevant to the ongoing climate crisis."
  - "In 2022, larger intact tree-covered areas that are less fragmented have relatively low temperatures on hot days and higher overall vitality."
  - "Currently, rare forest communities are most negatively affected due to the complete loss or fragmentation of habitats, pollution, overexploitation of species and ecosystems, competition from populations of adventive species, global climate change and unbalanced development of forestry, military actions."
- 10 papers shown; key papers: `s2:07778da86b890efd5cff406830d1fb6ccb538470`, `s2:95bb870f1723b10ed652f92639d09635d1a1f22c`
- _The evidence assessor returns ONE label for the node from all papers shown; the method has no per-paper contribution. Key papers and spans are those the assessor cited._

<details><summary>[1] Edaphic, structural and physiological contrasts across Amazon Basin forest-savanna ecotones suggest a role for potassium as a key modulator of tropical woody vegetation structure and function — J. Lloyd, T. Domingues, F. Schrodt, F. Y. Ishida et al. (2015); cutoff-filter date 2015-11-18; doi:10.5194/bg-12-6529-2015</summary>

```text
[1] Edaphic, structural and physiological contrasts across Amazon Basin forest-savanna ecotones suggest a role for potassium as a key modulator of tropical woody vegetation structure and function
    id: s2:c72d6fcfe60eab4083bf0b1aaeb876bc22e7b5b2
    date: 2015-11-18
    venue: Biogeosciences
    authors: J. Lloyd, T. Domingues, F. Schrodt, F. Y. Ishida, T. Feldpausch, G. Saiz, C. Quesada, M. Schwarz
    abstract: Abstract. Sampling along a precipitation gradient in tropical South America extending from ca. 0.8 to 2.0 m a−1, savanna soils had consistently lower exchangeable cation concentrations and higher C / N ratios than nearby forest plots. These soil differences were also reflected in canopy averaged leaf traits with savanna trees typically having higher leaf mass per unit area but lower mass-based nitrogen (Nm) and potassium (Km). Both Nm and Km also increased with declining mean annual precipitation (PA), but most area-based leaf traits such as leaf photosynthetic capacity showed no systematic variation with PA or vegetation type. Despite this invariance, when taken in conjunction with other measures such as mean canopy height, area-based soil exchangeable potassium content, [K]sa , proved to be an excellent predictor of several photosynthetic properties (including 13C isotope discrimination). Moreover, when considered in a multivariate context with PA and soil plant available water storage capacity (θP) as covariates, [K]sa also proved to be an excellent predictor of stand-level canopy area, providing drastically improved fits as compared to models considering just PA and/or θP. Neither calcium, nor magnesium, nor soil pH could substitute for potassium when tested as alternative model predictors (ΔAIC > 10). Nor for any model could simple soil texture metrics such as sand or clay content substitute for either [K]sa or θP. Taken in conjunction with recent work in Africa and the forests of the Amazon Basin, this suggests – in combination with some newly conceptualised interacting effects of PA and θP also presented here – a critical role for potassium as a modulator of tropical vegetation structure and function.
```
</details>

<details><summary>[2] **KEY** Does fragmentation contribute to the forest crisis in Germany? — Deepika Mann, C. Gohr, Jeanette S. Blumröder, P. Ibisch (2023); cutoff-filter date 2023-01-20; doi:10.3389/ffgc.2023.1099460</summary>

```text
[2] Does fragmentation contribute to the forest crisis in Germany?
    id: s2:95bb870f1723b10ed652f92639d09635d1a1f22c
    date: 2023-01-20
    venue: Frontiers in Forests and Global Change
    authors: Deepika Mann, C. Gohr, Jeanette S. Blumröder, P. Ibisch
    abstract: Intact forests contribute to the ecosystem functionality of landscapes by storing and sequestering carbon, buffering and cooling the microclimate, and providing a range of related ecosystem functions. Forest fragmentation not only poses a threat to many organisms but also reduces the resistance and resilience of the ecosystem, which is especially relevant to the ongoing climate crisis. The effects of recent extreme heat years on forests in Germany have not been studied in detail for the influence of fragmentation. We investigate the relation of forest fragmentation with temperature and vitality in Germany per ecoregion at the canopy level using satellite imagery at 1-km and 30-m resolution. We compiled and correlated forest maps for connectivity based on Thiessen polygons, canopy temperatures on the hottest days based on land surface temperature, and forest vitality based on the maximum normalized difference vegetation index per growing season. We differentiated between ecoregions and main forest types. In 2022, larger intact tree-covered areas that are less fragmented have relatively low temperatures on hot days and higher overall vitality. Nearly 98% of the almost 1.95 million forest fragments at 30-m resolution in Germany are smaller than 1 km2, which cover nearly 30% of the total forest area. To counteract the forest crisis, forest and landscape management should aim to reduce fragmentation and maintain tree biomass and forest cover in the landscape. Increasing the size of continuous forest fragments contributes to ecosystem-based adaptation to climate change.
```
</details>

<details><summary>[3] Forests for forests: combining vegetation indices with solar-induced chlorophyll fluorescence in random forest models improves gross primary productivity prediction in the boreal forest — Z. Pierrat, J. Bortnik, Bruce Johnson, A. Barr et al. (2022); cutoff-filter date 2022-11-24; doi:10.1088/1748-9326/aca5a0</summary>

```text
[3] Forests for forests: combining vegetation indices with solar-induced chlorophyll fluorescence in random forest models improves gross primary productivity prediction in the boreal forest
    id: s2:c2505f9cd81d82009410f095c3640611ca2de739
    date: 2022-11-24
    venue: Environmental Research Letters
    authors: Z. Pierrat, J. Bortnik, Bruce Johnson, A. Barr, T. Magney, D. Bowling, N. Parazoo, C. Frankenberg
    abstract: Remote sensing is a powerful tool for understanding and scaling measurements of plant carbon uptake via photosynthesis, gross primary productivity (GPP), across space and time. The success of remote sensing measurements can be attributed to their ability to capture valuable information on plant structure (physical) and function (physiological), both of which impact GPP. However, no single remote sensing measure provides a universal constraint on GPP and the relationships between remote sensing measurements and GPP are often site specific, thereby limiting broader usefulness and neglecting important nuances in these signals. Improvements must be made in how we connect remotely sensed measurements to GPP, particularly in boreal ecosystems which have been traditionally challenging to study with remote sensing. In this paper we improve GPP prediction by using random forest models as a quantitative framework that incorporates physical and physiological information provided by solar-induced fluorescence (SIF) and vegetation indices (VIs). We analyze 2.5 years of tower-based remote sensing data (SIF and VIs) across two field locations at the northern and southern ends of the North American boreal forest. We find (a) remotely sensed products contain information relevant for understanding GPP dynamics, (b) random forest models capture quantitative SIF, GPP, and light availability relationships, and (c) combining SIF and VIs in a random forest model outperforms traditional parameterizations of GPP based on SIF alone. Our new method for predicting GPP based on SIF and VIs improves our ability to quantify terrestrial carbon exchange in boreal ecosystems and has the potential for applications in other biomes.
```
</details>

<details><summary>[4] FOREST BIOMASS AND CARBON ESTIMATION USING VEGETATION INDICES AND LEAF AREA INDEX — Daniele Arndt Erthal, F. Breunig, R. Balbinot, Paulo Afonso da Rosa (2022); cutoff-filter date 2022-07-19; doi:10.26848/rbgf.v15.4.p1815-1826</summary>

```text
[4] FOREST BIOMASS AND CARBON ESTIMATION USING VEGETATION INDICES AND LEAF AREA INDEX
    id: s2:cb288bdb25dda1b6b392913defdd349639923420
    date: 2022-07-19
    venue: Revista Brasileira de Geografia Física
    authors: Daniele Arndt Erthal, F. Breunig, R. Balbinot, Paulo Afonso da Rosa
    abstract: Among the consequences of the current dynamics of manmade land use and cover, forest fragmentation results in a large number of isolated fragments of different sizes. Forest provides many environmental services such as carbon sequestration and storage in the form of biomass, demonstrating the crucial role of native forests and the need to develop new methods that estimate forest biomass and carbon by non-destructive methods. This work aimed to develop a methodology to study and estimate the dynamics of forest biomass and carbon stock in successive stages of regeneration in the northwestern region of Rio Grande do Sul, which was the study area. Yearly images from 1985 to 2014 of the Normalized Difference Vegetation Index - NDVI were calculated, and a global regression was archived to obtain the leaf area index (LAI) and estimate the forest biomass. It was possible to observe the good relationship between the increase in LAI as a function of the NDVI, estimating the forest biomass of 61,156 Gg in 2014, where 602 Gg correspond to the initial regeneration stage, 8,287 Gg for the medium stage, and 52,267 Gg for the advanced stage of regeneration. The total estimated carbon for the study area in 2014 was 27,520 Gg CO2 of which 271 Gg were present in the initial stage, 3,729 Gg in the medium stage, and 23,520 Gg in the advanced stage of regeneration.
```
</details>

<details><summary>[5] Tree species identity outweighs the effects of tree species diversity and forest fragmentation on understorey diversity and composition — Stefanie R. E. de Groote, Irene M. van Schrojenstein Lantman, B. Sercu, D. Dekeukeleire et al. (2017); cutoff-filter date 2017-11-22; doi:10.5091/plecevo.2017.1331</summary>

```text
[5] Tree species identity outweighs the effects of tree species diversity and forest fragmentation on understorey diversity and composition
    id: s2:564c22bec97fe2952ea9e3f80ed441dd319bed0b
    date: 2017-11-22
    venue: Plant Ecology and Evolution
    authors: Stefanie R. E. de Groote, Irene M. van Schrojenstein Lantman, B. Sercu, D. Dekeukeleire, R. Boonyarittichaikij, H. K. Smith, Robbe De Beelde, Kris Ceunen
    abstract: Background & aim : In general, biodiversity has positive effects on ecosystem functioning. In forests, understorey vegetation is influenced by both the composition and species richness of the overstorey through species-specific effects on environmental conditions at the forest floor. Forest fragmentation is also known to influence understorey vegetation composition and richness. However, the combined effects of tree species diversity and forest fragmentation have not been studied yet. With the TREEWEB research platform, consisting of 53 forest plots along a tree species diversity and forest fragmentation gradient, we aim to unravel the combined effects of tree species diversity, tree species identity and forest fragmentation on the understorey composition and diversity. 
Methods : The TREEWEB platform includes forest plots of three tree species richness levels, containing all possible species combinations of Quercus robur, Quercus rubra and Fagus sylvatica. Complete dilution is avoided in the design, allowing separation between tree species identity and diversity effects. Vegetation surveys were conducted in all plots to investigate the species richness, species diversity, compositional turnover and cover of the herb layer as well as the shrub layer cover. 
Key results : Within the TREEWEB platform, overstorey-understorey diversity relationships were mainly characterised by tree species identity effects. No clear effects of tree species diversity and forest fragmentation on understorey composition and diversity were found. 
Conclusion : Tree species identity effects were most important in explaining the observed patterns in the understorey vegetation. Further in-depth research will allow us to disentangle which mechanisms underlie these patterns and whether effects of fragmentation are more pronounced at higher trophic levels.
```
</details>

<details><summary>[6] MEDFATE 2.9.3: a trait-enabled model to simulate Mediterranean forest function and dynamics at regional scales — M. de Cáceres, R. Molowny‐Horas, Antoine Cabon, J. Martínez-Vilalta et al. (2023); cutoff-filter date 2023-06-06; doi:10.5194/gmd-16-3165-2023</summary>

```text
[6] MEDFATE 2.9.3: a trait-enabled model to simulate Mediterranean forest function and dynamics at regional scales
    id: s2:d1319c5aa8650a529c35e89b96ea847d4b0673dd
    date: 2023-06-06
    venue: Geoscientific Model Development
    authors: M. de Cáceres, R. Molowny‐Horas, Antoine Cabon, J. Martínez-Vilalta, Maurizio Mencuccini, R. García‐Valdés, D. Nadal-Sala, S. Sabaté
    abstract: Abstract. Regional-level applications of dynamic vegetation models are challenging because they need to accommodate the variation in plant functional
diversity, which requires moving away from broadly defined functional types. Different approaches have been adopted in the last years to incorporate
a trait-based perspective into modeling exercises. A common parametrization strategy involves using trait data to represent functional variation
between individuals while discarding taxonomic identity. However, this strategy ignores the phylogenetic signal of trait variation and cannot be
employed when predictions for specific taxa are needed, such as in applications to inform forest management planning. An alternative strategy
involves adapting the taxonomic resolution of model entities to that of the data source employed for large-scale initialization and estimating
functional parameters from available plant trait databases, adopting diverse solutions for missing data and non-observable parameters. Here we
report the advantages and limitations of this second strategy according to our experience in the development of MEDFATE (version 2.9.3), a novel
cohort-based and trait-enabled model of forest dynamics, for its application over a region in the western Mediterranean Basin. First, 217 taxonomic
entities were defined according to woody species codes of the Spanish National Forest Inventory. While forest inventory records were used to obtain
some empirical parameter estimates, a large proportion of physiological, morphological, and anatomical parameters were matched to measured plant
traits, with estimates extracted from multiple databases and averaged at the required taxonomic level. Estimates for non-observable key parameters
were obtained using meta-modeling and calibration exercises. Missing values were addressed using imputation procedures based on trait covariation,
taxonomic averages or both. The model properly simulated observed historical changes in basal area, wit [...]
```
</details>

<details><summary>[7] Laboratory Investigations on the Effect of Fragmentation and Heterogeneity of Coastal Vegetation in Wave Height Attenuation — K. G. Shirlal, B. John, S. Rao (2018); cutoff-filter date 2018-12-31; doi:10.1007/978-981-13-3134-3_2</summary>

```text
[7] Laboratory Investigations on the Effect of Fragmentation and Heterogeneity of Coastal Vegetation in Wave Height Attenuation
    id: s2:58b3b903b9afd0bd6a1d463c77cddd5a2ba66ff1
    date: 2018-12-31
    venue: Lecture Notes in Civil Engineering
    authors: K. G. Shirlal, B. John, S. Rao
    abstract: [no abstract available]
```
</details>

<details><summary>[8] Impact of time on interpretations of forest fragmentation: Three-decades of fragmentation dynamics over Canada — T. Hermosilla, M. Wulder, J. White, N. Coops et al. (2019); cutoff-filter date 2019-03-01; doi:10.1016/j.rse.2018.12.027</summary>

```text
[8] Impact of time on interpretations of forest fragmentation: Three-decades of fragmentation dynamics over Canada
    id: s2:b09a0707249d6fbf0cac6f193ea1017d703cb8ec
    date: 2019-03-01
    venue: Remote Sensing of Environment
    authors: T. Hermosilla, M. Wulder, J. White, N. Coops, Paul D. Pickell, D. K. Bolton
    abstract: Abstract Measures of forest fragmentation, and how fragmentation is changing through time, offer required information for understanding the status and dynamics of forest ecosystems, habitat conditions, and ecosystem functions. In this research, we investigate the multi-temporal characterization of forest fragmentation across the forested ecosystems of Canada (>650 million ha) and characterize the past three decades of forest fragmentation, providing useful context against which future analyses can be compared. Using 33 years of annual land cover maps produced from classified Landsat image best-available pixel composites (1984–2016), we describe and quantify the different forest patterns and dynamics that emerged in areas that were not disturbed in the analysis period, as well as following stand-replacing (i.e., wildfire, harvest) and non-stand-replacing (e.g., insects, water stress) disturbances. Baseline levels of fragmentation for each ecozone were determined by analyzing unchanged areas. Fragmentation dynamics by dominant forest disturbance showed that harvest activities generally lead to an increase in fragmentation related to the amount of forest cover (composition), while wildfires result in increasing fragmentation as a function of the spatial arrangement of the forest. The results presented herein also allow for characterization of the recovery of vegetation spatial patterns following various disturbance types, with areas dominated by fire presenting slower spatial recovery rates compared to harvest. By the end of the analysis period following disturbance events, forest fragmentation metrics in harvest-dominated landscapes were comparable to the pre-harvesting baseline, reaching 96% of mean pre-disturbance levels for mean forest patch size, and 83% for number of forest patches. In contrast, fire-dominated landscapes resulted in more event related fragmentation, with reduced forest cover (mean Thiel Sen slope = −0.13% year−1), mean forest patch size (−0.22 ha [...]
```
</details>

<details><summary>[9] Wild or tended nature? The effects of landscape location and vegetation density on physiological and psychological responses — Y. Chiang, Dongying Li, Hao-ann Jane (2017); cutoff-filter date 2017-11-01; doi:10.1016/j.landurbplan.2017.06.001</summary>

```text
[9] Wild or tended nature? The effects of landscape location and vegetation density on physiological and psychological responses
    id: s2:0a83bef6efcf3a55de298063f6fca6f039cb3ad5
    date: 2017-11-01
    venue: Landscape and Urban Planning
    authors: Y. Chiang, Dongying Li, Hao-ann Jane
    abstract: [no abstract available]
```
</details>

<details><summary>[10] **KEY** Rare diversity of forest vegetation of the steppe zone: current state, threats and directions of changes — P. Ustymenko, D. Dubyna, B. O. Baranovskyi, A. Zhykharieva (2022); cutoff-filter date 2022-09-28; doi:10.15421/032209</summary>

```text
[10] Rare diversity of forest vegetation of the steppe zone: current state, threats and directions of changes
    id: s2:07778da86b890efd5cff406830d1fb6ccb538470
    date: 2022-09-28
    venue: Ecology and Noospherology
    authors: P. Ustymenko, D. Dubyna, B. O. Baranovskyi, A. Zhykharieva
    abstract: Under the action of various forms of human activity, there was a violation of the integrity and unity of the vegetation cover of the steppe zone of Ukraine. The consequence of this is the fragmentation of vegetation. It was established that the decrease in the area of plant communities leads to an increase in their dependence on environmental factors. An important component of the phytocoenotic cover, and first of all the forest cover, which is the biotic basis of the functioning of the biosphere, its evolution and maintenance of an ecologically balanced state, is a rare phytocoenofund. The purpose of the work was to compile information on the current state of rare groups in the steppe zone using data from ecological and coenotic studies, sociological analysis and assessment of the latest threats to rare forest diversity. A critical analysis of the current rare phytocenophyte, the data of modern synphytosozological studies and the latest geobotanical information on the rare phytocenotic diversity made it possible to establish a modern rare phytocenophyte of the forests of the steppe zone of Ukraine. It has 16 associations of three formations. The sociological analysis showed that all phytocoenoses of 16 rare forest associations are characterized by a rare type of association, are located on the border of the range, and 5 associations are formed by an endemic species. According to their sociological status, they are divided into rare (4 associations) and endangered species (12 associations). The potential for natural recovery of populations of dominant species of groups in specific ecological conditions is very weak or weak in all 16 rare forest associations. Currently, rare forest communities are most negatively affected due to the complete loss or fragmentation of habitats, pollution, overexploitation of species and ecosystems, competition from populations of adventive species, global climate change and unbalanced development of forestry, military actions.
```
</details>

<details><summary>Post-hoc automated audit — NON-AUTHORITATIVE; uses hidden benchmark annotations</summary>

- primary auditor: `silence_as_null_error`; statuses {'H1': 'positive_or_present', 'H2': 'indeterminate'}; discriminative=False
- primary reasoning: H1 explicitly predicts that fragmentation increases exposure to heat and drought stress, reducing vegetation resilience, so it implies fragmentation impairs physiological function under drought. H2 is silent on drought resistance; it focuses on increased light and resource availability, not physiological drought resilience, so it makes no commitment either way.
- derived opposition call: `manufactured_from_silence`
- evidence attribution: `generic_compatibility_only` — The papers retrieved are topically related to forest fragmentation, ecosystem function, and resilience under stress, but they do not directly test or measure the physiological function of forest vegetation under drought as affected by fragmentation. The assessor treated general statements about ecosystem resistance and vitality as support, but these do not constitute direct evidence for the specific physiological mechanism in the proposition.
- disagreement flags: {'second_rater_vs_primary_discriminative': None, 'second_rater_vs_primary_status': None, 'retest_vs_primary_category': None, 'any': False}
</details>

**Human review** — `silence_as_null_error` · reviewer: Research Director · source: D045 · status: `first_pass_model_based_review` · genuinely discriminative: False · silence-as-null error: True · other fields not recorded

---

## #32 · `GP1-spider_orb_web_origin-X12`

**GP1-spider_orb_web_origin-X12** — case `spider_orb_web_origin`, node `X12`

> Convergent evolution of complex behaviors such as orb-weaving is possible within the spider family Araneidae and related families.

- generated from **H2** (Candidate B); abstraction: `class`
- generator's stated reason: The claim suggests that distantly related spiders can independently evolve orb-weaving behavior without shared gene expression patterns, supporting the possibility of convergent evolution in these families.
- influence: **0.215** (rank 1 in case, 32 overall; cumulative 72%) — favours **H2**
- log-likelihood contribution: H1 +0.976, H2 +1.191
- removing it alone: evidence withheld → case log-odds -0.091 (ranking unchanged); node deleted → -0.091 (ranking unchanged)

**Hypotheses (as shown to the verifier)**

- **H1** (Candidate A): Orb-weaving evolved in an ancient common ancestor; descendant non-orb-weaving lineages repeatedly lost orb-associated traits and molecular functions.
- **H2** (Candidate B): Cribellate and ecribellate orb webs arose independently/repeatedly in separate lineages through convergent evolution.

**Verifier cross-hypothesis judgments** — P(X|H) combines these by noisy-OR

| hypothesis | origin? | direct edge | route via parent | P(X\|H) |
| --- | --- | --- | --- | --- |
| H1 | no | `unlikely` | X4 [H→parent `unlikely`, P=0.30] → `implied` | 0.713 |
| H2 | yes | `strongly_implied` | X4 [H→parent `implied`, P=0.80] → `implied` | 0.987 |

- edge rationale, **H1** → node: If orb-weaving evolved only once in a common ancestor and was lost in some lineages, this suggests complex orb-weaving behaviors are not convergently evolved within Araneidae and related families.
- edge rationale, **H2** → node: If cribellate and ecribellate orb webs arose independently in separate lineages, this directly supports the possibility of convergent evolution of complex behaviors like orb-weaving within these spider families.
- parent `X4`: Orb-weaving behavior in cribellate spiders is not associated with homologous web-building gene expression patterns found in ecribellate orb-weaving spiders.
- chain rationale, `X4` → node: If orb-weaving behavior in cribellate spiders is not associated with homologous gene expression patterns found in ecribellate orb-weaving spiders, this suggests that similar behaviors may have evolved independently, supporting the possibility of convergent evolution.

**Verifier evidence** — label used in score: `support` (log-LR +1.2)

- queries: `Araneidae orb-weaving behavior evolution`; `spider families complex behavior phylogeny`
- assessor rationale: Record [4] directly states that convergent evolution has been common in orb-weaving spiders’ webs, and describes independent origins of complex web structures in different groups within Araneidae. This is direct evidence that complex behaviors such as orb-weaving can evolve convergently within Araneidae and related families. No other records directly address the proposition, and the evidence comes from a single independent study.
- supporting spans cited by the assessor:
  - "Convergence has been common in the evolution of orb-weaving spiders’ webs, and structures such as stabilimenta, reduced orbs, spring lines, meshes at the side of the orb, and asymmetrically extended "ladder webs" have arisen independently in a number of different groups. This paper describes brief observations of Eustala sp. that demonstrate still another apparent convergence that is perhaps more surprising than some of the others since the adaptive advantage of the convergent design is at first glance unclear."
- 10 papers shown; key papers: `s2:15ff40db2aeb8e43d65146ca92a30dd00f782a06`
- _The evidence assessor returns ONE label for the node from all papers shown; the method has no per-paper contribution. Key papers and spans are those the assessor cited._

<details><summary>[1] Cyclosa Menge, 1866 (Araneidae) Orb‐Weavers Build Stabilimenta That Resemble Larger Spiders — G. Olah, Phillip J. Torres, A. Pomerantz, R. Kirby et al. (2025); cutoff-filter date 2025-11-06; doi:10.1002/ece3.72371</summary>

```text
[1] Cyclosa Menge, 1866 (Araneidae) Orb‐Weavers Build Stabilimenta That Resemble Larger Spiders
    id: s2:cc79c1b72588a399467e4a97f5d24fbd72d75944
    date: 2025-11-01
    venue: Ecology and Evolution
    authors: G. Olah, Phillip J. Torres, A. Pomerantz, R. Kirby, S. Baxter, Juan Grados, Lawrence E. Reeves
    abstract: ABSTRACT Orb‐weaving spiders are known to create stabilimenta—silk situated at particular locations of the web. While anecdotal reports and popular media have long suggested that some spiders arrange debris in their webs to resemble a larger spider, this behavior has not been formally documented in the scientific literature. Here, we provide the first scientific record of this unique behavior in two orb‐weaving spiders (Cyclosa spp., Araneidae) from the tropical forests of Peru and the Philippines. We report that these spiders construct stabilimenta composed of detritus and silk, arranging the debris in the web into a shape that visually resembles the silhouette of a larger spider. This structure may serve as a “decoy” that serves an anti‐predator function of misdirecting or repelling the attacks of some predators. Video abstract: https://youtu.be/GDySHFRXbCE.
```
</details>

<details><summary>[2] SEXUAL CANNIBALISM, SIZE DIMORPHISM, AND COURTSHIP BEHAVIOR IN ORB‐WEAVING SPIDERS (ARANEIDAE) — M. Elgar (1991); cutoff-filter date 1991-03-31; doi:10.1111/j.1558-5646.1991.tb04419.x</summary>

```text
[2] SEXUAL CANNIBALISM, SIZE DIMORPHISM, AND COURTSHIP BEHAVIOR IN ORB‐WEAVING SPIDERS (ARANEIDAE)
    id: s2:f4edf9a801c9b78b6abf0db623f375382a63581c
    date: 1991-03-01
    venue: Evolution; international journal of organic evolution
    authors: M. Elgar
    abstract: [no abstract available]
```
</details>

<details><summary>[3] A review of the taxonomy of spiny-backed orb-weaving spiders of the subfamily Gasteracanthinae (Araneae, Araneidae) in Thailand — Kongkit Macharoenboon, Warut Siriwut, Ekgachai Jeratthitikul (2021); cutoff-filter date 2021-04-16; doi:10.3897/zookeys.1032.62001</summary>

```text
[3] A review of the taxonomy of spiny-backed orb-weaving spiders of the subfamily Gasteracanthinae (Araneae, Araneidae) in Thailand
    id: s2:aa15c2bc1895618271ff4d3af4ffb3f920c69a4d
    date: 2021-04-16
    venue: ZooKeys
    authors: Kongkit Macharoenboon, Warut Siriwut, Ekgachai Jeratthitikul
    abstract: Abstract Spiny-backed orb-weaving spiders of the subfamily Gasteracanthinae are broadly distributed in the Old World. Despite their use as a model species in biology, evolution, and behavior because of their extraordinary characteristics, the systematics of this group of spiders are still poorly understood. This study elucidates the systematics of Gasteracanthinae in Thailand based on morphological and molecular-based analyses. In total, seven species from three genera, namely Gasteracantha, Macracantha, and Thelacantha, were recorded in Thailand. Shape of abdominal spines, pattern of sigilla, and female genitalia are significant characters for species identification. In contrast, coloration shows highly intraspecific variation in most species within Gasteracanthinae. A phylogenetic tree based on partial sequences of COI, 16S, and H3 genes recovered Gasteracanthinae as a monophyletic group and supports the existence of three clades. Gasteracantha hasselti is placed as a sister taxon to Macracantha arcuata. Hence, we propose to transfer G. hasselti to Macracantha. Moreover, molecular species delimitation analyses (ABGD, bPTP, and GMYC) using 675 bp of COI gene support all nominal species, with evidence of possible additional cryptic species.
```
</details>

<details><summary>[4] **KEY** The “Sawtoothed” Orb Web of Eustala Sp. (Araneae, Araneidae) with a Discussion of Ontogenetic Changes in Spiders' Web-Building Behavior — W. Eberhard (1985); cutoff-filter date 1985-12-31; doi:10.1155/1985/37460</summary>

```text
[4] The “Sawtoothed” Orb Web of Eustala Sp. (Araneae, Araneidae) with a Discussion of Ontogenetic Changes in Spiders' Web-Building Behavior
    id: s2:15ff40db2aeb8e43d65146ca92a30dd00f782a06
    date: 1985
    venue: Psyche
    authors: W. Eberhard
    abstract: Convergence has been common in the evolution of orb-weaving spiders’ webs, and structures such as stabilimenta, reduced orbs, spring lines, meshes at the side of the orb, and asymmetrically extended "ladder webs" have arisen independently in a number of different groups. This paper describes brief observations of Eustala sp. that demonstrate still another apparent convergence that is perhaps more surprising than some of the others since the adaptive advantage of the convergent design is at first glance unclear. Ontogenetic changes in web design are also documented for Eustala sp.; younger individuals make more generalized or less derived webs than those of adults. Data on ontogenetic changes in the web forms of other spider species are summarized, and it is shown that this is a common ontogenetic pattern in spiders. The possible significance of this evolutionary pattern is discussed. Observations were made in February 1984 in Parque Nacional Corcovado on the Osa Peninsula of Costa Rica in second growth along a small stream near the Sirena station. Webs of six large nymphs and adult females and of two very young nymphs were observed. The construction of three of these webs was observed between 7 and I1 PM. Spiders were kindly identified by H. W. Levi. They apparently represent an undescribed species; voucher specimens (#2345, SAI-127b, and SAE-106) have been deposited in the Museum of Comparative Zoology in Cambridge, Mass. 02138, U.S.A.
```
</details>

<details><summary>[5] The natural history of the Australian garden orb-weaving spiders Hortophora biapicata and H. transmarina (Araneae: Araneidae) — Nikolas J. Willmott (2025); cutoff-filter date 2025-01-05; doi:10.1636/joa-s-22-061</summary>

```text
[5] The natural history of the Australian garden orb-weaving spiders Hortophora biapicata and H. transmarina (Araneae: Araneidae)
    id: s2:8bd91d541535f9b00f328de47cb5cfa2f248d06c
    date: 2025-01-05
    venue: The journal of arachnology
    authors: Nikolas J. Willmott
    abstract: Abstract. Australia is home to an incredible diversity of spiders, but much of their biology remains unstudied. The orb-weaving spiders (family Araneidae) are especially diverse and frequently encountered, yet the ecology of very few species has been explored. The common name “Australian garden orb-weaver” refers to several species, including Hortophora transmarina (Keyserling, 1865), found mostly along Australia's east coast, and Hortophora biapicata (L Koch, 1871), found mostly along Australia's south and south-eastern coasts. These two similar species are large, nocturnal orb-weavers that occupy a wide range of both natural and anthropogenically disturbed habitats. Here, I describe the general morphology, habitat use, diet and foraging behavior, key predators, laboratory rearing, and mating dynamics of these common but understudied spiders. This information was gathered via field observations, laboratory experiments, and literature reviews. These spiders provide a useful system for studying a number of aspects of spider biology, including mating systems, predation, anti-predator defences, and nocturnal behaviors.
```
</details>

<details><summary>[6] Figure 2 from: Framenau VW, Vink CJ, Scharff N, Baptista RLC, Castanheira PS (2021) Review of the Australian and New Zealand orb-weaving spider genus Novakiella (Araneae, Araneidae). Zoosystematics and Evolution 97(2): 393-405. https://doi.org/10.3897/zse.97.67788 — V. Framenau, C. Vink, N. Scharff, R. Baptista et al. (2021); cutoff-filter date 2021-07-26; doi:10.3897/zse.97.67788.figure2</summary>

```text
[6] Figure 2 from: Framenau VW, Vink CJ, Scharff N, Baptista RLC, Castanheira PS (2021) Review of the Australian and New Zealand orb-weaving spider genus Novakiella (Araneae, Araneidae). Zoosystematics and Evolution 97(2): 393-405. https://doi.org/10.3897/zse.97.67788
    id: s2:c00f751981ce9061cd3d693121f90076ef834fde
    date: 2021-07-26
    venue: unknown
    authors: V. Framenau, C. Vink, N. Scharff, R. Baptista, Pedro de S. Castanheira
    abstract: [no abstract available]
    note: merged with 7 other version(s) of the same work
```
</details>

<details><summary>[7] Systematics, phylogeny and biogeography of the Australasian leaf-curling orb-weaving spiders (Araneae: Araneidae: Zygiellinae), with a comparative analysis of retreat evolution — R. Kallal, G. Hormiga (2018); cutoff-filter date 2018-06-05; doi:10.1093/zoolinnean/zly014</summary>

```text
[7] Systematics, phylogeny and biogeography of the Australasian leaf-curling orb-weaving spiders (Araneae: Araneidae: Zygiellinae), with a comparative analysis of retreat evolution
    id: s2:82e2c2eff85f556bd1b89671ea0bf40a93203f73
    date: 2018-06-05
    venue: Zoological Journal of the Linnean Society
    authors: R. Kallal, G. Hormiga
    abstract: [no abstract available]
```
</details>

<details><summary>[8] Systematics and evolution of the orb-weaving spider genus Wagneriana F.O. Pickard-Cambridge, 1904 (Araneae; Araneidae) — Jimmy García (2018); cutoff-filter date 2018-11-01; doi:10.11606/t.41.2018.tde-20082018-134133</summary>

```text
[8] Systematics and evolution of the orb-weaving spider genus Wagneriana F.O. Pickard-Cambridge, 1904 (Araneae; Araneidae)
    id: s2:8140771e8bf7e265863c5fcbb12e410e2c3e93ce
    date: 2018-05-21
    venue: unknown
    authors: Jimmy García
    abstract: [no abstract available]
```
</details>

<details><summary>[9] The natural history of Argiope anasuja (Araneae: Araneidae) with special reference to their mating behavior — W.D.S.C. Dharmarathne (2024); cutoff-filter date 2024-04-08; doi:10.1636/joa-s-23-029</summary>

```text
[9] The natural history of Argiope anasuja (Araneae: Araneidae) with special reference to their mating behavior
    id: s2:053a4df85898727c6cdb9496f0cf1cb9a8d12727
    date: 2024-04-08
    venue: The journal of arachnology
    authors: W.D.S.C. Dharmarathne
    abstract: Abstract. Argiope anasuja Thorell, 1887 is a species of orb-weaving spider found in tropical and subtropical regions of the world. Despite its widespread distribution, little is known about its natural history and mating behavior. In this study, I describe some aspects of the natural history and mating behaviors of A. anasuja in captivity and in natural habitats. The spiders were found to occupy less shady areas close to water bodies, building their webs between 50 to 200 cm above the ground level. Web decorations were common in female webs, primarily in the central area, and consisted of dense zigzag bands of silk. A significant difference in copulation duration was observed between cannibalized and non-cannibalized individuals. Furthermore, a significant difference in copulation duration was found between individuals in natural environments and laboratory conditions. However, no significant difference was observed in courtship duration between individuals in natural environment and laboratory conditions. Understanding the mating behaviors of A. anasuja is important because they play a key role in determining the success of mating. This study highlights the natural history and mating behavior of A. anasuja, contributing to our understanding of this species in Sri Lanka.
```
</details>

<details><summary>[10] A phylotranscriptomic backbone of the orb-weaving spider family Araneidae (Arachnida, Araneae) supported by multiple methodological approaches. — R. Kallal, R. Fernández, Gonzalo Giribet, G. Hormiga (2018); cutoff-filter date 2018-09-01; doi:10.1016/j.ympev.2018.04.007</summary>

```text
[10] A phylotranscriptomic backbone of the orb-weaving spider family Araneidae (Arachnida, Araneae) supported by multiple methodological approaches.
    id: s2:7244045751e36a15ceb701e12b84deaf6f9a93fe
    date: 2018-09-01
    venue: Molecular Phylogenetics and Evolution
    authors: R. Kallal, R. Fernández, Gonzalo Giribet, G. Hormiga
    abstract: The orb-weaving spider family Araneidae is extremely diverse (>3100 spp.) and its members can be charismatic terrestrial arthropods, many of them recognizable by their iconic orbicular snare web, such as the common garden spiders. Despite considerable effort to better understand their backbone relationships based on multiple sources of data (morphological, behavioral and molecular), pervasive low support remains in recent studies. In addition, no overarching phylogeny of araneids is available to date, hampering further comparative work. In this study, we analyze the transcriptomes of 33 taxa, including 19 araneids - 12 of them new to this study - representing most of the core family lineages, to examine the relationships within the family using genomic-scale datasets resulting from various methodological treatments, namely ortholog selection and gene occupancy as a measure of matrix completion. Six matrices were constructed to assess these effects by varying orthology inference method and gene occupancy threshold. Orthology methods used are the benchmarking tool BUSCO and the tree-based method UPhO; three gene occupancy thresholds (45%, 65%, 85%) were used to assess the effect of missing data. Gene tree and species tree-based methods (including multi-species coalescent and concatenation approaches, as well as maximum likelihood and Bayesian inference) were used totalling 17 analytical treatments. The monophyly of Araneidae and the placement of core araneid lineages were supported, together with some previously unsound backbone divergences; these include high support for Zygiellinae as the earliest diverging subfamily (followed by Nephilinae), the placement of Gasteracanthinae as sister group to Cyclosa and close relatives, and close relationships between the Araneus + Neoscona clade and Cyrtophorinae + Argiopinae clade. Incongruences were relegated to short branches in the clade comprising Cyclosa and its close relatives. We found congruence between most of the comp [...]
```
</details>

<details><summary>Post-hoc automated audit — NON-AUTHORITATIVE; uses hidden benchmark annotations</summary>

- primary auditor: `silence_as_null_error`; statuses {'H1': 'indeterminate', 'H2': 'positive_or_present'}; discriminative=False
- primary reasoning: H2 (convergent origin) directly predicts that convergent evolution of orb-weaving is possible and should be observed. H1 (ancient origin with loss) does not speak to whether convergent evolution is possible or observed; it is silent on this point.
- derived opposition call: `manufactured_from_silence`
- evidence attribution: `informative_evidence_found` — The retrieval surfaced a paper (record [4]) that directly addresses the proposition, providing evidence for convergent evolution of complex orb-weaving behaviors within Araneidae. The assessor correctly identified and used this evidence. The process worked as intended.
- disagreement flags: {'second_rater_vs_primary_discriminative': None, 'second_rater_vs_primary_status': None, 'retest_vs_primary_category': None, 'any': False}
</details>

**Human review** — `generic_component_fact` · reviewer: Research Director · source: D045 · status: `first_pass_model_based_review` · genuinely discriminative: False · silence-as-null error: False · other fields not recorded

---

## #33 · `GP1-forest_fragmentation_resilience-X24`

**GP1-forest_fragmentation_resilience-X24** — case `forest_fragmentation_resilience`, node `X24`

> Forests with higher edge-to-area ratios are more susceptible to environmental stress-induced degradation than forests with lower edge-to-area ratios.

- generated from **H1** (Candidate B); abstraction: `class`
- generator's stated reason: The claim links fragmentation (which increases edge-to-area ratio) to decreased resistance, so forests in this class should generally show greater susceptibility to stress.
- influence: **0.193** (rank 6 in case, 33 overall; cumulative 73%) — favours **H1**
- log-likelihood contribution: H2 +0.976, H1 +1.169
- removing it alone: evidence withheld → case log-odds -1.438 (ranking unchanged); node deleted → -1.438 (ranking unchanged)

**Hypotheses (as shown to the verifier)**

- **H1** (Candidate B): Fragmentation increases exposure to heat, atmospheric dryness, wind, and drought stress, raising mortality and reducing ecosystem resilience, especially where water/heat stress dominates.
- **H2** (Candidate A): Edge formation can increase light availability and relax limiting-resource constraints, increasing growth, biomass, recovery capacity, and potentially resilience where climatic stress penalties are small enough.

**Verifier cross-hypothesis judgments** — P(X|H) combines these by noisy-OR

| hypothesis | origin? | direct edge | route via parent | P(X\|H) |
| --- | --- | --- | --- | --- |
| H2 | no | `unlikely` | X6 [H→parent `unlikely`, P=0.30] → `implied` | 0.713 |
| H1 | yes | `implied` | X6 [H→parent `strongly_implied`, P=0.95] → `implied` | 0.957 |

- edge rationale, **H2** → node: Candidate A suggests that edge formation can increase resilience and recovery capacity, implying that higher edge-to-area ratios may reduce, not increase, susceptibility to stress-induced degradation.
- edge rationale, **H1** → node: Candidate B states that fragmentation (which increases edge-to-area ratio) raises exposure to environmental stresses and reduces resilience, making degradation more likely.
- parent `X6`: Forests experiencing fragmentation are more likely to show decreased resistance to heat and drought stress compared to contiguous forests.
- chain rationale, `X6` → node: Fragmentation typically increases edge-to-area ratios, so if fragmented forests are less resistant to stress, it implies that forests with higher edge-to-area ratios are more susceptible to environmental stress-induced degradation.

**Verifier evidence** — label used in score: `support` (log-LR +1.2)

- queries: `forest edge-to-area ratio degradation`; `forest fragmentation environmental stress`
- assessor rationale: Record [3] directly reports that female agile antechinus in fragmented forests experience higher physiological stress in fragments with a greater proportion of edge habitat, and that their health responds negatively to the proportion of edge habitat. This provides direct evidence that higher edge-to-area ratios are associated with increased susceptibility to environmental stress-induced degradation. No other records directly address the proposition, and the evidence is limited to one independent study.
- supporting spans cited by the assessor:
  - "Females were trapped less often in edge than interior fragment habitat and their physiological stress level, indicated by the neutrophil/lymphocyte ratio in peripheral blood, was higher where fragments had a greater proportion of edge habitat. The latter trend was potentially due to lymphopoenia resulting from stress hormone-mediated leukocyte trafficking."
  - "Male agile antechinus' health responded negatively to habitat degradation, whilst females responded negatively to the proportion of edge habitat."
- 10 papers shown; key papers: `s2:b761e5242ef6e09f1930358a7d5e1f848e4ecd97`
- _The evidence assessor returns ONE label for the node from all papers shown; the method has no per-paper contribution. Key papers and spans are those the assessor cited._

<details><summary>[1] Genetic Diversity and Structure of Rear Edge Populations of Sorbus aucuparia (Rosaceae) in the Hyrcanian Forest — H. Yousefzadeh, Shahla Raeisi, O. Esmailzadeh, G. Jalali et al. (2021); cutoff-filter date 2021-07-19; doi:10.3390/plants10071471</summary>

```text
[1] Genetic Diversity and Structure of Rear Edge Populations of Sorbus aucuparia (Rosaceae) in the Hyrcanian Forest
    id: s2:299dcb24a8f6a5b8d009b2555b42bb4a127ea215
    date: 2021-07-01
    venue: Plants
    authors: H. Yousefzadeh, Shahla Raeisi, O. Esmailzadeh, G. Jalali, M. Nasiri, Ł. Walas, G. Kozlowski
    abstract: Sorbus aucuparia (Rosaceae) is a small tree species widely distributed in Eurasia. The Hyrcanian forest is the southernmost distribution limit of this species. Severe habitat degradation and inadequate human interventions have endangered the long-term survival of this species in this region, and it is necessary to develop and apply appropriate management methods to prevent the loss of its genetic diversity. In this study, we used 10 SSR markers in order to evaluate the genetic diversity of this taxon. Leaf samples were collected from five known populations of S. aucuparia throughout its distribution area in the Hyrcanian forest. Expected heterozygosity ranged from 0.61 (ASH) to 0.73, and according to the M-ratio, all populations showed a significant reduction in effective population size, indicating a genetic bottleneck. Global FST was not statistically significant and attained the same values with and without excluding null alleles (ENA) correction (FST = 0.12). Bayesian analysis performed with STRUCTURE defined two genetic clusters among the five known populations, while the results of discriminant analysis of principal components (DAPC) identified three distinct groups. The average proportion of migrants was 22. In general, the gene flow was asymmetrical, with the biggest differences between immigration and emigration in Barzekoh and Asbehriseh. The Mantel test showed that there was no significant correlation between genetic distance (FST) and geographic distance in S. aucuparia. The best pathway for theoretical gene flow is located across the coast of the Caspian Sea and significant spatial autocorrelation was observed in only one population. In order to reduce the extinction risk of very small and scattered populations of S. aucuparia in the Hyrcanian forest, it is very important to establish and/or enhance the connectivity through habitat restoration or genetic exchange.
```
</details>

<details><summary>[2] Using geoinformatics to link forest fire severity and fragmentation in India's Dalma Wildlife Sanctuary — S. Chaudhary, A. Pandey, B. Parida, S. Gupta (2022); cutoff-filter date 2022-02-08; doi:10.1007/s42965-021-00202-0</summary>

```text
[2] Using geoinformatics to link forest fire severity and fragmentation in India's Dalma Wildlife Sanctuary
    id: s2:091c59f3366f5477119db1a148d5a4bf2bf5d76d
    date: 2022-02-08
    venue: Tropical Ecology
    authors: S. Chaudhary, A. Pandey, B. Parida, S. Gupta
    abstract: [no abstract available]
```
</details>

<details><summary>[3] **KEY** Response of the Agile Antechinus to Habitat Edge, Configuration and Condition in Fragmented Forest — Christopher P. Johnstone, A. Lill, R. D. Reina (2011); cutoff-filter date 2011-11-04; doi:10.1371/journal.pone.0027158</summary>

```text
[3] Response of the Agile Antechinus to Habitat Edge, Configuration and Condition in Fragmented Forest
    id: s2:b761e5242ef6e09f1930358a7d5e1f848e4ecd97
    date: 2011-11-04
    venue: PLoS ONE
    authors: Christopher P. Johnstone, A. Lill, R. D. Reina
    abstract: Habitat fragmentation and degradation seriously threaten native animal communities. We studied the response of a small marsupial, the agile antechinus Antechinus agilis, to several environmental variables in anthropogenically fragmented Eucalyptus forest in south-east Australia. Agile antechinus were captured more in microhabitats dominated by woody debris than in other microhabitats. Relative abundances of both sexes were positively correlated with fragment core area. Male and female mass-size residuals were smaller in larger fragments. A health status indicator, haemoglobin-haematocrit residuals (HHR), did not vary as a function of any environmental variable in females, but male HHR indicated better health where sites' microhabitats were dominated by shrubs, woody debris and trees other than Eucalyptus. Females were trapped less often in edge than interior fragment habitat and their physiological stress level, indicated by the neutrophil/lymphocyte ratio in peripheral blood, was higher where fragments had a greater proportion of edge habitat. The latter trend was potentially due to lymphopoenia resulting from stress hormone-mediated leukocyte trafficking. Using multiple indicators of population condition and health status facilitates a comprehensive examination of the effects of anthropogenic disturbances, such as habitat fragmentation and degradation, on native vertebrates. Male agile antechinus' health responded negatively to habitat degradation, whilst females responded negatively to the proportion of edge habitat. The health and condition indicators used could be employed to identify conservation strategies that would make habitat fragments less stressful for this or similar native, small mammals.
```
</details>

<details><summary>[4] Integrated use of Sentinel-1 and Sentinel-2 data and open-source machine learning algorithms for land cover mapping in a Mediterranean region — Giandomenico De Luca, João M. N. Silva, S. Di Fazio, G. Modica (2022); cutoff-filter date 2022-01-12; doi:10.1080/22797254.2021.2018667</summary>

```text
[4] Integrated use of Sentinel-1 and Sentinel-2 data and open-source machine learning algorithms for land cover mapping in a Mediterranean region
    id: s2:2ea585e06ca129b1a5e77f9ba2aae30344eed85b
    date: 2022-01-12
    venue: European Journal of Remote Sensing
    authors: Giandomenico De Luca, João M. N. Silva, S. Di Fazio, G. Modica
    abstract: ABSTRACT This paper aims to develop a supervised classification integrating synthetic aperture radar (SAR) Sentinel-1 (S1) and optical Sentinel-2 (S2) data for land use/land cover (LULC) mapping in a heterogeneous Mediterranean forest area. The time-series of each SAR and optical bands, three optical indices (normalized difference vegetation index, NDVI; normalized burn ratio, NBR; normalized difference red-edge index, NDRE), and two SAR indices (radar vegetation index, RVI; radar forest degradation index, RFDI), constituted the dataset. The coherence information from SAR interferometry (InSAR) analysis and three optical biophysical variables (leaf area index, LAI; fraction of green vegetation cover, fCOVER; fraction of absorbed photosynthetically active radiation, fAPAR) of the single final month of the time-series were added to exploit their correlation with the canopy structure and improve the classification. The random forests (RF) algorithm was used to train and classify the final dataset, and an exhaustive grid search analysis was applied to set the optimal hyperparameters. The overall accuracy reached an F-scoreM of 90.33% and the integration of SAR improved it by 2.53% compared to that obtained using only optical data. The whole process was performed using freely available data and open-source software and libraries (SNAP, Google Earth Engine, Scikit-Learn) executed in Python-script language.
```
</details>

<details><summary>[5] Global spatial analysis of mangrove forest fragmentation — D. Kemalasari, A. de Carvalho Ximenes, F. Dahdouh-Guebas, N. Koedam (2013); cutoff-filter date 2013-12-31; https://www.semanticscholar.org/paper/913efc1370e4a9edd56b9ed65c426b1b56f50c66</summary>

```text
[5] Global spatial analysis of mangrove forest fragmentation
    id: s2:913efc1370e4a9edd56b9ed65c426b1b56f50c66
    date: 2013
    venue: unknown
    authors: D. Kemalasari, A. de Carvalho Ximenes, F. Dahdouh-Guebas, N. Koedam
    abstract: [no abstract available]
```
</details>

<details><summary>[6] Influence of Specimen Size on Accelerated Weathering of Laminated Veneer Lumber — D. Way, F. Kamke, Arijit Sinha (2019); cutoff-filter date 2019-12-31; doi:10.13073/fpj-d-18-00035</summary>

```text
[6] Influence of Specimen Size on Accelerated Weathering of Laminated Veneer Lumber
    id: s2:df25656a633f29efb20b3ecb923f6cba2ff2c88c
    date: 2019-06-21
    venue: Forest products journal
    authors: D. Way, F. Kamke, Arijit Sinha
    abstract: 
 Moisture intrusion can be significantly higher along specimen edges, particularly at edges where longitudinal grain is exposed, which is referred to as the edge effect. The influence of edge effects on moisture durability are assumed to decrease as the edge area to total-surface-area ratio decreases. Moisture durability assessment of laminated veneer lumber (LVL) is commonly evaluated using accelerated weathering (AW) and outdoor exposure methods, where small specimens are analyzed. The influence of specimen size (i.e., edge effect) on moisture durability evaluation of LVL was investigated in this study. To vary specimen size, three widths with constant length and thickness were evaluated. In addition, three AW methods were used to characterize how the method of inflicting degradation influenced edge effects. No consistent trends in mechanical property loss were found across AW methods, indicating that the influence of specimen size varied with AW method. The greatest influence of specimen size occurred when cyclic vacuum-soak-dry was included, where water absorption decreased significantly with increasing width, and three of four mechanical properties evaluated displayed an influence of specimen size. The smallest influence of specimen size occurred when a single soak-dry procedure was included, where only one of four mechanical properties evaluated displayed an influence of specimen size. Results from this study provide evidence that edge effects may occur during LVL moisture durability assessment but that the severity is dependent on AW conditions.
```
</details>

<details><summary>[7] Capítulo 7 Efectos sinérgicos de la fragmentación y la perturbación local en la diversi- dad de árboles de bosques tropicales montanos — Ramírez-Marcial (2006); cutoff-filter date 2006-12-31; https://www.semanticscholar.org/paper/46e67cda832043776eee08ae16a0520dc5a8001d</summary>

```text
[7] Capítulo 7 Efectos sinérgicos de la fragmentación y la perturbación local en la diversi- dad de árboles de bosques tropicales montanos
    id: s2:46e67cda832043776eee08ae16a0520dc5a8001d
    date: 2006
    venue: unknown
    authors: Ramírez-Marcial
    abstract: [no abstract available]
```
</details>

<details><summary>[8] Accounting for Greenhouse Gas Emissions from Forest Edge Degradation: Gold Mining in Guyana as a Case Study — S. Brown, A. Mahmood, K. Goslee, T. Pearson et al. (2020); cutoff-filter date 2020-12-07; doi:10.3390/f11121307</summary>

```text
[8] Accounting for Greenhouse Gas Emissions from Forest Edge Degradation: Gold Mining in Guyana as a Case Study
    id: s2:5bbbb3be70d6efe4b61755a303e74481a957e4d0
    date: 2020-12-07
    venue: Forests
    authors: S. Brown, A. Mahmood, K. Goslee, T. Pearson, Hansrajie Sukhdeo, D. Donoghue, P. Watt
    abstract: Background and Methods: Degradation of forests in developing countries results from multiple activities and is perceived to be a key source of greenhouse gas emissions, yet there are not reliable methodologies to measure and monitor emissions from all degrading activities. Therefore, there is limited knowledge of the actual extent of emissions from forest degradation. Degradation can be either in the forest interior, with a repeatable defined pattern within areas of forest, as with timber harvest, or on the forest edge and immediately bounding areas of deforestation. Forest edge degradation is especially challenging to capture with remote sensing or to predict from proxy factors. This paper addresses forest edge degradation and: (1) proposes a low cost methodology for assessing forest edge degradation surrounding deforestation; (2) using the method, provides estimates of gross carbon emissions from forest degradation surrounding and caused by alluvial mining in Guyana, and (3) compares emissions from mining degradation with other sources of forest greenhouse gas emissions. To estimate carbon emissions from forest degradation associated with mining in Guyana, 100 m buffers were located around polygons pre-mapped as mining deforestation, and within these buffers rectangular transects were established. Researchers collected ground data to produce estimates of the biomass damaged as a result of mining activities to apply to the buffer area around the mining deforestation. Results: The proposed method to estimate emissions from forest edge degradation was successfully piloted in Guyana, where 61% of the transects lost 10 Mg C ha−1 or less in trees from mining damage and 46% of these transects lost 1 Mg C ha−1 or less. Seventy percent of the damaged stems and 60% of carbon loss occurred in the first 50 m of the transects. The median loss in carbon stock from mining damage was 2.2 Mg C ha−1 (95% confidence interval: 0.0–10.2 Mg C ha−1). The carbon loss from mining degradat [...]
```
</details>

<details><summary>[9] Mediation of area and edge effects in forest fragments by adjacent land use — J. Hatfield, J. Barlow, C. Joly, A. Lees et al. (2019); cutoff-filter date 2019-07-17; doi:10.1111/cobi.13390</summary>

```text
[9] Mediation of area and edge effects in forest fragments by adjacent land use
    id: s2:513fbb4dff26f31caffcd78a6c90d938ef7642b1
    date: 2019-07-16
    venue: Conservation Biology
    authors: J. Hatfield, J. Barlow, C. Joly, A. Lees, Celso Henrique de Freitas Parruco, Joseph A. Tobias, C. Orme, C. Banks-Leite
    abstract: Habitat loss, fragmentation, and degradation have pervasive detrimental effects on tropical forest biodiversity, but the role of the surrounding land use (i.e., matrix) in determining the severity of these impacts remains poorly understood. We surveyed bird species across an interior‐edge‐matrix gradient to assess the effects of matrix type on biodiversity at 49 different sites with varying levels of landscape fragmentation in the Brazilian Atlantic Forest—a highly threatened biodiversity hotspot. Both area and edge effects were more pronounced in forest patches bordering pasture matrix, whereas patches bordering Eucalyptus plantation maintained compositionally similar bird communities between the edge and the interior and exhibited reduced effects of patch size. These results suggest the type of matrix in which forest fragments are situated can explain a substantial amount of the widely reported variability in biodiversity responses to forest loss and fragmentation.
```
</details>

<details><summary>[10] Comparable biophysical and biogeochemical feedbacks on warming from tropical moist forest degradation — Lei Zhu, Wei Li, P. Ciais, Jia-Ying He et al. (2023); cutoff-filter date 2023-03-02; doi:10.1038/s41561-023-01137-y</summary>

```text
[10] Comparable biophysical and biogeochemical feedbacks on warming from tropical moist forest degradation
    id: s2:c2bb551ca41b0d3b1510b1a26e794f147682c36f
    date: 2023-03-01
    venue: Nature Geoscience
    authors: Lei Zhu, Wei Li, P. Ciais, Jia-Ying He, A. Cescatti, M. Santoro, Katsumasa Tanaka, O. Cartus
    abstract: Tropical forests have undergone extensive deforestation and degradation during the past few decades, but the area and the carbon loss due to degradation could be larger than the losses from deforestation. Degraded forests also induce biophysical feedback on climate, as they sustain less cooling from evapotranspiration. Here we estimate the biophysical and biogeochemical temperature changes caused by tropical moist forest degradation using high-resolution remote sensing data from 2010. Degraded forests, including burned, isolated, edge and other degraded forests, account for 24.1% of the total tropical moist forest area. The land surface temperature of degraded tropical moist forests is higher than that of nearby intact forests, leading to a warming effect of 0.022 ± 0.014 °C over the tropics. The cumulative carbon deficit of degraded forests reaches 6.1 ± 2.0 PgC, equivalent to a biogeochemical warming effect of 0.026 ± 0.013 °C. Forest degradation caused by anthropogenic disturbances from 1990 to 2010 induces a daytime warming effect of 0.018 ± 0.008 °C and a carbon deficit of 2.3 ± 0.8 PgC. These values are of the same order of magnitude as those due to deforestation. Our results emphasize the importance of accounting for the combined biophysical and biogeochemical effects in mitigation pledges related to reducing forest degradation and the restoration of tropical forest. Biophysical and biogeochemical effects of forest degradation cause comparable temperature increases in tropical rainforests, according to analyses of high-resolution satellite observations.
```
</details>

<details><summary>Post-hoc automated audit — NON-AUTHORITATIVE; uses hidden benchmark annotations</summary>

- primary auditor: `silence_as_null_error`; statuses {'H1': 'positive_or_present', 'H2': 'indeterminate'}; discriminative=False
- primary reasoning: H1 explicitly predicts that increased edge-to-area ratio (fragmentation) raises susceptibility to environmental stress and reduces resilience. H2 does not speak to susceptibility to stress-induced degradation; it focuses on increased growth and recovery under relaxed resource constraints, not on stress vulnerability.
- derived opposition call: `manufactured_from_silence`
- evidence attribution: `informative_evidence_found` — The retrieval surfaced a paper (record [3]) that directly addresses the proposition, providing evidence that higher edge-to-area ratios in fragmented forests are associated with increased susceptibility to environmental stress-induced degradation. The assessor correctly identified and used this evidence. The process worked as intended.
- disagreement flags: {'second_rater_vs_primary_discriminative': None, 'second_rater_vs_primary_status': None, 'retest_vs_primary_category': None, 'any': False}
</details>

**Human review** — `silence_as_null_error` · reviewer: Research Director · source: D045 · status: `first_pass_model_based_review` · genuinely discriminative: False · silence-as-null error: True · other fields not recorded

---

## #34 · `GP1-glnbp_induced_fit_vs_conformational_selection-X17`

**GP1-glnbp_induced_fit_vs_conformational_selection-X17** — case `glnbp_induced_fit_vs_conformational_selection`, node `X17`

> Ligand binding to periplasmic binding proteins is enhanced when the protein adopts a closed conformation.

- generated from **H1** (Candidate B); abstraction: `class`
- generator's stated reason: If glutamine binding to GlnBP is favored in the closed state, it suggests that ligand binding in this protein family generally occurs more readily in closed conformations.
- influence: **0.193** (rank 9 in case, 34 overall; cumulative 74%) — favours **H1**
- log-likelihood contribution: H2 +0.976, H1 +1.169
- removing it alone: evidence withheld → case log-odds +2.035 (ranking unchanged); node deleted → +2.035 (ranking unchanged)

**Hypotheses (as shown to the verifier)**

- **H1** (Candidate B): Apo-GlnBP samples a pre-existing binding-competent closed or semi-closed conformation; glutamine preferentially binds/captures that pre-existing conformation.
- **H2** (Candidate A): Glutamine binds to open/binding-competent GlnBP before the major protein conformational rearrangement, after which GlnBP closes around the ligand.

**Verifier cross-hypothesis judgments** — P(X|H) combines these by noisy-OR

| hypothesis | origin? | direct edge | route via parent | P(X\|H) |
| --- | --- | --- | --- | --- |
| H2 | no | `unlikely` | X5 [H→parent `unlikely`, P=0.30] → `implied` | 0.713 |
| H1 | yes | `implied` | X5 [H→parent `strongly_implied`, P=0.95] → `implied` | 0.957 |

- edge rationale, **H2** → node: Candidate A states that ligand binding occurs before the protein closes, implying that the closed conformation does not enhance binding.
- edge rationale, **H1** → node: Candidate B suggests that ligand binding occurs preferentially to a closed or semi-closed conformation, implying that the closed state enhances binding.
- parent `X5`: Glutamine binding to GlnBP occurs preferentially when the protein is in a closed or semi-closed conformation.
- chain rationale, `X5` → node: The parent proposition provides a specific example that supports the general trend described in the child, but does not address all periplasmic binding proteins.

**Verifier evidence** — label used in score: `support` (log-LR +1.2)

- queries: `periplasmic binding protein closed conformation`; `ligand affinity periplasmic binding protein`
- assessor rationale: Record [5] directly states that the periplasmic binding protein VhCBP binds its ligand (GlcNAc)2 with greatest affinity when adopting a high-affinity conformation, which is implied to be the closed conformation, and that a low-affinity conformation facilitates ligand release. This directly supports the proposition that ligand binding is enhanced in the closed conformation. No other records provide direct statements about the relationship between ligand binding and protein conformation.
- supporting spans cited by the assessor:
  - "VhCBP displayed the greatest affinity toward (GlcNAc)2, with lower affinity for longer-chain chitooligosaccharides [(GlcNAc)3–4]."
  - "Isothermal calorimetry data suggested that VhCBP adopts the high-affinity conformation to bind (GlcNAc)2, while its low-affinity conformation facilitated sugar release."
- 10 papers shown; key papers: `s2:217bab073df03bde42f55f8caa3b033a837ad888`
- _The evidence assessor returns ONE label for the node from all papers shown; the method has no per-paper contribution. Key papers and spans are those the assessor cited._

<details><summary>[1] The Crystal Structure of Zn(II)-Free Treponema pallidum TroA, a Periplasmic Metal-Binding Protein, Reveals a Closed Conformation — Yong-Hwan Lee, M. Dorwart, K. Hazlett, R. Deka et al. (2002); cutoff-filter date 2002-04-15; doi:10.1128/jb.184.8.2300-2304.2002</summary>

```text
[1] The Crystal Structure of Zn(II)-Free Treponema pallidum TroA, a Periplasmic Metal-Binding Protein, Reveals a Closed Conformation
    id: s2:d6ac292e96552a9d71d29ab8504f3397df8858d2
    date: 2002-04-15
    venue: Journal of Bacteriology
    authors: Yong-Hwan Lee, M. Dorwart, K. Hazlett, R. Deka, M. Norgard, J. Radolf, C. Hasemann
    abstract: [no abstract available]
```
</details>

<details><summary>[2] Maltose-binding protein effectively stabilizes the partially closed conformation of the ATP-binding cassette transporter MalFGK2. — Jing-Wei Weng, Shuo Gu, Xin Gao, Xuhui Huang et al. (2017); cutoff-filter date 2017-04-05; doi:10.1039/c6cp07943a</summary>

```text
[2] Maltose-binding protein effectively stabilizes the partially closed conformation of the ATP-binding cassette transporter MalFGK2.
    id: s2:06d2b402da94b3ef48e03eb0e3fde4a751d7240e
    date: 2017-04-05
    venue: Physical Chemistry, Chemical Physics - PCCP
    authors: Jing-Wei Weng, Shuo Gu, Xin Gao, Xuhui Huang, Wen-Ning Wang
    abstract: [no abstract available]
```
</details>

<details><summary>[3] A solute-binding protein in the closed conformation induces ATP hydrolysis in a bacterial ATP-binding cassette transporter involved in the import of alginate — A. Kaneko, K. Uenishi, Y. Maruyama, N. Mizuno et al. (2017); cutoff-filter date 2017-08-03; doi:10.1074/jbc.m117.793992</summary>

```text
[3] A solute-binding protein in the closed conformation induces ATP hydrolysis in a bacterial ATP-binding cassette transporter involved in the import of alginate
    id: s2:385ff0ca1fdfe1c088e64a6d9f4aa74d0e8d6b6b
    date: 2017-08-02
    venue: Journal of Biological Chemistry
    authors: A. Kaneko, K. Uenishi, Y. Maruyama, N. Mizuno, S. Baba, T. Kumasaka, B. Mikami, K. Murata
    abstract: The Gram-negative bacterium Sphingomonas sp. A1 incorporates alginate into cells via the cell-surface pit without prior depolymerization by extracellular enzymes. Alginate import across cytoplasmic membranes thereby depends on the ATP-binding cassette transporter AlgM1M2SS (a heterotetramer of AlgM1, AlgM2, and AlgS), which cooperates with the periplasmic solute-binding protein AlgQ1 or AlgQ2; however, several details of AlgM1M2SS-mediated alginate import are not well-understood. Herein, we analyzed ATPase and transport activities of AlgM1M2SS after reconstitution into liposomes with AlgQ2 and alginate oligosaccharide substrates having different polymerization degrees (PDs). Longer alginate oligosaccharides (PD ≥ 5) stimulated the ATPase activity of AlgM1M2SS but were inert as substrates of AlgM1M2SS-mediated transport, indicating that AlgM1M2SS-mediated ATP hydrolysis can be stimulated independently of substrate transport. Using X-ray crystallography in the presence of AlgQ2 and long alginate oligosaccharides (PD 6–8) and with the humid air and glue-coating method, we determined the crystal structure of AlgM1M2SS in complex with oligosaccharide-bound AlgQ2 at 3.6 Å resolution. The structure of the ATP-binding cassette transporter in complex with non-transport ligand-bound periplasmic solute-binding protein revealed that AlgM1M2SS and AlgQ2 adopt inward-facing and closed conformations, respectively. These in vitro assays and structural analyses indicated that interactions between AlgM1M2SS in the inward-facing conformation and periplasmic ligand-bound AlgQ2 in the closed conformation induce ATP hydrolysis by the ATP-binding protein AlgS. We conclude that substrate-bound AlgQ2 in the closed conformation initially interacts with AlgM1M2SS, the AlgM1M2SS–AlgQ2 complex then forms, and this formation is followed by ATP hydrolysis.
```
</details>

<details><summary>[4] Open Conformation of the Escherichia coli Periplasmic Murein Tripeptide Binding Protein, MppA, at High Resolution — F. Bhatt, V. Patel, C. Jeffery (2018); cutoff-filter date 2018-05-19; doi:10.3390/biology7020030</summary>

```text
[4] Open Conformation of the Escherichia coli Periplasmic Murein Tripeptide Binding Protein, MppA, at High Resolution
    id: s2:5a47e8bc5487d7f664fdf14bd73afa31c6dd440f
    date: 2018-05-19
    venue: Biology
    authors: F. Bhatt, V. Patel, C. Jeffery
    abstract: Periplasmic ligand-binding proteins (PBPs) bind ligands with a high affinity and specificity. They undergo a large conformational change upon ligand binding, and they have a robust protein fold. These physical features have made them ideal candidates for use in protein engineering projects to develop novel biosensors and signaling molecules. The Escherichia coli MppA (murein peptide permease A) PBP binds the murein tripeptide, l-alanyl-γ-d-glutamyl-meso-diaminopimelate, (l-Ala-γ-d-Glu-meso-Dap), which contains both a D-amino acid and a gamma linkage between two of the amino acids. We have solved a high-resolution X-ray crystal structure of E. coli MppA at 1.5 Å resolution in the unliganded, open conformation. Now, structures are available for this member of the PBP protein family in both the liganded/closed form and the unliganded/open form.
```
</details>

<details><summary>[5] **KEY** A structural model for (GlcNAc)2 translocation via a periplasmic chitooligosaccharide-binding protein from marine Vibrio bacteria — Y. Kitaoku, T. Fukamizo, Sawitree Kumsaoad, P. Ubonbal et al. (2021); cutoff-filter date 2021-08-13; doi:10.1016/j.jbc.2021.101071</summary>

```text
[5] A structural model for (GlcNAc)2 translocation via a periplasmic chitooligosaccharide-binding protein from marine Vibrio bacteria
    id: s2:217bab073df03bde42f55f8caa3b033a837ad888
    date: 2021-08-01
    venue: Journal of Biological Chemistry
    authors: Y. Kitaoku, T. Fukamizo, Sawitree Kumsaoad, P. Ubonbal, R. Robinson, W. Suginta
    abstract: VhCBP is a periplasmic chitooligosaccharide-binding protein mainly responsible for translocation of the chitooligosaccharide (GlcNAc)2 across the double membranes of marine bacteria. However, structural and thermodynamic understanding of the sugar-binding/-release processes of VhCBP is relatively less. VhCBP displayed the greatest affinity toward (GlcNAc)2, with lower affinity for longer-chain chitooligosaccharides [(GlcNAc)3–4]. (GlcNAc)4 partially occupied the closed sugar-binding groove, with two reducing-end GlcNAc units extending beyond the sugar-binding groove and barely characterized by weak electron density. Mutation of three conserved residues (Trp363, Asp365, and Trp513) to Ala resulted in drastic decreases in the binding affinity toward the preferred substrate (GlcNAc)2, indicating their significant contributions to sugar binding. The structure of the W513A–(GlcNAc)2 complex in a ‘half-open’ conformation unveiled the intermediary step of the (GlcNAc)2 translocation from the soluble CBP in the periplasm to the inner membrane–transporting components. Isothermal calorimetry data suggested that VhCBP adopts the high-affinity conformation to bind (GlcNAc)2, while its low-affinity conformation facilitated sugar release. Thus, chitooligosaccharide translocation, conferred by periplasmic VhCBP, is a crucial step in the chitin catabolic pathway, allowing Vibrio bacteria to thrive in oceans where chitin is their major source of nutrients.
```
</details>

<details><summary>[6] The Open Conformation Satisfies Multiple NMR Experiments on Apo Glutamine-Binding Protein: Overcoming Pitfalls in the Study of Interdomain Dynamics — H. Kooshapur, Junhe Ma, N. Tjandra, G. Bermejo (2019); cutoff-filter date 2019-09-13; doi:10.1002/anie.201911015</summary>

```text
[6] The Open Conformation Satisfies Multiple NMR Experiments on Apo Glutamine-Binding Protein: Overcoming Pitfalls in the Study of Interdomain Dynamics
    id: s2:eb71f0a80f7f2961fcf1898dd7951b1b511f449b
    date: 2019-09-13
    venue: Angewandte Chemie
    authors: H. Kooshapur, Junhe Ma, N. Tjandra, G. Bermejo
    abstract: Glutamine-binding protein (GlnBP) from Escherichia coli is a prototypical periplasmic binding protein that has been crystallized in an apo, “open” conformation, with its two domains far apart, and a holo, “closed” form, with proximal domains that engulf the cognate L-Gln ligand. A fundamental question about such large-scale conformational transitions—whether the closed state exists in the absence of ligand—is a matter of controversy in the case of GlnBP. Previously, NMR observations have indicated no evidence of the closed form, whereas experimentally validated computations have suggested a remarkable ~40% population. Here, a paramagnetic NMR strategy designed to specifically detect the putative apo-closed species shows that a major population of the latter is highly improbable. Further, NMR residual dipolar couplings collected under three anisotropic conditions fail to reveal differential domain alignment (which would otherwise signal interdomain dynamics) and establish that the average solution conformation is satisfied by the apo-open crystal structure. Our results indicate that the computational prediction of large-scale interdomain motions is far from trivial and may lead to grossly erroneous conclusions without proper experimental validation.
```
</details>

<details><summary>[7] 19F NMR Studies of the Leucine-Isoleucine-Valine Binding Protein: Evidence That a Closed Conformation Exists in Solution — B. Salopek-Sondi, M. Vaughan, M. Skeels, J. Honek et al. (2003); cutoff-filter date 2003-10-31; doi:10.1080/07391102.2003.10506919</summary>

```text
[7] 19F NMR Studies of the Leucine-Isoleucine-Valine Binding Protein: Evidence That a Closed Conformation Exists in Solution
    id: s2:a03900e7d689eed3c47aa81db5f3d7f93aa50ba7
    date: 2003-10-01
    venue: Journal of Biomolecular Structure and Dynamics
    authors: B. Salopek-Sondi, M. Vaughan, M. Skeels, J. Honek, L. Luck
    abstract: [no abstract available]
```
</details>

<details><summary>[8] Structural analysis of the choline-binding protein ChoX in a semi-closed and ligand-free conformation — C. Oswald, S. Smits, Marina Höing, E. Bremer et al. (2009); cutoff-filter date 2009-11-01; doi:10.1515/bc.2009.113</summary>

```text
[8] Structural analysis of the choline-binding protein ChoX in a semi-closed and ligand-free conformation
    id: s2:04ae14ca367879385cca736afc5e5125e2202dd7
    date: 2009-11-01
    venue: Biological chemistry
    authors: C. Oswald, S. Smits, Marina Höing, E. Bremer, L. Schmitt
    abstract: [no abstract available]
```
</details>

<details><summary>[9] Ligand-induced structural changes analysis of ribose-binding protein as studied by molecular dynamics simulations — Hai-Yan Li, Zanxia Cao, Guodong Hu, Li-Ling Zhao et al. (2021); cutoff-filter date 2021-03-02; doi:10.3233/thc-218011</summary>

```text
[9] Ligand-induced structural changes analysis of ribose-binding protein as studied by molecular dynamics simulations
    id: s2:b407302d7c1be527f2abbdc5b5075a4a215f7ec3
    date: 2021-01-01
    venue: Technology and Health Care
    authors: Hai-Yan Li, Zanxia Cao, Guodong Hu, Li-Ling Zhao, Chun-Ling Wang, Jihua Wang
    abstract: BACKGROUND: The ribose-binding protein (RBP) from Escherichia coli is one of the representative structures of periplasmic binding proteins. Binding of ribose at the cleft between two domains causes a conformational change corresponding to a closure of two domains around the ligand. The RBP has been crystallized in the open and closed conformations. OBJECTIVE: With the complex trajectory as a control, our goal was to study the conformation changes induced by the detachment of the ligand, and the results have been revealed from two computational tools, MD simulations and elastic network models. METHODS: Molecular dynamics (MD) simulations were performed to study the conformation changes of RBP starting from the open-apo, closed-holo and closed-apo conformations. RESULTS: The evolution of the domain opening angle θ clearly indicates large structural changes. The simulations indicate that the closed states in the absence of ribose are inclined to transition to the open states and that ribose-free RBP exists in a wide range of conformations. The first three dominant principal motions derived from the closed-apo trajectories, consisting of rotating, bending and twisting motions, account for the major rearrangement of the domains from the closed to the open conformation. CONCLUSIONS: The motions showed a strong one-to-one correspondence with the slowest modes from our previous study of RBP with the anisotropic network model (ANM). The results obtained for RBP contribute to the generalization of robustness for protein domain motion studies using either the ANM or PCA for trajectories obtained from MD.
```
</details>

<details><summary>[10] Study on the mechanism of the BtuF periplasmic-binding protein for vitamin B12. — Ming Liu, Ting-Guang Sun, Jianping Hu, Wei-Zu Chen et al. (2008); cutoff-filter date 2008-06-01; doi:10.1016/j.bpc.2008.02.017</summary>

```text
[10] Study on the mechanism of the BtuF periplasmic-binding protein for vitamin B12.
    id: s2:49d80a3094057adfb3fcf4f1dfecf770065fe3b0
    date: 2008-06-01
    venue: Biophysical Chemistry
    authors: Ming Liu, Ting-Guang Sun, Jianping Hu, Wei-Zu Chen, Cun-xin Wang
    abstract: [no abstract available]
```
</details>

<details><summary>Post-hoc automated audit — NON-AUTHORITATIVE; uses hidden benchmark annotations</summary>

- primary auditor: `silence_as_null_error`; statuses {'H2': 'indeterminate', 'H1': 'positive_or_present'}; discriminative=False
- primary reasoning: H1 (conformational selection) implies that ligand binding is favored in the closed (or semi-closed) state, so it predicts the proposition as positive. H2 (induced fit) does not require or predict that binding is enhanced in the closed state; it is compatible with binding occurring in the open state, so it is indeterminate.
- derived opposition call: `manufactured_from_silence`
- evidence attribution: `informative_evidence_found` — The retrieval system surfaced a paper (record [5]) that directly addresses the relationship between ligand binding and the closed conformation of a periplasmic binding protein, and the assessor correctly identified and used this evidence to support the proposition. The process worked as intended, with both the queries and assessment functioning appropriately.
- second rater (LLM, blind): statuses {'H1': 'positive_or_present', 'H2': 'positive_or_present'}; discriminative=False (high confidence) — closed complex is high-affinity under both mechanisms
- disagreement flags: {'second_rater_vs_primary_discriminative': False, 'second_rater_vs_primary_status': True, 'retest_vs_primary_category': None, 'any': True}
</details>

**Human review** — `compatible_non_discriminative` · reviewer: Research Director · source: D045 · status: `first_pass_model_based_review` · genuinely discriminative: False · silence-as-null error: False · other fields not recorded

---

## #35 · `GP1-pfc_storage_vs_control-X13`

**GP1-pfc_storage_vs_control-X13** — case `pfc_storage_vs_control`, node `X13`

> Persistent neural activity in lateral prefrontal cortex, specifically the superior precentral sulcus, represents the identity of visual items held in working memory.

- generated from **H1** (Candidate A); abstraction: `specific`
- influence: **0.193** (rank 7 in case, 35 overall; cumulative 75%) — favours **H1**
- log-likelihood contribution: H1 +1.169, H2 +0.976
- removing it alone: evidence withheld → case log-odds +1.021 (ranking unchanged); node deleted → +1.021 (ranking unchanged)

**Hypotheses (as shown to the verifier)**

- **H1** (Candidate A): Prefrontal persistent activity is itself a substrate for working-memory storage; disrupting the relevant PFC population therefore disrupts the stored mnemonic representation.
- **H2** (Candidate B): PFC primarily controls, prioritizes, or allocates resources to working-memory representations maintained in sensory/posterior regions rather than directly storing the mnemonic content itself.

**Verifier cross-hypothesis judgments** — P(X|H) combines these by noisy-OR

| hypothesis | origin? | direct edge | route via parent | P(X\|H) |
| --- | --- | --- | --- | --- |
| H1 | yes | `implied` | X2 [H→parent `strongly_implied`, P=0.95] → `implied` | 0.957 |
| H2 | no | `unlikely` | X2 [H→parent `unlikely`, P=0.30] → `implied` | 0.713 |

- edge rationale, **H1** → node: If persistent activity in PFC is the substrate for working-memory storage, it is clearly expected that such activity in the superior precentral sulcus would represent the identity of visual items held in working memory.
- edge rationale, **H2** → node: If PFC primarily controls or allocates resources to representations stored elsewhere, it is less likely that persistent activity in the superior precentral sulcus directly represents the identity of visual items in working memory.
- parent `X2`: Persistent neural activity in prefrontal cortex encodes the content of items maintained in working memory.
- chain rationale, `X2` → node: The parent proposition supports the idea that persistent activity in prefrontal cortex encodes working memory content, which implies but does not guarantee that such activity in a specific lateral prefrontal region (superior precentral sulcus) represents the identity of visual items held in working memory.

**Verifier evidence** — label used in score: `support` (log-LR +1.2)

- queries: `superior precentral sulcus working memory`; `lateral prefrontal cortex visual identity representation`
- assessor rationale: Record [10] directly reports persistent activity in the superior precentral sulcus (PCS) during the maintenance of a working memory representation, and further shows that decoders can predict the location of items held in working memory from this activity. This supports the proposition that persistent neural activity in the lateral prefrontal cortex, specifically the superior PCS, represents the identity (location) of visual items held in working memory. No other records directly address this proposition.
- supporting spans cited by the assessor:
  - "Persistent activity increased from posterior-to-anterior IPS areas and from inferior-to-superior PCS areas during the maintenance of a working memory representation, the maintenance of covert attention, and the maintenance of a saccade plan."
  - "decoders trained to predict the locations on one task (e.g., working memory) cross-predicted the locations on other tasks (e.g., attention) in superior PCS and IPS2, suggesting that these patterns of maintenance activity may be interchangeable across the tasks."
- 10 papers shown; key papers: `s2:7aec191731033d7436cbb0a3bc09673d98c411e9`
- _The evidence assessor returns ONE label for the node from all papers shown; the method has no per-paper contribution. Key papers and spans are those the assessor cited._

<details><summary>[1] Differential roles for frontal eye fields (FEF) and intraparietal sulcus (IPS) in visual working memory and visual attention — Shani Offen, Justin L. Gardner, D. Schluppeck, D. Heeger (2010); cutoff-filter date 2010-09-29; doi:10.1167/10.11.28</summary>

```text
[1] Differential roles for frontal eye fields (FEF) and intraparietal sulcus (IPS) in visual working memory and visual attention
    id: s2:316c4f0568484ef0f0897d4622b2262e6517ece5
    date: 2010-09-29
    venue: Journal of Vision
    authors: Shani Offen, Justin L. Gardner, D. Schluppeck, D. Heeger
    abstract: Cortical activity was measured with functional magnetic resonance imaging to probe the involvement of the superior precentral sulcus (including putative human frontal eye fields, FEF) and the intraparietal sulcus (IPS) in visual short term memory and visual attention. In two experimental tasks, human subjects viewed two visual stimuli separated by a variable delay period. The tasks placed differential demands on short-term memory and attention, but the stimuli were visually identical until after the delay period. An earlier study (Offen, Schluppeck, & Heeger, 2009) had found a dissociation in early visual cortex that suggested different computational mechanisms underlying the two processes. In contrast, the results reported here show that the patterns of activation in prefrontal and parietal cortex were different from one another but were similar for the two tasks. In particular, the FEF showed evidence for sustained delay-period activity for both the working memory and the attention task, while the IPS did not show evidence for sustained delay-period activity for either task. The results imply differential roles for the FEF and IPS in these tasks; the results also suggest that feedback of sustained activity from frontal cortex to visual cortex might be gated by task demands.
```
</details>

<details><summary>[2] Listening to polyphonic music recruits domain-general attention and working memory circuits — Petr Janata, B. Tillmann, J. Bharucha (2002); cutoff-filter date 2002-06-01; doi:10.3758/cabn.2.2.121</summary>

```text
[2] Listening to polyphonic music recruits domain-general attention and working memory circuits
    id: s2:2fededbe97de622b55ff2358028975741c053635
    date: 2002-06-01
    venue: Cognitive, Affective, & Behavioral Neuroscience
    authors: Petr Janata, B. Tillmann, J. Bharucha
    abstract: [no abstract available]
```
</details>

<details><summary>[3] Topographic maps in human frontal cortex revealed in memory-guided saccade and spatial working-memory tasks. — S. Kastner, Kevin DeSimone, Christina S. Konen, S. Szczepanski et al. (2007); cutoff-filter date 2007-05-01; doi:10.1152/jn.00010.2007</summary>

```text
[3] Topographic maps in human frontal cortex revealed in memory-guided saccade and spatial working-memory tasks.
    id: s2:63f4a50dd409b284c11e747fdc0e63d8db1327f0
    date: 2007-05-01
    venue: Journal of Neurophysiology
    authors: S. Kastner, Kevin DeSimone, Christina S. Konen, S. Szczepanski, K. Weiner, K. Schneider
    abstract: [no abstract available]
```
</details>

<details><summary>[4] Practice‐related functional activation changes in a working memory task — H. Garavan, Dan Kelley, Allyson Rosen, Stephen M. Rao et al. (2000); cutoff-filter date 2000-10-01; doi:10.1002/1097-0029(20001001)51:1<54::aid-jemt6>3.0.co;2-j</summary>

```text
[4] Practice‐related functional activation changes in a working memory task
    id: s2:2ef334a0ef86f1525ebad76efdb110844d150448
    date: 2000-10-01
    venue: Microscopy research and technique (Print)
    authors: H. Garavan, Dan Kelley, Allyson Rosen, Stephen M. Rao, E. Stein
    abstract: [no abstract available]
```
</details>

<details><summary>[5] Neural basis for dynamic updating of object representation in visual working memory — S. Takahama, S. Miyauchi, J. Saiki (2010); cutoff-filter date 2010-02-15; doi:10.1016/j.neuroimage.2009.11.029</summary>

```text
[5] Neural basis for dynamic updating of object representation in visual working memory
    id: s2:a60233a8c4b358e85656ef94ed3440e6e153d7a6
    date: 2010-02-15
    venue: NeuroImage
    authors: S. Takahama, S. Miyauchi, J. Saiki
    abstract: [no abstract available]
```
</details>

<details><summary>[6] Load response functions in the human spatial working memory circuit during location memory updating — Hoi-Chung Leung, Hwamee Oh, J. Ferri, Yu-Ji Yi (2007); cutoff-filter date 2007-03-01; doi:10.1016/j.neuroimage.2006.12.012</summary>

```text
[6] Load response functions in the human spatial working memory circuit during location memory updating
    id: s2:3a996621a547e6f8d847fc15e1eaadedf017d69f
    date: 2007-03-01
    venue: NeuroImage
    authors: Hoi-Chung Leung, Hwamee Oh, J. Ferri, Yu-Ji Yi
    abstract: [no abstract available]
```
</details>

<details><summary>[7] Interference resolution in spatial working memory — Hoi-Chung Leung, John X. Zhang (2004); cutoff-filter date 2004-11-01; doi:10.1016/j.neuroimage.2004.07.053</summary>

```text
[7] Interference resolution in spatial working memory
    id: s2:c427edccd1b01d12795af538c4a85982c6eb18f0
    date: 2004-11-01
    venue: NeuroImage
    authors: Hoi-Chung Leung, John X. Zhang
    abstract: [no abstract available]
```
</details>

<details><summary>[8] Gradients of functional organization in posterior parietal cortex revealed by visual attention, visual short-term memory, and intrinsic functional connectivity — Ray W. Lefco, James A. Brissenden, Abigail L. Noyce, Sean M. Tobyne et al. (2020); cutoff-filter date 2020-06-08; doi:10.1016/j.neuroimage.2020.117029</summary>

```text
[8] Gradients of functional organization in posterior parietal cortex revealed by visual attention, visual short-term memory, and intrinsic functional connectivity
    id: s2:4f4d4288b547d3eb432223c5ef545580d129b2df
    date: 2020-06-08
    venue: NeuroImage
    authors: Ray W. Lefco, James A. Brissenden, Abigail L. Noyce, Sean M. Tobyne, D. Somers
    abstract: Visual attention and visual working memory tasks recruit a common network of lateral frontal cortical (LFC) and posterior parietal cortical (PPC) regions. Here, we examine finer-scale organization of this frontoparietal network. Three LFC regions recruited by visual cognition tasks, superior precentral sulcus (sPCS), inferior precentral sulcus (iPCS), and mid inferior frontal sulcus (midIFS) exhibit differential patterns of resting-state functional connectivity to PPC. A broad dorsomedial to ventrolateral gradient is observed, with sPCS connectivity dominating in the dorsomedial PPC band, iPCS dominating in the middle band, and midIFS dominating in the ventrolateral band. These connectivity-defined subregions of PPC capture differential task activation between a pair of visual attention and working memory tasks. The relative functional connectivity of sPCS and iPCS also varies along the rostral-caudal axis of the retinotopic regions of PPC. iPCS connectivity is relatively stronger near the IPS0/IPS1 and IPS2/IPS3 borders, especially on the lateral portions of these borders, which each preferentially encode central visual field representations. In contrast, sPCS connectivity is relatively stronger elsewhere in retinotopic IPS regions which preferentially encode peripheral visual field representations. These findings reveal fine-scale gradients in functional connectivity within the frontoparietal visual network that capture a high-degree of specificity in PPC functional organization.
```
</details>

<details><summary>[9] Accurate localization and coactivation profiles of the frontal eye field and inferior frontal junction: an ALE and MACM fMRI meta-analysis — M. Bedini, E. Olivetti, P. Avesani, D. Baldauf (2023); cutoff-filter date 2023-04-24; doi:10.1007/s00429-023-02641-y</summary>

```text
[9] Accurate localization and coactivation profiles of the frontal eye field and inferior frontal junction: an ALE and MACM fMRI meta-analysis
    id: s2:77cfa7be466a6728ecaa1a4701678121758cc3f4
    date: 2023-02-04
    venue: bioRxiv (preprint)
    authors: M. Bedini, E. Olivetti, P. Avesani, D. Baldauf
    abstract: The frontal eye field (FEF) and the inferior frontal junction (IFJ) are prefrontal structures involved in mediating multiple aspects of goal-driven behavior. Despite being recognized as prominent nodes of the networks underlying spatial attention and oculomotor control, and working memory and cognitive control, respectively, the limited quantitative evidence on their precise localization has considerably impeded the detailed understanding of their structure and connectivity. In this study, we performed an activation likelihood estimation (ALE) fMRI meta-analysis by selecting studies that employed standard paradigms to accurately infer the localization of these regions in stereotaxic space. For the FEF, we found the highest spatial convergence of activations for prosaccade and antisaccade paradigms at the junction of the precentral sulcus and superior frontal sulcus. For the IFJ, we found consistent activations across oddball/attention, working memory, task-switching and Stroop paradigms at the junction of the inferior precentral sulcus and inferior frontal sulcus. We related these clusters to previous meta-analyses, sulcal/gyral neuroanatomy, and a comprehensive brain parcellation, highlighting important differences compared to their results and taxonomy. Finally, we leveraged the ALE peak coordinates as seeds to perform a meta-analytic connectivity modeling (MACM) analysis, which revealed systematic coactivation patterns spanning the frontal, parietal, and temporal cortices. We decoded the behavioral domains associated with these coactivations, suggesting that these may allow FEF and IFJ to support their specialized roles in flexible behavior. Our study provides the meta-analytic groundwork for investigating the relationship between functional specialization and connectivity of two crucial control structures of the prefrontal cortex.
```
</details>

<details><summary>[10] **KEY** Prioritized maps of space in human frontoparietal cortex — T. Jerde, E. Merriam, Adam C. Riggall, J. H. Hedges et al. (2012); cutoff-filter date 2012-11-28; doi:10.1523/jneurosci.3810-12.2012</summary>

```text
[10] Prioritized maps of space in human frontoparietal cortex
    id: s2:7aec191731033d7436cbb0a3bc09673d98c411e9
    date: 2012-11-28
    venue: Journal of Neuroscience
    authors: T. Jerde, E. Merriam, Adam C. Riggall, J. H. Hedges, C. Curtis
    abstract: Priority maps are theorized to be composed of large populations of neurons organized topographically into a map of gaze-centered space whose activity spatially tags salient and behaviorally relevant information. Here, we identified four priority map candidates along human posterior intraparietal sulcus (IPS0–IPS3) and two along the precentral sulcus (PCS) that contained reliable retinotopically organized maps of contralateral visual space. Persistent activity increased from posterior-to-anterior IPS areas and from inferior-to-superior PCS areas during the maintenance of a working memory representation, the maintenance of covert attention, and the maintenance of a saccade plan. Moreover, decoders trained to predict the locations on one task (e.g., working memory) cross-predicted the locations on other tasks (e.g., attention) in superior PCS and IPS2, suggesting that these patterns of maintenance activity may be interchangeable across the tasks. Such properties make these two areas in frontal and parietal cortex viable priority map candidates.
```
</details>

<details><summary>Post-hoc automated audit — NON-AUTHORITATIVE; uses hidden benchmark annotations</summary>

- primary auditor: `silence_as_null_error`; statuses {'H1': 'positive_or_present', 'H2': 'indeterminate'}; discriminative=False
- primary reasoning: H1 directly predicts that persistent activity in lateral PFC (sPCS) represents mnemonic content, as it posits PFC as a storage substrate. H2 is silent on whether persistent activity in PFC represents item identity, as it only claims PFC controls or prioritizes representations stored elsewhere, not that it encodes the content itself.
- derived opposition call: `manufactured_from_silence`
- evidence attribution: `informative_evidence_found` — The retrieval surfaced a paper (record [10]) that directly reports persistent activity in the superior precentral sulcus during working memory maintenance and shows that this activity encodes the location of visual items. The assessor correctly identified this as supporting evidence for the proposition. The process worked as intended.
- auditor retest: `silence_as_null_error`; discriminative=False
- disagreement flags: {'second_rater_vs_primary_discriminative': None, 'second_rater_vs_primary_status': None, 'retest_vs_primary_category': False, 'any': False}
</details>

**Human review** — `evidence_construct_mismatch` · reviewer: Research Director · source: D045 · status: `first_pass_model_based_review` · genuinely discriminative: False · silence-as-null error: False · other fields not recorded

---

## #36 · `GP1-forest_fragmentation_resilience-X15`

**GP1-forest_fragmentation_resilience-X15** — case `forest_fragmentation_resilience`, node `X15`

> Forest edge environments in fragmented landscapes tend to support higher plant productivity than interior environments.

- generated from **H2** (Candidate A); abstraction: `class`
- generator's stated reason: If increased light at edges enhances growth rates, then edge environments across fragmented forests should generally show higher productivity than interiors.
- influence: **0.192** (rank 7 in case, 36 overall; cumulative 76%) — favours **H2**
- log-likelihood contribution: H2 +1.954, H1 +1.762
- removing it alone: evidence withheld → case log-odds -1.823 (ranking unchanged); node deleted → -1.823 (ranking unchanged)

**Hypotheses (as shown to the verifier)**

- **H1** (Candidate B): Fragmentation increases exposure to heat, atmospheric dryness, wind, and drought stress, raising mortality and reducing ecosystem resilience, especially where water/heat stress dominates.
- **H2** (Candidate A): Edge formation can increase light availability and relax limiting-resource constraints, increasing growth, biomass, recovery capacity, and potentially resilience where climatic stress penalties are small enough.

**Verifier cross-hypothesis judgments** — P(X|H) combines these by noisy-OR

| hypothesis | origin? | direct edge | route via parent | P(X\|H) |
| --- | --- | --- | --- | --- |
| H2 | yes | `implied` | X2 [H→parent `implied`, P=0.80] → `implied` | 0.948 |
| H1 | no | `unlikely` | X2 [H→parent `neutral`, P=0.50] → `implied` | 0.755 |

- edge rationale, **H2** → node: Candidate A states that edge formation can increase light and relax resource constraints, leading to increased growth and biomass, which clearly supports higher productivity at edges.
- edge rationale, **H1** → node: Candidate B argues that fragmentation increases stress and reduces resilience and productivity, especially at edges, making higher productivity at edges less likely.
- parent `X2`: Increased light availability at forest edges enhances plant growth rates by reducing resource limitation.
- chain rationale, `X2` → node: If increased light at forest edges enhances plant growth rates, it is reasonable to infer that edge environments generally support higher plant productivity than interiors, though other factors may also play a role.

**Verifier evidence** — label used in score: `strong_support` (log-LR +2.0)

- queries: `forest edge plant productivity`; `fragmented landscape interior plant biomass`
- assessor rationale: Record [2] directly compares plant productivity between forest edge and interior environments, finding higher productivity at the edge. It also explicitly states that increasing forest edges can increase productivity. No other records directly address this proposition. The evidence is methodologically strong, based on direct measurements of tree growth and stand volume across edge and interior plots, and represents an independent study.
- supporting spans cited by the assessor:
  - "The results showed that DBH (tree diameter at the breast height), tree height and stand volume in overstory increased from the central areas (CA) of forests to the edge areas (EA), and the plant species richness and diversity in understory were greater in EA than in CA."
  - "Our results suggest increasing forest productivity and plant species diversity could be achieved by making more edges in the forests."
- 10 papers shown; key papers: `s2:98ce68c812706ad0d936bc75fdb0203e1b6793b0`
- _The evidence assessor returns ONE label for the node from all papers shown; the method has no per-paper contribution. Key papers and spans are those the assessor cited._

<details><summary>[1] Effects of Geomorphological Processes and Phytoclimate Conditions Change on Forest Vegetation in the Pomeranian Bay Coastal Zone (Wolin National Park, West Pomerania) — J. Tylkowski, R. Paluszkiewicz, M. Winowski, Paweł Czyryca et al. (2023); cutoff-filter date 2023-03-31; doi:10.14746/quageo-2023-0010</summary>

```text
[1] Effects of Geomorphological Processes and Phytoclimate Conditions Change on Forest Vegetation in the Pomeranian Bay Coastal Zone (Wolin National Park, West Pomerania)
    id: s2:a575c732e06905662b8650f9c082dd811ff5c2ac
    date: 2023-02-07
    venue: Quaestiones Geographicae
    authors: J. Tylkowski, R. Paluszkiewicz, M. Winowski, Paweł Czyryca, A. Kostrzewski, M. Mazurek, G. Rachlewicz
    abstract: Abstract The functioning of plant associations, including forest associations, in the coastal cliff edge zone of the Pomeranian Bay in the Wolin National Park (WNP) is determined by short-term factors related to the dynamics of erosion and denudation processes and long-term phytoclimatic conditions' changes. The study presents a temporary analysis of the occurrence of sea abrasion and water and aeolian erosion, based on the applied hydrometeorological threshold values. The influence of changes in phytoclimatic conditions on the development and productivity of coastal forests with the dominant species of Fagus sylvatica was also presented. Assessments of spatial susceptibility to erosion of the cliff coast and the existing plant associations were also carried out in conditions of the risk of coast erosion. It was found that 55% of the cliff edge zone of the Pomeranian Bay of the WNP and the forest associations (mainly Luzulo pilosae-Fagetum) occurring there are in the zone of particular risk of increased erosion and denudation processes. In addition, unfavourable trends in changes in phytoclimatic conditions in the 21st century were found, which reflect climate changes unfavourable to the development of beech forests on Wolin Island.
```
</details>

<details><summary>[2] **KEY** Edge Effects on Tree Growth and Species Diversity in Forests of Different Types and Ages — Ji-Ping Li, Chun-Zhou Zhao, Yuan Peng, Yuan-Jie Hu et al. (2018); cutoff-filter date 2018-09-01; doi:10.3161/15052249pje2018.66.3.004</summary>

```text
[2] Edge Effects on Tree Growth and Species Diversity in Forests of Different Types and Ages
    id: s2:98ce68c812706ad0d936bc75fdb0203e1b6793b0
    date: 2018-09-01
    venue: Polish Journal of Ecology
    authors: Ji-Ping Li, Chun-Zhou Zhao, Yuan Peng, Yuan-Jie Hu, Xiao-Hong Yuan
    abstract: ABSTRACT Edge to interior gradients in forest ecosystems can influence the species composition and community structure as a result of variations in micro-environment. In this study, the edge effects on stand productivity and plant species diversity were investigated in two adjacent types of forests in central-southern China: Chinese fir adjacent with pine forests and Chinese fir adjacent with broad-leaved forests. A total of 48 sample plots for overstory and 240 sample quadrates for understory in different stand ages were set up. The tree growth parameters were measured in the overstory while the plant species diversity was measured in both overstory and understory of the examined forests. The results showed that DBH (tree diameter at the breast height), tree height and stand volume in overstory increased from the central areas (CA) of forests to the edge areas (EA), and the plant species richness and diversity in understory were greater in EA than in CA. The edge effect was greater in Chinese fir paired with broad-leaved forests than in Chinese fir paired with pine forests. The edge effect decreased in an order as young aged stands > middle aged stands > mature aged stands in the studied forests. The changes in tree growth and species diversity in the edge area compared to the interior were mainly attributed to the alteration of micro-environmental factors such as light density, temperature and moisture. Our results suggest increasing forest productivity and plant species diversity could be achieved by making more edges in the forests.
```
</details>

<details><summary>[3] Effects of anthropogenic fragmentation on primary productivity and soil carbon storage in temperate mountain grasslands — Emilia Ionela Cojoc, C. Postolache, B. Olariu, C. Beierkuhnlein (2016); cutoff-filter date 2016-11-07; doi:10.1007/s10661-016-5667-7</summary>

```text
[3] Effects of anthropogenic fragmentation on primary productivity and soil carbon storage in temperate mountain grasslands
    id: s2:db6babc2d036d0803d1552e7e4963dbe64293250
    date: 2016-11-07
    venue: Environmental Monitoring & Assessment
    authors: Emilia Ionela Cojoc, C. Postolache, B. Olariu, C. Beierkuhnlein
    abstract: [no abstract available]
```
</details>

<details><summary>[4] Phosphorus speciation and C:N:P stoichiometry of functional organic matter fractions in temperate forest soils — Simon Stahr, Markus Graf‐Rosenfellner, W. Klysubun, R. Mikutta et al. (2017); cutoff-filter date 2017-09-13; doi:10.1007/s11104-017-3394-7</summary>

```text
[4] Phosphorus speciation and C:N:P stoichiometry of functional organic matter fractions in temperate forest soils
    id: s2:6e1c6bb3d94ea81401461f2c18693ab02973dcc6
    date: 2017-09-13
    venue: Plant and Soil
    authors: Simon Stahr, Markus Graf‐Rosenfellner, W. Klysubun, R. Mikutta, J. Prietzel, F. Lang
    abstract: [no abstract available]
```
</details>

<details><summary>[5] Seaweeds: Their Productivity and Strategy for Growth — K. H. Mann (1973); cutoff-filter date 1973-12-07; doi:10.1126/science.182.4116.975</summary>

```text
[5] Seaweeds: Their Productivity and Strategy for Growth
    id: s2:d20bd1ef3788504ebd37a788ef2f76d4676f1624
    date: 1973-12-07
    venue: Science
    authors: K. H. Mann
    abstract: [no abstract available]
```
</details>

<details><summary>[6] SCALE-DEPENDENT EFFECTS OF FOREST EDGES ON MOUNTAIN GRASSLAND BIOGEOCHEMISTRY — Emilia Ionela Cojoc, A. Schweiger, C. Postolache, C. Beierkuhnlein (2020); cutoff-filter date 2020-12-31; doi:10.30638/eemj.2020.112</summary>

```text
[6] SCALE-DEPENDENT EFFECTS OF FOREST EDGES ON MOUNTAIN GRASSLAND BIOGEOCHEMISTRY
    id: s2:6a7a61fdbc14f92e6f6b877e40c95d6c60d986a2
    date: 2020
    venue: Environmental Engineering and Management Journal
    authors: Emilia Ionela Cojoc, A. Schweiger, C. Postolache, C. Beierkuhnlein
    abstract: Current landscapes have been intensively modified by humans and forest fragmentation has created substantial increases of forest edges. So far, scale-dependence between observable ecological patterns and the underlying processes affected by forest fragmentation have been widely ignored. To overcome the widespread ambiguity in selecting relevant spatial scales for studying the ecological effects of forest fragmentation, we investigated the effect of forest prevalence and edge length on carbon stocks, organic matter and plant-available nutrients (nitrate and ammonium) across varying spatial scales in a temperate mountainous grassland landscape of Romania. We calculated forest prevalence and edge length in the surroundings of 60 grassland plots with different spatial extents and quantified the effects of both factors on grassland productivity and soil biogeochemistry. We found a strong decreasing effect of forest edge length on soil carbon stock and organic matter and a contrasting increased effect on plantavailable nutrients in the range of 100 m to 300 m radius, particularly for nitrate in the first 150 m (marginal r2=0.22 ± 0.02, p<0.1). As the scale increased, we identified either an increasing tendency for carbon stock, organic matter and plant-available nutrients or an almost constant effect across the range of scales. Grassland above-ground biomass showed no clear trend with scale. In this study, we observed that the effect of forest prevalence and edge length on grassland soil biogeochemistry and productivity strongly varied with the spatial scale of investigation. Such profound scale-dependence of key ecosystem properties must be considered in management strategies aiming for sustainable ecosystem functioning.
```
</details>

<details><summary>[7] Changes in Root–Shoot Allometric Relations in Alpine Norway Spruce Trees After Strip Cutting — P. Nikolova, Jani Geyer, P. Brang, P. Cherubini et al. (2021); cutoff-filter date 2021-08-27; doi:10.3389/fpls.2021.703674</summary>

```text
[7] Changes in Root–Shoot Allometric Relations in Alpine Norway Spruce Trees After Strip Cutting
    id: s2:44dfc50625bb77108af5eb9a85b8a98af6323775
    date: 2021-08-27
    venue: Frontiers in Plant Science
    authors: P. Nikolova, Jani Geyer, P. Brang, P. Cherubini, S. Zimmermann, H. Gärtner
    abstract: Silvicultural interventions such as strip cuttings can change the resource availability of the edge trees. This may alter tree allometry, as light regime, water, and nutrient availability can change at the forest edge. Increased root growth may optimize resource uptake and/or enhance tree anchorage to withstand the altered wind regime. However, little is known about the patterns of the root–shoot allometric responses to strip cuttings. In three alpine stands differing in climate, site productivity, and stand characteristics, we selected 71 Norway spruce trees and took increment cores from stems, root collars, and main roots. This enabled us to study changes in the long-term root-stem allometry for 46 years and short-term allometric responses to intervention. The effects of cutting were compared between edge trees and trees from the stand interior in 10 years before and after the intervention. The long-term allocation to roots increased with stem diameter, with the strongest effects on the regularly managed stand with the tallest and largest trees. These results support the allometric biomass partitioning theory, which postulates resource allocation patterns between different plant organs to depend on plant size. Strip cutting on north-facing slopes boosted edge-tree growth in all plant compartments and enhanced allocation to roots. This change in allometry started 2 years after cutting but disappeared 7–8 years later. In the post-cutting period, the highest root–shoot increase was observed in the small trees independent of the site. This indicates the change in growing conditions to have the strongest effects in formerly suppressed trees. Thus, the effect of such acclimation on the wind firmness of subdominant spruce trees is a question with high importance for optimizing cutting layouts in lowering post-cutting vulnerability to disturbance. The results from this case study contribute to a better understanding of the structural acclimation of spruce trees from high- [...]
```
</details>

<details><summary>[8] Patch-size effects on early succession in southern Appalachian forests. — D. Phillips, D. J. Shure (1990); cutoff-filter date 1990-02-28; doi:10.2307/1940260</summary>

```text
[8] Patch-size effects on early succession in southern Appalachian forests.
    id: s2:8893f65ce05a69499e9ca2268f624ddef72bdadb
    date: 1990-02-01
    venue: Ecology
    authors: D. Phillips, D. J. Shure
    abstract: [no abstract available]
```
</details>

<details><summary>[9] Gap size and succession in cutover southern Appalachian forests: an 18 year study of vegetation dynamics — D. J. Shure, D. Phillips, P. Edward Bostick (2006); cutoff-filter date 2006-03-01; doi:10.1007/s11258-006-9105-8</summary>

```text
[9] Gap size and succession in cutover southern Appalachian forests: an 18 year study of vegetation dynamics
    id: s2:8515306e7c92701cf0b985fb3d21eaea33c5c901
    date: 2006-03-01
    venue: Plant Ecology
    authors: D. J. Shure, D. Phillips, P. Edward Bostick
    abstract: [no abstract available]
```
</details>

<details><summary>[10] Key-factors and key-stages that determine the leaf longevity of an evergreen broad-leaved tree, Neolitsea sericea (Lauraceae) at different growing sites in southern Japan — J. Yukawa, K. Yamamura, K. Fujimoto, M. Tokuda et al. (2017); cutoff-filter date 2017-12-31; doi:10.1007/s11284-017-1525-5</summary>

```text
[10] Key-factors and key-stages that determine the leaf longevity of an evergreen broad-leaved tree, Neolitsea sericea (Lauraceae) at different growing sites in southern Japan
    id: s2:de52cd9ca68b46562cdde2d7b4388f1b1b014ad1
    date: 2017
    venue: Ecological research
    authors: J. Yukawa, K. Yamamura, K. Fujimoto, M. Tokuda, Shunichiro Muroya, Tsukasa Maki, Toshiaki Sadoshima, T. Fukuda
    abstract: [no abstract available]
```
</details>

<details><summary>Post-hoc automated audit — NON-AUTHORITATIVE; uses hidden benchmark annotations</summary>

- primary auditor: `silence_as_null_error`; statuses {'H2': 'positive_or_present', 'H1': 'indeterminate'}; discriminative=False
- primary reasoning: H2 explicitly predicts that increased light at edges should enhance growth and productivity, so it implies higher productivity at edges. H1 focuses on increased stress and mortality but does not specifically predict whether edge environments have higher or lower productivity than interiors, so it is indeterminate.
- derived opposition call: `manufactured_from_silence`
- evidence attribution: `informative_evidence_found` — The retrieval system surfaced a paper (record [2]) that directly and methodologically addresses the proposition, comparing plant productivity at forest edges versus interiors and finding higher productivity at the edge. The assessor correctly identified and used this evidence. The queries were appropriate and the process worked as intended.
- disagreement flags: {'second_rater_vs_primary_discriminative': None, 'second_rater_vs_primary_status': None, 'retest_vs_primary_category': None, 'any': False}
</details>

**Human review** — `invalid_or_weak_implication` · reviewer: Research Director · source: D045 · status: `first_pass_model_based_review` · genuinely discriminative: False · silence-as-null error: False · other fields not recorded

---

## #37 · `GP1-gcn4_med15_complex_vs_condensate-X18`

**GP1-gcn4_med15_complex_vs_condensate-X18** — case `gcn4_med15_complex_vs_condensate`, node `X18`

> Phase separation between transcription factors and coactivator complexes facilitates transcriptional activation in eukaryotic cells.

- generated from **H2** (Candidate B); abstraction: `class`
- generator's stated reason: If phase separation between activation domains and Mediator subunits recruits Mediator, then similar phase separation events between other transcription factors and coactivators should also facilitate activation.
- influence: **0.192** (rank 3 in case, 37 overall; cumulative 77%) — favours **H2**
- log-likelihood contribution: H1 +1.762, H2 +1.954
- removing it alone: evidence withheld → case log-odds +0.187 (ranking CHANGES); node deleted → +0.187 (ranking CHANGES)

**Hypotheses (as shown to the verifier)**

- **H1** (Candidate A): Gcn4 activation domains activate transcription through dynamic multivalent contacts with Med15 activation-binding domains in soluble complexes; transcriptional activity should therefore track productive Gcn4-Med15 molecular binding/affinity even outside a condensed phase.
- **H2** (Candidate B): Gcn4 activation domains can activate transcription through phase-separation capacity and co-condensation with Mediator/Med15; transcriptional output should therefore track co-phase-separation/Med15 recruitment into condensates under the proposed condensate mechanism.

**Verifier cross-hypothesis judgments** — P(X|H) combines these by noisy-OR

| hypothesis | origin? | direct edge | route via parent | P(X\|H) |
| --- | --- | --- | --- | --- |
| H1 | no | `unlikely` | X5 [H→parent `neutral`, P=0.50] → `implied` | 0.755 |
| H2 | yes | `implied` | X5 [H→parent `implied`, P=0.80] → `implied` | 0.948 |

- edge rationale, **H1** → node: Candidate A posits that transcriptional activation is mediated by soluble complexes and productive binding outside of condensed phases, making phase separation unnecessary or less likely to facilitate activation.
- edge rationale, **H2** → node: Candidate B explicitly links transcriptional activation to phase separation and co-condensation between transcription factors and coactivator complexes, making the proposition clearly expected if B were true.
- parent `X5`: Phase separation between transcription factor activation domains and Mediator subunits facilitates recruitment of Mediator to active gene loci.
- chain rationale, `X5` → node: If phase separation between transcription factor activation domains and Mediator subunits facilitates Mediator recruitment, it is reasonable to infer that similar phase separation between transcription factors and coactivator complexes could facilitate transcriptional activation, though the child statement is broader and less specific.

**Verifier evidence** — label used in score: `strong_support` (log-LR +2.0)

- queries: `transcription factors coactivator phase separation`; `phase separation transcriptional activation eukaryotes`
- assessor rationale: Multiple independent studies directly report that phase separation between transcription factors and coactivator complexes facilitates transcriptional activation in eukaryotic cells. These include evidence of phase-separated condensates formed by transcription factors and coactivators correlating with increased gene expression, and genetic or chemical disruption of phase separation leading to reduced transcriptional activation. The findings span diverse systems, including mammalian, fungal, viral, and synthetic contexts, and consistently link phase separation to transcriptional activation.
- supporting spans cited by the assessor:
  - "Here we report that diverse ADs form phase-separated condensates with the Mediator coactivator. For the OCT4 and GCN4 TFs, we show that the ability to form phase-separated droplets with Mediator in vitro and the ability to activate genes in vivo are dependent on the same amino acid residues."
  - "Phase-separated condensates compartmentalize the transcription apparatus at super-enhancers of key cell-identity genes."
  - "The robust transcription of genes at such SEs is enabled by the formation of phase-separated condensates by transcription factors and coactivators with intrinsically disordered regions."
  - "We demonstrate that foci formation correlates with AR transcriptional activity, as this activity can be modulated by changing cellular foci content chemically or by silencing MED1."
  - "EBNA2 and EBNALP are transcription factors, and the expression of their target genes is suppressed by chemicals that perturb LLPS."
  - "Through epigenomic and transcriptomic analysis, our data indicated that both condensate formation and H3K4me3 binding of SGF29 are essential for establishing its precise chromatin location, recruiting transcriptional factors and co-activators to target specific genomic loci, and initiating the expression of genes associated with senescence, such as CDKN1A ."
  - "biofilm PrLDs promote the formation of phase-separated condensates in the nuclei of live cells, and PrLD mutations that abolish phase separation (such as the removal of aromatic residues) also prevent biofilm formation. Biofilm TF condensates can selectively recruit other TFs through PrLD-PrLD interactions and can co-recruit RNA polymerase II, implicating condensate formation in the assembly of active transcriptional complexes."
  - "we demonstrate that engineered transcription factor droplets form at target promoters and increase gene expression up to fivefold."
- 10 papers shown; key papers: `s2:003435bfefd4c328a2f6100c6a0308265b44aa17`, `s2:3df6dcfd2196421468c12488b5b545dee5817682`, `s2:57e1a73cb97fa845520402bc2ea61f76a808d729`, `s2:66dbf44a170cd1f7de5dcec4447a22fb10986978`, `s2:8b08e4e2ca491e532861ef5c30dad12b5fd20d75`, `s2:dfdd9da45946145fad6c8a616dcb5180e665446e`, `s2:e4f0debfff8b369862f80cc3adec3518a77760c0`
- _The evidence assessor returns ONE label for the node from all papers shown; the method has no per-paper contribution. Key papers and spans are those the assessor cited._

<details><summary>[1] **KEY** Transcription factors activate genes through the phase separation capacity of their activation domains — Ann Boija, Isaac A. Klein, Benjamin R. Sabari, Alessandra Dall’Agnese et al. (2018); cutoff-filter date 2018-11-15; doi:10.1016/j.cell.2018.10.042</summary>

```text
[1] Transcription factors activate genes through the phase separation capacity of their activation domains
    id: s2:e4f0debfff8b369862f80cc3adec3518a77760c0
    date: 2018-11-15
    venue: Cell
    authors: Ann Boija, Isaac A. Klein, Benjamin R. Sabari, Alessandra Dall’Agnese, Eliot L. Coffey, A. V. Zamudio, Charles H. Li, K. Shrinivas
    abstract: Gene expression is controlled by transcription factors (TFs) that consist of DNA-binding domains (DBDs) and activation domains (ADs). The DBDs have been well-characterized, but little is known about the mechanisms by which ADs effect gene activation. Here we report that diverse ADs form phase-separated condensates with the Mediator coactivator. For the OCT4 and GCN4 TFs, we show that the ability to form phase-separated droplets with Mediator in vitro and the ability to activate genes in vivo are dependent on the same amino acid residues. For the estrogen receptor (ER), a ligand-dependent activator, we show that estrogen enhances phase separation with Mediator, again linking phase separation with gene activation. These results suggest that diverse TFs can interact with Mediator through the phase-separating capacity of their ADs and that formation of condensates with Mediator is involved in gene activation.
    note: possibly the same work as s2:a0e4bee89a64f35ecc0bfb974cd06093a96a6681, s2:58d4e827e9b15400aa88ab7767613d7218c5cc7d
```
</details>

<details><summary>[2] **KEY** Coactivator condensation at super-enhancers links phase separation and gene control — Benjamin R. Sabari, Alessandra Dall’Agnese, Ann Boija, Isaac A. Klein et al. (2018); cutoff-filter date 2018-06-21; doi:10.1126/science.aar3958</summary>

```text
[2] Coactivator condensation at super-enhancers links phase separation and gene control
    id: s2:66dbf44a170cd1f7de5dcec4447a22fb10986978
    date: 2018-06-21
    venue: Science
    authors: Benjamin R. Sabari, Alessandra Dall’Agnese, Ann Boija, Isaac A. Klein, Eliot L. Coffey, K. Shrinivas, B. Abraham, N. Hannett
    abstract: Phase separation and gene control Many components of eukaryotic transcription machinery—such as transcription factors and cofactors including BRD4, subunits of the Mediator complex, and RNA polymerase II—contain intrinsically disordered low-complexity domains. Now a conceptual framework connecting the nature and behavior of their interactions to their functions in transcription regulation is emerging (see the Perspective by Plys and Kingston). Chong et al. found that low-complexity domains of transcription factors form concentrated hubs via functionally relevant dynamic, multivalent, and sequence-specific protein-protein interaction. These hubs have the potential to phase-separate at higher concentrations. Indeed, Sabari et al. showed that at super-enhancers, BRD4 and Mediator form liquid-like condensates that compartmentalize and concentrate the transcription apparatus to maintain expression of key cell-identity genes. Cho et al. further revealed the differential sensitivity of Mediator and RNA polymerase II condensates to selective transcription inhibitors and how their dynamic interactions might initiate transcription elongation. Science, this issue p. eaar2555, p. eaar3958, p. 412; see also p. 329 Phase-separated condensates compartmentalize the transcription apparatus at super-enhancers of key cell-identity genes. INTRODUCTION Mammalian genes that play prominent roles in healthy and diseased cellular states are often controlled by special DNA elements called super-enhancers (SEs). SEs are clusters of enhancers that are occupied by an unusually high density of interacting factors and drive higher levels of transcription than most typical enhancers. This high-density assembly at SEs has been shown to exhibit sharp transitions of formation and dissolution, forming in a single nucleation event and collapsing when chromatin factors or nucleation sites are deleted. These features led us to postulate that SEs are phase-separated multimolecular assemblies, also known a [...]
```
</details>

<details><summary>[3] Pharmacological inhibition of SRC-1 phase separation suppresses YAP oncogenic transcription activity — Guangya Zhu, Jingjing Xie, Zhenzhen Fu, Mingliang Wang et al. (2021); cutoff-filter date 2021-04-13; doi:10.1038/s41422-021-00504-x</summary>

```text
[3] Pharmacological inhibition of SRC-1 phase separation suppresses YAP oncogenic transcription activity
    id: s2:d805a2860a45978aac1a4080f9d6761a3b235ee0
    date: 2021-04-13
    venue: Cell Research
    authors: Guangya Zhu, Jingjing Xie, Zhenzhen Fu, Mingliang Wang, Qichen Zhang, Hao He, Zijun Chen, Xingdong Guo
    abstract: [no abstract available]
```
</details>

<details><summary>[4] **KEY** Phase Separation of Epstein-Barr Virus EBNA2 and Its Coactivator EBNALP Controls Gene Expression — Qiu Peng, Lu-Juan Wang, Zailong Qin, Jia Wang et al. (2020); cutoff-filter date 2020-01-15; doi:10.1128/jvi.01771-19</summary>

```text
[4] Phase Separation of Epstein-Barr Virus EBNA2 and Its Coactivator EBNALP Controls Gene Expression
    id: s2:57e1a73cb97fa845520402bc2ea61f76a808d729
    date: 2020-01-15
    venue: Journal of Virology
    authors: Qiu Peng, Lu-Juan Wang, Zailong Qin, Jia Wang, Xiang Zheng, Lingyu Wei, Xiao-Yue Zhang, Xue-Mei Zhang
    abstract: Protein condensates can be assembled via liquid-liquid phase separation (LLPS), a process involving the concentration of molecules in a confined liquid-like compartment. LLPS allows for the compartmentalization and sequestration of materials and can be harnessed as a sensitive strategy for responding to small changes in the environment. This study identified the Epstein-Barr virus (EBV) proteins EBNA2 and EBNALP, which mediate virus and cellular gene transcription, as transcription factors that can form liquid-like condensates at superenhancer sites of MYC and Runx3. This study discovered the first identified LLPS of EBV proteins and emphasized the importance of LLPS in controlling host gene expression. ABSTRACT Biological macromolecule condensates formed by liquid-liquid phase separation (LLPS) have been discovered in recent years to be prevalent in biology. These condensates are involved in diverse processes, including the regulation of gene expression. LLPS of proteins have been found in animal, plant, and bacterial species but have scarcely been identified in viral proteins. Here, we discovered that Epstein-Barr virus (EBV) EBNA2 and EBNALP form nuclear puncta that exhibit properties of liquid-like condensates (or droplets), which are enriched in superenhancers of MYC and Runx3. EBNA2 and EBNALP are transcription factors, and the expression of their target genes is suppressed by chemicals that perturb LLPS. Intrinsically disordered regions (IDRs) of EBNA2 and EBNALP can form phase-separated droplets, and specific proline residues of EBNA2 and EBNALP contribute to droplet formation. These findings offer a foundation for understanding the mechanism by which LLPS, previously determined to be related to the organization of P bodies, membraneless organelles, nucleolus homeostasis, and cell signaling, plays a key role in EBV-host interactions and is involved in regulating host gene expression. This work suggests a novel anti-EBV strategy where developing appropriate d [...]
```
</details>

<details><summary>[5] **KEY** Dynamic phase separation of the androgen receptor and its coactivators key to regulate gene expression — Fan Zhang, M. Biswas, Shabnam Massah, Joseph Lee et al. (2022); cutoff-filter date 2022-12-20; doi:10.1093/nar/gkac1158</summary>

```text
[5] Dynamic phase separation of the androgen receptor and its coactivators key to regulate gene expression
    id: s2:8b08e4e2ca491e532861ef5c30dad12b5fd20d75
    date: 2022-12-20
    venue: Nucleic Acids Research
    authors: Fan Zhang, M. Biswas, Shabnam Massah, Joseph Lee, Shreyas Lingadahalli, Samantha Wong, Christopher Wells, Jane Foo
    abstract: Abstract Numerous cancers, including prostate cancer (PCa), are addicted to transcription programs driven by specific genomic regions known as super-enhancers (SEs). The robust transcription of genes at such SEs is enabled by the formation of phase-separated condensates by transcription factors and coactivators with intrinsically disordered regions. The androgen receptor (AR), the main oncogenic driver in PCa, contains large disordered regions and is co-recruited with the transcriptional coactivator mediator complex subunit 1 (MED1) to SEs in androgen-dependent PCa cells, thereby promoting oncogenic transcriptional programs. In this work, we reveal that full-length AR forms foci with liquid-like properties in different PCa models. We demonstrate that foci formation correlates with AR transcriptional activity, as this activity can be modulated by changing cellular foci content chemically or by silencing MED1. AR ability to phase separate was also validated in vitro by using recombinant full-length AR protein. We also demonstrate that AR antagonists, which suppress transcriptional activity by targeting key regions for homotypic or heterotypic interactions of this receptor, hinder foci formation in PCa cells and phase separation in vitro. Our results suggest that enhanced compartmentalization of AR and coactivators may play an important role in the activation of oncogenic transcription programs in androgen-dependent PCa.
    note: possibly the same work as s2:44582020f21c0bff9dad63db2d2bd02553ba8b76
```
</details>

<details><summary>[6] Abstract 5729: Dynamic phase separation of the androgen receptor and its coactivators to regulate gene expression — Fan Zhang, M. Biswas, Joseph Lee, Shreyas Lingadahalli et al. (2022); cutoff-filter date 2022-06-15; doi:10.1158/1538-7445.am2022-5729</summary>

```text
[6] Abstract 5729: Dynamic phase separation of the androgen receptor and its coactivators to regulate gene expression
    id: s2:44582020f21c0bff9dad63db2d2bd02553ba8b76
    date: 2022-06-15
    venue: Cancer Research
    authors: Fan Zhang, M. Biswas, Joseph Lee, Shreyas Lingadahalli, Samantha Wong, Christopher Wells, N. Saxena, Bei Sun
    abstract: 
 Numerous cancers, including prostate cancer (PCa), have been shown to be addicted to transcription programs driven by specific genomic sites known as superenhancers (SEs). Recently, it has been proposed that the robust transcription of genes at such SEs is enabled by the formation of phase-separated condensates by transcription factors and coactivators with intrinsically disordered regions. The androgen receptor (AR), the main oncogenic driver in PCa, contains large disordered regions and is co-recruited with the transcriptional coactivator MED1 to SEs in androgen-dependent prostate cancer cells, thereby promoting oncogenic transcriptional programs. In this work, we show that AR-rich, liquid-like foci form in prostate cancer models upon androgen stimulation. We reveal that foci formation correlates with AR transcriptional activity, which can be modulated by changing cellular foci content genetically or chemically. We also demonstrate that the transcriptional coactivator MED1 plays an essential role in the formation of transcriptionally active AR-rich foci and that AR antagonists that block cofactor recruitment or DNA binding hinder foci formation and thus AR transcriptional activity. The liquid like properties of the condensates were also validated in-vitro by using recombinant AR protein. Using clinical specimens, we detected the interaction between AR and MED1 in advanced forms of prostate cancer and not in benign tissues. These results suggest that enhanced compartmentalization of AR and coactivators at SEs may play an important role in the activation of oncogenic transcription programs in androgen-dependent PCa. A better understanding of the assembly and the regulation of these AR-rich compartments may provide novel therapeutic options for PCa by targeting downstream events of androgen activation and DNA binding of AR.
 Citation Format: Fan Zhang, Maitree Biswas, Joseph Lee, Shreyas Lingadahalli, Samantha Wong, Christopher Wells, Neetu Saxena, Bei Sun, Ana K. [...]
    note: possibly the same work as s2:8b08e4e2ca491e532861ef5c30dad12b5fd20d75
```
</details>

<details><summary>[7] **KEY** SGF29 nuclear condensates reinforce cellular aging — K. Yan, Qian-Zhao Ji, Dongxin Zhao, Mingheng Li et al. (2023); cutoff-filter date 2023-11-07; doi:10.1038/s41421-023-00602-7</summary>

```text
[7] SGF29 nuclear condensates reinforce cellular aging
    id: s2:003435bfefd4c328a2f6100c6a0308265b44aa17
    date: 2023-11-07
    venue: Cell Discovery
    authors: K. Yan, Qian-Zhao Ji, Dongxin Zhao, Mingheng Li, Xiao-Yan Sun, Ze-Hua Wang, Xiaoqian Liu, Zunpeng Liu
    abstract: Phase separation, a biophysical segregation of subcellular milieus referred as condensates, is known to regulate transcription, but its impacts on physiological processes are less clear. Here, we demonstrate the formation of liquid-like nuclear condensates by SGF29, a component of the SAGA transcriptional coactivator complex, during cellular senescence in human mesenchymal progenitor cells (hMPCs) and fibroblasts. The Arg 207 within the intrinsically disordered region is identified as the key amino acid residue for SGF29 to form phase separation. Through epigenomic and transcriptomic analysis, our data indicated that both condensate formation and H3K4me3 binding of SGF29 are essential for establishing its precise chromatin location, recruiting transcriptional factors and co-activators to target specific genomic loci, and initiating the expression of genes associated with senescence, such as CDKN1A . The formation of SGF29 condensates alone, however, may not be sufficient to drive H3K4me3 binding or achieve transactivation functions. Our study establishes a link between phase separation and aging regulation, highlighting nuclear condensates as a functional unit that facilitate shaping transcriptional landscapes in aging.
```
</details>

<details><summary>[8] **KEY** Filamentation and biofilm formation are regulated by the phase-separation capacity of network transcription factors in Candida albicans — Collin Ganser, Mae I. Staples, Maureen A. Dowell, C. Frazer et al. (2023); cutoff-filter date 2023-12-13; doi:10.1371/journal.ppat.1011833</summary>

```text
[8] Filamentation and biofilm formation are regulated by the phase-separation capacity of network transcription factors in Candida albicans
    id: s2:dfdd9da45946145fad6c8a616dcb5180e665446e
    date: 2023-12-01
    venue: PLoS Pathogens
    authors: Collin Ganser, Mae I. Staples, Maureen A. Dowell, C. Frazer, Joseph Dainis, Shabnam Sircaik, Richard J. Bennett
    abstract: The ability of the fungus Candida albicans to filament and form biofilms contributes to its burden as a leading cause of hospital-acquired infections. Biofilm development involves an interconnected transcriptional regulatory network (TRN) consisting of nine transcription factors (TFs) that bind both to their own regulatory regions and to those of the other network TFs. Here, we show that seven of the nine TFs in the C. albicans biofilm network contain prion-like domains (PrLDs) that have been linked to the ability to form phase-separated condensates. Construction of PrLD mutants in four biofilm TFs reveals that these domains are essential for filamentation and biofilm formation in C. albicans. Moreover, biofilm PrLDs promote the formation of phase-separated condensates in the nuclei of live cells, and PrLD mutations that abolish phase separation (such as the removal of aromatic residues) also prevent biofilm formation. Biofilm TF condensates can selectively recruit other TFs through PrLD-PrLD interactions and can co-recruit RNA polymerase II, implicating condensate formation in the assembly of active transcriptional complexes. Finally, we show that PrLD mutations that block the phase separation of biofilm TFs also prevent filamentation in an in vivo model of gastrointestinal colonization. Together, these studies associate transcriptional condensates with the regulation of filamentation and biofilm formation in C. albicans, and highlight how targeting of PrLD-PrLD interactions could prevent pathogenesis by this species.
```
</details>

<details><summary>[9] **KEY** Liquid-liquid phase separation of light-inducible transcription factors increases transcription activation in mammalian cells and mice — Nils Schneider, Franz-Georg Wieland, Deqiang Kong, A. Fischer et al. (2021); cutoff-filter date 2021-01-01; doi:10.1126/sciadv.abd3568</summary>

```text
[9] Liquid-liquid phase separation of light-inducible transcription factors increases transcription activation in mammalian cells and mice
    id: s2:3df6dcfd2196421468c12488b5b545dee5817682
    date: 2021-01-01
    venue: Science Advances
    authors: Nils Schneider, Franz-Georg Wieland, Deqiang Kong, A. Fischer, M. Hörner, J. Timmer, Haifeng Ye, W. Weber
    abstract: Engineering liquid-liquid phase separation into synthetic and optogenetic transcription factors increases gene expression. Light-inducible gene switches represent a key strategy for the precise manipulation of cellular events in fundamental and applied research. However, the performance of widely used gene switches is limited due to low tissue penetrance and possible phototoxicity of the light stimulus. To overcome these limitations, we engineer optogenetic synthetic transcription factors to undergo liquid-liquid phase separation in close spatial proximity to promoters. Phase separation of constitutive and optogenetic synthetic transcription factors was achieved by incorporation of intrinsically disordered regions. Supported by a quantitative mathematical model, we demonstrate that engineered transcription factor droplets form at target promoters and increase gene expression up to fivefold. This increase in performance was observed in multiple mammalian cells lines as well as in mice following in situ transfection. The results of this work suggest that the introduction of intrinsically disordered domains is a simple yet effective means to boost synthetic transcription factor activity.
```
</details>

<details><summary>[10] Regulated splicing of large exons is linked to phase‐separation of vertebrate transcription factors — Toshihiko Kawachi, A. Masuda, Y. Yamashita, Jun-ichi Takeda et al. (2021); cutoff-filter date 2021-10-04; doi:10.15252/embj.2020107485</summary>

```text
[10] Regulated splicing of large exons is linked to phase‐separation of vertebrate transcription factors
    id: s2:4ca78a852bca09a32a1a4751af0b05de664720f1
    date: 2021-10-04
    venue: EMBO Journal
    authors: Toshihiko Kawachi, A. Masuda, Y. Yamashita, Jun-ichi Takeda, B. Ohkawara, Mikako Ito, K. Ohno
    abstract: Although large exons cannot be readily recognized by the spliceosome, many are evolutionarily conserved and constitutively spliced for inclusion in the processed transcript. Furthermore, whether large exons may be enriched in a certain subset of proteins, or mediate specific functions, has remained unclear. Here, we identify a set of nearly 3,000 SRSF3‐dependent large constitutive exons (S3‐LCEs) in human and mouse cells. These exons are enriched for cytidine‐rich sequence motifs, which bind and recruit the splicing factors hnRNP K and SRSF3. We find that hnRNP K suppresses S3‐LCE splicing, an effect that is mitigated by SRSF3 to thus achieve constitutive splicing of S3‐LCEs. S3‐LCEs are enriched in genes for components of transcription machineries, including mediator and BAF complexes, and frequently contain intrinsically disordered regions (IDRs). In a subset of analyzed S3‐LCE‐containing transcription factors, SRSF3 depletion leads to deletion of the IDRs due to S3‐LCE exon skipping, thereby disrupting phase‐separated assemblies of these factors. Cytidine enrichment in large exons introduces proline/serine codon bias in intrinsically disordered regions and appears to have been evolutionarily acquired in vertebrates. We propose that layered splicing regulation by hnRNP K and SRSF3 ensures proper phase‐separation of these S3‐LCE‐containing transcription factors in vertebrates.
```
</details>

<details><summary>Post-hoc automated audit — NON-AUTHORITATIVE; uses hidden benchmark annotations</summary>

- primary auditor: `silence_as_null_error`; statuses {'H1': 'indeterminate', 'H2': 'positive_or_present'}; discriminative=False
- primary reasoning: H2 (the condensate model) predicts that phase separation between transcription factors and coactivators facilitates transcriptional activation, so the proposition is positive_or_present under H2. H1 (the soluble complex model) does not address the role of phase separation in transcriptional activation in general, so it is indeterminate under H1.
- derived opposition call: `manufactured_from_silence`
- evidence attribution: `informative_evidence_found` — The retrieved papers directly address the proposition, providing experimental evidence that phase separation between transcription factors and coactivator complexes facilitates transcriptional activation in eukaryotic cells. The assessor correctly identified strong support from multiple studies across diverse systems, and the queries were well-constructed to surface this evidence.
- disagreement flags: {'second_rater_vs_primary_discriminative': None, 'second_rater_vs_primary_status': None, 'retest_vs_primary_category': None, 'any': False}
</details>

**Human review** — `generic_component_fact` · reviewer: Research Director · source: D045 · status: `first_pass_model_based_review` · genuinely discriminative: False · silence-as-null error: False · other fields not recorded

---

## #38 · `GP1-gcn4_med15_complex_vs_condensate-X23`

**GP1-gcn4_med15_complex_vs_condensate-X23** — case `gcn4_med15_complex_vs_condensate`, node `X23`

> Acidic activation domains engage Mediator subunits via phase separation mechanisms.

- generated from **H2** (Candidate B); abstraction: `mechanistic`
- generator's stated reason: The claim links transcriptional activation to condensate formation, implying that phase separation is a mechanism by which acidic activation domains interact with Mediator.
- influence: **0.192** (rank 4 in case, 38 overall; cumulative 78%) — favours **H2**
- log-likelihood contribution: H1 +1.762, H2 +1.954
- removing it alone: evidence withheld → case log-odds +0.187 (ranking CHANGES); node deleted → +0.187 (ranking CHANGES)

**Hypotheses (as shown to the verifier)**

- **H1** (Candidate A): Gcn4 activation domains activate transcription through dynamic multivalent contacts with Med15 activation-binding domains in soluble complexes; transcriptional activity should therefore track productive Gcn4-Med15 molecular binding/affinity even outside a condensed phase.
- **H2** (Candidate B): Gcn4 activation domains can activate transcription through phase-separation capacity and co-condensation with Mediator/Med15; transcriptional output should therefore track co-phase-separation/Med15 recruitment into condensates under the proposed condensate mechanism.

**Verifier cross-hypothesis judgments** — P(X|H) combines these by noisy-OR

| hypothesis | origin? | direct edge | route via parent | P(X\|H) |
| --- | --- | --- | --- | --- |
| H1 | no | `unlikely` | X6 [H→parent `neutral`, P=0.50] → `implied` | 0.755 |
| H2 | yes | `implied` | X6 [H→parent `implied`, P=0.80] → `implied` | 0.948 |

- edge rationale, **H1** → node: Candidate A posits that activation occurs via soluble complexes and productive binding outside of condensed phases, making phase separation mechanisms less likely.
- edge rationale, **H2** → node: Candidate B explicitly proposes that activation domains function through phase separation and co-condensation with Mediator, making the proposition clearly expected if B were true.
- parent `X6`: Transcriptional activation by acidic activation domains in yeast correlates with their ability to form condensates with Mediator subunits.
- chain rationale, `X6` → node: The parent suggests a correlation between activation domain function and condensate formation with Mediator, which implies but does not strongly guarantee that phase separation mechanisms are involved in their engagement.

**Verifier evidence** — label used in score: `strong_support` (log-LR +2.0)

- queries: `acidic activation domain Mediator phase separation`; `Mediator subunit phase separation transcription`
- assessor rationale: Record [7] directly states that activation domains (ADs) of transcription factors form phase-separated condensates with Mediator, and that this interaction is dependent on specific amino acid residues in the ADs. It further suggests that diverse transcription factors interact with Mediator via the phase-separating capacity of their ADs, which is consistent with the proposition that acidic activation domains engage Mediator subunits via phase separation mechanisms. No other records directly address this specific interaction.
- supporting spans cited by the assessor:
  - "Here we report that diverse ADs form phase-separated condensates with the Mediator coactivator. For the OCT4 and GCN4 TFs, we show that the ability to form phase-separated droplets with Mediator in vitro and the ability to activate genes in vivo are dependent on the same amino acid residues."
  - "These results suggest that diverse TFs can interact with Mediator through the phase-separating capacity of their ADs and that formation of condensates with Mediator is involved in gene activation."
- 10 papers shown; key papers: `s2:e4f0debfff8b369862f80cc3adec3518a77760c0`
- _The evidence assessor returns ONE label for the node from all papers shown; the method has no per-paper contribution. Key papers and spans are those the assessor cited._

<details><summary>[1] Low amounts of heavy water increase the phase separation propensity of a fragment of the androgen receptor activation domain — S. Bielskutė, C. Garcia-Cabau, Marta Frigolé-Vivas, E. Szulc et al. (2021); cutoff-filter date 2021-05-12; doi:10.1002/pro.4110</summary>

```text
[1] Low amounts of heavy water increase the phase separation propensity of a fragment of the androgen receptor activation domain
    id: s2:6c0b3bf72a8f0fc698c8fd39b947d9d31eebf0f2
    date: 2021-05-12
    venue: Protein Science
    authors: S. Bielskutė, C. Garcia-Cabau, Marta Frigolé-Vivas, E. Szulc, Eva De Mol, Mireia Pesarrodona, Jesús García, X. Salvatella
    abstract: The phase equilibria of intrinsically disordered proteins are exquisitely sensitive to changes in solution conditions and this can be used to investigate the driving forces of phase separation in vitro as well as the biological roles of phase transitions in live cells. Here we investigate how using D2O as co‐solvent in an aqueous buffer changes the phase equilibrium of a fragment of the activation domain of the androgen receptor, a transcription factor that plays a role in the development of the male phenotype and is a therapeutic target for castration resistant prostate cancer. We show how replacing even small fractions of H2O with D2O increases the propensity of this fragment to undergo liquid–liquid phase separation, likely reflecting a stabilization of the hydrophobic interactions that drive condensation. Our results indicate that it is necessary to take this effect into consideration when studying phase separation phenomena with biophysical methods that require using D2O as a co‐solvent. In addition, they suggest that additions of D2O may be used to enhance phase separation phenomena in cells, facilitating their observation.
```
</details>

<details><summary>[2] Driving forces behind phase separation of the carboxy-terminal domain of RNA polymerase II — D. Flores-Solis, Irina P Lushpinskaia, A. Polyansky, Arya Changiarath et al. (2023); cutoff-filter date 2023-09-25; doi:10.1038/s41467-023-41633-8</summary>

```text
[2] Driving forces behind phase separation of the carboxy-terminal domain of RNA polymerase II
    id: s2:aaee213f257d07a3fef6fea56f6fb908eede1543
    date: 2023-09-25
    venue: Nature Communications
    authors: D. Flores-Solis, Irina P Lushpinskaia, A. Polyansky, Arya Changiarath, M. Boehning, Milana Mirkovic, J. Walshe, Lisa M. Pietrek
    abstract: Eukaryotic gene regulation and pre-mRNA transcription depend on the carboxy-terminal domain (CTD) of RNA polymerase (Pol) II. Due to its highly repetitive, intrinsically disordered sequence, the CTD enables clustering and phase separation of Pol II. The molecular interactions that drive CTD phase separation and Pol II clustering are unclear. Here, we show that multivalent interactions involving tyrosine impart temperature- and concentration-dependent self-coacervation of the CTD. NMR spectroscopy, molecular ensemble calculations and all-atom molecular dynamics simulations demonstrate the presence of diverse tyrosine-engaging interactions, including tyrosine-proline contacts, in condensed states of human CTD and other low-complexity proteins. We further show that the network of multivalent interactions involving tyrosine is responsible for the co-recruitment of the human Mediator complex and CTD during phase separation. Our work advances the understanding of the driving forces of CTD phase separation and thus provides the basis to better understand CTD-mediated Pol II clustering in eukaryotic gene transcription.
```
</details>

<details><summary>[3] HP1β carries an acidic linker domain and requires H3K9me3 for phase separation — Weihua Qin, A. Stengl, Enes Ugur, Susanne Leidescher et al. (2021); cutoff-filter date 2021-01-01; doi:10.1080/19491034.2021.1889858</summary>

```text
[3] HP1β carries an acidic linker domain and requires H3K9me3 for phase separation
    id: s2:44ce0f4307f1dca8998ed6b79e3b155c5a7e75a9
    date: 2021-01-01
    venue: The Nucleus
    authors: Weihua Qin, A. Stengl, Enes Ugur, Susanne Leidescher, J. Ryan, M. Cardoso, H. Leonhardt
    abstract: ABSTRACT Liquid-liquid phase separation (LLPS) mediated formation of membraneless organelles has been proposed to coordinate biological processes in space and time. Previously, the formation of phase-separated droplets was described as a unique property of HP1α. Here, we demonstrate that the positive net charge of the intrinsically disordered hinge region (IDR-H) of HP1 proteins is critical for phase separation and that the exchange of four acidic amino acids is sufficient to confer LLPS properties to HP1β. Surprisingly, the addition of mono-nucleosomes promoted H3K9me3-dependent LLPS of HP1β which could be specifically disrupted with methylated but not acetylated H3K9 peptides. HP1β mutants defective in H3K9me3 binding were less efficient in phase separationin vitro and failed to accumulate at heterochromatin in vivo. We propose that multivalent interactions of HP1β with H3K9me3-modified nucleosomes via its chromodomain and dimerization via its chromoshadow domain enable phase separation and contribute to the formation of heterochromatin compartments in vivo.
```
</details>

<details><summary>[4] Niche stiffness sustains cancer stemness via TAZ and NANOG phase separation — Xinwei Liu, Yingying Ye, Li-Ling Zhu, Xiaoyun Xiao et al. (2023); cutoff-filter date 2023-01-16; doi:10.1038/s41467-023-35856-y</summary>

```text
[4] Niche stiffness sustains cancer stemness via TAZ and NANOG phase separation
    id: s2:3e54548c6b3066e2d01edbea46b2b86a754704eb
    date: 2023-01-16
    venue: Nature Communications
    authors: Xinwei Liu, Yingying Ye, Li-Ling Zhu, Xiaoyun Xiao, Boxuan Zhou, Yuanting Gu, Hang Si, Huixin Liang
    abstract: Stromal cells in the tumour microenvironment are reported to regulate cancer stemness via biomechanical signals. Here the authors show that TAZ activated by biomechanical cues enhanced cancer stem cell properties via phase separation with Nanog. Emerging evidence shows that the biomechanical environment is required to support cancer stem cells (CSCs), which play a crucial role in drug resistance. However, how mechanotransduction signals regulate CSCs and its clinical significance has remained unclear. Using clinical-practice ultrasound elastography for patients’ lesions and atomic force microscopy for surgical samples, we reveal that increased matrix stiffness is associated with poor responses to neoadjuvant chemotherapy, worse prognosis, and CSC enrichment in patients with breast cancer. Mechanically, TAZ activated by biomechanics enhances CSC properties via phase separation with NANOG. TAZ-NANOG phase separation, which is dependent on acidic residues in the N-terminal activation domain of NANOG, promotes the transcription of SOX2 and OCT4. Therapeutically, targeting NANOG or TAZ reduces CSCs and enhances the chemosensitivity in vivo. Collectively, this study demonstrated that the phase separation of a pluripotency transcription factor links mechanical cues in the niche to the fate of CSCs.
```
</details>

<details><summary>[5] Low-complexity domain of U1-70K modulates phase separation and aggregation through distinctive basic-acidic motifs — Song Xue, R. Gong, Fanqi He, Yan-Qin Li et al. (2019); cutoff-filter date 2019-11-07; doi:10.1126/sciadv.aax5349</summary>

```text
[5] Low-complexity domain of U1-70K modulates phase separation and aggregation through distinctive basic-acidic motifs
    id: s2:16a7294f4cdd378c4a54fe9937a79cb53866a007
    date: 2019-11-01
    venue: Science Advances
    authors: Song Xue, R. Gong, Fanqi He, Yan-Qin Li, Yunjia Wang, T. Tan, Shi-Zhong Luo
    abstract: A repetitive basic-acidic motif in U1-70K is critical for its phase separation and aggregation. Liquid-liquid phase separation (LLPS) facilitates the formation of functional membraneless organelles and recent reports have linked this phenomenon to protein aggregation in neurodegenerative diseases. Understanding the mechanism of LLPS and its regulation thus promises to shed light on the pathogenesis of these conditions. The RNA-binding protein U1-70K, which aggregates in brains of Alzheimer’s disease patients, is considered a potential target for Alzheimer’s therapy. Here, we report that two fragments in the low-complexity (LC) domain of U1-70K can undergo LLPS. We have demonstrated that the repetitive basic-acidic motifs in these fragments induce nucleotide-independent phase separation and initiate aggregation in vitro. We also have confirmed that LLPS and aggregation occur in vivo and that the content of ampholytic motifs in a protein domain determines the transition between droplets and aggregation, providing insights into the mechanism underlying the formation of diverse assembly states.
```
</details>

<details><summary>[6] Transcription activation is enhanced by multivalent interactions independent of phase separation — Jorge Trojanowski, Lukas Frank, A. Rademacher, Norbert Mücke et al. (2021); cutoff-filter date 2021-01-28; doi:10.1101/2021.01.27.428421</summary>

```text
[6] Transcription activation is enhanced by multivalent interactions independent of phase separation
    id: s2:a05c87c86f0e7e70d4936a3f90afded1bbb7d3c6
    date: 2021-01-28
    venue: bioRxiv (preprint)
    authors: Jorge Trojanowski, Lukas Frank, A. Rademacher, Norbert Mücke, Pranas Grigaitis, K. Rippe
    abstract: Transcription factors (TFs) consist of a DNA binding and an activation domain (AD) that are considered to be independent and exchangeable modules. However, recent studies conclude that also the physico-chemical properties of the AD can control TF assembly at chromatin by driving a phase separation into transcriptional condensates. Here, we dissected transcription activation by comparing different synthetic TFs at a reporter gene array with real-time single-cell fluorescence microscopy readouts. In these experiments, binding site occupancy, residence time and co-activator recruitment in relation to multivalent TF interactions were compared. While phase separation propensity and activation strength of the AD were correlated, the actual formation of liquid-like TF droplets had a neutral or inhibitory effect on transcription activation. Rather, we conclude that multivalent AD mediated interactions increase the transcription activation capacity of a TF by stabilizing chromatin binding and mediating the recruitment of co-activators independent of phase separation.
```
</details>

<details><summary>[7] **KEY** Transcription factors activate genes through the phase separation capacity of their activation domains — Ann Boija, Isaac A. Klein, Benjamin R. Sabari, Alessandra Dall’Agnese et al. (2018); cutoff-filter date 2018-11-15; doi:10.1016/j.cell.2018.10.042</summary>

```text
[7] Transcription factors activate genes through the phase separation capacity of their activation domains
    id: s2:e4f0debfff8b369862f80cc3adec3518a77760c0
    date: 2018-11-15
    venue: Cell
    authors: Ann Boija, Isaac A. Klein, Benjamin R. Sabari, Alessandra Dall’Agnese, Eliot L. Coffey, A. V. Zamudio, Charles H. Li, K. Shrinivas
    abstract: Gene expression is controlled by transcription factors (TFs) that consist of DNA-binding domains (DBDs) and activation domains (ADs). The DBDs have been well-characterized, but little is known about the mechanisms by which ADs effect gene activation. Here we report that diverse ADs form phase-separated condensates with the Mediator coactivator. For the OCT4 and GCN4 TFs, we show that the ability to form phase-separated droplets with Mediator in vitro and the ability to activate genes in vivo are dependent on the same amino acid residues. For the estrogen receptor (ER), a ligand-dependent activator, we show that estrogen enhances phase separation with Mediator, again linking phase separation with gene activation. These results suggest that diverse TFs can interact with Mediator through the phase-separating capacity of their ADs and that formation of condensates with Mediator is involved in gene activation.
```
</details>

<details><summary>[8] Membrane phase separation drives responsive assembly of receptor signaling domains — S. Shelby, Ivan Castello-Serrano, Kathleen C. Wisser, I. Levental et al. (2023); cutoff-filter date 2023-03-30; doi:10.1038/s41589-023-01268-8</summary>

```text
[8] Membrane phase separation drives responsive assembly of receptor signaling domains
    id: s2:3e04e08c5f243a1a6f3209ddca996f54406b08d8
    date: 2023-03-30
    venue: Nature Chemical Biology
    authors: S. Shelby, Ivan Castello-Serrano, Kathleen C. Wisser, I. Levental, S. Veatch
    abstract: Super-resolution imaging detects plasma membrane domains that emerge when receptors are clustered in live B cells. Domain structures arise due to the membrane phase transition and can tune local membrane organization and receptor activation. Plasma membrane heterogeneity has been tied to a litany of cellular functions and is often explained by analogy to membrane phase separation; however, models based on phase separation alone fall short of describing the rich organization available within cell membranes. Here we present comprehensive experimental evidence motivating an updated model of plasma membrane heterogeneity in which membrane domains assemble in response to protein scaffolds. Quantitative super-resolution nanoscopy measurements in live B lymphocytes detect membrane domains that emerge upon clustering B cell receptors (BCRs). These domains enrich and retain membrane proteins based on their preference for the liquid-ordered phase. Unlike phase-separated membranes that consist of binary phases with defined compositions, membrane composition at BCR clusters is modulated through the protein constituents in clusters and the composition of the membrane overall. This tunable domain structure is detected through the variable sorting of membrane probes and impacts the magnitude of BCR activation.
```
</details>

<details><summary>[9] A synergy between site-specific and transient interactions drives the phase separation of a disordered, low-complexity domain — Priyesh Mohanty, J. Shenoy, Azamat Rizuan, José F Mercado-Ortiz et al. (2023); cutoff-filter date 2023-08-14; doi:10.1073/pnas.2305625120</summary>

```text
[9] A synergy between site-specific and transient interactions drives the phase separation of a disordered, low-complexity domain
    id: s2:bd972aa1f604fbfc5d79d28be4457b61d9622a90
    date: 2023-08-14
    venue: Proceedings of the National Academy of Sciences of the United States of America
    authors: Priyesh Mohanty, J. Shenoy, Azamat Rizuan, José F Mercado-Ortiz, N. Fawzi, J. Mittal
    abstract: Significance The RNA-binding protein TDP-43 is a component of neuronal inclusions associated with diseases such as amyotrophic lateral sclerosis, frontotemporal dementia, and Alzheimer’s disease. The C-terminal domain (CTD) of TDP-43 is a disordered, low-complexity domain which is aggregation-prone and undergoes liquid–liquid phase separation (LLPS). CTD contains a hydrophobic, conserved region (CR, aa:319-341) which is α-helical and critical for oligomerization and LLPS. Using multiscale simulations and experiments, we report a noncanonical mechanism of biomolecular recognition wherein transient interactions involving hydrophobic residues in CR flanking regions drive the phase separation of CTD through direct enhancement of site-specific, CR-mediated interactions. Our study uncovers rich, mechanistic insights into CTD phase separation which is essential for understanding TDP-43 function and pathology.
```
</details>

<details><summary>[10] Single-molecule FRET unmasks structural subpopulations and crucial molecular events during FUS low-complexity domain phase separation — A. Joshi, Anuja Walimbe, Anamika Avni, Sandeep K Rai et al. (2023); cutoff-filter date 2023-11-13; doi:10.1038/s41467-023-43225-y</summary>

```text
[10] Single-molecule FRET unmasks structural subpopulations and crucial molecular events during FUS low-complexity domain phase separation
    id: s2:3551396e42b9fa572038a0f61c331a33a43ee425
    date: 2023-11-13
    venue: Nature Communications
    authors: A. Joshi, Anuja Walimbe, Anamika Avni, Sandeep K Rai, Lisha Arora, Snehasis Sarkar, S. Mukhopadhyay
    abstract: Biomolecular condensates formed via phase separation of proteins and nucleic acids are thought to be associated with a wide range of cellular functions and dysfunctions. We dissect critical molecular events associated with phase separation of an intrinsically disordered prion-like low-complexity domain of Fused in Sarcoma by performing single-molecule studies permitting us to access the wealth of molecular information that is skewed in conventional ensemble experiments. Our single-molecule FRET experiments reveal the coexistence of two conformationally distinct subpopulations in the monomeric form. Single-droplet single-molecule FRET studies coupled with fluorescence correlation spectroscopy, picosecond time-resolved fluorescence anisotropy, and vibrational Raman spectroscopy indicate that structural unwinding switches intramolecular interactions into intermolecular contacts allowing the formation of a dynamic network within condensates. A disease-related mutation introduces enhanced structural plasticity engendering greater interchain interactions that can accelerate pathological aggregation. Our findings provide key mechanistic underpinnings of sequence-encoded dynamically-controlled structural unzipping resulting in biological phase separation.
```
</details>

<details><summary>Post-hoc automated audit — NON-AUTHORITATIVE; uses hidden benchmark annotations</summary>

- primary auditor: `silence_as_null_error`; statuses {'H1': 'indeterminate', 'H2': 'positive_or_present'}; discriminative=False
- primary reasoning: H2 directly predicts that acidic activation domains engage Mediator via phase separation mechanisms, as it posits co-condensation as the activation route. H1, which centers on soluble complexes, does not address or exclude phase separation, so it is silent on this proposition.
- derived opposition call: `manufactured_from_silence`
- evidence attribution: `informative_evidence_found` — The retrieved literature included a paper (record [7]) that directly addresses the proposition, providing evidence that acidic activation domains of transcription factors interact with Mediator via phase separation mechanisms. The assessor correctly identified and used this evidence. The process worked as intended.
- disagreement flags: {'second_rater_vs_primary_discriminative': None, 'second_rater_vs_primary_status': None, 'retest_vs_primary_category': None, 'any': False}
</details>

**Human review** — `generic_component_fact` · reviewer: Research Director · source: D045 · status: `first_pass_model_based_review` · genuinely discriminative: False · silence-as-null error: False · other fields not recorded

---

## #39 · `GP1-gcn4_med15_complex_vs_condensate-X9`

**GP1-gcn4_med15_complex_vs_condensate-X9** — case `gcn4_med15_complex_vs_condensate`, node `X9`

> Soluble, dynamic protein-protein interactions between transcription factors and Mediator subunits are sufficient for transcriptional activation.

- generated from **H1** (Candidate A); abstraction: `mechanistic`
- generator's stated reason: The claim that Gcn4 activates transcription without condensate formation implies that dynamic, non-condensate interactions can drive activation.
- influence: **0.187** (rank 5 in case, 39 overall; cumulative 79%) — favours **H1**
- log-likelihood contribution: H1 +1.163, H2 +0.976
- removing it alone: evidence withheld → case log-odds -0.192 (ranking unchanged); node deleted → -0.192 (ranking unchanged)

**Hypotheses (as shown to the verifier)**

- **H1** (Candidate A): Gcn4 activation domains activate transcription through dynamic multivalent contacts with Med15 activation-binding domains in soluble complexes; transcriptional activity should therefore track productive Gcn4-Med15 molecular binding/affinity even outside a condensed phase.
- **H2** (Candidate B): Gcn4 activation domains can activate transcription through phase-separation capacity and co-condensation with Mediator/Med15; transcriptional output should therefore track co-phase-separation/Med15 recruitment into condensates under the proposed condensate mechanism.

**Verifier cross-hypothesis judgments** — P(X|H) combines these by noisy-OR

| hypothesis | origin? | direct edge | route via parent | P(X\|H) |
| --- | --- | --- | --- | --- |
| H1 | yes | `implied` | X1 [H→parent `implied`, P=0.80] → `implied` | 0.948 |
| H2 | no | `unlikely` | X1 [H→parent `unlikely`, P=0.30] → `implied` | 0.713 |

- edge rationale, **H1** → node: Candidate A posits that soluble, dynamic interactions between Gcn4 and Med15 are sufficient for transcriptional activation, which clearly supports the proposition.
- edge rationale, **H2** → node: Candidate B emphasizes phase separation and co-condensation as necessary for transcriptional activation, making it less likely that soluble, dynamic interactions alone are sufficient.
- parent `X1`: Transcriptional activation by Gcn4 occurs in the absence of Med15-Gcn4 condensate formation.
- chain rationale, `X1` → node: If Gcn4 can activate transcription without Med15-Gcn4 condensate formation, it suggests that other forms of interaction, such as soluble, dynamic protein-protein interactions, are likely sufficient for activation.

**Verifier evidence** — label used in score: `support` (log-LR +1.2)

- queries: `transcription factor Mediator interaction transcription`; `Mediator subunit protein-protein interaction activation`
- assessor rationale: Several records directly report physical and functional interactions between transcription factors and Mediator subunits that are sufficient for transcriptional activation. Record [9] describes MYC2's interaction with MED25 as essential for transcriptional activation, while [1] shows that disrupting the interaction between Pdr1 and Gal11A KIX inhibits gene activation. Record [2] identifies Tcf4's interaction with Mediator as central to transcriptional regulation in neural stem cells. These studies provide direct evidence for the sufficiency of soluble, dynamic protein-protein interactions between transcription factors and Mediator subunits in transcriptional activation.
- supporting spans cited by the assessor:
  - "The function of MYC2 depends on its physical and functional interaction with MED25, a subunit of the Mediator transcriptional co-activator complex. In addition to interacting with MYC2 and RNA polymerase II for preinitiation complex formation, MED25 also interacts with multiple genetic and epigenetic regulators and controls almost every step of MYC2-dependent transcription, including nuclear hormone receptor activation, epigenetic regulation, mRNA processing, transcriptional termination, and chromatin loop formation."
  - "Here we perform sequential biochemical and in vivo high-throughput screens to identify small-molecule inhibitors of the interaction of the C. glabrata Pdr1 activation domain with the C. glabrata Gal11A KIX domain. The lead compound (iKIX1) inhibits Pdr1-dependent gene activation and re-sensitizes drug-resistant C. glabrata to azole antifungals in vitro and in animal models for disseminated and urinary tract C. glabrata infection."
  - "Transcription factor families with high affinity for Mediator dominate enhancers and super enhancers and can explain genome-wide Mediator localization. We identify E-box transcription factor Tcf4 as a key regulator of NSCs. Tcf4 interacts with Mediator, colocalizes with Mediator at super enhancers and regulates neurogenic transcription factor genes with super enhancers and broad H3K4me3 domains."
- 10 papers shown; key papers: `s2:1c00e7c3a6c85b9dcf38ff8159948ca215ca368f`, `s2:253d57665358b04833504d10cf1f8382f2e0dd8e`, `s2:4c80fa5cf210e1c5a27ec55cc6b902f199816121`
- _The evidence assessor returns ONE label for the node from all papers shown; the method has no per-paper contribution. Key papers and spans are those the assessor cited._

<details><summary>[1] **KEY** Inhibiting Fungal Multidrug Resistance by Disrupting an Activator-Mediator Interaction — Joy L. Nishikawa, A. Boeszoermenyi, L. Vale-Silva, R. Torelli et al. (2016); cutoff-filter date 2016-02-17; doi:10.1038/nature16963</summary>

```text
[1] Inhibiting Fungal Multidrug Resistance by Disrupting an Activator-Mediator Interaction
    id: s2:1c00e7c3a6c85b9dcf38ff8159948ca215ca368f
    date: 2016-02-17
    venue: Nature
    authors: Joy L. Nishikawa, A. Boeszoermenyi, L. Vale-Silva, R. Torelli, B. Posteraro, Y. Sohn, Fei Ji, V. Gelev
    abstract: Eukaryotic transcription activators stimulate the expression of specific sets of target genes through recruitment of co-activators such as the RNA polymerase II-interacting Mediator complex. Aberrant function of transcription activators has been implicated in several diseases. However, therapeutic targeting efforts have been hampered by a lack of detailed molecular knowledge of the mechanisms of gene activation by disease-associated transcription activators. We previously identified an activator-targeted three-helix bundle KIX domain in the human MED15 Mediator subunit that is structurally conserved in Gal11/Med15 Mediator subunits in fungi. The Gal11/Med15 KIX domain engages pleiotropic drug resistance transcription factor (Pdr1) orthologues, which are key regulators of the multidrug resistance pathway in Saccharomyces cerevisiae and in the clinically important human pathogen Candida glabrata. The prevalence of C. glabrata is rising, partly owing to its low intrinsic susceptibility to azoles, the most widely used antifungal agent. Drug-resistant clinical isolates of C. glabrata most commonly contain point mutations in Pdr1 that render it constitutively active, suggesting that this transcriptional activation pathway represents a linchpin in C. glabrata multidrug resistance. Here we perform sequential biochemical and in vivo high-throughput screens to identify small-molecule inhibitors of the interaction of the C. glabrata Pdr1 activation domain with the C. glabrata Gal11A KIX domain. The lead compound (iKIX1) inhibits Pdr1-dependent gene activation and re-sensitizes drug-resistant C. glabrata to azole antifungals in vitro and in animal models for disseminated and urinary tract C. glabrata infection. Determining the NMR structure of the C. glabrata Gal11A KIX domain provides a detailed understanding of the molecular mechanism of Pdr1 gene activation and multidrug resistance inhibition by iKIX1. We have demonstrated the feasibility of small-molecule targeting of a tra [...]
```
</details>

<details><summary>[2] **KEY** Mediator complex interaction partners organize the transcriptional network that defines neural stem cells — M. Quevedo, Lize Meert, Mike R. Dekker, D. Dekkers et al. (2019); cutoff-filter date 2019-06-17; doi:10.1038/s41467-019-10502-8</summary>

```text
[2] Mediator complex interaction partners organize the transcriptional network that defines neural stem cells
    id: s2:253d57665358b04833504d10cf1f8382f2e0dd8e
    date: 2019-06-17
    venue: Nature Communications
    authors: M. Quevedo, Lize Meert, Mike R. Dekker, D. Dekkers, J. Brandsma, D. V. D. van den Berg, Z. Ozgür, W. Ijcken
    abstract: The Mediator complex regulates transcription by connecting enhancers to promoters. High Mediator binding density defines super enhancers, which regulate cell-identity genes and oncogenes. Protein interactions of Mediator may explain its role in these processes but have not been identified comprehensively. Here, we purify Mediator from neural stem cells (NSCs) and identify 75 protein-protein interaction partners. We identify super enhancers in NSCs and show that Mediator-interacting chromatin modifiers colocalize with Mediator at enhancers and super enhancers. Transcription factor families with high affinity for Mediator dominate enhancers and super enhancers and can explain genome-wide Mediator localization. We identify E-box transcription factor Tcf4 as a key regulator of NSCs. Tcf4 interacts with Mediator, colocalizes with Mediator at super enhancers and regulates neurogenic transcription factor genes with super enhancers and broad H3K4me3 domains. Our data suggest that high binding-affinity for Mediator is an important organizing feature in the transcriptional network that determines NSC identity. The Mediator complex regulates transcription by connecting enhancers to promoters. Here, the authors purify Mediator from neural stem cells (NSCs), identify 75 novel protein-protein interaction partners and characterize the Mediator-interacting network that regulates transcription and establishes NSC identity.
```
</details>

<details><summary>[3] Crosstalk between C/EBPβ phosphorylation, arginine methylation, and SWI/SNF/Mediator implies an indexing transcription factor code — E. Kowenz-Leutz, O. Pless, G. Dittmar, M. Knoblich et al. (2010); cutoff-filter date 2010-01-28; doi:10.1038/emboj.2010.3</summary>

```text
[3] Crosstalk between C/EBPβ phosphorylation, arginine methylation, and SWI/SNF/Mediator implies an indexing transcription factor code
    id: s2:be5abb21c13a245ecdb57b443bd35fb29b06f05e
    date: 2010-01-28
    venue: EMBO Journal
    authors: E. Kowenz-Leutz, O. Pless, G. Dittmar, M. Knoblich, A. Leutz
    abstract: Cellular signalling cascades regulate the activity of transcription factors that convert extracellular information into gene regulation. C/EBPβ is a ras/MAPkinase signal‐sensitive transcription factor that regulates genes involved in metabolism, proliferation, differentiation, immunity, senescence, and tumourigenesis. The protein arginine methyltransferase 4 PRMT4/CARM1 interacts with C/EBPβ and dimethylates a conserved arginine residue (R3) in the C/EBPβ N‐terminal transactivation domain, as identified by mass spectrometry of cell‐derived C/EBPβ. Phosphorylation of the C/EBPβ regulatory domain by ras/MAPkinase signalling abrogates the interaction between C/EBPβ and PRMT4/CARM1. Differential proteomic screening, protein interaction studies, and mutational analysis revealed that methylation of R3 constraines interaction with SWI/SNF and Mediator complexes. Mutation of the R3 methylation site alters endogenous myeloid gene expression and adipogenic differentiation. Thus, phosphorylation of the transcription factor C/EBPβ couples ras signalling to arginine methylation and regulates the interaction of C/EBPβ with epigenetic gene regulatory protein complexes during cell differentiation.
```
</details>

<details><summary>[4] Microphthalmia‐associated transcription factor interacts with LEF‐1, a mediator of Wnt signaling — K. Yasumoto, K. Takeda, Hideo Saito, Ken-ichi Watanabe et al. (2002); cutoff-filter date 2002-06-03; doi:10.1093/emboj/21.11.2703</summary>

```text
[4] Microphthalmia‐associated transcription factor interacts with LEF‐1, a mediator of Wnt signaling
    id: s2:fa473e9fadff205a17eba8fda63b71f659e44768
    date: 2002-06-03
    venue: EMBO Journal
    authors: K. Yasumoto, K. Takeda, Hideo Saito, Ken-ichi Watanabe, Kazuhiro Takahashi, S. Shibahara
    abstract: [no abstract available]
```
</details>

<details><summary>[5] Mediator MED23 regulates basal transcription in vivo via an interaction with P-TEFb — Wei Wang, Xiao Yao, Yan Huang, Xiangming Hu et al. (2013); cutoff-filter date 2013-01-22; doi:10.4161/trns.22874</summary>

```text
[5] Mediator MED23 regulates basal transcription in vivo via an interaction with P-TEFb
    id: s2:44775c74887d81430d047feb079fb3ef66244cf7
    date: 2013-01-01
    venue: Transcription
    authors: Wei Wang, Xiao Yao, Yan Huang, Xiangming Hu, Run-Zhong Liu, Dongming Hou, Rui-Chuan Chen, Gang Wang
    abstract: [no abstract available]
```
</details>

<details><summary>[6] The Interaction between the Forkhead Thyroid Transcription Factor TTF-2 and the Constitutive Factor CTF/NF-1 Is Required for Efficient Hormonal Regulation of the Thyroperoxidase Gene Transcription* — Lourdes Ortiz, P. Aza‐Blanc, M. Zannini, A. Cato et al. (1999); cutoff-filter date 1999-05-31; doi:10.1074/jbc.274.21.15213</summary>

```text
[6] The Interaction between the Forkhead Thyroid Transcription Factor TTF-2 and the Constitutive Factor CTF/NF-1 Is Required for Efficient Hormonal Regulation of the Thyroperoxidase Gene Transcription*
    id: s2:cbe1445e481379bb8648a661dcf7580168b4ac82
    date: 1999-05-21
    venue: Journal of Biological Chemistry
    authors: Lourdes Ortiz, P. Aza‐Blanc, M. Zannini, A. Cato, P. Santisteban
    abstract: The forkhead thyroid-specific transcription factor TTF-2 is the main mediator of thyrotropin and insulin regulation of thyroperoxidase (TPO) gene expression. This function depends on multimerization and specific orientation of its DNA-binding site, suggesting that TTF-2 is part of a complex interaction network within the TPO promoter. This was confirmed by transfection experiments and by protein-DNA interaction studies, which demonstrated that CTF/NF1 proteins bind 10 base pairs upstream of the TTF-2-binding site to enhance its action in hormone-induced expression of the TPO gene. GST pull-down assays showed that TTF-2 physically interacts with CTF/NF1 proteins. In addition, we demonstrate that increasing the distance between both transcription factors binding sites by base pair insertion results in loss of promoter activity and in a drastic decrease on the ability of the promoter to respond to the hormones. CTF/NF1 is a family of transcription factors that contributes to constitutive and cell-type specific gene expression. Originally identified as factors implicated in the replication of adenovirus, this group of proteins (CTF/NF1-A, -B, -C, and -X) is now known to be involved in the regulation of several genes. In contrast to other reports regarding the involvement of these proteins in inducible gene expression, we show here that members of this family of transcription factors are regulated by hormones. With the use of specific CTF/NF1 DNA probes and antibodies we demonstrate that CTF/NF1-C is a thyrotropin-, cAMP-, and insulin-inducible protein. Thus CTF/NF1 proteins do not only mediate hormone-induced gene expression cooperating with TTF-2, but are themselves hormonally regulated. All these findings are clearly of important value in understanding the mechanisms governing the transcription regulation of RNA polymerase II promoters, which often contain binding sites for multiple transcription factors.
```
</details>

<details><summary>[7] Ubiquitous transcription factor OTF-1 mediates induction of the MMTV promoter through synergistic interaction with hormone receptors. — Ulf Brüggemeier, M. Kalff, S. Franke, C. Scheidereit et al. (1991); cutoff-filter date 1991-02-28; doi:10.1016/0092-8674(91)90240-y</summary>

```text
[7] Ubiquitous transcription factor OTF-1 mediates induction of the MMTV promoter through synergistic interaction with hormone receptors.
    id: s2:409c5afbac28996b7b3d48023720273f4302089e
    date: 1991-02-08
    venue: Cell
    authors: Ulf Brüggemeier, M. Kalff, S. Franke, C. Scheidereit, M. Beato
    abstract: [no abstract available]
```
</details>

<details><summary>[8] Expression of the pro-apoptotic Bcl-2 family member Bim is regulated by the forkhead transcription factor FKHR-L1. — P. Dijkers, R. Medema, J. Lammers, L. Koenderman et al. (2000); cutoff-filter date 2000-10-31; doi:10.1016/s0960-9822(00)00728-4</summary>

```text
[8] Expression of the pro-apoptotic Bcl-2 family member Bim is regulated by the forkhead transcription factor FKHR-L1.
    id: s2:1a3dc86b3f8aa68a3b6b5b2e5b60525fb2dd3a56
    date: 2000-10-01
    venue: Current Biology
    authors: P. Dijkers, R. Medema, J. Lammers, L. Koenderman, P. Coffer
    abstract: [no abstract available]
```
</details>

<details><summary>[9] **KEY** Mediator subunit MED25: at the nexus of jasmonate signaling. — Qingzhe Zhai, Lei Deng, Chuanyou Li (2020); cutoff-filter date 2020-08-07; doi:10.1016/j.pbi.2020.06.006</summary>

```text
[9] Mediator subunit MED25: at the nexus of jasmonate signaling.
    id: s2:4c80fa5cf210e1c5a27ec55cc6b902f199816121
    date: 2020-08-07
    venue: Current opinion in plant biology
    authors: Qingzhe Zhai, Lei Deng, Chuanyou Li
    abstract: Upon perception by plant cells, the immunity hormone jasmonate (JA) triggers a genome-wide transcriptional program, which is largely regulated by the master transcription factor MYC2. The function of MYC2 depends on its physical and functional interaction with MED25, a subunit of the Mediator transcriptional co-activator complex. In addition to interacting with MYC2 and RNA polymerase II for preinitiation complex formation, MED25 also interacts with multiple genetic and epigenetic regulators and controls almost every step of MYC2-dependent transcription, including nuclear hormone receptor activation, epigenetic regulation, mRNA processing, transcriptional termination, and chromatin loop formation. These diversified functions have ascribed MED25 to a signal-processing and signal-integrating center during JA-regulated gene transcription. This review is focused on the interactions of MED25 with diverse transcriptional regulators and how these mechanistic interactions contribute to the initiation, amplification, and fine tuning of the transcriptional output of JA signaling.
```
</details>

<details><summary>[10] BET bromodomain inhibition releases the Mediator complex from select cis-regulatory elements — Anand S. Bhagwat, Jae-seok Roe, Beverly Mok, Anja F. Hohmann et al. (2016); cutoff-filter date 2016-04-09; doi:10.1016/j.celrep.2016.03.054</summary>

```text
[10] BET bromodomain inhibition releases the Mediator complex from select cis-regulatory elements
    id: s2:12ddaf6918a639edea5825d224c475ebe12fb43c
    date: 2016-04-07
    venue: Cell Reports
    authors: Anand S. Bhagwat, Jae-seok Roe, Beverly Mok, Anja F. Hohmann, Junwei Shi, C. Vakoc
    abstract: The bromodomain and extraterminal (BET) protein BRD4 can physically interact with the Mediator complex, but the relevance of this association to the therapeutic effects of BET inhibitors in cancer is unclear. Here, we show that BET inhibition causes a rapid release of Mediator from a subset of cis-regulatory elements in the genome of acute myeloid leukemia (AML) cells. These sites of Mediator eviction were highly correlated with transcriptional suppression of neighboring genes, which are enriched for targets of the transcription factor MYB and for functions related to leukemogenesis. An shRNA screen of Mediator in AML cells identified the MED12, MED13, MED23, and MED24 subunits as performing a similar regulatory function to BRD4 in this context, including a shared role in sustaining a block in myeloid maturation. These findings suggest that the interaction between BRD4 and Mediator has functional importance for gene-specific transcriptional activation and for AML maintenance.
```
</details>

<details><summary>Post-hoc automated audit — NON-AUTHORITATIVE; uses hidden benchmark annotations</summary>

- primary auditor: `silence_as_null_error`; statuses {'H1': 'positive_or_present', 'H2': 'indeterminate'}; discriminative=False
- primary reasoning: H1 explicitly predicts that soluble, dynamic protein-protein interactions are sufficient for transcriptional activation, so the proposition is positive under H1. H2 is silent on whether soluble interactions alone are sufficient, as it focuses on phase-separation and condensate mechanisms, making its status indeterminate.
- derived opposition call: `manufactured_from_silence`
- evidence attribution: `informative_evidence_found` — The retrieved literature includes multiple papers that directly address the sufficiency of soluble, dynamic protein-protein interactions between transcription factors and Mediator subunits for transcriptional activation. The assessor correctly identified and used these papers to support the proposition. The process worked as intended.
- disagreement flags: {'second_rater_vs_primary_discriminative': None, 'second_rater_vs_primary_status': None, 'retest_vs_primary_category': None, 'any': False}
</details>

**Human review** — `silence_as_null_error` · reviewer: Research Director · source: D045 · status: `first_pass_model_based_review` · genuinely discriminative: False · silence-as-null error: True · other fields not recorded

---

## #40 · `GP1-spider_orb_web_origin-X11`

**GP1-spider_orb_web_origin-X11** — case `spider_orb_web_origin`, node `X11`

> Orb-weaving behavior in spiders can arise through distinct genetic pathways rather than a single conserved web-building gene expression pattern.

- generated from **H2** (Candidate B); abstraction: `mechanistic`
- generator's stated reason: If cribellate orb-weaving spiders lack homologous web-building gene expression patterns found in ecribellate orb-weaving spiders, it implies that orb-weaving behavior can be produced by different genetic mechanisms.
- influence: **0.187** (rank 2 in case, 40 overall; cumulative 80%) — favours **H2**
- log-likelihood contribution: H1 +0.976, H2 +1.163
- removing it alone: evidence withheld → case log-odds -0.119 (ranking unchanged); node deleted → -0.119 (ranking unchanged)

**Hypotheses (as shown to the verifier)**

- **H1** (Candidate A): Orb-weaving evolved in an ancient common ancestor; descendant non-orb-weaving lineages repeatedly lost orb-associated traits and molecular functions.
- **H2** (Candidate B): Cribellate and ecribellate orb webs arose independently/repeatedly in separate lineages through convergent evolution.

**Verifier cross-hypothesis judgments** — P(X|H) combines these by noisy-OR

| hypothesis | origin? | direct edge | route via parent | P(X\|H) |
| --- | --- | --- | --- | --- |
| H1 | no | `unlikely` | X4 [H→parent `unlikely`, P=0.30] → `implied` | 0.713 |
| H2 | yes | `implied` | X4 [H→parent `implied`, P=0.80] → `implied` | 0.948 |

- edge rationale, **H1** → node: If orb-weaving evolved once in a common ancestor and was lost in some lineages, it suggests a single conserved genetic basis rather than multiple distinct pathways.
- edge rationale, **H2** → node: If orb-weaving arose independently in separate lineages, it is clearly expected that distinct genetic pathways could underlie the behavior.
- parent `X4`: Orb-weaving behavior in cribellate spiders is not associated with homologous web-building gene expression patterns found in ecribellate orb-weaving spiders.
- chain rationale, `X4` → node: If orb-weaving behavior in cribellate spiders is not associated with the same gene expression patterns as in ecribellate orb-weaving spiders, it suggests that orb-weaving can arise through distinct genetic pathways rather than a single conserved pattern.

**Verifier evidence** — label used in score: `support` (log-LR +1.2)

- queries: `spider orb-weaving gene expression`; `spider web-building genetic pathways`
- assessor rationale: Several records directly state that spider silk production involves diverse gene families, with evidence for multiple spidroin gene classes, gland- and sex-specific expression, and challenge to the idea of conserved motifs being essential. These findings indicate that orb-weaving behavior and silk production can arise from distinct genetic pathways, rather than a single conserved gene expression pattern. The studies are based on independent genomic and transcriptomic analyses across different orb-weaving spider species.
- supporting spans cited by the assessor:
  - "Together, these findings challenge long-standing paradigms regarding the evolutionary and functional significance of the proteins and conserved motifs essential for producing spider silks."
  - "Characterization of spidroin expression in distinct silk gland types indicates that glands can express multiple spidroin types."
  - "We identify at least 31 putative spidroin genes, with expansion of multiple spidroin gene classes relative to the golden orb-weaver, Trichonephila clavipes."
  - "Comparative gene expression analyses across six silk gland isolates in females plus a composite isolate of all silk glands in males demonstrated gland and sex-specific expression of spidroins, facilitating putative assignment of novel spidroin genes to classes."
- 10 papers shown; key papers: `s2:41b40170230f9a635ce04dad90275007e6503064`, `s2:80eb96215b61a202c7f5828eb4e8f2feb8db9f6c`, `s2:916edeea6dc75f55d67fda239a1949d0013a8779`
- _The evidence assessor returns ONE label for the node from all papers shown; the method has no per-paper contribution. Key papers and spans are those the assessor cited._

<details><summary>[1] **KEY** Golden orb-weaving spider (Trichonephila clavipes) silk genes with sex-biased expression and atypical architectures — Sandra M Correa-Garhwal, P. Babb, B. Voight, C. Hayashi (2020); cutoff-filter date 2020-12-22; doi:10.1093/g3journal/jkaa039</summary>

```text
[1] Golden orb-weaving spider (Trichonephila clavipes) silk genes with sex-biased expression and atypical architectures
    id: s2:41b40170230f9a635ce04dad90275007e6503064
    date: 2020-12-22
    venue: G3
    authors: Sandra M Correa-Garhwal, P. Babb, B. Voight, C. Hayashi
    abstract: Abstract Spider silks are renowned for their high-performance mechanical properties. Contributing to these properties are proteins encoded by the spidroin (spider fibroin) gene family. Spidroins have been discovered mostly through cDNA studies of females based on the presence of conserved terminal regions and a repetitive central region. Recently, genome sequencing of the golden orb-web weaver, Trichonephila clavipes, provided a complete picture of spidroin diversity. Here, we refine the annotation of T. clavipes spidroin genes including the reclassification of some as non-spidroins. We rename these non-spidroins as spidroin-like (SpL) genes because they have repetitive sequences and amino acid compositions like spidroins, but entirely lack the archetypal terminal domains of spidroins. Insight into the function of these spidroin and SpL genes was then examined through tissue- and sex-specific gene expression studies. Using qPCR, we show that some silk genes are upregulated in male silk glands compared to females, despite males producing less silk in general. We also find that an enigmatic spidroin that lacks a spidroin C-terminal domain is highly expressed in silk glands, suggesting that spidroins could assemble into fibers without a canonical terminal region. Further, we show that two SpL genes are expressed in silk glands, with one gene highly evolutionarily conserved across species, providing evidence that particular SpL genes are important to silk production. Together, these findings challenge long-standing paradigms regarding the evolutionary and functional significance of the proteins and conserved motifs essential for producing spider silks.
```
</details>

<details><summary>[2] Gene expression profiling reveals candidate genes for defining spider silk gland types. — R. C. Chaw, T. Clarke, Peter Arensburger, Nadia A. Ayoub et al. (2021); cutoff-filter date 2021-05-27; doi:10.1016/j.ibmb.2021.103594</summary>

```text
[2] Gene expression profiling reveals candidate genes for defining spider silk gland types.
    id: s2:cc7f245131dc6f6c8897a19a2df6c305b9ee8132
    date: 2021-05-27
    venue: Insect Biochemistry and Molecular Biology
    authors: R. C. Chaw, T. Clarke, Peter Arensburger, Nadia A. Ayoub, C. Hayashi
    abstract: Molecular studies of the secretory glands involved in spider silk production have revealed candidate genes for silk synthesis and a complicated history of spider silk gene evolution. However, differential gene expression profiles of the multiple silk gland types within an individual orb-web weaving spider are lacking. Each of these gland types produces a functionally distinct silk type. Comparison of gene expression among spider silk gland types would provide insight into the genes that define silk glands generally from non-silk gland tissues, and the genes that define silk glands from each other. Here, we perform 3' tag digital gene expression profiling of the seven silk gland types of the silver garden orb weaver Argiope argentata. Five of these gland types produce silks that are non-adhesive fibers, one silk includes both fibers and glue-like adhesives, and one silk is exclusively glue-like. We identify 1275 highly expressed, significantly upregulated, and tissue specific silk gland specific transcripts (SSTs). These SSTs include seven types of spider silk protein encoding genes known as spidroin genes. We find that the fiber-producing major ampullate and minor ampullate silk glands have more similar expression profiles than any other pair of glands. We also find that a subset of the SSTs is enriched for transmembrane transport and oxidoreductases, and that these transcripts highlight differences and similarities among the major ampullate, minor ampullate, and aggregate silk glands. Furthermore, we show that the wet glue-producing aggregate glands have the most unique SSTs, but still share some SSTs with fiber producing glands. Aciniform glands were the only gland type to share a majority of SSTs with other silk gland types, supporting previous hypotheses that duplication of aciniform glands and subsequent divergence of the duplicates gave rise to the multiple silk gland types within an individual spider.
```
</details>

<details><summary>[3] The common house spider, Parasteatoda tepidariorum, maintains silk gene expression on sub-optimal diet — Jeremy A. Miller, Jannelle M. Vienneau-Hathaway, Enkhbileg Dendev, M. Lan et al. (2020); cutoff-filter date 2020-12-09; doi:10.1371/journal.pone.0237286</summary>

```text
[3] The common house spider, Parasteatoda tepidariorum, maintains silk gene expression on sub-optimal diet
    id: s2:6b100bd01675e55c18259bfd3ae55725d48b0a89
    date: 2020-07-27
    venue: bioRxiv (preprint)
    authors: Jeremy A. Miller, Jannelle M. Vienneau-Hathaway, Enkhbileg Dendev, M. Lan, Nadia A. Ayoub
    abstract: Orb-web weaving spiders and their relatives spin multiple task-specific fiber types. The unique material properties of each silk type result from differences in amino acid sequence and structure of their component proteins, primarily spidroins (spider fibrous proteins). Amino acid content and gene expression measurements of spider silks suggest some spiders change expression patterns of individual protein components in response to environmental cues. We quantified mRNA abundance of three spidroin encoding genes involved in prey capture in the common house spider, Parasteatoda tepidariorum (Theridiidae), fed different diets. After 10 days of acclimation to the lab on a diet of mealworms, spiders were split into three groups: (1) individuals were immediately dissected, (2) spiders were fed high-energy crickets, or (3) spiders were fed low-energy flies, for 1 month. All spiders gained mass during the acclimation period and cricket-fed spiders continued to gain mass, while fly fed spiders either maintained or lost mass. Using quantitative PCR, we found no significant differences in the absolute or relative abundance of dragline gene transcripts, major ampullate spidroin 1 (MaSp1) and major ampullate spidroin 2 (MaSp2), among groups. In contrast, prey-wrapping minor ampullate spidroin (MiSp) gene transcripts were significantly less abundant in fly-fed than lab-acclimated spiders. However, when measured relative to actin, cricket-fed spiders showed the lowest expression of MiSp. Our results suggest that house spiders are able to maintain silk production, even in the face of a low-quality diet.
```
</details>

<details><summary>[4] Candidate egg case silk genes for the spider Argiope argentata from differential gene expression analyses — R. C. Chaw, Peter Arensburger, T. Clarke, Nadia A. Ayoub et al. (2016); cutoff-filter date 2016-08-08; doi:10.1111/imb.12260</summary>

```text
[4] Candidate egg case silk genes for the spider Argiope argentata from differential gene expression analyses
    id: s2:fc6425e540b2f1487bef3c88a8ffa19333c1cb0f
    date: 2016-08-01
    venue: Insect molecular biology (Print)
    authors: R. C. Chaw, Peter Arensburger, T. Clarke, Nadia A. Ayoub, C. Hayashi
    abstract: Orb‐web weaving spiders produce a variety of task‐specific silks from specialized silk glands. The genetics underlying the synthesis of specific silk types are largely unknown, and transcriptome analysis could be a powerful approach for identifying candidate genes. However, de novo assembly and expression profiling of silk glands with RNA‐sequencing (RNAseq) are problematic because the few known gene transcripts for silk proteins are extremely long and highly repetitive. To identify candidate genes for tubuliform (egg case) silk synthesis by the orb‐weaver Argiope argentata (Araneidae), we estimated transcript abundance using two sequencing methods: RNAseq reads from throughout the length of mRNA molecules, and 3′ digital gene expression reads from the 3′ region of mRNA molecules. Both analyses identified similar sets of genes as differentially expressed when comparing tubuliform and nonsilk gland tissue. However, incompletely assembled silk gene transcripts were identified as differentially expressed because of RNAseq read alignments to highly repetitive regions, confounding interpretation of RNAseq results. Homologues of egg case silk protein (ECP) genes were upregulated in tubuliform glands. This discovery is the first description of ECP homologues in an araneid. We also propose additional candidate genes involved in synthesis of tubuliform or other silk types.
```
</details>

<details><summary>[5] **KEY** The Nephila clavipes genome highlights the diversity of spider silk genes and their complex expression — P. Babb, N. Lahens, Sandra M Correa-Garhwal, David N. Nicholson et al. (2017); cutoff-filter date 2017-05-01; doi:10.1038/ng.3852</summary>

```text
[5] The Nephila clavipes genome highlights the diversity of spider silk genes and their complex expression
    id: s2:80eb96215b61a202c7f5828eb4e8f2feb8db9f6c
    date: 2017-05-01
    venue: Nature Genetics
    authors: P. Babb, N. Lahens, Sandra M Correa-Garhwal, David N. Nicholson, Eun Ji Kim, J. Hogenesch, M. Kuntner, L. Higgins
    abstract: Spider silks are the toughest known biological materials, yet are lightweight and virtually invisible to the human immune system, and they thus have revolutionary potential for medicine and industry. Spider silks are largely composed of spidroins, a unique family of structural proteins. To investigate spidroin genes systematically, we constructed the first genome of an orb-weaving spider: the golden orb-weaver (Nephila clavipes), which builds large webs using an extensive repertoire of silks with diverse physical properties. We cataloged 28 Nephila spidroins, representing all known orb-weaver spidroin types, and identified 394 repeated coding motif variants and higher-order repetitive cassette structures unique to specific spidroins. Characterization of spidroin expression in distinct silk gland types indicates that glands can express multiple spidroin types. We find evidence of an alternatively spliced spidroin, a spidroin expressed only in venom glands, evolutionary mechanisms for spidroin diversification, and non-spidroin genes with expression patterns that suggest roles in silk production.
```
</details>

<details><summary>[6] The Effect of Diet on Venom Gene Expression in Tetragnatha versicolor — Z. Hasan (2017); cutoff-filter date 2017-12-01; https://www.semanticscholar.org/paper/1f6739fdade798b2565e7cfbe605768f9e9b857b</summary>

```text
[6] The Effect of Diet on Venom Gene Expression in Tetragnatha versicolor
    id: s2:1f6739fdade798b2565e7cfbe605768f9e9b857b
    date: 2017-12-01
    venue: unknown
    authors: Z. Hasan
    abstract: [no abstract available]
```
</details>

<details><summary>[7] Orb weaver aggregate glue protein composition as a mechanism for rapid evolution of material properties — Nadia A. Ayoub, Lucas DuMez, Cooper Lazo, Maria Luzaran et al. (2023); cutoff-filter date 2023-04-18; doi:10.3389/fevo.2023.1099481</summary>

```text
[7] Orb weaver aggregate glue protein composition as a mechanism for rapid evolution of material properties
    id: s2:564852da0ffa8d3ead458427094bda9df3e9334e
    date: 2023-04-18
    venue: Frontiers in Ecology and Evolution
    authors: Nadia A. Ayoub, Lucas DuMez, Cooper Lazo, Maria Luzaran, Jamal Magoti, Sarah A. Morris, R. Baker, T. Clarke
    abstract: Introduction Orb web and cobweb weaving spiders in the superfamily Araneoidea are distinguished by their ability to make a chemically sticky aqueous glue in specialized aggregate silk glands. Aggregate glue is an environmentally responsive material that has evolved to perform optimally around the humidity at which a spider forages. Protein components and their post-translational modifications confer stickiness to the glue, but the identities of these proteins have not been described for orb web weavers. Methods Using biomechanics, gene expression data, and proteomics, we characterized the glue’s physical properties and molecular components in two congeners that live in different environments, Argiope argentata (dry southwest US) and Argiope trifasciata (humid southeast US). Results The droplets of A. argentata are less hygroscopic than those of A. trifasciata and have proportionately smaller viscoelastic protein cores, which incorporate a smaller percentage of absorbed water as humidity increases. Argiope argentata protein cores were many times stiffer and tougher than A. trifasciata protein cores. Each species’ glue included ~30 aggregate-expressed proteins, most of which were homologous between the two species, with high sequence identity. However, the relative contribution and number of gene family members of each homologous group differed. For instance, the aggregate spidroins (AgSp1 and AgSp2) accounted for nearly half of the detected glue composition in A. argentata, but only 38% in A. trifasciata. Additionally, AgSp1, which has highly negatively charged regions, was ~2X as abundant as the positively charged AgSp2 in A. argentata, but ~3X as abundant in A. trifasciata. As another example, A. argentata glue included 11 members of a newly discovered cysteine-rich gene family, versus 7 members in A. trifasciata. Discussion Cysteines form disulfide bonds that, combined with the higher potential for electrostatic interactions between AgSp1 and AgSp2, could contribu [...]
```
</details>

<details><summary>[8] Comparative Analysis of Various Spider Silks in Regard to Nerve Regeneration: Material Properties and Schwann Cell Response — S. Stadlmayr, Karolina Peter, F. Millesi, Anda Rad et al. (2023); cutoff-filter date 2023-12-11; doi:10.1002/adhm.202302968</summary>

```text
[8] Comparative Analysis of Various Spider Silks in Regard to Nerve Regeneration: Material Properties and Schwann Cell Response
    id: s2:1d17805a4161063a87c63d95c92090b6dded7daf
    date: 2023-12-11
    venue: Advanced Healthcare Materials
    authors: S. Stadlmayr, Karolina Peter, F. Millesi, Anda Rad, S. Wolf, Sascha Mero, M. Zehl, Axel Mentler
    abstract: Peripheral nerve reconstruction through the employment of nerve guidance conduits with Trichonephila dragline silk as a luminal filling has emerged as an outstanding preclinical alternative to avoid nerve autografts. Yet, it remains unknown whether the outcome is similar for silk fibers harvested from other spider species. This study compares the regenerative potential of dragline silk from two orb‐weaving spiders, Trichonephila inaurata and Nuctenea umbratica, as well as the silk of the jumping spider Phidippus regius. Proliferation, migration, and transcriptomic state of Schwann cells seeded on these silks are investigated. In addition, fiber morphology, primary protein structure, and mechanical properties are studied. The results demonstrate that the increased velocity of Schwann cells on Phidippus regius fibers can be primarily attributed to the interplay between the silk's primary protein structure and its mechanical properties. Furthermore, the capacity of silk fibers to trigger cells toward a gene expression profile of a myelinating Schwann cell phenotype is shown. The findings for the first time allow an in‐depth comparison of the specific cellular response to various native spider silks and a correlation with the fibers’ material properties. This knowledge is essential to open up possibilities for targeted manufacturing of synthetic nervous tissue replacement.
```
</details>

<details><summary>[9] house spider, Parasteatoda tepidariorum — Jeremy Miller, Jannelle M. Vienneau-Hathaway, Enkhbileg Dendev, M. Lan et al. (2023); cutoff-filter date 2023-12-31; https://www.semanticscholar.org/paper/bbe0b8bd8c0fcd1e0b42467650765d6fd5319231</summary>

```text
[9] house spider, Parasteatoda tepidariorum
    id: s2:bbe0b8bd8c0fcd1e0b42467650765d6fd5319231
    date: 2023
    venue: unknown
    authors: Jeremy Miller, Jannelle M. Vienneau-Hathaway, Enkhbileg Dendev, M. Lan, N. Ayoub
    abstract: [no abstract available]
```
</details>

<details><summary>[10] **KEY** Characterization of the genome and silk-gland transcriptomes of Darwin’s bark spider (Caerostris darwini) — P. Babb, M. Gregorič, N. Lahens, David N. Nicholson et al. (2022); cutoff-filter date 2022-06-06; doi:10.1371/journal.pone.0268660</summary>

```text
[10] Characterization of the genome and silk-gland transcriptomes of Darwin’s bark spider (Caerostris darwini)
    id: s2:916edeea6dc75f55d67fda239a1949d0013a8779
    date: 2022-06-06
    venue: PLoS ONE
    authors: P. Babb, M. Gregorič, N. Lahens, David N. Nicholson, Cheryl Y. Hayashi, L. Higgins, M. Kuntner, I. Agnarsson
    abstract: Natural silks crafted by spiders comprise some of the most versatile materials known. Artificial silks–based on the sequences of their natural brethren–replicate some desirable biophysical properties and are increasingly utilized in commercial and medical applications today. To characterize the repertoire of protein sequences giving silks their biophysical properties and to determine the set of expressed genes across each unique silk gland contributing to the formation of natural silks, we report here draft genomic and transcriptomic assemblies of Darwin’s bark spider, Caerostris darwini, an orb-weaving spider whose dragline is one of the toughest known biomaterials on Earth. We identify at least 31 putative spidroin genes, with expansion of multiple spidroin gene classes relative to the golden orb-weaver, Trichonephila clavipes. We observed substantial sharing of spidroin repetitive sequence motifs between species as well as new motifs unique to C. darwini. Comparative gene expression analyses across six silk gland isolates in females plus a composite isolate of all silk glands in males demonstrated gland and sex-specific expression of spidroins, facilitating putative assignment of novel spidroin genes to classes. Broad expression of spidroins across silk gland types suggests that silks emanating from a given gland represent composite materials to a greater extent than previously appreciated. We hypothesize that the extraordinary toughness of C. darwini major ampullate dragline silk may relate to the unique protein composition of major ampullate spidroins, combined with the relatively high expression of stretchy flagelliform spidroins whose union into a single fiber may be aided by novel motifs and cassettes that act as molecule-binding helices. Our assemblies extend the catalog of sequences and sets of expressed genes that confer the unique biophysical properties observed in natural silks.
```
</details>

<details><summary>Post-hoc automated audit — NON-AUTHORITATIVE; uses hidden benchmark annotations</summary>

- primary auditor: `reference_discriminator_recovered`; statuses {'H1': 'negative_or_absent', 'H2': 'positive_or_present'}; discriminative=True
- primary reasoning: H1 (ancient origin/loss) predicts that orb-weaving behavior in all orb-weaving spiders should be underpinned by homologous, conserved genetic pathways inherited from a common ancestor, so distinct genetic pathways would not be expected. H2 (convergent origins) predicts that orb-weaving could arise via different genetic mechanisms in different lineages, so distinct genetic pathways are expected.
- matched hidden reference discriminator: Ancient-origin/loss predicts orb-associated genes inherited from a common ancestor should show relaxed selection and/or gene loss in descendant lineages that lost orb-weaving. Convergent-origin predicts orb-associated genes should show convergent positive selection in independently orb-weaving lineages.
- derived opposition call: `genuine`
- evidence attribution: `informative_evidence_found` — The retrieved papers include genomic and transcriptomic studies of orb-weaving spiders, demonstrating diverse silk gene families, gland- and sex-specific expression, and challenging the notion of a single conserved web-building gene expression pattern. The assessor correctly identified that these findings support the proposition, and the queries were well-targeted to surface such evidence.
- disagreement flags: {'second_rater_vs_primary_discriminative': None, 'second_rater_vs_primary_status': None, 'retest_vs_primary_category': None, 'any': False}
</details>

**Human review** — `invalid_or_weak_implication` · reviewer: Research Director · source: D045 · status: `first_pass_model_based_review` · genuinely discriminative: False · silence-as-null error: False · other fields not recorded

---

