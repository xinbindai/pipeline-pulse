# TruSight Oncology 500 — Reference Guide

> ILLUMINA PROPRIETARY
> Document # 1000000067621 v13 — October 2025
> **For Research Use Only. Not for use in diagnostic procedures.**
> © 2025 Illumina, Inc. All rights reserved.

---

## Table of Contents

- [Overview](#overview) — 1
  - [DNA/RNA Input Recommendations](#dnarna-input-recommendations) — 1
  - [Assess Sample Quality](#assess-sample-quality) — 2
  - [Reference Samples (Optional)](#reference-samples-optional) — 2
  - [DNA Shearing Recommendations](#dna-shearing-recommendations) — 2
  - [Library Prep Automation (Optional)](#library-prep-automation-optional) — 3
  - [Limitations](#limitations) — 3
- [Consumables and Equipment](#consumables-and-equipment) — 4
  - [Kit Contents](#kit-contents) — 4
  - [Consumables and Equipment](#consumables-and-equipment-1) — 10
- [Protocol](#protocol) — 14
  - [Tips and Techniques](#tips-and-techniques) — 14
  - [Library Prep DNA-Only Workflow](#library-prep-dna-only-workflow) — 17
  - [Enrichment DNA-Only Workflow](#enrichment-dna-only-workflow) — 18
  - [Library Prep DNA and RNA Workflow](#library-prep-dna-and-rna-workflow) — 19
  - [Enrichment DNA and RNA Workflow](#enrichment-dna-and-rna-workflow) — 20
  - [Library Prep RNA-Only Workflow](#library-prep-rna-only-workflow) — 21
  - [Enrichment RNA-Only Workflow](#enrichment-rna-only-workflow) — 22
  - [Denature and Anneal RNA](#denature-and-anneal-rna) — 23
  - [Synthesize First Strand cDNA](#synthesize-first-strand-cdna) — 24
  - [Synthesize Second Strand cDNA](#synthesize-second-strand-cdna) — 25
  - [Clean Up cDNA](#clean-up-cdna) — 26
  - [Fragment gDNA](#fragment-gdna) — 28
  - [Perform End Repair and A-Tailing](#perform-end-repair-and-a-tailing) — 30
  - [Ligate Adapters](#ligate-adapters) — 32
  - [Clean Up Ligation](#clean-up-ligation) — 33
  - [Index PCR](#index-pcr) — 35
  - [Set Up First Hybridization](#set-up-first-hybridization) — 37
  - [Capture Targets One](#capture-targets-one) — 40
  - [Set Up Second Hybridization](#set-up-second-hybridization) — 42
  - [Capture Targets Two](#capture-targets-two) — 44
  - [Amplify Enriched Library](#amplify-enriched-library) — 47
  - [Clean Up Amplified Enriched Library](#clean-up-amplified-enriched-library) — 48
  - [Quantify Libraries (Optional)](#quantify-libraries-optional) — 50
  - [Normalize Libraries](#normalize-libraries) — 51
  - [Pool Libraries and Dilute to the Loading Concentration](#pool-libraries-and-dilute-to-the-loading-concentration) — 54
- [Resources and References](#resources-and-references) — 55
  - [Acronyms](#acronyms) — 56
  - [Revision History](#revision-history) — 57

---

## Overview

The TruSight™ Oncology 500 protocol describes an enrichment-based approach to convert DNA and RNA extracted from formalin-fixed paraffin embedded (FFPE) tissue samples into libraries enriched for cancer-related genes that can be sequenced on Illumina® next generation sequencing (NGS) systems. TruSight Oncology 500 enables the preparation of 48 libraries from DNA, RNA, or a combination of DNA and RNA libraries.

The kit is optimized to provide high sensitivity and specificity for low-frequency somatic variants across 523 genes. DNA biomarkers include the following:

- Single nucleotide variants (SNVs)
- Insertions
- Deletions
- Copy number variants (CNVs)
- Multinucleotide variants (MNVs)

TruSight Oncology 500 also detects immunotherapy biomarkers for tumor mutational burden (Tmb) and microsatellite instability (Msi) in DNA. Fusions and splice variants are detected in RNA.

With TruSight Oncology 500 HRD, homologous recombination deficiency (HRD) can be detected. The HRD protocol option is not available in all countries. For more information, contact Illumina Technical Support.

### DNA/RNA Input Recommendations

- The TruSight Oncology 500 assay is optimized to prepare libraries from gDNA that are fragmented to 90–250 bp.
- Use a minimum of 40 ng of DNA/RNA input with the TruSight Oncology 500 Kit assay. Inputs lower than 40 ng can decrease library yield and quality. Quantify the input nucleic acids before beginning the protocol. To obtain sufficient nucleic acid material, isolate nucleic acid from a minimum of 2 mm³ of FFPE tissue.
  - Use a nucleic acid isolation method that produces high recovery yields, minimizes sample consumption, and preserves sample integrity. The QIAGEN AllPrep DNA/RNA FFPE Kit provides a high yield of nucleic acids.
  - Use a fluorometric quantification method that uses DNA/RNA binding dyes such as AccuClear (DNA) or QuantiFluor (RNA).

### Assess Sample Quality

For optimal performance, assess DNA and RNA sample quality before using the TruSight Oncology 500 assay.

- DNA samples can be assessed using the TruSight FFPE QC Kit.
- Use DNA samples that result in a delta Cq value ≤ 5. Samples with a delta Cq > 5 might result in decreased assay performance.
- RNA samples can be assessed using Advanced Analytical Technologies Fragment Analyzer™ (Standard Sensitivity RNA Analysis Kit) or Agilent Technologies 2100 Bioanalyzer (Agilent RNA 6000 Nano Kit).
- Use RNA samples that result in a DV200 value of ≥ 20%. Using samples with a DV200 value < 20% might result in decreased assay performance.

### Reference Samples (Optional)

- Use reference materials with known variant composition, such as Horizon Discovery HD753 (DNA) and Agilent Universal Human Reference RNA. The Agilent Universal Human Reference RNA is an intact RNA sample. Process the sample after the intact RNA procedure described in [Denature and Anneal RNA](#denature-and-anneal-rna).
- Use RNase/DNase-free water as a no template control.
- Processing a reference sample or no template control reduces the total number of test samples that can be processed.

### DNA Shearing Recommendations

The assay is optimized using the Covaris E220evolution, LE220-plus, M220, ME220, ML230, or R230 Focused-ultrasonicator with the parameters provided in [Fragment gDNA](#fragment-gdna). Fragment size distribution can vary due to differences in sample quality and the sonication instrument used for fragmentation.

Use the following guidelines for shearing.

- Avoid excessive bubbles or an air gap in the shearing tube as it can lead to incomplete shearing.
  - Load the gDNA into the Covaris tube slowly to avoid creating bubbles.
  - Centrifuge the LE220-plus, E220evolution, and R230 Covaris tube to collect the sample at the bottom of the tube before shearing.
  - When using the M220, ME220, or ML230 Covaris tube, slowly insert pipette tip into tube until tip is just below the pre-slit septum.
- The recommended settings for the LE220-plus, E220evolution, and R230 instruments are designed for shearing in 130 µl microTUBEs (strip or plate). The recommended settings for the M220, ME220, and ML230 instruments are designed for use with Covaris microTUBE-50 (strip or single tube).
- **[Optional]** Assess fragment size distribution of sheared samples using the Agilent DNA 1000 Kit with the Agilent Bioanalyzer 2100.

### Library Prep Automation (Optional)

The TruSight Oncology 500 Kits are available in automation-compatible formats with additional reagent volume for use with third-party liquid handling robots. Refer to [Consumables and Equipment](#consumables-and-equipment) to determine the appropriate TruSight Oncology 500 Kit to order. Library prep automation methods are available from third-party liquid handling robot vendors. Contact your preferred vendor for more information on TruSight Oncology 500 library prep automation methods.

Automation is not available for TruSight Oncology 500 HRD.

### Limitations

Variant reporting is limited by a manifest file and a block list file. The manifest file excludes regions where the probe set does not effectively capture targets, and the block list file excludes specific positions from variant calling. TSO 500 probes target at least 97% of the Coding DNA Sequence (CDS) of 474 genes. Contact your local Illumina representative for more information if needed.

---

## Consumables and Equipment

The protocol assumes that you have reviewed the contents of this section, confirmed protocol contents, and obtained all required consumables and equipment.

### Kit Contents

Make sure the reagents have been identified in this section before proceeding to the protocol.

| Library prep kit | Catalog # |
| --- | --- |
| TruSight Oncology 500 DNA Kit (48 Sample Library Prep Kit Only) | 20028213 |
| TruSight Oncology 500 DNA/RNA Bundle (24 Sample Library Prep Kit Only) | 20028215 |
| TruSight Oncology 500 DNA Automation Kit (64 Sample Library Prep Kit Only) | 20045504 |
| TruSight Oncology 500 DNA/RNA Automation Kit (32 Sample Library Prep Kit Only) | 20045508 |
| TruSight Oncology 500 HRD (24 Samples) | 20076480 |

| Library prep kit plus NextSeq 500/550 System reagents | Catalog # |
| --- | --- |
| TruSight Oncology 500 DNA NextSeq Kit (48 Sample Library Prep Kit with NextSeq Kit) | 20028214 |
| TruSight Oncology 500 DNA/RNA Bundle NextSeq Kit (24 Sample Library Prep Kit with NextSeq Kit) | 20028216 |
| TruSight Oncology 500 DNA Automation Kit (64 Sample Library Prep Kit with NextSeq Kit) | 20045505 |
| TruSight Oncology 500 DNA Automation Kit (32 Sample Library Prep Kit with NextSeq Kit) | 20045990 |

| Library prep kit plus access to the PierianDx Clinical Genomics Workspace | Catalog # |
| --- | --- |
| TruSight Oncology 500 DNA Kit, plus PierianDx (48 Sample Library Prep Kit with PierianDx) | 20032624 |
| TruSight Oncology 500 DNA/RNA Bundle Kit, plus PierianDx (24 Sample Library Prep Kit with PierianDx) | 20032626 |
| TruSight Oncology 500 DNA Automation Kit (64 Sample Library Prep Kit with PierianDx) | 20045506 |
| TruSight Oncology 500 DNA/RNA Automation Kit (32 Sample Library Prep Kit with PierianDx) | 20045509 |

| Library prep kit plus NextSeq 500/550 System reagents, plus access to the PierianDx Clinical Genomics Workspace | Catalog # |
| --- | --- |
| TruSight Oncology 500 DNA NextSeq Kit, plus PierianDx (48 Sample Library Prep Kit with NextSeq Kit and PierianDx) | 20032625 |
| TruSight Oncology 500 DNA/RNA NextSeq Kit, plus PierianDx (24 Sample Library Prep Kit with NextSeq Kit and PierianDx) | 20032627 |
| TruSight Oncology 500 DNA Automation Kit (64 Sample Library Prep Kit with NextSeq Kit and PierianDx) | 20045507 |
| TruSight Oncology 500 DNA/RNA Automation Kit (32 Sample Library Prep Kit with NextSeq Kit and PierianDx) | 20045991 |

#### Library Prep

**Box 1 — Library Prep – RNA (Pre-Amp), Store at -25°C to -15°C**

DNA/RNA bundle customers receive one box. DNA kit customers do not receive this box.

| Qty 24/48 Manual | Qty 32/64 Automated | Reagent | Description |
| --- | --- | --- | --- |
| 1 | 2 | EPH3 | Elute, Prime, Fragment High Mix 3 |
| 1 | 3 | FSM | First Strand Synthesis Mix |
| 1 | 2 | RVT | Reverse Transcriptase |
| 1 | 2 | SSM | Second Strand Mix |

**Box 2 — Library Prep (Pre-Amp), Store at -25°C to -15°C**

| Qty 24/48 Manual | Qty 32/64 Automated | Reagent | Description |
| --- | --- | --- | --- |
| 2 | 3 | UMI1 | UMI Adapters v1 |

**Box 3 — Library Prep (Pre-Amp), Store at -25°C to -15°C**

| Qty 24/48 Manual | Qty 32/64 Automated | Reagent | Description |
| --- | --- | --- | --- |
| 2 | 3 | ALB1 | Adapter Ligation Buffer 1 |
| 2 | 3 | EPM | Enhanced PCR Mix |
| 2 | 6 | ERA1-A | End Repair A-tailing Enzyme Mix 1 |
| 2 | 5 | ERA1-B | End Repair A-tailing Buffer 1 |
| 2 | 3 | LIG3 | DNA Ligase 3 |
| 2 | 2 | STL | Stop Ligation Buffer |
| 2 | 2 | SUA1 | Short Universal Adapters 1 |

**Box 4 — Library Prep (Pre-Amp), See Storage Temperatures in Table**

| Qty 24/48 Manual | Qty 32/64 Automated | Reagent | Description | Storage Temperature |
| --- | --- | --- | --- | --- |
| 1 | 1 | RSB | Resuspension Buffer | 2°C to 8°C or -25°C to -15°C |
| 2 | 4 | SPB | Sample Purification Beads | 2°C to 8°C |
| 1 | 1 | TEB | TE Buffer | 2°C to 8°C |

**Box 5 — Library Prep - Unique PCR Index Primers (Pre-Amp), Store at -25°C to -15°C**

| Qty 24/48 Manual | Qty 32/64 Automated | Reagent | Description |
| --- | --- | --- | --- |
| 1 | 2 | UP01 | Unique Index Primer 01 |
| 1 | 2 | UP02 | Unique Index Primer 02 |
| 1 | 2 | UP03 | Unique Index Primer 03 |
| 1 | 2 | UP04 | Unique Index Primer 04 |
| 1 | 2 | UP05 | Unique Index Primer 05 |
| 1 | 2 | UP06 | Unique Index Primer 06 |
| 1 | 2 | UP07 | Unique Index Primer 07 |
| 1 | 2 | UP08 | Unique Index Primer 08 |
| 1 | 2 | UP09 | Unique Index Primer 09 |
| 1 | 2 | UP10 | Unique Index Primer 10 |
| 1 | 2 | UP11 | Unique Index Primer 11 |
| 1 | 2 | UP12 | Unique Index Primer 12 |
| 1 | 2 | UP13 | Unique Index Primer 13 |
| 1 | 2 | UP14 | Unique Index Primer 14 |
| 1 | 2 | UP15 | Unique Index Primer 15 |
| 1 | 2 | UP16 | Unique Index Primer 16 |

#### Enrichment

**Box 6 — Enrichment (Post-Amp), See Storage Temperatures in Table**

| Qty 24/48 Manual | Qty 32/64 Automated | Reagent | Description | Storage Temperature |
| --- | --- | --- | --- | --- |
| 2 | 3 | ET2 | Elute Target Buffer 2 | 2°C to 8°C |
| 2 | 2 | HP3 | 2 N NaOH | 2°C to 8°C |
| 1 | 1 | LNB1 | Library Normalization Beads 1 | 2°C to 8°C |
| 2 | 2 | LNS1 | Library Normalization Storage 1 | 2°C to 8°C |
| 2 | 2 | LNW1 | Library Normalization Wash 1 | 2°C to 8°C |
| 1 | 2 | RSB | Resuspension Buffer | 2°C to 8°C or -25°C to -15°C |
| 2 | 4 | SMB | Streptavidin Magnetic Beads | 2°C to 8°C |
| 2 | 3 | SPB | Sample Purification Beads | 2°C to 8°C |
| 2 | 3 | TCB1 | Target Capture Buffer 1 | 2°C to 8°C |

**Box 7 — Enrichment (Post-Amp), Store at -25°C to -15°C**

| Qty 24/48 Manual | Qty 32/64 Automated | Reagent | Description |
| --- | --- | --- | --- |
| 3 | 4 | EE2 | Enrichment Elution 2 |
| 1 | 1 | EEW | Enhanced Enrichment Wash |
| 2 | 3 | EPM | Enhanced PCR Mix |
| 1 | 1 | LNA1 | Library Normalization Additives 1 |
| 2 | 3 | PPC3 | PCR Primer Cocktail 3 |
| 2 | 3 | TCA1 | Target Capture Additives 1 |

**Box 8 — Enrichment (Post-Amp), Store at -25°C to -15°C**

DNA/RNA bundle customers receive one box. DNA kit customers receive two of this box.

| Qty 24 Manual | Qty 48 Manual | Qty 32/64 Automated | Reagent | Description |
| --- | --- | --- | --- | --- |
| 1 | 2 | 3 | OPD2 | Oncology DNA Probe Pool 2 |

**Box 9 — TruSight Oncology 500 Kit Content Set (RNA Only), Store at -25°C to -15°C**

DNA/RNA bundle customers receive one box. DNA kit customers do not receive this box.

| Qty 24/48 Manual | Qty 32/64 Automated | Reagent | Description |
| --- | --- | --- | --- |
| 1 | 1 | OPR1 | Oncology RNA Probes Master Pool |

**Box 10 — TruSight Oncology 500 HRD (Post-Amp), Store at -25°C to -15°C**

| Qty 24 Manual | Reagent | Description |
| --- | --- | --- |
| 1 | OPD3 | Oncology DNA Probe Pool 3 |

**Box 11 — TruSight Oncology 500 HRD Enrichment (Post-Amp), See Storage Temperatures in Table**

| Qty 24 Manual | Reagent | Description | Storage Temperature |
| --- | --- | --- | --- |
| 1 | ET2 | Elute Target Buffer 2 | 2°C to 8°C |
| 1 | HP3 | 2 N NaOH | 2°C to 8°C |
| 1 | LNB1 | Library Normalization Beads 1 | 2°C to 8°C |
| 1 | LNS1 | Library Normalization Storage 1 | 2°C to 8°C |
| 1 | LNW1 | Library Normalization Wash 1 | 2°C to 8°C |
| 1 | RSB | Resuspension Buffer | 2°C to 8°C or -25°C to -15°C |
| 1 | SMB | Streptavidin Magnetic Beads | 2°C to 8°C |
| 1 | SPB | Sample Purification Beads | 2°C to 8°C |
| 1 | TCB1 | Target Capture Buffer 1 | 2°C to 8°C |

**Box 12 — TruSight Oncology 500 HRD Enrichment (Post-Amp), Store at -25°C to -15°C**

| Qty 24 Manual | Reagent | Description |
| --- | --- | --- |
| 2 | EE2 | Enrichment Elution 2 |
| 1 | EEW | Enhanced Enrichment Wash |
| 1 | EPM | Enhanced PCR Mix |
| 1 | LNA1 | Library Normalization Additives 1 |
| 1 | PPC3 | PCR Primer Cocktail 3 |
| 1 | TCA1 | Target Capture Additives |

### Consumables and Equipment

Make sure that you have the required consumables and equipment before starting the protocol. The protocol has been optimized and validated using the items listed. Comparable performance is not guaranteed when using alternate consumables and equipment.

#### Consumables

| Consumable | Supplier |
| --- | --- |
| 1.7 ml microcentrifuge tubes, nuclease-free | General lab supplier |
| 15 ml conical tubes | General lab supplier |
| 50 ml conical tubes | General lab supplier |
| 20 µl aerosol resistant pipette tips | General lab supplier |
| 200 µl aerosol resistant pipette tips | General lab supplier |
| 1 ml aerosol resistant pipette tips | General lab supplier |
| 96-well storage plates, 0.8 ml (MIDI plates) | Fisher Scientific, part # AB-0859 |
| 96-well PCR plates, 0.2 ml (polypropylene) | General lab supplier |
| Ethanol (200 proof for molecular biology) | Sigma-Aldrich, part # E7023 |
| Microseal 'B' adhesive seal (adhesive plate seal) | Bio-Rad, part # MSB-1001 |
| Nuclease-free reagent reservoirs (PVC, disposable trough) | VWR, part # 89094-658 |
| Nuclease-free water | General lab supplier |
| RNase/DNase-free water | General lab supplier |
| [LE220-plus, R230] 8 microTUBE Strip (12 or 120) **or** 96 microTUBE Plate (1 or 10) | Covaris, part # 520053 (12) / 520109 (120); or 520078 (1) / 520069 (10) |
| [E220evo] 8 microTUBE Strip (12 or 120) | Covaris, part # 520053 (12) / 520109 (120) |
| [LE220-plus, E220evo, R230] 8 microTUBE Strip Foil Seal (12) | Covaris, catalog # 520108 |
| [ML230, ME220] microTUBE-50 AFA Fiber H Strip V2 | Covaris, part # 520240 |
| [M220] microTUBE-50 AFA Fiber Screw-Cap (25 or 250) | Covaris, part # 520166 (25) / 520167 (250) |
| [Optional for Quantity Libraries Procedure] 96-well microplate, black, flat, clear bottom | Corning, part # 3904 |
| [Optional] AccuClear Ultra High Sensitivity dsDNA Quantitation Kit with 1 DNA Standard | Biotium, catalog # 31029 |
| [Optional] AllPrep DNA/RNA FFPE Kit | QIAGEN, catalog # 80234 |
| [Optional] Agilent DNA 1000 Kit | Agilent, catalog # 5067–1504 |
| [Optional] Agilent RNA 6000 Nano Kit | Agilent, catalog # 5067–1511 |
| [Optional] DNA Reference Standard | Horizon Diagnostics, catalog # HD753 |
| [Optional] QuantiFluor RNA System | Promega, catalog # E3310 |
| [Optional] Standard Sensitivity RNA Analysis Kit | Agilent, catalog # DNF-471-0500 |
| [Optional] TruSight FFPE QC Kit | Illumina, catalog # 20139070 |
| [Optional] Universal Human Reference RNA | Agilent, catalog # 740000 |

#### Equipment (Pre-Amp)

| Equipment | Supplier |
| --- | --- |
| Thermal Cycler with a heated lid that can be turned off or an adjustable temperature | General lab supplier |
| (2) Heat blocks (Hybex incubator, heating base) | SciGene, catalog # 1057-30-O (115 V) or 1057-30-2 (230 V) |
| (2) MIDI heat block inserts (for use with Hybex) | Illumina, catalog # BD-60-601 |
| Tabletop centrifuge (plate centrifuge) | General lab supplier |
| Microcentrifuge (1.5 ml tubes) | General lab supplier |
| Magnetic stand-96 | Thermo Fisher, catalog # AM10027 |
| Vortexer | General lab supplier |
| Plate shaker (BioShake XP) | Q Instruments, part # 1808-0505 |
| One of the following ultrasonicators: Covaris E220evolution / LE220-plus / R230 / ML230 / ME220 / M220 Focused-ultrasonicator | Covaris, part # 500429 / 500569 / 500620 / 500656 / 500506 / 500295 |
| Required hardware for ultrasonicators (rack/waveguide/holder per model) | Covaris, part # 500430 / 500191 / 500750 / 500661 / 500518 / 500526 / 500414 / 500488 |
| [Optional] 8 microTUBE Strip Prep Station | Covaris, part # 500327 |
| [Optional] microTUBE Prep Station Snap & Screw Cap | Covaris, part # 500330 |
| [Optional] Rack Loading Station | Covaris, part # 500523 |
| [Optional] 2100 Bioanalyzer Desktop System | Agilent, part # G2940CA |
| [Optional] Fragment Analyzer Automated CE System | Agilent, part # M5310AA or M5311AA |

#### Equipment (Post-Amp)

| Equipment | Supplier |
| --- | --- |
| Heat block (Hybex incubator, 96-well plate) | SciGene, catalog # 1057-30-O (115 V) or 1057-30-2 (230 V) |
| MIDI heat block insert (for use with Hybex) | Illumina, catalog # BD-60-601 |
| Tabletop centrifuge (plate centrifuge) | General lab supplier |
| Microcentrifuge (1.5 ml tubes) | General lab supplier |
| Magnetic stand-96 | Thermo Fisher, catalog # AM10027 |
| Vortexer | General lab supplier |
| Plate shaker (BioShake XP) | Q Instruments, part # 1808-0505 |
| Thermal cycler | General lab supplier |
| [Optional] 2100 Bioanalyzer Desktop System | Agilent, part # G2940CA |
| [Optional] Fragment Analyzer Automated CE System | Agilent, part # M5310AA or M5311AA |

---

## Protocol

This section provides step-by-step instructions on how to use the kit to generate sequence-ready libraries from input DNA and RNA. Safe stopping points are indicated at the end of applicable steps.

- Before proceeding, confirm the kit contents and make sure that you have the necessary consumables and equipment.
- The protocol requires separate magnetic stands to reduce cross-contamination; one for pre-amp and one for post-amp procedures.
- Follow the protocol in the order described using the specified parameters. Unless a safe stopping point is specified, move immediately to the next step.

**TruSight Oncology 500 Kit protocol notes:**

- Review the complete sequencing workflow, from sample through analysis, to ensure compatibility of products and experiment parameters.
- Refer to the *NextSeq 500 and 550 Sequencing Systems Denature and Dilute Libraries Guide (document # 15048776)* for guidelines on the number of libraries and possible DNA/RNA combinations per sequencing run.
- Before beginning library preparation, record sample concentration and sample quality information. Save this information for later use during data analysis.
- Stability of the TruSight Oncology 500 Kit has been evaluated and performance demonstrated for up to eight uses of the kit.
- If beads are aspirated into the pipette tips during magnetic separation steps, dispense back to the same well of the plate on the magnetic stand. Then wait until the liquid is clear (~2 minutes).
- When washing beads:
  - Use the appropriate magnetic stand for the plate.
  - Dispense liquid directly onto the bead pellet so that beads on the side of the wells are wetted.
  - Keep the plate on the magnetic stand until the instructions specify to remove it.
  - Do not agitate the plate while on the magnetic stand. Do not disturb the bead pellet.

**TruSight Oncology 500 HRD kit notes:**

- Libraries are split into two reactions for dual enrichment with HRD and TSO 500 probes. For more details, refer to the Plate Layout Example.
- Libraries from the same sample enriched for HRD and TSO 500 share the same index and need to be sequenced together on the same flow cell.

### Tips and Techniques

Review tips and techniques before starting the protocol.

#### Avoiding Cross-Contamination

- Use a unidirectional workflow when moving from pre-amp to post-amp areas.
- To prevent amplification product or probe carryover, avoid returning to the pre-amp area after beginning work in the post-amp area.
- Clean work surfaces and equipment thoroughly before and after the procedure with an RNase/DNase inhibiting cleaner.
- When adding or transferring samples, change tips between each well.
- Handle and open only one index primer at a time. Recap each index tube immediately after use. Extra caps are provided with the kit.
- When adding indexing primers, change tips between each well.
- Remove unused indexing primer tubes from the working area.
- Change gloves if gloves come into contact with indexing primers, samples, or probes.

#### Sealing the Plate

- Always seal the plate with an appropriate plate seal before the following steps in the protocol:
  - Shaking steps
  - Vortexing steps
  - Centrifuge steps
  - Thermal cycling steps
- Apply the adhesive seal to cover the plate and seal with a rubber roller.
- Apply a new seal every time a plate is covered.
- Microseal 'B' adhesive seals are effective at -40°C to 110°C, and suitable for skirted or semiskirted PCR plates. Use Microseal 'B' for shaking, centrifuging, PCR amplification, and long-term storage.
- If droplets start hanging inside a sealed plate, centrifuge at 280 × g for 1 minute.

#### Plate Transfers

- When transferring volumes between plates, transfer the specified volume from each well of a plate to the corresponding well of the other plate.

#### Centrifugation

- When instructed to centrifuge the plate, centrifuge at 280 × g for 1 minute.

#### Handling Reagents

- Tightly recap all reagent tubes immediately after use to limit evaporation and prevent contamination.

#### Handling Beads

- When mixing beads with a pipette:
  - Use a suitable pipette and tip size for the volume being mixed. For example, use a 200 µl for volumes from 20 µl to 200 µl.
  - Adjust the volume setting to ~50–75% of the sample volume.
  - Pipette with a slow, smooth action.
  - Avoid aggressive pipetting, splashing, and introducing bubbles.
  - Position the pipette tip above the pellet and dispense directly into the pellet to release beads from the well or tube.
  - Make sure that the bead pellet is fully in solution. For example, for SMB pellets, the solution should look dark brown and have a homogenous consistency.
- Make sure that beads are at room temperature before use.

### Library Prep DNA-Only Workflow

> RNA and DNA libraries can be prepared simultaneously. Hands-on and total times are approximate and based on eight DNA samples. Times include degassing the Covaris ultrasonicator.

**Figure 1 — TruSight Oncology 500 Kit DNA-Only Workflow (Part 1)** — *Day 1*

| # | Step | Hands-on | Total | Reagents |
| --- | --- | --- | --- | --- |
| 1 | Fragment gDNA | 10 min | 120 min | TEB |
| | *Safe Stopping Point* | | | |
| 2 | Perform End Repair and A-Tailing | 10 min | 70 min | ERA1-A, ERA1-B |
| 3 | Ligate Adapters | 15 min | 50 min | ALB1, UMI1, LIG3, STL |
| 4 | Clean Up Ligation | 40 min | 50 min | SPB, RSB, 80% EtOH |
| 5 | Index PCR | 15 min | 60 min | EPM, UPxx |
| | *Safe Stopping Point* | | | |

### Enrichment DNA-Only Workflow

**Figure 2 — TruSight Oncology 500 Kit DNA-Only Workflow (Part 2)** — *Day 1 (continued) → Day 2*

| # | Step | Hands-on | Total | Reagents |
| --- | --- | --- | --- | --- |
| 1 | Set Up First Hybridization | 15 min | overnight | TCA1, TCB1, OPD2, [DNA-HRD] OPD3 |
| | *Overnight Hybridization → Day 2* | | | |
| 2 | Capture Targets One | 60 min | 100 min | SMB, EEW, EE2, HP3, ET2 |
| 3 | Set Up Second Hybridization | 10 min | 1.5–4 hr | TCA1, TCB1, OPD2, [DNA-HRD] OPD3 |
| 4 | Capture Targets Two | 25 min | 60 min | SMB, RSB, EE2, HP3, ET2 |
| | *Safe Stopping Point* | | | |
| 5 | Amplify Enriched Library | 5 min | 60 min | PPC3, EPM |
| 6 | Clean Up Amplified Enriched Library | 30 min | 40 min | SPB, RSB, 80% EtOH |
| | *Safe Stopping Point* | | | |
| 7 | Quantify Libraries (Optional) | — | — | — |
| 8 | Normalize Libraries | 40 min | 50 min | LNA1, LNB1, LNW1, HP3, LNS1, EE2 |
| | *Safe Stopping Point* | | | |

### Library Prep DNA and RNA Workflow

**Figure 3 — TruSight Oncology 500 Kit DNA and RNA Workflow (Part 1)** — *Day 1*

RNA branch (cDNA):

| # | Step | Hands-on | Total | Reagents |
| --- | --- | --- | --- | --- |
| 1 | Denature and Anneal RNA | 20 min | 40 min | EPH3 |
| 2 | Synthesize First Strand cDNA | 10 min | 50 min | FSM, RVT |
| 3 | Synthesize Second Strand cDNA | 10 min | 30 min | SSM |
| 4 | Clean Up cDNA | 30 min | 40 min | SPB, RSB, 80% EtOH |
| | *Safe Stopping Point* | | | |

DNA branch (sheared DNA):

| # | Step | Hands-on | Total | Reagents |
| --- | --- | --- | --- | --- |
| 1 | Fragment gDNA | 10 min | 120 min | TEB |
| | *Safe Stopping Point* | | | |

Merged branch:

| # | Step | Hands-on | Total | Reagents |
| --- | --- | --- | --- | --- |
| 5 | Perform End Repair and A-Tailing | 10 min | 70 min | ERA1-A, ERA1-B |
| 6 | Ligate Adapters | 15 min | 50 min | ALB1, LIG3, SUA1/UMI, STL |
| 7 | Clean Up Ligation | 40 min | 50 min | SPB, RSB, 80% EtOH |
| 8 | Index PCR | 15 min | 60 min | EPM, UPxx |
| | *Safe Stopping Point* | | | |

### Enrichment DNA and RNA Workflow

**Figure 4 — TruSight Oncology 500 Kit DNA and RNA Workflow (Part 2)** — *Day 1 (continued) → Day 2*

| # | Step | Hands-on | Total | Reagents |
| --- | --- | --- | --- | --- |
| 1 | Set Up First Hybridization | 15 min | overnight | TCA1, TCB1, OPR1, OPD2, [DNA-HRD] OPD3 |
| | *Overnight Hybridization → Day 2* | | | |
| 2 | Capture Targets One | 60 min | 100 min | SMB, EEW, EE2, HP3, ET2 |
| 3 | Set Up Second Hybridization | 10 min | 1.5–4 hr | TCA1, TCB1, OPR1, OPD2, [DNA-HRD] OPD3 |
| 4 | Capture Targets Two | 25 min | 60 min | SMB, RSB, EE2, HP3, ET2 |
| | *Safe Stopping Point* | | | |
| 5 | Amplify Enriched Library | 5 min | 60 min | PPC3, EPM |
| 6 | Clean Up Amplified Enriched Library | 30 min | 40 min | SPB, RSB, 80% EtOH |
| | *Safe Stopping Point* | | | |
| 7 | Quantify Libraries (Optional) | — | — | — |
| 8 | Normalize Libraries | 40 min | 50 min | LNA1, LNB1, LNW1, HP3, LNS1, EE2 |
| | *Safe Stopping Point* | | | |

### Library Prep RNA-Only Workflow

**Figure 5 — TruSight Oncology 500 Kit RNA-Only Workflow (Part 1)** — *Day 1*

| # | Step | Hands-on | Total | Reagents |
| --- | --- | --- | --- | --- |
| 1 | Denature and Anneal RNA | 20 min | 40 min | EPH3 |
| 2 | Synthesize First Strand cDNA | 10 min | 50 min | FSM, RVT |
| 3 | Synthesize Second Strand cDNA | 10 min | 30 min | SSM |
| 4 | Clean Up cDNA | 30 min | 40 min | SPB, RSB, 80% EtOH |
| | *Safe Stopping Point* | | | |
| 5 | Perform End Repair and A-Tailing | 10 min | 70 min | ERA1-A, ERA1-B |
| 6 | Ligate Adapters | 15 min | 50 min | ALB1, LIG3, SUA1, STL |
| 7 | Clean Up Ligation | 40 min | 50 min | SPB, RSB, 80% EtOH |
| 8 | Index PCR | 15 min | 60 min | EPM, UPxx |
| | *Safe Stopping Point* | | | |

### Enrichment RNA-Only Workflow

**Figure 6 — TruSight Oncology 500 Kit RNA-Only Workflow (Part 2)** — *Day 1 (continued) → Day 2*

| # | Step | Hands-on | Total | Reagents |
| --- | --- | --- | --- | --- |
| 1 | Set Up First Hybridization | 15 min | overnight | TCA1, TCB1, OPR1 |
| | *Overnight Hybridization → Day 2* | | | |
| 2 | Capture Targets One | 60 min | 100 min | SMB, EEW, EE2, HP3, ET2 |
| 3 | Set Up Second Hybridization | 10 min | 1.5–4 hr | TCA1, TCB1, OPR1 |
| 4 | Capture Targets Two | 25 min | 60 min | SMB, RSB, EE2, HP3, ET2 |
| | *Safe Stopping Point* | | | |
| 5 | Amplify Enriched Library | 5 min | 60 min | PPC3, EPM |
| 6 | Clean Up Amplified Enriched Library | 30 min | 40 min | SPB, RSB, 80% EtOH |
| | *Safe Stopping Point* | | | |
| 7 | Quantify Libraries (Optional) | — | — | — |
| 8 | Normalize Libraries | 40 min | 50 min | LNA1, LNB1, LNW1, HP3, LNS1, EE2 |
| | *Safe Stopping Point* | | | |

### Denature and Anneal RNA

This process denatures purified RNA and primes the RNA with random hexamers in preparation for cDNA synthesis.

> If working with only purified DNA, proceed directly to [Fragment gDNA](#fragment-gdna).

**Consumables**

- EPH3 (Elute, Prime, Fragment High Mix 3) (red cap)
- FSM (First Strand Synthesis Mix) (red cap)
- RVT (Reverse Transcriptase) (red cap)
- Nuclease-free water
- 96-well PCR plate
- 1.7 ml microcentrifuge tube
- Microseal 'B' adhesive seals

> ⚠️ The following procedures require an RNase- and DNase-free environment. Thoroughly decontaminate the work area with an RNase-inhibiting cleaner. Make sure that RNA-dedicated equipment is used.

**Preparation**

1. Prepare the following consumables:

   | Reagent | Storage | Instructions |
   | --- | --- | --- |
   | EPH3 | -25°C to -15°C | Thaw to room temperature. Vortex to resuspend. Centrifuge briefly. |
   | FSM | -25°C to -15°C | Thaw to room temperature. Vortex to resuspend. Centrifuge briefly. |
   | RVT | -25°C to -15°C | Keep on ice. Centrifuge briefly. |

2. Thaw RNA samples on ice.
3. Qualify and quantify the samples. Refer to [DNA/RNA Input Recommendations](#dnarna-input-recommendations).
4. Dilute a minimum of 40 ng RNA sample in RNase/DNase-free water for a final volume of 8.5 µl.
5. For FFPE or fragmented RNA, save the following **LQ-RNA** program on the thermal cycler:
   - Choose the preheat lid option and set to 100°C
   - Set the reaction volume to 17 µl
   - 65°C for 5 minutes
   - Hold at 4°C
6. For cell line or intact RNA, save the following **HQ-RNA** program on the thermal cycler:
   - Choose the preheat lid option and set to 100°C
   - Set the reaction volume to 17 µl
   - 94°C for 8 minutes
   - Hold at 4°C
7. Label a new 96-well PCR plate **CF** (cDNA Fragments).

**Procedure**

1. Combine the following volumes in a microcentrifuge tube to prepare the FSM+RVT Master Mix (reagent overage included):

   | Master Mix Component | 3 Samples (µl) | 8 Samples (µl) | 16 Samples (µl) | 24 Samples (µl) |
   | --- | --- | --- | --- | --- |
   | FSM | 27 | 72 | 144 | 216 |
   | RVT | 3 | 8 | 16 | 24 |

2. Pipette to mix.
3. Place the FSM+RVT Master Mix on ice until [Synthesize First Strand cDNA](#synthesize-first-strand-cdna).
4. Add 8.5 µl each purified RNA sample to the corresponding well of the CF PCR plate.
5. Add 8.5 µl EPH3 to each well.
6. Apply Microseal 'B' and shake the plate at 1200 rpm for 1 minute.
7. Centrifuge the plate at 280 × g for 1 minute.
8. Place on the preprogrammed thermal cycler and run the LQ-RNA or HQ-RNA program.

### Synthesize First Strand cDNA

This process reverse transcribes the RNA fragments primed with random hexamers into first strand cDNA using reverse transcriptase.

**Consumables**

- FSM+RVT Master Mix
- Microseal 'B' adhesive seals

**Preparation**

1. Save the following **1stSS** program on the thermal cycler with a heated lid:
   - Choose the preheat lid option and set to 100°C
   - Set the reaction volume to 25 µl
   - 25°C for 10 minutes
   - 42°C for 15 minutes
   - 70°C for 15 minutes
   - Hold at 4°C

**Procedure**

1. Remove the CF PCR plate from the thermal cycler.
2. Pipette FSM+RVT Master Mix to mix.
3. Add 8 µl FSM+RVT Master Mix to each well.
4. Pipette five times to mix.
5. Apply Microseal 'B' and shake the plate at 1200 rpm for 1 minute.
6. Centrifuge the plate at 280 × g for 1 minute.
7. Place the plate on the preprogrammed thermal cycler and run the 1stSS program.
8. If also preparing DNA libraries at the same time, begin to fragment gDNA while the 1stSS program is running. Refer to [Fragment gDNA](#fragment-gdna).

### Synthesize Second Strand cDNA

This process removes the RNA template and synthesizes double-stranded cDNA.

**Consumables**

- SSM (Second Strand Mix) (red cap)
- Microseal 'B' adhesive seals

**Preparation**

1. Prepare the following consumables:

   | Reagent | Storage | Instructions |
   | --- | --- | --- |
   | SSM | -25°C to -15°C | Thaw to room temperature. Invert 10 times to mix. Centrifuge briefly. |

2. Save the following **2ndSS** program on the thermal cycler with a heated lid. If the lid temperature cannot be set to 30°C, turn off the preheated lid heat option.
   - Choose the preheat lid option and set to 30°C
   - Set the reaction volume to 50 µl
   - 16°C for 25 minutes
   - Hold at 4°C

**Procedure**

1. Remove the CF PCR plate from the thermal cycler.
2. Add 25 µl SSM to each well.
3. Apply Microseal 'B' and shake the plate at 1200 rpm for 1 minute.
4. Place the plate on the preprogrammed thermal cycler and run the 2ndSS program.

### Clean Up cDNA

This process uses Sample Purification Beads (SPB) to purify the cDNA from unwanted reaction components.

**Consumables**

- SPB (Sample Purification Beads)
- 96-well MIDI plate (2). If stopping before [Fragment gDNA](#fragment-gdna), only one MIDI plate is required.
- [Required only if storing] 96-well PCR plate
- Freshly prepared 80% ethanol (EtOH)
- Microseal 'B' adhesive seals

> **About Reagents:** Aspirate and dispense SPB slowly due to the viscosity of the solution.

**Preparation**

1. Prepare the following consumables:

   | Reagent | Storage | Instructions |
   | --- | --- | --- |
   | RSB | 2°C to 8°C or -25°C to -15°C | Bring to room temperature. If stored at -25°C to -15°C, thaw at room temperature and vortex before use. |
   | SPB | 2°C to 8°C | Bring to room temperature for at least 30 minutes. |

2. Label a new 96-well MIDI plate **BIND1**.
3. Use one of the following plate options:
   - Label a new 96-well MIDI plate **PCF** (Purified cDNA Fragments) to continue with library prep immediately after cleaning up cDNA.
   - Label a new 96-well PCR plate **PCF** (Purified cDNA Fragments) to store the plate after cleaning up cDNA.
4. Prepare fresh 80% EtOH.

**Procedure — Bind**

1. Remove the CF PCR plate from the thermal cycler.
2. Vortex SPB for 1 minute to resuspend the beads.
3. Add 90 µl SPB to each well of the BIND1 MIDI plate.
4. Transfer 50 µl each sample from the CF PCR plate to the corresponding well of the BIND1 MIDI plate.
5. Apply Microseal 'B' and shake at 1800 rpm for 2 minutes.
6. Incubate at room temperature for 5 minutes.

**Procedure — Wash**

1. Place the BIND1 MIDI plate on a magnetic stand for 5 minutes.
2. Remove and discard all supernatant from each well.
3. Wash beads as follows:
   a. Keep on magnetic stand and add 200 µl fresh 80% EtOH to each well.
   b. Wait 30 seconds.
   c. Remove and discard all supernatant from each well.
4. Wash beads a **second** time.
5. Using a 20 µl pipette with fine tips, remove residual supernatant from each well.

**Procedure — Elute**

1. Remove the BIND1 MIDI plate from the magnetic stand.
2. Add 22 µl RSB to each well.
3. Apply Microseal 'B' and shake at 1800 rpm for 2 minutes.
4. Incubate at room temperature for 2 minutes.
5. Place on a magnetic stand for 2 minutes.
6. Transfer 20 µl eluate from each well of the BIND1 MIDI plate to the corresponding well of the PCF plate.
7. Add 30 µl RSB to each well of the PCF plate, and then pipette at least 10 times to mix.
8. Perform one of the following options based on sample type:
   - **[DNA and RNA samples]** Proceed to [Fragment gDNA](#fragment-gdna) or follow instructions at the safe stopping point. Purified cDNA fragments and sheared DNA samples can be stored in the same plate. Make sure to label wells.
   - **[RNA samples only]** If processing a sample from RNA only and not stopping at the safe stopping point, proceed to [Perform End Repair and A-Tailing](#perform-end-repair-and-a-tailing).

> **SAFE STOPPING POINT** — If you are stopping, apply Microseal 'B' to the PCF PCR plate, and briefly centrifuge at 280 × g. Store at -25°C to -15°C for up to 7 days.

### Fragment gDNA

This process fragments gDNA to a 90–250 bp fragment size using the Covaris Focused-ultrasonicator. Covaris shearing generates dsDNA fragments with 3' and 5' overhangs.

**Consumables**

- TEB (TE Buffer)
- [E220evo] Covaris 8 microTUBE Strip with foil seals
- [ML230, ME220] Covaris microTUBE-50 AFA Fiber H Strip V2
- [M220] Covaris microTUBE-50 AFA Fiber Screw-Cap
- [LE220-plus, R230] Covaris 8 microTUBE Strip with foil seals **or** Covaris 96 microTUBE Plate with foil seals
- 96-well MIDI plate
- [Optional] 96-well PCR plate

**Preparation**

1. Prepare the following consumables:

   | Reagent | Storage | Instructions |
   | --- | --- | --- |
   | TEB | 2°C to 8°C | Bring to room temperature. Invert to mix. |

2. Turn on and set up the Covaris instrument according to manufacturer guidelines.
3. Choose one of the following plate options:
   - To continue with library prep immediately after shearing gDNA, label the new 96-well MIDI plate **LP** (Library Preparation).
   - To store sheared gDNA after this step, use a 96-well PCR plate.
   - To process gDNA and cDNA samples simultaneously, continue to use the PCF plate from [Clean Up cDNA](#clean-up-cdna).
4. Thaw gDNA samples at room temperature.
5. Invert to mix.
6. Refer to [DNA/RNA Input Recommendations](#dnarna-input-recommendations) to qualify and quantify samples.
7. Dilute a minimum of 40 ng of each purified DNA sample in TEB for a final volume of 12 µl.

**Procedure**

1. Add 12 µl each diluted, purified gDNA sample into a Covaris 8 microTUBE Strip, 96 microTUBE Plate, or microTUBE-50.
2. Add 40 µl TEB to each sample.
3. Pipette to mix.
4. If you are using a microTUBE Strip or microTUBE Plate, prepare as follows:
   a. Fill any unused wells with 52 µl water. (For a microTUBE Plate, only fill unused wells within the columns that contain samples.)
   b. Pipette to mix.
   c. Seal it with the foil seal.
   d. Centrifuge briefly.
5. Fragment the gDNA using the following settings:

   | Setting | E220evolution | LE220-plus | M220 | ME220 | ML230 | R230 |
   | --- | --- | --- | --- | --- | --- | --- |
   | Peak Incident Power | 175 watts | 450 watts | 50 watts | 50 watts | 350 watts | 450 watts |
   | Duty Factor | 10% | 30% | 20% | 30% | 25% | 25% |
   | Cycles per Burst | 200 | 200 | 1000 | 1000 | 1000 | 600 |
   | Pulse repeats | N/A | N/A | 20 | 20 | 32 | 32 |
   | Pulse delay time | N/A | N/A | 10 s | 10 s | 40 s | 10 s |
   | Shearing Time | 280 s | 250 s | 200 s* | 200 s* | 320 s** | 320 s** |
   | Temperature | 7°C | 7°C | 20°C | 12°C | 12°C | 10°C |
   | Dithering | N/A | N/A | N/A | N/A | 3 mm Y @ 20 mm/s | 1.5 mm Y @ 10 mm/s |
   | Other | Intensifier | N/A | N/A | Wave guide | N/A | N/A |

   \* The shearing time of 200 seconds consists of 10-second bursts with 20 repeats.
   \*\* The shearing time of 320 seconds consists of 10-second bursts with 32 repeats.

6. If you are using a microTUBE Strip or microTUBE Plate, centrifuge briefly to collect droplets.
7. Transfer 50 µl each sheared gDNA sample to the corresponding wells of the LP plate (or PCF plate if processing cDNA simultaneously). Use a 20 µl pipette with fine tips; pipette 20 µl, an additional 20 µl, and then the remaining 10 µl.

> **SAFE STOPPING POINT** — If you are stopping, apply Microseal 'B' to the LP or PCF plate and briefly centrifuge at 280 × g. Store at -25°C to -15°C for up to 7 days.

### Perform End Repair and A-Tailing

This process converts the 5' and 3' overhangs resulting from the fragmentation step into blunt ends using an end repair mix. The 3' to 5' exonuclease activity removes the 3' overhangs and the 5' to 3' polymerase activity fills in the 5' overhangs. The 3' ends are A-tailed during this reaction to prevent them from ligating to each other during the adapter ligation reaction.

**Consumables**

- ERA1-A (End Repair A-tailing Enzyme Mix 1)
- ERA1-B (End Repair A-tailing Buffer 1)
- 1.7 ml microcentrifuge tube
- [Optional] 96-well MIDI plate if storing
- Microseal 'B' adhesive seals

> If a PCR plate was used to store the gDNA or cDNA samples, follow the plate transfer instructions in step 2 of Preparation.

**Preparation**

1. Prepare the following consumables:

   | Reagent | Storage | Instructions |
   | --- | --- | --- |
   | ERA1-A | -25°C to -15°C | Keep on ice. Centrifuge briefly, and then pipette to mix. |
   | ERA1-B | -25°C to -15°C | Thaw to room temperature. Centrifuge briefly, and then pipette to mix. If precipitates are present, warm the tube in your hands, and then pipette to mix until the crystals dissolve. |

2. If the PCF or LP PCR plates were stored at -25°C to -15°C:
   a. Thaw at room temperature.
   b. Centrifuge at 280 × g for 1 minute.
   c. Pipette to mix.
   d. Transfer the entire volume of sheared gDNA and/or cDNA to corresponding wells of a new 96-well MIDI plate.
3. Label the MIDI plate **LP2** (Library Preparation 2).
4. Preheat two Hybex incubators with MIDI heat block inserts: first to 30°C, second to 72°C.
5. Prepare an ice bucket.

**Procedure**

1. Combine the appropriate volumes in a microcentrifuge tube to prepare ERA1 Master Mix (reagent overage included):

   | Master Mix Component | 3 Samples (µl) | 8 Samples (µl) | 16 Samples (µl) | 24 Samples (µl) |
   | --- | --- | --- | --- | --- |
   | ERA1-B | 26 | 69 | 138 | 207 |
   | ERA1-A | 10 | 27 | 54 | 81 |

2. Pipette 10 times to mix, and then place ERA1 Master Mix on ice.
3. Add 10 µl ERA1 Master Mix to each sample in the LP2 MIDI plate.
4. Discard any remaining master mix after use.
5. Apply Microseal 'B' and shake the plate at 1800 rpm for 2 minutes.
6. Incubate at 30°C for 30 minutes.
7. Immediately transfer to another incubator at 72°C and incubate for 20 minutes.
8. Place the plate on ice for 5 minutes.

### Ligate Adapters

This process ligates adapters to the ends of the cDNA and/or gDNA fragments. SUA1 adapters are ligated to cDNA fragments only. UMI1 adapters containing unique molecular indexes are ligated to gDNA fragments only.

**Consumables**

- ALB1 (Adapter Ligation Buffer 1)
- LIG3 (DNA Ligase 3)
- STL (Stop Ligation Buffer)
- SUA1 (Short Universal Adapters 1)
- UMI1 (UMI Adapters v1)
- Microseal 'B' adhesive seals

> **About Reagents:**
> - ALB1 is highly viscous. Pipette slowly to avoid forming bubbles.
> - Make sure to use **UMI1 for DNA libraries only**, and **SUA1 for RNA libraries only**.

**Preparation**

1. Prepare the following consumables:

   | Item | Storage | Instructions |
   | --- | --- | --- |
   | ALB1 | -25°C to -15°C | Thaw to room temperature. Vortex ≥ 10 seconds to resuspend. Centrifuge briefly. |
   | LIG3 | -25°C to -15°C | Keep on ice. Centrifuge briefly, and then pipette to mix. |
   | STL | -25°C to -15°C | Thaw and bring to room temperature. Vortex to resuspend. Centrifuge briefly. |
   | SUA1 | -25°C to -15°C | Thaw to room temperature. Vortex ≥ 10 seconds to resuspend. Centrifuge briefly. |
   | UMI1 | -25°C to -15°C | Thaw to room temperature. Vortex ≥ 10 seconds to resuspend. Centrifuge briefly. |

**Procedure**

1. Add 60 µl ALB1 to each well.
2. Add 5 µl LIG3 to each well.
3. Add the appropriate adapters to each well:
   - For DNA libraries only, add 10 µl UMI1.
   - For RNA libraries only, add 10 µl SUA1.
4. Apply Microseal 'B' and shake the plate at 1800 rpm for 2 minutes.
5. Incubate at room temperature for 30 minutes.
6. Add 5 µl STL to each well.
7. Apply Microseal 'B' and shake the plate at 1800 rpm for 2 minutes.

### Clean Up Ligation

This process uses Sample Purification Beads to purify the gDNA and cDNA fragments and remove unwanted products, such as unligated adapters.

**Consumables**

- RSB (Resuspension Buffer)
- SPB (Sample Purification Beads)
- Freshly prepared 80% ethanol (EtOH)
- Microseal 'B' adhesive seals
- 96-well PCR plate

> **About Reagents:** Aspirate and dispense SPB slowly due to the viscosity of the suspension.

**Preparation**

1. Prepare the following consumables:

   | Reagent | Storage | Instructions |
   | --- | --- | --- |
   | RSB | 2°C to 8°C / -25°C to -15°C | Bring to room temperature. If stored at -25°C to -15°C, thaw to room temperature and vortex before use. |
   | SPB | 2°C to 8°C | Bring to room temperature for at least 30 minutes. Vortex for 1 minute before use. |

2. Label a new 96-well PCR plate **LS** (Library Samples).
3. Prepare fresh 80% EtOH.

**Procedure — Bind**

1. Vortex SPB for 1 minute to resuspend the beads.
2. Add 112 µl SPB to each well of the LP2 MIDI plate.
3. Apply Microseal 'B' and shake at 1800 rpm for 2 minutes.
4. Incubate at room temperature for 5 minutes.

**Procedure — Wash**

1. Place the LP2 MIDI plate on the magnetic stand for 10 minutes.
2. Remove and discard all supernatant from each well.
3. Wash beads as follows:
   a. Keep on magnetic stand and add 200 µl fresh 80% ethanol to each well.
   b. Wait 30 seconds.
   c. Remove and discard all supernatant from each well.
4. Wash beads a **second** time.
5. Using a 20 µl pipette with fine tips, remove residual supernatant from each well.

**Procedure — Elute**

1. Remove from the magnetic stand.
2. Add 27.5 µl RSB to each well.
3. Apply Microseal 'B' and shake the plate at 1800 rpm for 2 minutes.
4. Incubate at room temperature for 2 minutes.
5. Place on a magnetic stand for 2 minutes.
6. Transfer 25 µl of each eluate from the LP2 MIDI plate to the corresponding well of the LS PCR plate.

### Index PCR

In this step, library fragments are amplified using primers that add index sequences for sample multiplexing. The resulting product contains the complete library of fragments flanked by index sequences and adapters required for cluster generation.

**Consumables**

- EPM (Enhanced PCR Mix)
- UPxx (Unique Index Primer)
- Microseal 'B' adhesive seals

> ⚠️ This set of reagents contains potentially hazardous chemicals. Personal injury can occur through inhalation, ingestion, skin contact, and eye contact. Ventilation should be appropriate for handling of hazardous materials in reagents. Wear protective equipment, including eye protection, gloves, and laboratory coat appropriate for risk of exposure. Handle used reagents as chemical waste and discard in accordance with applicable regional, national, and local laws and regulations. For additional environmental, health, and safety information, refer to the SDS at support.illumina.com/sds.html.

**Preparation**

1. Prepare the following consumables:

   | Reagent | Storage | Instructions |
   | --- | --- | --- |
   | EPM | -25°C to -15°C | Thaw on ice. Vortex to resuspend. Centrifuge briefly. |
   | UPxx | -25°C to -15°C | Thaw to room temperature. Vortex to resuspend. Centrifuge briefly. |

2. Assign one UPxx index primer per library (xx = index primer number):
   - When sequencing multiple libraries on a single flow cell, assign a different indexing primer to each sample library.
   - Record sample layout orientation and the indexes for each, and save this information for later use during data analysis.
   - If using HRD enrichment, libraries from the same sample are enriched with different probes but use the same index and must be sequenced on the same flow cell.

   > Refer to the *NextSeq System Denature and Dilute Libraries Guide (document # 15048776)* for guidelines on the number of libraries and possible DNA/RNA combinations per sequencing run. For TSO 500 HRD, also refer to the *NovaSeq 6000 System Denature and Dilute Libraries Guide (document # 1000000106351)*.

3. If you sequence DNA and RNA libraries together, make sure that the two library types contain different index primers. For example, if DNA libraries contain UP01, select a different UPxx for RNA libraries.
4. For low-plex sequencing runs, use at least three libraries containing one of the following combinations to provide sufficient index diversity:
   - [UP01, UP02, UP03]
   - [UP04, UP05, UP06]
   - [UP07, UP08, UP09]
   - [UP10, UP11, UP12]
5. In the post-amp area, save the following **I-PCR** program on the thermal cycler:
   - Choose the preheat lid option and set to 100°C
   - Set the reaction volume to 50 µl
   - 98°C for 30 seconds
   - 15 cycles of: 98°C for 10 seconds, 60°C for 30 seconds, 72°C for 30 seconds
   - 72°C for 5 minutes
   - Hold at 10°C

**Procedure**

1. Add 5 µl indexing primer (UPxx) to each well of the LS PCR plate.
2. Apply a new tube cap to the remaining indexing primer.
3. Add 20 µl EPM to each well.
4. Apply Microseal 'B' and shake the plate at 1200 rpm for 1 minute.
5. Briefly centrifuge at 280 × g.
6. Move to the post-amp area to prevent amplification product carryover.
7. Place on the preprogrammed thermal cycler and run the I-PCR program.
8. Relabel the plate **ALS** (Amplified Library Samples).
9. Centrifuge briefly.

> **SAFE STOPPING POINT** — If you are stopping, apply Microseal 'B' to the ALS plate, and briefly centrifuge at 280 × g. Store at -25°C to -15°C for up to 30 days.

### Set Up First Hybridization

During this process, a pool of oligos specific to 55 genes hybridizes to RNA libraries, and a pool of oligos specific to 523 genes hybridize to DNA libraries prepared in [Index PCR](#index-pcr). If using TruSight Oncology 500 HRD, a pool of oligos specific for HRD hybridizes to DNA libraries. Enrichment of targeted regions requires two hybridization steps. In this first hybridization, oligos hybridize to the DNA and/or RNA libraries overnight (8–24 hours).

**Consumables**

- OPD2 (Oncology Probes DNA 2) (yellow cap)
- OPD3 (Oncology Probes DNA 3) (blue cap)
- OPR1 (Oncology Probes RNA 1) (red cap)
- TCA1 (Target Capture Additives 1)
- TCB1 (Target Capture Buffer 1)
- 96-well PCR plate
- Microseal 'B' adhesive seals

> ⚠️ This set of reagents contains potentially hazardous chemicals. (See full hazardous chemicals warning under [Index PCR](#index-pcr).)

> **About Reagents:**
> - Use OPD2 and OPD3 for DNA libraries only.
> - Use OPD3 for HRD enrichment only.
> - Use OPR1 for RNA libraries only.

**Preparation**

1. Prepare the following consumables:

   | Reagent | Storage | Instructions |
   | --- | --- | --- |
   | [DNA] OPD2 | -25°C to -15°C | Thaw to room temperature. Vortex to resuspend. Centrifuge briefly. |
   | [DNA-HRD] OPD3 | -25°C to -15°C | Thaw to room temperature. Vortex to resuspend. Centrifuge briefly. |
   | [RNA] OPR1 | -25°C to -15°C | Thaw to room temperature. Vortex to resuspend. Centrifuge briefly. |
   | TCA1 | -25°C to -15°C | Thaw to room temperature. Vortex to resuspend. Centrifuge briefly. |
   | TCB1 | 2°C to 8°C | Thaw to room temperature. Centrifuge briefly, then pipette to mix. Inspect for precipitates; if present, warm in hands then pipette to mix until crystals dissolve. |

2. If the ALS PCR plate was stored at -25°C to -15°C: thaw at room temperature, centrifuge at 280 × g for 1 minute, pipette to mix.
3. Label a new 96-well PCR plate **HYB1** (Hybridization 1).
4. Save the following **HYB1** program on the thermal cycler:
   - Choose the preheat lid option and set to 100°C
   - Set the reaction volume to 50 µl
   - 95°C for 10 minutes
   - 85°C for 2.5 minutes
   - 75°C for 2.5 minutes
   - 65°C for 2.5 minutes
   - Hold at 57°C

**Procedure**

1. To hybridize DNA or RNA libraries without HRD enrichment, transfer 20 µl of each library from the ALS PCR plate to the HYB1 PCR plate.
2. To hybridize DNA libraries with HRD enrichment, transfer as follows:
   a. **[DNA]** Transfer 20 µl of each DNA library from the ALS PCR plate to the HYB1 PCR plate.
   b. **[DNA-HRD]** Transfer 20 µl of each DNA library from the ALS PCR plate to a second well of the HYB1 PCR plate for HRD enrichment.
   c. **[RNA]** Transfer 20 µl of each RNA library from the ALS PCR plate to the HYB1 PCR plate.
3. Add 15 µl TCB1 to each well.
4. Add 10 µl TCA1 to each well.
5. Add the appropriate probe (only 1 probe per well — see Plate Layout Example, Figure 7):
   - For DNA libraries without HRD enrichment, add 5 µl OPD2 (yellow cap).
   - For DNA libraries with HRD enrichment, add 5 µl OPD3 (blue cap).
   - For RNA libraries, add 5 µl OPR1 (red cap).
6. Apply Microseal 'B' and shake the plate at 1200 rpm for 2 minutes.
7. Place on the preprogrammed thermal cycler and run the HYB1 program. Hold at 57°C for 8–24 hours to hybridize.

### Capture Targets One

This step uses Streptavidin Magnetic Beads (SMB) to capture probes hybridized to the targeted library DNA regions of interest. Three heated washes using Enhanced Enrichment Wash (EEW) remove nonspecific DNA binding from the beads. The enriched library is then eluted and prepared for a second round of hybridization.

**Consumables**

- EE2 (Enrichment Elution 2)
- EEW (Enhanced Enrichment Wash)
- ET2 (Elute Target Buffer 2)
- HP3 (2 N NaOH)
- SMB (Streptavidin Magnetic Beads)
- 1.7 ml microcentrifuge tube
- 96-well MIDI plate
- 96-well PCR plate
- Microseal 'B' adhesive seals

> ⚠️ This set of reagents contains potentially hazardous chemicals. (See full warning under [Index PCR](#index-pcr).)

> **About Reagents:** Make sure to use SMB and **not** SPB for this procedure.

**Preparation**

1. Prepare the following consumables:

   | Reagent | Storage | Instructions |
   | --- | --- | --- |
   | EE2 | -25°C to -15°C | Thaw to room temperature. Vortex to resuspend. Centrifuge briefly. |
   | EEW | -25°C to -15°C | Thaw to room temperature. Vortex for 1 minute to resuspend. |
   | ET2 | 2°C to 8°C | Bring to room temperature. Vortex to resuspend. Centrifuge briefly. |
   | HP3 | 2°C to 8°C | Bring to room temperature. Vortex to resuspend. Centrifuge briefly. |
   | SMB | 2°C to 8°C | Bring to room temperature for 30 minutes and vortex to resuspend. If precipitate or bead pellet present, reach room temperature, pipette up and down to release the pellet, then vortex to resuspend. |

2. Preheat a Hybex incubator with MIDI heat block insert to 57°C.
3. Label a new 96-well MIDI plate **CAP1** (Capture 1).
4. Label a new 96-well PCR plate **ELU1** (Elution 1).

**Procedure — Bind**

1. Remove the HYB1 PCR plate from the thermal cycler.
2. Vortex SMB for 1 minute to resuspend the beads.
3. Add 150 µl SMB to each well of the CAP1 MIDI plate.
4. Transfer 50 µl of each library from the HYB1 PCR plate to the corresponding well of the CAP1 MIDI plate.
5. Apply Microseal 'B' to the CAP1 MIDI plate and shake at 1800 rpm for 2 minutes.
6. Incubate in a Hybex incubator at 57°C for 25 minutes.
7. Place on a magnetic stand for 2 minutes.
8. While on the magnetic stand, use a pipette to remove and discard the supernatant from each well.

**Procedure — Wash**

1. Wash beads as follows:
   a. Remove the CAP1 MIDI plate from the magnetic stand.
   b. Add 200 µl EEW to each well.
   c. Pipette 10 times to mix.
   d. Apply Microseal 'B' and shake at 1800 rpm for 4 minutes. (If a bead pellet is still present, remove the seal and pipette to mix until all beads are resuspended, then apply a new Microseal 'B'.)
   e. Incubate in a Hybex incubator at 57°C for 5 minutes.
   f. Place on a magnetic stand for 2 minutes.
   g. While on the magnetic stand, remove and discard all supernatant from each well.
2. Wash beads a **second** time.
3. Wash beads a **third** time.
4. Using a 20 µl pipette, remove and discard all supernatant from each well.

**Procedure — Elute**

1. Combine the following volumes in a microcentrifuge tube to prepare the EE2+HP3 Elution Mix (prepare for a minimum of three libraries; discard any remaining after use):

   | Elution Mix Component | 3 Libraries (µl) | 8 Libraries (µl) | 16 Libraries (µl) | 24 Libraries (µl) |
   | --- | --- | --- | --- | --- |
   | EE2 | 95 | 171 | 342 | 513 |
   | HP3 | 5 | 9 | 18 | 27 |

2. Vortex briefly to mix.
3. Remove the CAP1 MIDI plate from the magnetic stand.
4. Slowly add 17 µl EE2+HP3 Elution Mix to each sample pellet.
5. Apply Microseal 'B' and shake at 1800 rpm for 2 minutes.
6. Place on a magnetic stand for 2 minutes.
7. Carefully transfer 15 µl eluate from each well of the CAP1 MIDI plate to the ELU1 PCR plate.
8. Add 5 µl ET2 to each eluate in the ELU1 PCR plate.
9. Apply Microseal 'B' to the ELU1 PCR plate and shake at 1200 rpm for 2 minutes.

### Set Up Second Hybridization

This step binds targeted regions of the enriched DNA and/or RNA libraries with capture probes a second time. The second hybridization ensures high specificity of the captured regions. To ensure optimal enrichment, perform the second hybridization step for 1.5–4 hours.

**Consumables**

- OPD2 (Oncology Probes DNA 2) (yellow cap)
- OPD3 (Oncology Probes DNA 3) (blue cap)
- OPR1 (Oncology Probes RNA 1) (red cap)
- TCA1 (Target Capture Additives 1)
- TCB1 (Target Capture Buffer 1)
- Microseal 'B' adhesive seals

> ⚠️ This set of reagents contains potentially hazardous chemicals. (See full warning under [Index PCR](#index-pcr).)

> **About Reagents:**
> - Use OPD2 and OPD3 for DNA libraries only.
> - Use OPD3 for HRD enrichment only.
> - Use OPR1 for RNA libraries only.

**Preparation**

1. Prepare the following consumables:

   | Reagent | Storage | Instructions |
   | --- | --- | --- |
   | [DNA] OPD2 | -25°C to -15°C | Thaw to room temperature. Vortex to resuspend. Centrifuge briefly. |
   | [DNA-HRD] OPD3 | -25°C to -15°C | Thaw to room temperature. Vortex to resuspend. Centrifuge briefly. |
   | [RNA] OPR1 | -25°C to -15°C | Thaw to room temperature. Vortex to resuspend. Centrifuge briefly. |
   | TCA1 | -25°C to -15°C | Thaw to room temperature. Vortex to resuspend. Centrifuge briefly. |
   | TCB1 | 2°C to 8°C | Thaw to room temperature. Centrifuge briefly, then pipette to mix. If precipitates present, warm in hands then pipette to mix until crystals dissolve. |

2. Save the following **HYB2** program on the thermal cycler:
   - Choose the preheat lid option and set to 100°C
   - Set the reaction volume to 50 µl
   - 95°C for 10 minutes
   - 85°C for 2.5 minutes
   - 75°C for 2.5 minutes
   - 65°C for 2.5 minutes
   - Hold at 57°C

**Procedure**

1. Add 15 µl TCB1 to each well of the ELU1 PCR plate.
2. Add 10 µl TCA1 to each well.
3. Add the appropriate probe to each well (only 1 probe per well — add the same probe used during the first hybridization):
   - For DNA libraries without HRD enrichment, add 5 µl OPD2 (yellow cap).
   - For DNA libraries with HRD enrichment, add 5 µl OPD3 (blue cap).
   - For RNA libraries, add 5 µl OPR1 (red cap).
4. Apply Microseal 'B' and shake the plate at 1200 rpm for 2 minutes.
5. Place on the preprogrammed thermal cycler and run the HYB2 program. Hybridize at 57°C for 1.5–4 hours.

### Capture Targets Two

This step uses Streptavidin Magnetic Beads (SMB) to capture probes hybridized to the targeted regions of interest. Resuspension Buffer (RSB) is used to rinse the captured libraries and remove nonspecific binding from the beads. The enriched library is then eluted and prepared for sequencing.

**Consumables**

- EE2 (Enrichment Elution 2)
- ET2 (Elute Target Buffer 2)
- HP3 (2 N NaOH)
- RSB (Resuspension Buffer)
- SMB (Streptavidin Magnetic Beads)
- 1.7 ml microcentrifuge tube
- [Optional] 15 ml conical tubes
- 96-well MIDI plate
- 96-well PCR plate
- Microseal 'B' adhesive seals

> ⚠️ This set of reagents contains potentially hazardous chemicals. (See full warning under [Index PCR](#index-pcr).)

> **About Reagents:** Make sure to use SMB and **not** SPB for this procedure.

**Preparation**

1. Prepare the following consumables:

   | Reagent | Storage | Instructions |
   | --- | --- | --- |
   | EE2 | -25°C to -15°C | Thaw to room temperature. Vortex to resuspend. Centrifuge briefly. |
   | ET2 | 2°C to 8°C | Bring to room temperature. Vortex to resuspend. Centrifuge briefly. |
   | HP3 | 2°C to 8°C | Bring to room temperature. Vortex to resuspend. Centrifuge briefly. |
   | RSB | 2°C to 8°C or -25°C to -15°C | Bring to room temperature. Vortex before use. If stored at -25°C to -15°C, thaw at room temperature and vortex before use. |
   | SMB | 2°C to 8°C | Bring to room temperature for 30 minutes and vortex to resuspend. If precipitate/bead pellet present, reach room temperature, pipette up and down to release the pellet, then vortex to resuspend. |

2. Preheat a Hybex incubator with MIDI heat block insert to 57°C.
3. Label a new 96-well MIDI plate **CAP2** (Capture 2).
4. Label a new 96-well PCR plate **ELU2** (Elution 2).

**Procedure — Bind**

1. Remove the ELU1 PCR plate from the thermal cycler.
2. Vortex SMB for 1 minute to resuspend the beads.
3. Add 150 µl SMB to each well of the CAP2 MIDI plate.
4. Transfer 50 µl of each library from the ELU1 PCR plate to the corresponding well of the CAP2 MIDI plate.
5. Apply Microseal 'B' to the CAP2 MIDI plate and shake at 1800 rpm for 2 minutes.
6. Incubate in a Hybex incubator at 57°C for 25 minutes.
7. Place on a magnetic stand for 2 minutes.
8. While on the magnetic stand, use a pipette to slowly remove and discard the supernatant from each well.

**Procedure — Wash**

1. Wash as follows:
   a. Remove the CAP2 MIDI plate from the magnetic stand.
   b. Add 200 µl RSB to each well.
   c. Apply Microseal 'B' and shake at 1800 rpm for 4 minutes.
   d. If a bead pellet is still present, remove the seal and pipette to mix until all beads are resuspended, then apply a new Microseal 'B'.
   e. Place on a magnetic stand for 2 minutes.
   f. While on the magnetic stand, carefully remove and discard the supernatant.
2. Using a 20 µl pipette with fine tips, remove any residual supernatant from each well.

**Procedure — Elute**

1. Combine the following volumes in a microcentrifuge tube to prepare the EE2+HP3 Elution Mix (minimum three libraries; discard any remaining after use):

   | Elution Mix Component | 3 Libraries (µl) | 8 Libraries (µl) | 16 Libraries (µl) | 24 Libraries (µl) |
   | --- | --- | --- | --- | --- |
   | EE2 | 95 | 209 | 418 | 627 |
   | HP3 | 5 | 11 | 22 | 33 |

2. Vortex to mix.
3. Remove the CAP2 MIDI plate from the magnetic stand.
4. Carefully add 22 µl EE2+HP3 Elution Mix to each sample pellet.
5. Apply Microseal 'B' and shake the CAP2 MIDI plate at 1800 rpm for 2 minutes.
6. Place on a magnetic stand for 2 minutes.
7. Transfer 20 µl eluate from each well of the CAP2 MIDI plate to the ELU2 PCR plate.
8. Add 5 µl ET2 to each eluate in the ELU2 PCR plate.
9. Apply Microseal 'B' to the ELU2 PCR plate and shake at 1200 rpm for 2 minutes.
10. Centrifuge briefly.

> **SAFE STOPPING POINT** — If you are stopping, store ELU2 plate at -25°C to -15°C for up to 7 days.

### Amplify Enriched Library

This step uses primers to amplify enriched libraries.

**Consumables**

- EPM (Enhanced PCR Mix)
- PPC3 (PCR Primer Cocktail 3)
- Microseal 'B' adhesive seals

> ⚠️ This set of reagents contains potentially hazardous chemicals. (See full warning under [Index PCR](#index-pcr).)

**Preparation**

1. Prepare the following consumables:

   | Reagent | Storage | Instructions |
   | --- | --- | --- |
   | EPM | -25°C to -15°C | Thaw on ice. Vortex to resuspend. Centrifuge briefly. |
   | PPC3 | -25°C to -15°C | Thaw to room temperature. Vortex to resuspend. Centrifuge briefly. |

2. If the ELU2 PCR plate was stored at -25°C to -15°C: thaw at room temperature, centrifuge at 280 × g for 1 minute, pipette to mix.
3. Save the following **EL-PCR** program on the thermal cycler:
   - Choose the preheat lid option and set to 100°C
   - Set the reaction volume to 50 µl
   - 98°C for 30 seconds
   - 18 cycles of: 98°C for 10 seconds, 60°C for 30 seconds, 72°C for 30 seconds
   - 72°C for 5 minutes
   - Hold at 10°C

**Procedure**

1. Add 5 µl PPC3 to each well of the ELU2 PCR plate.
2. Add 20 µl EPM to each well.
3. Apply Microseal 'B' and shake the ELU2 PCR plate at 1200 rpm for 2 minutes.
4. Briefly centrifuge at 280 × g.
5. Place on the preprogrammed thermal cycler and run the EL-PCR program.

### Clean Up Amplified Enriched Library

This step uses Sample Purification Beads (SPB) to purify the enriched library from unwanted reaction components.

**Consumables**

- RSB (Resuspension Buffer)
- SPB (Sample Purification Beads)
- Freshly prepared 80% ethanol (EtOH)
- 96-well MIDI plate
- 96-well PCR plate
- Microseal 'B' adhesive seals

> **About Reagents:** Aspirate and dispense SPB slowly due to the viscosity of the solution.

**Preparation**

1. Prepare the following consumables:

   | Item | Storage | Instructions |
   | --- | --- | --- |
   | RSB | 2°C to 8°C or -25°C to -15°C | Bring to room temperature. Vortex before use. If stored at -25°C to -15°C, thaw at room temperature and vortex before use. |
   | SPB | 2°C to 8°C | Bring to room temperature for 30 minutes. Vortex for 1 minute before using. |

2. Label a new 96-well MIDI plate **BIND2**.
3. Label a new 96-well PCR plate **PL** (Purified Libraries).
4. Prepare fresh 80% EtOH.

**Procedure — Bind**

1. Remove the ELU2 PCR plate from the thermal cycler.
2. Vortex SPB for 1 minute to resuspend the beads.
3. Add 110 µl SPB to each well of the BIND2 MIDI plate.
4. Transfer 50 µl of each library from the ELU2 PCR plate to the corresponding well of the BIND2 MIDI plate.
5. Apply Microseal 'B' to the BIND2 MIDI plate and shake at 1800 rpm for 2 minutes.
6. Incubate at room temperature for 5 minutes.

**Procedure — Wash**

1. Place the BIND2 MIDI plate on magnetic stand for 5 minutes.
2. Remove and discard all supernatant from each well.
3. Wash beads as follows:
   a. Keep on magnetic stand and add 200 µl fresh 80% ethanol to each well.
   b. Wait 30 seconds.
   c. Remove and discard all supernatant from each well.
4. Wash beads a **second** time.
5. Using a 20 µl pipette with fine tips, remove residual supernatant from each well.

**Procedure — Elute**

1. Remove the BIND2 MIDI plate from the magnetic stand.
2. Add 32 µl RSB to each well.
3. Apply Microseal 'B' and shake at 1800 rpm for 2 minutes.
4. Incubate at room temperature for 2 minutes.
5. Place on a magnetic stand for 2 minutes.
6. Transfer 30 µl of each eluate from the BIND2 MIDI plate to the corresponding well of the PL PCR plate.

> **SAFE STOPPING POINT** — If you are stopping, apply Microseal 'B' to the PL plate and briefly centrifuge at 280 × g. Store at -25°C to -15°C for up to 30 days.

### Quantify Libraries (Optional)

Accurately quantify to make sure that there is sufficient library available for clustering on the flow cell. Use a fluorometric quantification method to assess the quantity of enriched libraries before library normalization. Efficient bead-based library normalization requires ≥ 3 ng/µl of each library. The AccuClear Ultra High Sensitivity dsDNA Quantitation Kit has been demonstrated to be effective for quantifying libraries in this protocol.

**[AccuClear] Recommended Guidelines**

1. Combine 6 µl DNA standard with 44 µl RSB to dilute DNA standard to 3 ng/µl.
2. Use RSB as blank.
3. Run the diluted AccuClear DNA standard and blanks in triplicate.
4. Run libraries in single replicates.
5. Determine the average relative fluorescence unit (RFU) for DNA standard and blank.
6. Calculate the Normalized Standard RFU using the appropriate formula.
7. Calculate the Normalized RFU for each library using the appropriate formula.

**Assess Quantity** — Assess the resulting Normalized RFU for each library against the following criteria:

| Fluorescence Measurement | Recommendation |
| --- | --- |
| ≤ Average Blank RFU | Repeat library preparation and enrichment if purified DNA sample meets quantity and quality specifications. |
| > Average Blank RFU (and) < Normalized Standard RFU | Proceed to [Normalize Libraries](#normalize-libraries). Using libraries with RFU below the Normalized Standard RFU might not yield adequate sequencing results to confidently call variants that can be present in the sample. |
| ≥ Normalized Standard RFU | Proceed to [Normalize Libraries](#normalize-libraries). |

### Normalize Libraries

This process uses bead-based normalization to normalize the quantity of each library to ensure uniform library representation in the pooled libraries.

**Consumables**

- EE2 (Enrichment Elution 2)
- HP3 (2 N NaOH)
- LNA1 (Library Normalization Additives 1)
- LNB1 (Library Normalization Beads 1)
- LNS1 (Library Normalization Storage 1)
- LNW1 (Library Normalization Wash 1)
- 1.7 ml microcentrifuge tubes (2)
- 96-well MIDI plate
- 96-well PCR plate
- Microseal 'B' adhesive seals

> ⚠️ This set of reagents contains potentially hazardous chemicals. (See full warning under [Index PCR](#index-pcr).)

> **About Reagents:** Aspirate and dispense LNB1 slowly due to the viscosity of the suspension.

**Preparation**

1. Prepare the following consumables:

   | Reagent | Storage | Instructions |
   | --- | --- | --- |
   | EE2 | -25°C to -15°C | Thaw to room temperature. Vortex to resuspend. Centrifuge briefly. |
   | LNA1 | -25°C to -15°C | Thaw to room temperature. Vortex to resuspend. Centrifuge briefly. |
   | HP3 | 2°C to 8°C | Bring to room temperature. Vortex to resuspend. Centrifuge briefly. |
   | LNB1 | 2°C to 8°C | Bring to room temperature for at least 30 minutes. Pipette LNB1 pellet up and down to resuspend. |
   | LNS1 | 2°C to 8°C | Bring to room temperature. Vortex to resuspend. Centrifuge briefly. |
   | LNW1 | 2°C to 8°C | Bring to room temperature. Vortex to resuspend. |

2. If the PL plate was stored at -25°C to -15°C: thaw at room temperature, pipette to mix, centrifuge at 280 × g for 1 minute.
3. Label a new 96-well MIDI plate **BBN** (Bead-Based Normalization).
4. Label a new 96-well PCR plate **NL** (Normalized Libraries).

**Procedure**

1. Pulse vortex LNB1 tube for 1 minute at maximum speed. Invert to make sure all beads are resuspended. If a bead pellet remains, repeat vortexing.
2. Using a 1000 µl pipette set at 800 µl, pipette LNB1 up and down 10 times to mix.
   > It is critical to completely resuspend the bead pellet at the bottom of the tube. Resuspension is essential to achieve consistent cluster density.
3. Combine the following reagents in a new microcentrifuge tube to create LNA1+LNB1 Master Mix (reagent overage included):

   | Master Mix Component | 3 Libraries (µl) | 8 Libraries (µl) | 16 Libraries (µl) | 24 Libraries (µl) |
   | --- | --- | --- | --- | --- |
   | LNA1 | 132 | 352 | 704 | 1056 |
   | LNB1 | 24 | 64 | 128 | 192 |

4. Vortex to mix.
5. Combine the following reagents in a new microcentrifuge tube to create a fresh EE2+HP3 Elution Mix:

   | Elution Mix Component | 3 Libraries (µl) | 8 Libraries (µl) | 16 Libraries (µl) | 24 Libraries (µl) |
   | --- | --- | --- | --- | --- |
   | EE2 | 114 | 304 | 608 | 912 |
   | HP3 | 6 | 16 | 32 | 48 |

6. Vortex to mix.

**Procedure — Bind**

1. Vortex LNA1+LNB1 Master Mix.
2. Add 45 µl LNA1+LNB1 Master Mix to each well of the BBN MIDI plate.
3. Add 20 µl of each library from the PL PCR plate to the corresponding well of the BBN MIDI plate.
4. Apply Microseal 'B' to the BBN MIDI plate and shake at 1800 rpm for 30 minutes.
5. Place the BBN MIDI plate on a magnetic stand for 2 minutes.
6. Remove and discard all supernatant from each well.

**Procedure — Wash**

1. Wash beads as follows:
   a. Remove the BBN MIDI plate from the magnetic stand.
   b. Add 45 µl LNW1 to each well.
   c. Apply Microseal 'B' and shake at 1800 rpm for 5 minutes.
   d. Place on a magnetic stand for 2 minutes.
   e. Remove and discard all supernatant from each well.
2. Wash a **second** time.
3. Using a 20 µl pipette with fine tips, remove any residual supernatant from each well.

**Procedure — Elute**

1. Remove the BBN MIDI plate from the magnetic stand.
2. Vortex EE2+HP3 Elution Mix and then centrifuge briefly.
3. Carefully add 32 µl EE2+HP3 Elution Mix to each well.
4. Apply Microseal 'B' and shake at 1800 rpm for 2 minutes.
5. Place BBN MIDI plate on a magnetic stand for 2 minutes.
6. Transfer 30 µl of each eluate from the BBN MIDI plate to the corresponding well of the NL PCR plate.
7. Add 30 µl LNS1 to each library in the NL PCR plate.
8. Pipette up and down to mix.

> **SAFE STOPPING POINT** — If you are stopping, apply Microseal 'B' to the NL plate and briefly centrifuge at 280 × g. Store at -25°C to -15°C for up to 30 days.

### Pool Libraries and Dilute to the Loading Concentration

1. See the denature and dilute libraries guide for the sequencing system to pool, denature, and dilute libraries to the loading concentration.

---

## Resources and References

The TruSight Oncology 500 Kit support pages on the Illumina support site provide additional resources, including training, compatible products, and other considerations. Always check support pages for the latest versions.

| Resource | Description |
| --- | --- |
| TruSight Oncology 500 Checklist (document # 1000000067619) | Provides a checklist of steps for the experienced user. |
| Illumina Adapter Sequences (document # 1000000002694) | Provides adapter sequences for Illumina library prep kits. |

### Acronyms

| Acronym | Definition |
| --- | --- |
| 1stSS | 1st Strand Synthesis |
| 2ndSS | 2nd Strand Synthesis |
| ALS | Amplified Library Samples |
| BBN | Bead Based Normalization |
| CAP1 | Capture 1 |
| CAP2 | Capture 2 |
| cDNA | Complementary DNA |
| CF | cDNA Fragments |
| ELU1 | Elution 1 |
| ELU2 | Elution 2 |
| gDNA | Genomic DNA |
| HQ-RNA | High-quality RNA |
| HRD | Homologous Recombination Deficiency |
| HYB1 | Hybridization 1 |
| HYB2 | Hybridization 2 |
| LP | Library Preparation |
| LP2 | Library Preparation 2 |
| LQ-RNA | Low-quality RNA |
| LS | Library Samples |
| NL | Normalized Libraries |
| PCF | Purified cDNA Fragments |
| PL | Purified Libraries |

### Revision History

| Document | Date | Description of Change |
| --- | --- | --- |
| v13 | October 2025 | Added a section on the limitations of variant reporting. |
| v12 | May 2025 | Added information for the TruSight FFPE QC Kit. Added Covaris ML230, M220, and R230 instrument information. Updated the note for the potentially hazardous chemicals in the reagents. |
| v11 | January 2023 | Updated information in Overview section to specify HRD protocol option is not available in all countries. |
| v10 | July 2022 | Added information on OPD3 probes and the related HRD enrichment workflow. |
| v09 | October 2021 | Corrections to consumable acronyms and appendix numbering. |
| v08 | June 2021 | Removed overview section. |
| v07 | April 2021 | Removed duplicate step information in procedure sections. Thermal cycle split into two steps in Denature and Anneal RNA section. Removed resuspend reagent from Clean Up cDNA consumables. Changed the second midi plate to optional in Clean Up cDNA. Added a note to write LP on the new plate in Fragment gDNA section. Moved caution to the beginning of the procedure. Added clarification not to thaw both DNA and RNA unless using both. Changed Elute section verbiage in Capture Targets One to match targets two. Added missing Table row in Clean Up Amplified Enriched Library. Split Formula step into two steps in Quantify Libraries. Added clarification that the microplate is optional in the consumables section. Included a requirement to have a thermal cycler with a heated lid and adjustable temperature. |
| v06 | September 2020 | Added information on Library Prep Automation kits and automation formats for use with third party liquid handling robots. |
| v05 | April 2020 | Updated LNB1 mixing instructions to ensure resuspension. Fixed shake speed in Clean Up cDNA section from 1500 to 1800 rpm. |
| v04 | November 2019 | Noted that guidelines regarding the number of libraries and possible DNA/RNA combinations per sequencing run are in the NextSeq System Denature and Dilute Libraries Guide (document # 15048776). |
| v03 | October 2019 | Added an RNA only workflow. Added gene amplifications as a biomarker. Removed RNA maximum input guidance and dilution recommendations. Noted 40 ng minimum DNA/RNA input. Removed sample concentration amount in TEB for fragmenting gDNA. Added kits with PierianDx. Added Covaris consumables/equipment and ME220 settings. Added cross-contamination/sealing tips. Noted library/combination guidelines on support pages. Added LNB1 mixing instructions and bind-step vortex. Added AccuClear quantitation guidelines. |
| v02 | June 2019 | Updated the list of acronyms. |
| v01 | March 2019 | Added steps to the protocol for sample libraries derived from RNA. Added kit contents, consumables, and equipment for RNA. |
| v00 | December 2018 | Initial release. |

---

*Illumina, Inc. · 5200 Illumina Way · San Diego, California 92122 U.S.A. · +1.800.809.ILMN (4566) · +1.858.202.4566 (outside North America) · techsupport@illumina.com · www.illumina.com*

*For Research Use Only. Not for use in diagnostic procedures. © 2025 Illumina, Inc. All rights reserved. Document # 1000000067621 v13*
