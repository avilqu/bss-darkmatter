#!/usr/bin/env python3
"""Build a Dark Matter control page from a src/Control Pages/<Page>/ folder.

    tools/build-page.py "src/Control Pages/BSS-Test"            -> build/BSS-Test.dmz
    tools/build-page.py "src/Control Pages/BSS-Test" --folder   -> also build/Sites/... folder

Every NN-<anything>.txt in the folder becomes one button, in filename order. Each file
must start with the usual header:

    ;=== BSS-TEST-Hello-10 ===                        <- Reference Name (FriendlyName)
    ; Page: BSS-Test   Button: "Hello (10s)"  ...     <- button caption

page.json in the folder holds the site/user, the page GUID and each button's widget ID
and position. It is created on the first build and must be committed: DM and workspaces
identify the page and buttons by these IDs, so they must never change.
Edit "left"/"top" (pixels) or "kind" ("small" 120x45 / "large" 120x60) by hand if you like;
pull-page.py also copies positions back from the dome.

Install the .dmz on DS-Master with File > Import, or copy the --folder output into
<ContentPath>\\Sites (with DM closed). See README.md "Deploying a page".
"""

import argparse
import sys
import zipfile
from pathlib import Path

import dmpage as dm


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("page_dir", type=Path)
    ap.add_argument("--site", help="DM site for a new page.json (default: Mt Cook)")
    ap.add_argument("--user", help="DM user for a new page.json (default: Operator)")
    ap.add_argument("--columns", type=int, default=6, help="grid width for new buttons (default 6)")
    ap.add_argument("--out", type=Path, default=dm.REPO / "build", help="output folder (default build/)")
    ap.add_argument("--folder", action="store_true", help="also write the native page folder under <out>/Sites/")
    args = ap.parse_args()

    page_dir = args.page_dir.resolve()
    files = dm.button_files(page_dir)
    if not files:
        sys.exit(f"{page_dir}: no NN-*.txt button files")

    pj_path, pj = dm.load_page_json(page_dir)
    if pj is None:
        pj = {
            "site": args.site or "Mt Cook",
            "user": args.user or "Operator",
            "pageName": page_dir.name,
            "pageGuid": dm.new_page_guid(),
            "created": dm.dm_date(dm.now()),
            "buttons": {},
        }
        print(f"new page.json: site={pj['site']} user={pj['user']} guid={pj['pageGuid']}")
    elif args.site or args.user:
        sys.exit("site/user are already set in page.json; edit it by hand if you really mean to move the page")

    site, user, name, guid = pj["site"], pj["user"], pj["pageName"], pj["pageGuid"]
    buttons = pj["buttons"]

    # assign IDs and positions to new buttons
    taken = {(b["left"], b["top"]) for b in buttons.values()}
    for f in files:
        if f.name not in buttons:
            left, top = dm.free_slot(taken, args.columns)
            taken.add((left, top))
            buttons[f.name] = {"prefix": dm.new_widget_prefix("small"), "kind": "small", "left": left, "top": top}
            print(f"  new button {f.name} at {left},{top}")
    gone = [n for n in buttons if not (page_dir / n).exists()]
    for n in gone:
        print(f"  WARNING: {n} is in page.json but the file is gone; dropping it from the page")
        del buttons[n]

    # duplicate reference names break Control Ref.Run()
    refs = {}
    widgets, out_files = [], {}
    stamp = dm.dm_date(dm.now())
    for f in files:
        ref, label = dm.parse_src_button(f)
        if ref in refs:
            sys.exit(f"duplicate Reference Name {ref} in {refs[ref]} and {f.name}")
        refs[ref] = f.name
        b = buttons[f.name]
        widgets.append({**b})
        out_files[b["prefix"] + ".txt"] = dm.button_txt(
            f.read_text(encoding="utf-8"), ref, label, site, user,
            created=pj.get("created", stamp), modified=stamp)

    page_file = f"{guid}.xml"
    out_files = {page_file: dm.page_xml(name, guid, widgets), **out_files}
    folder = f"{name}_{guid}"
    install_to = f"<ContentPath>\\SITES\\{site}\\{user}\\Control Pages\\{folder}"
    manifest = dm.dmz_xml(name, guid, install_to, list(out_files),
                          f"{name} Control Page built from git by tools/build-page.py")

    args.out.mkdir(parents=True, exist_ok=True)
    dmz = args.out / f"{name}.dmz"
    with zipfile.ZipFile(dmz, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr(page_file, out_files[page_file])
        z.writestr("DMZ.XML", manifest)
        for fn, data in out_files.items():
            if fn != page_file:
                z.writestr(fn, data)
    print(f"wrote {dmz.relative_to(dm.REPO) if dmz.is_relative_to(dm.REPO) else dmz}  ({len(files)} buttons)")
    print(f"  installs to {install_to}")

    if args.folder:
        d = args.out / "Sites" / site / user / "Control Pages" / folder
        d.mkdir(parents=True, exist_ok=True)
        for fn, data in out_files.items():
            (d / fn).write_bytes(data)
        print(f"wrote folder {d}")

    dm.save_page_json(pj_path, pj)


if __name__ == "__main__":
    main()
