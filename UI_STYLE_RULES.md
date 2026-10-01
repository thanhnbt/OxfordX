# Shared UI rules

Use the following hierarchy throughout this project:

- Unit title: 25?32px, weight 750, dark navy. Supporting subtitle: 17?21px, regular, muted blue-gray.
- Activity title: 25?30px, weight 700. Section heading: 21?27px, weight 650?700.
- Learning prose: 16?18px, line height 1.5?1.6. Preserve the larger vocabulary word and sentence examples.
- Activity navigation: 15px, weight 550, neutral blue-gray. Selected item: weight 700, pale blue background, left marker. Grammar uses the same navigation style.
- Labels: 11?13px; helper text: 14?16px. Avoid faint text for information the learner needs.
- Keep subject, grammar marker, base verb and if-clause colors semantic; do not replace them with general navigation colors.
- Use compact, consistent 12?20px spacing. Fill the available workspace; do not center narrow quiz content inside it.
- Keep all 11 vocabulary words together, with image left and word/audio, IPA, sound-out stacked right.
- On mobile retain readable text and touch targets of at least 44px. Allow text to wrap rather than shrinking it to fit.
- Apply visual changes to maintained source files in web/, rebuild index.html and run the relevant QA scripts. Keep print styles separate.

Current whole-project verification: 276 data, 108 regression, 71 bilingual/grammar, 74 concept-map and 18 vocabulary layout checks. See qa/QA_V2_REPORT.md.
