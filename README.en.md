# pdf-layout-translate 📄✨

<div align="center">

**[简体中文](README.md) | [English](README.en.md)**

</div>

**Translate any beautifully-formatted PDF / Word document into Chinese as-is — layout intact, charts in place, text selectable.**

A translation-craft skill for AI Agents: don't re-typeset, just swap the words.

---

## Why you need this

You've surely been here before:

> You find a beautifully-typeset English report/paper/white paper, feed it to a translation tool, and get back —
> charts displaced, tables collapsed, multi-column turned single-column, fonts resized. A 190-page book comes out with nothing left but "reference value."

Most document translators take the "extract text → re-typeset → output" route, which is guaranteed to destroy the layout.
This skill takes a different road: **original page as the base + text overlay translation** —

```
┌──────────────────────────────────────────────────┐
│  Original PDF (kept as-is: layout/charts/colors/ │
│  headers & footers)                              │
│  + Erase the text layer (redaction, graphics     │
│    untouched)                                    │
│  + Overlay Chinese at the same coordinates       │
│    (matching size/color/weight/alignment)        │
└──────────────────────────────────────────────────┘
```

The result: the finished document looks identical to the original — only the words are Chinese — and the text is still selectable, searchable, and copyable.

## Use cases

### 🎯 Where it's battle-tested: long-form professional research reports

This skill grew out of real-world jobs, and its most polished territory is **end-to-end Chinese localization of sell-side/investment-bank research**:

- **A 190-page Morgan Stanley blue book**: hundreds of charts, tables, and scatter plots delivered with zero layout shifts
- **The four Goldman Sachs 2027 reports** (Global Outlook / China Outlook / Macro Outlook / China Strategy): mixed vector and raster charts, with in-chart titles, legends, and axis labels patched in one by one

It has already waded through everything that makes research reports hard: dense charts, specialized terminology, strict number-reconciliation requirements, and 100+ pages needing resumable execution. If your material looks like a research report — many pages, many charts, typesetting that matters — use it directly. Every pit has been stepped in for you.

### ✅ Built-in support, ready to go

- **Word / DOCX documents** (.doc/.docx): in-place replacement; tables, headers/footers, text boxes, and text inside embedded images are all handled; delivered as PDF by default
- **Scanned PDFs** (no text layer): automatically downgrades to a Chinese side-by-side edition ("original page image + Chinese translation page") — no forced overlay

### 🌱 Scenarios you can extend into

The craft is general (original page as base + text overlay). As long as a document has "a text layer + layout worth keeping," it's worth a try:

- **Academic papers**: two-column layouts with mixed charts and formulas — exactly where re-typesetting translators fail hardest
- **Contracts / legal documents**: clause numbering, signature blocks, and table positions must not move; line-by-line correspondence with the original aids review
- **Product manuals / technical docs**: screenshot callouts, parameter tables, and warning boxes stay exactly in place
- **Financial reports / prospectuses**: number-dense documents — the number-reconciliation mechanism fits perfectly
- **White papers / industry reports**: same structure as research reports, directly applicable
- **Other target languages**: swap the Chinese font and character set (the handbook is written around Chinese localization; other languages need your own adjustments)

> Not a fit: plain-text excerpt translation, or any translation where layout doesn't matter — that's home turf for ordinary translation tools; don't use this heavy craft there.

## Track record

A 190-page English investment-bank blue book (hundreds of charts, tables, scatter plots) translated end to end:

- ✅ Zero layout/chart-position changes across the book; page-by-page pixel comparison passed
- ✅ Body text selectable and searchable
- ✅ With embedded Chinese fonts, shrunk from 400MB+ to **~13MB** (font subsetting)
- ✅ 31 complex chart blind spots (legends/axis labels/in-chart labels) patched one by one, verified with high-magnification renders
- ✅ Company names, index names, chemical formulas kept in English per agreed scope

## What's inside the skill

`SKILL.md` is a complete craft handbook you can feed directly to an Agent, including:

