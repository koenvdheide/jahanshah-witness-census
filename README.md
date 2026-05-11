# Jahanshah Qaraqoyunlu Manuscript Witness Census

A codicological inventory of manuscript witnesses to the *Dīvān* of Jahanshah Qaraqoyunlu (d. 872 AH / 1467 CE; pen name *Ḥaqīqī* / *Hakîkî*), Qaraqoyunlu ruler-poet.

Authors:

- Koen van der Heide, Independent Scholar (ORCID [0009-0008-9855-3848](https://orcid.org/0009-0008-9855-3848))
- Negar Kazemipourleilabadi, Ludwig-Maximilians-Universität München, Department of Art History (ORCID [0009-0008-2289-7492](https://orcid.org/0009-0008-2289-7492))

License: [CC BY 4.0](LICENSE)

## Coverage

14 audited entries of manuscripts containing poetry by Jahānshāh Qaraqoyunlu, plus 10 ancillary reference extracts. Verification breakdown: 9 verified Jahānshāh witnesses + 2 attribution-disputed candidates + 1 lost-attested + 2 rejected.

Source types in scope:

- Witness, candidate, and audit entries (counted in the 14-entry register; 12 non-rejected): full divans, fragmentary copies, *mecmuʿa* / *jung* / *cönk* anthologies containing ≥1 Hakîkî *ghazal*, candidates with disputed attribution, and audit-preserved rejected leads.
- Ancillary scholarly sources (consulted but not register entries): 5 *tezkire* entries (in [`data/tezkire_extracts/`](data/tezkire_extracts/)) plus 5 research-log extracts (in [`data/research_log/`](data/research_log/)), totalling 10 reference extracts on Hakîkî with verbatim sample verses where retrieved.

For each witness, decoration / paper / illumination data is captured when accessible and recorded as descriptive per-witness data in the dossiers.

| Category | Count | Witnesses |
|:---------|:-----:|:----------|
| TEIS Yesevi roster (verified) | 5 | BL Or 9493 · Matenadaran 965 · Süleymaniye Fatih 3808 · Ankara DTCF / Atatürk Üniv. İsmail Saib I/2221 · Tehran University 8198 |
| Institutional fragment (verified) | 1 | Ankara MK A 5252 |
| Alevi shrine, Ocak tradition (verified) | 3 | Diyarbakır Ulutürk *cönk* (Anatolian) · Ilkhchi Kırklar Ocağı pirs' archive (Iranian Azerbaijani) · Ilkhchi *cem cönks* (Iranian Azerbaijani) |
| Disputed candidate | 2 | catalogue-ambiguous Hakîkî attributions; see [`data/witness_register.json`](data/witness_register.json) for entries |
| Lost but attested | 1 | Diyarbakır Yazma Eserler Kütüphanesi (former, per Cunbur 1999) |
| Rejected (audit) | 2 | "Baku-Doerfer" hypothesis (traced to Rahimov 1986 published edition); AMEA 2021 acquisition (surrogate of Süleymaniye Fatih 3808) |

> *Inclusion criterion for `rejected` entries*: only candidates cited in published scholarship or acquired as Cihānşāh witnesses by a major institution are audit-preserved in the register. Routine search false-positives (name-collision noise, namesake disambiguations, body-text catalogue matches) are recorded in the per-session JSONs under [`data/searches/`](data/searches/), not in the register itself. The two current rejected entries both address one underlying question (whether Baku holds an independent Cihānşāh codex) and answer it in the negative with independent evidence. Each rejected entry carries a `rejection_type` sub-classification (`derivative_surrogate` or `non_manuscript_misidentification`); see [`data/spec.md`](data/spec.md) for definitions.

## Findings

Two structural findings stand out:

1. By reported contents, the witnesses fall into two groups: a fuller form with *masnavīs* (Group A) and a narrower form without (Group B). No direct stemmatic collation has been performed. Matenadaran 965, Tehran University 8198, and Süleymaniye Fatih 3808 are reported as Group A (Mat 965 and Süleymaniye Fatih 3808 contents counts remain unresolved at the codex level pending direct collation); BL Or 9493 is Group B. Jāmī's contemporary *Münşe'āt* (which describes Cihānşāh's lifetime divan as containing both *ghazals* and *masnavīs*) supports the *masnavī*-bearing form as conservative for that layer. Caveat: Mat 965 vs Süleymaniye Fatih 3808 contents identity is unresolved at the codex level (Anatolia DB listings suspected boilerplate).
2. The Alevi shrine tradition extends the textual corpus. The Anatolian and Iranian Azerbaijani *Ocak* lineages have preserved eleven *ghazals* not present in the institutional editions examined (eight from the Diyarbakır Ulutürk *cönk*, three from the Ilkhchi *cem cönks*) plus a complete divan codex in the Ilkhchi Kırklar Ocağı pirs' archive that has not yet been examined by scholars outside the shrine community.

## Repository contents

- [`data/`](data/): deposit artifacts
  - `witness_register.json`: 14-entry register with verification status per witness
  - `search_keys.json`: 5-family search-key matrix (modern Latin / 19th-c. Orientalist / Soviet-Cyrillic / Arabic-script / catalogue-context) covering Persian, Turkish, Ottoman Turkish, and Azerbaijani Turkic forms, plus a `script_families` block of 9 additional script traditions (Russian Cyrillic modern, Az Latin/Cyrillic, Georgian Mkhedruli, Uzbek Latin/Cyrillic, Tajik Cyrillic, Devanagari, Urdu nastaʿliq) added in v1.0.1
  - `spec.md`: witness register JSON schema (v1) reference
  - `searches/`: per-scope search session JSONs across 8 v1.0.0 scopes (UK/European, Turkey/Anatolia, Iran/Caucasus, mecmûʿa-Nesîmî adjacency, tezkire, auctions, catalogue/scribe/edition backchain, South Asian/global), plus v1.0.1 follow-on probe, crosscheck, and gap-disposition artifacts (27 files total at v1.0.1)
  - `tezkire_extracts/`: verbatim *tezkire* entries on Hakîkî (5 entries: TEIS Yesevi, Macit/Bilig 2000, Yınanç MEB, Konukcu TDV, Câmî Münşeʾāt)
  - `research_log/`: archived source extracts and methodological assessments (5 files: Macit 2000 full extract, Minorsky 1954 codicology recheck, Nuruosmaniye 04281 decoration extract, Sohrabiabad-Akın 2019 witness list, TEIS Yesevi bibliography 2026-05-02)

## Methodology

Witness census combining:

- Aggregator sweeps: Fihrist (UK), Qalamos (German-speaking world), Al-Furqan (Islamic-mss union gateway), YEK portal (Turkey), NLAI / Majlis / DENA-FANKHA (Iran), Matenadaran (Armenia), Islamisation of Anatolia DB, Salar Jung / Khuda Bakhsh / Rampur Raza (South Asia), HMML / WorldCat (global)
- Tezkire extraction and target logging: Devletshah, Sām Mīrzā, ʿAlī Şīr Navāʾī, Sādīqī Bēg, ʿĀşıq Çelebi, Hidayat *Riyāḍ al-ʿĀrifīn*, plus the modern TEIS Yesevi authoritative entry
- Mecmûʿa adjacency mining: Nesîmî catalogue entries searched for misattributed or co-located Hakîkî *ghazals*; a heuristic that empirically grounded the Hurufi-cluster transmission diagnostic via Ankara MK A 5252
- Auction-house archives: Christie's, Sotheby's, Bonhams (zero direct Jahānshāh witnesses surfaced; the corpus is 100% institutional / private archive)
- Scribe-name search: Qanbar-ʿAlī b. Khusraw al-Iṣfahānī (BL Or 9493 colophon)
- Printed-catalogue OCR backchain: Rieu, Blochet, Pertsch, Karatay, Monzavī, Storey, Browne, Gibb (via Google Books / Internet Archive / HathiTrust)
- Modern editor backchain: Hüseyinzade, Rahimov, Recebov, Demirci, Değirmençay, Macit, Alemdârî, Ownuk-Hangeldi (manuscript bases checked; several resolved, several inferred or unrecovered)

The Alevi shrine corpus (Diyarbakır Ulutürk *cönk* in the Anatolian *Ocak* tradition; Ilkhchi pirs' archive and Ilkhchi *cem cönks* in the Iranian Azerbaijani *Ocak* tradition) preserves eleven *ghazals* not present in the institutional editions examined, plus a complete divan codex in the Ilkhchi Kırklar Ocağı pirs' archive that has not yet been examined by scholars outside the shrine community.

## Citation

If you use this dataset, please cite:

> van der Heide, K. & Kazemipourleilabadi, N. (2026). *Jahanshah Qaraqoyunlu Manuscript Witness Census* (Version 1.0.1) [Data set]. Zenodo. *DOI to be added once the Zenodo release mints it.*

A `CITATION.cff` file is included; GitHub renders a "Cite this repository" widget from it once indexed.

## Status

Research-grade corpus, not a critical edition. Several entries carry open access requirements (ILL-procurement of base editions; field correspondence for Diyarbakır Ulutürk and Ilkhchi pirs' archive).

## Author Contributions

Following the [CRediT (Contributor Roles Taxonomy)](https://credit.niso.org/):

- Negar Kazemipourleilabadi: Conceptualization (research-question origination); Investigation (background information on Persian / Turkish / Ottoman-Turkish / Azerbaijani sources); Writing, Review & Editing (native-speaker proofreading of multilingual orthography across Persian, Turkish, Ottoman Turkish, and Azerbaijani).
- Koen van der Heide: Conceptualization (joint); Methodology; Data Curation; Investigation (corpus building, search orchestration, source verification); Software (analysis pipeline); Writing, Original Draft; Visualization.
