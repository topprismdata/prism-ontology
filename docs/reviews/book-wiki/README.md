# 销售管理 LLM Wiki

面向 LLM 消费的销售管理领域知识库，从 21 份权威文献（经典教材、学术期刊、专利、行业报告）构建。
用途：为 prism-ontology（销售管理世界模型）等本体/语义层项目提供**带页码锚点的权威依据**。

## 架构

```text
book-wiki/
├── README.md            # 本文件：结构与约定
├── INDEX.md             # 21 份文献总索引（key、类型、页数、相关度、一句话定位）
├── ARCHITECTURE.md      # LLM wiki 架构选型报告（DeepWiki-Open / STORM / LightRAG / RAGFlow 对比与推荐）
├── books/<key>.md       # 书籍卡片：定位 + 章节地图(带PDF页码) + 核心框架 + 评审价值
├── concepts/<slug>.md   # 概念页面：定义 + 核心框架 + 跨文献对照(≥3来源带页码) + 对本体的评审要点
└── raw/<key>.txt        # pdftotext -layout 全文（\x0c 换页符 = PDF 页边界，页码锚点的依据）
```

## 页面约定（LLM 消费契约）

1. **YAML front-matter 必填**：`type`（book/concept）、`key`/`slug`、`title`、`sources`、`relevance_to_ontology`。
2. **引用格式**：`[key p.N]`（如 `[zoltners1983-territory-alignment p.1244]`）。N 为 **PDF 物理页码**，可通过 `raw/<key>.txt` 按换页符切分回溯验证。
3. **概念页规则**：每个核心论断至少 3 份独立文献支撑；"对 prism-ontology 的评审要点"必须落到具体类/属性/关系名。
4. **卡片规则**：章节地图逐章带 PDF 页码；核心框架清单每条 50 字内。

## 文献清单

见 [INDEX.md](INDEX.md)。四类：经典教材（Zoltners×3、Johnston & Marshall、Kotler、Stern、Farris）、学术期刊（Management Science、JPSSM×2、EJOR×2）、专利与白皮书（US7620564、brandidea PJP）、行业报告（Salesforce 年报、全渠道）。

## 构建方法（透明度声明）

- 全文由 `pdftotext -layout` 提取（`raw/`，约 200 万词），**全部语料被处理**；
- 章节地图与概念页面由 LLM 按"grep 定位 → 换页符切分验证页码 → 上下文提炼"流程生成，引用可回溯；
- 原书版权归原作者，本 wiki 仅用于本地研究/评审，不对外分发原文文本。

## 状态

- [x] 语料提取（21/21）
- [x] 架构选型报告（ARCHITECTURE.md：静态 markdown 即架构）
- [x] 书籍卡片 21/21
- [x] 概念页面 12/12（含 ontology-fundamentals-study-notes.md 本体工程基础笔记）
- [x] 本体评审报告 → ../_verification/prism-ontology-EXPERT-REVIEW.md
