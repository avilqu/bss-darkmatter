# Southern Sky Tour (SST)

Control page: **BSS-SouthernSkyTour**. Example show: an evening on the ground at Aoraki,
with the galactic centre high overhead (mid-July, 22:00 NZST).

## Running order

| File | Reference name | Button label | Length |
|---|---|---|---|
| `00-setup.dm` | `BSS-SST-Setup` | Setup | ~6 s |
| `10-milkyway-intro-40.dm` | `BSS-SST-MilkyWayIntro-40` | Milky Way (40s) | 40 s |
| `20-southern-cross-60.dm` | `BSS-SST-SouthernCross-60` | Southern Cross (60s) | 60 s |
| `99-play-all.dm` | `BSS-SST-PlayAll` | ▶ Play all | ~110 s |

## Presenter notes

- Live show: press **Setup**, then each segment in order, talking over it.
- Automated: press **Play all**.
- Needs the **BSS-Lib** page loaded in the workspace (Setup calls `BSS-Lib-SetupGround`).

## Requirements

- No external files. Everything is created with `Scene Add` and removed afterwards.
