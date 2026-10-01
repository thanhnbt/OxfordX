# Oxford Discover 4 — Unit 1–3 review

Open `index.html` locally or upload that file to GitHub Pages. It embeds all lesson data, pictures, styles and scripts. No build is needed to view the downloaded page.

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

Rebuilding/source validation requires the original matching Teacher's Book PDF at the repository root. Local source PDFs and diaries are excluded from Git. The built page and browser checks run without them. Windows QA can use installed Edge; other systems use Playwright Chromium. Set `OXFORD_BROWSER_PATH` only to override the browser executable.

Maintained sources: `web/`, `scripts/`, `data/hybrid.json`, `data/classwork.json`, image assets and provenance records. Generated `index.html` should be committed with its source changes.

## Reuse the local skill

Project guidance is in `AGENTS.md`; the task skill is `skills/oxford-review-project/SKILL.md`. After downloading, ask your agent to read and apply that local skill. This does not depend on a globally installed skill. The broader pedagogy skill and PDF/OCR helpers are included in their existing project folders.

Read `PRE_COMMIT_REVIEW.md` before committing. QA screenshots/results are generated locally. Notes remain specific to the browser/origin and can be exported from For grown-ups. Browser speech uses device voices; it is not the textbook audio.
