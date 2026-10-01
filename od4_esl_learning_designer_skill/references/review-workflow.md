# Book-based unit review

Use `unit-review` for one unit and `multi-unit-review` for several units. Review helps the learner retrieve and explain previously encountered content. If class diaries are absent, call it a book-based review; do not invent session dates or assert material was taught.

## Source and visual audit

Audit source before UI work. Separate reproduced student pages, teacher guidance, and answer keys. Extract embedded text first; OCR only unreadable/missing regions and visually verify it. Record PDF page, printed guide page and Student Book page separately.

Inventory each vocabulary visual. Prefer the book's dedicated picture, then a meaning-relevant book crop. Embedded page images can contain multiple pictures: region crops must exclude headword labels for retrieval tasks and preserve instructional details. Save source file, one-based page, crop bbox in PDF points with coordinate convention, asset path, visual role and review status. A scene showing a telescope user does not prove that the person is an astronomer. Do not label a generic scene as an exact headword illustration.

Visual statuses: `exact-book-image`, `supporting-book-image`, `authored-support-diagram`, `no-suitable-book-image`, `needs-review`. Label authored diagrams honestly. Report coverage; do not invent images to claim 100% book coverage.

## Review design

Preserve source Big Questions, core/context vocabulary, grammar and reading strategies. Keep paired-unit boundaries; do not include the next unit merely because it shares a Big Question. Default extensions to off.

Use a small concept map with meaning-bearing arrows, grouped vocabulary with IPA/sound-it-out/exact-target audio, a short reading recap, contextual language practice, a choice of speaking/writing/drawing, and retrieval. Do not force the full new-lesson sequence into every review. Introduce content in small batches, one main task at a time. English is primary; Vietnamese support is optional. Keep technical/source notes and answer keys in parent mode.

Hide word labels, pronunciation, definitions and answer-bearing alt text until the learner reveals an image prompt. Audio that gives the target word belongs after reveal or must be identified as a clue. Images for abstract words may test explanation rather than unique name identification.

Examples, summaries and practice questions adapted from the book must be identified as adaptations in parent notes. Book transcripts read by TTS are not official book audio. Never claim browser TTS will work offline without testing that device. Decline an unrelated voice/headword substitution and provide a readable fallback.

For a requested single uploadable HTML, embed scripts, styles, data and images; retain separate source data/crop manifests and reproducible build helpers in the workspace. Do not publish the entire source PDF as part of the web bundle.

## Validation gates

1. Source: compare complete headword lists and grammar/strand references with supplied material; manually check adapted reading facts.
2. Images: validate paths, bbox bounds, packed bytes and decode; visually review every crop beside its source and record status.
3. Skill: run the skill-creator structural validator, verify references/helpers, and exercise the relevant workflow. Structural validation is not behavioral validation.
4. Pilot: complete Unit 1 through recall, saved notes and open output before extending to the remaining units.
5. Browser: test desktop/mobile, recall leakage, navigation, quiz scoring/retry, saving, unavailable speech/storage, and all-unit printing. Preserve a readable fallback if persistence/audio is unavailable.
6. Report PASS / FAIL / NOT RUN / BLOCKED with evidence. Incorrect content/images, leaked answers and broken primary flows block delivery. Self-reported practice is not mastery. Adult QA is not evidence of child usability; record learner observation and audible pronunciation checks as pending when unavailable.

Project implementation for this repository: `scripts/build_review.py`, `scripts/validate_review.py`, `qa/browser-check.cjs` at the workspace root. These are project helpers, not scripts shipped inside the skill package; other projects must supply equivalent helpers.

## Vietnamese learner support and grammar emphasis

When requested for Vietnamese ESL learners, use an English–Vietnamese hybrid mode with concise secondary Vietnamese meanings, instructions and faithful reading recaps. Keep English practice targets and audio in English. Offer an English mode that reduces scaffolding and persist the mode when storage is available. Hide Vietnamese headword meanings together with IPA/definitions during retrieval.

Make grammar a visible entry point tied to the unit's communicative purpose. Use Understand → Build → Try, colored sentence parts with text labels, worked examples with natural Vietnamese translations, finite meaningful sentence-builder choices, exact constructed-sentence audio, rule-specific feedback, error correction and a learner-authored sentence. Distinguish if + present simple from will + base verb; do not imply all verbs take infinitives. Definitions, examples and translations are authored scaffolds, not new claims about the book.

Validate builder sentence/translation synchronization, English-only audio, saved writing, bilingual/English mode persistence, answer hiding, responsive grammar stages and the actual beforeprint event. Adult interpretation of learner needs is provisional until observed with the child. Project helpers: `web/v2.css`, `web/v2.js`, `data/hybrid.json` and `qa/v2-check.cjs`.
