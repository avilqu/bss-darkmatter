"""Shared helpers for build-page.py and pull-page.py.

Dark Matter control page format, as found in <ContentPath>\\Sites\\<Site>\\<User>\\Control Pages:

    <PageName>_<PAGE-GUID>/
        <PAGE-GUID>.xml                      DMButtonPageConfiguration: one <Widget> per button
        WIDGETBUTTONSMALL_<uuid_with_underscores>.txt
                                             UTF-8 BOM + CRLF: <DMScriptHeader> XML, then the script

In the button header, <FriendlyName> is the Reference Name (used by Control Ref.Run())
and <Text> is the caption. DM saves the caption last set by Control Text, so <Text>
is not a reliable label.
"""

import json
import re
import uuid
from datetime import datetime
from pathlib import Path
from xml.sax.saxutils import escape

REPO = Path(__file__).resolve().parent.parent

# Widget kinds the tools manage. Sizes are what DM uses on the dome's existing pages.
KINDS = {
    "small": {"type": "WidgetButtonSmallType", "prefix": "WIDGETBUTTONSMALL", "w": 120, "h": 45},
    "large": {"type": "WidgetButtonType", "prefix": "WIDGETBUTTON", "w": 120, "h": 60},
}
BUTTON_TYPES = {k["type"]: name for name, k in KINDS.items()}

# Default grid for buttons that have no position yet (5 px gap between buttons).
GRID_X0, GRID_Y0, GRID_DX, GRID_DY = 10, 10, 125, 65

BOM = "﻿"


def dm_date(d):
    """DM header date, e.g. 09/24/23 5:57:08 (hour not zero-padded)."""
    return f"{d:%m/%d/%y} {d.hour}:{d:%M:%S}"


def now():
    return datetime.now().replace(microsecond=0)


def new_page_guid():
    return str(uuid.uuid4()).upper()


def new_widget_prefix(kind):
    return f"{KINDS[kind]['prefix']}_{str(uuid.uuid4()).replace('-', '_')}"


def crlf(text):
    return text.replace("\r\n", "\n").replace("\n", "\r\n")


def normalize_script(text):
    """Script text as kept in git: no BOM, LF, no trailing blank lines, one final newline."""
    text = text.lstrip(BOM).replace("\r\n", "\n").replace("\r", "\n")
    return "\n".join(line.rstrip() for line in text.rstrip().split("\n")) + "\n"


# ---------------------------------------------------------------- src side

HEAD_REF = re.compile(r"^;===\s*(\S+)\s*===")
HEAD_LABEL = re.compile(r'Button:\s*"([^"]*)"')


def parse_src_button(path):
    """Return (ref, label) from the ;=== Ref === / Button: "label" header comments."""
    ref = label = None
    for line in path.read_text(encoding="utf-8").splitlines()[:6]:
        if ref is None and (m := HEAD_REF.match(line)):
            ref = m.group(1)
        if label is None and (m := HEAD_LABEL.search(line)):
            label = m.group(1)
    if not ref:
        raise SystemExit(f"{path}: first line must be ';=== <RefName> ===' (the Reference Name)")
    return ref, label or ref


def load_page_json(page_dir):
    p = page_dir / "page.json"
    if not p.exists():
        return p, None
    return p, json.loads(p.read_text(encoding="utf-8"))


def save_page_json(path, data):
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def button_files(page_dir):
    return sorted(p for p in page_dir.glob("*.txt") if re.match(r"\d+-", p.name))


