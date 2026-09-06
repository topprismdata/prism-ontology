# 架构决定（简版）

**决定：静态 markdown wiki 即最终架构，不引入独立 RAG 服务。**

## 理由

1. **语料规模小**：21 份文献 ≈ 200 万词 ≈ 25MB 文本。LLM 直接 `grep` + 按页读取完全够用，检索延迟毫秒级，无需向量库。
2. **消费方是 LLM 本身**：本 wiki 的主要读者是 agent（ZCode/评审流程）。对 LLM 而言，"front-matter 索引 + 页码锚点 + grep 回溯"比 RAG 检索更**可控、可验证**——每条引用都能回到 `raw/*.txt` 按换页符切分校验，杜绝幻觉引用。
3. **零运维**：无需 docker/服务/索引重建；wiki 即 git 仓库，天然版本化（这本身就是 DeepWiki/STORM 类产品的核心输出物）。

## 与现有方案的关系（借鉴而非部署）

| 方案 | 借鉴点 | 不采用原因 |
|---|---|---|
| DeepWiki-Open (17.9k★) | 层级页面组织（总览→书籍→概念）、Mermaid 关系图 | 面向代码仓库设计，文档输入需改造；重（Next.js+Python+LiteLLM） |
| Stanford STORM | 多视角提问→大纲→带引用成文 | 面向"从零写条目"，我们的引用必须锚定已有文献页码 |
| LightRAG / GraphRAG | 实体图谱、跨文档概念聚合 | 200万词规模收益低于成本；概念页已显式聚合跨书观点 |

## 检索协议（LLM 消费入口）

```bash
# 1. 查概念：先读索引
cat INDEX.md
# 2. 定位文献与页码：读概念页/书籍卡片的引用 [key p.N]
# 3. 回溯验证：按换页符切分原文取第 N 页
awk 'BEGIN{RS="\f"} NR==N' raw/<key>.txt
# 4. 全文检索
grep -n "关键词" raw/*.txt
```

## 演进路径（如果以后需要）

- 语料 > 50 份或多用户并发问答时：加 **LightRAG**（单机、轻量、支持本地模型）做图谱检索层，`books/`+`concepts/` markdown 直接作为 ingestion 语料。
- 需要多人浏览 UI 时：任何 markdown 站点生成器（如 mkdocs）直接可用，无需改造。
