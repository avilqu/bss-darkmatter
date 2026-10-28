# Virtual Stargazing (VS)

Control page: **BSS-VirtualStargazing** (site Mt Cook, user Theater). Automated show narrated by a
recorded voiceover, one button per chapter. No text on the dome.
Names: references `BSS-VS-<What>`, assets `<Name>-BSS-VS`. Needs the **BSS-Lib** page loaded.

## Buttons

| File | Reference name | Button label | Length | Starts from → ends with |
|---|---|---|---|---|
| `00-BSS-VS-Setup.txt` | `BSS-VS-Setup` | Setup | 12 s | anything → 1000 km above Aoraki, dim sky, real time, logo up; loads BSS-VS-Seq and BSS-Lib-LoadAssets (Milky Way image, Earth 16K, LocalGroup, Vol Milky Way, LEDA) |
| `01-BSS-VS-LoadSeq.txt` | `BSS-VS-LoadSeq` | Load BSS-VS-Seq | ~0.5 s | loads the JS sequencer (generated, see below) |
| `02-BSS-VS-ForceMoon.txt` | `BSS-VS-ForceMoon` | Moon: auto | 0.2 s | cycles auto → on → off |
| `03-BSS-VS-ForcePlanets.txt` | `BSS-VS-ForcePlanets` | Planets: auto | 0.2 s | cycles auto → on → off |
| `04-BSS-VS-ForceCore.txt` | `BSS-VS-ForceCore` | Core: auto | 0.2 s | cycles auto → on → off |
| `05-BSS-VS-CheckSky.txt` | `BSS-VS-CheckSky` | Check sky | 0.1 s | logs what chapter 2 would play now |
| `06-BSS-VS-StopSeq.txt` | `BSS-VS-StopSeq` | Stop chapter | 0.1 s | stops the sequencer (chapter 2 or Play all) before the next segment or chapter |
| `07-BSS-VS-PlayAll.txt` | `BSS-VS-PlayAll` | Play all | ~20–22 min | Setup → end of ch. 9 (runs chapters 1–9 through BSS-VS-Seq, see below) |
| `10-BSS-VS-DarkSkies.txt` | `BSS-VS-DarkSkies` | 1 Dark skies | ~112 s | Setup → ground at Mt Cook Village, bright sky, logo off |
| `20-BSS-VS-DistancesAndPerspective.txt` | `BSS-VS-DistancesAndPerspective` | 2 Distances | ~90–200 s | ground, bright sky → same (runs 21–26) |
| `21-BSS-VS-Dist-Intro.txt` | `BSS-VS-Dist-Intro` | 2.1 Intro | ~10 s | ground, bright sky → same |
| `22-BSS-VS-Dist-Moon.txt` | `BSS-VS-Dist-Moon` | 2.2 Moon | ~18 s | same → same |
| `23-BSS-VS-Dist-Planets.txt` | `BSS-VS-Dist-Planets` | 2.3 Planets | ~12 s | planets normal → **planets enlarged** |
| `231`…`235-BSS-VS-Dist-<Planet>.txt` | `BSS-VS-Dist-Mercury` … `-Saturn` | 2.3 \<Planet\> | ~11 s each | enlarged → enlarged |
| `239-BSS-VS-Dist-PlanetsEnd.txt` | `BSS-VS-Dist-PlanetsEnd` | 2.3 Planets end | 4 s | enlarged → normal |
| `24-BSS-VS-Dist-Stars.txt` | `BSS-VS-Dist-Stars` | 2.4 Stars | ~41 s | bright sky → **stars hidden** |
| `25-BSS-VS-Dist-Core.txt` | `BSS-VS-Dist-Core` | 2.5 Core | ~17 s | stars hidden → same |
| `26-BSS-VS-Dist-Magellan.txt` | `BSS-VS-Dist-Magellan` | 2.6 Magellan | ~37 s | stars hidden → bright sky, stars back |
| `30-BSS-VS-CelestialNav.txt` | `BSS-VS-CelestialNav` | 3 Celestial nav | ~95 s | ground, bright sky, real time → same |
| `40-BSS-VS-Constellations.txt` | `BSS-VS-Constellations` | 4 Constellations | ~149 s | ground facing south, bright sky, real time → same (cuts to 10 Jul 2026 for Scorpius, back to Now) |
| `50-BSS-VS-VirtualTelescope.txt` | `BSS-VS-VirtualTelescope` | 5 Virtual telescope | ~150 s | ground, bright sky, real time → same, facing south |
| `60-BSS-VS-SouthernLights.txt` | `BSS-VS-SouthernLights` | 6 Southern lights | ~84 s | ground facing south, bright sky, real time → **in space** ~22,000 km above 70° N, camera still (next chapter must land) |
| `70-BSS-VS-Moon.txt` | `BSS-VS-Moon` | 7 Moon | ~223 s | in space, bright sky, real time → **in space** 10,000 km above the Moon's far side, sky at ~next New Moon (**not real time**), Moon scale 1 (next chapter must reset time) |
| `80-BSS-VS-SolarSystem.txt` | `BSS-VS-SolarSystem` | 8 Solar system | ~144 s | end of ch. 7 (above the Moon) → **in space** ~20 AU from the Sun in the ecliptic plane, camera parented to Ecliptic, **planet orbits on**, real time, Moon scale 1 |
| `90-BSS-VS-MilkyWay.txt` | `BSS-VS-MilkyWay` | 9 Milky Way | ~172 s | end of ch. 8 → **in space** 200 million ly from the Sun, camera parented to Galactic, **still orbiting** (Longitude.Rate 2), LEDA galaxies and Vol Milky Way on, Visible Milky Way off (Setup resets all of it) |

