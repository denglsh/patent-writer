# patent-writer

辅助撰写中国发明专利（CNIPA）申请文件的 Agent Skill——采用开放的 **Agent Skills 格式**（SKILL.md + references/ + scripts/ + assets/），不绑定特定 Agent 工具。

## 用途

从**技术框架/交底书 + 参考专利**两项必要材料出发，先确定格式模板（内置 playbook，或由 skill 自动从参考专利提取），再逐章生成权利要求书、说明书、摘要等完整申请文件（约 12000~15000 字），全文终检后交付统一排版的 .docx。

## 跨 Agent 安装

| 环境 | 安装位置 | 说明 |
|---|---|---|
| ZCode | `~/.agents/skills/patent-writer/`（全局）或项目 `.agents/skills/` | 原生支持，自动触发 |
| Claude Code / Claude.ai | `~/.claude/skills/patent-writer/` 或项目 `.claude/skills/` | 同为 Agent Skills 格式 |
| 其他遵循 Agent Skills 规范的工具 | 按各工具文档指定的 skills 目录放置 | 格式通用 |
| 不支持该格式的 Agent | 将 SKILL.md 与 references/ 作为提示词/上下文手动提供 | 撰写流程与规则照常生效；scripts 可在命令行独立调用 |

对运行环境的唯一要求是具备 **.docx 创建与 OOXML 编辑能力**：SKILL.md 已写成工具无关的表述——有 docx 类技能的环境直接调用；没有的环境用 python-docx 或直接编辑 OOXML，脚本链路完全一致。

## 依赖

- Python 3.10+
- `pip install -r scripts/wordfmt/requirements.txt`
  （python-docx ≥1.1.2；latex2mathml + mathml2omml 用于把 LaTeX 公式转为 Word 公式对象）

## 结构

```
patent-writer/
├── SKILL.md                        ← 流程编排与交互规则（工具无关）
├── references/
│   ├── writing-playbook-cn.md      ← 内置分章节撰写提示词（基于 2026D0071IN 参考格式预提取）
│   ├── format-extraction.md        ← 参考专利格式提取提示词（自动生成专属 playbook）
│   ├── quality-constraints.md      ← 专利实体质量约束（保护范围/从权梯队/清楚性红线）
│   └── word-format-spec.md         ← 参考专利 Word 版式规格与排版流程
├── scripts/
│   └── wordfmt/                    ← 版式引擎（--preset patent 归一）+ latex2omml.py（LaTeX→公式对象）
└── assets/
    └── 2026D0071IN-…-六稿.docx     ← 自带参考专利原件（风电叶片应变传感器布局方法及系统）
```

## 流程

1. **阶段 A**：依次收集两项必要材料（① 技术框架/交底书；② 参考专利，无自带备选），确定格式模板
2. **阶段 B**：按 playbook 第0步~第8步逐步撰写（方案拆解 → 权利要求书 → 摘要 → 技术领域 → 背景技术 → 发明内容 → 附图说明 → 具体实施方式 → 终检），每步附自检清单，用户只回答编号选项
3. **阶段 C**：全文终检 → 交付统一 Word 文档（各章实时写入同一 docx，始终按文档顺序成稿）

## 特性

- 固定流水线，全程用户只需回答编号选项（1/2/3）
- 每章写完即写入同一个 .docx（建骨架留占位 + 逐章替换），下一章接着上一章的 Word 写，会话中不贴全文
- 排版自动对齐参考专利（楷体四号、首行缩进2字符、1.5倍行距、不带行号），每章写入后零内容改动归一
- 四处逐字镜像复用纪律（权利要求 ↔ 发明内容 ↔ 实施例 ↔ 系统模块）
- 内置 CNIPA 硬性要求自检（"所述"链条、摘要 ≤300 字、编号格式等）
- 具体实例数值【待填】确认机制，避免 AI 编造数据
- 公式强制以 Word 公式对象呈现（LaTeX → OMML），独立成段居中，禁止文字化省略
