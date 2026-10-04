---
name: "darkmatter-scripting"
description: "Write, debug and structure DigitalSky Dark Matter (Sky-Skan planetarium) button scripts, JavaScript engines and dome shows. Use for any Dark Matter / DigitalSky scripting or show-building question."
---

# DigitalSky Dark Matter — scripting & show-building reference

Knowledge compiled from a full read of the DSA Dark Matter community forum (darkmatter.digitalskyacademy.com, ~2,300 posts, 2018–Oct 2026, DM 1.1 → 1.7), mainly answers from Sky-Skan staff (Markus Steblei, Beth Moger, Troy Whitmer, Glenn Smith, Sascha) and Jeff Nee (Sky-Skan content developer, ex-JPL). Sky-Skan has no public scripting manual; the forum and the in-app Help/Asset Manager are the de facto docs.

## How to help the user

1. Before writing non-trivial code, find out (or state assumptions about): DM version (Help > About; 1.4 added Playlist/rendering + SRT, 1.5 Spout/alpha-slides, 1.6 middle-mouse page drag, 1.7 JS file I/O), single-PC/portable vs multi-channel dome, and the content drive (`<ContentPath>` is usually `E:\DigitalSkyDM`, sometimes D: or C:).
2. Deliver scripts as one plain-text block ready to paste into a button's ScriptPad, commented with `;`, self-contained (Scene Add / Scene Remove rather than relying on Asset Manager assets the user may not have), with unique asset names carrying an org/show prefix (e.g. `-ORG`).
3. Always build in timing (`+X` waits and `[a:c:d]` transitions), fade-in/out, and cleanup. Put `Control Text="..."` before every `Control Pause`.
4. Flag anything unverified (property names not seen on the forum) and tell the user the reliable way to get exact syntax: drag the property name from the Asset Manager into the ScriptPad.
5. Remind about the multi-PC rule when files are involved: every media/image file must exist at the same path on every renderer (and on DS-Master and the sound PC for audio/video).

## 1. Architecture & vocabulary

