;=== SNIPPET: lift off from the ground, fly to a planet, come home ===
; Total ~60 s. Stop time first; don't touch the viewport navigator during this.
Scene DateTime.Rate=0 [2::]
+2
; lift off
Scene Camera { Altitude=1e7 } [4:3:8]
+1
Scene Camera.Orient=SouthAndDown [3:3:8]
Scene Camera.SS.Elevation=45 [3:3:8]
+14
; fly to the planet (wait the full a+c+d)
Scene Camera.FlyTo(Mars, Altitude=1e7, Orient=SouthAndDown) [8:6:8]
+22
; ... talk ...
+5
; home
Scene Camera.FlyTo(Here, Orient=SouthAndUp) [8:6:8]
+22
