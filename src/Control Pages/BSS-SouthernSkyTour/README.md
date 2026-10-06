# Southern Sky Tour (SST)

Control page: **BSS-SouthernSkyTour**. Example show: an evening on the ground at Aoraki,
with the galactic centre high overhead (mid-July, 22:00 NZST).

## Running order

| File | Reference name | Button label | Length |
|---|---|---|---|
| `00-BSS-SST-Setup.txt` | `BSS-SST-Setup` | Setup | ~6 s |
| `10-BSS-SST-MilkyWayIntro-40.txt` | `BSS-SST-MilkyWayIntro-40` | Milky Way (40s) | 40 s |
| `20-BSS-SST-SouthernCross-60.txt` | `BSS-SST-SouthernCross-60` | Southern Cross (60s) | 60 s |
| `99-BSS-SST-PlayAll.txt` | `BSS-SST-PlayAll` | ▶ Play all | ~110 s |

## Presenter notes

- Live show: press **Setup**, then each segment in order, talking over it.
- Automated: press **Play all**.
- Needs the **BSS-Lib** page loaded in the workspace (Setup calls `BSS-Lib-SetupGround`).

## Requirements

- No external files. Everything is created with `Scene Add` and removed afterwards.
