from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import landscape, letter
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas


OUT = Path(__file__).parent / "output" / "pdf"
OUT.mkdir(parents=True, exist_ok=True)
PDF = OUT / "AnalogAtlas_Architecture_and_Features.pdf"
W, H = landscape(letter)

NAVY = colors.HexColor("#10243A")
BLUE = colors.HexColor("#22577A")
TEAL = colors.HexColor("#178F8A")
GOLD = colors.HexColor("#D99A2B")
INK = colors.HexColor("#243447")
MUTED = colors.HexColor("#5C6B78")
PALE = colors.HexColor("#F2F6F8")
PALE_BLUE = colors.HexColor("#E8F1F6")
PALE_TEAL = colors.HexColor("#E7F4F1")
PALE_GOLD = colors.HexColor("#FAF2E2")
WHITE = colors.white


def wrap(text, font, size, width):
    words = text.split()
    lines, line = [], ""
    for word in words:
        test = word if not line else line + " " + word
        if stringWidth(test, font, size) <= width:
            line = test
        else:
            if line:
                lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


def header(c, title, subtitle, page):
    c.setFillColor(NAVY)
    c.rect(0, H - 62, W, 62, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 19)
    c.drawString(28, H - 31, title)
    c.setFont("Helvetica", 9)
    c.setFillColor(colors.HexColor("#DCE7EF"))
    c.drawString(29, H - 48, subtitle)
    c.setFillColor(MUTED)
    c.setFont("Helvetica", 8)
    c.drawRightString(W - 28, 17, f"ANALOGATLAS  |  V1.1  |  {page}/3")
    c.setStrokeColor(colors.HexColor("#D8E0E5"))
    c.line(28, 28, W - 28, 28)


def section_label(c, x, y, text, color=BLUE):
    c.setFillColor(color)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(x, y, text.upper())


def card(c, x, y, w, h, title, body, fill=PALE, accent=BLUE, title_size=10, body_size=8.1):
    c.setFillColor(fill)
    c.setStrokeColor(colors.HexColor("#D6E0E6"))
    c.setLineWidth(0.7)
    c.roundRect(x, y, w, h, 7, fill=1, stroke=1)
    c.setFillColor(accent)
    c.roundRect(x, y, 4, h, 2, fill=1, stroke=0)
    tx = x + 12
    ty = y + h - 17
    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", title_size)
    c.drawString(tx, ty, title)
    c.setFillColor(INK)
    c.setFont("Helvetica", body_size)
    for i, line in enumerate(wrap(body, "Helvetica", body_size, w - 24)[:5]):
        c.drawString(tx, ty - 13 - i * 10, line)


def arrow(c, x1, y1, x2, y2, color=TEAL, label=None):
    c.setStrokeColor(color)
    c.setFillColor(color)
    c.setLineWidth(1.5)
    c.line(x1, y1, x2, y2)
    import math
    ang = math.atan2(y2 - y1, x2 - x1)
    size = 6
    left = (x2 - size * math.cos(ang - 0.45), y2 - size * math.sin(ang - 0.45))
    right = (x2 - size * math.cos(ang + 0.45), y2 - size * math.sin(ang + 0.45))
    p = c.beginPath()
    p.moveTo(x2, y2)
    p.lineTo(*left)
    p.lineTo(*right)
    p.close()
    c.drawPath(p, fill=1, stroke=0)
    if label:
        c.setFont("Helvetica", 7.2)
        c.setFillColor(MUTED)
        c.drawCentredString((x1 + x2) / 2, (y1 + y2) / 2 + 5, label)


def pill(c, x, y, w, text, fill=PALE_TEAL, fg=TEAL):
    c.setFillColor(fill)
    c.roundRect(x, y, w, 18, 9, fill=1, stroke=0)
    c.setFillColor(fg)
    c.setFont("Helvetica-Bold", 7.5)
    c.drawCentredString(x + w / 2, y + 5.5, text)


