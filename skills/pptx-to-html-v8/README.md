# PPTX to Native HTML Converter (V8 Engine)

This project provides a highly accurate, standalone CLI tool for converting Microsoft PowerPoint (.pptx) files into interactive, native HTML/CSS web presentations. 

Unlike standard converters that export static images of slides, this tool leverages Windows COM automation (`win32com`) to parse the internal presentation DOM and reconstruct complex geometries natively.

## Key Features
- **Native Typography & Geometry:** Extracts font family, font size, bold/italic formatting, and absolute positions to reconstruct text natively in CSS.
- **V8 Table Engine:** Tables are fully parsed into HTML `<table>`, `<tr>`, `<td>` elements with pixel-perfect borders, cell padding, and background fills. No blurry PNG fallbacks for grids!
- **CSS Shapes & Borders:** AutoShapes (Rectangles, Ovals, Rounded Rects) are rendered natively using CSS `border-radius`, `background-color`, and exact `border` properties.
- **Smart Autofit:** Injects JavaScript logic to gracefully scale text down if it exceeds its bounding box, mimicking PowerPoint's "Shrink Text on Overflow" behavior.
- **Responsive Scaling:** The generated HTML presentation automatically scales to fit the viewer's browser window while maintaining the original PPTX aspect ratio.

## Prerequisites

### 1. System Requirements
- **OS:** Windows Only (Required for COM automation).
- **Software:** Microsoft PowerPoint must be installed locally and activated.

### 2. Python Environment (Core Engine)
- Install **Python 3.8+** (Make sure to add it to PATH during installation).

### 3. Node.js Environment (Optional - For QA/VRT)
- Install **Node.js** (v14+) if you intend to run the Playwright Visual Regression Tests.

---

## Installation

### Core Tool Setup
1. Clone this repository.
2. Open a terminal in the repository folder.
3. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```
   *(This will install `pywin32`, `python-pptx`, and `beautifulsoup4`)*

### QA Testing Setup (Optional)
If you want to run the automated Playwright testing pipeline:
1. Navigate to the `qa` folder:
   ```bash
   cd qa
   ```
2. Install Node dependencies and the Playwright browsers:
   ```bash
   npm install
   npx playwright install chromium
   ```

---

## Usage

### 1. Converting a PPTX to HTML
Run the core script via CLI from the root folder:

```bash
python scripts/pptx2html.py --input "path/to/your/presentation.pptx" --output "path/to/export/dir"
```

- `-i`, `--input`: The absolute or relative path to the PPTX file.
- `-o`, `--output`: The folder where the HTML file and associated images will be saved. (Defaults to `hybrid_export`).

**Example:**
```bash
python scripts/pptx2html.py -i "./sample.pptx" -o "./output"
```
This will generate `output/presentation.html` and a folder of background/fallback images at `output/images/`.

### 2. Running Visual Regression Testing (QA)
1. Ensure your HTML is generated into a folder (e.g., `hybrid_export/presentation.html`).
2. Run the snapshot script from the `qa` folder:
   ```bash
   cd qa
   node vrt_snapshots.js
   ```
This will open a headless Chromium browser, navigate to the generated presentation, and take high-fidelity screenshots for manual or automated comparison.

---

## AI Skill Integration (Antigravity)
This repository includes a `SKILL.md` file, making it a drop-in Skill for Antigravity AI agents.
Copy this folder into your `~/.gemini/config/skills/` directory. You can then ask the AI to "convert my PPTX to HTML" and it will automatically execute the CLI tool on your behalf.
