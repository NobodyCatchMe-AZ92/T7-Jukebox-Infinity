==========================================================================================
  JUKEBOX INFINITY  -  VERSION 1.1
  A Jukebox for TEKKEN 7 (PC / Steam)
  by t7jukeboxauthor  -  check for updates at tekkenmods.com and nexusmods.com
==========================================================================================

Choose the music for every stage and menu in Tekken 7 - from the game's own soundtrack, 89 bonus
tracks hidden in the game files, and your own .mp3 / .wav / .wem songs. Everything is set up in a
Jukebox menu inside the game, on the main menu between Customization and Gallery.

TIP: every section below has a tag like [S5]. Search this file (Ctrl+F) for the tag to jump to it.


CONTENTS
--------
  [S1]  What Jukebox Infinity does
  [S2]  Requirements
  [S3]  Installing  (main download or LITE)
  [S4]  Uninstalling
  [S5]  Quick start - your first custom song in 2 minutes
  [S6]  Playlists
  [S7]  The Playlist Editor
  [S8]  Song Sets - several song pairs per stage, chosen or played at random
  [S9]  Controls (all Jukebox screens)
  [S10] Adding your own songs
  [S11] Loop points
  [S12] Making .wem files
  [S13] Volume
  [S14] The game's own songs, Bonus Tracks and exporting them
  [S15] Random songs on one stage ("Random: <folder>")
  [S16] When each song plays (rounds, match point, character themes)
  [S17] The settings file (T7Jukebox.ini)
  [S18] Online play and other mods
  [S19] Troubleshooting
  [S20] Log files and bug reports
  [S21] Files the mod creates
  [S22] Credits and license


------------------------------------------------------------------------------------------
[S1] WHAT JUKEBOX INFINITY DOES
------------------------------------------------------------------------------------------
- Adds a "Jukebox" entry to the main menu (between Customization and Gallery).
- 1 default + 3 custom playlists + Random playlists. Exactly one playlist is active at a time and
  it applies everywhere: offline, online, in every mode.
- Two songs per stage, like the PS4 version's Jukebox: one for the early rounds ("Round 1") and one
  from match point onward ("Final Round"). Twilight Conflict and Dragon's Nest get a third slot for
  Lars' and Leroy's character themes ("Special").
- Songs for the 4 menu scenes too: Main Menu, Character Select, Online Warm-Up and Customization.
- Song Sets: up to 5 sets of songs per stage and menu (e.g. two carefully matched Round 1 + Final
  Round pairs), with a Random Set option that plays one of your sets at random each match.
- Use the game's own songs (every stage, menu, boss, story, credits and Tekken Bowl track), 89
  Bonus Tracks (unused / beta / alternate songs found in the game files), or your own songs:
  .mp3, .wav and .wem, organised in folders.
- Song preview with loop preview, a volume setting per song (0-300%), loop points for mp3 / wav.
- Random playlists: random songs from everything, from your songs only, or from one folder - plus
  "Random: <folder>" assignments for single stages.
- The game's sound files are never changed. Everything happens in memory while the game runs:
  remove the mod's DLL and the game is exactly as before.

What the mod does NOT include: any of the game's music. The Tekken 7 songs and Bonus Tracks are
read from YOUR game's own files while you play.


------------------------------------------------------------------------------------------
[S2] REQUIREMENTS
------------------------------------------------------------------------------------------
- TEKKEN 7 on Steam, updated to the final version.
- Windows 10 or 11 (64-bit).
- Nothing else to install - no Cheat Engine, no pak files, no loader.

Safety check: when the game starts, the mod first checks that the game code it needs is exactly
what it expects. If it is not (a different game version, or another mod patching the same code),
Jukebox Infinity stays switched off and writes the reason into its log ([S20]). The game then runs
as normal.


------------------------------------------------------------------------------------------
[S3] INSTALLING
------------------------------------------------------------------------------------------
Two downloads - pick ONE:

  Jukebox_Infinity_v1.1.zip        The full mod, with the custom Jukebox background video.
  Jukebox_Infinity_LITE_v1.1.zip   The same mod without the video (smaller download). The
                                   Jukebox screens then show the game's Gallery video instead.

1. Open your game folder:  Steam > right-click TEKKEN 7 > Manage > Browse local files.
2. Go into  TekkenGame\Binaries\Win64  (the folder with TekkenGame-Win64-Shipping.exe).
3. Copy everything from the zip's "Win64" folder into that folder:

     Win64\winmm.dll                                  the mod
     Win64\Jukebox Songs\                             your songs go here (contains a short guide)
     Win64\t7jukebox\Jukebox Background.usm           the background video (main download only)

