# Jukebox Infinity - technical notes

How the mod works, and everything we learned about Tekken 7's music, menus, fonts and videos while building it.
Written for anyone who wants to fix, extend or port this mod, or build a different Tekken 7 (or UE4 / Wwise /
Scaleform) mod. Addresses are **RVAs in the final Steam build of `TekkenGame-Win64-Shipping.exe`**
(PE timestamp `0x63EB1C19`), UE4 4.14, Wwise (bank version 118, a Wwise 2016 runtime), Scaleform GFx with AS3 movies.

Contents

1. [Overview](#1-overview)
2. [Loading: one DLL, many proxy names](#2-loading-one-dll-many-proxy-names)
3. [The music pipeline (Wwise)](#3-the-music-pipeline-wwise)
4. [Serving our songs](#4-serving-our-songs)
5. [The bank patch (prefetch tracks)](#5-the-bank-patch-prefetch-tracks)
6. [Volume](#6-volume)
7. [mp3 / wav / PCM / ADPCM: the mod's own player](#7-mp3--wav--pcm--adpcm-the-mods-own-player)
8. [The game's own files: paks, AES, the BGM table](#8-the-games-own-files-paks-aes-the-bgm-table)
9. [Rounds, match point, character themes](#9-rounds-match-point-character-themes)
10. [Random playlists](#10-random-playlists) (and Song Sets)
11. [Loop preview and track parts (SeekOnEvent)](#11-loop-preview-and-track-parts-seekonevent)
12. [Music pak mods](#12-music-pak-mods)
13. [The main-menu entry](#13-the-main-menu-entry)
14. [Our screens: the game's dialog and the Controller Setup movie](#14-our-screens-the-games-dialog-and-the-controller-setup-movie)
15. [Scaleform from C++: Invoke, members, the GFx::Value layout](#15-scaleform-from-c-invoke-members-the-gfxvalue-layout)
16. [Text, fonts and non-Latin names](#16-text-fonts-and-non-latin-names)
17. [Information bar and button guides](#17-information-bar-and-button-guides)
18. [Input](#18-input)
19. [Background video (CRI USM)](#19-background-video-cri-usm)
20. [Safety: hook checks, bad files, recovery](#20-safety-hook-checks-bad-files-recovery)
21. [What did not work (and why)](#21-what-did-not-work-and-why)
22. [Source map](#22-source-map)

---

## 1. Overview

The mod is one native DLL (`winmm.dll` proxy) using MinHook. It never writes to game files: every change (a media
path swapped, a bank byte changed, a menu label) happens in memory, in the game's own code paths. Its on-disk
footprint is `T7Jukebox.ini`, `Jukebox Songs\` and `t7jukebox\` (log, optional background video) next to the exe.

The core idea: **Tekken 7 plays all music through one Wwise event whose song is chosen by Wwise states; when a
state change makes Wwise open a song's `.wem`, the mod hands Wwise a different file.** Everything else (playlists,
menus, preview, volume) is built around knowing which song the game is about to play and which one we want.

Hooks (17), all prologue-checked before patching:

| RVA | What | Why |
|---|---|---|
| `0x442140` | play_bgm (sound manager, actor, bgm id) | the one place music is requested |
| `0x4424F0` | set volume (unused, which, value 0..10) | BGM volume (song %), mute |
| `0x25A4B50` | Wwise IO open-by-path (`this, const wchar_t *path, AkFileDesc *`) | serve our file instead of the game's media |
| `0x25A8400` | Wwise IO read | bank patch in flight; .wem loop header |
| `0x25A4220` | Wwise IO close (`this, AkFileDesc &`) | know when a muted "shadow" stream ends |
| `0x1D7E600` | `FPakFile::Find` | hide music from pak mods (section 12) |
| `PostEvent` (wide name, exported) | `AK::SoundEngine::PostEvent(const wchar_t *...)` | keep the BGM_Container playing id |
| `CreateFileW` (import) | | serve the background video |
| `0x4D22A0` | main menu build | the Jukebox entry |
| `0x4D08C0` | main menu update (menu, ctx) | our screens' tick, input |
| `0x2C42D0` | generic list cursor | the virtual 12th main-menu item |
| `0x2C3ED0` | list confirm | open the Jukebox |
| `0x4570E0` | set text by loc key | relabel main-menu slots |
| `0x4535B0` | text variable registry lookup | fix the Quit slot's field name |
| `0x4D27A0` | main menu info line | our description |
| `0x4D1C70` | main menu News panel input | blocked while our screens are up |
| `0x507BD0` | Player Information panel refresh | capture its object to hide it |

## 2. Loading: one DLL, many proxy names

`tools/gen_proxy.py` builds `src/proxy_multi.cpp` + `src/proxy.def`: one DLL that is a valid **winmm, version,
dinput8, xinput1_3 or dsound** proxy (the game imports all of them; none are KnownDLLs). Named exports (the union of
the five DLLs) forward by name and sit at ordinals 1000+; ordinals 1..182 are NONAME stubs forwarding to the same
ordinal of the real DLL (the game imports `DSOUND` and `XINPUT1_3` by ordinal). `proxy_common.hpp` loads
`System32\<own file name>` lazily. Users rename the DLL to dodge a clash with another mod (Ghost AI = dinput8,
ReShade = dxgi).

`DllMain` runs only in `TekkenGame-Win64-Shipping.exe` and creates the event `Local\t7jukebox_<pid>`: a second copy
of the mod under another name sees it and stays inert. All work happens on an init thread.

## 3. The music pipeline (Wwise)

- **`0x442140(soundmgr, actor, bgm_id)`** is the one place music is requested: menus (`0x3E334A`: 447
  `MainMenu_cs7sp4`, 448 `CharaSelect_cs7sp4`), stage load (`0x3FC2A7`), fight start (`0x2D236E`), each round start
  (`0x4425C0` via `0x44282B`).
- It sets two Wwise states via `SetState` `0x25A94E0`: **`BGM_Selector`** = name(bgm_id) (`0x328D80`) and
  **`FinalRound`** = name2(bgm_id) (`0x328C70`), then `0x4420B0` posts the event **`BGM_Container`** once
  (flag `[mgr+0x14]`). Every later music change is only a state change; the bank's switch containers then start the
  new song's Sound, and Wwise opens its `.wem`.
- The BGM table: ids 0..4095 resolve through the two name lookups. Per stage there is usually a `Normal` and a
  `Final` state pair (e.g. Mishima Dojo: bgm 0 `stg00_wanoma/Normal` -> media 238485712, bgm 1
  `stg00_wanoma/Final` -> 421738342). Some stages have no Final (Geometric Plane plays `stg21_gimmick/Normal` all
  match). Day / evening variants share or borrow tracks (Jungle Outpost Day's final is the evening variant's).
- `AkBankBGM.bnk` (the game loads the 7,686,443-byte one from `pakchunk0-WindowsNoEditor_P.pak`): 219 Sounds,
  48 switch containers, 39 events, **no interactive-music objects** - songs are plain looping Sounds, and a song's
  loop is the media's own RIFF `smpl` loop.
- Other music: Tekken Bowl has its own bank (`AkBankTKBOWL.bnk`, event `BGM_TKBowl_Play`, switch group
  `TKBowl_Fever`: Ball Wall / Fever Night) - unreachable through `BGM_Container`, so those songs are played by
  media id (section 4, `wem:` songs).
- The exe exports the Wwise API by name (`PostEvent` x3, `SeekOnEvent` x6, `GetSourcePlayPosition`, `SetState`,
  `GetIDFromString`, `ExecuteActionOnEvent`, `StopPlayingID` ...): look them up with `GetProcAddress` on the exe.

## 4. Serving our songs

The Wwise sample IO hook builds media paths with `CAkFileLocationBase::GetFullFilePath` (`0x25A56D0`,
`L"%u.wem"` / `L"%u.bnk"`) and opens them with **open-by-path `0x25A4B50`** -> `FPlatformFileManager` file size
(`0x7CDFF0` vslot `0xE8`); the `AkFileDesc` keeps an `FString*` of the path (`desc+0x10`) that later reads reopen.
**Replacing the path argument redirects the whole stream.** `PakPlatformFile` falls through to loose absolute
paths, so a file in `Jukebox Songs` is read directly, plain (pak encryption is an archive feature, not Wwise's).

Song kinds (keys in the INI / code):

| Key | Meaning | How it plays |
|---|---|---|
| `Tekken 4\Airport.wem` | a user file | open hook swaps the path |
| `bgm:<id>` | a game song | request that bgm id's states instead |
| `bgm:<id>@<ms>` | part of a game song (credits) | states + SeekOnEvent (section 11) |
| `wem:<media>` | a game media file by id (Bonus Tracks, Bowl) | open hook swaps in the game's own `<media>.wem` path |
| `random:<key>` | a random pick from a folder | resolved once per scene / match |

The slot an opened BGM track belongs to = the `FinalRound` state of the last music request (`Normal` -> Round 1,
`Final` -> Final Round). A **carrier**: when the game would not open a new stream (e.g. Geometric Plane at match
point, or a preview), the mod requests some other state pair (bgm 1 or 23) so Wwise opens a fresh stream, and the
open hook serves that stream our file.

Same song in Round 1 and Final: for a Wwise-played file the mod skips the state change at match point (no new
stream = no restart) and only applies the Final slot's volume.

## 5. The bank patch (prefetch tracks)

Swapping the media of a **prefetch** Sound (Wwise "zero latency": the bank holds the first part of the media) gave
a click then silence: the bank's head belongs to the original song. The read hook follows the bank structure while
Wwise reads `AkBankBGM.bnk` and sets every Sound's stream type 1 (prefetch) -> 2 (stream only) in the buffer before
Wwise parses it (133 of 219 Sounds). Pure streaming then works for every stage. (`tools/bnk.py` parses a plain bank
offline.)

## 6. Volume

- `Init.bnk` holds the RTPC `BGM_Volume` (FNV-1 `"bgm_volume"` = `0x145D321E`) on two buses with a 3-point curve
  `(0,-1,Log1) (6,-0.499,Linear) (10,0,Linear)` (y = linear gain - 1). The options screen sends integers 0..10
  through `0x4F6E80 -> 0x4424F0(unused, which, value) -> AkAudioDevice::SetRTPCValue 0x25A92C0`, every frame while
  it is open; values above 10 clamp.
- While Wwise reads `Init.bnk` the mod replaces that curve in memory (only if the bytes match exactly) with
  `(0,-1) (50,0) (150,+2)` linear = gain x/50 up to x3. `setvol_hook` then sends
  `x = 50 * gain(option) * song% / 100`: the player's own Music setting still works, and a song can go to 300%.
- 0 = mute: used while the Jukebox screens are open and under "shadow" streams (section 7).

## 7. mp3 / wav / PCM / ADPCM: the mod's own player

- `src/player.hpp`: whole-file decode to s16 (dr_mp3 / dr_wav, Wwise PCM, Wwise IMA ADPCM), XAudio2 2.9, 4 x 4096-frame
  buffers, loop wrap (Song Loops.txt, or the file's `smpl`), 75 ms fade-out on switch, no fade-in at song start,
  per-track gain + song % (atomic), follows the Windows default device (`IMMNotificationClient`) and rebuilds on
  device loss.
- When a music open targets an mp3 / wav (or a player-decoded game file) the open hook lets Wwise open its
  **original** media - the "shadow" - muted (`BGM_Volume` 0), and the player plays our file. The IO close hook sees the
  shadow's file object close and stops the player. Menu themes start instantly, so the mod pre-mutes in `play_hook`
  before the request goes through (else the vanilla theme blips).
- **Wwise IMA ADPCM** (fmt `0x0002`): blocks of 36 bytes **per channel** (i16 sample, u8 step index, pad, 32 data
  bytes) = header sample + 63 nibbles (low nibble first) = 64 samples per channel per block. Found by trying layouts
  offline and scoring sample continuity.
- Levels: Wwise applies each Sound's bank volume (Tekken Bowl: Ball Wall -6.5 dB, Fever Night -5.5 dB) and XAudio2
  mixes 6 channels to stereo at full level, so player-decoded game files get a fixed trim (ADPCM -17 dB, PCM -12 dB,
  Bonus Tracks their own level) to match the game's loudness.

## 8. The game's own files: paks, AES, the BGM table

- Paks: `pakchunk0/1/2-WindowsNoEditor.pak` + patch paks `pakchunk0/1-WindowsNoEditor_P.pak` (patch first). Indexes
  are plain (v3); `tools/paklist.py` / `pakget.py` list / extract. Some entries are AES-256-ECB encrypted (whole
  16-byte blocks; the trailing remainder is plain) with the community-known Tekken 7 key (also used by the QuickBMS
  `Encrypt.bms` script); `src/gamefile.hpp` reads `<id>.wem` straight from the paks (never `~mods`) and decrypts any
  file that does not start with `RIFF`.
- 642 `.wem` media in the paks; `tools/wem_scan.py` lists codec / channels / length / loop for all of them.
  Codecs seen: `0xFFFF` Wwise Vorbis (most music), `0x0002` IMA ADPCM, `0x0001` / `0xFFFE` PCM.
- `src/export_media.hpp` (`tools/gen_export_media.py`): bgm id -> the game media behind it (for L3 export).
- Stage ids (global current stage `exe+0x34DF550`): 0 Mishima Dojo, 1 Forgotten Realm, 2 / 53 Jungle Outpost
  (evening / day), 3 Arctic Snowfall, 4 / 54 Twilight Conflict (day / evening), 5 Dragon's Nest, 6 Souq, 7 Devil's
  Pit, 8 Mishima Building, 9 Abandoned Temple, 30 Duomo di Sirio, 31 Arena, 32 / 33 G Corp. Helipad (day / night),
  35 Brimstone & Fire, 36 Precipice of Fate, 37 Violet Systems, 39 Kinder Gym, 40 / 55 Infinite Azure (day / night),
  41 Geometric Plane, 51 Howard Estate, 52 Hammerhead, 56 Last Day on Earth, 57 Cave of Enlightenment, 58 Vermilion
  Gates, 59 Island Paradise; online warm-up = stage 42 `stg22_grid`.
- The PC exe still contains the PS4 Jukebox code (`CJukeBox::exec`, `SwfJukeBox::exec`, main-menu action id 5,
  text keys `jukebox_msg_000..056`), but **not** its movie (`UI_PS4/flash/SW_UI_JukeBox`) or art - so this mod
  rebuilds the UI from PC movies instead.
- **Bonus Tracks**: of the 642 media, everything the game's tables do not reach was scanned (length, loop, data hash
  to collapse copies) and listened to; 89 named keepers are in `src/unused_tracks.hpp`
  (`{ media, title, copies, level_db, cat }`). Also found: the credits file `600143732.wem` holds two songs
  (Aloneness 0..186.5 s, The Long Goodbye after), and AkBankBGM embeds one full song (`614444607`, Mishima Dojo
  "Round1" state, bgm 418).

## 9. Rounds, match point, character themes

`0x4425C0` (round start) decides `Normal` vs `Final`: match point = a player's wins (`[0x248780()+0x20]` / `+0x110`)
== rounds to win (`0x6FCF70()`) - 1; then the bgm id comes from `0x32A730([exe+0x34CE960], stage (0x6FCF60), key)`.
Special cases: some fights take their bgm from an object (`+0x99C` / `+0x9A0`), and **character themes replace the
Final state at match point**: Lars on Twilight Conflict -> bgm 47 `stg04_manhattan/VREDE4` (`exe+4427C1`, evening
`exe+4427E3`), Lars in the NJPW costume -> 434 `stg00_wanoma/NJPW`, Leroy on Dragon's Nest -> 444
`stg05_bridge/LEROY` (`exe+442797`). Boss fights use `BossKazumi_*` / `BossMRX_*`. The mod treats `Final`,
`VREDE4`, `LEROY`, `NJPW` and `*_Final` as "final", and gives the three character-theme stages a separate Special
slot.

Scenes: the mod tracks a "scene entry" (a scene change, a stage load, or a fight start not right after a stage load)
so a new random pick happens once per menu visit / match, not per round.

## 10. Random playlists

Pools: Random (All) = the standard game songs (Normal/Final of every stage, the menu themes with audio on PC,
character / boss / story / bowl / credits songs) + every user file; Random (Custom) = user files; Random (Folder) =
one top folder, `Tekken 7 Default` (game songs) or `Tekken 7 Bonus Tracks`. One pick per scene entry, kept all match;
optionally a second pick at match point (`RandomSwitchAtMatchPoint`). The final-round switch is suppressed for
Random by keeping the Normal states. Some BGM table entries have no media on PC (e.g. `CharaSelect_ac7`, bgm 49,
the PS4 jukebox's old-Tekken tracks `T1_bgm_*`): they are excluded so a pick is never silent.

### Song Sets (1.1)

Every stage / scene of a Custom playlist is a `StageSets` (`src/library.hpp`): five `Assign`s (Round 1 / Final /
Special song + volume each), `has[set][slot]` for Sets 2-5 (Set 1 is always assigned; `""` = the game's music) and
`sel` (Set 1..5, or Random Set). `cur_assign()` (`src/main.cpp`) builds the assignment of a scene entry once - the
same moment "Random: <folder>" slots are resolved: `pick_set()` takes the selected set (Set 1 when it is unassigned)
or, for Random Set, a uniform pick among the assigned sets; `effective()` fills the set's unassigned slots with Set
1's songs. Everything downstream (match-point switch, same-song continuation, character themes, volumes) sees one
ordinary `Assign`, so sets needed no other playback change. The per-entry copy is rebuilt when the settings change
(`Settings::gen`). INI: Set 1 keeps the pre-1.1 keys; Sets 2-5 write `<id>.SetN.Early|Final|Special[Volume]` only
for assigned slots (`default` = the game's music, so an empty value never means "unassigned"); `<id>.Set` only when
not Set 1. Editor: the stage row's right column (`ButtonSymbol_mc`, pinned like the volume) shows the set, with the
volume arrows; the "*" moved into the row's unused left-aligned `Operation_mc` field (row x -240).

## 11. Loop preview and track parts (SeekOnEvent)

- The music is **one** event, `BGM_Container`, posted once (at the main menu). The mod's PostEvent hook adds
  `AK_EnableGetSourcePlayPosition` (`0x100000`) to its flags and keeps the playing id.
- Loop preview of a Wwise-played song: the read hook parses the RIFF header (rate + `smpl` loop) on the first read
  of the music file; hold-Y then calls `SeekOnEvent(GetIDFromString(L"BGM_Container"), all objects, loopEnd - 3000 ms)`.
- Track parts (the two credits songs in one file): a 20 ms thread checks `GetSourcePlayPosition` while a part plays
  and seeks back to the part's start when it leaves its range.

## 12. Music pak mods

`FindFileInPakFiles` (`0x1D7E9A0`) asks every mounted pak (`FPakFile::Find` `0x1D7E600`, first hit wins; `~mods`
paks have the higher read order). The pak-find hook returns "not here" for `AkBankBGM.bnk` and the BGM bank's media
ids in any pak that is not the game's own `Content/Paks/pakchunk*`, so lookups fall through to the original files.
Only music is affected; voices, SFX and all other assets of pak mods still load. Without this, a BGM pak mod changes
the bank under the Jukebox and media ids stop matching.

## 13. The main-menu entry

- Main menu movie `SW_UI_MainMenu`; controller object: `+0x20` movie wrapper, `+0x30` clip-path table, `+0x4B4` the
  action of the cursor item, `+0x4BC` item count (11), cursor = **global `exe+0x34D67A8`** (also used as the "game
  mode" index by other mods - so a real 12th item would shift every index: not done).
- Tables (writable `.data`, 11 entries): loc keys `exe+0x343D9B0`, actions `exe+0x343DA08`
  `[0,1,2,3,4,6,7,8,9,11,12]` (5 = the removed PS4 Jukebox), has-submenu `exe+0x343DA38`, selectable `exe+0x343DA48`.
- **Virtual entry**: the movie has 14 item slots (`Main0..13`). The mod remaps the controller's clip tables so items
  5..10 draw one slot lower and draws "Jukebox" in slot 5; the list-cursor hook (`0x2C42D0` from `0x4D093C`) runs a
  12-item visual list while the game's own cursor stays on Customization when Jukebox is highlighted; the confirm
  hook (`0x2C3ED0`) opens our screen. Labels: `0x4570E0` renames `$Main5..10 -> $Main6..11`; slot 11's text fields
  are misnamed copies (`DT_Button_Main0_mc`) - the text registry hook (`0x4535B0`) fixes the path.
- The description line belongs to the **information bar's** movie (`[exe+0x34D6780]+0x20`), written via `0x4D27A0
  -> 0x4C9B40` = text variable `$InfoText0` + `_root.RefreshScroll` - only on cursor changes, not every frame.

## 14. Our screens: the game's dialog and the Controller Setup movie

- **Playlist screen** = the game's generic dialog: `h = 0x26BDC0(menu)`, message `0x2A1AD0(h, text)`, layout
  `0x2A1AB0(h, 0)` (big rows), raw button `0x2A1980(h, text, index, false, -1)`, open `0x2A18E0(h, 0, 2, true)`,
  cursor/result `dlg+0xE4`, finished `+0xE9`, decided `+0xEA`, destroy `0x556440(menu, h)`. **Max 6 big rows** (a
  7th crashed in another mod) - hence one RANDOM row cycled with Left / Right, relabelled live through
  `$button_big_text<n>` with `0x458020` on the dialog's movie (`dlg+0x88`).
- Hiding the main menu: items `Off`, `SubMenu_mc Off`, News `End`/`Off`, information bar `0x4C9A70(bar, 0, 1)`,
  button guide `0x45C310([exe+0x34D5D38], 0)`, Player Information panel (its own movie; object captured from its
  refresh `0x507BD0`) `End`.
- **Playlist Editor** = our own instance of `SW_UI_ControllerSetup` (two lists, a top row with arrows, 19 rows,
  dialog): `0x4D9190([exe+0x34D67D8], owner = the main menu's coroutine context, path, layer 0xA, true, 0)`; visible
  after `gotoAndPlay "Start"` on `_root.Title_mc / ListArea1_mc / ListArea2_mc`; unload `0x4DA630`. Rows are
  relabelled on scroll (the movie has no scrollbar). None of Controller Setup's logic runs - only its movie.
- Movie-clip positions: the ScaleformUI player UObject `[wrapper+0x50]`, `GetPosition` vtbl `+0x2B0`,
  `SetPosition` `+0x2B8`; `GetMovieClip` (`0xF42F10`) walks paths from the root, so drop a leading `_root.`.
- Speaker icon: each row's `Rep_BtnIcon_mc` shows external image `Rep_btnIcon_NN` on frame `BTNnn`;
  `SwfBase::setExternalTexture` `0x458380(w, UTexture *, name)` with a texture loaded by `StaticLoadObjectInternal`
  `0x93E580` (class may be null) - here `SW_UI_OnlineTournament_Result/TalkIcon`.
- Background video scene: `SwfBackMovie` `[exe+0x34D5D00]`, scene table `0x343D430` (index = position + 1; 11 =
  Gallery), play `0x44FAF0`, preload `0x44F7F0`, fade `0x44F9B0`.

## 15. Scaleform from C++: Invoke, members, the GFx::Value layout

- The movies are **AS3** (AS2 names like `_y` return undefined; use `y`, `text`, `htmlText`, `textWidth`).
- GFx Movie thunks: `Invoke` `0x1DBFDC0(movie, "path.method", GVal *result, const GVal *args, unsigned n)`; the
  movie = `0xF42E80([wrapper+0x50])`.
- **This build's GFx::Value is 0x30 bytes**: `+0/+8` list links, `+0x10` ObjectInterface*, `+0x18` type, `+0x20` data.
  Types: 1 null, 2 bool, 3 int, 4 uint, 5 number (double), 6 string, 7 wide string, 8 object, 9 array, 10 display
  object; flag `0x40` = managed (release it via the ObjectInterface).
- Members: `Invoke("<clip>.getChildAt", [0])` returns the clip's first child (a text field inside a `DT_*_mc`
  clip); ObjectInterface vtbl `+0x20` GetMember, `+0x28` SetMember, `+0x10` release.
- **A managed string's data is a pointer to the string node, whose first field is the `const char *` text** (reading
  `data` as `char *` gives garbage).
- All of this runs inside SEH guards: an exception switches the feature off and logs it instead of crashing.

## 16. Text, fonts and non-Latin names

- `SetHtmlText` on a `DT_*_mc` clip = the movie's AS3 text code: it applies the language's font to the **whole**
  field (read back: `FACE="BNSUCGothicLatintk7CS M"`), dropping any `<font face>` inside, and each write nudges the
  field 0.05 px up (the mod pins the field's `y`).
- Fonts live in `UI_common/flash/fontlib/gfxfontlib` (14 DefineFont3). Movies name them by their **SymbolClass**
  names: `$Frutiger_Neue_LT_Pro_Condensed` (412 glyphs, Latin), `$UCGothicLatin_M/DB/B` (Latin + Cyrillic + Greek),
  `$UCGothic_M/DB/B` (BNSUCGothictk7CS: kana, 7187 kanji, Hangul, Cyrillic), `$UCGothicBIG5_M/DB/B` (FZLanTingHei:
  15352 hanzi), `$NewCinema_A`, `$Frutiger_LT_Arabic_*`. A face given by its DefineFont name does nothing.
- Non-Latin names: `tools/gen_font_cover.py` writes which code points each font has (`src/font_cover.hpp`, ranges
  only). After `SetHtmlText`, the mod reads the field's `htmlText` back, wraps runs the field's font cannot draw in
  `<font face="$UCGothic_M">` (or `$UCGothicBIG5_M`) inside the game's own markup, and sets `htmlText` directly.
  The information bar applies its text a frame or more later, so its field is re-checked every frame while such a
  name is shown (the wrap is idempotent).
- Single-line fields drop everything after `<br>`, `\n` or `<p>`; `<textformat tabstops='[x]'>` + `\t` works (the
  right-aligned note in the editor's bar). Icon tags `<#view>`, `<#y>`, `<#lsb>` ... (59 in the exe) render per
  controller when written through the bar / guide setters with flag `0x400`.

## 17. Information bar and button guides

- Information bar: one text field, `_root.InfoArea_mc.Info_Text_mc.Info_Text_L_mc.Info_Text_L0_mc.DT_Info_L0_mc`
  (`$InfoText0`; L1/L2 are ticker copies). The field autosizes to its text, so its `width` is not the bar width
  (usable text width at 1080p: 1720 px).
- Button guides: `SwfButtonHelp` `[exe+0x34D5D38]`, show `0x45C310(obj, bool)`, set by id `0x45C470(obj, id, 0,0,0)`
  (sprintf of `<#tag> label` pairs into `$Text` via `0x458250` on `[obj+0x20]`, variants `+0x28` / `+0x30`). The game
  **squeezes** a guide line that is wider than its box (not via any clip scale, `textAutoSize` or the field's
  `scaleX` - inside its text pipeline). To get one size on every row: widen the guide field by 800 px and scale it
  once by `(1662.2 / 1720) * 1720 / <widest row's natural width>`, measured after a re-layout.

## 18. Input

- Menu pad word: `0x3ED5F0([exe+0x34D5B78], &out, 2)` - per-frame press bits in the XInput layout: d-pad 0..3,
  Start `0x10`, View `0x20`, L3 `0x40`, LB `0x100`, RB `0x200`, A `0x1000`, B `0x2000`, X `0x4000`, Y `0x8000`.
  Keyboard and other pads arrive in the same word. Held state (for repeat): record 2 word `+0x94` of
  `[exe+0x34CE510]`.
- Hold-to-repeat: 270 ms delay, then every 70 ms; a repeat never wraps around the list ends.

## 19. Background video (CRI USM)

- Menu videos are loose `Content/Movies/Ui/*.usm`: CRI Mana, Sofdec Prime (codec 1), 1920x1080, 30 fps, video only.
  The exe has no H.264 / VP9 decoder for USM.
- **The game's USM video packets are encrypted** (every `@SFV` data packet after its first 0x40 bytes; chained
  XOR with two 32-byte masks, mask1 = ~mask2). A plain encode plays as black. The masks were recovered
  statistically (most common byte per column of the chained region); `tools/usm_crypt.py recover` does that from any
  game video you own, then `encrypt` prepares your encode. The mod itself contains no key: the shipped video is
  pre-encrypted.
- Playback: on Jukebox open the mod plays the Gallery scene (scene 11) and its `CreateFileW` hook serves
  `t7jukebox\Jukebox Background.usm` for `Gallery.usm`; on leaving, the saved main-menu scene plays again. Without
  the file, Gallery's own video shows.

## 20. Safety: hook checks, bad files, recovery

- Prologue bytes of every hooked function are compared first; a mismatch in a core hook (open, read, play_bgm,
  set_volume) keeps the whole mod off, others disable only their feature. Logged.
- Bad files: an mp3 / wav / player-decoded file that fails to load is remembered (path + size + mtime) and the
  game's music plays for the rest of the match; a loose `.wem` is checked first (Vorbis -> Wwise, PCM / ADPCM ->
  player, anything else -> not served).
- Recovery: if the game leaves the main menu by itself while a Jukebox screen is open (menu rebuild, or a music
  request from a stage while the menu is stale), every screen state is dropped and the music unmuted.
- Logs: `t7jukebox\t7jukebox.log` + 4 previous sessions, 4 MB cap; `t7jukebox\debuglog.txt` enables detail lines.

## 21. What did not work (and why)

- **Pre-reading the bank through the platform file at boot** -> crash. Patch it in the read hook instead.
- **Swapping a prefetch Sound's media** -> click + silence (section 5).
- **Inserting a real 12th main-menu item** -> would shift the global mode index every other mod and the game use.
- **Two lines in the stage list's top row**: `<br>`, `\r`, `\n`, `<p>` all drop the rest; `&nbsp;` forced wrap shows
  line 1 only -> the overview moved to the information bar.
- **Fixing text-field drift by position**: ScaleformUI `GetPosition` returns (0,0) for text fields; re-creating the
  field drifts too; AS2 `_y` is undefined (AS3!). Working fix: pin the inner text field's `y` via `getChildAt(0)`.
- **A wrong GFx::Value size** (0x20 assumed) crashed the editor -> it is 0x30 in this build.
- **Guide size**: scaling the field, `textAutoSize`, the parent clip, no-break-space padding, a 200 px wider box -
  all failed (the squeeze is internal); the +800 box with one measured scale works.
- **`<font face="<DefineFont name>">`** for CJK did nothing; the SymbolClass name is needed, and `SetHtmlText`
  overwrites it anyway -> read-back + re-wrap.
- **Reading the background video through ReadFile** to decrypt it: the buffers are reused raw (decryption happens
  on a copy) -> recover the masks from the files instead.
- **Keyboard polling for dev hotkeys** is deaf while the game has focus; a Ctrl+numpad hotkey crashed the game in
  its own code -> dev triggers were files in `t7jukebox\`.
- **Converting user songs into the bank** (the classic pak approach) needs a new pak per change and a restart - the
  reason this mod serves files at runtime instead.

## 22. Source map

| File | Contents |
|---|---|
| `src/main.cpp` | init, hooks (play_bgm, volume, IO open / read / close, pak find, PostEvent), playlist logic, Random, preview, credits parts |
| `src/library.hpp` | stage / scene table, game song list (`kVanillaTracks`), Jukebox Songs scan, settings (INI) load / save, Song Loops template |
| `src/bank.hpp` | AkBankBGM / Init.bnk in-flight patches, BGM media id set |
| `src/player.hpp` | the mod's audio player (XAudio2), Wwise PCM / ADPCM decoding, bad-file memory |
| `src/gamefile.hpp` | reading `.wem` from the game's paks (v3 index, AES) |
| `src/exporter.hpp`, `src/export_media.hpp` | L3 export |
| `src/mainmenu.hpp` | main-menu entry, information bar, button guides, Scaleform helpers |
| `src/playlists.hpp` | playlist screen (game dialog), Random behaviour dialog |
| `src/editor.hpp` | Playlist Editor (Controller Setup movie): stage list, Song Browser, preview, export, guides |
| `src/background.hpp` | background video |
| `src/html_text.hpp`, `src/font_cover.hpp` | HTML text + fallback fonts |
| `src/unused_tracks.hpp` | the Bonus Tracks list |
| `src/proxy_*`, `src/proxy.def` | the multi-name proxy |
| `src/decoders.cpp` | dr_mp3 / dr_wav implementation unit |