| Module | Content |
|---|---|
| Pre-flight checks | Text-layer vs. scanned-PDF detection; scanned versions auto-downgrade to a Chinese side-by-side edition, no forced overlay |
| Main pipeline | Four-part-key full-text index → block-wise translation → redaction erase → same-coordinate Chinese overlay |
| Font subsetting | Working pyftsubset commands; whole book from 400MB+ down to ~2MB |
| Line-by-line acceptance | Machine scanning with dual criteria (leftover English / blanked-out lines), focusing on paragraph edges and page edges |
| Number reconciliation | The number-token sets of original and output must match exactly, catching translation misalignment |
| **29 hard-won pitfalls** | Every one paid for with real tuition (see below) |
| Word/DOCX support | In-place replacement for .doc/.docx (tables/headers/footers/text boxes fully scanned), embedded images via the raster-overlay craft, PDF delivery by default |
| Execution organization & patrol | Long-task splitting/batched checkpointing/sub-agent scheduling with timed patrol fallback: resumable when broken, always noticed when broken, taken over when noticed |

### 29 pitfalls — sample a few

- 🏷️ **Four-part-key indexing**: block/line numbers are unstable across batches; a wrong key misaligns an entire page (the v1 crash, documented)
- 🎨 **Colored text evades the "find gray text" scan**: in-chart labels sharing colors with graphics need an "any channel dark enough" criterion, then row segmentation to separate text from arrow lines
- 📉 **Measurement ledgers go stale**: coordinates handed across sessions can be globally offset or miscopied — re-measure each item against the original before executing; the original is the only authority
- 🔲 **Cover patches cause collateral damage**: table borders cut into 25 breaks, gold legend lines covered, badge color mismatches… patch avoidance must extend to legend swatches, block edges, and decorative lines
- 🐘 **No font subsetting = 400MB+**: embedding a full CJK font makes the output too big to deliver
- 👻 **Covering text ≠ deleting text**: residual characters still sit in the text layer; copy them out and you get ghost gibberish
- 🌀 **Giant-type page floods**: when the backfill overflows its width, never stretch — reduce font size or wrap
- 🧹 **Line-end fragments**: orphan snippets like `"n."` and `". A"` bypass whole-sentence translation and need dedicated scan-and-clean
- 🔀 **Same-block text across cells bleeds across cells**: text from adjacent cells/frames often lives in one text block; block-based backfill writes cell A's content into cell B (target blank, neighbor overloaded) — rewrite cell by cell against the original spans; and the same chart design repeats across the book, so fix one and sweep all
- 📝 **Word's pitfalls live elsewhere**: python-docx only walks body paragraphs and misses tables/headers/footers/text boxes; Word splits one sentence into multiple runs, so aggregate per paragraph; verify fonts before PDF conversion or the layout drifts
- ……plus whole-line loss at paragraph/page edges, raster-image blind spots, mixed-size font bleed, re-drawing special text in original style, and more

## Quick start

### Install

```bash
git clone --depth 1 https://github.com/jia295339800/pdf-layout-translate.git
```

Put `SKILL.md` into your Agent's user-skill directory, e.g. `user-skills/pdf-layout-translate/`.
On Agents with a Skill mechanism (e.g. LingGuang), just say: "**Translate this PDF with pdf-layout-translate, keep the layout unchanged.**"

### Dependencies

