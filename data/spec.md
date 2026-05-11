# Witness Register Schema (v1)

This document describes the structure of `witness_register.json`, the primary artifact of this deposit. It is organised as a **core schema** (the v1 design fields, present in every witness entry) plus **observed extension fields** (per-witness fields added during execution to record codex-specific evidence). The register is hand-curated, not generated, so a future witness may carry additional extension fields not documented here.

## Schema version

`schema_version: 1`. Generated 2026-05-02.

## Top-level structure

```json
{
  "schema_version": 1,
  "generated": "2026-05-02",
  "purpose": "...",
  "rejection_inclusion_criterion": "...",
  "witnesses": [ ... ],
  "stats": { ... },
  "teis_yesevi_roster": [ ... ]
}
```

The `teis_yesevi_roster` block lists the five witnesses on the TEIS Yesevi roster (a subset of the entries in `witnesses[]`).

## Witness entry: core fields

Every witness entry carries the listed core fields with `null` for unknown values. Beyond the core, observed extension fields (e.g. `verification_caveat`, `dimensions_mm`, `script`, `columns`) appear only in entries where they are relevant and are omitted entirely otherwise.

### Identity fields

| Field | Type | Description |
|---|---|---|
| `witness_id` | string | Stable internal identifier. Lowercase snake_case. Usually `<collection-slug>_<shelfmark-slug>`. |
| `shelfmark` | string | Catalogue shelfmark in its native form. |
| `collection` | string | Holding institution and sub-collection. |
| `city`, `country` | string | Location of holding institution. |

### Codicology fields (all optional)

| Field | Type | Description |
|---|---|---|
| `date_ah`, `date_ce` | string \| null | Hijri and CE year of copying, or range. |
| `scribe` | string \| null | Scribe name as transcribed from the colophon. |
| `languages` | array of string \| null | Languages present in the codex. |
| `folios` | integer \| null | Total folio count. |
| `dimensions_cm` | string \| null | Dimensions in centimeters, e.g. `"23 × 16"`. Field present in 14/14 entries; non-null in 1/14 (BL Or 9493 only); Nuruosmaniye uses `dimensions_mm`; other entries are null. |
| `dimensions_mm` | string \| null | Optional alternate dimensions in millimeters when the source quotes mm-precision values (1/14 entries). |
| `lines_per_page` | string or integer \| null | Line count per page. May be a range. |
| `contents` | string \| null | Free-text contents description. |

### Status (3 fields)

| Field | Type | Description |
|---|---|---|
| `completeness` | string \| null | One of: `complete`, `fragment`, `fragment_or_excerpt`, `unknown`. May be `null` for rejected non-witness entries that were never substantively evaluated. |
| `fragment_type` | string \| null | If `completeness` is `fragment` or `fragment_or_excerpt`, kind of fragment. |
| `digital_surrogate` | string \| null | URL to digital surrogate, if extant. |

### Decoration object

The `decoration` object records paper, illumination, and binding observations. Core fields are present in every entry; extension fields appear when relevant evidence was recovered.

```json
{
  "paper_description": "string or null",
  "illumination": "string or null",
  "binding": "string or null",
  "data_source": "string or null",
  "notes": "string or null",
  "confidence": "very_high | high | moderate | low | very_low | unknown"
}
```

`data_source` records who described the decoration (firsthand examiner, catalogue entry, photograph, IIIF surrogate). `confidence` follows the project-wide qualitative scale and is present in 14/14 entries.

**Observed extension fields inside `decoration`** (added when a single confidence value would conflate distinct sub-judgments):

- `seals_marks` (string): waqf seals, ownership marks, library stamps. Recorded for 2 witnesses where seals are codicologically diagnostic.
- `decoration_data_confidence` (qualitative): confidence in the decoration evidence itself, separate from the next field.
- `cihansah_attribution_confidence` (qualitative): confidence that the codex is a Cihānşāh witness (relevant when an Ottoman-period homonym ambiguity exists).

### Provenance and verification (5 fields)

| Field | Type | Description |
|---|---|---|
| `scholarly_attestation` | array of object | Each object has `author`, `year`, `ref`, and optionally `saw_firsthand` (boolean or string `"likely"`; omitted for attestation objects where firsthand status is not assessed, e.g. authoritative encyclopedia entries). May carry an optional `remark` field for verbatim cross-collation evidence. |
| `discovery_source` | string | URL or printed-catalogue reference that originally surfaced the witness. |
| `verification_status` | string | See enum below. |
| `verification_caveat` | string | Optional free-text qualification of `verified` or candidate status (4/14 entries). |
| `notes` | string \| null | Free-text notes on dating, scribal hand, or context. |

## Witness entry: observed extension fields

Beyond the core schema, individual entries carry codex-specific evidence fields. The most common:

