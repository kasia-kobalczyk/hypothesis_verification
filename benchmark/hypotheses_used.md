# Hypothesis pairs used in this project

Every candidate pair the verifier has been run on, with the role each played.
Text is **verbatim from ResearchBench** and has never been rewritten -- that
constraint held throughout (see docs/DECISIONS.md).

`gold` is the finding the source paper reported. `negative` is a ResearchBench
model-generated alternative that passed the frozen R1-R6 screening and the v2
length band.

Machine-readable copy: `benchmark/hypotheses_used.jsonl`.

---

## RBV2-0012-N00

- **role:** debug-5
- **discipline:** Biology
- **source DOI:** 10.1016/j.tcb.2023.07.009
- **literature cutoff:** 2024-03-31
- **runs:** 4; gold rank 1, 1, 1, 2

**Question**

> What are the roles and mechanisms by which the cystine transporter SLC7A11 (also known as xCT) contributes to a novel form of regulated cell death termed "disulfidptosis," particularly in the context of cancer cell metabolism and stress responses?

**Gold hypothesis**

The main hypothesis is that SLC7A11 overexpression in cancer cells induces a unique form of cell death, termed disulfidptosis, under conditions of glucose deprivation. This process is driven by disulfide stress resulting from the accumulation of intracellular cystine and other disulfide molecules, leading to aberrant protein disulfide bonding, particularly in the actin cytoskeleton, and culminating in cell death.

**Negative hypothesis**

SLC7A11/xCT-mediated cystine uptake driven by NADPH debt causes a significant impairment in mitochondrial respiratory complex I activity, leading to the formation of dysfunctional mitochondrial ROS (mitoROS) and a unique type of regulated cell death termed "disulfidptosis" characterized by the sequential activation of autophagy and necroptosis in cancer cells under chronic glucose-starved conditions.

---

## RBV2-0005-N07

- **role:** debug-5
- **discipline:** Energy Science
- **source DOI:** 10.1007/s13399-020-01243-6
- **literature cutoff:** 2021-01-02
- **runs:** 4; gold rank 2, 2, 1, 1

**Question**

> How can traditional pulping processes be improved to meet the increasing global demand for paper and pulp-derived products, while simultaneously reducing energy and chemical requirements, maximizing pulp yields and quality, and exploring new high-value applications, particularly in the context of a shift towards bio-based nanotechnology and sustainable practices?

**Gold hypothesis**

Traditional pulping processes can be significantly improved by adopting a multi-pronged approach that includes optimizing existing methods (e.g., Kraft pulping) through techniques like extended impregnation and pre-hydrolysis, incorporating post-treatment of pulps to produce high-value products like nanocellulose, and leveraging lignin genetic engineering to reduce the recalcitrance of wood and improve pulping efficiency, leading to reduced energy and chemical consumption while diversifying the use of pulp feedstocks.

**Negative hypothesis**

Incorporating cellulose nanofibrils (CNFs) at a concentration of 5-10 wt% during the initial pulping stage can improve pulp quality and yield while reducing energy and chemical requirements, particularly when CNFs are pretreated with mild alkaline solutions and introduced at temperatures of 60-80°C. The inclusion of CNFs in the early stages of pulping is hypothesized to facilitate fiber bonding and reinforcement, paving the way for bio-based, high-strength paper products with novel applications in sustainable nanotechnology.

---

## RBV2-0018-N05

- **role:** debug-5
- **discipline:** Biology
- **source DOI:** 10.1038/s41592-024-02201-0
- **literature cutoff:** 2023-04-30
- **runs:** 4; gold rank 1, 2, 1, 1

**Question**

> How can generative pretrained models be leveraged to advance cellular biology and genetic research using single-cell sequencing data?

**Gold hypothesis**

A generative pretrained transformer model, scGPT, can be developed for single-cell biology by training on a repository of over 33 million cells, enabling it to effectively distill critical biological insights and adapt through transfer learning for various downstream tasks such as cell type annotation, multi-batch integration, and gene network inference.

**Negative hypothesis**

Integrating generative pretrained models, such as fine-tuned GPTs for genomic sequence embedding, with deep learning architectures like Enformer, can enhance the accuracy and resolution of single-cell gene expression prediction by leveraging long-range genomic interactions and contextualized representations, thereby revealing critical regulatory mechanisms underlying cellular differentiation pathways.

---

---

## RBV2-0034-N04

- **role:** debug-5
- **discipline:** Earth Science
- **source DOI:** 10.1007/s12665-023-11347-7
- **literature cutoff:** 2023-12-28
- **runs:** 4; gold rank 1, 1, 1, 1

**Question**

> How can the spatio-temporal distribution and trends of landslide disasters in Nepal from 2011 to 2020 be analyzed to identify landslide-prone areas and assess the impact of various factors such as rainfall and earthquakes on landslide occurrences?

**Gold hypothesis**

The landslide disasters in Nepal from 2011 to 2020 have been significantly influenced by both natural factors (such as monsoon rainfall and the 2015 Gorkha earthquake) and anthropogenic factors (such as urbanization and road construction), leading to an increase in landslide occurrences, particularly during the monsoon season and in regions affected by the Gorkha earthquake, indicating a spatial and temporal clustering of events.

**Negative hypothesis**

The spatio-temporal patterns of landslide disasters in Nepal's mountainous Himalayan Range from 2011 to 2020 are significantly influenced by the interaction of extreme rainfall rates (>1,000 mm/year) and earthquake-induced stress on the terrain, with a higher likelihood of landslides occurring within 1-2 years after a significant seismic event, especially during the pre-monsoon season (April-June).

---

## RBV2-0038-N04

- **role:** debug-5
- **discipline:** Law
- **source DOI:** 10.1016/j.cell.2023.11.011
- **literature cutoff:** 2023-03-18
- **runs:** 4; gold rank 1, 1, 1, 1

**Question**

> How does fetal metabolism change during development, and how is it impacted by altered maternal metabolism, specifically hyperglycemia in diabetic pregnancies?

**Gold hypothesis**

The paper presents a comprehensive, multi-tissue atlas of *in vivo* fetal murine metabolism during mid-to-late gestation, revealing that maternal hyperglycemia alters fetal metabolic profiles, including sorbitol accumulation, changes in amino acid levels, and variations in nutrient sourcing, ultimately indicating a dynamic fetal metabolic landscape affected by maternal glycemic state.

**Negative hypothesis**

In diabetic pregnancies, hyperglycemia disrupts fetal metabolic plasticity by altering specific redox states and the regulation of key metabolic enzymes, such as glucose-6-phosphate dehydrogenase (G6PD) and isocitrate dehydrogenase (IDH), during critical mid-gestation stages. These alterations affect fetal growth by changing the balance of redox homeostasis and metabolic flux, measurable through targeted metabolomic profiling and redox-sensitive fluorescent probes.

---

## RBV2-0268-N03

- **role:** dev-20 (held out once, now development); diagnostic phase 1/2
- **discipline:** Business
- **source DOI:** 10.1016/j.gsf.2023.101689
- **literature cutoff:** 2024-06-30
- **runs:** 3; gold rank 1, 1, 1

**Question**

> How do green finance, eco-innovation, renewable energy, and carbon taxes impact CO2 emissions in BRICS countries, and can these factors be leveraged to effectively reduce emissions from 2001 to 2020?

**Gold hypothesis**

Green finance, eco-innovation, renewable energy consumption and output, and carbon taxes are negatively correlated with CO2 emissions in BRICS countries, making them effective tools for reducing emissions and promoting sustainable development in these economies.

**Negative hypothesis**

Green finance, specifically in the form of green bonds and loans, will have a statistically significant moderating effect on the relationship between renewable energy adoption and carbon tax-induced reductions in CO2 emissions in Eastern BRICS countries from 2001 to 2020, contingent upon varying levels of social globalization.

---

## RBV2-0279-N03

- **role:** dev-20 (held out once, now development); diagnostic phase 1/2
- **discipline:** Law
- **source DOI:** 10.1038/s41586-024-07018-7
- **literature cutoff:** 2023-11-01
- **runs:** 3; gold rank 2, 1, 2

**Question**

> How can we improve the efficacy of T-cell therapies, particularly in addressing their limitations in solid tumors and treatment-resistant hematological malignancies, such as poor in vivo persistence and T-cell exhaustion? Specifically, can we leverage naturally occurring mutations found in T-cell neoplasms to enhance therapeutic T-cell function, and if so, which specific mutations are most promising?

**Gold hypothesis**

Mutations found in T-cell neoplasms, specifically the CARD11-PIK3R3 gene fusion, can be utilized to enhance the anti-tumor activity of therapeutic T cells by increasing CBM signalosome activation, enhancing NF-κB and AP-1 signaling, boosting IL-2 production, and improving anti-tumor efficacy without evidence of malignant transformation.

**Negative hypothesis**

Genomically engineered T cells that specifically express mutated versions of TP53, CARD11, CCR4, PLCG1, and ZEB1, in combination with CRISPR-Cas9 gene editing, can enhance T-cell persistence in solid tumors by directly targeting T-cell exhaustion mechanisms, thereby improving therapeutic outcomes in patients with treatment-resistant cancer.

---

## RBV2-0131-N03

- **role:** dev-20 (held out once, now development); diagnostic phase 1/2
- **discipline:** Physics
- **source DOI:** 10.1016/j.jallcom.2024.174187
- **literature cutoff:** 2024-05-31
- **runs:** 3; gold rank 1, 1, 1

**Question**

> How can we develop a highly efficient and stable photocatalyst, based on silver vanadate, that can effectively degrade organic pollutants like methylene orange (MO) and tetracycline (TC) in water under visible light irradiation, overcoming the limitations of single-component photocatalysts?

**Gold hypothesis**

The synthesized AgVO3/Ag4V2O7/BiOI (AVO/AVO7/BOI) double S-scheme heterojunction photocatalyst will demonstrate enhanced photocatalytic performance for the degradation of methylene orange (MO) and tetracycline (TC) under visible light due to increased active sites from its irregular hexagonal morphology, efficient charge separation and transfer facilitated by the double S-scheme structure, and the formation of an internal electric field arising from the varying work functions of the components.

**Negative hypothesis**

A silver vanadate-based photocatalyst with a surface-engineered iodine-rich layer, synthesized via a controlled chemical precipitation method to achieve a uniform layer thickness of 5-10 nanometers, can enhance the internal electric field, leading to improved charge separation and significantly increased photocatalytic activity for the degradation of organic pollutants like methylene orange (MO) and tetracycline (TC) under visible light irradiation (400-500 nm) at a pH range of 6-8, through a synergistic effect where the iodine-rich layer modifies the silver vanadate's band structure, thereby boosting its photocatalytic performance.

---

## RBV2-0192-N05

- **role:** dev-20 (held out once, now development); diagnostic phase 1/2
- **discipline:** Physics
- **source DOI:** 10.1016/j.carbon.2024.119040
- **literature cutoff:** 2024-03-31
- **runs:** 3; gold rank 2, 1, 2

