;=== BSS-SST-Setup ===
; Page: BSS-SouthernSkyTour   Button: "Setup"   Length: ~6 s
; Ground at Aoraki (via BSS-Lib) + fixed show date/time.
Control Text="Setting up..."
; EDIT SITE.USER to your Site and User names
Control SITE.USER.BSS-Lib.BSS-Lib-SetupGround.Run()
+1.5
; scene is dark at this point -- set time while nobody can see it jump
; 2026-07-15 22:00 NZST = 10:00 UTC. For a live "tonight" show use: Scene DateTime=$Now
Scene DateTime="2026/07/15 10:00:00"
Scene DateTime.Rate=0 [0]
+4.5
Control Text="Setup (done)"
