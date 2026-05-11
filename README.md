# Jahanshah Qaraqoyunlu (Hakîkî) Manuscript Witness Census

A codicological inventory of manuscript witnesses to the *Dīvān* of **Jahanshah Qaraqoyunlu** (d. 872 AH / 1467 CE; pen name **Ḥaqīqī** / **Hakîkî**), Qaraqoyunlu ruler-poet.

**Authors**:

- **Koen van der Heide**, Independent Scholar (ORCID [0009-0008-9855-3848](https://orcid.org/0009-0008-9855-3848))
- **Negar Kazemipourleilabadi**, Ludwig-Maximilians-Universität München, Department of Art History (ORCID [0009-0008-2289-7492](https://orcid.org/0009-0008-2289-7492))

**License**: [CC BY 4.0](LICENSE)
**DOI**: *(minted on first Zenodo release; will be added here)*

## Coverage

14 audited entries: 9 verified Jahānshāh witnesses + 2 attribution-disputed candidates + 1 lost-attested + 2 rejected for audit:

- **9 verified witnesses**: 5 on the TEIS Yesevi roster (one likely partial, one with disputed institutional attribution); 1 institutional fragment (Ankara MK A 5252); 3 Alevi shrine witnesses in the *Ocak* tradition (Diyarbakır Ulutürk *cönk*, Anatolian; Ilkhchi Kırklar Ocağı pirs' archive, Iranian Azerbaijani; Ilkhchi *cem cönks*, Iranian Azerbaijani).
- **2 candidates flagged as probably non-Cihānşāh** (Konya Hacı Bektaş BY0000010729; Nuruosmaniye 04281, probably Yusuf Hakîkî or other homonym).
- **1 lost-attested-only** (Diyarbakır YE per Cunbur 1999).
- **2 rejected** (the "Baku-Doerfer" hypothesis traced to Rahimov 1986 published edition; the AMEA 2021 acquisition shown to be a surrogate of Süleymaniye Fatih 3808).

> *Inclusion criterion for `rejected` entries*: only candidates cited in published scholarship or acquired as Cihānşāh witnesses by a major institution are audit-preserved in the register. Routine search false-positives (name-collision noise, namesake disambiguations, body-text catalogue matches) are recorded in the per-session JSONs under [`data/searches/`](data/searches/), not in the register itself. The two current rejected entries both address one underlying question (whether Baku holds an independent Cihānşāh codex) and answer it in the negative with independent evidence. Each rejected entry carries a `rejection_type` sub-classification (`derivative_surrogate` or `non_manuscript_misidentification`); see [`data/spec.md`](data/spec.md) for definitions.

## Repository contents

- [`data/`](data/): deposit artifacts
  - `witness_register.json`: 14-entry register with verification status per witness
  - `search_keys.json`: 5-family search-key matrix (modern Latin / 19th-c. Orientalist / Soviet-Cyrillic / Arabic-script / catalogue-context) covering Persian, Turkish, Ottoman Turkish, and Azerbaijani Turkic forms
  - `spec.md`: witness register JSON schema (v1) reference
  - `searches/`: per-scope search session JSONs across 8 v1.0.0 scopes (UK/European, Turkey/Anatolia, Iran/Caucasus, mecmûʿa-Nesîmî adjacency, tezkire, auctions, catalogue/scribe/edition backchain, South Asian/global), plus v1.0.1 follow-on probe, crosscheck, and gap-disposition artifacts (27 files total at v1.0.1)
  - `tezkire_extracts/`: verbatim *tezkire* entries on Hakîkî (5 entries: TEIS Yesevi, Macit/Bilig 2000, Yınanç MEB, Konukcu TDV, Câmî Münşeʾāt)
  - `research_log/`: archived source extracts and methodological assessments (5 files: Macit 2000 full extract, Minorsky 1954 codicology recheck, Nuruosmaniye 04281 decoration extract, Sohrabiabad-Akın 2019 witness list, TEIS Yesevi bibliography 2026-05-02)
  - `README.md`: methodology overview and file conventions

## Methodology

The census combines aggregator sweeps, *tezkire* extraction, *mecmûʿa* adjacency mining, auction-house archives, scribe-name search, printed-catalogue OCR backchain, and modern-editor backchain. See [`data/README.md`](data/README.md) for the full methodology details.

The Alevi shrine corpus (Diyarbakır Ulutürk *cönk* in the Anatolian *Ocak* tradition; Ilkhchi pirs' archive and Ilkhchi *cem cönks* in the Iranian Azerbaijani *Ocak* tradition) preserves eleven *ghazals* not present in the institutional editions examined, plus a complete divan codex in the Ilkhchi Kırklar Ocağı pirs' archive that has not yet been examined by scholars outside the shrine community.

## Citation

If you use this dataset, please cite:

> van der Heide, K. & Kazemipourleilabadi, N. (2026). *Cihānşāh Qaraqoyunlu (Hakîkî) Manuscript Witness Census* (Version 1.0.1) [Data set]. Zenodo. *DOI to be added once the Zenodo release mints it.*

A `CITATION.cff` file is included; GitHub renders a "Cite this repository" widget from it once indexed.

## Status

Research-grade corpus, not a critical edition. Several entries carry open access requirements (ILL-procurement of base editions; field correspondence for Diyarbakır Ulutürk and Ilkhchi pirs' archive). See [`data/README.md`](data/README.md) for methodology details.

## Author Contributions

Following the [CRediT (Contributor Roles Taxonomy)](https://credit.niso.org/):

- **Negar Kazemipourleilabadi**: Conceptualization (research-question origination); Investigation (background information on Persian / Turkish / Ottoman-Turkish / Azerbaijani sources); Writing, Review & Editing (native-speaker proofreading of multilingual orthography across Persian, Turkish, Ottoman Turkish, and Azerbaijani).
- **Koen van der Heide**: Conceptualization (joint); Methodology; Data Curation; Investigation (corpus building, search orchestration, source verification); Software (analysis pipeline); Writing, Original Draft; Visualization.
