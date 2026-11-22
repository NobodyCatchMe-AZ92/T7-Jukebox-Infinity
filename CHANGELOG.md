# Changelog

## 1.1 - Song Sets

- **New Feature**: Song Sets - every stage and menu of a Custom playlist has 5 song sets, each with its own Round 1,
  Final Round (and Special) songs and volumes. Choose the set with Left / Right in the Stage Selector.
- **New Feature**: Random Set - plays one of the stage's assigned sets at random every match / menu visit, keeping
  each set's Round 1 and Final Round songs together. The help bar shows the sets it picks from ("Random Set - 1, 3").
- **New Feature**: "No Song (Unassigned)" in the Song Browser (Sets 2-5): an unassigned slot plays Set 1's song; an
  unassigned set plays Set 1.
- The stage list's "*" moved to the left of the stage name; Reset Stage / Reset All clear all song sets.
- Existing playlists become Set 1 automatically - nothing to redo. T7Jukebox.ini keeps its format (new lines only
  for Sets 2-5 and the set selection).

## 1.0 (first public release)

- Jukebox entry on the main menu (between Customization and Gallery) with a playlist screen and a Playlist Editor
  built from the game's own menus.
- Playlists: Tekken 7 Default, Custom 1-3, Random (All / Custom / Folder: any folder, Tekken 7 Default, Tekken 7
  Bonus Tracks); Random behaviour: one song per match or a new song at match point.
- Per stage: Round 1 and Final Round songs; Special slot for Lars' theme (Twilight Conflict) and Leroy's theme
  (Dragon's Nest); 4 menu scenes (Main Menu, Character Select, Online Warm-Up, Customization).
- Songs: the game's whole soundtrack (with official titles), 89 Bonus Tracks found in the game files, and your own
  .mp3 / .wav / .wem in folders; "Random: <folder>" assignments.
- Song preview and loop preview, per-assignment volume (0-300%), loop points for mp3 / wav (Song Loops.txt),
  L3 export of game songs as .wem, View opens the songs folder, X refreshes folders.
- Non-Latin song names in the game's Japanese / Chinese / Korean fonts.
- Optional Jukebox background video (main download).
- Works under the proxy names winmm / version / dsound / xinput1_3 / dinput8; only one copy runs.
- Safety: game code checked before hooking; broken files fall back to the game's music; logs with 4 previous
  sessions; music pak mods do not interfere.
