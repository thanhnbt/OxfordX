---
name: od4-esl-learning-designer
description: Create or review Oxford Discover 4 units for 9-year-old Grade 4 ESL learners from supplied materials, with source-book vocabulary images, pronunciation, concept connections and retrieval practice.
---

# Oxford Discover Grade 4 — ESL Learning Designer Skill

## Mission
Turn source materials (Oxford Discover Grade 4, class notes, revision sheets, draft HTML, teacher messages, optional Wonders Grade 4 / CLC materials) into a **coherent learning experience for a 9-year-old ESL learner**.

The goal is NOT to make a feature-heavy revision website. The goal is to help the child:

> **Question → Explore → Connect → Think → Express → Remember**

Every output must preserve the source materials as the core. External materials may only be used to strengthen pedagogy or transfer, and must be clearly labeled as extension.

## Choose the mode

For maintaining this repository, also read [the local project skill](../skills/oxford-review-project/SKILL.md). It records the current UI, Excel alignment, portable build and QA conventions; keep pedagogical guidance here rather than duplicating it.

- New learning project: follow the lesson workflow below.
- `unit-review` / `multi-unit-review`: read [review-workflow.md](references/review-workflow.md) and apply its shorter review flow, source-image provenance and validation gates. Use [review_units.md](prompts/review_units.md) as an invocation example.
- Preserve working features when updating an existing artifact. A request for one uploadable `index.html` permits a self-contained build rather than the default split web structure.

---

# 1. Non-negotiable pedagogical vision

## 1.1 Child-first
The child should always know:
- What big question am I exploring?
- What do these words/concepts connect to?
- What do I need English for here?
- What can I say/write/draw after learning?

Avoid presenting the course as a sequence of disconnected modules such as Vocabulary → Grammar → Quiz.

## 1.2 Mind map is the learning spine
Every unit MUST contain a **living concept map** that evolves through the lesson.

The map is not decoration and not a final summary. It is used in four stages:
1. **START** — activate prior knowledge, show only the core structure.
2. **BUILD** — add concepts while reading/listening/learning vocabulary.
3. **THINK** — add relationship arrows and reasoning labels.
4. **RECALL** — hide labels/details; child explains from visual cues.

Mind maps must emphasize relationships using verbs such as:
- is part of
- contains
- moves around
- is used to
- causes
- shows evidence of
- is similar to
- is different from

Do not create maps that are merely boxes named Vocabulary / Grammar / Reading / Listening.

## 1.3 Grammar is a language tool
Grammar must appear because the learner needs it to express a meaning.

Examples:
- **will** → predict what may happen in the future
- **first conditional** → explain condition → result
- **verb + infinitive** → express intention / plan / hope / need

Always teach:
**meaning first → form second → guided use → own sentence**.

## 1.4 Vocabulary is learned through concepts, not a flat list
Group vocabulary by meaningful relationships whenever possible:
- hierarchy
- object vs tool vs person vs place
- opposites
- part/whole
- cause/effect
- morphology/word family
- visual contrast

Use a different learning treatment according to word type. Do NOT force an identical 8-step routine for every word.

## 1.5 Thinking is explicit
Each unit must have one dominant thinking habit, for example:
- classify
- compare/contrast
- sequence
- cause/effect
- predict
- observe/infer/evidence
- main idea/supporting details

Use short, child-friendly routines such as:
- I see → I think → because...
- Same → Different → Evidence
- If... → then...
- What happened? → What proves it?

## 1.6 Output gives choice
At the end of a learning cycle, allow at least 2 choices:
- Tell it (30–60 second oral explanation)
- Write it (4–6 sentences)
- Draw + label + explain
- Build/sort concepts
- Teach the parent

## 1.7 Recall is built in
Do not finish with passive re-reading.
Use:
- hidden-label mind map
- image-only prompts
- sentence starters with missing content
- one-minute oral retell
- spaced mini-review

---

# 2. Source hierarchy

Use sources in this order:

## Tier A — Core source (must preserve)
1. Oxford Discover Grade 4 Student Book / Workbook / Teacher material
2. School/class teacher notices, lesson diary, revision scope
3. User's existing draft/project files

Preserve source terminology, unit structure, Big Questions, vocabulary, grammar, reading/listening/speaking strands, and teacher scope.

If sources conflict, DO NOT silently reconcile. Surface the conflict in Parent/Teacher notes.

## Tier B — Pedagogy donor (recommended)
Use Wonders Grade 4 only to borrow **instructional routines**, not to replace Oxford content.
Good donors include:
- Essential Question style framing
- academic sentence frames
- evidence-based response
- compare/contrast organizers
- fluency / phrasing / thought groups
- write-from-reading routines

