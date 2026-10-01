---
name: pdf-to-html-ocr
description: Convert scanned or photographed worksheet PDFs into faithful, responsive CMath HTML while preserving source diagrams and other instructional visuals.
---

# PDF Worksheet to Responsive HTML

Use this skill for scanned PDFs or page images. It is optimized for this repository's vertical worksheets, not fixed 16:9 slide decks.

## Source preparation

1. Identify the input PDF, date, lesson topic, and whether it is NDBH or BTVN.
2. Check whether PyMuPDF is available before installing anything.
3. Register reusable inputs in `scripts/extract_pdf.py`.
4. Render every page at 3× into:
   - `outputdata/<DDMMYYYY>/images_ndbh_<date>/`, or
   - `outputdata/<DDMMYYYY>/images_btvn_<date>/`.

Reuse `extract_pdf()`; do not create another extractor unless the source needs different processing.

## OCR and content modeling

Inspect every rendered page with the image viewer. For each page:

- Count the visible regions: header, exercise blocks, tables/diagrams, and footer.
- Build a visual inventory before writing HTML. Record every non-decorative image,
  diagram, chart, number puzzle, and visual referenced by wording such as
  "hình bên" or "trong hình".
- Transcribe printed wording exactly and in reading order. Do not summarize or paraphrase.
- Treat clear handwriting as answer data, not as printed question text.
- Verify mathematical answers independently when practical.
- If the printed source is internally inconsistent, preserve the conflicting wording and add a concise **Lưu ý từ bản gốc**. Do not silently rewrite it.

### Preserve source visuals

Keep original instructional visuals by default. Do not omit, describe in text
only, or redraw a source visual merely because its surrounding question has
been transcribed.

- Reuse the original embedded raster asset when it contains the complete visual.
- PDF vector artwork and compound visuals may not appear in the embedded-image
  list. Crop those regions from a high-resolution page render with
  `extract_pdf_region()` in `scripts/extract_pdf.py`; do not use a screenshot
  from a browser or manually redraw them.
- Crop only surrounding whitespace or page furniture. Keep all labels, marks,
  colors, proportions, and visual clues that affect the exercise.
- Reconstruct a visual as semantic HTML/CSS only when the user requests it, the
  source is unreadable, or faithful responsive use is impossible. Preserve the
  original crop as the reference when reconstruction is necessary.
- Place each visual beside the exact prompt it belongs to and outside protected
  answer markup so it remains visible in locked and question-only modes.
- Use responsive image styling (`max-width: 100%; height: auto`) and useful alt
  text that identifies the visual without revealing the answer.
- Decorative rules, logos, and repeated page furniture may be omitted.

Before moving on from a page, explicitly reconcile the visual inventory with
the generated HTML. Any prompt that references a figure must have a matching
visible asset.

Create one data-driven content module such as `scripts/content_12_btvn.py`. Reuse helpers from `scripts/generate_v2.py`:

- `hdr()` and `foot()` for one `.page-card` per source page.
- `A()` and `Ablk()` for protected answers.
- `gen_theory()`, `gen_debai()`, or `gen_btvn()` for the required access mode.

Do not duplicate the full HTML shell or shared CSS inside each content module.

## Responsive and navigation requirements

- Output to `outputdata/<DDMMYYYY>/<class>_<type>_<date>.html`.
- Inherit `styles/shared.css`; preserve font smoothing and the fluid 17–19px root scale.
- Grids collapse to one column on narrow screens.
- Wide tables scroll horizontally inside the table area.
- Controls have touch-friendly sizing.
- Every page includes the generator-provided `../../index.html` **Back to Main Menu** link.
- Print mode hides navigation and preserves readable worksheet layout.

Update `index.html` in the same change:

- Add the lesson card to the correct date group.
- Ensure that date group has a visible `session-topic` outside the card grid.
- Keep all card targets valid.

## QA

Before delivery:

1. Confirm extracted image count equals PDF page count.
2. Confirm generated `.page-card` count equals PDF page count.
3. Check a list of distinctive sentences from every page against the generated HTML.
4. Confirm every visual-inventory item has a matching `<img>` or justified
   semantic reconstruction, and verify every local image path exists.
5. Confirm answer and blank markup exists where expected.
6. Confirm all Main Menu card targets exist and the lesson's back link resolves.
7. Render the lesson and Main Menu at a desktop width and a narrow width (about 500px); inspect images for clipping, distortion, missing labels, and unreadable text.
8. Run `git diff --check`.
9. Remove temporary screenshots/profiles; keep the extracted OCR page images and
   the source visual assets used by the HTML.

Return clickable links to the root Main Menu and the generated lesson.

## Conditional reference

Read `examples/manual_results.html` only when the source is genuinely slide-like and requires a fixed 16:9 container or complex chart reconstruction. Ordinary worksheets do not need this large example.
