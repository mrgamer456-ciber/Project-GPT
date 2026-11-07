# CrossStrike alpha / CLUT comparison (non-destructive)

Four PNG candidates are generated for every TEXR record:
- current: same palette and alpha interpretation as the original exporter.
- alpha2x: PS2 GS alpha 0..128 mapped to PNG alpha 0..255.
- clut_csm1: tests the PS2 GS CSM1 8-bit CLUT entry ordering (swap 8..15 with 16..23 in each 32-entry group).
- alpha2x_csm1: applies both tests.

These are comparison candidates only. No original BIN or existing PNG is overwritten.
Each area's comparison_first16.jpg compares the first 16 records, with variants in columns.