def free_slot(taken, columns):
    """First grid position, row by row, not already used by another button."""
    i = 0
    while True:
        left = GRID_X0 + (i % columns) * GRID_DX
        top = GRID_Y0 + (i // columns) * GRID_DY
        if (left, top) not in taken:
            return left, top
        i += 1


# ---------------------------------------------------------------- DM side

def button_txt(script, ref, label, site, user, created, modified, version=1):
    header = f"""<?xml version="1.0" encoding="utf-8"?>
<DMScriptHeader xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <Text>{escape(label)}</Text>
  <Description />
  <Created>{created}</Created>
  <Modified>{modified}</Modified>
  <Version>{version}</Version>
  <FriendlyName>{escape(ref)}</FriendlyName>
  <Author>{escape(site)}.{escape(user)}</Author>
  <Keywords />
  <Info />
  <MinValue>0</MinValue>
  <MaxValue>100</MaxValue>
  <InitialValue>0</InitialValue>
  <AssetTracking />
  <ImageButtonImagePath />
</DMScriptHeader>
"""
    return (BOM + crlf(header + normalize_script(script))).encode("utf-8")


def page_xml(name, guid, widgets):
    """widgets: list of dicts with prefix, kind, left, top."""
    parts = [f"""<?xml version="1.0" encoding="utf-8"?>
<DMButtonPageConfiguration xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <Name>{escape(name)}</Name>
  <Prefix>{guid}</Prefix>
  <SUGW>0606</SUGW>
  <KeyWords />
  <Group />
  <Type>ControlPage</Type>
  <MatrixTransformX>0</MatrixTransformX>
  <MatrixTransformY>0</MatrixTransformY>
  <Widgets>"""]
    for w in widgets:
        k = KINDS[w["kind"]]
        parts.append(f"""    <Widget>
      <Prefix>{w['prefix']}</Prefix>
      <Type>{k['type']}</Type>
      <OffsetLeft>{w['left']}</OffsetLeft>
      <OffsetRight>{w['left'] + k['w']}</OffsetRight>
      <OffsetTop>{w['top']}</OffsetTop>
      <OffsetBottom>{w['top'] + k['h']}</OffsetBottom>
      <Height>0</Height>
      <Width>0</Width>
      <WidgetStyle />
      <ScriptFilePath>{w['prefix']}.txt</ScriptFilePath>
      <ImageButtonImageFilePath>Button Images\\{w['prefix']}</ImageButtonImageFilePath>
    </Widget>""")
    parts.append("  </Widgets>\n</DMButtonPageConfiguration>")
    return crlf("\n".join(parts)).encode("utf-8")


def dmz_xml(name, guid, install_to, filenames, description):
    files = "".join(f"""
    <DMZFile>
      <Filename>{escape(f)}</Filename>
      <InstallTo>{escape(install_to)}</InstallTo>
    </DMZFile>""" for f in filenames)
    xml = f"""<?xml version="1.0" encoding="utf-8"?>
<DMZPackage xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <Name>{escape(name)}</Name>
  <Category>Control Page</Category>
  <CompletionCode>{guid}</CompletionCode>
  <PackageID>{uuid.uuid4()}</PackageID>
  <Version>0</Version>
  <Description>{escape(description)}</Description>
  <Files>{files}
  </Files>
</DMZPackage>"""
    return crlf(xml).encode("utf-8")


def parse_page_xml(data):
    """Return (name, guid, widgets) from a page .xml (bytes). widgets: dicts with prefix,
    type, left, top, script."""
    text = data.decode("utf-8-sig")
    tag = lambda s, t: (m.group(1) if (m := re.search(rf"<{t}>([^<]*)</{t}>", s)) else None)
    head = text.split("<Widgets>")[0]
    widgets = []
    for w in re.findall(r"<Widget>.*?</Widget>", text, re.S):
        widgets.append({
            "prefix": tag(w, "Prefix"),
            "type": tag(w, "Type"),
            "left": int(tag(w, "OffsetLeft") or 0),
            "top": int(tag(w, "OffsetTop") or 0),
            "script": tag(w, "ScriptFilePath"),
        })
    return tag(head, "Name"), tag(head, "Prefix"), widgets


def split_button_txt(data):
    """Return (header_fields, script) from a DM button .txt (bytes)."""
    text = data.decode("utf-8-sig", errors="replace").replace("\r\n", "\n")
    end = text.find("</DMScriptHeader>")
    if end < 0:
        return {}, text
    header = text[:end]
    script = text[end + len("</DMScriptHeader>"):].lstrip("\n")
    fields = dict(re.findall(r"<(\w+)>([^<]*)</\1>", header))
    for empty in re.findall(r"<(\w+) />", header):
        fields.setdefault(empty, "")
    return fields, script
