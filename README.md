# bss-darkmatter

Dark Matter (Sky-Skan DigitalSky) button scripts and show pages for BSS.
Git is the source of truth; Dark Matter is the deploy target.

Assumes DM 1.6+, content drive `E:\DigitalSkyDM` (`<ContentPath>`).

## Layout

The repo mirrors Dark Matter's own folders, so files map 1:1 to the dome PCs.

| Folder | On the dome | Purpose |
|---|---|---|
| `Sites/Mt Cook/<User>/` | `<ContentPath>\Sites\Mt Cook\<User>\` | **Native copy from the dome**, byte-identical (GUID names, XML headers, CRLF). Users: `Theater`, `Operator`, `Richard`. Copy back to restore. Don't hand-edit. |
| ↳ `Control Pages/<Page>_<GUID>/` | same | `<GUID>.xml` = page layout; `WIDGETBUTTON*_<uuid>.txt` = one button (XML `DMScriptHeader` + script); `Button Images/`. |
| ↳ `JavaScript/<GUID>/JS_<uuid>.txt` | same | JS engines (same header format). |
| ↳ `Workspaces/<Name>.xml` + `Script for <Name>` | same | Workspace layouts and their startup scripts (extensionless). |
| ↳ `Shows/`, `Public/`, `Preferences.xml` | same | Shows (`.dms`), shared items, user prefs. |
| `src/Control Pages/<Page>/` | one control page | **Hand-written source**: `NN-<RefName>.txt`, pasteable into ScriptPad. `BSS-Lib` = shared buttons; one folder per show page. |
| `src/JavaScript/` | JS engine source | `.js` sources; `tools/wrap-js.sh` turns them into loader buttons in `src/Control Pages/BSS-Lib/`. |
| `src/Workspaces/` | startup scripts | `Script for <Workspace>.txt` we write (paste via File > Workspaces > Edit Startup Script). |
| `src/Snippets/` | nothing | Copy-paste templates. Never called directly. |
| `Assets/BSS/` | `<ContentPath>\Assets\BSS\` | Small images / SRTs. Large video lives on the content drive, not in git. |
| `config/` | `C:\ProgramData\Sky-Skan\DigitalSkyDM\` | DS-Master config (DMSettings, network, renderheads). See `config/README.md`. |
| `exports/` | File > Export / Import | `.dmz` control-page and workspace packages. |
| `tools/` | — | `build-page.py` (src → .dmz), `pull-page.py` (dome → src), `wrap-js.sh`. |
| `build/` | — | Build output, not in git. |

## Conventions

- **One file per button.** File header gives the Reference Name, the page and the button label.
- **Reference names:** `BSS-<Page>-<What>[-<seconds>]`, e.g. `BSS-SST-MilkyWayIntro-40`.
  Page codes: `Lib` = BSS-Lib, `SST` = Southern Sky Tour.
- **Asset names** created by scripts end with `-BSS-<Page>` (e.g. `GCLabel-BSS-SST`) so pages never collide.
- **Filenames:** `src/Control Pages/<Page>/NN-<RefName>.txt` (NN = running order on the page).
- **Segments are self-contained:** Remove → Add → animate → Remove. They must run correctly on their own or from play-all.
- Every `Control Pause` is preceded by `Control Text="..."`; each button resets its own caption when done.
- Cross-page calls to BSS-Lib use the full path `Control SITE.USER.BSS-Lib.<RefName>.Run()`.
  **Replace `SITE.USER` with your real Site and User names** (Control Page Manager) — it is a deliberate placeholder.
  The BSS-Lib page must be loaded in every workspace that uses it.

## Deploying a page

A page is a folder `src/Control Pages/<Page>/` with `NN-<RefName>.txt` buttons (filename order =
grid order) and a `page.json` holding the DM site/user, page GUID, and each button's widget ID and
position. `page.json` is created by the first build and **must be committed**: DM and workspaces
know the page and buttons by those IDs.

1. Write or edit the button `.txt` files. First line `;=== <RefName> ===`, second line has `Button: "<label>"`.
2. Build: `tools/build-page.py "src/Control Pages/<Page>"` → `build/<Page>.dmz` (not in git; rebuild any time).
   New pages default to site `Mt Cook`, user `Operator` (`--user Theater` to change on the first build).
   Positions: edit `left`/`top` in `page.json`, or move buttons in DM and pull.
3. Commit (`src/` + `page.json`), copy the `.dmz` to DS-Master, File > Import.
4. Copy any media to every PC (see the page's `media.md`).

**Updating an existing page** (until the BSS-Test checklist says otherwise): DM seems to import a
page that already exists as a renamed copy with a new GUID (`Jack20230922034335_…` on the dome).
So either delete the page in DM before importing, or paste changed buttons into ScriptPad by hand,
or (DM closed) copy `build-page.py --folder` output over the page folder in `<ContentPath>\Sites`.

**Edits made on the dome** go back to git with
`tools/pull-page.py "src/Control Pages/<Page>" --from <Sites\Mt Cook folder or exported .dmz>`
(`--dry-run` first). It pulls script edits, moved buttons and buttons added on the dome; it only
warns about deleted buttons and sliders/labels (which the build does not create).

Single buttons in other pages: paste the `.txt` into ScriptPad, set Name and Reference Name from the
header, save; bring dome-side changes back the same day. Export pages to `exports/` now and then.

For JS engines: edit `src/JavaScript/<Engine>.js`, then run `tools/wrap-js.sh` (see its header) and paste the regenerated loader button from `src/Control Pages/BSS-Lib/`.

## Syncing the native copy

`Sites/` and `config/` are snapshots of the dome, refreshed by copying the whole folders from the
master PC (or a backup drive) and committing. `.gitattributes` keeps them byte-exact.
