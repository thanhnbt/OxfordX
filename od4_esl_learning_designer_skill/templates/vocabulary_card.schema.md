# Vocabulary Card Schema

Required fields:

```json
{
  "word": "astronomer",
  "pos": "n",
  "ipa": "/əˈstrɑːnəmɚ/",
  "sound_out": "uh-STRAH-nuh-mer",
  "english_meaning": "a scientist who studies stars, planets, and space",
  "vietnamese_support": "nhà thiên văn học",
  "visual": {
    "type": "image|diagram|illustration|symbol",
    "asset": "assets/images/astronomer.webp",
    "alt": "an astronomer looking through a telescope"
  },
  "concept_cluster": "People who study space",
  "map_connection": ["astronomer", "uses", "telescope"],
  "example": "An astronomer studies space.",
  "source_label": "CORE-BOOK"
}
```

For source-book review, additionally record `id`, `source_pdf_page` (one-based), `student_book_page` and `visual_role`. Store image extraction metadata in a separate manifest keyed by visual ID: source file, PDF/printed guide/Student Book pages, bbox in PDF points with coordinate convention, extraction method, asset path, visual role and review status. Authored support diagrams must have no invented book crop coordinates. See [review-workflow.md](../references/review-workflow.md).
