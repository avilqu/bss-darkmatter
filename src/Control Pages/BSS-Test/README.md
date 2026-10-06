# BSS-Test (TEST)

Throwaway page to check that `tools/build-page.py` output works in Dark Matter.
Delete the page in DM when done. No external files needed.

| File | Reference name | Button label | Length |
|---|---|---|---|
| `10-BSS-TEST-Hello-10.txt` | `BSS-TEST-Hello-10` | Hello (10s) | ~10 s |
| `20-BSS-TEST-CallHello.txt` | `BSS-TEST-CallHello` | Call Hello by ref | ~10.5 s |

## Test checklist (on DS-Master)

Note the answers here; they decide the deploy workflow in the main README.

1. **Import:** File > Import > `BSS-Test.dmz`. Does it import without errors?
2. **Where did it land?** In the Control Page Manager / Explorer: under user `Operator`
   (`E:\DigitalSkyDM\Sites\Mt Cook\Operator\Control Pages\BSS-Test_<GUID>`) or a new user folder?
3. **Layout:** two small buttons side by side, top left, labels "Hello (10s)" / "Call Hello by ref".
4. **Hello:** press it. "Hello from git" grows in the south, holds, shrinks, disappears (~10 s).
5. **Reference name:** press "Call Hello by ref". Does the Hello text appear?
   - If not: open Hello's properties. Is the Reference Name `BSS-TEST-Hello-10`? Save the button, retry.
6. **Re-import:** change a word in `Hello from git`, rebuild, import again.
   Is the page updated in place, or do you get a second page `BSS-Test<timestamp>`?
   (Pages like `Jack20230922034335` on the dome suggest DM makes a renamed copy.)
7. **Pull back:** edit the Hello script in ScriptPad on the dome and save, copy
   `Sites\Mt Cook` (or File > Export the page) to gerty, then run
   `tools/pull-page.py "src/Control Pages/BSS-Test" --from <that folder or .dmz>`.
   The src file should show your edit.
