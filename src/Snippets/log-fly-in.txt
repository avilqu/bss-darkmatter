;=== SNIPPET: logarithmic fly-in using the BSS-Helpers JS engine ===
; Needs BSS-Lib-LoadHelpers run once beforehand (e.g. from the show's Setup button).
; Camera should already be in space with Orient=SouthAndDown, parented to the target.
; LogFly(targetAltitude_m, factorPerStep, stepSeconds): <1 flies in, >1 flies out.
; Not renderable with Playlist Creator (JS waits count as 0 s).
JS BSS-Helpers.Execute("LogFly(1e7, 0.97, 0.1)")
; JS runs async: wait roughly steps x step; stop early with JS BSS-Helpers.Stop()
+20