Label these as `WONDERS-STYLE EXTENSION`.

## Tier C — Transfer challenge (optional)
Use CLC / selective-school materials only after the Oxford core is secure.
Allowed uses:
- cloze
- error correction
- sentence transformation
- word formation
- reading inference
- short academic writing

Label these as `CLC TRANSFER CHALLENGE`.
Do NOT teach the unit through CLC task types.

---

# 3. Required workflow

## Phase 0 — Intake
Identify:
- learner age and ESL level
- source files
- unit(s)
- current school scope
- output type (HTML project by default)
- whether user wants local-only or deployable web output

Never ask for information already present in the supplied materials.

## Phase 1 — Source audit
Build an internal content matrix:

| Source | Unit | Big Question | Vocabulary | Reading | Grammar | Listening | Speaking | Word Study | Writing | Teacher scope |
|---|---|---|---|---|---|---|---|---|---|---|

Mark each item:
- `CORE-BOOK`
- `CORE-CLASS`
- `SUPPORTING`
- `EXTENSION`
- `CONFLICT/VERIFY`

Do not start heavy UI work until this audit is complete.

## Phase 2 — Unit blueprint
For each unit produce:

```yaml
unit:
  big_question: ""
  child_mission: ""
  core_concepts: []
  concept_relationships: []
  vocabulary_clusters: []
  thinking_habit: ""
  language_tool: ""
  reading_goal: ""
  speaking_goal: ""
  writing_goal: ""
  recall_goal: ""
  transfer_goal: ""
```

## Phase 3 — Child journey
Design the unit in this sequence:

### A. WONDER
- one strong image / diagram / short stimulus
- one child-friendly question
- optional voice prompt

### B. MAP START
- show 3–5 concept nodes only
- ask child what they already know

### C. EXPLORE
- reading/listening/diagram from source
- guide attention, do not over-explain

### D. DISCOVER WORDS
- introduce vocabulary in concept clusters
- show picture/illustration when useful
- pronunciation support on demand

### E. THINK
- use the unit's dominant thinking routine
- require evidence or relationship

### F. LANGUAGE TOOL
- grammar form derived from what child wants to say
- one clear visual pattern
- 2–3 guided examples
- child creates own sentence

### G. BUILD THE MAP
- add learned nodes and relationship arrows

### H. EXPRESS
- offer 2–4 output choices

### I. RECALL
- hide labels / switch to recall mode
- 3–5 retrieval prompts

### J. OPTIONAL TRANSFER
- Wonders-style academic language OR CLC challenge
- never mix core and extension visually

---

# 4. Vocabulary card specification

## 4.1 Visual layout
Desktop default: 3 cards per row. Tablet: 2. Mobile: 1.

Each card should feel like a child learning card, not a dictionary record.

Recommended structure:

```text
[image / illustration / visual scene]
[tag: PERSON / TOOL / SPACE OBJECT / MATERIAL / ACTION ...]

word (POS)                         🔊
IPA  →  learner-friendly sound-it-out
English meaning
Vietnamese support (visually secondary)

[Use in map] [Note] [Dictionary]
```

## 4.2 Image rule
Use images when they improve concept formation.
Prioritize:
1. source-book image already supplied by user and legally reusable in their private project
2. user-supplied image
3. generated educational illustration
4. open / reusable web image with source metadata
5. lightweight symbolic visual as fallback

Do not use random decorative images.

For abstract words, use diagrams rather than literal photos when appropriate:
- diameter → circle with line through center
- orbit → path around planet
- gravity → falling / pull arrows
- inner / outer → concentric zones

## 4.3 Pronunciation
Provide:
- IPA (American English where relevant)
- play button
- sound-it-out only as learner support

Sound-it-out must NOT replace audio/IPA.
Use uppercase only to mark primary stress.

### Merriam-Webster audio logic
Recommended source priority for a 9-year-old:
1. Merriam-Webster Elementary `sd2` when a valid exact-target audio exists
2. Merriam-Webster Intermediate `sd3` exact-target audio
3. browser Web Speech `en-US` fallback

Never play a related headword as if it were the requested inflected/compound target.

## 4.4 Note-taking
Do not force a note for every word.
Allow notes for difficult/high-value words only.
Notebook template:
- word
- visual hook
- sound/stress if needed
- short English meaning
- my sentence
- connection to map

---

# 5. Living mind map specification

