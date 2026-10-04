;=== BSS-SST-PlayAll ===
; Page: BSS-SouthernSkyTour   Button: "Play all"   Length: ~110 s
; Runs the segments in order. Run() doesn't wait, so each call is followed by
; that button's length. Keep these waits in sync with the segment headers.
Control Text="Playing..."
Control BSS-SST-Setup.Run()
+6
Control BSS-SST-MilkyWayIntro-40.Run()
+40
Control BSS-SST-SouthernCross-60.Run()
+60
Control Text="Play all"