def page_one(c):
    header(c, "AnalogAtlas | System Architecture", "A reproducible science build feeds a small, static application that works offline.", 1)
    ytop = H - 91
    cols = [(28, 205, "LOCAL INPUTS", BLUE), (293, 205, "PYTHON SCIENCE BUILD", TEAL), (558, 205, "PRODUCT OUTPUT", GOLD)]
    for x, _, label, col in cols:
        section_label(c, x, ytop, label, col)

    boxes = [
        [("Earth terrain", "GEBCO_2026 15-arcsec grid, or a documented official replacement."),
         ("Moon terrain", "LOLA polar DEM candidate; verify labels, posting and target coverage."),
         ("Mars terrain", "MOLA MEGDR 128 pixels/degree for the Jezero reference."),
         ("Frozen configuration", "Targets, bounds, grid origin, gates, methods and source versions."),
         ("Site registry", "Cited analog examples and contrast controls, kept out of calibration.")],
        [("1. Normalize inputs", "Adapters provide elevation, valid-data mask, units and source lineage."),
         ("2. Project", "Local metric Lambert azimuthal equal-area; body-specific planetary radii."),
         ("3. Common grid", "Area-weighted elevation resampling to 500 m square cells."),
         ("4. Terrain", "Horn 3x3 slope; 1 km derivative baseline; 1.5 km stencil footprint."),
         ("5. Support features", "Four summaries on fixed 16 x 16 km (256 km2) supports."),
         ("6. Compare and validate", "Discovery-only IQR tolerances; deterministic score; held-out validation after freeze.")],
        [("Science tables", "Parquet support features, scores and exclusion reasons."),
         ("Compact app data", "Local JSON / GeoJSON for targets, top candidates, registry and validation."),
         ("Run provenance", "Source versions, config checksum, methods, caveats and run ID."),
         ("Static web app", "React + Vite + MapLibre with local Natural Earth vectors."),
         ("Offline experience", "Target selector, ranked map/list, candidate detail and datasheet.")],
    ]
    xcols = [28, 293, 558]
    widths = [205, 205, 205]
    heights = [65, 54, 54, 54, 54, 54]
    for col_idx, entries in enumerate(boxes):
        x, w = xcols[col_idx], widths[col_idx]
        y = ytop - 24
        for i, (title, body) in enumerate(entries):
            h = heights[i]
            fill = PALE_BLUE if col_idx == 0 else PALE_TEAL if col_idx == 1 else PALE_GOLD
            accent = BLUE if col_idx == 0 else TEAL if col_idx == 1 else GOLD
            card(c, x, y - h, w, h, title, body, fill, accent, title_size=9, body_size=7.6)
            y -= h + 7
    arrow(c, 242, 350, 286, 350, BLUE)
    arrow(c, 507, 350, 551, 350, TEAL)
    c.setFillColor(MUTED)
    c.setFont("Helvetica-Oblique", 8)
    c.drawCentredString(W / 2, 53, "No backend, hosted tiles, cloud processing, paid service or LLM is required at runtime.")
    c.showPage()


def page_two(c):
    header(c, "Science Engine | Scale, Features and Score", "All bodies use the same declared support geometry and interpretable terrain summaries.", 2)
    section_label(c, 28, H - 91, "PROCESSING SCALE", BLUE)
    steps = [
        (28, "DEM + mask", "Source elevations, nodata and lineage"),
        (182, "Metric LAEA", "Local equal-area projection"),
        (336, "500 m grid", "Area-weighted resampling"),
        (490, "Horn slope", "3x3; 1 km baseline"),
        (644, "16 km support", "32 x 32 cells = 256 km2"),
    ]
    for x, title, body in steps:
        card(c, x, 391, 126, 62, title, body, PALE_BLUE, BLUE, 9.2, 7.7)
    for (x, _, _), (nx, _, _) in zip(steps, steps[1:]):
        arrow(c, x + 128, 422, nx - 3, 422, TEAL)

    section_label(c, 28, 355, "FOUR FEATURES - TWO EQUALLY WEIGHTED FAMILIES", TEAL)
    card(c, 28, 227, 230, 111, "Slope distribution | family weight 0.50",
         "Median slope: typical inclination (degrees).\nSlope P90: upper-tail steepness (degrees).\nEach feature weight: 0.25 overall.", PALE_TEAL, TEAL, 10, 8.2)
    card(c, 28, 145, 230, 67, "Terrain variability | family weight 0.50",
         "Relief P95-P5 (metres) + population slope SD (degrees). Each feature weight: 0.25 overall.", PALE_GOLD, GOLD, 9.5, 8)

    card(c, 282, 264, 225, 74, "Target vector",
         "One fixed 16 x 16 km reference support per body: Connecting Ridge reference and Jezero landing neighborhood.", PALE_BLUE, BLUE, 10, 8)
    card(c, 282, 180, 225, 70, "Tolerance, frozen before validation",
         "For each feature: delta = 0.25 x mean of the three window-specific Earth IQRs. Same alpha for all features.", PALE_TEAL, TEAL, 9.5, 7.8)
    card(c, 282, 100, 225, 65, "No target heterogeneity estimate",
         "One support gives n=1. Spatial heterogeneity is not estimated or treated as zero; it is omitted.", PALE, BLUE, 9.2, 7.7)

    card(c, 532, 275, 230, 95, "Per-feature agreement",
         "a = 1 - min(1, |candidate value - target value| / delta).\nClamp each feature agreement to [0, 1].", PALE_TEAL, TEAL, 10, 8.2)
    card(c, 532, 168, 230, 93, "Terrain Morphology Agreement",
         "Score = 100 x sum(feature weight x agreement).\nA 0-100 index; not probability, safety, or mission suitability.", PALE_GOLD, GOLD, 9.6, 8.1)
    card(c, 532, 82, 230, 73, "Eligibility and missing data",
         "Require >=90% valid cells and all four features. Otherwise exclude with a reason; never renormalize around missing features.", PALE, BLUE, 9.2, 7.6)

    arrow(c, 508, 302, 525, 315)
    arrow(c, 508, 215, 532, 285)
    arrow(c, 647, 270, 647, 265)
    c.setFillColor(MUTED)
    c.setFont("Helvetica-Oblique", 7.8)
    c.drawString(28, 67, "IQR and alpha are normalization heuristics. Correlation is audited before validation; no post-validation tuning or PCA scoring.")
    c.showPage()