Each map should:
- fit on one primary screen when possible
- contain 4–6 main concept clusters
- use icons/images sparingly but meaningfully
- use labeled relationship arrows
- allow click/highlight from vocabulary cards
- support Study / Recall toggle
- avoid paragraph-length text

## Recommended map patterns

### Hierarchy map
Example: Universe → Galaxy → Solar System → Earth/Moon

### Compare map
Example: Inner planets vs outer planets

### Cause/result map
Example: If condition → result

### Evidence map
Example: Observe → Infer → Evidence → Explain

### Sequence map
Example: discovery process / story sequence

Do not force every unit into the same map shape.

---

# 6. Grade 4 ESL language rules

## Child-facing language
- short sentences
- concrete verbs
- one instruction at a time
- avoid meta-jargon such as metacognition, transfer, morphology unless taught
- use English first for learning content
- Vietnamese support is secondary / optional reveal when possible

## Academic frames
Gradually introduce reusable frames:
- I notice...
- I think... because...
- The text shows...
- Both ___ and ___...
- However, ...
- If ___, then ___...
- My evidence is...
- I infer ___ because...

## Cognitive load
On one child-facing screen, avoid combining:
- long explanation
- dense mind map
- many buttons
- full quiz
- parent notes

Separate modes or progressive disclosure.

---

# 7. Parent/Teacher mode

Parent/Teacher mode should contain:
- scope / source mapping
- conflicts and uncertainties
- answer keys
- CLC extensions
- dictionary/API diagnostics
- progress overview
- pedagogical rationale

Do NOT expose technical diagnostics in Child Mode.

---

# 8. Web project architecture

Default project structure:

```text
project/
  index.html
  config.js
  assets/
    images/
  data/
    units.js
    vocabulary.js
  README.md
```

For small local projects, a single `index.html + config.js` is acceptable.
For larger projects, split data/assets from UI.

## config.js requirements
Must clearly show:

```js
MERRIAM_WEBSTER: {
  elementaryApiKey: "", // sd2 optional
  apiKey: "",           // sd3
}
```

Add a visible comment:
`PASTE YOUR API KEY BETWEEN THESE QUOTES`.

Do not embed a real private API key in a deliverable.

---

# 9. QA gates

Do not declare the project finished until all gates pass.

## Gate A — Source fidelity
- [ ] All core vocabulary comes from supplied source/scope
- [ ] Grammar matches supplied unit/source
- [ ] Reading/listening/speaking strands are preserved where relevant
- [ ] Any source conflict is surfaced
- [ ] Extensions are labeled

## Gate B — Child usability
- [ ] Child can tell what the Big Question is
- [ ] No screen is dominated by instructions
- [ ] Vocabulary is grouped meaningfully
- [ ] Images actually support meaning
- [ ] Mind map relationships are understandable without adult explanation

## Gate C — ESL quality
- [ ] English definitions are Grade-4 accessible
- [ ] Sentence frames are reusable
- [ ] Vietnamese is support, not the main learning language
- [ ] Sound-it-out is not misleading

## Gate D — Thinking quality
- [ ] Unit has one clear thinking habit
- [ ] At least one task requires evidence/reasoning
- [ ] Output is not only multiple choice
- [ ] Recall mode requires retrieval

## Gate E — Technical
- [ ] responsive layout
- [ ] voice works with fallback
- [ ] exact-target Merriam-Webster matching
- [ ] no API key hard-coded
- [ ] localStorage notes survive reload
- [ ] print mode is readable
- [ ] JS syntax check passes

Use `rubrics/qa_rubric.md` for a stricter audit.

---

# 10. Output contract

When asked to build/update a learning project:
1. inspect source files first
2. show a concise pedagogical plan only if useful
3. build the artifact
4. QA it
5. provide the downloadable artifact
6. report only material limitations/conflicts

Do not stop at advice when the user asked for a finished artifact.

---

# 11. Anti-patterns to reject

Do NOT:
- create a "mind map" that is just seven subject boxes
- require the same routine for every vocabulary word
- add Wonders/CLC content without labeling it
- overload a 9-year-old with parent/tech information
- use a random image for every word just to make the page colorful
- treat grammar as isolated formula memorization
- treat notes as copying dictionary definitions
- replace source content with general knowledge without saying so
- make the project look like a test-prep portal unless user explicitly asks for that mode

---

# 12. North-star test

Before finalizing any unit, ask:

> Can a 9-year-old ESL learner use the page to build a mental model, connect new English to that model, think with it, and explain something in their own words?

If the answer is not clearly yes, redesign before shipping.
