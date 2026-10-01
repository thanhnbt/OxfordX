from utils import pt_to_px, bgr_to_hex, is_system_font, map_font
from underline_utils import check_word_underline


def escape_text(raw_text):
    return raw_text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('\r', '<br>').replace('\n', '<br>').replace('\x0b', '<br>')


def extract_font_style(font):
    style = ""
    try:
        if font.Name:
            family = map_font(font.Name)
            fallback = "sans-serif"
            if is_system_font(family): fallback = "Arial, sans-serif"
            style += f"font-family: '{family}', {fallback};"
        if font.Size: style += f"font-size: {pt_to_px(font.Size)}px;"
        if font.Bold: style += "font-weight: bold;"
        if font.Italic: style += "font-style: italic;"
        color = bgr_to_hex(font.Color.RGB)
        if color != "transparent": style += f"color: {color};"
    except: pass
    return style


def render_span(text, style, u_class=""):
    span_html = f'<span style="{style}">{text}</span>' if style else text
    if u_class:
        return f'<u class="{u_class}">{span_html}</u>'
    return span_html


def render_words(paragraph, slide_lines, tolerance=(-8, 15)):
    html = ""
    for w_idx in range(1, paragraph.Words().Count + 1):
        word = paragraph.Words(w_idx)
        text = escape_text(word.Text)
        style = extract_font_style(word.Font)
        u_class = check_word_underline(word, slide_lines, pt_to_px, tolerance=tolerance)
        try:
            if not u_class and word.Font.Underline and word.Font.Underline != 0:
                u_class = "step-underline"
        except: pass
        html += render_span(text, style, u_class)
    return html


def render_runs(paragraph):
    html = ""
    for r_idx in range(1, paragraph.Runs().Count + 1):
        run = paragraph.Runs(r_idx)
        text = escape_text(run.Text)
        style = extract_font_style(run.Font)
        u_class = ""
        try:
            if run.Font.Underline and run.Font.Underline != 0:
                u_class = "step-underline"
        except: pass
        html += render_span(text, style, u_class)
    return html


def _space_css(p, space_attr, rule_attr):
    """Paragraph space-before/after as a CSS length. LineRule -1 means the value is in lines."""
    try:
        value = float(getattr(p.ParagraphFormat, space_attr))
        if value <= 0:
            return "0"
        if getattr(p.ParagraphFormat, rule_attr) == -1:
            return f"{value}em"
        return f"{pt_to_px(value)}px"
    except:
        return "0"


def get_paragraph_format(p, tf2, p_idx):
    align = "left"
    try:
        pp_align = p.ParagraphFormat.Alignment
        align_map = {1: "left", 2: "center", 3: "right", 4: "justify"}
        align = align_map.get(pp_align, "left")
    except: pass

    left_indent = 0
    first_line = 0
    if tf2:
        try:
            p2 = tf2.TextRange.Paragraphs.Item(p_idx)
            left_indent = pt_to_px(p2.ParagraphFormat.LeftIndent)
            first_line = pt_to_px(p2.ParagraphFormat.FirstLineIndent)
        except: pass
    else:
        try: left_indent = pt_to_px(p.ParagraphFormat.LeftIndent)
        except: pass

    bullet_char = ""
    try:
        if p.ParagraphFormat.Bullet.Visible:
            bullet_char = "• "
            if p.ParagraphFormat.Bullet.Character:
                bullet_char = escape_text(chr(p.ParagraphFormat.Bullet.Character)) + " "
    except: pass

    line_height = "normal"
    try:
        space_within = p.ParagraphFormat.SpaceWithin
        rule = p.ParagraphFormat.LineRuleWithin
        if rule == -1:
            # PowerPoint's "single" spacing is the font's own line box (~1.2x), not 1.0.
            line_height = str(round(float(space_within) * 1.2, 3))
        elif rule == 0:
            line_height = f"{pt_to_px(space_within)}px"
    except: pass

    # PowerPoint's paragraph spacing (spcBef/spcAft) — without it paragraphs bunch up.
    space_before = _space_css(p, "SpaceBefore", "LineRuleBefore")
    space_after = _space_css(p, "SpaceAfter", "LineRuleAfter")

    return align, left_indent, first_line, bullet_char, line_height, space_before, space_after


def render_paragraph_tag(align, indent, first_line, bullet_char, line_height="normal", step_class="", for_table=False, space_before="0", space_after="0"):
    indent_prop = "margin-left" if for_table else "padding-left"
    style = f"margin: {space_before} 0 {space_after} 0; {indent_prop}: {indent}px; text-indent: {first_line}px; text-align: {align};"
    if not for_table:
        style += f" line-height: {line_height};"
    html = f"<p class='{step_class.strip()}' style='{style}'>" if step_class else f"<p style='{style}'>"
    if bullet_char:
        html += f"<span>{bullet_char}</span>"
    return html