**Question**

> How can we improve the tribological performance (wear resistance and self-lubricating ability) of face-centered cubic (FCC) high-entropy alloys (HEAs), specifically CoCrFeNiMn, under dry sliding conditions, while avoiding the mechanical property degradation associated with conventional soft-solid lubricants?

**Gold hypothesis**

The proper incorporation of few-layer graphene as a reinforcement in CoCrFeNiMn high-entropy alloy (HEA), achieved through a tunable fabrication process that promotes a partially chemical interface reaction, leads to a tailored composite structure with enhanced tribological properties. This enhancement is due to the combined effect of in-situ carbide strengthening and graphene self-lubrication, resulting in significantly reduced wear rate and friction coefficient compared to most HEA-based self-lubrication composites.

**Negative hypothesis**

By leveraging the exceptional strain-hardening capabilities and self-healing properties of metallic glass (MG) films, and the electro-mechanical coupling characteristics of graphene, a 3D printed, hierarchical CoCrFeNiMn HEA/MG/graphene nanocomposite with a hybrid "honeycomb-spiral" lattice structure and surface-functionalized graphene layers will exhibit superior wear resistance, self-lubricating ability, and reduced CoF under dry sliding conditions, while maintaining the mechanical properties of pristine CoCrFeNiMn HEAs.

---

## RBV2-0135-N03

- **role:** dev-20 (held out once, now development); diagnostic phase 1/2
- **discipline:** Astronomy
- **source DOI:** 10.1016/j.newast.2024.102233
- **literature cutoff:** 2023-12-31
- **runs:** 3; gold rank 1, 2, 2

**Question**

> How can we analyze the photometric properties and orbital period variations of the short-period contact binary V415 Gem to better understand its structure and dynamics?

**Gold hypothesis**

V415 Gem is a W-subtype shallow contact binary with a mass ratio of approximately 2.297 and a contact degree of 3.6%, exhibiting an O'Connell effect due to cool star-spots and a cyclic variation in its orbital period attributed to the light-travel time effect of a third component with an estimated mass of approximately 1.08 solar masses.

**Negative hypothesis**

The photometric properties and orbital period variations of the short-period contact binary V415 Gem can be better understood by modeling its structure using a modified version of the convective common envelope model, where the adiabatic constants of the envelopes of the two companions are calculated using a self-consistent stellar evolution code and are constrained to be equal, and the mean radii of the components are calculated using a synthetic light-curve analysis and differ from the radii of the corresponding single stars predicted by the MESA stellar evolution grid.

---

## RBV2-0143-N04

- **role:** dev-20 (held out once, now development); diagnostic phase 1/2
- **discipline:** Physics
- **source DOI:** 10.1038/s41586-024-07276-5
- **literature cutoff:** 2024-03-18
- **runs:** 3; gold rank 1, 1, 2

**Question**

> How can we achieve long-term, stable, and efficient continuous-flow ammonia electrosynthesis via lithium-mediated nitrogen reduction (Li-NRR) with high gas-phase ammonia output, while overcoming the limitations of commonly used solvents like tetrahydrofuran (THF)?

**Gold hypothesis**

A chain-ether-based solvent, specifically diethylene glycol dimethyl ether (DG), can enable long-term continuous ammonia synthesis in a lithium-mediated nitrogen reduction (Li-NRR) system by exhibiting non-polymerization properties, a high boiling point, forming a compact and stable solid-electrolyte interphase (SEI) on the gas diffusion electrode (GDE) that facilitates ammonia release into the gas phase, and avoiding electrolyte degradation, thereby leading to high ammonia faradaic efficiency (FE) and a high percentage of ammonia in the gas phase.

**Negative hypothesis**

The incorporation of iodine as a supported catalyst in a modified lithium-mediated nitrogen reduction (Li-NRR) reactor design, with an optimal iodine concentration of 1 mol%, a surface area of 100 m²/g, and a supporting material of carbon nanotubes, can enhance the efficiency, stability, and gas-phase ammonia output of continuous-flow ammonia electrosynthesis, while reducing the limitations and costs associated with commonly used solvents like tetrahydrofuran (THF).

---

## RBV2-0138-N01

- **role:** dev-20 (held out once, now development); diagnostic phase 1/2
- **discipline:** Material Science
- **source DOI:** 10.1016/j.cej.2023.147667
- **literature cutoff:** 2023-12-31
- **runs:** 3; gold rank 1, 2, 2

**Question**

> How can we develop a cost-effective, efficient, and selective porous carbon material for CO2 capture, utilizing readily available and environmentally friendly resources and methods, while also enhancing surface functionality to improve adsorption capabilities?

**Gold hypothesis**

The use of potassium thiosulfate (K2S2O3) as both an activating and sulfur-doping agent during the pyrolysis of carbonized coconut shells (CS) provides a straightforward method to synthesize highly microporous, S-doped carbon materials that exhibit significant CO2 adsorption capacity, good CO2/N2 selectivity, high isosteric heat of adsorption, and excellent cycling stability, making them promising candidates for effective and selective CO2 capture.

**Negative hypothesis**

"Incorporating dual doping with sulfur (S) and phosphorus (P) into microporous carbon materials derived from biomass precursors via optimized thermal and chemical activation processes will enhance CO2 adsorption capacity and selectivity. This enhancement is hypothesized to arise from synergistic effects between S and P in promoting both microporosity and specific chemical binding to CO2. The methodology will focus on achieving uniform heteroatom doping through precursor pretreatment, quantifying the chemical states of S and P, and designing pore size distributions optimized for CO2 interactions."

---

---

## RBV2-0153-N03

- **role:** dev-20 (held out once, now development); diagnostic phase 1/2
- **discipline:** Energy Science
- **source DOI:** 10.1016/j.cej.2023.147980
- **literature cutoff:** 2021-12-31
- **runs:** 3; gold rank 2, 1, 2

**Question**

> How can a low-cost and easily fabricated separator material be developed to address the challenges of water-induced side reactions and dendrite growth in aqueous zinc-ion batteries (ZIBs) to achieve high stability and long cycle life?

**Gold hypothesis**

A low-cost separator composed of cellulose nanofibers (CNF) and lithium magnesium silicate (LMS) (CNF + LMS) can significantly improve the stability and cycle life of zinc-ion batteries by accelerating the desolvation kinetics of [Zn(H2O)6]2+ ions, promoting homogeneous zinc deposition on the anode surface, enhancing the separator's wettability, tensile strength, and ionic conductivity, effectively suppressing water-induced side reactions, and enabling dendrite-free zinc deposition for long cycling performance.

**Negative hypothesis**

"Incorporating a bio-inspired, hierarchically structured separator that combines cellulose nanofibers with a BaTiO3 ceramic component exhibiting piezoelectric properties will effectively suppress zinc dendrite growth and mitigate water-induced side reactions in aqueous zinc-ion batteries. The separator's hierarchical structure, achieved by layer-by-layer deposition, will enable electro-mechanical regulation through piezoelectric polarization at low-frequency mechanical vibrations of 10 Hz, fostering uniform Zn plating and enhanced battery stability over 3000 cycles at a current density of 0.5 mA cm−2."

---

## RBV2-0165-N01

- **role:** dev-20 (held out once, now development); diagnostic phase 1/2
- **discipline:** Energy Science
- **source DOI:** 10.1016/j.cej.2024.149776
- **literature cutoff:** 2024-03-31
- **runs:** 3; gold rank 1, 1, 1

**Question**

> How can we develop efficient and water-resistant Mn-based catalysts for the degradation of volatile organic compounds (VOCs), specifically toluene, using a novel, energy-efficient synthesis method that avoids high-temperature treatments?

**Gold hypothesis**

Mn-based catalysts with good toluene degradation performance (T90 = 209 °C) and water-resistance (5.0 vol%) can be synthesized through a non-thermal derivation method involving Na2CO3 solution treatment of Mn-MIL-100. The optimal catalyst, Mn-Na-1.0, exhibits an abundance of surface Mn3+ and Oads species, better surface lattice oxygen mobility, low-temperature reducibility, and high surface area, accounting for its high catalytic performance. Importantly, the introduced water vapor is activated and dissociated to form dissociation adsorbed active oxygen species, which serve as additional active sites and provide active oxygen species to accelerate the oxidation of intermediates and toluene mineralization.

**Negative hypothesis**

Controlled alkali treatment of manganese-based metal-organic frameworks (Mn-MOFs) at a specified concentration range (e.g., 0.1-0.5 M NaOH) for a defined duration (e.g., 1-4 hours) and under ambient temperature and stirring conditions can transform the frameworks into Mn(OH)\(_2\) nanostructures. This process retains a hierarchical porous structure conducive to catalysis and develops efficient and water-resistant catalysts for the degradation of volatile organic compounds (VOCs), specifically toluene, without the requirement for high-temperature treatments. Characterization techniques such as X-ray diffraction (XRD), scanning electron microscopy (SEM), and Brunauer-Emmett-Teller (BET) analysis will confirm the structural transformation and assess the surface area and porosity of the resulting catalysts.

---

## RBV2-0288-N00

- **role:** dev-20 (held out once, now development); diagnostic phase 1/2
- **discipline:** Law
- **source DOI:** 10.1016/j.tree.2023.09.014
- **literature cutoff:** 2023-12-31
- **runs:** 3; gold rank 1, 2, 1

**Question**

> How can climate change mitigation policies in Latin America be improved to avoid the pitfalls of tree monoculture plantations, specifically considering their impact on carbon sequestration and wildfire risk, and thus promote more resilient landscapes?

**Gold hypothesis**

The Chilean Climate Change Law's (CCL) exclusion of tree monocultures as a climate mitigation strategy and its focus on native forest restoration provide a valuable model for other Latin American countries. The experiences of Chile with mega-fires and the negative ecological impacts of homogeneous forest plantations demonstrate that relying on monocultures is not a sustainable or effective approach for carbon sequestration and climate resilience. Therefore, diverse landscapes, with a priority on native ecosystems, should be prioritized.

**Negative hypothesis**

Improving climate change mitigation policies in Latin America through the adoption of mixed-species reforestation (e.g., combining native species such as Melia azedarach and Eucalyptus robusta, along with other region-specific species like Cedrela odorata and Swietenia macrophylla) and integrated land management strategies (including controlled burns, buffer zones, and community-led conservation initiatives) can enhance carbon sequestration by 30% and reduce wildfire risk by 25% over five years compared to traditional tree monocultures.

---

## RBV2-0084-N05

- **role:** dev-20 (held out once, now development)
- **discipline:** Physics
- **source DOI:** 10.1016/j.radphyschem.2024.111640
- **literature cutoff:** 2024-04-30
- **runs:** 3; gold rank 1, 1, 1

**Question**

