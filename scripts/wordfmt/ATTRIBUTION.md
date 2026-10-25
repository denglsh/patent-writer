# wordfmt — 专利版式引擎（vendored）

来源：https://github.com/danxiaozhiren/format-xingwen-word-skill
（skill: format-xingwen-word，原仓库无 LICENSE 文件；此处 vendored 供 patent-writer skill 私有使用，非再分发。）

本目录在原引擎基础上做了以下扩展（patent-writer 项目补丁）：

1. `xingwen_word/presets.py`：新增 `patent` 预设——参数提取自参考专利 2026D0071IN：
   楷体四号（14pt）、正文首行缩进 2 字符、1.5 倍行距、段前 0.2 行、
   A4 上/左/右 2.5cm 下 1.5cm、行网格 lines/312、每 5 行行号。
2. `xingwen_word/roles.py`：`preset == "patent"` 时启用专利角色识别——
   部件标题（摘要/权利要求书/说明书等）→ main_title（居中加粗）；
   说明书小节标题（技术领域/背景技术/发明内容/附图说明/具体实施方式）→ heading_1（左对齐加粗）；
   其余（含 "1." 开头的权利要求段、"S1、" 步骤段）一律 body，避免被编号规则误判为标题。
3. `xingwen_word/formatting.py`：新增四个版式能力——
   `line_multiple`（倍数行距，如 1.5）、`first_indent_chars`（按字符的首行缩进，写入 w:firstLineChars）、
   `space_before_lines`（按行的段前距，写入 w:beforeLines）、`line_number_count_by`（节内行号 w:lnNumType）。
4. `format_document.py`：`--preset` 放行 `patent`。

依赖：`python -m pip install -r requirements.txt`（python-docx>=1.1.2）。
