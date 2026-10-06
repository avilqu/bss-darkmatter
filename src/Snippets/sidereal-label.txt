;=== SNIPPET: text label fixed to the stars ===
; Azimuth = RA in hours x 15, Elevation = Dec. Avoid exactly +/-90.
; UNVERIFIED: Frame=Sidereal on SlideText -- confirm by dragging the property from the Asset Manager.
Scene Remove(NAME-BSS-PAGE)
+0.1
Scene Add(NAME-BSS-PAGE, SlideText, Scale=0)
+0.1
Scene NAME-BSS-PAGE.Text.String="Label text"
Scene NAME-BSS-PAGE { Frame=Sidereal Azimuth=RA_DEG Elevation=DEC_DEG }
+0.8
Scene NAME-BSS-PAGE.Scale=0.3 [1:1:1]
+15
Scene NAME-BSS-PAGE.Scale=0 [1:1:1]
+3
Scene Remove(NAME-BSS-PAGE)
