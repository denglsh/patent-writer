# 附图自动生成协议

触发：阶段 B 第6步《附图说明与绘图需求清单》经用户确认后执行；阶段 C 复核。
目标：把绘图需求清单变成黑白线图 PNG 并插入交付 docx，消灭"附图需另行绘制"的人工缺口。

## 一、工具选择（探测顺序）

1. **draw.io 桌面版 CLI**（`draw.io` 或 `drawio` 在 PATH）：优先使用——流程图/框图更精致且可编辑（生成 .drawio XML 后经 CLI 导出 PNG；修复 PNG 用 drawio-skill 的 repair_png.py）。
2. **matplotlib（默认，零安装）**：探测不到 draw.io CLI 时使用，纯 Python，本协议附模板。**不要求用户安装任何软件。**
3. 都不可用时：输出每幅图的绘图需求清单交用户手绘（退化模式）。

## 二、CNIPA 附图硬性要求

- **黑白线条图**：禁止彩色、禁止灰度填充（必要的阴影线/剖面线除外）。
- 图内中文标注用宋体，标记与正文术语**逐字一致**（同一部件图与文同名）。
- 图号（图1、图2…）与"附图说明"章节**逐字一致**；图号置于图**下方居中**。
- 图中避免大段文字，流程框内每行不超过约 12 字。
- 摘要附图（图1）另需在正文中已写"（指定图1为摘要附图）"——playbook 第2步已保证。

## 三、matplotlib 模板（黑白线图）

公共样式：

```python
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
plt.rcParams["font.family"] = ["SimSun"]      # 宋体；黑体标注可用 "SimHei"
plt.rcParams["axes.unicode_minus"] = False
BLACK = "#000000"
```

流程图（图1：方法 S1~S5(+S6)）——竖排圆角框 + 箭头：

```python
fig, ax = plt.subplots(figsize=(4, 7)); ax.axis("off")
steps = ["S1：构建出厂有限元数字孪生模型", "S2：加载工况获取全场数据", "S3：生成候选布置点集合",
         "S4：构建传感器布局优化模型", "S5：迭代求解得到布置方案"]
n = len(steps); h, gap = 0.12, 0.06
for i, s in enumerate(steps):
    y = 1 - (i + 1) * (h + gap)
    ax.add_patch(FancyBboxPatch((0.2, y), 0.6, h, boxstyle="round,pad=0.015",
                 fc="white", ec=BLACK, lw=1.2))
    ax.text(0.5, y + h / 2, s, ha="center", va="center", fontsize=10)
    if i:  # 与上一框连箭头
        ax.add_patch(FancyArrowPatch((0.5, y + h + gap), (0.5, y + h + 0.005),
                     arrowstyle="-|>", mutation_scale=14, color=BLACK, lw=1.2))
ax.set_xlim(0, 1); ax.set_ylim(0, 1)
fig.savefig("图1.png", dpi=300, bbox_inches="tight", facecolor="white")
```

框图（图2 系统模块、图5 电子设备硬件）：同上思路，用 `FancyBboxPatch` 排布模块矩形、`FancyArrowPatch` 连线；图5 按 playbook 固定元素画处理器510/存储器520/输入输出接口530/通信接口540/总线550。

示意图（图3 候选点分布、图4 最终布置结果）：`ax.scatter(..., s=18, c="black", marker="o")`，功能区边界用黑色实线圈画；**不用颜色区分**，用形状（o/s/^）+ 图例（黑色边框、白底）区分类别。

## 四、流程

1. 逐图生成：按第6步绘图需求清单，每图输出 PNG（300dpi、白底）到工作目录 `附图/` 子文件夹。
2. 插入 docx：替换"附图"占位段——每图一段：图片居中 + 图号文字置于图下方居中（图号文字与附图说明逐字一致）。
3. 展示全部 PNG 路径给用户审阅（1=通过 2=某幅重绘，说明改哪里）。
4. 版式归一（--preset patent，图片对象自动保留）。
5. 阶段 C 复核：图号与附图说明逐字比对、黑白检查、正文引用（"如图N所示"）与实际图号一致。
