# UI/UX v2 — Oxford Discover 4, Vietnamese Grade 4 ESL

## Diagnosis and intended outcome

The first version preserves scope and works technically, but repeated white cards, equally weighted tabs, large soft source pictures and dictionary-like vocabulary make it feel like a prototype. Grammar has little visual priority and Vietnamese only supports vocabulary definitions. English instructions alone add avoidable reading effort for this learner.

The revision should feel like a coherent learning workspace for a nine-year-old: clear entry points, attractive but restrained illustrations, readable bilingual support and grammar that can be understood and practised. Book content remains the source of scope. No CEFR level is inferred from Grade 4.

## Information and navigation

- Desktop: a stable chapter sidebar, compact top utility bar, spacious main canvas. Mobile: a compact chapter picker above the content, without a sidebar consuming screen width.
- Home: one learning promise, three distinct chapter cards, an obvious grammar shortcut for each unit and a short explanation of the learning sequence.
- Unit: Big Question plus Vietnamese explanation, activity navigation with clear active state; Grammar Lab gets a visible shortcut and a distinct navigation treatment.
- Keep vocabulary, concept connections and productive output in the same learning journey. Grammar is prominent, but remains connected to the chapter meaning.

## Bilingual strategy

Default **English + tiếng Việt**. A persistent toggle switches to **English**. The mode changes scaffolding rather than substituting the source vocabulary or English practice targets.

- Navigation: short English label, small Vietnamese helper in hybrid mode.
- Vocabulary: retain source picture, word, IPA, sound-it-out and English meaning. Show concise Vietnamese meaning as secondary support in hybrid mode; English mode retains optional reveal. Audio reads English only.
- Reading: English paragraph first; optional Vietnamese explanation appears directly beneath it in hybrid mode. Translations preserve the short adapted recap rather than introducing new book claims.
- Thinking/output: Vietnamese instructions explain what to do; response frames stay English.
- Grammar: explain the communicative purpose in Vietnamese, pair worked English examples with natural Vietnamese translations, and highlight structure consistently. Avoid implying a word-for-word equivalence between the languages.
- Retrieval: do not reveal headword translations, IPA or definitions before the child reveals a card. Vietnamese task instructions may remain because they are scaffolding, not answers.

## Grammar Lab specification

Three small steps: **Understand / Hiểu ý**, **Build / Ráp câu**, **Try / Luyện tập**. Each stage has one main objective and a clear next action.

Semantic colors are stable across units: subject = blue; grammar marker = purple; lexical/base verb = amber; condition = teal. Text labels accompany color so the design works without color recognition.

1. Unit 1, will: predictions; distinguish the subject, will, base verb and rest of the sentence. Include a future marker in examples. Practice avoiding will + past/ing.
2. Unit 2, future real conditional: possibility → future result. Highlight present simple inside if and will + base verb in the result. Explain why will is not placed in the if part of these model sentences.
3. Unit 3, infinitives: the selected verbs want/plan/hope/decide/try followed by to + base verb. Do not generalize the pattern to every English verb.

Worked examples are authored practice grounded in the source unit. A sentence builder offers finite, meaningful choices, updates color-coded English and natural Vietnamese together, and speaks the exact constructed English. Guided checks preserve source grammar; bilingual explanations identify the rule. A separate error-correction prompt and a learner-authored sentence follow. Open responses are not falsely graded automatically.

## Visual system

Warm white canvas, dark navy chapter rail, indigo learning emphasis, restrained amber CTAs. Use a coherent type scale, deliberate whitespace, lightweight borders and modest shadows. Avoid excessive gradients, heavy glow or decorative badges on every element.

Use source vocabulary pictures at appropriate size; preserve aspect ratios and avoid enlarging low-resolution crops into dominant hero artwork. The home hero may use a lightweight authored vector composition clearly separate from the source-book imagery. Unit 1/2/3 get distinct book-image excerpts.

Keep approximately six vocabulary cards per desktop batch, responsive layout, touch targets of at least 44px for primary controls, keyboard focus, readable contrast, reduced-motion support and print styling isolated from the app layout.

## Implementation order

1. Save a v1 copy and keep notes/audio compatibility.
2. Add bilingual/grammar metadata to authored unit data; keep original word lists and source references.
3. Replace layout and apply the v2 visual system.
4. Implement Grammar Lab and progressive bilingual scaffolding; add grammar shortcuts.
5. Build self-contained index.html and run source/asset/JS checks.
6. Run real browser checks for navigation, language persistence, recall leakage, builder grammar/translation/audio, feedback and saved writing; retain existing quiz/storage/mobile/HTTP regression checks.
7. Inspect home, all grammar units, vocabulary/mobile and print screenshots. Fix failures before delivery.

## Acceptance and limits

Implementation completed on 2026-10-01. The standalone output passes 276 data/source/asset checks, 108 browser regression checks and 71 v2 interaction checks. See [QA v2 report](qa/QA_V2_REPORT.md) for evidence and remaining device/learner checks.

No wrong source content, broken controls, leaked retrieval answers, misleading sentence-builder output or mobile overflow. Verify actual output, not only CSS/text matching. All new English/Vietnamese mappings are reviewed as authored scaffolds; existing core scope remains audited.

Audible voice quality and independent observation with the learner remain device/learner checks. UI polish and adult review cannot certify learning effectiveness. Deliver one index.html, revised skill guidance and a v2 QA report; no GitHub publication is assumed without a repository destination.
