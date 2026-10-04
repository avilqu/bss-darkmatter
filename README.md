# bss-darkmatter

Dark Matter (Sky-Skan DigitalSky) button scripts and show pages for BSS.
Git is the source of truth; Dark Matter is the deploy target.

Assumes DM 1.6+, content drive `E:\DigitalSkyDM` (`<ContentPath>`).

## Layout

| Folder | In Dark Matter | Purpose |
|---|---|---|
| `lib/` | control page **BSS-Lib** | Small set of shared buttons every show may call (setup, reset, JS loader). Keep it stable. |
| `js/` | JS engine source | Source of JS engines. `tools/wrap-js.sh` turns them into loader buttons in `lib/`. |
| `shows/<show>/` | one control page per show | Self-contained segment buttons + setup + play-all. |
| `snippets/` | nothing | Copy-paste templates. Never called directly. |
| `assets/` | `<ContentPath>\Assets\BSS\` | Small images / SRTs. Large video lives on the content drive, not in git. |
| `exports/` | File > Export | Periodic `.dmz` backups of the control pages. |
| `tools/` | — | Helper scripts run on the dev machine. |

## Conventions

- **One file per button.** File header gives the Reference Name, the page and the button label.
- **Reference names:** `BSS-<Page>-<What>[-<seconds>]`, e.g. `BSS-SST-MilkyWayIntro-40`.
  Page codes: `Lib` = BSS-Lib, `SST` = Southern Sky Tour.
- **Asset names** created by scripts end with `-BSS-<Page>` (e.g. `GCLabel-BSS-SST`) so pages never collide.
- **Filenames:** `NN-name-seconds.dm` in shows (NN = running order), plain names in `lib/`.
- **Segments are self-contained:** Remove → Add → animate → Remove. They must run correctly on their own or from play-all.
- Every `Control Pause` is preceded by `Control Text="..."`; each button resets its own caption when done.
- Cross-page calls to BSS-Lib use the full path `Control SITE.USER.BSS-Lib.<RefName>.Run()`.
  **Replace `SITE.USER` with your real Site and User names** (Control Page Manager) — it is a deliberate placeholder.
  The BSS-Lib page must be loaded in every workspace that uses it.

## Deploying a change

1. Edit the `.dm` file here.
2. In DM, open the button's ScriptPad, select all, paste, save. Set the Reference Name from the file header.
3. If the change was made in ScriptPad on the dome PC, copy it back here the same day.
4. Every so often export the pages to `exports/` (File > Export) and commit.

For JS engines: edit `js/<engine>.js`, then run `tools/wrap-js.sh` (see its header) and paste the regenerated `lib/load-*.dm`.