> How does increasing the concentration of Bi2O3 while correspondingly decreasing B2O3 in a Li2O-BaO-ZnO-B2O3-Bi2O3 glass system affect its structural, mechanical, and gamma-ray shielding properties?

**Gold hypothesis**

In the 5Li2O-5BaO-10ZnO-(30-x)B2O3-(50+x)Bi2O3 glass system, increasing the Bi2O3 content leads to a decrease in mechanical properties such as elastic moduli, packing density, and hardness, while enhancing gamma-ray shielding properties, evidenced by a measurable increase in the linear attenuation coefficient, particularly at lower gamma-ray energies.

**Negative hypothesis**

Increasing concentrations of Bi2O3 from 20% to 40% while correspondingly decreasing B2O3 in the Li2O-BaO-ZnO-B2O3-Bi2O3 glass system will result in optimized gamma-ray shielding efficacy, enhanced structural integrity as measured by modulus of rupture tests, and superior mechanical properties, with these effects specifically analyzed across a gamma energy range of 0.1 to 3 MeV. Monte Carlo simulations using the Geant4 software will be employed to predict and validate these changes.

---

## RBV2-0110-N03

- **role:** dev-20 (held out once, now development)
- **discipline:** Math
- **source DOI:** 10.1007/s10915-023-02412-1
- **literature cutoff:** 2021-12-31
- **runs:** 3; gold rank 2, 2, 1

**Question**

> How can the accuracy and reliability of physics-informed neural networks (PINNs) be improved for simulating problems involving strong nonlinear discontinuities, such as shock waves in hyperbolic equations?

**Gold hypothesis**

The introduction of the Physics-Informed Neural Networks with Equation Weights (PINNs-WE) framework enhances the capability of neural networks to simulate strong nonlinear discontinuities by utilizing a physics-dependent weighting strategy and incorporating the Rankine–Hugoniot relations as constraints, allowing for accurate capture of shock waves without additional dissipation.

**Negative hypothesis**

By implementing a gradient-statistics-driven learning rate annealing algorithm that dynamically adjusts based on gradient intensity and utilizing a novel network architecture incorporating layers designed specifically for handling nonlinear discontinuities, such as trainable differential operators and customized activations, we can significantly improve the accuracy and reliability of physics-informed neural networks (PINNs) in simulating problems like shock waves in hyperbolic equations.

---

## RBV2-0281-N03

- **role:** dev-20 (held out once, now development)
- **discipline:** Cell Biology
- **source DOI:** 10.1038/s43587-023-00560-5
- **literature cutoff:** 2023-09-25
- **runs:** 3; gold rank 1, 1, 2

**Question**

> How can senescent cells be effectively and safely targeted to ameliorate age-related pathologies and metabolic dysfunction using a novel therapeutic approach?

**Gold hypothesis**

The main hypothesis of this paper is that CAR T cells targeting uPAR can effectively eliminate uPAR-positive senescent cells in aged tissues, leading to improvements in metabolic function and physical fitness, with the potential for long-term therapeutic and preventive effects from a single administration.

**Negative hypothesis**

CAR T cells engineered with tandem chimeric antigen receptors (CARs) to dual-target urokinase-type plasminogen activator receptor (uPAR) and p16INK4a will more effectively and safely eliminate heterogeneous populations of senescent cells compared to targeting uPAR alone, thereby ameliorating specific age-related pathologies such as liver fibrosis and atherosclerosis in preclinical models.

---

## RBV2-0317-N03

- **role:** dev-20 (held out once, now development)
- **discipline:** Energy Science
- **source DOI:** 10.1016/j.eng.2022.06.005
- **literature cutoff:** 2023-07-31
- **runs:** 3; gold rank 2, 1, 2

**Question**

> How can we develop a miniaturized, cost-effective, sensitive, and reliable electrode for the concurrent and in situ detection of Pb<sup>2+</sup> and Cu<sup>2+</sup> in groundwater, overcoming the limitations of traditional analytical techniques and the poor conductivity of 2D metal oxide nanosheets?

**Gold hypothesis**

A miniaturized electrode based on AuNPs electrochemically seeded onto *in situ* grown mesoporous NiO on a nickel foam substrate can achieve simultaneous and sensitive detection of Pb<sup>2+</sup> and Cu<sup>2+</sup> in groundwater due to enhanced conductivity and electron transfer facilitated by the low-barrier Ohmic contact of AuNPs and the high surface area of the mesoporous NiO structure.

**Negative hypothesis**

A miniaturized, cost-effective, and sensitive electrode for concurrent detection of Pb²⁺ and Cu²⁺ ions in groundwater can be developed by integrating mesoporous 2D NiO nanosheets, functionalized with thiol and amine groups for enhanced selectivity, into a glassy carbon substrate. The electrode will employ differential pulse voltammetry to distinguish between ion-specific electrochemical responses, leveraging the high sensitivity and improved conductivity from Ag⁺-doped NiO nanosheets, showing reliability in varied groundwater matrices.

---

## RBV2-0117-N06

- **role:** dev-20 (held out once, now development)
- **discipline:** Energy Science
- **source DOI:** 10.1016/j.diamond.2023.110713
- **literature cutoff:** 2023-12-31
- **runs:** 3; gold rank 1, 1, 1

**Question**

> How can a simple, single-layer graphene-based metamaterial structure be designed to achieve ultra-wideband, high-efficiency, and tunable absorption in the terahertz frequency range, overcoming the complexity of multi-layered designs and providing stable absorption properties for practical applications?

**Gold hypothesis**

A terahertz absorber made of a single layer of graphene patterned with three distinct but interconnected rectangular graphene patterns can achieve three-peak broadband absorption in the terahertz band (1.53-4.92 THz) with high absorptivity (>0.9), by strategically combining the resonances of individual patterns, allowing for tuning via the Fermi energy level, and demonstrating stability against variations in incident angles and physical parameters.

**Negative hypothesis**

A single-layer graphene-based metamaterial absorber achieving ultra-wideband terahertz absorption through a precisely engineered hybrid-topology design, utilizing asymmetrically arranged metallic/dielectric resonant nanostructures (square-disk-loop patterns) with electrostatic gating-induced Fermi-level modulation. The design strategically manipulates both geometric resonances and electronic properties by implementing a periodic array of complementary nanostructures with sub-wavelength dimensions, enabling dynamically tunable absorption spanning 1-4 THz with >80% efficiency, characterized by a nanoscale electrostatic gating mechanism providing real-time absorption control.

---

## RBV2-0233-N00

- **role:** dev-20 (held out once, now development)
- **discipline:** Material Science
- **source DOI:** 10.1038/s41586-023-06786-y
- **literature cutoff:** 2024-01-02
- **runs:** 3; gold rank 2, 2, 1

**Question**

> How can we computationally predict the functional synthesizability of high-entropy ceramics (specifically carbides, carbonitrides, and borides) for hot-pressed sintering, considering both the entropic gain and enthalpy costs associated with disorder, and how can we overcome the computational cost of such prediction?

**Gold hypothesis**

The **Disordered Enthalpy-Entropy Descriptor (DEED)**, defined as the ratio of entropy gain (inverse of the standard deviation of the thermodynamic density of states) and enthalpy cost (expectation value of the POCC-tile energies to the convex hull), is a reliable descriptor for the functional synthesizability of high-entropy ceramics during hot-pressed sintering. Moreover, this DEED can be efficiently computed using a convolutional algorithm called cPOCC by approximating the thermodynamic density of states by the convolution of two subsystems' thermodynamic density of states.

**Negative hypothesis**

Predicting the functional synthesizability of high-entropy carbides, carbonitrides, and borides for hot-pressed sintering can be achieved through the incorporation of a hybrid disorder descriptor, which combines the energy distribution spectrum and configurational entropy, specifically utilizing density functional theory (DFT) and the Boltzmann formula to calculate configurational entropy, and is further augmented by a novel high-throughput approach, named "Compound Calculator", which utilizes a hybrid mean field statistical mechanical model, derived from a combination of ab-initio energies and Monte Carlo simulations, obtained from high-performance computing (HPC) facility leveraging the computational tools of Materials Project and AFLOW.

---

## RBV2-0246-N04

- **role:** dev-20 (held out once, now development)
- **discipline:** Law
- **source DOI:** 10.1016/j.marpol.2024.106017
- **literature cutoff:** 2024-02-29
- **runs:** 3; gold rank 1, 1, 1

**Question**

> What are the specific transaction costs that hinder the successful development and implementation of multi-use projects at sea, and what strategies can be employed to mitigate these costs?

**Gold hypothesis**

The successful development of multi-use at sea is significantly affected by transaction costs arising from risk and uncertainty, inadequate governance frameworks, and challenges in obtaining appropriate insurance coverage. These transaction costs manifest as costs associated with planning, deciding, changing plans, obtaining permits and licenses, resolving disputes, and writing and enforcing contracts. Mitigation strategies include implementing thorough risk analyses, clear management structures, and robust safety protocols, as well as developing dedicated regulations for multi-use and streamlining permitting processes.

**Negative hypothesis**

Developing a decentralized, permissioned blockchain-based platform, utilizing Hyperledger Fabric, for dynamic risk assessment and stakeholder communication in multi-use sea projects, will reduce specific transaction costs—including legal liabilities and insurance premiums—by enhancing transparency, trust, and collaborative decision-making. This platform will incorporate adaptive smart contracts that automatically adjust to new data inputs and stakeholder feedback, thereby fostering flexible, inclusive risk governance.

---

## RBV2-0052-N08

- **role:** dev-20 (held out once, now development)
- **discipline:** Energy Science
- **source DOI:** 10.1016/j.jcis.2023.11.159
- **literature cutoff:** 2024-02-29
- **runs:** 3; gold rank 1, 2, 2

**Question**

> How can we efficiently enhance the photocatalytic hydrogen evolution reaction (HER) of Cd0.9Zn0.1S (CZS) under visible light by suppressing electron-hole recombination and increasing reactive sites, while also maintaining the catalyst's recyclability and stability, specifically addressing the limitations of existing CZS-based photocatalysts?

**Gold hypothesis**

A novel ZFO@C/CZS composite with an S-scheme heterojunction will exhibit significantly enhanced photocatalytic hydrogen evolution reaction (HER) performance compared to the individual components (CZS or ZFO@C) due to efficient charge transfer, increased reactive sites, and reduced electron-hole recombination, leading to improved stability, recyclability, and higher apparent quantum efficiency (AQE).

**Negative hypothesis**

Carbon-coating on Cd0.9Zn0.1S (CZS) nanoparticles synthesized via chemical vapor deposition will enhance the photocatalytic hydrogen evolution reaction (HER) under visible light by improving charge carrier separation due to a porous carbon architecture that facilitates electron transfer, while increasing reactive sites through tailored carbon layer thickness of 20-50 nm, and maintaining catalyst stability and recyclability across multiple reaction cycles.

---

## RBV2-0050-N04

