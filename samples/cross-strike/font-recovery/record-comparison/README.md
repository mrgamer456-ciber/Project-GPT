# CrossStrike TEXR record comparison

This is a diagnostic only. No source PAK/TEXR files or game assets are modified.

- TEXR files examined: 7
- Candidate rows: 168
- Records 0–3 in each area were compared.
- Candidate palette location: record +0x10 (256 RGBA entries).
- Candidate pixel offsets: +0x410, +0x420, +0x4D0, +0x540.
- Both indexed 8bpp and packed 4bpp interpretations are previewed.
- Preview images are composited over dark grey to reveal transparent glyphs.
- Use record-comparison.csv to compare distinct index counts and alpha histograms.

A candidate is not confirmed merely because it looks brighter; it must also match record structure and produce coherent glyph shapes.
