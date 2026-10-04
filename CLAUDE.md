# Dark Matter development — instructions for Claude Code

This repo holds planetarium content for Sky-Skan DigitalSky Dark Matter (DM): button scripts, JavaScript engines, control pages and full dome shows, both live/interactive and automated or recorded. You are my development partner.

## Knowledge sources, in order of priority

1. **Dome profile** (imported below). It describes my system: DM version, computers, paths, asset prefix and naming conventions. Always follow it.
2. **The `darkmatter-scripting` skill** (`.claude/skills/darkmatter-scripting/`). Core DM syntax, commands, assets and gotchas.
3. **`docs/3-dm-forum-research-notes.md`**: raw forum notes for detail and edge cases. Search it (grep) when the skill doesn't cover something. Don't read it in full unless needed.
4. **`docs/4-verified-script-examples.md`**: working scripts from the DSA forum. Use them as patterns.
5. **My own scripts in this repo.** Match their style and naming.

@docs/2-dome-profile.md

## Repo layout

Unless the dome profile or existing files say otherwise:

```
shows/<ShowName>/
    buttons/        one file per button: <NN>-<RefName>.txt (DM script, pasteable into ScriptPad)
    js/             JavaScript engine sources, if kept separately
    media.md        list of media/image files the show needs and where they go on each PC
    README.md       show structure: chapters, segments, durations, master Play order
lib/                reusable buttons and JS helpers (dm / wait / log helpers etc.)
docs/               reference material (see above)
```

## Script rules

- **One file = one button.** The file content must paste straight into a ScriptPad button. Header comments with `;`: button name, reference name, total duration, short purpose.
- **Self-contained.** Create assets with `Scene Add` / `Scene Remove`, named with my asset prefix from the dome profile. Always Remove before Add, wait `+0.1` after Add, then fade in, run, fade out and clean up.
- **Eased timings** that are comfortable on the dome (`[2:2:2]`, `[3:3:8]`, …), not linear jumps.
- Put `Control Text="..."` before every `Control Pause`.
- **Show structure:** short segment buttons with their timing built in, chapter buttons, a Setup button and a master Play button. If a show may be rendered with the Playlist Creator, keep all timing in DM script: no waits inside JavaScript, no nested `Run()`.
- **JavaScript for an older engine:** `var`, plain functions, no `)` inside comments, about 10 padding comment lines before `.Execute(@"` so Event Viewer line numbers map (reported − 10).
- **Files on renderers:** whenever a script uses a media or image file, tell me which files must be copied to every renderer (and DS-Master / sound PC for audio and video), and to which path. Keep `shows/<ShowName>/media.md` up to date.

## Uncertainty and debugging

- If you're not sure of a property name or behaviour (it isn't in the skill or the docs), say so in the reply and mark it in the script with `; UNVERIFIED:`. Tell me how to check it: drag the property from the Asset Manager into the ScriptPad, or look in Event Viewer > Renderers / JavaScript Processor.
- Ask me about my DM version or setup only if the dome profile doesn't answer it.
- When I report a bug, ask for the exact script as it is on the system and any Event Viewer message before guessing.
- You can't run DM here. Check scripts by reading them: balanced `[a:c:d]`, Remove/Add pairs, every Added asset removed at the end, `+` waits that add up to the stated duration.

## Style

Keep explanations short. The script is the main deliverable.
