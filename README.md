# pdf-layout-translate

把含文字和图表的 PDF 翻译成中文，同时保持原版式与图表位置不变（原版打底 + 文字覆盖翻译）。扫描版自动降级为中文对照版。先出样张确认，再整篇处理。

## 安装

```bash
git clone --depth 1 https://github.com/jia295339800/pdf-layout-translate.git
```

将 `SKILL.md` 放入你的 Agent 用户技能目录（user-skills/pdf-layout-translate/）即可。依赖：Python 的 PyMuPDF、numpy、fontTools，以及 Noto CJK 中文字体（需做子集）。

## 核心流程

1. 样张先行：先做 2–3 个代表页样张，确认后才做整篇
2. 全文块索引（四元键 pno/bidx/lidx/span）→ 提取 → 翻译 → 原版打底覆盖
3. 字体子集化（pyftsubset），整本可压到约 2MB
4. 逐行扫描验收：英文残留 / 盖板留白双判据，段首段尾、页首页尾重点扫，数字对账，4x 渲染目检
5. 发布前全量扫描，更新原产物

技能正文含 13 条实战坑清单（圆牌压字、巨字糊页、字体膨胀、混排字号、特殊样式文字、残句清理等）。
