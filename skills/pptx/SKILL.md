---
name: pptx
description: |
  Create professional PowerPoint (.pptx) presentations using pptxgenjs (JavaScript).

  Triggers when user mentions:
  - "make a ppt" or "create a presentation"
  - "slide deck" or "pitch deck"
  - ".pptx file"
author: Jansen Lin
license: MIT
---

# PPTX Skill

Create professional PowerPoint presentations using **pptxgenjs** in the OpenWork environment.

---

## Environment Prerequisites (CRITICAL)

OpenWork runs a **non-interactive shell** that does NOT load `~/.zshrc`. Global npm packages are installed but `NODE_PATH` is not set. **You MUST prefix every `node` command with `NODE_PATH`:**

```bash
NODE_PATH=$(npm root -g) node script.js
```

Without this prefix, `require('pptxgenjs')` will fail with `MODULE_NOT_FOUND`.

### Verify Setup

```bash
# Check pptxgenjs is installed globally
npm list -g pptxgenjs

# Test it can be loaded
NODE_PATH=$(npm root -g) node -e "const p = require('pptxgenjs'); console.log('pptxgenjs OK')"
```

If not installed, run: `npm install -g pptxgenjs`

### Additional Dependencies (optional)

```bash
npm install -g react-icons react react-dom sharp   # For icons
pip install "markitdown[pptx]"                      # For reading existing .pptx
pip install Pillow                                  # For thumbnails
```

---

## Quick Start

Write a `.js` script, then execute with `NODE_PATH`:

```bash
NODE_PATH=$(npm root -g) node generate_ppt.js
```

### Minimal Example

```javascript
const pptxgen = require("pptxgenjs");

let pres = new pptxgen();
pres.layout = "LAYOUT_16x9";
pres.author = "Jansen";

let slide = pres.addSlide();
slide.background = { color: "1E2761" };
slide.addText("Hello World", {
  x: 1, y: 2, w: 8, h: 1.5,
  fontSize: 44, fontFace: "Arial",
  color: "FFFFFF", bold: true, align: "center"
});

pres.writeFile({ fileName: "output.pptx" });
```

---

## Layout Dimensions

| Layout | Width | Height |
|--------|-------|--------|
| `LAYOUT_16x9` | 10" | 5.625" (default) |
| `LAYOUT_16x10` | 10" | 6.25" |
| `LAYOUT_4x3` | 10" | 7.5" |
| `LAYOUT_WIDE` | 13.3" | 7.5" |

---

## Design Guidelines

### Before Starting

- **Pick a bold, content-informed color palette**: The palette should feel designed for THIS topic.
- **Dominance over equality**: One color should dominate (60-70%), with 1-2 supporting tones and one accent.
- **Dark/light contrast**: Dark backgrounds for title + conclusion slides, light for content.
- **Commit to a visual motif**: Pick ONE distinctive element and repeat it across every slide.

### Color Palettes

| Theme | Primary | Secondary | Accent |
|-------|---------|-----------|--------|
| **Midnight Executive** | `1E2761` (navy) | `CADCFC` (ice blue) | `FFFFFF` (white) |
| **Forest & Moss** | `2C5F2D` (forest) | `97BC62` (moss) | `F5F5F5` (cream) |
| **Coral Energy** | `F96167` (coral) | `F9E795` (gold) | `2F3C7E` (navy) |
| **Warm Terracotta** | `B85042` (terracotta) | `E7E8D1` (sand) | `A7BEAE` (sage) |
| **Ocean Gradient** | `065A82` (deep blue) | `1C7293` (teal) | `21295C` (midnight) |
| **Charcoal Minimal** | `36454F` (charcoal) | `F2F2F2` (off-white) | `212121` (black) |
| **Teal Trust** | `028090` (teal) | `00A896` (seafoam) | `02C39A` (mint) |
| **Berry & Cream** | `6D2E46` (berry) | `A26769` (dusty rose) | `ECE2D0` (cream) |
| **Cherry Bold** | `990011` (cherry) | `FCF6F5` (off-white) | `2F3C7E` (navy) |

### Typography

| Header Font | Body Font |
|-------------|-----------|
| Georgia | Calibri |
| Arial Black | Arial |
| Calibri | Calibri Light |
| Trebuchet MS | Calibri |
| Palatino | Garamond |

| Element | Size |
|---------|------|
| Slide title | 36-44pt bold |
| Section header | 20-24pt bold |
| Body text | 14-16pt |
| Captions | 10-12pt muted |

