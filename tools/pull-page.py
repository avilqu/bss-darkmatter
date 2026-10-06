#!/usr/bin/env python3
"""Copy button scripts edited on the dome back into src/Control Pages/<Page>/.

    tools/pull-page.py "src/Control Pages/BSS-Test"                       # from Sites/ in this repo
    tools/pull-page.py "src/Control Pages/BSS-Test" --from "E:/backup/Sites/Mt Cook"
    tools/pull-page.py "src/Control Pages/BSS-Test" --from "BSS-Test (Exported Control Page).dmz"
    tools/pull-page.py ... --dry-run                                      # report only

The page is found by the pageGuid in page.json, under any user of the site. --from takes a
site folder (<ContentPath>\\Sites\\<Site>) or a .dmz exported from DM (File > Export).

What it does:
  - button script changed on the dome  -> rewrites the src .txt (whole script, header comments included)
  - button moved on the dome           -> updates left/top in page.json
  - button added on the dome           -> new NN-<RefName>.txt + page.json entry
  - button deleted on the dome         -> warning only; delete the src file yourself
  - sliders, labels, images...         -> warning only; build-page.py does not create them
Button captions (<Text>) are not pulled: DM saves whatever Control Text last displayed.
"""

import argparse
import re
import sys
import zipfile
from pathlib import Path

import dmpage as dm


class Source:
    """Read files of one DM page from a site folder or a .dmz."""

    def __init__(self, src, guid):
        self.zip = None
        if src.suffix.lower() == ".dmz":
            self.zip = zipfile.ZipFile(src)
            names = {n.lower(): n for n in self.zip.namelist()}
            self.names = names
            if f"{guid}.xml".lower() not in names:
                sys.exit(f"{src}: this .dmz is not page {guid}. If DM imported a renamed copy, "
                         "it got a new GUID; see README.md")
            self.where = str(src)
        else:
            hits = sorted(src.glob(f"*/Control Pages/*_{guid}"))
            if not hits:
                sys.exit(f"page {guid} not found under {src}/*/Control Pages/")
            if len(hits) > 1:
                print(f"WARNING: page found in several places, using the first: {[str(h) for h in hits]}")
            self.dir = hits[0]
            self.where = str(self.dir)

    def read(self, name):
        if self.zip:
            key = self.names.get(name.lower())
            return self.zip.read(key) if key else None
        p = self.dir / name
        return p.read_bytes() if p.exists() else None


def keep_local_header(local, dome):
    """For a button made on the dome, the src file has a ;=== header the dome copy lacks.
    Return the dome script with that header on top (unchanged local if only the header differs)."""
    lines = local.split("\n")
    for n in range(1, len(lines)):
        if not lines[n - 1].startswith(";"):
            break
        if "\n".join(lines[n:]) == dome:
            return local
    return "\n".join(lines[:2]) + "\n" + dome


def safe_name(s):
    return re.sub(r"[^A-Za-z0-9._-]+", "-", s).strip("-") or "Button"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("page_dir", type=Path)
    ap.add_argument("--from", dest="src", type=Path, help="site folder or .dmz (default: Sites/<site> in this repo)")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    page_dir = args.page_dir.resolve()
    pj_path, pj = dm.load_page_json(page_dir)
    if pj is None:
        sys.exit(f"{page_dir}: no page.json; build and import the page first")
    guid = pj["pageGuid"]
    src = Source(args.src or dm.REPO / "Sites" / pj["site"], guid)
    print(f"pulling from {src.where}")

    _, _, widgets = dm.parse_page_xml(src.read(f"{guid}.xml"))
    by_prefix = {b["prefix"].lower(): n for n, b in pj["buttons"].items()}
    seen, changed = set(), 0
    other = {}

    for w in widgets:
        kind = dm.BUTTON_TYPES.get(w["type"])
        if not kind:
            other[w["type"]] = other.get(w["type"], 0) + 1
            continue
        data = src.read(w["script"] or w["prefix"] + ".txt")
        if data is None:
            print(f"  WARNING: {w['prefix']}: script file missing on the dome, skipped")
            continue
        fields, script = dm.split_button_txt(data)
        dome = dm.normalize_script(script)
        fname = by_prefix.get(w["prefix"].lower())

        if fname is None:
            # button created on the dome
            ref = fields.get("FriendlyName") or safe_name(fields.get("Text", ""))
            nums = [int(n.split("-")[0]) for n in pj["buttons"]] or [0]
            fname = f"{(max(nums) // 10 + 1) * 10:02d}-{safe_name(ref)}.txt"
            if not dm.HEAD_REF.match(dome):
                label = fields.get("Text", "").strip() or ref
                dome = f';=== {ref} ===\n; Page: {pj["pageName"]}   Button: "{label}"   (added on the dome)\n' + dome
            print(f"  NEW   {fname}  (added on the dome, ref {ref})"
                  + ("" if fields.get("FriendlyName") else "  -- no Reference Name set in DM, check it"))
            pj["buttons"][fname] = {"prefix": w["prefix"], "kind": kind, "left": w["left"], "top": w["top"]}
            if not args.dry_run:
                (page_dir / fname).write_text(dome, encoding="utf-8")
            changed += 1
            seen.add(fname)
            continue

        seen.add(fname)
        b = pj["buttons"][fname]
        path = page_dir / fname
        local = dm.normalize_script(path.read_text(encoding="utf-8")) if path.exists() else None
        if local and dm.HEAD_REF.match(local) and not dm.HEAD_REF.match(dome):
            # dome copy has no header (button made on the dome): keep ours on top
            dome = keep_local_header(local, dome)
        if local != dome:
            print(f"  EDIT  {fname}  (script changed on the dome)")
            if not args.dry_run:
                path.write_text(dome, encoding="utf-8")
            changed += 1
        m = dm.HEAD_REF.match(dome)
        ref = m.group(1) if m else None
        if not ref:
            print(f"  WARNING: {fname}: the ;=== <RefName> === first line is gone; build-page.py needs it")
        elif fields.get("FriendlyName") and fields["FriendlyName"] != ref:
            print(f"  WARNING: {fname}: Reference Name on the dome is {fields['FriendlyName']}, "
                  f"src header says {ref}; fix the ;=== line")
        if (b["left"], b["top"]) != (w["left"], w["top"]) or b.get("kind") != kind:
            print(f"  MOVE  {fname}  {b['left']},{b['top']} -> {w['left']},{w['top']}")
            b.update(left=w["left"], top=w["top"], kind=kind)
            changed += 1

    for n in pj["buttons"]:
        if n not in seen:
            print(f"  WARNING: {n}: not on the dome page (deleted there?). Delete the src file and "
                  f"its page.json entry if that was intended.")
    for t, c in other.items():
        print(f"  WARNING: {c} x {t} on the dome page; not managed, a rebuild will not include it")

    if args.dry_run:
        print(f"dry run: {changed} change(s) not written")
    else:
        dm.save_page_json(pj_path, pj)
        print(f"{changed} change(s)" if changed else "up to date")


if __name__ == "__main__":
    main()
