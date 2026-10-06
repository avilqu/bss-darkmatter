;=== BSS-Lib-ResetSoft ===
; Page: BSS-Lib   Button: "Soft reset"   Length: ~7 s
; Restores global state that shows commonly change, WITHOUT "Assets Reset"
; (which unloads everything and takes ~15 s). Assets added by show segments
; are their own responsibility (they Remove themselves).
Control Text="Resetting..."
Scene Visibility=0 [2]
+2
; stop any running helper loop
JS BSS-Helpers.Stop()
Scene DateTime.Rate=0 [0]
Scene Earth.RotationModel=Diurnal
Scene Earth.AnnualReference="Sun"
Scene Sun { Xscale=2.5 Yscale=2.5 Zscale=2.5 }
Scene Moon { Xscale=2.5 Yscale=2.5 Zscale=2.5 }
+0.1
; back on the ground (button on this page, so the short reference name works)
Control BSS-Lib-SetupGround.Run()
+4.5
Control Text="Soft reset"
