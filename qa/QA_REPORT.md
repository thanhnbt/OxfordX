# QA report — Unit 1–3 preview

Historical v1 report. Current deliverable and validation: [QA v2 report](QA_V2_REPORT.md).

Date: 2026-10-01 (Asia/Bangkok).

Deliverable: root `index.html`, 377,106 bytes, self-contained. SHA-256: `6fbcbda9cd44b9e11d3732a3efed0589c18187a6e795a0bccad913edd2c5d3cd`.

## Executed validation

| Gate | Result | Evidence |
|---|---|---|
| Data, source vocabulary, image provenance, embedded bytes, JS syntax | PASS — 271 assertions, 0 failures | [data-results.json](data-results.json); `python scripts/validate_review.py` |
| Browser interaction, storage, quiz, responsive layout, print, speech fallback, HTTP hosting | PASS — 108 assertions, 0 failures | [browser-results.json](browser-results.json); `node qa/browser-check.cjs` |
| Skill frontmatter and structural validation | PASS — “Skill is valid!” | skill-creator `scripts/quick_validate.py od4_esl_learning_designer_skill` |
| Book facts and image meaning | PASS for included adaptations/crops | [SOURCE_AUDIT.md](SOURCE_AUDIT.md); [contact sheet](book-image-contact-sheet.jpg); per-asset hashes in [visual-review.json](visual-review.json) |
| Desktop/mobile appearance | PASS by visual inspection | [desktop home](desktop-home.png), [Unit 1 words](desktop-unit1-words.png), [Unit 2 words](desktop-unit2-words.png), [mobile home](mobile-home.png), [mobile Unit 3](mobile-unit3-words.png) |
| Print | PASS — six A4 pages, two per unit; all pages inspected | [print-review.pdf](print-review.pdf) |

Automated checks assert observable behavior and source invariants. Counts are not a measure of pedagogical effectiveness.

## Behavior exercised

- Three-unit navigation and each learning section, including single-unit review.
- Source lists: 33 key words, 12 context words and 18 word-study forms. Source grammar is anchored in the matching PDF page.
- Unit 1 and 3 each have 11 dedicated source pictures. Unit 2 has six supporting source pictures and five explicitly marked authored diagrams; no claim of 11 exact book pictures.
- Map label hiding, picture-card hiding and answer-free alt text; reveal opens one card.
- Grammar retry/correct feedback; all unit quizzes and balanced nine-question mixed review; wrong-answer review and scoring.
- Notes, practice flags, writing and self-checks persist after reload. Storage-disabled mode reports visit-only saving instead of claiming successful persistence.
- Audio contract with a deterministic mock: exact plural target `stars`, English voice, chosen speaking rate. Missing API and non-English-only voice scenarios give a readable fallback; unrelated-language voices are not substituted.
- No horizontal overflow at 1440, 768 and 390 pixels for the tested sections. Narrow navigation tabs deliberately scroll inside their own area.
- The one-file site loads all images over local HTTP without an asset folder; notes persist on that HTTP origin.
- Print hides interactive controls and includes all three units/33 cards. No JavaScript runtime errors in the main browser run.

## Fixes found during QA

1. Earth-core crop included an adjacent line of exercise text; cropped again and visually verified.
2. Mixed-quiz hash navigation could regenerate the question set after opening; made the hash handler preserve an existing mixed quiz and reran checks.
3. Print reading headings could be orphaned at the bottom of vocabulary pages; moved the reading section to the next page for each unit.
4. Ambiguous/abstract Unit 2 visuals needed retrieval context; added meaning cues that do not disclose the target word.
5. Header art contained part of a clipped book title; cropped to an image detail.

Some initial test failures were test-selector/mock problems, not product defects: hidden print phonetics counted in recall assertions, the Audio button's accessible name, duplicate navigation/CTA selectors, and incomplete mock speech constructors. Corrected the tests and reran against the final artifact.

## Adult rubric self-review

| Dimension | Score / 2 | Observation |
|---|---|---|
| Big Question & purpose | 2 | Source Big Question above each unit's activities. |
| Concept map | 2 | Relationship labels, comparison scaffold, four stages and hidden-label recall. |
| Vocabulary | 2 | Concept groups, original pictures/support diagrams, pronunciation and sentences. |
| Thinking | 2 | Visualization, compare/contrast and author's-purpose prompts; a detail is requested for support. |
| Grammar | 2 | Meaning, pattern, example, guided checks and learner-authored sentence. |
| ESL accessibility | 2 | Short English, optional Vietnamese, frames; provisional adult judgment. |
| Output | 2 | Speaking, writing or paper drawing with explanation. |
| Recall | 2 | Hidden picture/map prompts and quizzes plus productive output. |
| Visual design | 1 | Clear responsive layout; original vocabulary source pictures remain small/soft. |
| Source fidelity | 2 | Scope/strand references, exact core lists, adaptation and visual provenance disclosed. |

Total: **19/20, provisional adult self-review**. This is not an independent pedagogical evaluation or evidence of learning gains.

## Not yet verified

- **NOT RUN:** learner observation, actual session duration, and independent behavioral evaluation of the skill. The current artifact exercises one-unit and multi-unit flows and the real missing-dedicated-image case in Unit 2, but is not a blind forward-test of the skill.
- **NOT RUN:** audible TTS pronunciation/quality on the learner's device, cross-browser Safari/Firefox testing, and offline speech support. The test uses headless Edge and mocks the speech contract; it does not certify recorded pronunciation.
- **NOT RUN / not required by this input:** damaged/scanned-PDF OCR scenarios. This PDF's teacher text is extractable; student picture regions were rendered/cropped.
- **NOT PROVIDED:** class diary; the page intentionally reports book scope instead of invented actual sessions.
- **NOT PERFORMED:** GitHub commit, push or Pages deployment. No repository URL/remote was supplied. Single-file static hosting was tested locally.

## Build again

1. `python scripts/build_review.py`
2. `python scripts/validate_review.py`
3. `npm install --prefix tmp/qa playwright --ignore-scripts --no-audit --no-fund` if the QA dependency is absent.
4. `node qa/browser-check.cjs` (the script uses the installed Windows Edge executable).

The build keeps authored data/crops separate in the workspace, embeds them into `index.html`, and invalidates visual-review status if an asset's hash changes. Future content or image changes require the affected source/visual review again.
