---
name: pptx-to-html-v8
description: Convert a Microsoft PowerPoint presentation (.pptx) to a native HTML/CSS interactive web presentation.
---

# PPTX to HTML Converter (V8 Table Engine)

## Overview
This skill instructs the agent to convert a .pptx file into a directory of HTML, CSS, and exported images using the native Antigravity V8 PPTX engine (which uses win32com for high-fidelity DOM mapping).

## Prerequisites
- The host must be a Windows machine.
- Microsoft PowerPoint must be installed locally (it relies on COM automation).
- The required python packages must be installed: pip install -r requirements.txt.

## Project Structure
The converter is split into modules for maintainability:
```
scripts/
├── pptx2html.py          # Main converter — shape classification, HTML assembly
├── utils.py              # Pure utility functions (pt_to_px, bgr_to_hex, etc.)
├── text_renderer.py      # Unified text rendering (Words/Runs paths, font extraction)
├── underline_utils.py    # Geometric underline collision detection
└── templates/
    ├── style.css         # Shared CSS (uses {{SLIDE_W}}/{{SLIDE_H}} placeholders)
    └── presentation.js   # Shared JS — autoFit, resize, navigation, animation steps
```

## How to use
When the user asks you to convert a PPTX file to HTML, do the following:
1. Locate the absolute path of the input .pptx file.
2. Determine an output directory (default to export or the same folder as the input).
3. Run the python script from the `scripts/` directory (modules use relative imports):
   ```
   cd scripts
   python pptx2html.py -i <absolute-path-to-input.pptx> -o <path-to-output-dir>
   ```
4. Wait for the script to finish.
5. Respond to the user with a summary of the conversion and a clickable link to presentation.html in the output directory.
6. Run QA, always passing both paths — with `--pptx` the checker reads the source deck and stops reporting genuinely image-only slides as failures:
   ```
   python qa/check_underlines.py <output-dir>/presentation.html --pptx <absolute-path-to-input.pptx>
   ```
   It exits non-zero when a check fails. Without a path argument it prints usage and exits — it never guesses an output directory.

## Output conventions
- The generated page links back to a menu with `<a class="nav-home" href="../../index.html">`, so the output directory is expected to sit **two levels below** the project root (e.g. `outputdata/bai_7/`). Add a card to the root `index.html` for each new deck.
- The `<title>` is taken from the input .pptx filename.

## Caveats
- The script opens PowerPoint in the background. If it fails midway, PowerPoint may stay open as a ghost process. You may need to run `taskkill /F /IM POWERPNT.EXE` if you encounter COM lock errors.

