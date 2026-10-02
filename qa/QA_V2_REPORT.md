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

UI refresh (2026-10-02): standalone Unit pages use a visible 200px vertical activity rail on desktop, with no inner reserved menu column. Unit heading, question and activity align at the workspace inset. Mobile uses wrapped activity controls and a stacked topbar. Vocabulary headers alternate blue, mint and cream; word weight is 700, definitions regular, sound clues 650. Existing grammar token colors and note keys remain intact. Reviewed Unit 3 desktop (1440px) and mobile (390px) captures in tmp/qa/ui-refresh-*.png; both have no horizontal overflow. Full browser suite passed: standalone 61, regression 108, bilingual/grammar 71, vocabulary 18, Connect 74, classwork 32, dictionary 10. Source validation passed 284 checks. Validator now extracts the real runtime after the JSON data block, avoiding scripts inside the embedded lesson string.

HTML book reconstruction (2026-10-02): Unit 3 reading now renders one live SB30-31 book spread. The full-page raster and duplicate recap are removed; all 90 thought groups and 472 word spans retain their original text, timing keys, and recorded audio bytes. Four original art crops retain the soldier, general, pit scene and compound craftsmen/head-detail illustration; source provenance, pixel crop bounds and hashes are recorded in data/reading-spread-manifest.json. CSS clip masks exclude neighboring printed prose; Think callouts are live HTML. Source image and desktop/mobile render comparison completed, with matching hashes in qa/visual-review.json. Player remains above the reading; desktop uses facing pages and narrow screens reflow vertically. Existing thinking/listening drafts and classroom panels remain available. Source validation: 284 PASS; Unit output/browser checks: 61 PASS; classwork: 32 PASS. A dedicated qa/reading-spread-check.cjs covers unique text, unchanged timings/audio, art decoding, responsive layout, seeking and repeat; run with npm run test:reading from qa. Other UI sections were not redesigned in this change.
Final dedicated reading check: 51 PASS, 0 FAIL, including presence of the existing thinking/listening answer fields and absence of the duplicate short-reading panel.

Content restoration and responsive correction (2026-10-02): restored the complete original bilingual reading review alongside the full HTML book lesson; thinking, listening, author-purpose guidance and saved-answer fields remain intact. All six Unit activities remain navigable. At <=680px reading text spans the available width, art moves into the vertical flow, callouts stop floating and the right page becomes one column. Tablets use a single book page at a time. Audio buttons retain 44px targets. Automatic thought scrolling targets only .book-scroll, keeping player controls visible. Desktop/tablet/mobile captures reviewed in tmp/qa/responsive-reading-{1440,768,390}.png. Final source validation 284 PASS; whole-project suite 61 output, 108 regression, 71 bilingual/grammar, 18 vocabulary, 74 Connect, 32 classwork, 10 dictionary PASS. Dedicated reading regression 55 PASS after the final scroll fix, including restored recap/answer fields, mobile text width and player visibility after seeking.

Culture Note popup (2026-10-02): added a Unit 3 button under the Remember the reading introduction, aligned left. data/culture-note.json preserves all three English paragraphs from the supplied Culture Note image and pairs them with authored Vietnamese translations. EN mode displays English only; EN+VI displays each paragraph with its translation. Native modal supports Escape, an explicit Close button, backdrop dismissal and restored trigger focus; its sticky header keeps Close accessible while reading. Desktop/mobile screenshots reviewed in tmp/qa/culture-note-{1440,390}.png. Original reading panels and saved-answer fields remain intact. Final source validation 284 PASS; focused popup checks 38 PASS across desktop/mobile and both modes. Run npm run test:culture-note in qa. Language changes are dispatched through the existing button handler in the automated check; popup open/close actions use browser clicks.
