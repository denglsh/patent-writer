# 参考专利 Word 版式规格（preset: patent）

排版基准 = 自带参考专利 2026D0071IN 六稿实测值（从其 OOXML 提取）。
引擎位置：`<skill>/scripts/wordfmt/`（见该目录 ATTRIBUTION.md）。

## 版式规格

| 项目 | 值 |
|---|---|
| 纸张 | A4（210×297mm） |
| 页边距 | 上 2.5cm、左 2.5cm、右 2.5cm、下 1.5cm（页眉 1.5cm、页脚 1.75cm） |
| 行网格 | lines 型，linePitch 312 |
| 行号 | **关闭**（2026-10-25 用户要求；参考原件含每5行行号但不沿用。归一时会主动删除文档中已有行号。如需恢复：`presets.py` 中 `_page` 的 `line_number_count_by` 改为 5） |
| 正文字体 | 楷体（中文）/ Times New Roman（西文），四号 = 14pt |
| 正文对齐 | 两端对齐 |
| 首行缩进 | 2 字符（w:firstLineChars="200"） |
| 行距 | 1.5 倍（w:line="360" lineRule="auto"） |
| 段前距 | 0.2 行（w:beforeLines="20"） |
| 部件标题（摘要/权利要求书/说明书/说明书附图/附图清单） | 楷体四号加粗，居中，不缩进 |
| 说明书小节标题（技术领域/背景技术/发明内容/附图说明/具体实施方式） | 楷体四号加粗，左对齐，不缩进 |
| 公式 | **独立成段、居中**，Word 公式对象（m:oMathPara，LaTeX 经 `scripts/wordfmt/latex2omml.py` 转换，Cambria Math 渲染）；变量定义文字化句紧随其后 |

注：页边距按 mm 写入时与参考件存在 1 twip（0.0018mm）舍入差，可忽略。

## 角色识别（--preset patent 时）

- **文档第一段视为发明名称标题行** → main_title（居中加粗）；若第一段本身是部件标题或附图注记则按其自身角色。
- 命中部件标题词表（整段仅含"摘要""权利要求书"等）→ main_title（居中加粗）。
- 命中说明书小节词表（技术领域等）→ heading_1（左对齐加粗）。
- "（指定图1为摘要附图）" → note。
- 其余一律 body——包括 "1." 开头的权利要求段和 "S1、" 步骤段，**不会**被编号规则误判为标题。

## 使用流程

### 每章写入后的版式归一（阶段 B，每章一次）

```bash
cd <skill>/scripts/wordfmt
python format_document.py <工作目录>/<发明名称>.docx \
  --preset patent --output <临时文件>.docx --report <临时>.json
```

- 检查报告：`summary.status == "ok"` 且 `summary.output_withheld == false` 才用临时文件**替换**原 docx；否则保留原文件、先排查报告里的 warnings。
- 归一是幂等的：对已归一文件重复运行结果不变。

### 阶段 C 交付前校验

```bash
python format_document.py <发明名称>.docx --preset patent --diagnose-only --report final_check.json
```

确认 status=ok、role_counts 合理（heading_1 = 5 个说明书小节 + 各部件标题计入 main_title）、无 warnings 后交付。

## 调参

版式参数全部集中在 `scripts/wordfmt/xingwen_word/presets.py` 的 `PRESETS["patent"]`。
要改字体/字号/缩进/行距/页边距/行号间隔，直接改该字典即可，无需动引擎代码。

## 已知边界（继承自原引擎）

- 浮动文本框/形状、批注/修订/域代码、水印/脚注/书签：保留但不归一。
- 附图（图片对象）原样保留。
- 严格的逐页视觉核对（行×字网格）仍需在 Word/WPS 里打开确认。