## Rules
- **Rule 1 (Ungroup)**: `MsoGroup` (Type 6) objects must always be dynamically ungrouped (`com_shape.Ungroup()`) before parsing the DOM. If left grouped, PowerPoint's fallback mechanism exports them as static images, which causes text nodes inside the group to be unselectable and incorrectly converted in the final HTML.
- **Rule 2 (Underline/Collision)**: Never use substring matching (`word in run.Text`) to detect underlines, as it will incorrectly highlight entire runs or paragraphs if there are duplicate words. Instead, use geometric collision detection: calculate the intersection between the `BoundTop/BoundLeft/BoundHeight/BoundWidth` of `run` or `word` and the line shape's coordinates. The collision logic lives in `scripts/underline_utils.py` — always import from there instead of inlining it in `pptx2html.py`.
- **Rule 3 (Underline vs Formatting Precision)**: Use `run = p.Runs()` when precise original text formatting is required. Only fall back to `word = p.Words()` for text rendering when word-level granularity is explicitly needed (e.g. precise underline targets on a specific slide), because iterating by `Words()` destroys original formatting runs.
- **Rule 4 (OCR Injection)**: When replacing unrenderable shapes with OCR HTML overrides (`ocr_overrides/slide_N.html`), always use a boolean flag (e.g., `ocr_applied_for_slide = True`) per slide to guarantee the HTML is injected exactly **once**. Without this, multiple unrenderable placeholders on the same slide will cause the OCR HTML to be injected multiple times, breaking the layout.
- **Rule 5 (OCR CSS for Overrides)**: Any injected OCR HTML container inside the PPTX framework must have `position: absolute; top: 0; left: 0; width: 100%; height: 100%;` to cover the slide correctly. It should also have `overflow-y: auto;` to allow scrolling if the OCR text is longer than the 540px slide height. If using container queries (`cqw`), `container-type: size;` MUST be defined on the container.
- **Rule 6 (Post-Processing Injection)**: If OCR HTML overrides are generated and the generator script (`pptx2html.py`) does not natively support injecting them, use a standalone python script (like `scratch_inject_overrides.py`) utilizing `BeautifulSoup` to post-process the `presentation.html` file by targeting slide containers (e.g. `div` with `class_="slide"` and `data-slide="X"`).
- **Rule 7 (Font.Underline in Runs)**: When iterating `p.Runs()`, always check `run.Font.Underline`. If the value is non-zero and not `None`, wrap the span in `<u class="step-underline">`. This handles underlines that are set via Font formatting rather than geometric line shapes. The same fallback applies in `p.Words()` paths (both textbox and table) — after collision detection, check `word.Font.Underline` as a secondary underline source.
- **Rule 8 (fill_type 3 — Textured Fill)**: `msoFillTextured` (fill_type=3) should NOT force a shape to PNG export when the shape contains text. Instead, treat it as CSS-renderable and extract `com_shape.Fill.ForeColor.RGB` as the background color. Only export as PNG for fill_type values other than 1 (solid) and 3 (textured-with-text).
- **Rule 9 (OCR Override Integration)**: The converter natively checks for `ocr_overrides/slide_N.html` files relative to the input PPTX path. When found, the OCR HTML replaces all shape rendering for that slide. OCR overrides are the correct approach for slides that are entirely image-based (e.g., scanned worksheets) where COM text extraction yields no usable content.
- **Rule 10 (Collision Tolerance)**: Underline collision tolerance must use a negative lower bound to catch line shapes positioned slightly above the word's bottom edge. Use `(-8, 15)` for textbox words and `(-8, 45)` for table cell words. PowerPoint positions thin line shapes 0–6px above the text bottom edge; a tolerance starting at `0` will miss these matches. The `mark_used_lines()` pre-scan uses `(-15, 15)` which is intentionally wider.
- **Rule 11 (Module Architecture)**: Text rendering logic (font extraction, span generation, underline wrapping) is centralized in `text_renderer.py`. Never duplicate these in `pptx2html.py` — always import `render_words`, `render_runs`, `get_paragraph_format`, `render_paragraph_tag`. CSS and JS are in `templates/style.css` and `templates/presentation.js` with `{{SLIDE_W}}`/`{{SLIDE_H}}` placeholders replaced at generation time.
- **Rule 12 (No overflow-y: auto on autofit-containers)**: Never add `overflow-y: auto` to `.autofit-container` divs. The `applyAutoFit()` JavaScript checks `scrollHeight > clientHeight` to detect overflow and shrinks font sizes. Adding `overflow-y: auto` causes the scrollbar itself to trigger false overflow detection, shrinking all fonts to the 8px minimum. Only OCR override containers (which don't use autoFit) may use `overflow-y: auto`.
- **Rule 13 (Video Handling)**: Embedded video shapes (`msoMedia`, Type 16) are extracted from the PPTX ZIP archive using `extract_video()` from `utils.py`. The function parses `ppt/slides/_rels/slideN.xml.rels` to find the video relationship, then extracts the media file to the images directory. The converter renders a `<video controls>` tag with a poster image (PNG export of the video shape) and `object-fit: contain`. If extraction fails, the shape falls back to a static PNG thumbnail.
- **Rule 14 (Web Font Language Coverage)**: A Google font that renders fine in English can be missing the target language's glyphs — Molengo, for example, ships only `latin`/`latin-ext`, so Vietnamese tone marks (U+1EA0-1EF9) fall back per-glyph and the text visibly breaks apart. `build_font_map()` in `utils.py` probes each font's css2 stylesheet for a `/* vietnamese */` block and swaps the ones that lack it for the closest family that has it (`FONT_SUBSTITUTES`). Pick a substitute by **measured advance width**, not by eye: a wider face re-wraps every line and destroys the author's layout (Molengo -> Source Sans 3 at 0.97x, not Be Vietnam Pro at 1.14x). When the probe cannot reach the network it returns `None` and the original font is kept.
- **Rule 15 (Font Weight Axes)**: `get_google_font_url()` must request real bold/italic cuts (`:ital,wght@0,400;0,700;1,400;1,700`), otherwise the browser synthesises them and bold text looks smeared. Google silently drops axes a family does not have, so the same suffix is safe for static fonts.
- **Rule 16 (Paragraph Metrics)**: Two PowerPoint metrics must be carried across or paragraphs collapse together. (a) `SpaceBefore`/`SpaceAfter` become the `<p>` margins — `LineRuleBefore/After == -1` means the value is in lines (`em`), otherwise points (`px`). (b) PowerPoint's "single" line spacing is the font's own line box, roughly **1.2x**, not `1.0` — emit `line_height * 1.2` when `LineRuleWithin == -1`.
- **Rule 17 (Merged Table Cells)**: COM's `Cell` object exposes no rowspan/colspan, and iterating the raw grid duplicates a merged cell's text in every row it covers. Detect merges geometrically instead: every cell of a merged block reports the **same anchor `Shape.Left`/`Shape.Top`**, so `build_merge_map()` in `utils.py` treats a repeated origin as a continuation, emits `rowspan`/`colspan` on the anchor, and skips the rest.

## Known limitations
- Slides hidden in PowerPoint (`Slide.SlideShowTransition.Hidden`) are **not** skipped — the converter walks `1..Slides.Count` and exports every one of them. Check the source deck for hidden slides before converting, or they will appear in the HTML.
- An HTML table row cannot be shorter than its content, so a table whose text is a hair taller than PowerPoint's row height grows by a few pixels (~2% on a full-height table) and can nudge the shape below it. Nothing is lost; it only shifts.
- `applyAutoFit()` measures `scrollHeight` against `clientHeight`, but every slide except the first is `display: none` at load time and therefore measures 0 — so autofit only ever runs on slide 1. This is deliberate for now: forcing it to run on every slide shrinks dense slides to the 8px floor, which is far less readable than PowerPoint's own behaviour of letting text spill past its box. Decks whose text overflows in PowerPoint will overflow in the HTML the same way.
