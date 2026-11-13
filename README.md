# Jukebox Infinity - a Jukebox for Tekken 7 (PC)

**Version 1.0** - by t7jukeboxauthor

Choose the music for every stage and menu in Tekken 7: the game's own soundtrack, 89 bonus tracks hidden in the
game files, and your own `.mp3` / `.wav` / `.wem` songs - all set up in a Jukebox menu inside the game, restored in
the spirit of the PS4 version's Jukebox.

- A **Jukebox** entry on the main menu, with playlists and a Playlist Editor built from the game's own menus.
- **Two songs per stage** - Round 1 and Final Round (from match point) - plus a Special slot for Lars' and Leroy's
  character themes, and songs for the Main Menu, Character Select, Online Warm-Up and Customization.
- **Custom playlists** (3), **Random playlists** (everything / your songs / one folder) and per-stage
  "Random: <folder>" picks.
- **Song preview** with loop preview, a **volume per song** (0-300%), **loop points** for mp3 / wav.
- The game's **whole soundtrack** with official titles, **89 Bonus Tracks** (beta / unused / alternate versions
  found in the game files), and **export** of any game song as a `.wem`.
- Runs entirely in memory: no game file is changed. Remove the DLL and the game is exactly as before.
- Client-side only, fine for online play.

## Download and install

Get the latest release from the Releases page (or tekkenmods.com / nexusmods.com):

- `JukeboxInfinity.zip` - the full mod with the Jukebox background video
- `JukeboxInfinityLITE.zip` - the same without the video

Copy the zip's `Win64` folder contents into `TEKKEN 7\TekkenGame\Binaries\Win64`. Full instructions, controls,
troubleshooting and a guide to making `.wem` files: **[dist/README.txt](dist/README.txt)** (the README that ships
in the zips).

Requirements: Tekken 7 on Steam (final version), Windows 10 / 11 64-bit. Nothing else.

## This repository

| Path | |
|---|---|
| `src/` | the mod (C++20, MinHook) |
| `third_party/` | MinHook, dr_libs (dr_mp3 / dr_wav) |
| `build.bat` | builds `build\winmm.dll` (dev) and `build\public\winmm.dll` (release) with Visual Studio 2022 |
| `dist/` | the user README and the files that ship next to the DLL |
| `tools/` | Python tools for the game's paks, Wwise banks, `.wem` files, Scaleform movies, fonts, USM videos |
| `docs/TECHNICAL.md` | **how it all works** - Tekken 7's music pipeline (Wwise states, IO hooks, bank patches, volume RTPC), its menus (Scaleform AS3, dialogs, the main menu), fonts, input, the encrypted USM videos, addresses, and the dead ends |
| `docs/MAINTAINING.md` | building, testing, common changes, embedding in another DLL mod, releasing |

If you want to make a different Tekken 7 mod - music, menus, UI text, videos - `docs/TECHNICAL.md` is the place to
start: most of what it describes (the Scaleform helpers, the dialog API, the pak / AES reader, the multi-name proxy)
is reusable as is.

## Building

```
build.bat
```

Needs Visual Studio 2022 (C++ x64). Output: `build\public\winmm.dll` (release) and `build\winmm.dll` (dev, with
debug info). The game must be the final Steam build; the mod verifies the code it hooks and stays off otherwise.

## Credits

- Built by t7jukeboxauthor with Claude (Anthropic's AI assistant, Claude Code), which did the reverse engineering
  and programming together with the author.
- The Tekken 7 modding community: ThePaSch's T7 Jukebox tool (and xRuneXero, Ressen_XiaoPai and Gneiss, credited
  there, for the stage music IDs and the music bank key), Dr.Shadowds' Cheat Engine table that revealed the PS4
  Jukebox hidden in the PC game.
- [MinHook](https://github.com/TsudaKageyu/minhook) (BSD 2-Clause), [dr_libs](https://github.com/mackron/dr_libs)
  (Unlicense / MIT-0) - see `THIRD_PARTY_LICENSES.txt`.

## License

MIT - see [LICENSE](LICENSE). Third-party code keeps its own license (`third_party/`).

TEKKEN is a trademark of Bandai Namco Entertainment Inc. This is an unofficial fan-made mod, not affiliated with or
endorsed by Bandai Namco. No game files (music, video, art) are included in this repository or the releases; the
mod reads the game's own files from the user's installation.
