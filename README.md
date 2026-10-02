# Oxford Discover 4 — Unit 1–3 review

Merriam-Webster is now the default vocabulary audio provider. In `web/dictionary-config.js`, replace the `MW_CONFIG.MW_API_KEY` placeholder `8xxx` with an Intermediate Dictionary key and keep `REFERENCE: 'sd3'`, then rebuild. Placeholder/missing keys fall back to browser speech. MW spelling suggestions are not played as the requested word. Direct frontend keys are visible in the built page; use a server proxy for confidential keys. MW audio URL rules follow https://dictionaryapi.com/products/json. IPA and child-friendly definitions remain the authored book-based content. Live MW authentication has not been tested without a real key.

Dictionary vocabulary audio is configured in `web/dictionary-config.js`; rebuild after changing it. The default Free Dictionary API needs no key. Optional proxy settings accept an endpoint returning dictionary-compatible phonetics and a public/restricted client token; secret provider keys belong on that proxy server. Vocabulary prefers a US recording when the URL identifies it, otherwise an available recording, then browser TTS. Sentences/readings use browser TTS. Only the clicked word is sent for dictionary lookup; written notes are not sent. The root `index.html` is the main menu; each standalone lesson is generated under `output/unit-N.html`.

Open `index.html` locally or upload it with the `output/` folder to GitHub Pages. The menu links to self-contained Unit pages with their own data, images, styles and scripts. Unit 3 also embeds its synchronized source lesson. Keep the relative folder structure intact when hosting.

## Rebuild and verify

Use Python 3.10+ and Node.js 20+. From the repository root:

```sh
python -m pip install -r requirements.txt
cd qa
npm ci
npx playwright install chromium
cd ..
python scripts/build_review.py
python scripts/validate_review.py
cd qa
npm test
cd ..
```

`build_review.py` and source validation require the original matching Teacher's Book PDF at the repository root. `build_outputs.py` can regenerate the menu and Unit pages from the existing `data/review.json` and image assets without the PDF. Local source PDFs and diaries are excluded from Git. The browser checks run without them. Windows QA can use installed Edge; other systems use Playwright Chromium. Set `OXFORD_BROWSER_PATH` only to override the browser executable.

Maintained sources: `web/`, `scripts/`, `data/hybrid.json`, `data/classwork.json`, image assets and provenance records. Generated `index.html` and `output/unit-N.html` files should be committed with their source changes. The merged QA fixture is written under ignored `tmp/qa/`.

## Reuse the local skill

Project guidance is in `AGENTS.md`; the task skill is `skills/oxford-review-project/SKILL.md`. After downloading, ask your agent to read and apply that local skill. This does not depend on a globally installed skill. The broader pedagogy skill and PDF/OCR helpers are included in their existing project folders.

Read `PRE_COMMIT_REVIEW.md` before committing. QA screenshots/results are generated locally. Notes remain specific to the browser/origin and can be exported from For grown-ups. Browser speech uses device voices; it is not the textbook audio.
