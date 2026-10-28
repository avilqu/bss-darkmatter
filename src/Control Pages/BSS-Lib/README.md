# BSS-Lib

Shared buttons, used by every show page. Must be loaded in any workspace that calls them.
Call them from another page with the full path, then wait the button's length (`Run()` doesn't wait):

```
Control Mt Cook.Theater.BSS-Lib.BSS-Lib-SkyBright.Run()
+5
```

| File | Reference name | Button label | Length | Source |
|---|---|---|---|---|
| `20-BSS-Lib-ResetSoft.txt` | `BSS-Lib-ResetSoft` | Soft reset | 11.2 s | new |
| `30-BSS-Lib-FadeOut.txt` | `BSS-Lib-FadeOut` | Fade out | 3 s | new |
| `40-BSS-Lib-LoadHelpers.txt` | `BSS-Lib-LoadHelpers` | Load BSS-Helpers | ~0.5 s | generated from `src/JavaScript/BSS-Helpers.js` |
| `41-BSS-Lib-LoadAssets.txt` | `BSS-Lib-LoadAssets` | Load assets | 5 s | Theater/Adrien "Load assets" (textures + extragalactic; no constellations, Mars/Jupiter maps) |
| `50-BSS-Lib-SkyDim.txt` | `BSS-Lib-SkyDim` | Sky: dim | 2 s | Theater/Adrien "Sky settings (dim)" |
| `51-BSS-Lib-SkyBright.txt` | `BSS-Lib-SkyBright` | Sky: bright | 5 s | Theater/Adrien "Sky settings (bright)" |
| `55-BSS-Lib-TimeNow.txt` | `BSS-Lib-TimeNow` | Time now | 9 s | Theater/Adrien "Time now" |
| `56-BSS-Lib-EquatorOn.txt` | `BSS-Lib-EquatorOn` | Equator on | 3 s | Theater/Jack "Equatorial ON" |
| `57-BSS-Lib-EquatorOff.txt` | `BSS-Lib-EquatorOff` | Equator off | 3 s | idem |
| `58-BSS-Lib-EclipticOn.txt` | `BSS-Lib-EclipticOn` | Ecliptic on | 3 s | Theater/Adrien "Ecliptic" (first half) |
| `59-BSS-Lib-EclipticOff.txt` | `BSS-Lib-EclipticOff` | Ecliptic off | 3 s | Theater/Adrien "Ecliptic" (second half) |
| `60-BSS-Lib-LogoIn.txt` | `BSS-Lib-LogoIn` | Logo in | 2.1 s | Operator/CONTROLPANEL "Hermitage logo" (first half) |
| `61-BSS-Lib-LogoOut.txt` | `BSS-Lib-LogoOut` | Logo out | 2 s | Operator/CONTROLPANEL "Hermitage logo" (second half) |
| `70-BSS-Lib-TakeOff.txt` | `BSS-Lib-TakeOff` | Take off | 10 s | Theater/Adrien "Take off" |
| `71-BSS-Lib-Land.txt` | `BSS-Lib-Land` | Land | 10.5 s | Theater/Adrien "Land" |
| `72-BSS-Lib-HomePosition.txt` | `BSS-Lib-HomePosition` | Home position | 9.1 s | Theater/Adrien "Home position" (fixed coordinates instead of Here) |
| `73-BSS-Lib-FaceNorth.txt` | `BSS-Lib-FaceNorth` | Face north | 11 s | Theater/Adrien "Spin dome" (first half) |
| `74-BSS-Lib-FaceSouth.txt` | `BSS-Lib-FaceSouth` | Face south | 11 s | Theater/Adrien "Spin dome" (second half) |
| `75-BSS-Lib-GoToMoon.txt` | `BSS-Lib-GoToMoon` | Go to Moon | 31 s | Theater/Adrien "Go to Moon" (wait fixed to the full flight) |
| `80-BSS-Lib-StarTrailsOn.txt` | `BSS-Lib-StarTrailsOn` | Star trails on | 3.5 s | Theater/Adrien "Star trails" (first half) |
| `81-BSS-Lib-StarTrailsOff.txt` | `BSS-Lib-StarTrailsOff` | Star trails off | 3 s | Theater/Adrien "Star trails" (second half) |
| `82-BSS-Lib-CardinalOn.txt` | `BSS-Lib-CardinalOn` | Cardinal on | 3 s | Theater/Adrien "Cardinal points" (first half) |
| `83-BSS-Lib-CardinalOff.txt` | `BSS-Lib-CardinalOff` | Cardinal off | 3 s | Theater/Adrien "Cardinal points" (second half) |
| `84-BSS-Lib-SCPOn.txt` | `BSS-Lib-SCPOn` | SCP on | 4.2 s | replaces Theater/Adrien "Poles" (self-contained ring) |
| `85-BSS-Lib-SCPOff.txt` | `BSS-Lib-SCPOff` | SCP off | 3 s | idem, removes the ring |
| `86-BSS-Lib-AtmosphereOff.txt` | `BSS-Lib-AtmosphereOff` | Atmosphere off | 3 s | Theater/Adrien "Atmosphere" (second half) |
| `87-BSS-Lib-AtmosphereOn.txt` | `BSS-Lib-AtmosphereOn` | Atmosphere on | 3.1 s | Theater/Adrien "Atmosphere" (first half) |
| `88-BSS-Lib-CloudsOn.txt` | `BSS-Lib-CloudsOn` | Clouds on | 3 s | Theater/Adrien "Clouds" (first half) |
| `89-BSS-Lib-CloudsOff.txt` | `BSS-Lib-CloudsOff` | Clouds off | 3 s | Theater/Adrien "Clouds" (second half) |
| `90-BSS-Lib-ConstLoad.txt` | `BSS-Lib-ConstLoad` | Const: load | 1.5 s | Theater/Adrien "Load assets" + sticks |
| `91-BSS-Lib-ConstUnload.txt` | `BSS-Lib-ConstUnload` | Const: unload | 0.5 s | new |
| `92-BSS-Lib-SticksOn.txt` | `BSS-Lib-SticksOn` | Sticks on | 3 s | Theater/Adrien "All sticks" (first half) |
| `93-BSS-Lib-SticksOff.txt` | `BSS-Lib-SticksOff` | Sticks off | 3 s | Theater/Adrien "All sticks" (second half) |
| `94-BSS-Lib-ArtNorthOn.txt` | `BSS-Lib-ArtNorthOn` | Art north on | 3 s | Theater/Adrien "All art", northern group |
| `95-BSS-Lib-ArtNorthOff.txt` | `BSS-Lib-ArtNorthOff` | Art north off | 3 s | idem |
| `96-BSS-Lib-ArtZodiacOn.txt` | `BSS-Lib-ArtZodiacOn` | Art zodiac on | 3 s | Theater/Adrien "Zodiac art" |
| `97-BSS-Lib-ArtZodiacOff.txt` | `BSS-Lib-ArtZodiacOff` | Art zodiac off | 3 s | idem |
| `98-BSS-Lib-ArtSouthOn.txt` | `BSS-Lib-ArtSouthOn` | Art south on | 3 s | Theater/Adrien "All art", southern group |
| `99-BSS-Lib-ArtSouthOff.txt` | `BSS-Lib-ArtSouthOff` | Art south off | 3 s | idem |
| `100-BSS-Lib-CarinaOn.txt` | `BSS-Lib-CarinaOn` | Carina on | 7 s | Theater/Adrien "NGC3372" (first half) |
| `101-BSS-Lib-CarinaOff.txt` | `BSS-Lib-CarinaOff` | Carina off | 3 s | idem (second half) |
| `102-BSS-Lib-CarinaRingOn.txt` | `BSS-Lib-CarinaRingOn` | Carina ring on | 4.2 s | replaces Theater/Adrien "NGC3372 label" (self-contained ring) |
| `103-BSS-Lib-CarinaRingOff.txt` | `BSS-Lib-CarinaRingOff` | Carina ring off | 3 s | idem, removes the ring |
| `104-BSS-Lib-JewelBoxOn.txt` | `BSS-Lib-JewelBoxOn` | Jewel Box on | 7 s | Theater/Adrien "NGC4755" (first half) |
| `105-BSS-Lib-JewelBoxOff.txt` | `BSS-Lib-JewelBoxOff` | Jewel Box off | 3 s | idem (second half) |
| `106-BSS-Lib-JewelBoxRingOn.txt` | `BSS-Lib-JewelBoxRingOn` | Jewel Box ring on | 4.2 s | replaces Theater/Adrien "NGC4755 label" (self-contained ring) |
| `107-BSS-Lib-JewelBoxRingOff.txt` | `BSS-Lib-JewelBoxRingOff` | Jewel Box ring off | 3 s | idem, removes the ring |
| `108-BSS-Lib-WishingWellOn.txt` | `BSS-Lib-WishingWellOn` | Wishing Well on | 7 s | Theater/Adrien "NGC3532" (first half) |
| `109-BSS-Lib-WishingWellOff.txt` | `BSS-Lib-WishingWellOff` | Wishing Well off | 3 s | idem (second half) |
| `110-BSS-Lib-47TucOn.txt` | `BSS-Lib-47TucOn` | 47 Tuc on | 7 s | Theater/Adrien "NGC104" (first half) |
| `111-BSS-Lib-47TucOff.txt` | `BSS-Lib-47TucOff` | 47 Tuc off | 3 s | idem (second half) |
| `112-BSS-Lib-47TucRingOn.txt` | `BSS-Lib-47TucRingOn` | 47 Tuc ring on | 4.2 s | replaces Theater/Adrien "NGC104 label" (self-contained ring) |
| `113-BSS-Lib-47TucRingOff.txt` | `BSS-Lib-47TucRingOff` | 47 Tuc ring off | 3 s | idem, removes the ring |
| `114-BSS-Lib-AuroraOn.txt` | `BSS-Lib-AuroraOn` | Aurora on | 7.5 s (animates 60 s more) | Theater/Adrien "Aurora" (first half) |
| `115-BSS-Lib-AuroraOff.txt` | `BSS-Lib-AuroraOff` | Aurora off | 3 s | idem (second half), aborts AuroraOn |
| `116-BSS-Lib-SolarWindOn.txt` | `BSS-Lib-SolarWindOn` | Solar wind on | 4 s | Theater/Adrien "Stellar wind" (first half) |
| `117-BSS-Lib-SolarWindOff.txt` | `BSS-Lib-SolarWindOff` | Solar wind off | 3 s | idem (second half) |
| `118-BSS-Lib-MagFieldOn.txt` | `BSS-Lib-MagFieldOn` | Mag field on | 4.5 s | Theater/Adrien "Magnetic field" (first half) |
| `119-BSS-Lib-MagFieldOff.txt` | `BSS-Lib-MagFieldOff` | Mag field off | 3 s | idem (second half) |
| `120-BSS-Lib-OrbitsOn.txt` | `BSS-Lib-OrbitsOn` | Orbits on | 3 s | Theater/Adrien "Planets orbits" (first half) |
| `121-BSS-Lib-OrbitsOff.txt` | `BSS-Lib-OrbitsOff` | Orbits off | 3 s | idem (second half) |
| `122-BSS-Lib-AsteroidsOn.txt` | `BSS-Lib-AsteroidsOn` | Asteroids on | 4 s | Theater/Adrien "Main asteroid belt" (first half) |
| `123-BSS-Lib-AsteroidsOff.txt` | `BSS-Lib-AsteroidsOff` | Asteroids off | 3.5 s | idem (second half), unloads it |

