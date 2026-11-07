# CrossStrike PS2 — final project status

## Completed
- Extracted the seven PAK archives and identified 105 sections.
- Identified and extracted 382 TEXR texture records across COMMON, FLAT, ISLAND, KASBAH, OFFSHORE, SNOWFIELD and TRAINING.
- Created non-destructive PNG exports using the current best visual interpretation (linear indexed pixels with the original palette and alpha).
- Created diagnostic reports for record headers, palette values and pixel-index usage.
- Compared alpha scaling and CSM1 palette-order candidates.
- Compared a PSMT8 unswizzle candidate. The tested unswizzle mapping visibly deforms the previews and is rejected.

## Important result
All inspected TEXR records share the same 16-byte record header:
`40 80 00 00 00 00 00 08 00 00 00 00 00 00 00 00`.

The tested PSMT8 unswizzle is not a valid fix for these files. Keep the linear export as the current preview baseline. Do not replace the originals with the rejected unswizzled output.

## Remaining limitation
The exact PS2 GS texture interpretation has not been proven from the available TEXR records alone. The small duplicated areas and colored pixel speckles are not fully corrected yet. A final claim that every PNG is pixel-perfect would be inaccurate.

## Final export to the editing folder
Run the workflow **Extract every CrossStrike TEXR texture** once from GitHub Actions. It exports all records again and copies the original-color PNGs into the flat folder:
`samples/cross-strike/textures-to-edit/`.

Workflow:
https://github.com/mrgamer456-ciber/Project-GPT/actions/workflows/convert-crossstrike-texr-png-v3.yml

After it finishes successfully, the folder should contain 382 PNGs plus this README. Existing BIN files and earlier test outputs are not overwritten.