- **Master/UI (DS-Master)** runs the interface; **renderers** (DS-01…DS-nn) each drive projectors; a **sound PC** may play audio. The Viewport mirrors the dome.
- **Assets** = everything in the universe (planets, slides, media, cameras, JS engines…). Shown in the **Asset Manager** (folders, properties). Sky-Skan folders are locked/protected — to edit, drag an asset into your own folder, then click the link icon ("break the chain") to make an independent copy, rename (Information section), save.
- **Control Pages** = pages of **buttons** (scripts), sliders, picture buttons, info widgets. The **Bridge** is the always-present default control panel. Workspaces hold layouts; each workspace has a **Startup Script** (File > Workspaces > Edit Startup Script; stored as "Script for…" files under `<ContentPath>\Sites\<Site>\<User>`).
- Each button has a **Name** (label) and a **Reference Name** (used by `Control Ref.Run()`); make reference names unique (template `ORG-Show-ButtonText`).
- **ScriptPad** = script editor (Ctrl+F find/replace, ESC closes search). **Direct Command** window runs one-off commands. **Event Viewer** (Windows menu) has Renderers tab (missing files: "Unable to load texture") and JavaScript Processor tab (JS errors, `LogMessage` output).
- **Dataset Explorer (DSE)** = presenter-friendly browser of astronomy datasets. **Online Data Center (ODC)** (Tools menu) downloads comets/asteroids/exoplanets; drag a list row onto a control page to auto-generate a load/unload button; folder icon creates assets under protected "Exoplanet Systems"/"Comets".
- DMZ = zip package (control page or asset group or content); File > Import / Export. Imported control pages land in a new user folder (Control Page Manager).
- Key paths: Sites `E:\DigitalSkyDM\Sites`, assets `E:\DigitalSkyDM\Assets\…`, core content `<ContentPath>\Core\…`, HTML pages `<ContentPath>\Core\HTML\…`, config `C:\ProgramData\Sky-Skan\DigitalSkyDM\` (DMSettings.xml, `<Site>\<PC>\renderheads.xml`, Logs, Defaults\Targets). Legacy DS2 aliases still work: `<ShowPath>`=E:\DigitalSky\Shows, `<SndPath>`=E:\DigitalSky\Sound, `<SvPath>`=E:\DigitalSky\SkyVision, `<DataPath>`=E:\DigitalSky\Data. Custom aliases can be added in DMSettings.xml (`<ContentPath Index="2" Path="E:\…" Alias="FpPath" />`).
- Back up regularly: `C:\ProgramData\Sky-Skan`, `E:\DigitalSkyDM\Sites`, `E:\DigitalSkyDM\Assets` (+ any `E:\DigitalSky\Shows`, `Core\HTML` content). Export control pages periodically.

## 2. Script syntax fundamentals

**Routing prefix** (first word = destination): `Scene` (anything on the dome), `Assets` (Asset Manager load/unload), `Control` (control pages/buttons), `JS` (JavaScript engines), `SRT` (subtitle assets), `Kernel` (low-level render/system), `Remote` (UDP/device assets), `Spice` (SPICE automation), `DSE` (Dataset Explorer), `DirectCommand`.

- Comment: `;` at line start (also inline after a command). Not `//` (that's JS only).
- Wait: `+2` on its own line = wait 2 s before following lines. Commands between waits fire together. A script with no waits runs instantly.
- Property set: `Scene Asset.Property=value [timing]`; group form: `Scene Asset { Prop1=v Prop2=v } [timing]`.
- Relative change: `+=` / `-=` works on numeric properties and DateTime (`Scene mySlide.Azimuth+=180 [1:1:1]`).
- Rates: `Scene Obj.Zrot.Rate=10 [1::]` (deg/s, forever). `Scene DateTime.Rate=86400 [1::]` (s per s). Stop with `=0 [2::]`.
- Methods use parentheses: `.Play()`, `.Pause()`, `.Run()`, `.Abort()`, `.ConvertInPlace(...)`, `.FlyTo(...)`, `.NavOrbit(x,y)`, `.YawPitchRoll(y,p,r)`, `.Exposure.Clear()`, `.add(...)` (collections), `.RTZ()` (return to zero).
- Strings with spaces need quotes: `Inherit="Position Rotate Scale"`, `Slide.TextLock="Height to Width"`, file paths. (Dragging from the Asset Manager sometimes drops these quotes — add them back.)
- Asset names may contain spaces (`Scene Vol Milky Way.Visibility=80`) but avoid them in your own.
- Double quote inside a string: use two single quotes `''`. Newline in SlideText: `\n`.
- Colors: names (`White`, `Black`, `Yellow`, `Lime`), hex (`#E46C0A`, `#FFFFFFFF`), or `{ Red=100 Green=50 Blue=0 }` (0–100; these act like a filter — keep 100 for "normal").
- A blanked property sometimes needs a space: `Scene Moon.EffectSpec=" "` (1.6).

