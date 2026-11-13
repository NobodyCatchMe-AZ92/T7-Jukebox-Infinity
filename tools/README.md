# Tools

Python helpers used to build the mod's data and to research the game. All of them only READ the game's files;
none of them are needed to build or run the mod. Run with `py -I tools/<name>.py ...` (Python 3.12).
Usage is in each file's header.

| Tool | What it does |
|---|---|
| `paklist.py` | list the files of a Tekken 7 pak (UE4 v3/v4, plain index) |
| `pakget.py` | extract files from a pak (zlib blocks) |
| `bnk.py` | parse a plain Wwise bank: sources, stream types, sizes |
| `bgm_states.py` | map `BGM_Selector` / `FinalRound` state values to the media they play (FNV-1 names -> switch containers -> Sounds) |
| `bgm_hierarchy.py` | explore AkBankBGM's object hierarchy (research for loop preview) |
| `wem_scan.py` | every `.wem` in the paks: codec, channels, length, `smpl` loop, which banks use it |
| `gen_export_media.py` | `src/export_media.hpp`: bgm id -> game media for L3 export |
| `gen_font_cover.py` | `src/font_cover.hpp`: which characters each game font can draw |
| `gen_proxy.py` | `src/proxy_multi.cpp` + `src/proxy.def`: the multi-name proxy (needs `pefile`) |
| `gfx_dump.py` | dump a Scaleform movie uasset: sprites, frame labels, named placements, external images, exports |
| `ue_tex.py` | decode small UE4 UI textures (DXT1 / DXT5 / BGRA) to a PNG contact sheet |
| `t7re.py` | static RE helper for the exe: strings, xrefs, disassembly (needs `capstone`, `pefile`, `numpy`; exe path via `T7_EXE`) |
| `usm_crypt.py` | recover the game's USM video masks from a game video you own, verify them, encrypt your own background video |
| `release/pii_scan.py` | privacy scan for release files (see docs/MAINTAINING.md) |

Some tools need a decrypted bank: extract `AkBankBGM.bnk` / `Init.bnk` with `pakget.py` from
`pakchunk0-WindowsNoEditor_P.pak` and decrypt it if it does not start with `BKHD` (AES-256-ECB, the key in
`src/gamefile.hpp`; whole 16-byte blocks only).
