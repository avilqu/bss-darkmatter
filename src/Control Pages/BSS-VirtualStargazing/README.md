# Virtual Stargazing (VS)

Control page: **BSS-VirtualStargazing**. Automated show (rendered with the Playlist Creator or
played with a Play button) on the ground at Aoraki, in four seasonal versions.

Names: references `BSS-VS-<What>[-<seconds>]`, assets `<Name>-BSS-VS`.

## Page layout (filename numbers)

| NN | Use |
|---|---|
| `01`–`04` | Seasonal Setup buttons (location, date/time, fade in) |
| `10`–`89` | Segments, in running order. A segment used only in some seasons goes in the season tables below. |
| `90` | End (fade out, stop time) |
| `95`–`98` | Play buttons, one per season |

## Buttons

| File | Reference name | Button label | Length |
|---|---|---|---|
| `01-BSS-VS-SetupSpring.txt` | `BSS-VS-SetupSpring` | Setup Spring | 6 s |
| `02-BSS-VS-SetupSummer.txt` | `BSS-VS-SetupSummer` | Setup Summer | 6 s |
| `03-BSS-VS-SetupAutumn.txt` | `BSS-VS-SetupAutumn` | Setup Autumn | 6 s |
| `04-BSS-VS-SetupWinter.txt` | `BSS-VS-SetupWinter` | Setup Winter | 6 s |
| `90-BSS-VS-End.txt` | `BSS-VS-End` | End | 4 s |
| `95-BSS-VS-PlayAllSpring.txt` | `BSS-VS-PlayAllSpring` | Play Spring | ~10 s |
| `96-BSS-VS-PlayAllSummer.txt` | `BSS-VS-PlayAllSummer` | Play Summer | ~10 s |
| `97-BSS-VS-PlayAllAutumn.txt` | `BSS-VS-PlayAllAutumn` | Play Autumn | ~10 s |
| `98-BSS-VS-PlayAllWinter.txt` | `BSS-VS-PlayAllWinter` | Play Winter | ~10 s |

Seasonal dates (placeholders, about 2 h after sunset, NZ time; scripts use UTC):

| Season | Local | UTC |
|---|---|---|
| Spring | 2026-10-15 21:30 NZDT | 2026/10/15 08:30:00 |
| Summer | 2027-01-15 23:15 NZDT | 2027/01/15 10:15:00 |
| Autumn | 2027-04-15 20:30 NZST | 2027/04/15 08:30:00 |
| Winter | 2027-07-15 20:00 NZST | 2027/07/15 08:00:00 |

## Running order per season

Each Play button runs Setup<Season> → segments → End. For a Playlist Creator render, add the same
buttons one by one with these delays (nested `Run()` and JS waits are not rendered).

| # | Spring | Summer | Autumn | Winter | Length |
|---|---|---|---|---|---|
| 1 | SetupSpring | SetupSummer | SetupAutumn | SetupWinter | 6 s |
| … | *(segments TBD)* | | | | |
| last | End | End | End | End | 4 s |

## Rules for this page

- Segments carry their own timing (no `Control Pause`); all waits are DM `+N` (no JS waits, no nested `Run()`).
- Segments are self-contained: Remove → Add → animate → Remove, assets suffixed `-BSS-VS`.
- A segment may assume a Setup has run (ground at Aoraki, time frozen) and must leave time frozen.
- Setup inlines `BSS-Lib-SetupGround` rather than calling it, so it renders. Keep both in sync.

## Requirements

- No external files yet (see `media.md`).
