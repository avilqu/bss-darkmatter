# Dark Matter Script for VS Code

Syntax highlighting for DM button scripts (`src/**/*.txt`, mapped in `.vscode/settings.json`).
`;` comment toggling (Ctrl+/), bracket matching, and `-` kept inside words so double-click selects `Name-BSS-Page`.

Highlights: `;===` headers, comments (with `UNVERIFIED:`/`TODO`/`PLACEHOLDER` flagged), `+N` waits,
routing prefixes (`Scene`, `Control`, `Assets`, `JS`…), `Control Pause`/`Abort`, `[a:c:d]` timings,
methods `.Run()`, properties before `=`, strings, `<ContentPath>`-style aliases, `#RRGGBB` colours, `{f}`.

Install / update after editing:

    cd tools/vscode-darkmatter && npx --yes @vscode/vsce package -o darkmatter-script.vsix && code --install-extension darkmatter-script.vsix --force

Then run "Developer: Reload Window".