### Spacing

- 0.5" minimum margins from slide edges
- 0.3-0.5" between content blocks
- Leave breathing room — don't fill every inch

### For Each Slide

**Every slide needs a visual element** — image, chart, icon, or shape. Text-only slides are forgettable.

**Layout options:**
- Two-column (text left, visual right)
- Icon + text rows (icon in colored circle, bold header, description below)
- 2x2 or 2x3 grid
- Half-bleed image with content overlay
- Large stat callouts (big numbers 60-72pt with small labels below)
- Timeline or process flow (numbered steps, arrows)

### Avoid (Common Mistakes)

- **Don't repeat the same layout** — vary columns, cards, and callouts across slides
- **Don't center body text** — left-align paragraphs and lists; center only titles
- **Don't default to blue** — pick colors that reflect the specific topic
- **Don't create text-only slides** — add images, icons, charts, or visual elements
- **NEVER use "#" with hex colors** — causes file corruption (`"FF0000"` not `"#FF0000"`)
- **NEVER use accent lines under titles** — hallmark of AI-generated slides
- **NEVER use unicode bullets "•"** — use `bullet: true` instead (unicode creates double bullets)

---

## API Reference

### Text

```javascript
// Basic text
slide.addText("Title", {
  x: 1, y: 1, w: 8, h: 2,
  fontSize: 24, fontFace: "Arial",
  color: "363636", bold: true, align: "center", valign: "middle"
});

// Rich text arrays
slide.addText([
  { text: "Bold ", options: { bold: true } },
  { text: "Italic ", options: { italic: true } }
], { x: 1, y: 3, w: 8, h: 1 });

// Multi-line (requires breakLine: true)
slide.addText([
  { text: "Line 1", options: { breakLine: true } },
  { text: "Line 2", options: { breakLine: true } },
  { text: "Line 3" }
], { x: 0.5, y: 0.5, w: 8, h: 2 });

// Character spacing (NOT letterSpacing)
slide.addText("SPACED TEXT", { x: 1, y: 1, w: 8, h: 1, charSpacing: 6 });
```

### Lists & Bullets

```javascript
// Correct: multiple bullets
slide.addText([
  { text: "First item", options: { bullet: true, breakLine: true } },
  { text: "Second item", options: { bullet: true, breakLine: true } },
  { text: "Third item", options: { bullet: true } }
], { x: 0.5, y: 0.5, w: 8, h: 3 });

// Numbered list
{ text: "First", options: { bullet: { type: "number" }, breakLine: true } }

// Sub-items
{ text: "Sub-item", options: { bullet: true, indentLevel: 1 } }
```

### Shapes

```javascript
slide.addShape(pres.shapes.RECTANGLE, {
  x: 0.5, y: 0.8, w: 1.5, h: 3.0,
  fill: { color: "FF0000" },
  line: { color: "000000", width: 2 }
});

// With shadow (NEVER use negative offset, NEVER encode opacity in color string)
slide.addShape(pres.shapes.RECTANGLE, {
  x: 1, y: 1, w: 3, h: 2,
  fill: { color: "FFFFFF" },
  shadow: { type: "outer", color: "000000", blur: 6, offset: 2, angle: 135, opacity: 0.15 }
});

// With transparency
slide.addShape(pres.shapes.RECTANGLE, {
  x: 1, y: 1, w: 3, h: 2,
  fill: { color: "0088CC", transparency: 50 }
});
```

### Images

```javascript
// From file
slide.addImage({ path: "images/photo.png", x: 1, y: 1, w: 5, h: 3 });

// From base64
slide.addImage({ data: "image/png;base64,iVBORw0KGgo...", x: 1, y: 1, w: 5, h: 3 });

// Sizing modes
{ sizing: { type: "contain", w: 4, h: 3 } }  // fit inside
{ sizing: { type: "cover", w: 4, h: 3 } }    // fill area (may crop)
```

### Charts

