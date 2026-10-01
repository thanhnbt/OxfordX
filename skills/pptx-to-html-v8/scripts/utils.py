import os
import re
import urllib.request

def pt_to_px(pt):
    try:
        return round(float(pt) * 1.333333, 1)
    except:
        return 0

def get_vertical_align_css(anchor):
    if anchor == 1: return "flex-start"
    if anchor == 3: return "center"
    if anchor == 4: return "flex-end"
    return "flex-start"

def bgr_to_hex(color_ref):
    try:
        r = color_ref & 0xFF
        g = (color_ref >> 8) & 0xFF
        b = (color_ref >> 16) & 0xFF
        return f"#{r:02X}{g:02X}{b:02X}"
    except:
        return "inherit"

def is_system_font(font_name):
    lower_name = font_name.lower()
    sys_fonts = ['arial', 'calibri', 'times new roman', 'tahoma', 'segoe ui', 'verdana', 'helvetica']
    for sf in sys_fonts:
        if sf in lower_name:
            return True
    return False

# Chars that only a font with a Vietnamese subset can draw (precomposed tone marks
# live in U+1EA0-1EF9, outside Google's latin-ext subset).
VIETNAMESE_CHARS = re.compile(r"[Ạ-ỹĂăĐđƠơƯư]")

# Closest Google family with a Vietnamese subset, for fonts that lack one.
FONT_SUBSTITUTES = {
    # Molengo has no Vietnamese subset; Source Sans 3 covers it with near-identical
    # advance widths (0.97x), so line breaks stay where the deck's author put them.
    "molengo": "Source Sans 3",
    "_default_sans": "Source Sans 3",
    "_default_serif": "Noto Serif",
}

_BROWSER_UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
               "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

_font_map = {}      # original font name -> family actually used in the HTML
_axis_cache = {}    # family -> css2 axis suffix ("", ":wght@400;700", ...)


def has_vietnamese(text):
    return bool(VIETNAMESE_CHARS.search(text or ""))


_network_down = False


def _fetch_google_css(query):
    """Return the css2 body for `query`, or None when Google refuses / we are offline."""
    url = f"https://fonts.googleapis.com/css2?family={query}"
    req = urllib.request.Request(url, headers={"User-Agent": _BROWSER_UA})
    global _network_down
    if _network_down:
        return None
    try:
        with urllib.request.urlopen(req, timeout=8) as resp:
            return resp.read().decode("utf-8", "replace")
    except urllib.error.HTTPError:
        return None  # Google answered - that family or axis just does not exist
    except Exception:
        _network_down = True
        print("Google Fonts unreachable - keeping the deck's original font names")
        return None


def _serves_vietnamese(family):
    css = _fetch_google_css(family.replace(' ', '+'))
    if css is None:
        return None  # unknown (offline) - caller keeps the original font
    return "/* vietnamese */" in css


def _axis_suffix(family):
    """Ask Google for real bold/italic cuts so the browser stops synthesising them."""
    if family in _axis_cache:
        return _axis_cache[family]
    q = family.replace(' ', '+')
    suffix = ""
    for candidate in (":ital,wght@0,400;0,700;1,400;1,700", ":wght@400;700"):
        if _fetch_google_css(q + candidate) is not None:
            suffix = candidate
            break
    _axis_cache[family] = suffix
    return suffix


def build_font_map(fonts_set, needs_vietnamese):
    """Decide which web font each PPTX font becomes. Call once before rendering text."""
    _font_map.clear()
    for f in fonts_set:
        name = (f or "").strip()
        if not name or is_system_font(name):
            continue
        if needs_vietnamese and _serves_vietnamese(name) is False:
            key = name.lower()
            if key in FONT_SUBSTITUTES:
                _font_map[name] = FONT_SUBSTITUTES[key]
            elif "serif" in key and "sans" not in key:
                _font_map[name] = FONT_SUBSTITUTES["_default_serif"]
            else:
                _font_map[name] = FONT_SUBSTITUTES["_default_sans"]
    return dict(_font_map)


def map_font(font_name):
    return _font_map.get((font_name or "").strip(), font_name)


def get_google_font_url(fonts_set):
    families = []
    for f in fonts_set:
        if not is_system_font(f) and f.strip():
            family = map_font(f)
            query = family.replace(' ', '+') + _axis_suffix(family)
            if query not in families:
                families.append(query)
    if not families:
        return ""
    family_query = "&family=".join(families)
    return f"https://fonts.googleapis.com/css2?family={family_query}&display=swap"


