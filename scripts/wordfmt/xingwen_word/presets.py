"""Fixed 行文检查版式 presets and report scope constants."""

from __future__ import annotations

from typing import Any


PRESETS: dict[str, dict[str, dict[str, Any]]] = {
    "formal": {
        "_page": {
            "width_mm": 210,
            "height_mm": 297,
            "top_mm": 37,
            "bottom_mm": 35,
            "left_mm": 27,
            "right_mm": 27,
            "text_area_width_mm": 156,
            "text_area_height_mm": 225,
            "grid_line_count": 22,
            "grid_char_count": 28,
            "grid_type": "linesAndChars",
            "line_pitch_twips": 600,
            "char_space_twips": 316,
        },
        "main_title": {
            "font": "方正小标宋简体",
            "latin_font": "Times New Roman",
            "size": 22,
            "bold": False,
            "align": "center",
            "first_indent": 0,
            "line": 36,
            "space_after": 30,
            "keep_together": True,
            "keep_with_next": True,
            "widow_control": True,
            "outline_level": "0",
        },
        "subtitle": {"font": "楷体_GB2312", "latin_font": "Times New Roman", "size": 16, "align": "center", "first_indent": 0, "line": 30, "widow_control": True},
        "recipient": {"font": "仿宋_GB2312", "latin_font": "Times New Roman", "size": 16, "align": "left", "first_indent": 0, "line": 30, "keep_with_next": True, "widow_control": True},
        "body": {"font": "仿宋_GB2312", "latin_font": "Times New Roman", "size": 16, "align": "justify", "first_indent": 32, "line": 30, "widow_control": True},
        "heading_1": {"font": "黑体", "latin_font": "Times New Roman", "size": 16, "bold": False, "align": "justify", "first_indent": 32, "line": 30, "keep_together": True, "keep_with_next": True, "widow_control": True, "outline_level": "0"},
        "heading_2": {"font": "楷体_GB2312", "latin_font": "Times New Roman", "size": 16, "bold": True, "align": "justify", "first_indent": 32, "line": 30, "keep_together": True, "keep_with_next": True, "widow_control": True, "outline_level": "1"},
        "heading_3": {"font": "仿宋_GB2312", "latin_font": "Times New Roman", "size": 16, "bold": False, "align": "justify", "first_indent": 32, "line": 30, "keep_together": True, "keep_with_next": True, "widow_control": True, "outline_level": "2"},
        "heading_4": {"font": "仿宋_GB2312", "latin_font": "Times New Roman", "size": 16, "bold": False, "align": "justify", "first_indent": 32, "line": 30, "keep_together": True, "keep_with_next": True, "widow_control": True, "outline_level": "3"},
        "attachment": {"font": "仿宋_GB2312", "latin_font": "Times New Roman", "size": 16, "align": "justify", "first_indent": 32, "line": 30, "widow_control": True},
        "signature": {"font": "仿宋_GB2312", "latin_font": "Times New Roman", "size": 16, "align": "right", "first_indent": 0, "line": 30, "widow_control": True},
        "date": {"font": "仿宋_GB2312", "latin_font": "Times New Roman", "size": 16, "align": "right", "first_indent": 0, "line": 30, "widow_control": True},
        "needs_review": {"font": "仿宋_GB2312", "latin_font": "Times New Roman", "size": 16, "align": "justify", "first_indent": 32, "line": 30, "widow_control": True},
    },
}
PRESETS["checklist"] = PRESETS["formal"]

# 专利预设：参数提取自参考专利 2026D0071IN（楷体四号、首行缩进2字符、1.5倍行距、
# 段前0.2行、A4 上/左/右2.5cm 下1.5cm、行网格 lines/312）。
# 行号默认关闭（2026-10-25 用户要求，见 _page 中 line_number_count_by=None；
# 归一引擎会主动删除文档中已存在的行号设置；如需恢复改为 5）。
# 扩展键：line_multiple（倍数行距）、first_indent_chars（按字符首行缩进）、
# space_before_lines（按行段前）、line_number_count_by（行号间隔）——由 formatting.py 支持。
PRESETS["patent"] = {
    "_page": {
        "width_mm": 210,
        "height_mm": 297,
        "top_mm": 25,
        "bottom_mm": 15,
        "left_mm": 25,
        "right_mm": 25,
        "grid_type": "lines",
        "line_pitch_twips": 312,
        "line_number_count_by": None,  # 用户要求去除行号（2026-10-25）；如需恢复改为 5
    },
    "main_title": {"font": "楷体", "latin_font": "Times New Roman", "size": 14, "bold": True, "align": "center", "line_multiple": 1.5, "widow_control": True},
    "heading_1": {"font": "楷体", "latin_font": "Times New Roman", "size": 14, "bold": True, "align": "left", "first_indent": 0, "line_multiple": 1.5, "widow_control": True},
    "heading_2": {"font": "楷体", "latin_font": "Times New Roman", "size": 14, "bold": True, "align": "left", "first_indent": 0, "line_multiple": 1.5, "widow_control": True},
    "body": {"font": "楷体", "latin_font": "Times New Roman", "size": 14, "align": "justify", "first_indent_chars": 2, "line_multiple": 1.5, "space_before_lines": 0.2, "widow_control": True},
    "note": {"font": "楷体", "latin_font": "Times New Roman", "size": 14, "align": "left", "line_multiple": 1.5, "widow_control": True},
}

COMMON_REPORT_ROLES = [
    "main_title",
    "subtitle",
    "issue_number",
    "metadata",
    "separator",
    "article_title",
    "recipient",
    "body",
    "heading_1",
    "heading_2",
    "heading_3",
    "heading_4",
    "attachment",
    "note",
    "signature",
    "date",
    "cc",
    "printing_area",
]

LIMITED_FORMAT_AREAS = [
    {
        "area": "floating_text_boxes_and_shapes",
        "status": "unsupported",
        "note": "Floating text boxes and shapes are preserved; python-docx does not expose complete safe editing for them.",
    },
    {
        "area": "comments_tracked_changes_and_fields",
        "status": "unsupported",
        "note": "Comments, tracked changes, and field codes are preserved when present but are not fully normalized by this script.",
    },
    {
        "area": "watermarks_footnotes_endnotes_and_bookmarks",
        "status": "unsupported",
        "note": "These structures require deeper OOXML handling and are reported as outside the current automatic formatting scope.",
    },
]