- **role:** dev-20 (held out once, now development)
- **discipline:** Astronomy
- **source DOI:** 10.1016/j.nima.2024.169329
- **literature cutoff:** 2024-06-30
- **runs:** 3; gold rank 1, 2, 1

**Question**

> How can we develop an effective gamma-ray detection system to enhance the detection and analysis of short gamma-ray bursts (SGRBs) resulting from neutron star mergers, in the context of multimessenger astrophysics?

**Gold hypothesis**

The StarBurst Multimessenger Pioneer, utilizing an array of thallium-doped cesium iodide (CsI:Tl) scintillation detectors read by silicon photomultipliers (SiPMs), can significantly enhance the detection and localization of short gamma-ray bursts (SGRBs) associated with neutron star mergers, due to its increased sensitivity and effective area compared to existing detectors like the Fermi Gamma-ray Burst Monitor.

**Negative hypothesis**

Implementing a network of 10 low-cost, lightweight gamma-ray detector arrays distributed across key geographical locations, synchronized with real-time data from existing gravitational-wave observatories, will improve the localization of short gamma-ray bursts (SGRBs) from neutron star mergers by at least 30% as measured by reduction in localization error. This configuration will utilize advanced data fusion algorithms to integrate gamma-ray detection and gravitational-wave signal processing, thereby enhancing multimessenger astrophysical studies.

---

## RBV2-0230-N02

- **role:** dev-20 (held out once, now development)
- **discipline:** Material Science
- **source DOI:** 10.1038/s41586-024-07723-3
- **literature cutoff:** 2024-06-25
- **runs:** 3; gold rank 2, 1, 1

**Question**

> How can we improve the power conversion efficiency and long-term stability of inverted perovskite solar cells by addressing the limitations of self-assembled monolayers (SAMs) at the buried interface, specifically focusing on poor wettability and agglomeration that lead to interfacial losses?

**Gold hypothesis**

The use of a hybrid self-assembled monolayer composed of Me-4PACz co-assembled with 4,4′,4″-nitrilotribenzoic acid (NA) will significantly enhance the interfacial characteristics of inverted perovskite solar cells by improving wettability, homogenizing the distribution of Me-4PACz, facilitating better carrier extraction, and reducing non-radiative recombination, ultimately leading to higher power conversion efficiency and improved long-term stability compared to devices using only Me-4PACz.

**Negative hypothesis**

Improving the long-term stability and power conversion efficiency of inverted perovskite solar cells by addressing the limitations of self-assembled monolayers (SAMs) at the buried interface through a novel, surface-engineering approach that combines tailored energy alignment with a dynamic, molecular "self-healing" mechanism. This mechanism will be induced by introducing specific metal-organic ligands that can dynamically bridge interfacial defects and adapt to conditions of poor wettability and agglomeration, facilitated by a trigger temperature of 80°C and optimized concentrations of 10wt% ligand to TCDI-1 matrix.

---

## RBV2-0210-N05

- **role:** calibration-20
- **discipline:** Energy Science
- **source DOI:** 10.1016/j.carbon.2024.119215
- **literature cutoff:** 2024-05-31
- **runs:** 1; gold rank 1

**Question**

> How can we develop high-performance, lightweight microwave absorbing materials (MAMs) that exhibit strong absorption, wide bandwidth, and thin thickness to effectively address the increasing electromagnetic wave (EMW) pollution from electronic devices, with a particular focus on metal selenides and their tunable stoichiometric compositions?

**Gold hypothesis**

Hollow spherical composites of Ni<ce:inf loc="post">x</ce:inf>Se<ce:inf loc="post">y</ce:inf> and nano-porous carbon (Ni<ce:inf loc="post">x</ce:inf>Se<ce:inf loc="post">y</ce:inf>@NC) with abundant selenium vacancies, synthesized through a solvothermal process and high-temperature selenylation, can achieve superior broadband microwave absorption, with tunable dielectric properties resulting in a minimum reflection loss of −54 dB and an optimal absorption bandwidth covering the entire Ku band at a thickness of only 1.67 mm.

**Negative hypothesis**

The synthesis of hierarchical cobalt selenide nanostructures with controlled Co:Se stoichiometric ratios (1:1, 1:1.5, and 1:2) will be achieved through a synergistic approach that combines a hydrothermal process (conducted at varying temperatures of 180-240 °C for 6-12 hours) for initial crystallization, followed by a precise electrospinning technique to layer the produced nanostructures. This method will fabricate multi-layered microwave absorbing materials (MAMs) with a total thickness less than 2 mm, achieving exceptional microwave absorption characterized by reflection losses greater than -60 dB over bandwidths exceeding 5 GHz across the Ku, X, and C bands. The optimization of electrospinning parameters—including voltage (15 kV), flow rate (1 mL/h), and collector distance (20 cm)—will be systematically investigated through a response surface methodology to determine the ideal conditions for absorption performance.

---

## RBV2-0218-N09

- **role:** calibration-20
- **discipline:** Law
- **source DOI:** 10.1016/j.heliyon.2024.e28601
- **literature cutoff:** 2024-03-31
- **runs:** 1; gold rank 1

**Question**

> How can data platform management, combined with structured analytical frameworks, effectively enhance corruption prevention and control in grassroots government, specifically addressing the limitations of existing methods that primarily focus on laws and regulations and often suffer from information asymmetry?

**Gold hypothesis**

The synergistic application of data platform management and the "5W" analysis framework, alongside other analytical models (SWOT, PDCA), significantly enhances the corruption prevention and control capabilities of grassroots governments, addressing information asymmetry and offering a more comprehensive method for combating corruption compared to traditional reliance on laws and regulations.

**Negative hypothesis**

Implementing a data platform management approach that operationalizes specific elements of the CARE theory of dignity — such as transparency protocols, access control technologies, and ethical review boards — can significantly enhance corruption prevention and control in grassroots government. This approach will effectively address information asymmetry and ensure the management of personal data respects individual dignity, thus improving public trust and participation.

---

## RBV2-0065-N07

- **role:** calibration-20
- **discipline:** Cell Biology
- **source DOI:** 10.1038/s41556-024-01360-8
- **literature cutoff:** 2024-02-28
- **runs:** 1; gold rank 1

**Question**

> How can the regulation and mechanisms of ferroptosis be understood and potentially leveraged for therapeutic strategies across a broad spectrum of diseases, including cancer and neurodegenerative disorders?

**Gold hypothesis**

Ferroptosis involves a complex molecular ecosystem that integrates signals from reactive oxygen species, oxidizable lipids, and lipid peroxidation, and by elucidating these mechanisms, its regulation can be potentially harnessed to develop therapies for diseases characterized by oxidative stress and cell death, such as cancer and neurodegenerative disorders.

**Negative hypothesis**

The targeted knockdown of GPX4 in cancer cells using an engineered CRISPR-dCas9 system fused with transcriptional repressors, delivered via lipid nanoparticle-based delivery mechanisms, can enhance ferroptosis in treatment-resistant cancers such as renal cell carcinoma and diffuse large B cell lymphoma, providing a precise, off-target-minimized therapeutic strategy.

---

---

## RBV2-0256-N04

- **role:** calibration-20
- **discipline:** Physics
- **source DOI:** 10.1016/j.cej.2024.148982
- **literature cutoff:** 2024-01-31
- **runs:** 1; gold rank 1

**Question**

> How can we effectively remove food dyes (specifically allura red AC, carmine, and tartrazine) from aqueous solutions using a low-cost, sustainable adsorbent derived from sweet potato residue, and what are the detailed molecular-level adsorption mechanisms involved?

**Gold hypothesis**

The adsorption of allura red AC and carmine on sweet potato residue-derived activated carbon (SPAC) follows a monolayer behavior, whereas tartrazine adsorption is a multi-layer process. These dyes adsorb through different configurations (horizontal, non-horizontal, or a combination), with tartrazine undergoing an aggregation process at various temperatures, carmine aggregating only at higher temperatures, and allura red AC showing no aggregation. The adsorption processes are endothermic physisorption and are driven by a combination of electrostatic, van der Waals forces, hydrogen bonding, and π-π stacking interactions. SPAC is shown to be a promising material, especially for allura red AC removal.

**Negative hypothesis**

Sweet potato residue-derived activated carbon, produced through chemical activation using iron (III) chloride at an optimal temperature of 900 °C and impregnation ratio determined through initial pilot studies, can effectively remove food dyes such as allura red AC, carmine, and tartrazine from aqueous solutions. This process utilizes a dual-layer adsorption mechanism, which will be modeled using a combination of monolayer, two-site, and double-layer adsorption models, specifically with the assistance of statistical physics models to predict adsorption kinetics, capacities, and thermodynamics. The unique structural and chemical properties of sweet potato residue, such as its higher carbohydrate content, are hypothesized to contribute to adsorption efficiency, distinguishing it from lignin-based analogs.

---

## RBV2-0122-N08

- **role:** calibration-20
- **discipline:** Chemistry
- **source DOI:** 10.1038/s41563-023-01702-1
- **literature cutoff:** 2023-10-25
- **runs:** 1; gold rank 2

**Question**

> How can we enable decentralized and sustainable electrochemical ammonia synthesis under ambient conditions using an alternative to lithium, which has traditionally been used in lithium-mediated nitrogen reduction reactions?

**Gold hypothesis**

Calcium can effectively mediate the electrochemical reduction of nitrogen to ammonia under ambient conditions, providing a sustainable alternative to lithium-based methods. The hypothesis is that using calcium tetrakis(hexafluoroisopropyloxy)borate (Ca[B(hfip)4]2) as the electrolyte achieves significant Faradaic efficiency, thus supporting the feasibility of using abundant materials for ammonia production.

**Negative hypothesis**

The application of low-valent calcium complexes stabilized by specific β-diketiminate ligands, under controlled electrochemical conditions such as a potential range of -1.0 to -2.0 V vs. a standard reference electrode and utilizing potassium as a terminal reductant, can facilitate the efficient reduction of dinitrogen to ammonia at ambient temperatures, outperforming traditional lithium-mediated methods in terms of reaction mechanism and product yield.

---

## RBV2-0200-N03

- **role:** calibration-20
- **discipline:** Energy Science
- **source DOI:** 10.1016/j.jes.2023.05.028
- **literature cutoff:** 2024-05-31
- **runs:** 1; gold rank 1

**Question**

> How can we improve the efficiency of photocatalytic CO2 reduction using crystalline carbon nitride (CCN) materials by creating a heterojunction that maximizes redox potential and facilitates efficient charge separation, and how does this affect the CO2 reduction pathway?

**Gold hypothesis**

An S-scheme heterojunction formed by depositing ultrafine WO3 nanoparticles onto the surface of crystalline carbon nitride (CCN) nanosheets will lead to enhanced optical capture, increased CO2 adsorption and activation, improved textural properties, and spatial separation and directed movement of light-triggered charge carriers, thereby maximizing redox potential and resulting in significantly improved photocatalytic CO2 reduction activity with high CO selectivity, stability, and reusability, occurring via intermediates CO2*-, COOH*, and CO*.

