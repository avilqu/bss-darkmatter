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
| `50-BSS-Lib-SkyDim.txt` | `BSS-Lib-SkyDim` | Sky: dim | 2 s | Theater/Adrien "Sky settings (dim)" |
| `51-BSS-Lib-SkyBright.txt` | `BSS-Lib-SkyBright` | Sky: bright | 5 s | Theater/Adrien "Sky settings (bright)" |
| `55-BSS-Lib-TimeNow.txt` | `BSS-Lib-TimeNow` | Time now | 9 s | Theater/Adrien "Time now" |
| `60-BSS-Lib-LogoIn.txt` | `BSS-Lib-LogoIn` | Logo in | 2.1 s | Operator/CONTROLPANEL "Hermitage logo" (first half) |
| `61-BSS-Lib-LogoOut.txt` | `BSS-Lib-LogoOut` | Logo out | 2 s | Operator/CONTROLPANEL "Hermitage logo" (second half) |
| `70-BSS-Lib-TakeOff.txt` | `BSS-Lib-TakeOff` | Take off | 10 s | Theater/Adrien "Take off" |
| `71-BSS-Lib-Land.txt` | `BSS-Lib-Land` | Land | 10.5 s | Theater/Adrien "Land" |
| `72-BSS-Lib-HomePosition.txt` | `BSS-Lib-HomePosition` | Home position | 9.1 s | Theater/Adrien "Home position" (fixed coordinates instead of Here) |
| `80-BSS-Lib-StarTrailsOn.txt` | `BSS-Lib-StarTrailsOn` | Star trails on | 3.5 s | Theater/Adrien "Star trails" (first half) |
| `81-BSS-Lib-StarTrailsOff.txt` | `BSS-Lib-StarTrailsOff` | Star trails off | 3 s | Theater/Adrien "Star trails" (second half) |
| `82-BSS-Lib-CardinalOn.txt` | `BSS-Lib-CardinalOn` | Cardinal on | 3 s | Theater/Adrien "Cardinal points" (first half) |
| `83-BSS-Lib-CardinalOff.txt` | `BSS-Lib-CardinalOff` | Cardinal off | 3 s | Theater/Adrien "Cardinal points" (second half) |
| `84-BSS-Lib-SCPOn.txt` | `BSS-Lib-SCPOn` | SCP on | 4.2 s | replaces Theater/Adrien "Poles" (self-contained ring) |
| `85-BSS-Lib-SCPOff.txt` | `BSS-Lib-SCPOff` | SCP off | 3 s | idem, removes the ring |
| `86-BSS-Lib-AtmosphereOff.txt` | `BSS-Lib-AtmosphereOff` | Atmosphere off | 3 s | Theater/Adrien "Atmosphere" (second half) |
| `87-BSS-Lib-AtmosphereOn.txt` | `BSS-Lib-AtmosphereOn` | Atmosphere on | 3.1 s | Theater/Adrien "Atmosphere" (first half) |

Live toggles from the dome (with `Control Pause`) are split into On/Off pairs with fixed lengths,
so they work from a master script as well as by hand.

## Requirements

- `BSS-Lib-LogoIn/Out` use the Asset Manager asset **Development > hermitageLogo** (not created
  by script). It must exist for the user whose workspace runs the show.
- `BSS-Lib-SCPOn` uses `Lib-Ring-M.png`: repo `Assets/BSS/Lib/` → `<ContentPath>\Assets\BSS\Lib\`
  on DS-Master and every renderer.
