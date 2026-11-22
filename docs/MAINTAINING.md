# Maintaining Jukebox Infinity

How to build, change, test and release the mod from this repository. How everything works is in
[TECHNICAL.md](TECHNICAL.md).

## What you need

- Tekken 7 on Steam, final version (the addresses in the code are for that build; the mod checks the code it
  hooks and stays off on any other build).
- Windows, Visual Studio 2022 with the C++ x64 tools (`build.bat` calls `vcvars64.bat` from the Community edition's
  default path - edit `VSDIR` for another edition).
- Python 3.12 for the tools (standard library; `t7re.py` needs `capstone`, `pefile`, `numpy`; `gen_proxy.py`
  needs `pefile`).

## Building

```
build.bat   -> build\winmm.dll          dev build (with a PDB, for debugging)
            -> build\public\winmm.dll   release build (no debug info, NDEBUG) - ship this one
```

Install: copy the DLL to `TEKKEN 7\TekkenGame\Binaries\Win64` (next to `TekkenGame-Win64-Shipping.exe`). The game
holds the DLL open while it runs - close it first. Check `Win64\t7jukebox\t7jukebox.log`: the first line is the
version banner, then one `hook ...: create 0 enable 0` line per hook (0 = MH_OK).

Version: `kModVersion` in `src/library.hpp` (also the first line of `T7Jukebox.ini`; an INI without the current
version line is rewritten once at startup, keeping the user's settings) and the banner in `src/main.cpp`.

## Testing checklist (in game)

- Main menu: Jukebox between Customization and Gallery, both directions; description; Quit label; other items work.
- Playlist screen: make each playlist active; RANDOM row Left / Right through every folder; X Random behaviour.
- Editor: assign a file, a game song, a Bonus Track and a "Random:" row to Round 1 / Final / Special; volumes;
  preview / hold-Y loop preview (mp3, wav, .wem, game song, Bonus PCM track); LB / RB; X refresh; View; Start reset;
  L3 export; long names scroll; a Japanese file name.
- Matches: Custom playlist (Round 1 -> match point switch), the same song in both slots (continues), Lars on
  Twilight Conflict / Leroy on Dragon's Nest (Special), Random (one song / new song at match point), menus.
- A broken file (empty .mp3, text renamed to .wem): the game's music, logged.
- A clean install (no INI, empty Jukebox Songs): files created, default playlist.

## Common changes

- **New stage or scene**: `kStages` in `src/library.hpp` (id + name); its game songs in `kVanillaTracks`.
- **Song Sets**: `StageSets` in `src/library.hpp` (5 `Assign`s, `has[set][slot]`, `sel`), INI keys
  `<id>.SetN.<slot>` / `<id>.Set`; the set is picked per scene entry in `cur_assign()` (`src/main.cpp`).
- **Game song titles / order**: `kVanillaTracks` (`src/library.hpp`) - `{ bgm id, internal name, round, title,
  hidden, media, part start / end }`. `hidden` keeps a duplicate out of the browser (still labelled if assigned).
- **Bonus Tracks**: `src/unused_tracks.hpp` - `{ media, title, copies, level_db, cat }`, kept alphabetical.
  Find candidates with `tools/wem_scan.py` (every pak `.wem`: codec, length, loop) and the bank tools.
- **L3 export map**: `tools/bgm_states.py` (state -> media from a plain AkBankBGM dump) then
  `tools/gen_export_media.py` -> `src/export_media.hpp`.
- **Fonts**: extract `UI_common/flash/fontlib/gfxfontlib.uasset` with `tools/pakget.py`, run
  `tools/gen_font_cover.py` -> `src/font_cover.hpp`.
- **Proxy names**: `tools/gen_proxy.py` -> `src/proxy_multi.cpp` + `src/proxy.def`.
- **Background video**: encode Sofdec Prime 1920x1080 30 fps, no audio; `tools/usm_crypt.py recover` (masks from a
  game video) then `encrypt`; ship it as `Win64\t7jukebox\Jukebox Background.usm`.
- **Menu / movie research**: `tools/gfx_dump.py` (sprites, frame labels, placements, exports of a movie uasset),
  `tools/ue_tex.py` (UI textures to PNG), `tools/t7re.py` (strings, xrefs, disassembly of the exe).

## Using it inside another DLL mod

The code has no global constructor work: `DllMain` checks the process, creates the `Local\t7jukebox_<pid>` guard
event and starts `init_thread`. To ship it inside another mod's DLL: compile `src/main.cpp` + `src/decoders.cpp`
as their own translation units (everything is in `namespace jb`), drop `proxy_multi.cpp` / `proxy.def`, turn
`DllMain` into an exported start function called by the host, and let `MH_Initialize` accept
`MH_ERROR_ALREADY_INITIALIZED` when the host already initialised MinHook. Keep the guard event, so a standalone
Jukebox DLL in the same folder stays inert. Settings, songs and logs stay in their own files and folders.

## Releasing

1. Bump `kModVersion` / the banner, update `CHANGELOG.md`, build, test (checklist above).
2. Package (the zip contents = the install layout):
   ```
   Jukebox Infinity <ver>/README.txt                      (dist/README.txt)
   Jukebox Infinity <ver>/THIRD_PARTY_LICENSES.txt
   Jukebox Infinity <ver>/Win64/winmm.dll                 (build/public/winmm.dll)
   Jukebox Infinity <ver>/Win64/Jukebox Songs/!PUT CUSTOM SONGS HERE ... .txt   (dist/Jukebox Songs/)
   Jukebox Infinity <ver>/Win64/t7jukebox/Jukebox Background.usm   (main download only; not in this repo)
   ```
   Main file `Jukebox_Infinity_v<ver>.zip` (with the video), secondary `Jukebox_Infinity_LITE_v<ver>.zip`
   (without), e.g. `Jukebox_Infinity_v1.1.zip` / `Jukebox_Infinity_LITE_v1.1.zip`.
3. Privacy scan everything that goes public - the zips' contents and this repo:
   `set T7_PII_TERMS=<your real name>,<your email>` then `py tools/release/pii_scan.py <folder or file> ...`
   (searches UTF-8 and UTF-16, binaries too; terms are never printed). Short name terms can match inside ordinary
   words (e.g. a 4-letter first name inside "generic") - check each hit's masked excerpt.
4. Never commit or ship: game files (music, videos, movies, textures, banks), the user's own `T7Jukebox.ini` /
   songs / logs, debug builds with PDB paths.