- Python: `PyMuPDF (fitz)`, `numpy`, `fontTools` (pyftsubset)
- Chinese fonts: Source Han Sans/Serif (Noto CJK), Regular + Bold, subset required
- OTF ↔ TTF conversion: hand-written fontTools script (PyMuPDF's OTF support is spotty)

### A note for human readers

This skill is built for Agents — it's not off-the-shelf software but a set of operating procedures for "getting the job done right."
If you want to follow along manually, the code snippets in `SKILL.md` can be copied directly.

## Workflow (five steps)

1. **Sample first**: pick 2–3 representative pages (body/chart/cover) and produce a sample; only proceed after user sign-off — the confirmed plan is the acceptance standard
2. **Build the index**: full-text block index (four-part key pno/bidx/lidx/span, globally unique), recording each span's bbox/size/color/weight
3. **Translate**: aggregate by block for translation; payloads carry the four-part key for backfill positioning; numbers/names/code/brand names preserved, terminology unified across the book
4. **Overlay**: redaction erase (never touching graphics) → same-coordinate insert_text Chinese overlay, baseline at `y1 − 0.22 × size`
5. **Acceptance**: line-by-line scan (dual criteria: missed translation / missed backfill) → number reconciliation → 4x rendered crops inspection → publish as an update to the original artifact

## FAQ

**Q: Is the output really pixel-identical in layout?**
A: That is the entire point of this skill — don't re-typeset, just swap the words. Page-by-page pixel comparison is mandatory acceptance before publishing.

**Q: What about scanned PDFs?**
A: Automatic downgrade to a Chinese side-by-side edition ("original page image + Chinese translation page") — no forced overlay (there's no text layer to erase).

**Q: Are English labels inside charts translated too?**
A: Kept by default (legends, brand marks, abbreviations); key labels the user confirms get point-by-point overlay, verified one by one.

**Q: What if the text inside a chart image is already garbled in the source file?**
A: It can't be translated. The sample-stage integrity pre-check flags unreadable image blocks up front and keeps them as-is (figure captions and source lines are still translated); readable in-chart text — text layer or image — is handled by the corresponding craft.

**Q: Can it translate into other languages?**
A: The craft is the same — swap the target font and character set. The handbook is distilled around Chinese localization, so other languages need your own adjustments.

## Changelog

- **v1.5.5** (2026-11-22) — Added Pit 28 "SMask Loss Pit" (source images may be a black-background JPEG + transparency mask; losing the mask exposes the black background; full-book black-background scan before publishing) and Pit 29 "Pixel-Level Image Reconstruction Pit" (five compositing traps when erasing/redrawing text in bitmaps)
- **v1.5.4** (2026-11-22) — Added Pit 26 "Checklist Pit" (chart patch lists must be generated by programmatic full-book scanning, never hand-picked pages; final acceptance = page-by-page scan of the whole book) and Pit 27 "Redact Collateral Pit" (partially overlapping redact annotations silently truncate neighboring span characters; requires a full-book old-vs-new span truncation scan)
- **v1.5.3** (2026-11-22) — Added Pit 25 "Scope Pit": the keep-untranslated scope must never silently carry across documents; re-confirm chart coverage scope at the sample stage
- **v1.5.2** (2026-11-22) — Added 4.0 "Delivery Naming": output files take the report's own main title (optionally with a "Chinese edition" suffix), one name per report in a batch, no internal generic names
- **v1.5.1** (2026-11-19) — Added "in-chart text integrity pre-check": before delivering the sample, inspect chart images for readable text; corrupted image blocks are flagged as keep-as-is up front
- **v1.5.0** (2026-11-19) — Added 4.1 "Execution Organization" (task-splitting principles/batched checkpointing/sub-agent scheduling/lost-handoff fallback/three-piece acceptance) and 4.2 "Timed Patrol" disconnect fallback: scheduled with dispatch, resumed on stall, closed on delivery
- **v1.4.0** (2026-11-19) — Added Word/DOCX input support: in-place replacement craft, embedded-image text handling, PDF delivery (with a font-verification defense)
- **v1.3.1** (2026-11-19) — Pit 24 field lessons: identical chart designs repeat across the book — sweep and fix all at once; misplaced text can overflow the frame, so clear ranges extend by actual spans
- **v1.3.0** (2026-11-19) — Added Pit 24: same-block text across cells bleeds across cells on block-based backfill (with per-span landing acceptance)
- **v1.2.0** (2026-11-19) — Added Pits 21–23: colored-text scan criteria, stale-coordinate-ledger defense, patch avoidance extended to legend swatches and decorative lines
- **v1.1.0** — Added 6 pitfalls: covered-text ghosts, raster images, line-end fragments, version pinning, etc.
- **v1.0.0** — First release: full pipeline + 13 pitfalls

## Feedback

Found a problem or have a new pit to contribute? Open an [Issue](https://github.com/jia295339800/pdf-layout-translate/issues) or a PR —
every new pit is a tuition waiver for the next user.