**Negative hypothesis**

Introducing a heterojunction between crystalline carbon nitride (CCN) and cadmium sulfide (CdS), synthesized through a hydrothermal method, can significantly enhance photocatalytic CO2 reduction efficiency by improving redox potential and charge separation. This improvement favors the selective formation of methane over methanol under UV-visible light irradiation at room temperature. Characterization techniques such as X-ray diffraction and transmission electron microscopy will confirm the heterojunction formation, while gas chromatography will be used to evaluate product selectivity.

---

## RBV2-0163-N04

- **role:** calibration-20
- **discipline:** Cell Biology
- **source DOI:** 10.1038/s41588-024-01664-3
- **literature cutoff:** 2022-04-14
- **runs:** 1; gold rank 1

**Question**

> How can spatially resolved omics data be utilized to accurately and efficiently cluster cells into distinct cell types and tissue domains, while addressing scalability challenges and integrating spatial information effectively?

**Gold hypothesis**

BANKSY is a scalable and versatile algorithm that integrates spatial and molecular information through a novel spatial feature augmentation strategy, allowing for accurate cell-type identification and tissue domain segmentation across diverse spatial omics datasets. By embedding cells in a product space that includes both their own transcriptome and local microenvironment, BANKSY outperforms existing methods in both cell typing and domain segmentation tasks.

**Negative hypothesis**

By utilizing MERFISH to generate spatially resolved single-cell transcriptomic data, we can cluster cells into distinct cell types and tissue domains with higher accuracy and efficiency. This is achieved by modifying existing clustering algorithms, such as k-means and hierarchical clustering, to incorporate spatial correlations directly into their distance metrics and feature engineering processes. This approach leverages combinatorial labeling techniques to process up to 1000 RNA species per cell, effectively addressing scalability challenges and integrating spatial dimensions into clustering analyses.

---

## RBV2-0199-N04

- **role:** calibration-20
- **discipline:** Environmental Science
- **source DOI:** 10.1038/s41566-024-01382-6
- **literature cutoff:** 2024-01-25
- **runs:** 1; gold rank 1

**Question**

> How can the performance and stability of blue perovskite light-emitting diodes (LEDs) be improved to reach efficiencies comparable to state-of-the-art blue organic LEDs and inorganic quantum dot LEDs?

**Gold hypothesis**

The incorporation of bis(triphenylphosphine)iminium chloride (PPNCl) as an ionic additive in mixed-halide perovskites enhances the formation of quasi-three-dimensional phases, reduces defect density, and improves energy transfer efficiency, resulting in efficient and stable blue-emitting light-emitting diodes (LEDs) with a maximum external quantum efficiency (EQE) of 21.4% and extended operational lifespan.

**Negative hypothesis**

By introducing a novel quaternary halide composition strategy with precisely controlled Br:Cl ratios (65-75 mol% Br, 25-35 mol% Cl), combined with a multi-layer interface passivation technique using bifunctional organic ligands with phosphonic and amino terminal groups, blue perovskite LEDs can achieve:
1) Spectral stability with wavelength deviation < 5% over 500 hours of continuous operation
2) Photoluminescence quantum yield improvement of >30%
3) Reduced non-radiative recombination through targeted surface and interfacial defect mitigation

---

## RBV2-0295-N08

- **role:** calibration-20
- **discipline:** Astronomy
- **source DOI:** 10.1016/j.nima.2024.169242
- **literature cutoff:** 2024-05-31
- **runs:** 1; gold rank 2

**Question**

> How can the angular resolution and sensitivity of MeV gamma-ray astronomy be improved by extending the sensitive energy range of an Electron-Tracking Compton Camera (ETCC) to higher energies?

**Gold hypothesis**

Utilizing double-hit events in an Electron-Tracking Compton Camera (ETCC) significantly enhances the angular resolution and extends the sensitive energy range from 0.2–2.1 MeV to up to 3.5 MeV, thereby improving the overall performance of MeV gamma-ray astronomy.

**Negative hypothesis**

The integration of a liquid time projection chamber (TPC) into the Electron-Tracking Compton Camera (ETCC) framework, paired with advanced convolutional neural networks (CNNs) to analyze event data, will enhance angular resolution to below 1 degree and sensitivity to above 500 counts per second per unit area for MeV gamma-ray detection, facilitating improved measurements of high-energy astrophysical phenomena.

---

## RBV2-0125-N08

- **role:** calibration-20
- **discipline:** Energy Science
- **source DOI:** 10.1007/s12011-023-03645-9
- **literature cutoff:** 2023-04-12
- **runs:** 1; gold rank 2

**Question**

> How can we effectively synthesize metal nanoparticles using green, environmentally friendly, cost-effective, and non-toxic methods, specifically focusing on plant-based approaches, and how can these nanoparticles be characterized and applied for antimicrobial, anticancer, dye degradation, and wastewater treatment purposes?

**Gold hypothesis**

Plant-based green synthesis methods provide a viable, eco-friendly, cost-effective, non-toxic, and stable approach for producing metal nanoparticles, which can be characterized and applied in various biomedical and environmental applications, such as antimicrobial, anticancer, dye degradation, and wastewater treatment.

**Negative hypothesis**

The use of leaf extracts from Camellia sinensis and Hibiscus sabdariffa, which are rich in flavonoids and phenolic compounds, significantly enhances the synthesis efficiency of silver nanoparticles through a unique reduction mechanism that minimizes aggregation, resulting in nanoparticles with improved antimicrobial, anticancer, and dye degradation properties compared to those synthesized using traditional chemical reduction methods.

---

## RBV2-0203-N00

- **role:** calibration-20
- **discipline:** Energy Science
- **source DOI:** 10.1016/j.rinp.2024.107509
- **literature cutoff:** 2024-02-29
- **runs:** 1; gold rank 1

**Question**

> How can we design a cost-effective, easily fabricated plasmonic light absorber (PLA) that achieves ultra-broadband and wide-angle absorption in the visible and near-infrared regions, suitable for applications like solar energy harvesting, without relying on complex multilayered structures or noble metals?

**Gold hypothesis**

The proposed plasmonic light absorber (PLA), consisting of a periodic array of all-dielectric GaAs cylinder resonators (CR) adhered to an ultra-thin GaAs spacer layer backed with a tungsten (W) substrate, can achieve ultra-broadband (0.39 μm to 2.09 μm with a 137.1% relative bandwidth) and wide-angle absorption (stable up to 55° for TE mode and 75° for TM mode). The designed PLA achieves a remarkable short-circuit current density of over 64.75569 mA/cm² and exhibits nearly perfect solar energy trapping due to the effective coupling of multiple resonances, resulting in enhanced photovoltaic performance.

**Negative hypothesis**

We propose a plasmonic light absorber (PLA) design utilizing a cascade-coupled resonator architecture with gradient-doped InGaAs/GaAs semiconductor nanostructures. The metasurface will systematically modulate bandgap transitions across a precisely engineered composition gradient (x = 0.2-0.7 in In1-xGaxAs), creating a spatially-controlled mode interaction system. By implementing a targeted doping concentration range of 1 × 10^18 to 5 × 10^19 cm^-3 and maintaining a consistent layer thickness of 100-300 nm, we aim to achieve ultra-broadband absorption (wavelength range 600-1500 nm) with controlled mode coupling mechanisms that enhance absorption through critically coupled resonant modes.

---

## RBV2-0305-N01

- **role:** calibration-20
- **discipline:** Business
- **source DOI:** 10.1007/s10639-023-12080-1
- **literature cutoff:** 2023-08-14
- **runs:** 1; gold rank 2

**Question**

> What are the key determinants influencing Gen Z students' adoption intentions of metaverse technology in higher education settings in Jordan?

**Gold hypothesis**

The extended UTAUT2 model, which includes Personal Innovativeness in IT, effectively predicts Gen Z students' intentions to adopt metaverse technology in educational settings, with factors such as performance expectancy, effort expectancy, facilitating conditions, hedonic motivation, and price value significantly influencing adoption intentions, while social influence does not. Personal Innovativeness in IT is identified as a crucial determinant impacting adoption intentions both directly and indirectly through performance and effort expectations.

**Negative hypothesis**

The adoption intentions of metaverse technology among Gen Z students in higher education settings in Jordan are significantly influenced by hedonic motivation, price value perception, and habit. These influences are moderated by individual differences such as age, gender, and experience, which will be quantitatively measured using targeted surveys with validated scales for each construct. Regression analysis and structural equation modeling will be employed to analyze these relationships.

---

## RBV2-0284-N01

- **role:** calibration-20
- **discipline:** Energy Science
- **source DOI:** 10.1016/j.fuel.2023.129688
- **literature cutoff:** 2024-01-31
- **runs:** 1; gold rank 1

**Question**

> How can we improve the cycling stability and specific capacitance of transition metal-based spinel oxide supercapacitor electrodes, which suffer from limited surface area, while maintaining their cost-effectiveness?

**Gold hypothesis**

A CuAl2O4/rGO nanocomposite, synthesized via a simple hydrothermal method, will exhibit significantly enhanced supercapacitor performance compared to individual CuAl2O4 or rGO, with rGO acting as a support structure to increase the electroactive surface area of CuAl2O4, leading to higher specific capacitance, better cycling stability, and improved energy and power density.

**Negative hypothesis**

Incorporating a gradient multilayer structure of spinel ferrite@graphene nanocomposites, specifically with a compositional gradient ranging from higher ferrite content at the base to higher graphene content at the top, into transition metal-based spinel oxide supercapacitor electrodes, fabricated through a controlled hydrothermal synthesis method, can significantly enhance cycling stability and specific capacitance while maintaining cost-effectiveness.

---

## RBV2-0095-N03

- **role:** calibration-20
- **discipline:** Cell Biology
- **source DOI:** 10.1038/s41586-024-07379-z
- **literature cutoff:** 2024-04-07
- **runs:** 1; gold rank 1

**Question**

> How can broad-spectrum RAS inhibition be effectively used to treat pancreatic ductal adenocarcinoma (PDAC) driven by KRAS mutations, and how can resistance to this treatment be overcome?

**Gold hypothesis**

The main hypothesis of the paper is that RMC-7977, a multi-selective RAS(ON) inhibitor, can effectively inhibit the active GTP-bound forms of KRAS, HRAS, and NRAS in pancreatic ductal adenocarcinoma (PDAC) models, providing significant anti-tumor activity while maintaining a suitable therapeutic index. Furthermore, it suggests that combining RMC-7977 with TEAD inhibitors can overcome resistance mechanisms identified in relapsed tumors, such as Myc copy number gain.

**Negative hypothesis**

