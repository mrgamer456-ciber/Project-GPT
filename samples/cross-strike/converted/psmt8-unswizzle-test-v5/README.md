# CrossStrike PSMT8 unswizzle test (V5)

This is a non-destructive spatial-layout test. For each TEXR texture it creates:
- linear: current row-major pixel interpretation.
- psmt8_unswizzled: applies the PS2 GS PSMT8 byte-address mapping to the pixel indices.

Both variants use the exact same palette and alpha bytes. This isolates pixel ordering;
no brightness, alpha, palette, source BIN, or existing PNG is changed.

Each area folder contains a side-by-side JPEG preview of the first 16 textures.
The address mapping is checked to be a one-to-one permutation of all 16,384 bytes.
A visually better candidate is evidence for this layout, not proof that every TEXR
record uses it. Inspect the previews before adopting any conversion globally.