4. Start the game. "Jukebox" appears on the main menu, between Customization and Gallery.

Adding the video later (LITE users): copy "t7jukebox\Jukebox Background.usm" from the main
download into Win64\t7jukebox\ and restart the game.

Already using a mod called winmm.dll? The mod works under several file names - rename
winmm.dll to ONE of these (just never to a name another mod in the folder already uses):

     winmm.dll   version.dll   dsound.dll   xinput1_3.dll   dinput8.dll

Note: T7 Ghost AI uses dinput8.dll, ReShade uses dxgi.dll - keep winmm.dll if you use those.
Only one copy of Jukebox Infinity ever runs, even if two copies are installed by accident.


------------------------------------------------------------------------------------------
[S4] UNINSTALLING
------------------------------------------------------------------------------------------
Delete winmm.dll (or whatever you renamed it to) from TekkenGame\Binaries\Win64. That's all:
the game's music, files and saves were never changed.

To remove everything, also delete (all in the same folder):
  T7Jukebox.ini      your playlists and settings
  t7jukebox\         the background video and the log files
  Jukebox Songs\     your songs (keep it if you want them)


------------------------------------------------------------------------------------------
[S5] QUICK START - YOUR FIRST CUSTOM SONG IN 2 MINUTES
------------------------------------------------------------------------------------------
1. Copy an .mp3 into TekkenGame\Binaries\Win64\Jukebox Songs.
2. Start the game, highlight "Jukebox" on the main menu, press A.
3. Pick CUSTOM PLAYLIST 1 > "Edit Playlist".
4. Pick a stage (e.g. Mishima Dojo) > ROUND 1.
5. In the Song Browser, press LB / RB until you see the "Uncategorized" folder, highlight your song,
   press Y to hear it, then A to assign it.
6. Press B back to the playlist list, pick CUSTOM PLAYLIST 1 > "Make CUSTOM PLAYLIST 1 the Active
   Playlist".
7. Play a match on that stage.

(Song not listed? It was added while the game was running - press X in the Playlist Editor to
refresh the folders.)


------------------------------------------------------------------------------------------
[S6] PLAYLISTS
------------------------------------------------------------------------------------------
Main menu > Jukebox opens the playlist screen. The active playlist is marked "(ACTIVE)".

  TEKKEN 7 DEFAULT      The game's normal music. (This is the setting after installing.)
  CUSTOM PLAYLIST 1-3   Your own choice of song for every stage and menu. Anything you leave
                        empty plays the game's normal music.
  RANDOM (...)          A random song for every match and every menu visit. Press Left / Right
                        on this row to choose what it picks from:

    RANDOM (ALL)                               the game's songs + all your songs
    RANDOM (CUSTOM)                            only your songs (everything in Jukebox Songs)
    RANDOM (FOLDER: <name>)                    only the songs of one of your folders
    RANDOM (FOLDER: Tekken 7 Default)          only the game's own songs
    RANDOM (FOLDER: Tekken 7 Bonus Tracks)     only the Bonus Tracks ([S14])

  (The Bonus Tracks are only in their own Random option, never in RANDOM (ALL).)

Press A on a playlist:
  - "Make <PLAYLIST> the Active Playlist" switches to it at once.
  - "Edit Playlist" (Custom 1-3 only) opens the Playlist Editor ([S7]).

Random behaviour - press X on the playlist screen to choose:
  - "One Random Song for the Entire Match"   (default)
  - "A New Random Song for the Final Round"  (a second random pick at match point)

The music goes quiet while you are in the Jukebox screens (so you can preview songs) and comes
back when you leave, already using your new settings.


------------------------------------------------------------------------------------------
[S7] THE PLAYLIST EDITOR
------------------------------------------------------------------------------------------
LEFT: the Stage Selector - all 29 stages (incl. DLC stages and day / night versions) and the menu
scenes Main Menu, Character Select, Online Warm-Up and Customization.
  - A "*" left of a stage name means it has music of its own in this playlist (in any song set).
  - The right column shows the stage's song set: Set 1 ... Set 5 or Random Set. Change it with
    Left / Right ([S8]).
  - The bar at the bottom shows the highlighted stage's songs in the selected set:
    "Set 1:   Round 1: ...  |  Final: ...".