### Timing brackets `[a:c:d]`
- `[a:c:d]` = acceleration : constant : deceleration seconds; total duration = a+c+d. `[3]` = 3 s linear (abrupt start/stop). `[0]` = instant (default).
- For dome comfort prefer eased moves with long ramps: `[2:2:2]` over `[6]`, `[5:0:5]` over `[1:8:1]`, and longer settle `[4:3:8]`.
- Rate form `[w::]` = ramp up over w s then continue indefinitely. `[3:-1:-1]` = forever (older form). `NavOrbit/Throttle` use `C=-1` for forever.
- Overlap moves (start the next before the previous ends) for continuous flights; overlapping position moves blend, rotations don't — split position and rotation into separate commands with different durations (Troy's technique).
- Easing makes relative angles inexact (`YawPitchRoll(90,0,0) [1:1:1]` won't reach 90°); find the target with a linear move, then copy absolute Xrot/Yrot/Zrot.

## 3. Core commands

### Scene objects on the fly
```
Scene Remove(MySlide-ORG)
+0.1
Scene Add(MySlide-ORG, Slide, Visibility=0)
+0.1
Scene MySlide-ORG.Picture="<ContentPath>\Assets\ORG\image.png"
```
- Always Remove before Add (resets state); wait ≥0.1 s after Add, after ConvertInPlace/parent changes, and before modifying freshly loaded heavy files (large images/videos may need +1…+3). `Control WaitForAll(AssetName)` waits until an asset is loaded on all channels (timing then varies by system).
- Don't put strings containing commas inside `Scene Add(...)`; set them on the next line after the wait.
- `Scene Remove(A, B, C)` removes several; remove children before parents.
- Collections: `Scene Add(grp, Collection)` then `Scene grp.add(A, B, C)`; setting `grp.Visibility` etc. applies to members.

### Asset Manager assets
- `Assets Folder.Load(Asset)`, `Assets Folder.UnLoad(Asset)`, multiple: `Load(A, B, C)`, whole folder: `Assets Folder.Load()`.
- Fully qualified: `Assets Site.User.Folder.Load(X)` (e.g. `Assets Sky-Skan.Public.Trailers.Load(Asteroid_Trl)`).
- Parents load automatically with a child but do NOT unload automatically — unload them explicitly.
- `Assets Reset` resets everything (the Bridge "Assets Reset" button adds a fade + ~15 s of waits; copy and customise it rather than editing the original).
- Renaming an asset folder breaks scripts that reference it.

### Control
- `Control Text="Next: fly to Mars"` sets this button's caption; `Control Pause` waits for the presenter to click the button again.
- `Control RefName.Run()` / `.Abort()` start/stop another button. Run() is asynchronous (doesn't wait) — follow it with `+N` equal to that button's length. In recent versions it only reliably finds buttons on the same page; for other pages use the full path `Control Site.User.Page Name.RefName.Run()` (the page must be loaded in the workspace). After copying a button to a new page, edit+save it so its reference name registers.
- Bridge buttons are protected from page buttons; trigger them via JS `DigitalSky.SendScript("Control Bridge-AssetsReset.Run()")` after giving them a reference name.
- `Control Abort` aborts the current script. `Control RefName.Text="…"` sets another button's caption; `Control Site.User.Page.Widget.Picture=<path>` changes a picture widget.
- Sliders: drag a property name from the Asset Manager onto a page to auto-create a slider; `{f}` is the slider value (`Scene myObj.Xrot.Rate={f} [0.2::]`). Min/max/initial in Script Properties.

### Global scene
- `Scene Visibility=0 [1]` fades the whole realtime scene (also `Scene Scene.Visibility`). `Scene Camera.Visibility` fades the realtime layer only (use with fulldome video).
- `Scene FontName="Arial"` default label font (startup, before loading); per asset `Scene X.Text.Fontname="Georgia"`.

## 4. Time

- `Scene DateTime="2026/10/03 21:30:00"` (UTC; quotes when there's a space), `Scene DateTime=2461245.76` (Julian date), `Scene DateTime=Now` / `$Now`.
- Built-in variables: `$Sunrise $Sunset $SolarNoon $NextFullMoon $LastFullMoon $VernalEquinox/$SpringEquinox $SummerSolstice $AutumnalEquinox $WinterSolstice $JD2000`. Modifiers: `$Sunset+2h`, `$Sunrise-2h`, `$Sunset-1h-30m` (write one unit per term; `-1h30m` is parsed as −1h+30m). These pick the *next* event, so set a date first; `$SolarNoon` reported ~2 min off.
- Relative: `Scene DateTime+=1d [24]` (d, h, m, s, y; e.g. `+=12h15m`, `-=1y5d1h`). Rate: `Scene DateTime.Rate=86400 [1::]`, endless `Scene DateTime.rate+=7.2d`.
- Copy current time/location into a script: right-click empty area of the Bridge date/time (or location) widget, Ctrl+V in the script.
- `Scene Earth.RotationModel=Diurnal|Annual|Precess|None`: Annual removes daily spin (planets/Moon motion visible), Precess ≈ almost no rotation (Sun tracing ecliptic, precession), with `Scene Earth.AnnualReference="Sun"` (or "Moon" for monthly Moon motion). Always reset both to Diurnal/"Sun" afterwards. `Scene Earth.LookAt="Sun"` freezes the Sun in the sky.
- Stop time before changing the camera's rotation inheritance (`Scene DateTime.Rate=0 [2::]` +2, then ConvertInPlace).
- For reproducible views always set full space-time coordinates (date+time and camera position).
- Custom variables: JS `DigitalSky.AddVariable("Name","FuncName")` → use `$Name` (or `$Name+param`) in scripts; `DigitalSky.AddEventVariable(...)` adds to the date widget; `RemoveVariable` to clean up.

## 5. Camera & flying

- **Parent/attach:** `Scene Camera.ConvertInPlace(Earth, Position Rotate Scale)` re-parents the camera to Earth without jumping (inherits rotation → you stay over the same ground). `ConvertInPlace(Mars, Position)` = position only (good for time-lapses in space). Empty first arg keeps current parent: `ConvertInPlace(, "Position Rotate")`. ConvertInPlace breaks any motion in progress and rewrites rotation values.
- **Ground view:** `Scene Camera { Parent=Earth Orient=SouthAndUp SS.Elevation=90 Latitude=-43.7 Longitude=170.1 Altitude=500 }` ; here & now: `Latitude=$Here Longitude=$Here Altitude=$Here` + `Scene DateTime=$Now`.
- **Space flight by lat/long/alt** (most intuitive): set `Orient=SouthAndDown` first, then `Scene Camera { Latitude=0 Longitude=100 Altitude=5e6 } [3:3:8]`. Liftoff: `Scene Camera{Altitude=1e7} [4:3:8]` +1 `Scene Camera.Orient=SouthAndDown [3:3:8]` `Scene Camera.SS.Elevation=45 [3:3:8]`.
- Orient values: SouthAndUp (on ground), SouthAndDown (in space looking down at parent), Locked, LookAt (with `Camera.LookAt=X`), Free (any manual viewport nav or Xrot change sets Free → drift). Sweet spot: `SS.Elevation`, `SS.Azimuth` (use SS.Azimuth for dome offsets, not Camera.Zrot).
- **FlyTo:** `Scene Camera.FlyTo(Mercury, Altitude=1e7, Orient=SouthAndDown) [8:6:8]` then wait the full duration; `Scene Camera.FlyTo(Here, Orient=SouthAndUp)` returns to the observer location.
- **Exact keyframes:** fly in the viewport, then drag the Viewport's camera icon into the script → `Scene Camera { Xpos=… Ypos=… Zpos=… Xrot=… Yrot=… Zrot=… }`; add timing. Same date/time needed for identical views.
- **Recenter gently:** `Scene Camera.ConvertInPlace(Earth, Position)` +0.1 `Scene Camera.LookAt=Earth` +0.1 `Scene Camera.Orient=LookAt [2:2:2]`.
- **Orbit/fly rates:** prefer `Scene Camera.Longitude.Rate=1.5 [2::]`, `Latitude.Rate`, `Altitude.Rate` (positive = away). `Scene Camera.NavOrbit(x,y) [a:c:d]` and `Scene Camera.Throttle=-1e18 [10:10:0]` exist but are independent of the viewport navigator and can jump if mixed with manual flying; stop NavOrbit with `NavOrbit(0,0) [a::]`. Throttle is linear m/s (no log fly) — for log-style fly-ins use a JS loop that scales Altitude.
- Roll/turn: `Scene Camera.YawPitchRoll(0,0,22.5) [1:3:1]`; `Scene Camera.Zrot=180 [0]` flips dome orientation (sets Free).
- Avoid exactly 90° latitude (use 89.999) and crossing longitude ±180° while changing Orient (causes flips) — split Orient and Longitude changes into separate timed steps.
- Don't mix viewport navigation and scripted flights during a show.
- **Waypoints:** Virtual assets as fly-to targets, e.g. always arrive on the sunlit side: `Scene Add(SunLook, Virtual)` +0.1 `Scene SunLook { Parent=Mars Xpos=0 Ypos=0 Zpos=0 LookAt=Sun }` +0.1 `Scene Camera.ConvertInPlace(SunLook, Position Rotate)`.
- **Scale tricks** for smooth long flights: shrink origin/grow destination objects (`Scene Sun {Xscale=0.01 Yscale=0.01 Zscale=0.01} [1:1:1]`) instead of flying huge distances. Default Sun/Moon scale is 2.5 — set 1.0 for correct eclipses and shadows.
- **Second camera:** `Scene Add(Cam2, Camera, Visibility=0, Parent=Earth)`; parent the main Camera to it to use camera-only functions on a rig. Inset (picture-in-picture) camera: `Scene Add(CamTel, Camera, Parent=Camera, Type=Inset)` (set Type only inside Scene Add — changing it later crashed 1.4), show via a slide `Picture="Camera:CamTel"`, `Slide.Blend=Alpha`; FOV works on inset cameras only (no dome zoom). Planet clouds don't render in inset cameras (add a duplicate Planet or sphere).
- Viewport keys: R roll, Y yaw/pitch, Ctrl / Ctrl+Shift for finer moves.
- Camera.Exposure trails: `Scene Camera.Exposure=On`, `.Exposure.Clear()`, `.Exposure.addAsset(Stars)`, `.removeAsset(Sun)`, `.Exposure.Visibility=100 [1]`; 3D history trails use a Trail asset (Parent=observer, Follow=object, TrailLen).

## 6. Assets cookbook (common types & properties seen in working scripts)

- **Slide** (2D dome image): `Picture` (file or `Media:MediaAsset` or `Camera:CamName`), `Azimuth`, `Elevation`, `Width`, `Height`, `Rotation`, `Scale`, `Lens` (Standard, AllSky, Panorama/spherical), `Frame` (Dome default; `Sidereal` = fixed to stars, Azimuth=RA×15, Elevation=Dec), `Layer` (Background, Foreground, Chromo…), `Slide.Blend` (Color/Alpha), `Slide.TextLock="Height to Width"`, Visibility, Red/Green/Blue. Fade in by `Scale=0`→`1 [1:1:1]` or Visibility.
- **SlideText**: `Text.String`, `Text.TextColor`, `Text.BackgroundColor`, `Text.BackgroundVis`, `Text.Fontname`, `Scale` (animatable; ×10 ≈ FontHeight), `FontHeight` (default 10, not animatable), Azimuth/Elevation/Lens=AllSky.
- **Media** (video/audio source, never visible itself): `MediaFile`, `Looping=On` (bug: set Off, +0.1, On), `Volume` (0–100, fade `[1]`), `Seek=00:01:05.50`, `DSISpec`, `AudioFile`; methods `.Play()`, `.Pause()`. Show it on a Slide/plane/sphere via `Picture="Media:Name"` or `TopEmissiveMap="Media:Name"`.
- **Fulldome video layer** "Video" (Fulldome asset type): `Scene Video.Source="Media:Name"`, `Scene Video.Visibility=100 [1]`, `Scene Video.Layer=PreDisplay` (behind realtime), `Video.OverlayAsset` (one only). Unsliced fisheye on all channels: Media with `DSISpec` = `<ContentPath>\Core\Common\Fisheye.dsi` + Fulldome asset, or an AllSky slide (Az 180, El 90, Width 180) / camera-parented Hemisphere with `BottomEmissiveMap`. Sliced SkyVision content (per-renderer files with `_*` wildcards) plays best for 4K/60fps. Media widget controls whatever media is loaded into Video.
- **Primitives** (Sphere, Hemisphere, PlaneXY, PlaneXZ, RingPlane): `TopImage`/`BottomImage`, `TopEmissiveMap`/`BottomEmissiveMap`, `TopEmissive`/`BottomEmissive` (color), `TopColor`/`BottomColor`, `Solidness=Solid|Transparent`, `LightSource=Scene|Camera|Self`, Unit, X/Y/Zpos, X/Y/Zrot, X/Y/Zscale, Label.*. PlaneXZ parented to Camera with `LookAt=Camera` is a handy "3D slide" (Longitude=azimuth, Latitude=elevation, Altitude=distance). Overlay on Earth: Sphere parented to Earth, Unit=Megameter, scale ~6.4, TopEmissiveMap. 360 video: sphere parented to Camera, `BottomEmissiveMap="Media:…"`, Zpos=0.5 raises horizon (stills show pole artifacts — use 1-s video or a spherical-panorama slide).
- **Model** (OBJ+MTL, left-handed, triangulated; "Right Handed" loading property for others): `Model="path.obj"`, Parent, Unit, scale/rot/pos, `LightSource`, `Emissivity`, `LookAt`, `Controller1`/`Control1`. MTL: `map_Kd Media:Name` for video textures, `refl -type sphere textures\\EarthRefl_Soft.dds`, Ns (shininess), Kd (diffuse brightness). Reload: `Model=""` +0.1 `Model="path"`.
- **Virtual** (invisible null): positioning, LookAt, label anchor, camera target; nested virtuals (Longitude→Latitude→Distance) to place objects on a planet.
- **Planet / Sun / Comet / Orbit / OrbitController / SymbolController / Aurora / Light / Line / Trail / PView / Camera / Collection / Location** also addable. `Scene Add(X, Planet, Cloud.Altitude=0.01)` (1.6 requires non-zero cloud altitude).
- **Units:** M, KM, MM (= **megameter**, not millimetre; planets are in megameters), TM, AU / "Astronomical Unit", P (parsec), KP, MP, Lightyear, Kiloparsec, Megaparsec.
- **Coordinate frames:** Parent = origin of an object's coordinates. "World" is the fixed absolute frame (at Sun's centre, non-rotating); "Sun" rotates with time; EarthBC = Earth barycentre (doesn't spin), Earth = rotating globe; Equatorial, Ecliptic, Galactic in the Coordinate Systems group. 2D assets use `Frame=`, 3D assets use `Parent=`.
- **Stars:** single "Stars" asset (Milky Way folder) — pick individual stars with a SymbolController: `Scene Add(SiriusCtl, SymbolController)` +0.1 `Scene SiriusCtl.RefObject="Stars"` `Scene SiriusCtl.Symbol="HIP=32349"`; then a Virtual/Sun/Sphere with `Controller1="SiriusCtl"`, `Control1=Position` (parent "Stars" or "Galactic"). Star look: `Scene Stars.Lum`, `AbsShift`, `HaloScale`, `FadePoint`, `MinPoint`, `MaxPoint`, `MinHalo`, `MaxHalo`, `RedAbsShift`; profiles via the Webinar 3 page → copy into startup. Gaia is a separate StarCatalog asset (1.5+).
- **Planets in the sky:** `Scene Jupiter.Sprite.LumAdj=1.7`, `Scene Mars.Sprite.ColorAdj=#E46C0A`, labels `Label.Brightness`, `Label.MinSize/MaxSize/Size`, `Label.Text`, `Label.HJ/VJ`.
- **Earth:** `Earth.Atmosphere.Visibility`, `Earth.Cloud.Visibility`, `Cloud.Rotate`, `Cloud.Rotate.Rate=1 [3::]`, `Cloud.Cover`, `Cloud.Activity` (need `Cloud.ShowDetail`), `Atmosphere.Sun` (10 default, 20 max — eclipse darkness), `Atmosphere.RSH` (default 0.135), `Atmosphere.OuterPolarRadius=1.104` near the poles (default ~1.02), `Earth.Cardinal.Visibility`, `Earth.Ecliptic.Visibility`. Moon shadow effects: `Scene Moon.EffectSpec="<ContentPath>\Core\Astronomy\SolarSystem\Earth\Moon\MoonEffects.xml"` (blank `" "` disables).
- **Comets/asteroids by code** (from ODC drag): OrbitController (`Unit=au, Epoch, A0, E0, N0, L0, L1, M0, G0`) → Orbit (`Parent=Ecliptic, Controller1=…Ctl, Control1=Transform, Style=Trailing`) → Comet (`Parent=…Orbit, Unit=mm`). Interstellar/unstable orbits: use raw position data (JPL Horizons vector tables) instead.
- **Lines:** VLA files (3D, proper motion) or `.lines` in a Line asset: `Scene myLine.Model=<file>`; no native 3D line command. 2D lines: sidereal slide with a half-line image.
- **Subtitles (1.4+):** `SRT Add(Sub-ORG, SRT)`, `SRT Remove(Sub-ORG)`, `SRT Sub-ORG.SRTFile="…srt"`, `ClockSource=Media`, `MediaClock="MediaAsset"`; an .srt with the same name as the video auto-appears in it.
- **Dataset Explorer:** `DSE AddHeader(Name, Parent, Type, pic)`, `DSE Add(Display, AssetName, Parent, Type{Blank,Visibility,Planets,Planet,Points}, pic)`, `DSE Remove(Display)` (temporary).
- **Kernel:** `Kernel Channels(i).Overlay.FR=On` (fps in viewport; `Channels(1)` renderer 1), `Kernel Channels().Spout.Enabled=On`, `Kernel DomeMask.Enabled=true`, `Kernel DomeMask.WhiteMask=<file>`. `DirectCommand FileSync (<path>)` = sync content to renderers.
- **External:** `Spice Shortcut(15)`, `Spice Show.Open(path)`, `Spice SendCue(...)`; UDP assets + JS handlers (`Remote Name.Cmd(...)`); DM listens for UDP via Tools > UDP Remote Preferences.

## 7. JavaScript engines

```
JS Remove(MyEngine-ORG)
+0.1
JS Add(MyEngine-ORG)
+0.1
;(pad ~10 comment lines here so JS error line numbers = reported line - 10)
JS MyEngine-ORG.Execute(@"
var running = 0;
function dm(s){ DigitalSky.SendScript(s); DigitalSky.LogMessage(s); }
function wait(n){ DigitalSky.LogMessage("+"+n); DigitalSky.Wait(n); }
function Start(rate){ ... }
function Stop(){ running = 0; }
@")
+0.1
JS MyEngine-ORG.FunctionAsync(Start, 2)
```
- `JS Add/Remove(name)` (= older `AddEngine/RemoveEngine`). Everything between `@"` and `@")` is JavaScript. Call functions with `JS Engine.FunctionAsync(Func, args)`, `FunctionSync`, or `JS Engine.Func(args)`; for string args containing commas use `JS Engine.Execute("Func('a, b')")`.
- Old ES5-style engine: use `var` (no `let`), plain functions; template literals appear in newer posts (1.6+). No `import/include` — paste helper functions in. Avoid `)` inside JS comments (it terminated the block in older versions). DM strips blank lines.
- API seen: `DigitalSky.SendScript(str)`, `Wait(sec)`, `LogMessage(str)`, `LogError`, `GetAssetInstance("Camera")`, `.GetPropertyInstance("Altitude").Value`, `CreateAssetInstance("SlideText","Name")`, `obj.SetProperty("Text.String", v, new Transition(a,c,d))`, `AddVariable`, `RemoveVariable`, `AddEventVariable`, `Popup`; 1.7 file I/O: `DirectoryExists`, `CreateDirectory`, `FileExists`, `OpenFile(path,"r"|"w")`, `OpenLocalFile(path,true)` (append), `ReadToEnd/ReadLine/WriteLine/Close/IsOpen`. JS paths need double backslashes.
- Building DM strings in JS: wrap values in quotes: `dm('Scene MyText.Text.String="' + s + '"')`.
- Variables declared outside functions persist across buttons for that engine name until it's removed. Pattern: one "load" button defines functions (or put it in startup/setup); show buttons call them.
- Loops: use a `running` flag + `DigitalSky.Wait(0.1)` inside `while`; always provide a Stop function. JS clock drifts from media clock over minutes.
- JS assets in the Asset Manager have Load Call / Unload Call fields (e.g. `Start` / `Stop`).
- **Rendering caveat:** the Playlist renderer only sees `+X` waits in DM script — waits inside JS count as 0 s. For renderable JS, have JS emit DM commands with explicit waits or log a DM script (`dm()`/`wait()` helpers) and paste it into a button.

## 8. Show building (live, automated, recorded)

- **One button = one thing.** Segment buttons with built-in timing, chapter buttons that call segments, one Setup/Load button, and a master Play button (`Control Seg1.Run()` `+45` `Control Seg2.Run()` `+30` …). Name buttons with durations ("FlyToMars-30"). Keep a hidden/off-screen area for helper buttons and a "testing" area for drafts.
- Setup button (top-left of each show page) rather than editing the workspace startup script: reset, preload heavy media at visibility 0, set star profile, time, location.
- Automated shows (Sky-Skan example): big Load button, chapter restart buttons, language/audio-track buttons, on-page timer/chapter info widgets, load buttons disabled while running, central init button.
- Presenter UX: `Control Text` before every pause, clearly marked beginner path (left column of master buttons), background image with show title on each page, per-show presenter workspaces, VNC tablet or HTML control pages (served at `http://localhost:3736/…`, from `<ContentPath>\Core\HTML`, remote via port 3736) for remote control.
- Schedule tasks / unattended loops: JS scheduler (forum "Scheduling Tasks and countdown timers").
- **Recording a show to video:** Playlist Creator (DM 1.4+) renders any button sequence to PNG/JPG frames at chosen resolution/fps (viewport or a DMGPU window; renderheads without mask for no soft edge). Add buttons individually in order and use the playlist's own "+" delay; nested `Control X.Run()` and JS timing are not respected; particles drop out of PNG renders. Frames have no audio — encode with ffmpeg (e.g. H.264, crf ~21) and slice with SkyVision Renderer 3 for best playback, or play unsliced. For quick previews use OBS/screen capture of a full-screen viewport.
- Video specs: H.264 MP4/MKV safest (H.265 can desync), ≤~25 Mbps, 24/30/48/60 fps (29.97/59.94 OK) — never 25 fps (tearing on 60 Hz multi-channel); constant frame rate; audio WAV/MP3. Edit/trim videos rather than seeking live.

## 9. Gotchas checklist

- File on every PC at identical paths (use Asset Manager assets/DMZ import for auto-distribution, "Sync content" / `DirectCommand FileSync`, or robocopy); check Event Viewer > Renderers. Avoid very long paths, commas and spaces in folder names; the Depot folder is temporary.
- DM keeps files open after loading (older builds) — restart DM to replace a file.
- Copy-pasted buttons share reference names → rename and re-save.
- Assets that are Sky-Skan-locked can't be saved; preload and fade, or make a broken-link copy.
- Remove trailing JS loops and unload engines when done; run Assets Reset after shows.
- Eclipses/shadows need Sun & Moon scale 1 (Moon Visibility 0 still casts shadow — scale it to 0).
- Particles attached to Camera break in stereo; attach to a virtual point.
- `Camera.Zrot` in reset scripts breaks orientation.
- When sharing scripts that rely on Asset Manager assets, also export the asset folder.

## 10. Template: self-contained show segment

```
;=== ORG-MilkyWay-Intro-40 : fade in a labelled image, hold, clean up ===
Control Text="Running..."
Scene Remove(MWLabel-ORG)
Scene Remove(MWSlide-ORG)
+0.1
Scene Add(MWSlide-ORG, Slide, Visibility=0)
Scene Add(MWLabel-ORG, SlideText, Scale=0)
+0.1
Scene MWSlide-ORG.Picture="<ContentPath>\Assets\ORG\milkyway.png"
Scene MWSlide-ORG.Slide.TextLock="Height to Width"
Scene MWSlide-ORG { Azimuth=180 Elevation=35 Width=60 }
Scene MWLabel-ORG.Text.String="Our Galaxy"
Scene MWLabel-ORG { Lens=AllSky Azimuth=180 Elevation=12 }
+1
Scene MWSlide-ORG.Visibility=100 [2]
Scene MWLabel-ORG.Scale=0.3 [1:1:1]
+35
Scene MWSlide-ORG.Visibility=0 [2]
Scene MWLabel-ORG.Scale=0 [1:1:1]
+2.5
Scene Remove(MWLabel-ORG)
Scene Remove(MWSlide-ORG)
Control Text="Milky Way intro (40s)"
```

## 11. Where to look for more

Forum (login needed): Dark Matters Q&A, Shared Content, Tutorials (Slide Asset Tutorial t=483, HTML Control Pages t=491, Camera Animation t=228, Model import t=128, Video On Dome t=278, Exoplanets t=485, JS file I/O t=479, Scheduling t=341, DS2→DM tools t=459), DaMON monthly meeting recordings (t=172; Rendering Mar 2025 t=309, JavaScript Feb 2026 t=432). Sky-Skan cloud content: cloud.skyskan.com shares (password published on the forum). Built-in control pages worth copying from: Tutorial 1/2, Webinar 1–3, Earth Based Astronomy, Solar System – Planets, Constellations, Messier, Spacecraft – Earth/Mars Based, Rosetta – 67P, Climate Science.