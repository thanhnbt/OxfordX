# Pre-commit review — 2026-10-01

## Completed

- Added a reusable project-local skill at `skills/oxford-review-project/SKILL.md`, linked from root `AGENTS.md` and the existing pedagogical skill. The skill has no dependency on global skill paths.
- Added root README, Python dependency declarations and a QA package/lockfile. Browser checks use shared `qa/runtime.cjs` instead of `tmp/qa`; use installed Windows Edge when available or Playwright Chromium elsewhere.
- Added `.gitignore` for dependency folders, temporary files, original PDF/Excel inputs, extracted diary data, historical HTML and generated QA artifacts.
- Preserved the built standalone HTML and maintained sources. Eight class-diary supplements remain separate from core textbook content. Unit 4 diary/book label discrepancy is documented in `qa/TIMETABLE_AUDIT.md`.

## Commit contents

Include `index.html`, `web/`, `scripts/`, `assets/`, maintained `data/*.json` except the ignored diary extraction, local skills, `AGENTS.md`, `.gitignore`, `README.md`, `requirements.txt`, design/plan documentation, QA scripts/config/lockfile and evidence reports. Image provenance and visual-review hashes are part of the reusable source project.

Do not use this development file list as a Pages deployment bundle: only `index.html` is needed for the website. Check textbook image redistribution permissions before making a source repository public; the source PDF and pupil diary are excluded by default.

## Remaining actions and limits

This workspace has no `.git` repository or configured remote. No commit or push has been made. Once you initialize/choose the repository, inspect staged paths with `git diff --cached --name-only` before committing. Gitignore does not remove files that were already tracked in another repository.

Downloaded `index.html` runs without source materials. Rebuilding or verifying PDF provenance requires the matching local Teacher's Book PDF. Keep source materials in your own storage, rather than adding pupil diaries to Git. Workbook/Grammar Book assignments are references, not copied exercises; their source files have not been supplied. Dinosaur material remains outside Unit 1–3.

Skill structure and source validation have passed. The portable QA command is `npm test` from `qa/`. Latest full-suite results are recorded in `qa/QA_V2_REPORT.md`. Audible voice quality and observation with the child remain device/learner checks. Linux/macOS execution is supported by configuration but has not been run on those operating systems.
