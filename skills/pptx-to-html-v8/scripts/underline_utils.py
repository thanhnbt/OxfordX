def detect_underline_lines(com_slide, spid_to_step, pt_to_px, slide_idx=None):
    slide_lines = []
    for i in range(1, com_slide.Shapes.Count + 1):
        try:
            sh = com_slide.Shapes(i)
            if sh.Type == 9:
                h = pt_to_px(sh.Height)
                w = pt_to_px(sh.Width)
                if h <= 2 and w <= 250:
                    spid = str(sh.Id)
                    slide_lines.append({
                        'id': spid,
                        'left': pt_to_px(sh.Left),
                        'top': pt_to_px(sh.Top),
                        'right': pt_to_px(sh.Left) + w,
                        'step': spid_to_step.get(spid, 0),
                        'used': False
                    })
        except Exception as e:
            print(f"Error checking line shape {i}: {e}")
    if len(slide_lines) > 0 and slide_idx is not None:
        print(f"Found {len(slide_lines)} lines on slide {slide_idx}")
    return slide_lines


def mark_used_lines(com_slide, slide_lines, pt_to_px):
    if not slide_lines:
        return
    for i in range(1, com_slide.Shapes.Count + 1):
        sh = com_slide.Shapes(i)
        has_text = False
        try: has_text = sh.HasTextFrame and sh.TextFrame.HasText
        except: pass
        if has_text:
            try:
                for p_idx in range(1, sh.TextFrame.TextRange.Paragraphs().Count + 1):
                    p = sh.TextFrame.TextRange.Paragraphs(p_idx)
                    for w_idx in range(1, p.Words().Count + 1):
                        word = p.Words(w_idx)
                        _check_collision(word, slide_lines, pt_to_px, (-15, 15), mark_only=True)
            except: pass
        if sh.Type == 19 and getattr(sh, 'HasTable', False):
            try:
                for r in range(1, sh.Table.Rows.Count + 1):
                    for c in range(1, sh.Table.Columns.Count + 1):
                        cell = sh.Table.Cell(r, c)
                        if cell.Shape.HasTextFrame and cell.Shape.TextFrame.HasText:
                            for p_idx in range(1, cell.Shape.TextFrame.TextRange.Paragraphs().Count + 1):
                                p = cell.Shape.TextFrame.TextRange.Paragraphs(p_idx)
                                for w_idx in range(1, p.Words().Count + 1):
                                    word = p.Words(w_idx)
                                    _check_collision(word, slide_lines, pt_to_px, (-15, 15), mark_only=True)
            except: pass


def check_word_underline(word, slide_lines, pt_to_px, tolerance=(-15, 15)):
    return _check_collision(word, slide_lines, pt_to_px, tolerance, mark_only=False)


def _check_collision(word, slide_lines, pt_to_px, tolerance, mark_only):
    try:
        bl = pt_to_px(word.BoundLeft)
        br = bl + pt_to_px(word.BoundWidth)
        bb = pt_to_px(word.BoundTop) + pt_to_px(word.BoundHeight)
        for line in slide_lines:
            diff = line['top'] - bb
            if tolerance[0] <= diff <= tolerance[1]:
                overlap_left = max(bl, line['left'])
                overlap_right = min(br, line['right'])
                if overlap_right - overlap_left > 5:
                    line['used'] = True
                    if not mark_only:
                        step_cls = f" step-{line['step']} hidden-step" if line['step'] > 0 else ""
                        return f"step-underline{step_cls}"
                    return ""
    except: pass
    return ""