Press A on a stage to choose what to change in its selected song set:
  ROUND 1                     the song for the early rounds
  FINAL ROUND                 the song from match point onward ([S16])
  SPECIAL - LARS' THEME       Twilight Conflict (Day / Evening) only ([S16])
  SPECIAL - LEROY'S THEME     Dragon's Nest only ([S16])
  Reset Stage to Default      back to the game's music on this stage - all 5 song sets are
                              cleared and Set 1 is selected again
(Menu scenes have one song, so A goes straight to the Song Browser. A does nothing on a stage set
to Random Set - pick one of its sets first to edit it.)

RIGHT: the Song Browser.
  - The top row is the folder. Change it with LB / RB (from anywhere) or Left / Right on that row.
    Folders: "Tekken 7" (the game's songs), "Tekken 7 Bonus Tracks", "Random" ([S15]), then your
    own folders, then "Uncategorized" (songs directly in Jukebox Songs).
  - "Default (game music)" = the game's normal song for this slot.
  - "No Song (Unassigned)" (first song of the Tekken 7 folder, Sets 2-5 only) = leave this slot of
    the set empty ([S8]).
  - "*" marks the song currently assigned to this slot.
  - The volume column: Left / Right changes the highlighted song's volume in 5% steps (hold to
    repeat). The volume is saved with the assignment when you press A.
  - Y previews the song from the start; Y again stops. HOLD Y to preview the loop: playback jumps
    to a few seconds before the loop end, so you hear the song wrap around.
    A speaker icon shows which song is previewing.
  - Long names scroll when highlighted.
  - A assigns the highlighted song (with its volume) and returns to the Stage Selector.

Other buttons in the editor:
  X       Refresh Folders - reads Jukebox Songs again (new / renamed / deleted songs and folders).
  View    (Back / Select) opens the Jukebox Songs folder in File Explorer.
  Start   (on the Stage Selector) Reset All - every stage and menu of this playlist (all song sets)
          back to default.
  L3      (Tekken 7 and Bonus Tracks folders) export the song as a .wem file ([S14]).

If an assigned song file no longer exists, the bar shows "(!!!!ERROR: MISSING FILE!!!!)" next to
it and the game's music plays there until you assign something else.


------------------------------------------------------------------------------------------
[S8] SONG SETS - SEVERAL SONG PAIRS PER STAGE
------------------------------------------------------------------------------------------
Every stage and menu of a Custom playlist has 5 song sets. Each set is a complete choice of music
for that stage: its own Round 1, Final Round (and Special) songs, each with its own volume.

Example: on Arena, Set 1 = a Round 1 song and a Final Round song that belong together, Set 2 = a
second matching pair. Choose "Random Set" and every match on Arena plays one of the two pairs - the
Round 1 and Final Round songs of a pair always stay together.

Choosing the set:
  - In the Stage Selector, highlight the stage and press Left / Right. The right column shows the
    selection: Set 1, Set 2, Set 3, Set 4, Set 5 or Random Set. It is saved at once.
  - The selected set is the one that plays - and the one you edit with A.
  - Random Set picks one of the stage's assigned sets at random for every match / menu visit. The
    bar shows which sets it picks from, e.g. "Random Set - 1, 3".

Filling a set:
  - Select the set, press A and choose songs as usual. The Song Browser's title shows the set
    (e.g. "Arena - Round 1 - Set 2").
  - Set 1 always has music: what you choose, or the game's music. It is the same as the stage's
    songs before Song Sets existed, so older playlists keep working unchanged.
  - Sets 2-5 start out UNASSIGNED (empty). A set counts as assigned as soon as one of its slots has
    a song - "Default (game music)" counts too.
  - "No Song (Unassigned)", the first song of the Tekken 7 folder in Sets 2-5, empties a slot again.

What plays when something is unassigned:
  - An unassigned set that is selected plays Set 1 (the bar says "Set 2: Unassigned - Set 1 plays").
  - An unassigned slot inside an assigned set plays Set 1's song for that slot (the bar shows
    "Set 1's song"). Example: Set 2 with only a Round 1 song uses Set 1's Final Round song.
  - Random Set ignores unassigned sets. With only Set 1 assigned it always plays Set 1.

Resetting:
  - Reset Stage to Default clears all 5 sets of the stage and selects Set 1 again.
  - Reset All (Start) does that for every stage and menu of the playlist.

