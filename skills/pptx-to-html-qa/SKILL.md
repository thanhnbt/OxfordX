---
name: pptx-to-html-qa
description: Quality Assurance (QA) and Visual Regression Testing for PPTX to HTML conversions.
---

# PPTX to HTML QA Skill

## Overview
This skill outlines the standard Quality Assurance (QA) procedures to verify that a PowerPoint (.pptx) file has been correctly converted to HTML/CSS by the Antigravity V8 Engine. 

## Primary QA Script
The main QA script is `qa/check_underlines.py`. Run it from the project root:
```
python qa/check_underlines.py
```
It automatically scans all output directories under `outputdata/` and validates:
1. **Underline Validation** — checks that expected words on specific slides have `<u>` tags (collision-detected or Font.Underline).
2. **Font.Underline Preservation** — verifies that Runs-path slides preserve Font.Underline formatting.
3. **Content Coverage** — ensures slides have CSS-rendered text or OCR overrides (not just PNG images). Known photo-only slides are skipped.
4. **Shape Rendering** — confirms specific shapes are CSS-rendered rather than PNG fallbacks.

Expected underlines and slide-specific rules are defined per `basename` (e.g. `bai_3`, `bai_2`) inside the script.

## Automated Visual Regression Testing (VRT)
When running VRT on slides, use Playwright to take screenshots of the generated HTML (`presentation.html`) and compare them against the native PowerPoint renders (`images/slide_*.png`). 

### Available VRT Scripts
If the user provides a `qa/` folder (e.g. `qa/vrt_snapshots.js`, `qa/check_slides_visual.js`), use them to automate the visual checks:
1. `node qa/vrt_snapshots.js` - Takes full-page screenshots of specific slides or steps to detect visual regressions.
2. `python qa/check_underlines.py` - Validates underlines, content coverage, and shape rendering across all outputs.

## QA Checklist for PPTX Conversions
When the user asks you to "QA" or "Check" a slide, systematically verify the following:
1. **Underline & Formatting**: Ensure that underlines are precisely on the target words, not bleeding across the whole paragraph. (See `pptx-to-html-v8` Rule 2, 3, 10).
2. **Missing Text / Truncation**: Text blocks must not be cut off. Do NOT use `overflow-y: auto` (scrollbars) on autofit-containers as a solution for overflowing text. Instead, rely on the native `applyAutoFit` script which dynamically shrinks font sizes to fit content within bounds. (See `pptx-to-html-v8` Rule 12).
3. **Ghost Shapes / Z-Index**: Verify that native PPTX background images do not cover up interactive HTML layers. Overrides should have a high `z-index` (e.g., `z-index: 100`).
4. **Grouped Shapes**: Ensure no text is trapped inside a static `MsoGroup` image unless intentionally rasterized.

## How to execute QA
1. Run `python qa/check_underlines.py` — this is the standard automated check covering underlines, content coverage, and shape rendering.
2. If visual debugging is needed, run `node qa/check_slides_visual.js` to dump screenshots of the exact DOM state.
3. If DOM logic is in question, parse `outputdata/*/presentation.html` and validate coordinates, dimensions, and text alignment.
4. Present the findings to the user. Do not make assumptions about visual correctness without running a snapshot check or inspecting the DOM bounding boxes.
