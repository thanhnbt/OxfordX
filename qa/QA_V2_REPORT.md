# QA v2 — Unit 1–3 bilingual review

Date: 2026-10-01. Deliverable: root `index.html`, 546,495 bytes, standalone; images, lesson data, styles and scripts are embedded.

SHA-256: `caee6391029b005b7eba0f553a3278b24829b8d6847a1992bcb832e15fcb17c2`.

## Executed gates

| Gate | Result | Evidence |
|---|---|---|
| Source vocabulary, image provenance, embedded assets, JavaScript syntax | 276 passed, 0 failed | [data-results.json](data-results.json), `python scripts/validate_review.py` |
| Browser regression: navigation, quizzes, notes, audio fallback, responsive layout, HTTP hosting | 108 passed, 0 failed | [browser-results.json](browser-results.json), `node qa/browser-check.cjs` |
| Bilingual UI, language persistence, Grammar Lab, builder translations/audio, saved writing, feedback, mobile and actual print output | 71 passed, 0 failed | [v2-results.json](v2-results.json), `node qa/v2-check.cjs` |
| ESL skill structure | Valid | skill-creator `quick_validate.py` |

## Content and visual review

The core 33 vocabulary words and source references remain intact. All 36 visual assets have hash-bound review records. Vocabulary retains IPA, sound-out guidance, speech and source-book pictures. Vietnamese explanations and finite sentence-builder translations were reviewed as authored ESL scaffolding.

Grammar is emphasized through three stages: understand, build, try. Unit 1 teaches prediction with will + base verb; Unit 2 pairs present simple in the if clause with will + base verb in the result; Unit 3 restricts its infinitive pattern to the selected verbs. Examples, translations and feedback explain these distinctions without presenting open writing as automatically graded.

Desktop home, all three grammar units, vocabulary and mobile screenshots were inspected. Responsive interaction checks cover widths 390, 768 and 1024 pixels. Color roles also have written labels. Mobile navigation and the active activity tab remain reachable.

The six-page A4 print output includes bilingual grammar in hybrid mode. Actual printing exposed a callback that restored the old print content; this was corrected and covered by assertions after PDF generation.

Preview evidence: [desktop home](v2-desktop-home.png), [Unit 2 grammar](v2-grammar-unit2.png), [mobile grammar](v2-mobile-grammar.png), [print PDF](v2-print-review.pdf).

## Practical limits

Browser checks verify speech targets and fallback behavior, not audible voice quality on the child's device. No independent learner observation has been performed; this report does not certify learning effectiveness. Notes stay within the browser/origin and can be exported. No GitHub upload or deployment was performed because this workspace has no configured repository destination.

Usability follow-up: opening the file or hosted root starts Unit 1 immediately. Explicit Home and unit/activity deep links remain available. All visible Chapter labels were replaced with Unit, and desktop navigation identifies Unit 1, Unit 2 and Unit 3. Four additional browser assertions cover this behavior.

Connect sizing follow-up: image heights increased from 58px desktop / 47px mobile to bounded 112?164px; typography uses linear interpolation with CSS clamp and container-width units. At activity widths below 680px, directional maps stack vertically and stage controls use two columns. 74 additional checks passed across 360, 390, 768, 1024, 1440 and 1920px, covering every Unit and all four map stages (image size, label size, overflow and direction). Data checks (276) and v2 browser checks (71) were rerun and passed. The 108-check regression result above belongs to the preceding naming/landing change. Screenshots: [desktop Connect](connect-1440.png), [mobile Connect](connect-390.png).

Typography/density follow-up: learning instructions now use 17-18px, worked English sentences 20-21px, Vietnamese scaffolds 16px, desktop activity labels 16px and grammar step labels 17px. Topbar reduced from 82px to 60px; unit header, tabs, step controls and pattern margins reduced. Mobile keeps 15px activity/step labels, 17px instruction text and 20px example text. All 276 data checks, 71 v2 browser checks and 74 Connect checks passed after the layout changes; v2 was rerun after final callout refinements. Print CSS is unaffected.

Whole-project hierarchy audit: shared styles now cover Home cards, Unit titles, activity navigation, reading, writing, grammar companions, quiz, audio/parent dialogs and mobile. Unit titles retain emphasis; subtitle and helper text use a quieter tone. Navigation uses medium weight and a consistent selected background/left marker; grammar semantic colors remain distinct. Final gates: 276 data checks, 71 v2 checks, 108 browser regressions, 74 Connect checks and 18 all-words layout checks, all passed. The regression selector for mixed review was scoped to the rail because the end-of-Unit button also opens mixed review. Missing directional arrow glyphs were corrected. Screenshots regenerated during browser runs; desktop and mobile captures reviewed.

Pre-commit portability audit (2026-10-01): QA moved to qa/package.json with a committed lockfile and shared runtime; no tmp/qa dependency remains in the five check scripts. `npm test` from qa completed: regression 108, v2 71, vocabulary 18, Connect 74, classwork 32; source validation 276. Total 579 passed, zero failures. Both local project skill and pedagogical skill passed structural validation. Browser execution was verified on Windows/Edge; Chromium configuration for other systems was not exercised here. See PRE_COMMIT_REVIEW.md and root README for packaging and source-material requirements.