The "*" left of a stage name shows that any of its sets differs from the defaults.


------------------------------------------------------------------------------------------
[S9] CONTROLS (ALL JUKEBOX SCREENS)
------------------------------------------------------------------------------------------
Xbox button names, PlayStation in brackets. On keyboard, use the keys you have mapped to these
buttons in the game's own controls.

  Main menu      A (Cross) on "Jukebox"                  open the Jukebox

  Playlists      Up / Down                               select a playlist
                 A (Cross)                               open the playlist's options
                 Left / Right on the RANDOM row          choose what Random picks from
                 X (Square)                              Random behaviour
                 B (Circle)                              back to the main menu

  Stage Selector Up / Down (hold to scroll)              select a stage
                 A (Cross)                               choose Round 1 / Final Round / ...
                 Left / Right                            change the stage's song set ([S8])
                 Start (Options)                         Reset All
                 X (Square)                              Refresh Folders
                 View / Back (Share)                     open the Jukebox Songs folder
                 B (Circle)                              back to the playlists

  Song Browser   Up / Down (hold to scroll)              select a song
                 A (Cross)                               assign the song
                 Y (Triangle)                            preview / stop
                 hold Y (Triangle)                       preview the loop
                 Left / Right (hold to repeat)           song volume  (on the folder row: folder)
                 LB / RB (L1 / R1)                       previous / next folder
                 L3                                      export (Tekken 7 / Bonus folders only)
                 X (Square)                              Refresh Folders
                 View / Back (Share)                     open the Jukebox Songs folder
                 B (Circle)                              back to the Stage Selector

The button guide at the bottom of the screen always shows the buttons of the current panel.


------------------------------------------------------------------------------------------
[S10] ADDING YOUR OWN SONGS
------------------------------------------------------------------------------------------
Where:   TEKKEN 7\TekkenGame\Binaries\Win64\Jukebox Songs
Formats: .mp3, .wav and .wem (see [S12] for .wem).

Folders:
  - Every folder directly inside Jukebox Songs is a folder in the Song Browser, e.g.
      Jukebox Songs\Tekken 3\
      Jukebox Songs\Tekken Tag Tournament 2\
  - Songs in deeper folders (Jukebox Songs\Tekken 3\Arcade\) are listed in their top folder.
  - Songs directly in Jukebox Songs are listed under "Uncategorized".
  - The folder "!EXPORTS" is ignored by the Song Browser ([S14]).

Names: the Song Browser shows the file name - name your files the way you want to see them
("Tekken 3 - Jin Kazama.mp3"). File extensions can be hidden: ShowFileExtensions=0 in [S17].
Japanese, Chinese, Korean and Cyrillic names are shown in the game's own fonts for those
languages.

Added songs while the game is running? Press X (Refresh Folders) in the Playlist Editor.

Renamed / moved / deleted a song that is assigned somewhere? The editor marks it as a missing file
and the game's music plays there until you assign it again (assignments are saved by the song's
path inside Jukebox Songs).

A song that cannot be played (an empty or broken file, an unsupported .wem): the game's own music
plays instead for that match, and the log says which file it was ([S20]).


------------------------------------------------------------------------------------------
[S11] LOOP POINTS
------------------------------------------------------------------------------------------
Songs loop until the music changes, like the game's own songs.

.mp3 / .wav - use "Song Loops.txt" in the Jukebox Songs folder (the mod creates it, with
instructions and two examples). One entry per song: the file name, then the loop start and end
as MINUTES:SECONDS.MILLISECONDS, then a blank line:

    Tekken 3 - Jin Kazama.mp3
    LoopStart=0:12.530
    LoopEnd=3:04.257

  - The song plays from the very beginning, and from LoopEnd it jumps back to LoopStart.
  - Without an entry, the whole song loops.
  - Entries match by file name, in any folder. If two entries have the same name, the first wins.
  - Delete Song Loops.txt and the mod creates a fresh one with the instructions.

.wem - the loop points stored inside the .wem are used ([S12]).

Check a loop: HOLD Y on the song in the Song Browser.


------------------------------------------------------------------------------------------
[S12] MAKING .WEM FILES
------------------------------------------------------------------------------------------
Do you need .wem? Usually not: .mp3 and .wav work just as well, with loop points in
Song Loops.txt. Use .wem when you already have them (BGM packs made for other Tekken 7 music
mods, music from other Wwise games) or want the game's own audio engine to play your songs.

