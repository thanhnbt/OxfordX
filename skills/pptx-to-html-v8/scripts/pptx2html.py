import os
import win32com.client
from pptx import Presentation
from utils import pt_to_px, get_vertical_align_css, bgr_to_hex, is_system_font, get_google_font_url, extract_video, build_font_map, has_vietnamese, build_merge_map
from underline_utils import detect_underline_lines, mark_used_lines
from text_renderer import render_words, render_runs, get_paragraph_format, render_paragraph_tag

def generate_html(pptx_path, output_dir):
    abs_pptx_path = os.path.abspath(pptx_path)
    images_dir = os.path.join(output_dir, "images")
    os.makedirs(images_dir, exist_ok=True)
    
    py_prs = Presentation(abs_pptx_path)
    slide_w_px = int(py_prs.slide_width / 9525)
    slide_h_px = int(py_prs.slide_height / 9525)
    
    powerpoint = win32com.client.Dispatch("PowerPoint.Application")
    com_prs = powerpoint.Presentations.Open(abs_pptx_path, ReadOnly=True, WithWindow=False)

    # Pre-scan for fonts
    used_fonts = set()
    deck_has_vietnamese = False
    for slide_idx in range(1, com_prs.Slides.Count + 1):
        com_slide = com_prs.Slides(slide_idx)
        for i in range(1, com_slide.Shapes.Count + 1):
            com_shape = com_slide.Shapes(i)
            try:
                if com_shape.HasTextFrame and com_shape.TextFrame.HasText:
                    tr = com_shape.TextFrame.TextRange
                    if not deck_has_vietnamese and has_vietnamese(tr.Text):
                        deck_has_vietnamese = True
                    for r_idx in range(1, tr.Runs().Count + 1):
                        font_name = tr.Runs(r_idx).Font.Name
                        if font_name:
                            used_fonts.add(font_name)
            except:
                pass

    substitutions = build_font_map(used_fonts, deck_has_vietnamese)
    for original, replacement in substitutions.items():
        print(f"Font '{original}' has no Vietnamese subset -> using '{replacement}'")
    font_url = get_google_font_url(used_fonts)

    templates_dir = os.path.join(os.path.dirname(__file__), "templates")
    with open(os.path.join(templates_dir, "style.css"), "r", encoding="utf-8") as f:
        css_content = f.read().replace("{{SLIDE_W}}", str(slide_w_px)).replace("{{SLIDE_H}}", str(slide_h_px))

    html_content = [
        "<!DOCTYPE html>",
        "<html>",
        "<head>",
        '    <meta charset="utf-8">',
        f'    <title>{os.path.splitext(os.path.basename(abs_pptx_path))[0]}</title>',
    ]

    if font_url:
        html_content.append(f'    <link href="{font_url}" rel="stylesheet">')

    html_content.extend([
        '    <style>',
        f'        {css_content}',
        '    </style>',
        "</head>",
        "<body>",
        '    <a class="nav-home" href="../../index.html">&#127968; Menu</a>',
        '    <div id="slide-container">'
    ])

    for slide_idx in range(1, com_prs.Slides.Count + 1):
        print(f"Processing Slide {slide_idx}/{com_prs.Slides.Count}...")
        com_slide = com_prs.Slides(slide_idx)
        py_slide = py_prs.slides[slide_idx - 1]
        
        active_class = "active" if slide_idx == 1 else ""
        html_content.append(f'        <div class="slide {active_class}" data-slide="{slide_idx}">')
        
        ocr_applied_for_slide = False

        # Map animations (with paragraph level tracking)
        spid_p_to_step = {}
        anim_step = 1
        sp_tgts = py_slide.element.xpath('.//p:timing//p:spTgt')
        for tgt in sp_tgts:
            spid = tgt.get('spid')
            if not spid: continue
            
            txEl = tgt.xpath('.//p:txEl//p:pRg', namespaces={'p': 'http://schemas.openxmlformats.org/presentationml/2006/main'})
            if txEl:
                st = int(txEl[0].get('st', 0))
                key = f"{spid}_p{st+1}"
            else:
                key = spid
                
            if key not in spid_p_to_step:
                spid_p_to_step[key] = anim_step
                anim_step += 1
                
        spid_to_step = {k: v for k, v in spid_p_to_step.items() if "_" not in k}
                
        max_step = anim_step - 1
        html_content[-1] = html_content[-1].replace(f'data-slide="{slide_idx}"', f'data-slide="{slide_idx}" data-max-step="{max_step}"')

        # Ungroup all grouped shapes (Type 6) to prevent fallback to images
        ungroup_done = False
        while not ungroup_done:
            ungroup_done = True
            for i in range(1, com_slide.Shapes.Count + 1):
                try:
                    if com_slide.Shapes(i).Type == 6:
                        com_slide.Shapes(i).Ungroup()
                        ungroup_done = False
                        break
                except:
                    pass
        
        slide_lines = detect_underline_lines(com_slide, spid_to_step, pt_to_px, slide_idx)
        mark_used_lines(com_slide, slide_lines, pt_to_px)

        shape_elements = []
        
        for i in range(1, com_slide.Shapes.Count + 1):
            com_shape = com_slide.Shapes(i)
            spid = str(com_shape.Id)
            
            try:
                x = pt_to_px(com_shape.Left)
                y = pt_to_px(com_shape.Top)
                w = pt_to_px(com_shape.Width)
                h = pt_to_px(com_shape.Height)
            except Exception as e:
                continue
                
            anim_step = spid_to_step.get(spid, 0)
            step_class = f"step-{anim_step} hidden-step" if anim_step > 0 else ""
            
            has_text = False
            try: has_text = com_shape.HasTextFrame and com_shape.TextFrame.HasText
            except: pass
            
            # Smart Fallback V7 Logic
            is_css_renderable = False
            auto_shape_type = -1
            fill_type = -1
            spid = str(com_shape.Id)
            shape_type = com_shape.Type
            z_index = com_shape.ZOrderPosition
            
            try: auto_shape_type = com_shape.AutoShapeType
            except: pass
            try: 
                if com_shape.Fill.Visible:
                    fill_type = com_shape.Fill.Type
            except: pass
                
            # Types: 1=Rect, 5=Rounded Rect, 9=Oval
            if shape_type == 19 and getattr(com_shape, 'HasTable', False):
                is_css_renderable = True
            elif shape_type in [14, 17]: # Placeholder, TextBox
                is_css_renderable = True
            elif shape_type == 1 and auto_shape_type in [1, 5, 9]: # AutoShape Rect, Rounded Rect, Oval
                is_css_renderable = True
                
            is_video = shape_type == 16  # msoMedia
            if shape_type in [5, 6, 13, 16, 24]: # msoFreeform, msoGroup, msoPicture, msoMedia, msoSmartArt
                is_css_renderable = False
                
            # Force full-screen pictures to act as backgrounds
            if shape_type == 13 and w >= slide_w_px * 0.95 and h >= slide_h_px * 0.95:
                z_index = 0
                
            # Rule 2: Fallback for Gradient/Picture/Texture Fills
            # msoFillSolid = 1, msoFillTextured = 3
            if fill_type != -1 and fill_type != 1:
                if fill_type == 3 and has_text:
                    pass
                else:
                    is_css_renderable = False
                
            # Restore msoLine (Type 9) if it is orthogonal (straight horizontal or vertical)
            if shape_type == 9:
                used = False
                for line in slide_lines:
                    if line['id'] == spid and line['used']:
                        used = True
                        break
                if used:
                    continue
                    
                if w <= 2 or h <= 2:
                    is_css_renderable = True
                else:
                    is_css_renderable = False

            html_code = ""
            if is_css_renderable:
                bg_color = "transparent"
                border_css = "none"
                border_radius = "0"
                
                if auto_shape_type == 5: border_radius = "15px"
                if auto_shape_type == 9: border_radius = "50%"
                
                try:
                    if com_shape.Fill.Visible and fill_type in [1, 3]:
                        bg_color = bgr_to_hex(com_shape.Fill.ForeColor.RGB)
                    if com_shape.Line.Visible:
                        l_color = bgr_to_hex(com_shape.Line.ForeColor.RGB)
                        l_width = max(1, round(com_shape.Line.Weight))
                        if shape_type == 9:
                            if h <= 2: h = max(h, float(l_width))
                            else: w = max(w, float(l_width))
                        else:
                            border_css = f"{l_width}px solid {l_color}"
                except:
                    pass
                
                html_code = f"<div class='autofit-container' style='width: 100%; height: 100%; display: flex; flex-direction: column; "
                if bg_color != "transparent": html_code += f"background-color: {bg_color}; "
                
                if shape_type == 9:
                    try:
                        html_code += f"background-color: {bgr_to_hex(com_shape.Line.ForeColor.RGB)}; "
                    except: pass
                elif border_css != "none":
                    html_code += f"border: {border_css}; "
                if border_radius != "0": html_code += f"border-radius: {border_radius}; "
                
                v_align = "flex-start"
                m_t, m_r, m_b, m_l = 0, 0, 0, 0
                
                if has_text:
                    try:
                        tf = com_shape.TextFrame
                        v_align = get_vertical_align_css(tf.VerticalAnchor)
                        m_l = pt_to_px(tf.MarginLeft)
                        m_t = pt_to_px(tf.MarginTop)
                        m_r = pt_to_px(tf.MarginRight)
                        m_b = pt_to_px(tf.MarginBottom)
                    except:
                        pass
                        
                html_code += f"justify-content: {v_align}; padding: {m_t}px {m_r}px {m_b}px {m_l}px; box-sizing: border-box;'>"
                
                if shape_type == 19:
                    html_code = html_code.replace(f"padding: {m_t}px {m_r}px {m_b}px {m_l}px;", "padding: 0px 0px 0px 0px;")
                    
                if shape_type == 19 and getattr(com_shape, 'HasTable', False):
                    table = com_shape.Table
                    html_code += f'<table style="border-collapse: collapse; width: 100%; height: 100%; table-layout: fixed;">'
                    merge_map = build_merge_map(table)
                    for r in range(1, table.Rows.Count + 1):
                        row = table.Rows(r)
                        html_code += f'<tr style="height: {pt_to_px(row.Height)}px;">'
                        for c in range(1, table.Columns.Count + 1):
                            span = merge_map.get((r, c), (1, 1))
                            if span is None:
                                continue  # covered by a merged cell that started earlier
                            rowspan, colspan = span
                            span_attr = ""
                            if rowspan > 1: span_attr += f' rowspan="{rowspan}"'
                            if colspan > 1: span_attr += f' colspan="{colspan}"'
                            cell = table.Cell(r, c)
                            col = table.Columns(c)
                            cell_width = pt_to_px(col.Width)
                            if colspan > 1:
                                cell_width = sum(pt_to_px(table.Columns(cc).Width)
                                                 for cc in range(c, min(c + colspan, table.Columns.Count + 1)))
                            
                            cell_bg = "transparent"
                            try:
                                if cell.Shape.Fill.Visible: cell_bg = bgr_to_hex(cell.Shape.Fill.ForeColor.RGB)
                            except: pass
                            
                            cell_border = ""
                            border_map = {1: 'top', 2: 'bottom', 3: 'left', 4: 'right'}
                            for b_idx, b_name in border_map.items():
                                try:
                                    border = cell.Borders(b_idx)
                                    if border.Visible:
                                        weight = pt_to_px(border.Weight)
                                        color = bgr_to_hex(border.ForeColor.RGB)
                                        cell_border += f"border-{b_name}: {weight}px solid {color}; "
                                except: pass
                                
                            cell_valign = "middle"
                            try:
                                c_margin_top = pt_to_px(cell.Shape.TextFrame.MarginTop)
                                c_margin_bottom = pt_to_px(cell.Shape.TextFrame.MarginBottom)
                                c_margin_left = pt_to_px(cell.Shape.TextFrame.MarginLeft)
                                c_margin_right = pt_to_px(cell.Shape.TextFrame.MarginRight)
                            except:
                                c_margin_top = 4; c_margin_bottom = 4; c_margin_left = 9.6; c_margin_right = 9.6
                                
                            html_code += f'<td{span_attr} style="width: {cell_width}px; background-color: {cell_bg}; {cell_border} padding: {c_margin_top}px {c_margin_right}px {c_margin_bottom}px {c_margin_left}px; box-sizing: border-box; vertical-align: {cell_valign}; word-break: break-word; overflow-wrap: anywhere;">'
                            
                            if cell.Shape.HasTextFrame and cell.Shape.TextFrame.HasText:
                                tf2 = None
                                try:
                                    if getattr(cell.Shape, 'HasTextFrame2', False) or cell.Shape.TextFrame2:
                                        tf2 = cell.Shape.TextFrame2
                                except: pass
                                
                                for p_idx in range(1, cell.Shape.TextFrame.TextRange.Paragraphs().Count + 1):
                                    p = cell.Shape.TextFrame.TextRange.Paragraphs(p_idx)
                                    align, p_indent, p_first_line, bullet_char, _, p_sp_bef, p_sp_aft = get_paragraph_format(p, tf2, p_idx)
                                    html_code += render_paragraph_tag(align, p_indent, p_first_line, bullet_char, for_table=True, space_before=p_sp_bef, space_after=p_sp_aft)
                                    html_code += render_words(p, slide_lines, tolerance=(-8, 45))
                                    html_code += "</p>"
                            html_code += '</td>'
                        html_code += '</tr>'
                    html_code += '</table>'
                elif has_text:
                    tf2 = None
                    try:
                        if getattr(com_shape, 'HasTextFrame2', False) or com_shape.TextFrame2:
                            tf2 = com_shape.TextFrame2
                    except: pass
                    
                    try:
                        tr = com_shape.TextFrame.TextRange
                        for p_idx in range(1, tr.Paragraphs().Count + 1):
                            p = tr.Paragraphs(p_idx)
                            align, left_indent, first_line, bullet_char, line_height, sp_before, sp_after = get_paragraph_format(p, tf2, p_idx)

                            p_anim_step = spid_p_to_step.get(f"{spid}_p{p_idx}", 0)
                            p_step_class = f" step-{p_anim_step} hidden-step" if p_anim_step > 0 else ""

                            html_code += render_paragraph_tag(align, left_indent, first_line, bullet_char, line_height, p_step_class, space_before=sp_before, space_after=sp_after)

                            if len(slide_lines) > 0:
                                html_code += render_words(p, slide_lines)
                            else:
                                html_code += render_runs(p)
                            html_code += "</p>"
                    except: pass
                html_code += "</div>"

            shape_str = ""
            if is_css_renderable:
                shape_str = f'            <!-- CSS Render {spid} -->\n            <div class="shape {step_class}" data-spid="{spid}" style="left: {x}px; top: {y}px; width: {w}px; height: {h}px; z-index: {z_index};">\n                {html_code}\n            </div>'
            else:
                if is_video:
                    poster_name = f"slide_{slide_idx}_shape_{spid}.png"
                    poster_path = os.path.join(images_dir, poster_name)
                    try:
                        com_shape.Export(os.path.abspath(poster_path), 2)
                    except: pass
                    video_result = extract_video(abs_pptx_path, slide_idx, images_dir)
                    if video_result:
                        shape_str = f'            <!-- Video {spid} -->\n'
                        shape_str += f'            <div class="shape {step_class}" data-spid="{spid}" style="left: {x}px; top: {y}px; width: {w}px; height: {h}px; z-index: {z_index};">\n'
                        vid_id = f"vid_{slide_idx}_{spid}"
                        if isinstance(video_result, list):
                            sources_json = ','.join(f'"images/{p}"' for p in video_result)
                            shape_str += f'                <video id="{vid_id}" controls poster="images/{poster_name}" style="width: 100%; height: 100%; object-fit: contain;">\n'
                            shape_str += f'                    <source src="images/{video_result[0]}" type="video/mp4">\n'
                            shape_str += f'                </video>\n'
                            shape_str += f'                <script>(function(){{var v=document.getElementById("{vid_id}"),parts=[{sources_json}],i=0;v.addEventListener("ended",function(){{if(i<parts.length-1){{i++;v.src=parts[i];v.play();}}}});}})();</script>\n'
                        else:
                            shape_str += f'                <video controls poster="images/{poster_name}" style="width: 100%; height: 100%; object-fit: contain;">\n'
                            shape_str += f'                    <source src="images/{video_result}" type="video/mp4">\n'
                            shape_str += f'                </video>\n'
                        shape_str += f'            </div>'
                    else:
                        render_h = max(2, h)
                        render_w = max(2, w)
                        shape_str = f'            <!-- Native PNG for {spid} (video fallback) -->\n'
                        shape_str += f'            <img class="shape {step_class}" data-spid="{spid}" src="images/{poster_name}" style="left: {x}px; top: {y}px; width: {render_w}px; height: {render_h}px; z-index: {z_index};">'
                else:
                    img_name = f"slide_{slide_idx}_shape_{spid}.png"
                    img_path = os.path.join(images_dir, img_name)

                    # Check for OCR override (ONLY APPLY ONCE PER SLIDE)
                    override_path = os.path.join(os.path.dirname(pptx_path), "ocr_overrides", f"slide_{slide_idx}.html")
                    if os.path.exists(override_path):
                        if not ocr_applied_for_slide:
                            with open(override_path, "r", encoding="utf-8") as f:
                                shape_str = f"<!-- OCR Override for Slide {slide_idx} -->\n" + f.read() + "\n"
                                print(f"  [+] Applied OCR override for Slide {slide_idx}")
                            ocr_applied_for_slide = True
                        else:
                            shape_str = "" # Already applied, skip this shape
                    else:
                        try:
                            com_shape.Export(os.path.abspath(img_path), 2)
                            render_h = max(2, h)
                            render_w = max(2, w)
                            shape_str = f'            <!-- Native PNG for {spid} -->\n'
                            shape_str += f'            <img class="shape {step_class}" data-spid="{spid}" src="images/{img_name}" style="left: {x}px; top: {y}px; width: {render_w}px; height: {render_h}px; z-index: {z_index};">'
                        except: pass
                    
            if shape_str:
                shape_elements.append(shape_str)

        try:
            while com_slide.Shapes.Count > 0:
                com_slide.Shapes(1).Delete()
        except: pass
            
        bg_name = f"slide_{slide_idx}_pure_bg.png"
        bg_path = os.path.join(images_dir, bg_name)
        com_slide.Export(os.path.abspath(bg_path), "PNG")
        
        html_content.append(f'            <!-- Pure Slide Background -->')
        html_content.append(f'            <img class="shape" style="left: 0; top: 0; width: {slide_w_px}px; height: {slide_h_px}px; z-index: 0;" src="images/{bg_name}">')

        for el in shape_elements:
            html_content.append(el)

        html_content.append('        </div>')
        
    try:
        com_prs.Close()
        powerpoint.Quit()
    except: pass

    html_content.append('    </div>')
    
    with open(os.path.join(templates_dir, "presentation.js"), "r", encoding="utf-8") as f:
        js_content = f.read().replace("{{SLIDE_W}}", str(slide_w_px)).replace("{{SLIDE_H}}", str(slide_h_px))

    html_content.append(f"""
    <script>
        {js_content}
    </script>
</body>
</html>
    """)

    output_html = os.path.join(output_dir, "presentation.html")
    with open(output_html, "w", encoding="utf-8") as f:
        f.write("\n".join(html_content))
        
    print(f"Successfully generated V8 Table Engine presentation: {output_html}")

if __name__ == '__main__':
    import argparse
    import os
    import sys
    
    parser = argparse.ArgumentParser(description='Convert PPTX to HTML (Native V8 Engine)')
    parser.add_argument('-i', '--input', required=True, help='Path to input PPTX file')
    parser.add_argument('-o', '--output', default='hybrid_export', help='Output directory (default: hybrid_export)')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.input):
        print(f'Error: File not found -> {args.input}')
        sys.exit(1)
        
    generate_html(args.input, args.output)
