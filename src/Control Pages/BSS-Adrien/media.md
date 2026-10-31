# BSS-Adrien — media

The buttons are unchanged copies, so they depend on the same files and Asset Manager folders as
`Theater/Adrien`. Nothing new has to be copied: all of this is already on the dome if the original
page works there. Nothing here is packed into `Assets/BSS/` yet (TODO, with the rest of the asset
packing).

## Files

Each must be at the same path on **DS-Master and every renderer**. All are used by
`010-BSS-Adrien-LoadAssets`.

| File | Path on every PC | Status |
|---|---|---|
| `Jupiter_14K.dds` | `<ContentPath>\Assets\Jack\` | another user's folder, not in the repo |
| `MWPAN2_4KX2K.JPG` | `<ContentPath>\Core\Astronomy\AllSky\` | DM core content |
| `Mars_16K.dds` | `<ContentPath>\Core\Astronomy\SolarSystem\Mars\` | DM core content |
| `Earth_16K-Clouds.dds`, `Earth_16K-Surface.dds`, `Earth_16K-CityLights.dds` | `<ContentPath>\Core\Astronomy\SolarSystem\Earth\` | DM core content |

## Asset Manager folders

| Folder | Assets | Used by |
|---|---|---|
| `Constellations` | `<Name> Art`, `<Name> Stick`, `<Name> IAU` for the constellations, plus `Proxima Cen`, `Proxima Circle`, `hadar Cen`, `hadar Circle`, `Achernar Eri`, `Achernar Circle` | Load assets, All boundaries / sticks / art, Zodiac art, Orion, Scorpius, star buttons |
| `DeepSkyPhoto` | `<object>`, `<object>_circle`, `<object>_label` for m42, m104, ngc104, ngc253, ngc2070, ngc3372, ngc3532, ngc4755, ngc5128, ngc7293; `sc`, `smc` | Purple panel |
| `Line and circle` | Circumpolar Region, Stick diamond Crux, Stick diamond Crux1, Stick False Crux, Stick False Crux1 | Circumpolar Region, Wrong crosses stick |
| `MaoriConstellations` | Mahutonga, MauisFishHook, TeWakaORangi, TeWakaoTamarereti | Yellow panel |
| `Aoraki` | southernLights1-2, northernLights1-2, stellarWindPart, sunSpawn, magFieldCentreA-C, magFieldRingA1-C2 | Aurora, Stellar wind, Magnetic field |
| `Basics` | PoleCircles | Poles |
| `Taichi` | FulldomeAurora | Fulldome aurora |
| `Jack` | GreatEmu | Galactic Emu |
| `Asteroids` | Main Belt Asteroids | Main asteroid belt |
| `Extragalactic` | LEDA200Mpc, LocalGroup | Load assets (needed by the Local Group and LEDA sliders) |
| `Milky Way` | Vol Milky Way | Load assets |
