;=== BSS-Lib-SetupGround ===
; Page: BSS-Lib   Button: "Ground: Aoraki"   Length: ~4 s
; Puts the observer on the ground at Aoraki/Mount Cook Village, looking south,
; with normal diurnal Earth rotation. Does NOT set date/time: shows do that.
; Coordinates: Mount Cook Village approx. -- check against your site's Location asset.
Control Text="Setting up..."
Scene Visibility=0 [1]
+1
Scene Earth.RotationModel=Diurnal
Scene Earth.AnnualReference="Sun"
Scene Camera { Parent=Earth Orient=SouthAndUp SS.Elevation=90 Latitude=-43.7357 Longitude=170.0962 Altitude=760 }
; SS.Elevation=90 suits a concentric dome; lower it (e.g. 30) for a tilted/unidirectional dome.
;
; --- BSS star profile: paste Stars.* values here (e.g. copied from the Webinar 3 page) ---
; Scene Stars { Lum=... AbsShift=... HaloScale=... }
;
+0.5
Scene Visibility=100 [2]
+2.5
Control Text="Ground: Aoraki"
