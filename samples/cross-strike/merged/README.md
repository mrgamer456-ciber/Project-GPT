# Combined CrossStrike PAK

- Output: `CROSSSTRIKE_ALL.PAK`
- Format: HJK1 version 2
- Source PAKs: 7
- Combined sections: 105
- Output size: 17,649,920 bytes
- All section payloads were byte-for-byte validated against the seven source PAKs.
- Repeated 4-byte section tags were preserved; no sections were discarded.

## Important compatibility note

This is an experimental all-in-one archive. The existing game code requests COMMON.PAK and map-specific PAK files separately. A combined archive is NOT confirmed loadable by the current game until the PAK loader and asset lookup are changed to select sections by source/map. Keep the original seven PAKs unchanged.

## Section tag counts

- BARL: 2
- CHNK: 7
- COLG: 7
- COLH: 7
- COLT: 7
- ENVR: 7
- INDX: 7
- MATL: 7
- MODL: 2
- NAVL: 7
- NAVN: 7
- RADR: 6
- SNDS: 3
- SNOW: 1
- SPWN: 7
- TEXR: 7
- UIMG: 7
- VERT: 7