def page_three(c):
    header(c, "Product | Validation and Team Build", "What users inspect, what stays held out, and how the four-person team assembles the demo.", 3)
    section_label(c, 28, H - 91, "OFFLINE APPLICATION", BLUE)
    ux = [
        (28, 419, "Select reference", "Moon or Mars; show the fixed support and source."),
        (28, 345, "Explore candidates", "Ranked map and list across three bounded Earth discovery windows."),
        (28, 271, "Inspect datasheet", "Four feature values, units, score contributions, coverage and lineage."),
        (28, 197, "Assess evidence", "Evidence Quality is separate: coverage, source lineage and sensitivity."),
        (28, 123, "Read limitations", "Scale, run provenance, sources, caveats and explicit non-claims."),
    ]
    for x, y, title, body in ux:
        card(c, x, y, 230, 61, title, body, PALE_BLUE, BLUE, 9.5, 7.7)

    section_label(c, 292, H - 91, "DISCOVERY AND VALIDATION ARE SEPARATE", TEAL)
    card(c, 292, 384, 210, 91, "Discovery windows",
         "East African Rift / Afar; Namib; Ladakh / western Himalaya. Used only to estimate Earth IQRs and rank candidates.", PALE_TEAL, TEAL, 9.5, 7.9)
    card(c, 292, 276, 210, 91, "Held-out site examples",
         "Atacama / Yungay; Haughton Crater; Death Valley. Scored only after scientific freeze; site-target relevance is reviewed.", PALE_GOLD, GOLD, 9.5, 7.9)
    card(c, 292, 168, 210, 91, "Contrast controls + report",
         "Preselected controls are not true negatives. Show descriptive ranks, failures and limits; no ROC-AUC or predictive claim.", PALE, BLUE, 9.5, 7.9)
    arrow(c, 398, 380, 398, 371, TEAL, "freeze first")

    section_label(c, 532, H - 91, "TEAM OF FOUR", GOLD)
    roles = [
        ("Science / data", "Sources, licenses, windows, targets and site labels."),
        ("Geospatial", "Adapters, projection, common grid, masks and feature build."),
        ("Scoring / validation", "Freeze, tolerance, deterministic score, controls and report."),
        ("Frontend / demo", "Offline map, ranking, detail, datasheet and presentation."),
    ]
    y = 418
    for title, body in roles:
        card(c, 532, y, 230, 62, title, body, PALE_GOLD, GOLD, 9.2, 7.7)
        y -= 73

    c.setFillColor(NAVY)
    c.roundRect(28, 43, W - 56, 48, 8, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(42, 72, "48-hour sequence")
    c.setFont("Helvetica", 8)
    c.drawString(42, 57, "Rules + schemas  >  vertical slice  >  all windows/targets  >  freeze  >  rank  >  validate  >  offline QA  >  demo")
    c.showPage()


def main():
    c = canvas.Canvas(str(PDF), pagesize=landscape(letter), pageCompression=1)
    c.setTitle("AnalogAtlas Architecture and Features")
    c.setAuthor("AnalogAtlas project team")
    c.setSubject("Printable architecture, science pipeline, scoring and application overview")
    page_one(c)
    page_two(c)
    page_three(c)
    c.save()
    print(PDF)


if __name__ == "__main__":
    main()