```javascript
// Bar chart
slide.addChart(pres.charts.BAR, [{
  name: "Sales", labels: ["Q1", "Q2", "Q3", "Q4"], values: [4500, 5500, 6200, 7100]
}], {
  x: 0.5, y: 0.6, w: 6, h: 3, barDir: "col",
  chartColors: ["0D9488", "14B8A6", "5EEAD4"],
  showValue: true, dataLabelPosition: "outEnd",
  valGridLine: { color: "E2E8F0", size: 0.5 },
  catGridLine: { style: "none" },
  showLegend: false
});

// Pie chart
slide.addChart(pres.charts.PIE, [{
  name: "Share", labels: ["A", "B", "Other"], values: [35, 45, 20]
}], { x: 7, y: 1, w: 5, h: 4, showPercent: true });

// Line chart
slide.addChart(pres.charts.LINE, [{
  name: "Trend", labels: ["Jan", "Feb", "Mar"], values: [32, 35, 42]
}], { x: 0.5, y: 4, w: 6, h: 3, lineSize: 3, lineSmooth: true });
```

### Tables

```javascript
slide.addTable([
  [
    { text: "Header 1", options: { fill: { color: "6699CC" }, color: "FFFFFF", bold: true } },
    { text: "Header 2", options: { fill: { color: "6699CC" }, color: "FFFFFF", bold: true } }
  ],
  ["Cell 1", "Cell 2"]
], {
  x: 1, y: 1, w: 8, h: 2,
  border: { pt: 1, color: "999999" },
  colW: [4, 4]
});
```

### Backgrounds

```javascript
slide.background = { color: "F1F1F1" };                          // Solid color
slide.background = { path: "https://example.com/bg.jpg" };       // Image URL
slide.background = { data: "image/png;base64,iVBORw0KGgo..." };  // Base64
```

### Icons (react-icons)

```javascript
const React = require("react");
const ReactDOMServer = require("react-dom/server");
const sharp = require("sharp");
const { FaCheckCircle } = require("react-icons/fa");

function renderIconSvg(IconComponent, color = "#000000", size = 256) {
  return ReactDOMServer.renderToStaticMarkup(
    React.createElement(IconComponent, { color, size: String(size) })
  );
}

async function iconToBase64Png(IconComponent, color, size = 256) {
  const svg = renderIconSvg(IconComponent, color, size);
  const pngBuffer = await sharp(Buffer.from(svg)).png().toBuffer();
  return "image/png;base64," + pngBuffer.toString("base64");
}

// Usage
const iconData = await iconToBase64Png(FaCheckCircle, "#4472C4", 256);
slide.addImage({ data: iconData, x: 1, y: 1, w: 0.5, h: 0.5 });
```

---

## Common Pitfalls (CRITICAL)

1. **NEVER use "#" in hex colors** — `"FF0000"` not `"#FF0000"` (corrupts file)
2. **NEVER encode opacity in hex color** — `"00000020"` corrupts file; use `opacity: 0.12` instead
3. **NEVER use unicode bullets "•"** — use `bullet: true` (unicode creates double bullets)
4. **NEVER reuse option objects** — pptxgenjs mutates them in-place; use factory functions:
   ```javascript
   // WRONG
   const shadow = { type: "outer", blur: 6, offset: 2, color: "000000", opacity: 0.15 };
   slide.addShape(pres.shapes.RECTANGLE, { shadow, ... });
   slide.addShape(pres.shapes.RECTANGLE, { shadow, ... }); // corrupted!

   // CORRECT
   const makeShadow = () => ({ type: "outer", blur: 6, offset: 2, color: "000000", opacity: 0.15 });
   slide.addShape(pres.shapes.RECTANGLE, { shadow: makeShadow(), ... });
   slide.addShape(pres.shapes.RECTANGLE, { shadow: makeShadow(), ... });
   ```
5. **NEVER use negative shadow offset** — corrupts file; use `angle: 270` for upward shadows
6. **Use `breakLine: true`** between text array items, or they run together
7. **Avoid `lineSpacing` with bullets** — use `paraSpaceAfter` instead
8. **Each presentation needs a fresh `new pptxgen()` instance** — don't reuse
9. **Don't use `ROUNDED_RECTANGLE` with accent borders** — rectangular overlays won't cover rounded corners; use `RECTANGLE`
10. **Set `margin: 0`** on text boxes when aligning text precisely with shapes or icons

---

## Workflow

### Creating from Scratch

1. Plan slide structure and content
2. Choose color palette and typography
3. Write a `.js` script using pptxgenjs API
4. Execute: `NODE_PATH=$(npm root -g) node generate_ppt.js`
5. QA: Review the output file

### Reading Existing .pptx

```bash
python -m markitdown presentation.pptx
```

---

## Output

Generated `.pptx` files are compatible with:
- Microsoft PowerPoint
- Apple Keynote
- LibreOffice Impress
- Google Slides (via import)