Chapter timings are estimates until the voiceover is recorded (see `media.md`).

## Chapter 2: conditional segments

The Moon, planet and galactic-core parts only make sense when those objects are up, so chapter 2 is split
into segments 21–26, each with its own voiceover file. Each one states what it starts from and ends with, so
any subset chains cleanly. The `2 Distances` button starts the **BSS-VS-Seq** JS engine
(`src/JavaScript/BSS-VS-Sequencer.js`), which:

1. computes the altitude of the Moon, Mercury–Saturn and Sgr A* from the **PC clock** and the Aoraki position
   (its own low-precision ephemeris, checked against astropy to within 0.4°);
2. picks the segments: `auto` = Moon/planet above 10°, core above 15°; `on` = above the horizon; `off` = skip.
   The toggles 02–04 cycle these; Setup resets them to auto, so set them after Setup;
3. runs 21 Intro, [22 Moon], [23 Planets, one 231–235 per planet up, 239 PlanetsEnd], 24 Stars, [25 Core],
   26 Magellan, waiting each segment's length (table `LEN` in the JS) + 0.5 s;
4. logs every decision in Event Viewer > JavaScript Processor (`BSS-VS-Seq: ...`).

The same engine also serves chapter 7: `MoonView(offset, alt, a, c, d)` sends the camera to the point of
Earth opposite the Moon (from the PC clock), `offset` degrees north, so the Moon shows above the north limb.

After changing a segment length, update `LEN` in the .js and regenerate the loader:

    tools/wrap-js.sh src/JavaScript/BSS-VS-Sequencer.js BSS-VS-Seq BSS-VS-LoadSeq BSS-VirtualStargazing \
        > "src/Control Pages/BSS-VirtualStargazing/01-BSS-VS-LoadSeq.txt"

Testing another time: the engine uses the PC clock, not the DM sky time. In a ScriptPad, run
`JS BSS-VS-Seq.SetTestOffset(5)` (hours ahead; `0` to go back) and press Check sky.

Limits: the chapter length varies, and `2 Distances` returns at once (the JS keeps running), so a master Play
button can't use a fixed `+N` after it. That's why **Play all** is in the JS too, below. The Playlist Creator can't render chapter 2 as a whole (JS waits);
single segments are fine.

## Play all

`07 Play all` calls `PlayShow(1)` in **BSS-VS-Seq**: it runs each chapter button, waits its length from the
table `CHAPTERS` in the .js (+0.5 s), and plays the chapter 2 segments itself. Press Setup first. "Stop chapter"
ends it before the next chapter; `JS BSS-VS-Seq.PlayShow(N)` in a ScriptPad restarts from chapter N.
After changing a chapter's waits, update its length in `CHAPTERS` (the total on the button's last comment line)
and regenerate the loader as above. Not renderable as a whole with the Playlist Creator.