Live toggles from the dome (with `Control Pause`) are split into On/Off pairs with fixed lengths,
so they work from a master script as well as by hand.

## Requirements

- The constellation buttons (92–99) need `BSS-Lib-ConstLoad` first and `BSS-Lib-ConstUnload` after.
  They use the Sky-Skan **Constellations** folder (`<Name> Stick`, `<Name> Art`). Groups follow Adrien's
  "All art" order: north 31 (incl. Orion, Monoceros, Ophiuchus), zodiac 12, south 45 (incl. Cetus).

- `BSS-Lib-LogoIn/Out` use the Asset Manager asset **Development > hermitageLogo** (not created
  by script). It must exist for the user whose workspace runs the show.
- `BSS-Lib-SCPOn` and the deep-sky rings (102–113) use `Lib-Ring-M.png` (SCP, Carina) and `Lib-Ring-S.png`
  (Jewel Box, 47 Tuc): repo `Assets/BSS/Lib/` → `<ContentPath>\Assets\BSS\Lib\` on DS-Master and every renderer.
- The deep-sky photos (100–111) use the Asset Manager assets **DeepSkyPhoto > ngc3372, ngc4755, ngc3532,
  ngc104** (as Adrien's NGC buttons). TODO: export the folder (DMZ) and convert to Scene Add + files.
  The "On" button loads the photo, the "Off" button unloads it: anything a show changes on the photo
  (e.g. a zoom with Scale) must be undone before calling "Off".
- The aurora, solar wind and magnetic field buttons (114–119) use the Asset Manager folder **Aoraki**
  (`southernLights1/2`, `northernLights1/2`, `sunSpawn`, `stellarWindPart`, `magFieldCentreA/B/C`,
  `magFieldRingA1…C2`), as Adrien's buttons. TODO: export the folder (DMZ) and convert to Scene Add + files.
  `BSS-Lib-AuroraOn` keeps running 60 s after its fade-in (slow Activity/ColorShift changes);
  `BSS-Lib-AuroraOff` aborts it first.
- `BSS-Lib-AsteroidsOn/Off` (122–123) load/unload the Asset Manager asset **Asteroids > Main Belt Asteroids**,
  as Adrien's button. TODO: check whether it is Sky-Skan core content; if not, export it (DMZ) and convert.
