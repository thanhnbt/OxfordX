---
name: oxford-review-project
description: Maintain this Oxford Discover 4 review project from Teacher's Book PDFs and class diary Excel files, with Vietnamese Grade 4 ESL scaffolding, portable HTML builds and source/browser QA.
---

# Oxford review project

Use this skill for updates to this downloaded project. Resolve the repository root as two directories above this file; run commands from that root. No machine-specific paths are required.

## Start with the relevant source

- Read `UI_STYLE_RULES.md` for UI changes. Preserve the requested compact layout, vertical activity menu, all 11 words without pagination, and image-left vocabulary headers.
- Read `od4_esl_learning_designer_skill/references/review-workflow.md` for lesson/content changes; consult that skill's full `SKILL.md` when designing a new lesson.
- For diary alignment, read `qa/TIMETABLE_AUDIT.md` and `data/classwork.json`. Check diary unit labels against the PDF: SB36–40 dinosaur material is Unit 4 even where this diary calls it Unit 3. Distinguish scheduled lessons from confirmed completed lessons. Never embed student names or missing-work comments.

## Maintain sources, then build

Edit `web/review.template.html`, `web/v2.css`, `web/v2.js`, `data/hybrid.json`, `data/classwork.json` or `scripts/build_review.py`; do not patch generated `index.html` alone. Core authored unit data/crop coordinates live in the build script. `data/review.json` and the image manifest are generated.

Keep English targets/audio and natural Vietnamese support appropriate for a 9-year-old Grade 4 ESL learner. Grammar follows meaning → form → guided use → own sentence. Hide all answers in recall mode. Preserve saved-note keys and fallback behavior. Open writing is not automatically graded.

Place the matching Teacher's Book PDF at the repository root for rebuilding. Keep the original Excel local for future source audit. Install dependencies using the root README; never require another machine's `tmp/qa` or Edge path.

Run `python scripts/build_review.py` to generate a standalone `index.html`. Run `python scripts/validate_review.py` for source, assets and syntax. Changing images requires visual review and updated hash evidence in `qa/visual-review.json`; do not mark a crop reviewed from code checks alone.

## Verify the actual behavior

Run `npm test` from `qa/` for a release/content-wide update. For a small scoped change, run the relevant check script from the repository root:

- `qa/browser-check.cjs`: navigation, quiz, notes, audio/storage fallback, hosting.
- `qa/v2-check.cjs`: bilingual grammar, builders, actual printing, responsive stages.
- `qa/all-words-check.cjs`: 11 cards, image/heading structure and responsive overflow.
- `qa/connect-check.cjs`: all concept-map stages and readable sizes.
- `qa/classwork-check.cjs`: eight classroom panels and saved drafts.

Inspect desktop/mobile screenshots for affected sections; inspect actual print output when print/content changes. Report PASS, FAIL, NOT RUN honestly. Device voice quality and learner observation require separate evidence.

Before commit, read `.gitignore` and `PRE_COMMIT_REVIEW.md`. Keep PDFs, original diaries, dependencies and temporary files out of Git. Refresh report byte size/hash only after the final build, and describe which checks ran. The webpage deployment needs only `index.html`; the reusable development repository needs sources, scripts, skills and QA configuration. Do not infer permission to commit, push or deploy.
