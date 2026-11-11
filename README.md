# Mistery 观点索引与检索 Skill

面向 [Mistery（@wr0789）](https://x.com/wr0789) 公开表达的非官方检索工具。按主题、日期、关键词查找原推链接，辅助阅读和比较不同时期的观点。

**公开版包含 2,639 条原推链接索引、22 条整理摘要和主题导读，不分发推文全文或网友回复。** 资料日期为 2026-09-26 至 2026-11-11，覆盖不完整。主题由关键词辅助标记，摘要由整理者撰写，不能当作作者原文。

## 直接使用

下载本仓库后，用浏览器打开 [离线索引页](mistery-knowledge/assets/知识库.html)。检索不联网，查看原推时才跳转 X。GitHub 文件预览显示 HTML 源码；离线页面需下载后打开。本仓库未开通 GitHub Pages。

也可以使用 Python 3.10 或更新版本，无第三方运行依赖：

```bash
git clone https://github.com/shefferxu/mistery-knowledge.git
cd mistery-knowledge
python -X utf8 mistery-knowledge/scripts/jiansuo.py "恒科 定投"
python -X utf8 mistery-knowledge/scripts/jiansuo.py --topic "交易心理与人性"
python -X utf8 mistery-knowledge/scripts/jiansuo.py --id 2118852349091553792
```

多个关键词默认全部匹配；`--any` 改为任意词匹配；`--order oldest` 按时间正序排列。日期过滤为北京时间，`--since YYYY-MM-DD --until YYYY-MM-DD` 包含首尾日。

## 作为 Skill 使用

将仓库内的 [mistery-knowledge](mistery-knowledge) 文件夹复制到支持 Agent Skills 的工具的技能目录，或直接让助手读取 [SKILL.md](mistery-knowledge/SKILL.md)。

例如：

> 使用 $mistery-knowledge，查找 m姐关于恒科定投的原推，区分整理摘要和已核对的原文。

> 使用 $mistery-knowledge，对比三浪趋势策略和流动性收缩时短线策略的适用条件。

## 内容与范围

- [主题导读](mistery-knowledge/references/主题导读.md)：市场、资金、交易、人性、学习和生活等入口。
- [覆盖说明](mistery-knowledge/references/覆盖说明.md)：范围与缺口。
- [数据说明](mistery-knowledge/references/数据说明.md)：字段及本地资料使用方法。
- `references/index.jsonl`：来源元数据、主题标签及部分整理摘要。
- `scripts/jiansuo.py`：关键词、日期、主题及 ID 检索。

公开索引不包含逐条全文观点归纳，不是账户历史全集，也不包含图片和语音的转写。来源文章中的观点、预测和事实陈述未全部独立核实。历史判断不能直接当作当前行情结论。

## 本地全文检索

用户可自行提供具有使用权限的 JSONL 资料，存放在仓库的 `local_data/` 中：

```bash
python -X utf8 mistery-knowledge/scripts/jiansuo.py "关键词" --data local_data/posts.jsonl
```

该目录已加入 Git 忽略规则。原始采集文件、登录凭据、完整离线全文页及原始语料包均不进入公开版。

## 验证

```bash
python -X utf8 -m unittest discover -s tests -v
```

测试覆盖检索条件、作者范围、精确 ID 和公开索引的内容类型。测试通过不证明原作者观点正确，也不证明内容全量。

## 来源与权利

本项目与原作者无隶属或代言关系。原推及媒体的权利归相应权利人；原文通过来源链接访问。本仓库目前未指定单独的开源许可证。