How the mod plays a .wem:
  - Wwise Vorbis .wem (what Tekken 7 itself uses): played by the game's own audio engine.
  - PCM / ADPCM .wem: played by the mod's own player. (The .wem files from L3 export are such.)
  - Anything else: not played - the game's music stays, and the log names the file.

BGM packs from other Tekken 7 music tools: copy their .wem files into Jukebox Songs (a folder per
pack works well). The ".stub" files that come with some packs are not needed.

Making your own Vorbis .wem with Audiokinetic Wwise (free for non-commercial use):
  1. Install Wwise through the Audiokinetic Launcher. Tekken 7 uses a 2016 version of Wwise, so a
     Wwise 2016 version is the safest choice; files from much newer versions may not play.
  2. Prepare a 48 kHz stereo .wav. For loop points, set loop markers in the WAV with an audio editor
     that writes them (a "smpl" loop, e.g. Wavosaur).
  3. In a new Wwise project, import the .wav (Project Explorer > Audio > Default Work Unit >
     Import Audio Files) and tick "Loop" in the sound's General Settings.
  4. Give it a Vorbis conversion: Conversion Settings > Vorbis (any quality).
  5. Convert it (right-click the sound > Convert). The .wem appears in the project folder under
     .cache\Windows\SFX\ with a random-looking name - rename it (e.g. "My Song.wem") and copy it
     into Jukebox Songs.
  6. Check it in game: Y to preview, hold Y to hear the loop.

A .wem plays but is silent / does not loop right? Convert the song to .mp3 or .wav instead and set
its loop in Song Loops.txt - that always works.


------------------------------------------------------------------------------------------
[S13] VOLUME
------------------------------------------------------------------------------------------
- Each assignment has its own volume (0-300%, 100% = the file as it is), set in the Song
  Browser with Left / Right before pressing A. The same song can be quiet on one stage and loud
  on another.
- Random picks (Random playlists, "Random: <folder>" assignments) play at 100%, or at the
  volume you set for that song in the [Volume] section of T7Jukebox.ini ([S17]):
      [Volume]
      Tekken 3 - Jin Kazama.mp3=60
  Write the file name, or its path inside Jukebox Songs if two songs have the same name.
- The game's own Music volume setting (Options > Sound) applies on top, as for the game's songs.


------------------------------------------------------------------------------------------
[S14] THE GAME'S OWN SONGS, BONUS TRACKS AND EXPORTING THEM
------------------------------------------------------------------------------------------
Folder "Tekken 7": every song of the game, with its official title - all stage songs (1st / 2nd),
the menu themes of every season, the character / boss themes (Kazumi, Akuma, Lars, Leroy, NJPW),
the story mode tracks, Tekken Bowl (Ball Wall, Fever Night), and the credits songs (Aloneness and
The Long Goodbye, as separate songs). Assign any of them to any stage or menu.

Folder "Tekken 7 Bonus Tracks": 89 tracks that are in the game files but never (or hardly ever)
play in the game - beta / location-test versions, alternate mixes, unused songs. They have
their own Random option ([S6]) and are not part of RANDOM (ALL).

Export (L3): on a song in the Tekken 7 or Bonus Tracks folder, press L3 > Yes. The song is saved
as a .wem file into Jukebox Songs\!EXPORTS. Use it to build your own folders of game songs, for
example a "Dojo Remixes" folder for a "Random: Dojo Remixes" stage assignment ([S15]): move the
exported files from !EXPORTS into a folder of your own. (The !EXPORTS folder itself is not shown in
the Song Browser.) The credits songs export as one file ("Aloneness + The Long Goodbye").

The game's songs are read from your own game files; exports are for your own use.


------------------------------------------------------------------------------------------
[S15] RANDOM SONGS ON ONE STAGE ("RANDOM: <FOLDER>")
------------------------------------------------------------------------------------------
In a Custom playlist, a slot can play a random song from a folder instead of one fixed song:
in the Song Browser, go to the "Random" folder and assign "Random: <folder name>"
(e.g. "Random: Tekken 4", "Random: Tekken 7", "Random: Uncategorized").

  - A new pick for every match / every visit of a menu.
  - Round 1 and Final Round both set to the same "Random: <folder>" follow the Random behaviour
    ([S6]): one song for the whole match, or a new song at match point.
  - Picks play at 100% or at their [Volume] entry ([S13]).
  - Y on a "Random:" row previews a random song from it.
  - If the folder is gone, the bar shows "(!!!!ERROR: MISSING FOLDER!!!!)" and the game's music
    plays.