A combination therapy of the broad-spectrum RAS inhibitor XYZ (a specific inhibitor under preclinical or clinical investigation) with a targeted ERK pathway inhibitor ABC (e.g., selumetinib or a comparable compound) will synergistically reduce tumor burden and overcome drug resistance in pancreatic ductal adenocarcinoma (PDAC) driven by KRAS mutations. This combination will be administered using a sequential dosing approach guided by pharmacokinetic and pharmacodynamic profiling of both inhibitors, with resistance development monitored in patient-derived xenografts (PDX) and KRAS-mutant PDAC organoid models.

---

## RBV2-0114-N00

- **role:** calibration-20
- **discipline:** Cell Biology
- **source DOI:** 10.1038/s41586-023-06855-2
- **literature cutoff:** 2023-04-30
- **runs:** 1; gold rank 2

**Question**

> The paper investigates how the Gabija anti-phage defense system in bacteria operates at the molecular level to protect cells from viral infection, and how viruses can overcome this defense mechanism. Specifically, it aims to uncover the structural basis of the Gabija complex's assembly and function, and the mechanisms of viral evasion.

**Gold hypothesis**

The Gabija defense system in bacteria comprises a supramolecular complex formed by GajA and GajB proteins, essential for phage resistance, with GajA functioning as a DNA endonuclease and GajB possessing a helicase domain, while the viral protein Gad1 can evade this defense by encapsulating the GajAB complex, thereby inhibiting its DNA-binding and cleavage activities.

**Negative hypothesis**

A specific protein component of the Gabija anti-phage defense system contains a Toprim domain characterized by conserved glutamate and aspartate residues, which facilitates magnesium-dependent endonucleolytic cleavage of double-stranded viral DNA. This catalytic activity is essential for the Gabija system's function in neutralizing phage infection.

---

## RBV2-0232-N00

- **role:** calibration-20
- **discipline:** Earth Science
- **source DOI:** 10.1038/s41560-023-01375-9
- **literature cutoff:** 2023-10-04
- **runs:** 1; gold rank 2

**Question**

> How can earth-abundant, inexpensive cathode materials be designed to enable high energy density and rate capability in Li-ion batteries while avoiding voltage fade during cycling?

**Gold hypothesis**

The main hypothesis of the paper is that starting from a high-Mn-content disordered rock salt (DRX), it is possible to achieve a high-capacity cathode material by allowing it to transform during electrochemical cycling into a δ phase with partial spinel-like ordering, facilitated by Mn mobility, resulting in high energy density and rate capability without the typical voltage fade seen in other Mn-based cathodes.

**Negative hypothesis**

The mechanochemically synthesized Li4Mn2O5 cathode material with engineered nanostructured surface defects and tailored chemical composition will exhibit a unique combination of high energy density, rate capability, and electrochemical stability, while avoiding voltage fade during cycling, by harnessing the synergistic effects of localized lattice instability, multi-electron transfer processes, and optimized redox activity.

---

## RBV2-0058-N03

- **role:** calibration-20
- **discipline:** Law
- **source DOI:** 10.1016/j.foodchem.2023.136990
- **literature cutoff:** 2023-12-31
- **runs:** 1; gold rank 2

**Question**

> How can we efficiently and effectively screen for optimal natural deep eutectic solvents (NDES) and optimize the extraction process parameters for lentinan from shiitake mushrooms, moving beyond time-consuming empirical methods to achieve high extraction yields while preserving lentinan's biological activity?

**Gold hypothesis**

A combined approach using COSMO-RS for in silico screening of a large library of natural deep eutectic solvent (NDES) candidates can effectively identify optimal solvent compositions for lentinan extraction from shiitake mushrooms, and an ANN-GA model can successfully optimize key extraction parameters (time, temperature, and liquid-to-solid ratio) for the selected NDES, leading to significantly improved lentinan yields compared to traditional methods.

**Negative hypothesis**

The development of a hybrid model combining reinforcement learning (RL) with Bayesian optimization (BO) can efficiently and effectively screen for optimal natural deep eutectic solvents (NDES) and optimize the extraction process parameters for lentinan from shiitake mushrooms, resulting in high extraction yields while preserving lentinan's biological activity. Specifically, this approach will leverage RL to dynamically adjust extraction parameters in real-time based on feedback from the extraction process, while BO will be used to iteratively refine NDES formulations and extraction conditions by balancing exploration and exploitation.

---

## RBV2-0285-N04

- **role:** calibration-20
- **discipline:** Cell Biology
- **source DOI:** 10.1038/s41586-023-06799-7
- **literature cutoff:** 2024-01-02
- **runs:** 1; gold rank 2

**Question**

> How can we develop a new class of antibiotics that effectively targets the lipopolysaccharide (LPS) transport machinery in Gram-negative bacteria, particularly Acinetobacter species, to combat antibiotic resistance?

**Gold hypothesis**

A new class of macrocyclic peptide antibiotics can effectively inhibit the LPS transporter in Acinetobacter by binding to a substrate-bound conformation of the transporter, trapping it in a non-functional state that prevents further LPS transport and hinders bacterial viability.

**Negative hypothesis**

Developing a dual-functional small-molecule antibiotic targeting the MsbA transporter, which combines an allosteric inhibitor that locks MsbA in an inward-facing conformation with a prodrug moiety specifically cleaved by bacterial LpxC enzymes, will combat Acinetobacter species by disrupting LPS transport and amplifying bacterial killing through localized activation.

---

---

## RBV2-0140-N01

- **role:** calibration-20
- **discipline:** Energy Science
- **source DOI:** 10.1016/j.applthermaleng.2023.121578
- **literature cutoff:** 2023-12-31
- **runs:** 1; gold rank 1

**Question**

> How can we design an air-cooled battery thermal management system (BTMS) for electric vehicles that maintains optimal temperature uniformity and efficiently handles varying operating conditions, particularly high discharge rates, while avoiding complex control strategies?

**Gold hypothesis**

A parallel air-cooled battery thermal management system (BTMS) that intelligently integrates J-type, U-type, and L-type flow patterns, coupled with a control strategy that dynamically switches between these flow types based on the location of the highest temperature within the battery pack, along with structurally decreased widths of parallel channels at both ends, can maintain a temperature difference below 0.5 K under high discharge rates and varying operating conditions, significantly improving temperature uniformity compared to systems that rely on a single flow pattern.

**Negative hypothesis**

A neural network-based model can be developed to optimize a reciprocating airflow system for thermal management of Li-ion battery packs in electric vehicles. This model will use historical thermal performance data and real-time sensor inputs, such as temperature, discharge rates, and airflow velocity, to predictively adjust airflow periods and velocities. These predictions will be integrated into the operation of the airflow system using a defined set of actuator commands, while maintaining simplicity by avoiding complex real-time control strategies. The proposed system will be validated through experimental setups replicating varying discharge rate conditions, ensuring robustness and adaptability to real-world environments.

---

## RBV2-0098-N08

- **role:** calibration-20
- **discipline:** Law
- **source DOI:** 10.1016/j.ribaf.2023.102118
- **literature cutoff:** 2023-12-31
- **runs:** 1; gold rank 1

**Question**

> How does the digitalization of Chinese A-share listed companies impact the probability of successful completion of their cross-border Mergers and Acquisitions (M&A) transactions?

**Gold hypothesis**

Firm digitalization positively influences the completion rate of cross-border M&A transactions for Chinese A-share listed companies, with this effect being amplified in situations with higher financial constraints, for technology-based M&A transactions, and when there are shorter institutional distances. This positive impact is achieved through enhanced innovation capabilities that reduce the technology gap with target firms and provide more accurate valuations, as well as through the mitigation of management myopia, which promotes more strategic long-term planning.

**Negative hypothesis**

Increased adoption of advanced digital technologies (specifically, AI-powered analytics platforms and integrated cloud-based ERP systems) by Chinese A-share listed acquiring companies will decrease the likelihood of achieving pre-defined synergy targets within three years post-completion of cross-border M&A transactions. This is because the readily available, granular, and often short-term oriented data provided by these technologies may lead acquiring company managers to overemphasize easily quantifiable, short-term metrics of the target firm during due diligence and integration planning, potentially neglecting crucial long-term strategic alignment and integration complexities that are less amenable to immediate digital measurement.

---

## RBV2-0063-N05

- **role:** reserve-12 (spent, one use)
- **discipline:** Business
- **source DOI:** 10.1016/j.techfore.2023.123153
- **literature cutoff:** 2024-02-29
- **runs:** 1; gold rank 2

**Question**

> How can regions rich in natural resources overcome challenges to achieve digital transformation?

**Gold hypothesis**

While digital transformation is typically weaker in resource-rich regions, this drawback can be mitigated if these regions have strong awareness, motivation, and capability. Specifically, government reports (awareness), resource consumption (motivation), and the presence of researchers (capability) positively influence the extent of digital transformation.

**Negative hypothesis**

In natural-resource-rich regions, implementing targeted digital literacy programs tailored to local industry needs (e.g., mining, agriculture) significantly enhances the effectiveness and speed of digital transformation, when combined with organizational cultural adaptations that mitigate resistance to change.

---

## RBV2-0083-N01

- **role:** reserve-12 (spent, one use)
- **discipline:** Environmental Science
- **source DOI:** 10.1038/s41579-023-00967-2
- **literature cutoff:** 2023-09-10
- **runs:** 1; gold rank 1

**Question**

> How does plastic pollution, specifically microplastics, affect the microbial communities in soil ecosystems, and what are the implications for soil health and environmental change?

**Gold hypothesis**

The soil plastisphere represents a distinct microbial environment influenced by the presence of plastic particles, leading to lower microbial diversity compared to bulk soil, with certain microbial taxa and functional genes, including antibiotic resistance genes, being enriched in the plastisphere, suggesting potential implications for soil health and environmental risk.

**Negative hypothesis**

The cascading effects of microplastic-induced disturbances in soil pH and nutrient cycling lead to a tipping point in soil microbial communities, resulting in a decline in beneficial fungi and bacteria, and a subsequent decrease in soil organic matter turnover, altered nutrient availability, and impaired plant growth and ecosystem services in high-diversity soils with intermediate levels of pH variability.

---

## RBV2-0108-N03

- **role:** reserve-12 (spent, one use)
- **discipline:** Material Science
- **source DOI:** 10.1016/j.jhazmat.2023.132803
- **literature cutoff:** 2022-12-31
- **runs:** 1; gold rank 1

**Question**

> How can a durable and self-cleaning membrane be developed to efficiently separate oil from water, particularly high-viscosity crude oil emulsions, while also rapidly degrading organic pollutants within the wastewater, addressing limitations in existing membranes' mechanical stability, fouling resistance, and slow degradation rates?

**Gold hypothesis**