- `candidate_provenance` (4/14): origin of a candidate witness traced from a tezkire or printed-catalogue lead.
- `columns` (3/14): page columnation, when relevant.
- `script` (3/14): script style (e.g. *nastaʿlīq*, *nasta'liq*, *taʿlīq*).
- `rejection_reason` (2/14): explicit reasoning for `rejected` entries (audit-preserved).
- `rejection_type` (2/14): sub-classification of rejected entries. Values: `derivative_surrogate` (the entry is a copy/microfilm of an existing witness and would double-count it if included) and `non_manuscript_misidentification` (the entry was never an independent manuscript, e.g. a printed edition once treated as if it were an MS witness).

Single-occurrence extension fields document evidence specific to one witness (e.g. `alemdari_findings`, `disambiguation_caveat`, `recovery_method`, `decoration_data_value_for_or_9493_question`). These are not part of the v1 schema; they are research notes that future versions may either lift to first-class fields or move into `notes`.

## verification_status enum

The terminal-state enum has six values:

| Value | Count | Meaning |
|---|---|---|
| `verified` | 8 | Primary-source-attested or independently confirmed witness. |
| `verified_with_attribution_caveat` | 1 | Witness existence and primary attribution are confirmed, but a caveat remains (institutional/holding attribution disagreement OR unresolved attribution to Cihānşāh). |
| `candidate_probably_non_cihansah` | 1 | Manuscript confirmed to exist; attribution to Cihānşāh weakly supported. |
| `candidate_probably_yusuf_hakiki_or_other_homonym` | 1 | Manuscript confirmed to exist; attribution probably points to a homonym (Yusuf Hakîkî or another *Hakîkî* poet). |
| `lost_witness_attested_only` | 1 | Witness attested in scholarly literature but no longer extant or no longer locatable. |
| `rejected` | 2 | Investigated and dismissed; audit-preserved with explicit `rejection_reason` plus a `rejection_type` sub-classification (`derivative_surrogate` or `non_manuscript_misidentification`; see extension fields above). **Inclusion criterion**: only candidates cited in published scholarship or acquired as Cihānşāh witnesses by a major institution appear here. Routine search false-positives live in per-session JSONs under `data/searches/`. |

`pending` is a transient state allowed during execution. At publication, no entry carries `pending`.

## Stats block

The `stats` object aggregates counts (`by_completeness` and `by_country` count active non-rejected entries; `by_verification` includes all 14):

```json
{
  "total_witnesses_active": 12,
  "total_entries_including_rejected_and_lost": 14,
  "by_verification": { "<status>": <count>, ... },
  "by_completeness": { "<value>": <count>, ... },
  "by_country": { "<ISO-or-name>": <count>, ... }
}
```

The two top-line counts: `total_witnesses_active = 12` excludes only the 2 `rejected` entries (the 1 `lost_witness_attested_only` entry is counted among the active 12). `total_entries_including_rejected_and_lost = 14` is the audit-preserved total.

## Verification rule

Every entry in `witness_register.json` carries an evidence trail that resolves independently. Resolvable references typically appear in `discovery_source`; where a witness was first surfaced through means other than a single URL/printed reference, the resolvable evidence may live in `scholarly_attestation`, `rejection_reason`, or `decoration.data_source` instead. Candidate bibliography is treated as candidate, not attested, until verified by an independently resolvable source URL or printed-catalogue reference. The `rejected` entries are kept in the register, not silently deleted, to preserve the audit trail of which proposed witnesses were investigated and dismissed. Inclusion in the register requires that the candidate has been cited in published scholarship or acquired by a major institution as a Cihānşāh witness; routine search false-positives are documented in the per-session JSONs under `data/searches/` and not promoted to the register. The two current rejected entries both address one underlying question, namely whether Baku holds an independent Cihānşāh codex, and both answer it in the negative with independent evidence.

## Example entry: bl_or_9493 (abridged)

```json
{
  "witness_id": "bl_or_9493",
  "shelfmark": "Or 9493",
  "collection": "British Library, Oriental Manuscripts",
  "city": "London",
  "country": "UK",
  "date_ah": "Shawwāl 893",
  "date_ce": "September 1488",
  "scribe": "Qanbar-ʿAlī b. Khusraw al-Iṣfahānī",
  "languages": ["Persian", "Turkish"],
  "folios": 85,
  "dimensions_cm": "23 × 16",
  "writing_surface_cm": "16 × 11",
  "lines_per_page": "10-11",
  "contents": "105 Persian ghazals + 1 mustazad (ff. 1b-42a); 87 Turkish ghazals (ff. 45b-80a); 32 Turkish quatrains (ff. 80b-85a); 2 added poems by 'Farrukh' on f. 85b (one Persian, one Turkish)",
  "completeness": "complete",
  "fragment_type": null,
  "digital_surrogate": null,
  "decoration": {
    "paper_description": null,
    "illumination": null,
    "binding": null,
    "data_source": null,
    "confidence": "unknown",
    "notes": "Minorsky 1954 reports state of preservation 'perfect' and calls it a 'handsome little manuscript'. No further decoration data in any open-access scholarly source."
  },
  "scholarly_attestation": [
    {"author": "Minorsky", "year": 1954, "ref": "BSOAS 16/2: 271-297", "saw_firsthand": true},
    {"author": "Macit", "year": 2000, "ref": "Bilig 13: 9-17", "saw_firsthand": true},
    {"author": "Düzgün, D.", "year": "n.d.", "ref": "academia.edu/43146022 (self-deposited preprint)", "saw_firsthand": false},
    {"author": "Alemdârî", "year": "2001 / 1379 SH", "ref": "...", "saw_firsthand": true}
  ],
  "discovery_source": "https://www.fihrist.org.uk/catalog/manuscript_6481",
  "verification_status": "verified",
  "fihrist_decoration_facet": "Decoration: No, per sweep 2026-05-02. Caveat: Fihrist's coarse boolean tag does not distinguish illumination from decorated paper.",
  "notes": "Posthumous copy: 21 years after Jahānshāh's death."
}
```

The `writing_surface_cm` and `fihrist_decoration_facet` fields illustrate single-occurrence extension fields that future schema versions may lift to first-class.
