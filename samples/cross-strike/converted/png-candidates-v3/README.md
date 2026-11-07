# CrossStrike — extraction of all TEXR texture records

This version reads every texture record, not just one fixed slice.
Record layout inferred from file lengths: 16-byte global header, then fixed 0x4420-byte records.
Each record: 0x10-byte header, 256 RGBA palette entries at record+0x10, 128x128 indexed pixels at record+0x410, and 0x10 bytes of record padding.
Only the original, unmodified colors are exported. No brightness, contrast, or color enhancement is applied. Source BIN files are never modified.

| Area | Texture count | Record size | PNGs |
|---|---:|---:|---:|
## COMMON
- TEXR size: 2,197,456 bytes
- Texture count in header: 126
- Record size validated: 0x4420 (17,440 bytes)
- SHA-256: 23a7ed73561b3b472d25bfdc1e7907cc244f69ee76ef938e44c1d01c6dc2b94e
- PNG previews: 126 (original colors only, no brightness adjustment)
- [Open contact sheet](COMMON/COMMON_contact_sheet.jpg)

## FLAT
- TEXR size: 366,256 bytes
- Texture count in header: 21
- Record size validated: 0x4420 (17,440 bytes)
- SHA-256: f44f42b2899a42578deb3decd70cae051057c2599b3f21e7487a51fd021fc953
- PNG previews: 21 (original colors only, no brightness adjustment)
- [Open contact sheet](FLAT/FLAT_contact_sheet.jpg)

## ISLAND
- TEXR size: 418,576 bytes
- Texture count in header: 24
- Record size validated: 0x4420 (17,440 bytes)
- SHA-256: 3bd4da36df2218c777b699df88adce31f11e66d48255e5b2a89d7c28db2e93f7
- PNG previews: 24 (original colors only, no brightness adjustment)
- [Open contact sheet](ISLAND/ISLAND_contact_sheet.jpg)

## KASBAH
- TEXR size: 436,016 bytes
- Texture count in header: 25
- Record size validated: 0x4420 (17,440 bytes)
- SHA-256: 4a7968fb181995e0132be3ab9e45194a97fec469d592085fcd1f8e0a1dcaefeb
- PNG previews: 25 (original colors only, no brightness adjustment)
- [Open contact sheet](KASBAH/KASBAH_contact_sheet.jpg)

## OFFSHORE
- TEXR size: 2,336,976 bytes
- Texture count in header: 134
- Record size validated: 0x4420 (17,440 bytes)
- SHA-256: 3f91806a4beba4e2e7d727e6945837925f13d75d81fa9ccb09313c2ab1af1d24
- PNG previews: 134 (original colors only, no brightness adjustment)
- [Open contact sheet](OFFSHORE/OFFSHORE_contact_sheet.jpg)

## SNOWFIELD
- TEXR size: 470,896 bytes
- Texture count in header: 27
- Record size validated: 0x4420 (17,440 bytes)
- SHA-256: cd02a24150e3594588b1ff2518afd5b0ab9c462d2005e127719a4d3bce18747f
- PNG previews: 27 (original colors only, no brightness adjustment)
- [Open contact sheet](SNOWFIELD/SNOWFIELD_contact_sheet.jpg)

## TRAINING
- TEXR size: 436,016 bytes
- Texture count in header: 25
- Record size validated: 0x4420 (17,440 bytes)
- SHA-256: 6a413dc9699866935dfe27f6120ee10e5d647b8577e1634788e04864ae6fdfad
- PNG previews: 25 (original colors only, no brightness adjustment)
- [Open contact sheet](TRAINING/TRAINING_contact_sheet.jpg)