A PVA/GO@MOF membrane, fabricated through chemical crosslinking and suction filtration, will exhibit superior performance in oily wastewater treatment due to the incorporation of UiO-66-NH2 MOF nanoparticles within a PVA/GO matrix, resulting in a robust, porous structure with enhanced water absorption, hydrophilicity, and photocatalytic activity; the GO nanosheets will provide photothermal conversion capabilities and mechanical stability, leading to exceptional underwater superoleophobicity, low oil adhesion, high separation efficiency for high-viscosity crude oil emulsions, and rapid self-cleaning through synergistic photothermal and photocatalytic effects, all while maintaining robust chemical and mechanical stability in harsh environments.

**Negative hypothesis**

A composite membrane integrating UiO-66-NH2@PAA-modified MOFs with covalently bonded TiO2 nanoparticles can achieve simultaneous high-efficiency oil/water separation, enhanced fouling resistance, and accelerated degradation of organic pollutants in wastewater. Specifically, the TiO2 nanoparticles, incorporated via surface grafting onto the MOF structure, will utilize visible light photocatalysis to enhance pollutant degradation rates. Design considerations include nanoparticle loading at 5% by weight, TiO2 particle sizes of ~10 nm, and a performance evaluation in emulsified crude oil matrices to maintain ≥99% separation efficiency over 50 cycles, while achieving degradation of model pollutants at rates of ≥10 mg/L/hour under 10 mW/cm² visible light irradiation.

---

## RBV2-0113-N08

- **role:** reserve-12 (spent, one use)
- **discipline:** Energy Science
- **source DOI:** 10.1038/s41586-023-06927-3
- **literature cutoff:** 2023-12-05
- **runs:** 1; gold rank 1

**Question**

> How can we overcome the limitations of physical qubit control in current quantum processors to enable the development and practical utility of large-scale, fault-tolerant quantum computation for complex algorithms, particularly for those that are difficult to simulate classically? This includes addressing the overhead associated with logical qubit encoding and the efficient control of many physical qubits.

**Gold hypothesis**

A programmable quantum processor based on encoded logical qubits, implemented using reconfigurable neutral-atom arrays with a zoned architecture, can achieve improved algorithmic performance by utilizing hardware-efficient control over logical qubits with parallel, transversal gates. This system allows for scaling to larger code distances, fault-tolerant logical algorithms, and the realization of complex, classically hard circuits.

**Negative hypothesis**

Implement a hybrid quantum-classical control model on neutral-atom platforms, utilizing reinforcement learning algorithms to dynamically adjust qubit configurations and gate operations. Specifically, employ deep Q-networks to optimize control parameters in response to real-time fidelity and error rate metrics, thereby enhancing qubit coherence and reducing logical qubit encoding overhead.

---

## RBV2-0132-N09

- **role:** reserve-12 (spent, one use)
- **discipline:** Energy Science
- **source DOI:** 10.1016/j.apcatb.2023.123669
- **literature cutoff:** 2024-04-30
- **runs:** 1; gold rank 1

**Question**

> How can we develop a highly efficient, stable, and visible-light-driven photocatalyst that can simultaneously remove toxic Cr(VI) and organic pollutants like tetracycline (TC) from wastewater, addressing the limitations of existing photocatalytic materials and processes?

**Gold hypothesis**

A direct Z-scheme PPy/NH2-UiO-66 heterojunction, synthesized by ball milling, exhibits significantly enhanced photocatalytic activity for the reduction of Cr(VI) and the degradation of tetracycline (TC) due to improved light capture ability, high redox potential, enhanced interfacial charge transfer, and improved separation efficiency of photogenerated carriers resulting from the synergistic combination of PPy and NH2-UiO-66.

**Negative hypothesis**

A polypyrrole (PPy)-based supramolecular photocatalyst, doped with iron (Fe) and cobalt (Co) and functionalized with carboxylic acid ligands, can efficiently and stably remove both toxic Cr(VI) and organic pollutants like tetracycline (TC) from wastewater under visible-light irradiation. The dopants enhance the redox capability and photocatalytic efficiency by facilitating electron transfer, while the carboxylic acid ligands improve selectivity and stability through enhanced surface interactions.

---

## RBV2-0159-N04

- **role:** reserve-12 (spent, one use)
- **discipline:** Energy Science
- **source DOI:** 10.1016/j.jenvman.2023.119545
- **literature cutoff:** 2023-12-31
- **runs:** 1; gold rank 2

**Question**

> How can a novel, stable, and efficient photocatalyst be developed, specifically a copper-based complex, to effectively degrade a variety of hazardous organic dyes (erythrosine, malachite green, methylene blue, and Eriochrome Black T) in wastewater under visible light irradiation, addressing the limitations of traditional UV-responsive photocatalysts?

**Gold hypothesis**

A novel rod-like octahedral distorted coordination complex, [Cu(phen)2(OAc)]·PF6, can be synthesized and effectively utilized as a visible-light-driven photocatalyst for the degradation of hazardous organic dyes, demonstrating high photocatalytic efficiency, especially for cationic dyes, with minimal loss of efficiency over multiple reuse cycles.

**Negative hypothesis**

A novel photocatalyst, synthesized using a sol-gel method, consisting of a copper complex doped into carbon nitride (Cu-g-C3N4), will effectively degrade hazardous organic dyes such as erythrosine, malachite green, methylene blue, and Eriochrome Black T in wastewater under visible light. This photocatalyst aims to demonstrate enhanced stability and degradation efficiency through increased charge separation and visible light absorption, outperforming traditional UV-responsive photocatalysts.

---

## RBV2-0193-N06

- **role:** reserve-12 (spent, one use)
- **discipline:** Business
- **source DOI:** 10.1016/j.jbusres.2023.114325
- **literature cutoff:** 2023-12-31
- **runs:** 1; gold rank 2

**Question**

> How can virtual influencers (VIs), which are artificial computer-generated personas, be perceived as authentic in the metaverse, and what are the manifestations of such authenticity?

**Gold hypothesis**

