;=== SNIPPET: show an image on the dome, hold, clean up ===
; Copy into a show button. Replace NAME, PAGE, the image path, position and hold time.
; The image must exist at the same path on every renderer (check Event Viewer > Renderers).
Scene Remove(NAME-BSS-PAGE)
+0.1
Scene Add(NAME-BSS-PAGE, Slide, Visibility=0)
+0.1
Scene NAME-BSS-PAGE.Picture="<ContentPath>\Assets\BSS\image.png"
Scene NAME-BSS-PAGE.Slide.TextLock="Height to Width"
Scene NAME-BSS-PAGE { Azimuth=180 Elevation=35 Width=60 }
; large images may need +1..+3 here before fading in
+1
Scene NAME-BSS-PAGE.Visibility=100 [2]
+20
Scene NAME-BSS-PAGE.Visibility=0 [2]
+2.5
Scene Remove(NAME-BSS-PAGE)