def build_merge_map(table):
    """Map every table cell to its (rowspan, colspan), or None when it is swallowed by a merge.

    PowerPoint's COM Cell has no span properties, but every cell of a merged block
    reports the same anchor Shape geometry, so identical Left/Top marks a continuation.
    """
    rows, cols = table.Rows.Count, table.Columns.Count
    origins = {}
    for r in range(1, rows + 1):
        for c in range(1, cols + 1):
            try:
                shape = table.Cell(r, c).Shape
                origins[(r, c)] = (round(float(shape.Left), 1), round(float(shape.Top), 1))
            except Exception:
                origins[(r, c)] = (r, c)  # unknown geometry - treat as its own cell

    spans, seen = {}, set()
    for r in range(1, rows + 1):
        for c in range(1, cols + 1):
            key = origins[(r, c)]
            if key in seen:
                spans[(r, c)] = None
                continue
            seen.add(key)
            colspan = 1
            while c + colspan <= cols and origins[(r, c + colspan)] == key:
                colspan += 1
            rowspan = 1
            while r + rowspan <= rows and origins[(r + rowspan, c)] == key:
                rowspan += 1
            spans[(r, c)] = (rowspan, colspan)
    return spans


def extract_video(pptx_path, slide_idx, output_dir):
    """Extract embedded video from PPTX ZIP for a specific slide. Returns filename or None."""
    import zipfile
    from xml.etree import ElementTree as ET
    import shutil

    rels_path = f"ppt/slides/_rels/slide{slide_idx}.xml.rels"
    try:
        with zipfile.ZipFile(pptx_path, 'r') as z:
            if rels_path not in z.namelist():
                return None
            rels_xml = z.read(rels_path)
            root = ET.fromstring(rels_xml)
            ns = 'http://schemas.openxmlformats.org/package/2006/relationships'
            video_target = None
            for rel in root.findall(f'{{{ns}}}Relationship'):
                rel_type = rel.get('Type', '')
                if 'video' in rel_type.lower() or 'media' in rel_type.lower():
                    video_target = rel.get('Target')
                    break
            if not video_target:
                return None
            import posixpath
            media_path = posixpath.normpath(posixpath.join('ppt/slides', video_target))
            ext = os.path.splitext(media_path)[1] or '.mp4'
            out_name = f"slide_{slide_idx}_video{ext}"
            out_path = os.path.join(output_dir, out_name)
            with z.open(media_path) as src, open(out_path, 'wb') as dst:
                shutil.copyfileobj(src, dst)
            file_size = os.path.getsize(out_path)
            print(f"  [+] Extracted video: {out_name} ({file_size:,} bytes)")
            if file_size > 95 * 1024 * 1024:
                parts = split_video(out_path, slide_idx, output_dir)
                if parts:
                    os.remove(out_path)
                    return parts
            return out_name
    except Exception as e:
        print(f"  [!] Video extraction failed for slide {slide_idx}: {e}")
        return None


def split_video(video_path, slide_idx, output_dir):
    """Split video into 2 parts if > 95MB. Returns list of filenames or None."""
    import subprocess
    import json
    try:
        result = subprocess.run(
            ['ffprobe', '-v', 'quiet', '-print_format', 'json', '-show_format', video_path],
            capture_output=True, text=True
        )
        duration = float(json.loads(result.stdout)['format']['duration'])
        mid = duration / 2
        base = f"slide_{slide_idx}_video"
        p1 = os.path.join(output_dir, f"{base}_part1.mp4")
        p2 = os.path.join(output_dir, f"{base}_part2.mp4")
        subprocess.run(['ffmpeg', '-y', '-i', video_path, '-t', str(mid), '-c', 'copy', p1],
                       capture_output=True)
        subprocess.run(['ffmpeg', '-y', '-i', video_path, '-ss', str(mid), '-c', 'copy', p2],
                       capture_output=True)
        s1 = os.path.getsize(p1)
        s2 = os.path.getsize(p2)
        print(f"  [+] Split video: part1={s1:,} bytes, part2={s2:,} bytes")
        return [f"{base}_part1.mp4", f"{base}_part2.mp4"]
    except Exception as e:
        print(f"  [!] Video split failed: {e}")
        return None