Virtual influencers (VIs) can be perceived as authentic through manifestations of true-to-ideal authenticity (matching a socially constructed ideal), true-to-fact authenticity (disclosure of their virtual nature), and true-to-self authenticity (the creators' intrinsic motivations).

**Negative hypothesis**

Virtual influencers in the metaverse can achieve perceived authenticity by incorporating visually asymmetrical features, subtle behavioral quirks, and carefully timed communicative nuances, which align with the uncanny valley concept. This strategy involves controlled design parameters, systematic integration techniques, and precise measurement metrics to optimize the human-like imperfections that enhance authenticity.

---

## RBV2-0206-N00

- **role:** reserve-12 (spent, one use)
- **discipline:** Law
- **source DOI:** 10.1007/s11846-023-00631-2
- **literature cutoff:** 2023-03-06
- **runs:** 1; gold rank 2

**Question**

> How do different types of family involvement (specifically family ownership and family control) affect a firm's adoption of ESG criteria and ESG scores, and how are these relationships moderated by market competition and the institutional environment?

**Gold hypothesis**

Both family ownership and family control are positively related to a firm's ESG score, indicating that family involvement generally encourages the adoption of ESG criteria. Additionally, market competition negatively moderates the relationship between both family ownership/control and ESG scores, suggesting that increased competition diminishes the likelihood of prioritizing ESG. The institutional environment negatively moderates the relationship between family control and ESG scores, implying that a stronger institutional context weakens the positive impact of family control on ESG adoption.

**Negative hypothesis**

Family firms are more likely to adopt Environmental, Social, and Governance (ESG) criteria and achieve higher ESG scores when the socioemotional wealth they seek to preserve aligns with ESG principles, and this effect is more pronounced in highly competitive markets with supportive institutional environments. Specifically, socioemotional wealth will be measured using a composite index derived from surveys and archival data, ESG criteria adoption will be quantified using third-party ESG ratings and self-reported data, market competition will be assessed using Herfindahl-Hirschman Index (HHI) scores, and institutional support will be evaluated using World Bank governance indicators.

---

## RBV2-0207-N00

- **role:** reserve-12 (spent, one use)
- **discipline:** Physics
- **source DOI:** 10.1016/j.apcatb.2023.123196
- **literature cutoff:** 2023-12-31
- **runs:** 1; gold rank 1

**Question**

> How can we enhance the efficiency of photocatalytic hydrogen production, specifically when coupled with selective oxidation of organic molecules, by optimizing interfacial electron transfer rates in a quantum dot-based system? Specifically, how to make fast electron transfer from CdS quantum dots to a Pt cocatalyst for efficient hydrogen production with high selectivity?

**Gold hypothesis**

Atomically dispersed Pt-modified CdS quantum dots (Pt-CdS QDs), prepared through a one-step in-situ method, achieve ultrafast electron transfer (∼1.7 ps) from CdS to Pt due to strong electronic metal-support interactions (EMSI). This fast electron transfer facilitates enhanced photocatalytic hydrogen evolution when coupled with the selective oxidation of 2-thiophene methanol (TM) to 2-thiophenecarboxaldehyde (TD), resulting in significantly improved H2-production rates and high selectivity for the desired oxidation product.

**Negative hypothesis**

Developing a quantum-engineered multifunctional electron transfer interface for CdS quantum dots by implementing a synergistic tri-modal strategy: (1) precise electronic metal-support interaction (EMSI) via 2-3 nm MoS2 nanosheets with controlled sulfur vacancies and preferential (002) crystal orientation, (2) strategically modulated Zn2+ surface functionalization with in-situ electrochemical reduction to generate atomically dispersed electron mediators, and (3) tailored sulfur vacancy engineering to create programmable charge transfer pathways, enabling unprecedented photocatalytic hydrogen production efficiency through comprehensive interfacial electronic structure optimization.

---

## RBV2-0222-N05

- **role:** reserve-12 (spent, one use)
- **discipline:** Math
- **source DOI:** 10.1007/s13399-022-02664-1
- **literature cutoff:** 2022-02-08
- **runs:** 1; gold rank 1

**Question**

> How can agronomic waste materials, particularly mandarin peels, be effectively utilized as low-cost biosorbents for the removal of synthetic aromatic dyes like Acid Brown 14 (AB14) from industrial wastewater?

**Gold hypothesis**

The main hypothesis of the paper is that mandarin peel-derived biosorbent, when modified with triethylenetetramine (TETA) to form Mandarin-CO-TETA (MCT), can serve as an effective and low-cost biosorbent for the removal of Acid Brown 14 dye from industrial wastewater, with the process being pH-dependent and following pseudo-second-order kinetics and Langmuir isotherm models, indicating monolayer sorption.

**Negative hypothesis**

Mandarin peels, when subjected to a specified two-stage functionalization process involving optimal concentrations of triethylenetetramine (TETA) at controlled low temperatures and specific pH levels, followed by NaOH chemical activation, can serve as superior biosorbents with enhanced adsorption capacities as quantified by kinetics and capacity at equilibrium for the removal of synthetic aromatic dyes such as Acid Brown 14 (AB14) from industrial wastewater, demonstrating efficiency over existing materials.

---

## RBV2-0225-N02

- **role:** reserve-12 (spent, one use)
- **discipline:** Astronomy
- **source DOI:** 10.1038/s41550-023-02107-5
- **literature cutoff:** 2023-10-29
- **runs:** 1; gold rank 2

**Question**

> What is the detailed composition of Ganymede's surface at a local scale, and how can this composition inform our understanding of its geological processes and potential habitability?

**Gold hypothesis**

Ganymede's surface is composed of a mixture of salts and organics, including hydrated sodium chloride, ammonium chloride, sodium/ammonium carbonate, and possibly organic compounds like aliphatic aldehydes, suggesting that these materials originate from endogenic processes such as the extrusion of subsurface brines that may have interacted with the moon's rocky interior.

**Negative hypothesis**

The local-scale distribution of hydrated magnesium sulfate minerals on Ganymede's surface will be quantitatively mapped using high-resolution near-infrared spectroscopy and statistical correlation analysis, with mineral concentration gradients mathematically modeled as a function of subsurface ocean convection dynamics through a multi-parameter geophysical regression framework that establishes statistically significant correlations between surface mineralogical patterns and underlying fluid movement at meter-level spatial resolution.

---

## RBV2-0226-N06

- **role:** reserve-12 (spent, one use)
- **discipline:** Math
- **source DOI:** 10.1016/j.csite.2023.103928
- **literature cutoff:** 2023-12-31
- **runs:** 1; gold rank 2

**Question**

> How can the solidification process of phase change materials (PCMs) be accelerated through the use of nanoparticles and optimized system geometry, while maintaining precision in modeling and improving energy transfer performance?

**Gold hypothesis**

The introduction of alumina nanoparticles with varying shape factors (m) and volume fractions (φ), combined with an optimized finned tank geometry and adaptive grid modeling, can significantly enhance the freezing rate of phase change materials (PCMs) by improving thermal conductivity and reducing solidification time, with specific increases in conductivity leading to reduced freezing times of up to 26.9%.

**Negative hypothesis**

Incorporating a hybrid nanoparticle blend of graphene, aluminum oxide (Al₂O₃), and carbon nanotubes into a multi-layered honeycomb structure, where cell geometry and nanoparticle distribution are dynamically optimized based on real-time thermal flux gradients, can significantly accelerate the solidification process of paraffin-based phase change materials (PCMs). This approach enhances thermal conductivity pathways and convective heat transfer, precisely modeled with a multi-scale adaptive finite volume method incorporating adaptive grid realignment responsive to changes in thermal diffusion characteristics.

---

## RBV-19  (11-candidate listwise instance, v1 dev20 slice)

- **role:** early multi-candidate debugging; the k=11 arm of the k-scaling work
- **discipline:** Cell Biology
- **source DOI:** 10.1038/s41586-024-07098-5
- **literature cutoff:** 2023-05-07 (moved earlier by version search, DECISIONS)

**Question**

> How does interleukin-10 (IL-10) regulate inflammation through lipid metabolism in macrophages, and how can this mechanism be exploited to control inflammation, particularly in the context of IL-10 deficiency?

**Candidates (gold marked)**

- **H0 (GOLD)** IL-10 regulates inflammation by controlling sphingolipid metabolism, specifically through the modulation of very long chain (VLC) ceramides. IL-10 deficiency leads to increased saturated VLC ceramides, which drive inflammation via the transcription factor REL. Restoring MUFA synthesis or targeting ceramide synthesis can mitigate this inflammation.

- **H1** Interleukin-10 (IL-10) regulates inflammation in macrophages through dual modulation of sphingolipid metabolism and monounsaturated fatty acid (MUFA) synthesis via a signaling cascade involving specific post-translational modifications and downstream secondary messengers. Specifically, IL-10 induces phosphorylation of sphingosine kinase (SK) and activation of Stearoyl-CoA Desaturase-2 (SCD2) mediated by the STAT3 pathway, leading to increased production of anti-inflammatory sphingosine-1-phosphate (S1P) and oleic acid. This dual modification enhances plasma membrane fluidity and integrity of the endothelial barrier, attenuating pro-inflammatory ceramide signaling and cytokine production. In IL-10 deficiency, pharmacological activation of SK and SCD2 can restore balance in lipid signaling, providing potential therapeutic avenues to mitigate inflammation-associated diseases.

- **H2** IL-10 regulates inflammation in macrophages by modulating the balance between sphingosine-1-phosphate (S1P) and ceramide through its influence on the phosphorylation state of specific phosphatases, such as PP2A, that deactivate ceramide-producing enzymes like ceramide synthases. This modulation maintains low ceramide levels and supports anti-inflammatory outcomes. In the context of IL-10 deficiency, dysregulation of this phosphorylation balance leads to unchecked ceramide accumulation and pro-inflammatory responses. Therapeutic strategies could involve the targeted activation of these phosphatases through small molecule activators or mimetics of IL-10 activity on their phosphorylation sites, thereby restoring balance and controlling inflammation effectively.

- **H3** IL-10 regulates inflammation in macrophages through modulation of sphingolipid metabolism by altering the activity of specific enzymes. Specifically, IL-10 affects the activity of sphingosine kinase (SK), promoting the production of anti-inflammatory sphingosine-1-phosphate (S1P) over pro-inflammatory ceramide. In the context of IL-10 deficiency, there is reduced SK activity, resulting in diminished S1P levels, elevated ceramide signaling, and enhanced macrophage-driven inflammation with compromised endothelial barrier integrity. Restoration of this metabolic balance by targeting sphingolipid metabolism—potentially through SK activation or ceramide inhibition—may mitigate inflammation due to IL-10 deficiency.

- **H4** IL-10 regulates inflammation in macrophages by modulating sphingolipid metabolism via a dual mechanism involving the enhancement of sphingosine kinase (SK) activity and the regulation of serine/threonine phosphatase 2A (PP2A) activity. Specifically, IL-10 promotes SK activation, which increases sphingosine-1-phosphate (S1P) production, while concurrently enhancing PP2A-mediated deactivation of ceramide synthases through targeted phosphatase modulation. This results in decreased ceramide synthesis and stabilized endothelial barrier integrity, ultimately dampening inflammatory responses. In IL-10 deficient macrophages, impaired SK and PP2A functions result in excessive ceramide accumulation and compromised inflammation control. Therapeutic approaches focusing on the combined use of SK activators and PP2A enhancers could be investigated to restore sphingolipid balance and mitigate inflammation effectively, particularly in diseases characterized by IL-10 deficiency.

- **H5** Modulating Stearoyl-CoA Desaturase-2 (SCD2) activity in macrophages through dietary interventions enriched with specific monounsaturated fatty acid (MUFA) precursors, such as oleic acid and palmitoleic acid, can mitigate inflammatory responses associated with interleukin-10 (IL-10) deficiency. This is achieved by altering lipid mediator profiles and enhancing cell signaling pathways involved in the resolution of inflammation. The dietary intervention will be tested using controlled doses (e.g., 0.5% and 1.5% of total dietary fat content) administered over a period of four weeks in an in vivo mouse model, with adjustments based on preliminary in vitro trials.

- **H6** Targeted modulation of Stearoyl-CoA Desaturase-2 (SCD2) via pharmacological activators or genetic overexpression can compensate for interleukin-10 (IL-10) deficiency in macrophages by enhancing the synthesis of specific anti-inflammatory monounsaturated fatty acids (MUFAs), such as oleic acid, leading to a measurable decrease in pro-inflammatory cytokines.

- **H7** Selective enhancement of Stearoyl-CoA Desaturase-2 (SCD2) activity in macrophages, through a combined approach of CRISPR-mediated activation and dietary supplementation of oleic and palmitoleic acid, can ameliorate inflammatory responses associated with interleukin-10 (IL-10) deficiency. This modulation leads to an optimized balance of anti-inflammatory lipid mediators and signaling pathways that promote inflammation resolution. Validation will involve a tiered approach, starting with primary macrophage cultures and macrophage-like cell lines, followed by in vivo studies using IL-10 knockout mice. Genetic modification will use lentiviral vectors under the control of a macrophage-specific promoter. Dietary interventions will include precise MUFA concentrations at 1% and 2% of total dietary fat, administered via chow over four weeks. Key endpoints will assess the reduction in pro-inflammatory cytokines and histological analysis of inflammatory sites, offering potential therapeutic pathways for IL-10 deficiency-related disorders such as auto-inflammatory diseases.

- **H8** Interleukin-10 (IL-10) enhances macrophage-mediated anti-inflammatory responses by orchestrating a dual metabolic regulation of sphingolipid and monounsaturated fatty acid (MUFA) pathways. Specifically, IL-10 upregulates sphingosine kinases (SphK1 and SphK2) to elevate sphingosine-1-phosphate (S1P) levels, activating S1P receptors (e.g., S1P1, S1P3) which modulate pro-inflammatory cytokine production and promote macrophage polarization toward an anti-inflammatory phenotype. Concurrently, IL-10 stimulates the expression of Stearoyl-CoA Desaturase-2 (SCD2), facilitating the conversion of palmitoyl-CoA into MUFAs, which further modulate inflammatory responses through the enhancement of lipid raft formation and stabilization of membrane integrity. In IL-10-deficient macrophages, the lack of this coordinated regulation leads to impaired S1P signaling, decreased MUFA levels, altered lipid profiles, disrupted endothelial barrier integrity, and heightened pro-inflammatory cytokine secretion. Targeted therapeutic strategies that restore S1P signaling and enhance MUFA synthesis may ameliorate inflammatory responses and improve tissue repair processes.

- **H9** Interleukin-10 (IL-10) regulates lipid metabolism in macrophages by modulating the expression of ceramide synthase and sphingomyelinase, leading to a shift in sphingolipid balance towards anti-inflammatory metabolites, thereby facilitating macrophage apoptosis to resolve inflammation. This effect will be assessed in primary human macrophages treated with varying concentrations of IL-10 (0, 10, 50, and 100 ng/mL) for 24 and 48 hours. The expression levels of ceramide synthase and sphingomyelinase will be quantified using qPCR and Western blot analyses, while apoptosis will be measured using flow cytometry. Additionally, lipid profiles will be determined using mass spectrometry to characterize the changes in sphingolipid metabolism following IL-10 treatment. Appropriate controls, including untreated macrophages and those treated with an IL-10 receptor antagonist, will be included to validate the findings.

- **H10** Interleukin-10 (IL-10) enhances macrophage-mediated anti-inflammatory responses by modulating sphingolipid metabolism, specifically through upregulating the enzyme sphingosine kinases (SphK1 and SphK2) to promote the conversion of ceramide to sphingosine-1-phosphate (S1P) in IL-10 deficient macrophages. This process is hypothesized to restore endothelial barrier integrity and reduce pro-inflammatory cytokine production, as evidenced by detailed in vitro assays using wild-type and IL-10 knock-out macrophage cell lines and in vivo studies in IL-10 deficient mouse models.

