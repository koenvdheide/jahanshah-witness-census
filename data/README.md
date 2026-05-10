# Ḥaqīqī / Hakîkî (Jahānshāh Qaraqoyunlu) Manuscript Witness Census: Data

This directory contains the deposit artifacts behind the witness census of **Jahānshāh Qaraqoyunlu** (r. 1438-67), pen name **Ḥaqīqī** (Persian and Azerbaijani Turkic).

**Authors**:

- **Koen van der Heide**, Independent Scholar (ORCID [0009-0008-9855-3848](https://orcid.org/0009-0008-9855-3848))
- **Negar Kazemipourleilabadi**, Ludwig-Maximilians-Universität München, Department of Art History (ORCID [0009-0008-2289-7492](https://orcid.org/0009-0008-2289-7492))

Author contributions follow the [CRediT taxonomy](https://credit.niso.org/) and are stated in the parent `README.md`.

## Scope

Witness census of manuscripts containing poetry by Jahānshāh Qaraqoyunlu. Source types in scope:

- **Witness, candidate, and audit entries** (counted in the 14-entry register; 12 non-rejected): full divans, fragmentary copies, *mecmuʿa* / *jung* / *cönk* anthologies containing ≥1 Hakîkî *ghazal*, candidates with disputed attribution, and audit-preserved rejected leads.
- **Ancillary scholarly sources** (consulted but not register entries): 5 *tezkire* entries (in `tezkire_extracts/`) plus 5 research-log extracts (in `research_log/`), totalling 10 reference extracts on Hakîkî with verbatim sample verses where retrieved.

For each witness, decoration / paper / illumination data is captured when accessible and recorded as descriptive per-witness data in the dossiers.

## Findings summary

| Category | Count | Witnesses |
|:---------|:-----:|:----------|
| TEIS Yesevi roster | 5 | BL Or 9493 · Matenadaran 965 · Süleymaniye Fatih 3808 · Ankara DTCF / Atatürk Üniv. İsmail Saib I/2221 · Tehran University 8198 |
| Institutional fragment | 1 | Ankara MK A 5252 |
| Alevi shrine, Ocak tradition (verified) | 3 | Diyarbakır Ulutürk *cönk* (Anatolian) · Ilkhchi Kırklar Ocağı pirs' archive (Iranian Azerbaijani) · Ilkhchi *cem cönks* (Iranian Azerbaijani) |
| Disputed candidate | 2 | Konya Hacı Bektaş BY0000010729 · Nuruosmaniye 04281 |
| Lost but attested | 1 | Diyarbakır Yazma Eserler Kütüphanesi (former) |
| Rejected (audit) | 2 | "Baku-Doerfer" · AMEA 2021 acquisition |

**Two structural findings stand out**:

1. **By reported contents (no direct stemmatic collation has been performed), the witnesses fall into a fuller form with *masnavīs* (Group A) and a narrower form without (Group B).** Matenadaran 965, Tehran University 8198, and Süleymaniye Fatih 3808 are reported as Group A (Mat 965 and Süleymaniye Fatih 3808 contents counts remain unresolved at the codex level pending direct collation); BL Or 9493 is Group B. Jāmī's contemporary *Münşe'āt* (which describes Cihānşāh's lifetime divan as containing both *ghazals* and *masnavīs*) supports the *masnavī*-bearing form as conservative for that layer. Caveat: Mat 965 vs Süleymaniye Fatih 3808 contents identity is unresolved at the codex level (Anatolia DB listings suspected boilerplate).
2. **The Alevi shrine tradition extends the textual corpus.** The Alevi shrine tradition (Anatolian and Iranian Azerbaijani *Ocak* lineages) has preserved **eleven *ghazals*** not present in the institutional editions examined (eight from the Diyarbakır Ulutürk *cönk*, three from the Ilkhchi *cem cönks*) plus a complete divan codex in the Ilkhchi Kırklar Ocağı pirs' archive that has not yet been examined by scholars outside the shrine community.

## File conventions

| File | Purpose |
| --- | --- |
| `README.md` | This file |
| `spec.md` | Witness register JSON schema (v1) reference: field-by-field documentation with example entry. |
| `search_keys.json` | 5-family search-key matrix (modern Latin / 19th-c. Orientalist / Soviet-Cyrillic / Arabic-script / catalogue-context) covering Persian, Turkish, Ottoman Turkish, and Azerbaijani Turkic forms |
| `witness_register.json` | Merged deduplicated witness list. Authoritative artifact. |
| `searches/search_YYYY-MM-DD_<scope>.json` | Per-search-session JSON output (8 files) |
| `tezkire_extracts/<tezkire_name>_haqiqi.md` | Tezkire and reference extracts on Hakîkî (5 files) |
| `research_log/` | Archived source extracts and methodological assessments (5 files) |

## Verification rule

Every entry in `witness_register.json` cites a source URL or printed-catalogue reference that resolves independently. The two `rejected` entries (Baku-Doerfer, AMEA 2021) are audit-preserved with explicit rejection reasoning.

## Methodology

Witness census combining:

- **Aggregator sweeps**: Fihrist (UK), Qalamos (German-speaking world), Al-Furqan (Islamic-mss union gateway), YEK portal (Turkey), NLAI / Majlis / DENA-FANKHA (Iran), Matenadaran (Armenia), Islamisation of Anatolia DB, Salar Jung / Khuda Bakhsh / Rampur Raza (South Asia), HMML / WorldCat (global)
- **Tezkire extraction and target logging**: Devletshah, Sām Mīrzā, ʿAlī Şīr Navāʾī, Sādīqī Bēg, ʿĀşıq Çelebi, Hidayat *Riyāḍ al-ʿĀrifīn*, plus the modern TEIS Yesevi authoritative entry
- **Mecmûʿa adjacency mining**: Nesîmî catalogue entries searched for misattributed or co-located Hakîkî *ghazals*, a heuristic that empirically grounded the Hurufi-cluster transmission diagnostic via Ankara MK A 5252
- **Auction-house archives**: Christie's, Sotheby's, Bonhams (returned zero direct Jahānshāh witnesses; the corpus is 100% institutional / private archive)
- **Scribe-name search**: Qanbar-ʿAlī b. Khusraw al-Iṣfahānī (BL Or 9493 colophon)
- **Printed-catalogue OCR backchain**: Rieu, Blochet, Pertsch, Karatay, Monzavī, Storey, Browne, Gibb (via Google Books / Internet Archive / HathiTrust)
- **Modern editor backchain**: Hüseyinzade, Rahimov, Recebov, Demirci, Değirmençay, Macit, Alemdârî, Ownuk-Hangeldi (manuscript bases checked; several resolved, several inferred or unrecovered)