------------------------------------------------------------------------------------------
[S16] WHEN EACH SONG PLAYS
------------------------------------------------------------------------------------------
Which songs: in a Custom playlist, the stage's selected song set - or, with Random Set, one of its
assigned sets picked for this match ([S8]).

Round 1 / Final Round: the Round 1 song plays from the start of the match. The Final Round song
starts at match point - the round where either player can win the match - exactly where the game
switches to its own second song. On stages that have no second song in the game, your Final Round
song still starts at match point.

The same song in Round 1 and Final Round simply keeps playing at match point (at the Final Round
slot's volume).

Special (Lars' and Leroy's themes): when Lars fights on Twilight Conflict (Day / Evening), or Leroy
on Dragon's Nest, the game plays their character theme at match point. The Special slot chooses
what plays then. Left on Default, the game's character theme plays - not your Final Round song.

Menu scenes: Main Menu, Character Select, Online Warm-Up (the warm-up stage while you wait for an
online match) and Customization.

Where it works: the stage and menu music of all modes - for example Arcade, Versus, Practice,
Treasure Battle, Ghost Battle, online matches and replays. Scenes with scripted music of their
own (story cutscenes and the like) keep their music.


------------------------------------------------------------------------------------------
[S17] THE SETTINGS FILE (T7Jukebox.ini)
------------------------------------------------------------------------------------------
TekkenGame\Binaries\Win64\T7Jukebox.ini is written by the Jukebox menu; you never have to edit it.
Changes made by hand while the game runs are picked up at the next song change.

[Jukebox]
  Playlist=                    Default | Custom 1 | Custom 2 | Custom 3 | Random (All) |
                               Random (Custom Only) | Random (Folder)
  RandomFolder=                the folder for Random (Folder): a folder name inside Jukebox Songs,
                               "Tekken 7 Default" or "Tekken 7 Bonus Tracks"
  RandomSwitchAtMatchPoint=    0 = one random song for the whole match, 1 = a new one at match point
  ShowFileExtensions=          1 = show .mp3 / .wav / .wem in the menu, 0 = names only

[Custom 1] / [Custom 2] / [Custom 3]   one line per stage and slot, e.g.
  0.Early=Tekken 4\Airport.wem        Mishima Dojo, Round 1 (paths inside Jukebox Songs)
  0.Final=bgm:1                       Mishima Dojo, Final Round = a game song
  0.EarlyVolume=80                    (written when not 100)
  4.Special=...                       Twilight Conflict Lars' theme slot
  Empty = the game's music. A comment above each stage gives its name.
  The lines above are Set 1. Song Sets ([S8]):
  31.Set=Random                       Arena: the selected set (2..5 or Random; no line = Set 1)
  31.Set2.Early=My Songs\A.mp3        Arena, Set 2, Round 1 (Set2 .. Set5; same slot names)
  31.Set2.Final=default               "default" = the game's music
  A slot of Sets 2-5 without a line is unassigned.

[Volume]
  <file name or path>=0..300           the volume of a song when it is picked at random ([S13])


------------------------------------------------------------------------------------------
[S18] ONLINE PLAY AND OTHER MODS
------------------------------------------------------------------------------------------
Online: the music is only on your PC - your opponent hears their own music and is not affected.
The mod changes nothing about the fight itself.

Music pak mods (.pak files in Content\Paks\~mods that replace the game's music): while Jukebox
Infinity is installed, their MUSIC is ignored and the game's original music is used, so the
Jukebox always knows what is playing. Everything else in those paks (and all other pak mods)
works as normal. To keep using songs from such a mod, put its .wem files into Jukebox Songs and
assign them ([S12]).

Other DLL mods: works together with T7 Ghost AI (dinput8.dll) and ReShade (dxgi.dll). If another
mod also uses the name winmm.dll, rename Jukebox Infinity ([S3]).


------------------------------------------------------------------------------------------
[S19] TROUBLESHOOTING
------------------------------------------------------------------------------------------
No "Jukebox" on the main menu
  - Is winmm.dll in TekkenGame\Binaries\Win64 (next to TekkenGame-Win64-Shipping.exe), not in the
    TEKKEN 7 folder itself?
  - Is there a file t7jukebox\t7jukebox.log in that folder? No log = the DLL was not loaded:
    another mod may use the name winmm.dll - rename ours ([S3]).
  - Log says the game code "is not what Jukebox Infinity expects": the game is not the final Steam
    version, or another mod changes the same game code.

My song is not in the Song Browser
  - Press X (Refresh Folders). Check the extension (.mp3 / .wav / .wem) and that the song is not
    in Jukebox Songs\!EXPORTS. Songs in deeper folders are listed in their top folder.

My song does not play in the match / the game's music plays instead
  - Is the right playlist ACTIVE ([S6])? Editing a playlist does not make it active.
  - Is the song in the right slot? Round 1 plays until match point ([S16]).
  - The file may be broken or an unsupported .wem - the log names it ([S20]). Try playing it in a
    media player, or convert it to .mp3.
  - The bar shows "MISSING FILE"? The song was renamed / moved: assign it again.

A .wem is silent or does not loop properly
  - See [S12]. Convert it to .mp3 / .wav and set the loop in Song Loops.txt.

The loop of my mp3 / wav is wrong
  - Check the entry in Song Loops.txt: exact file name (with .mp3 / .wav), MINUTES:SECONDS.MILLI-
    SECONDS, a blank line between entries ([S11]). Hold Y to test.

A song is too loud / too quiet
  - Fixed songs: Left / Right in the Song Browser, then A. Random picks: [Volume] ([S13]).

My music pak mod stopped working
  - Expected - see [S18].

The Jukebox screens show the Gallery video instead of the Jukebox video
  - You have the LITE version, or t7jukebox\Jukebox Background.usm is missing ([S3]).

No sound from mp3 / wav after changing the audio device (headphones / speakers)
  - The mod follows the Windows default device; if it does not recover, restart the game.

Song names show white boxes
  - The game's fonts cover Latin, Japanese, Chinese, Korean and Cyrillic. Other alphabets cannot
    be shown. Known gap: a folder name in those alphabets shows boxes on the playlist screen's
    "RANDOM (FOLDER: ...)" row (the Song Browser shows it fine).


------------------------------------------------------------------------------------------
[S20] LOG FILES AND BUG REPORTS
------------------------------------------------------------------------------------------
The log: TekkenGame\Binaries\Win64\t7jukebox\t7jukebox.log (this session). The 4 sessions before
are kept as t7jukebox.previous1.log (the last one) to t7jukebox.previous4.log. Each log is at most
4 MB.

More detail for a bug report: create an empty file named  debuglog.txt  in the t7jukebox folder,
restart the game, reproduce the problem, and include t7jukebox.log (and T7Jukebox.ini) in your
report. Delete debuglog.txt afterwards.

Please describe: what you did, what you expected, what happened - and which playlist, stage and
song (file type) were involved.


------------------------------------------------------------------------------------------
[S21] FILES THE MOD CREATES
------------------------------------------------------------------------------------------
All in TEKKEN 7\TekkenGame\Binaries\Win64:
  T7Jukebox.ini                     your settings and playlists
  Jukebox Songs\                    your songs (created if missing)
  Jukebox Songs\Song Loops.txt      loop points for mp3 / wav (created if missing)
  Jukebox Songs\!EXPORTS\           songs exported with L3
  t7jukebox\                        log files (and the background video)

The mod never writes to the game's own files, saves or settings.


------------------------------------------------------------------------------------------
[S22] CREDITS AND LICENSE
------------------------------------------------------------------------------------------
Jukebox Infinity by t7jukeboxauthor. Built with the help of Claude (Anthropic's AI assistant,
Claude Code), which did the reverse engineering and programming together with the author.

Thanks to the Tekken 7 modding community, whose earlier work showed the way:
  - ThePaSch's T7 Jukebox tool - and xRuneXero and Ressen_XiaoPai for the stage music ID lists, and
    Gneiss for finding the music bank's encryption key, credited there.
  - Dr.Shadowds' Cheat Engine table, which revealed the PS4 Jukebox hidden in the PC game.

Third-party code inside winmm.dll (licenses in THIRD_PARTY_LICENSES.txt):
  - MinHook by Tsuda Kageyu (BSD 2-Clause)
  - dr_mp3 and dr_wav by David Reid (Unlicense / MIT No Attribution)

Jukebox Infinity is free software under the MIT license; the source code is published on GitHub.
TEKKEN is a trademark of Bandai Namco Entertainment Inc. This is an unofficial fan-made mod, not
affiliated with or endorsed by Bandai Namco.
