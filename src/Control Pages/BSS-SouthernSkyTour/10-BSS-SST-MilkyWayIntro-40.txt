;=== BSS-SST-MilkyWayIntro-40 ===
; Page: BSS-SouthernSkyTour   Button: "Milky Way (40s)"   Length: 40 s
; Labels the galactic centre (Sagittarius) and slowly turns the sky.
; Needs: BSS-SST-Setup run first.
; Sidereal slides: Azimuth = RA x 15, Elevation = Dec.
; UNVERIFIED: Frame=Sidereal on SlideText (seen on Slide) -- if the label sticks
; to the dome instead of the stars, use a Slide with a text image instead.
Control Text="Milky Way - running"
Scene Remove(GCLabel-BSS-SST)
+0.1
Scene Add(GCLabel-BSS-SST, SlideText, Scale=0)
+0.1
Scene GCLabel-BSS-SST.Text.String="Centre of our Galaxy"
; Sgr A*: RA 17h45.7m = 266.4 deg, Dec -29.0
Scene GCLabel-BSS-SST { Frame=Sidereal Azimuth=266.4 Elevation=-29.0 }
+0.8
Scene GCLabel-BSS-SST.Scale=0.3 [1:1:1]
+3
; let the sky turn: 1 hour of sky per 10 s
Scene DateTime.Rate=360 [3::]
+30
Scene DateTime.Rate=0 [2::]
Scene GCLabel-BSS-SST.Scale=0 [1:1:1]
+3
Scene Remove(GCLabel-BSS-SST)
; 0.1+0.1+0.8+3+30+3 = 37 s, + ~3 s buffer
+3
Control Text="Milky Way (40s)"
