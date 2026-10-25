#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""LaTeX → OMML（Word 公式对象）转换器。

用法:
  python latex2omml.py '<latex>'              # 输出 <m:oMath>…</m:oMath>，供插入段落内
  python latex2omml.py '<latex>' --display    # 包裹 <m:oMathPara>（独立成段的展示公式，专利常用）
  python latex2omml.py '<latex>' --with-ns    # 根元素附 xmlns:m 声明（独立校验用）
  echo '<latex>' | python latex2omml.py -     # 从 stdin 读

依赖: pip install latex2mathml mathml2omml
说明: 输出为 OMML XML 片段（不含 w:p 壳）。插入 docx 时放进段落 XML；
     document.xml 根元素已声明 xmlns:m，片段无需自带命名空间。
     公式对象由 Word 以 Cambria Math 渲染，无需另设字体。
"""

from __future__ import annotations

import argparse
import sys

M_NS = "http://schemas.openxmlformats.org/officeDocument/2006/math"


def latex_to_omml(latex: str) -> str:
    import latex2mathml.converter
    import mathml2omml

    latex = latex.strip()
    if latex.startswith("$$") and latex.endswith("$$"):
        latex = latex[2:-2]
    elif latex.startswith("$") and latex.endswith("$"):
        latex = latex[1:-1]
    mathml = latex2mathml.converter.convert(latex.strip())
    omml = mathml2omml.convert(mathml).strip()
    if not omml.startswith("<m:oMath"):
        raise ValueError(f"意外的 OMML 输出: {omml[:80]}")
    return omml


def main() -> int:
    parser = argparse.ArgumentParser(description="LaTeX → OMML (Word 公式对象)")
    parser.add_argument("latex", help="LaTeX 公式；'-' 表示从 stdin 读")
    parser.add_argument("--display", action="store_true", help="包裹 <m:oMathPara>（独立成段的展示公式）")
    parser.add_argument("--with-ns", action="store_true", help="根元素附 xmlns:m 声明（便于独立校验）")
    args = parser.parse_args()

    latex = sys.stdin.read() if args.latex == "-" else args.latex
    try:
        omml = latex_to_omml(latex)
    except Exception as exc:
        print(f"转换失败: {exc}", file=sys.stderr)
        return 1
    if args.display:
        omml = f"<m:oMathPara>{omml}</m:oMathPara>"
    if args.with_ns:
        if omml.startswith("<m:oMathPara>"):
            omml = omml.replace("<m:oMathPara>", f'<m:oMathPara xmlns:m="{M_NS}">', 1)
        else:
            omml = omml.replace("<m:oMath>", f'<m:oMath xmlns:m="{M_NS}">', 1)
    print(omml)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
