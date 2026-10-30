---
name: page-seo-inspector
description: 对一个 URL 做单页 SEO 检查，覆盖 HTTP、索引指令、标题描述、canonical、标题层级、分享标签、结构化数据、图片链接和资源信号。附 Python 脚本，无需第三方数据 API Key，输出分组报告或 JSON。用于“单页 SEO 检查”“产品页 SEO”“分类模板检查”“多语言页面基础检查”。
---

# 单页 SEO 检查

## 运行

`<SKILL_DIR>` 为本 SKILL.md 所在目录。Python 3.10+：

```bash
uv run <SKILL_DIR>/scripts/page_seo_inspector.py https://example.com/products/example/
uv run <SKILL_DIR>/scripts/page_seo_inspector.py https://example.com/products/example/ --json
```

依赖 requests、beautifulsoup4，无需 Key。也可在虚拟环境安装本目录 `requirements.txt`，改用 Python 运行同一脚本。

## 覆盖范围

| 类别 | 检查 |
|---|---|
| HTTP | 本次状态、跳转、内容类型、压缩、HTML大小、脚本请求耗时 |
| 索引指令 | 响应头及 meta robots、canonical、viewport、字符集 |
| 页面描述 | title、description、lang、hreflang标签数量及可选x-default |
| 标题层级 | H1–H6数量、文本、层级线索 |
| 分享预览 | Open Graph和Twitter/X标签 |
| 结构化数据 | JSON-LD语法、@graph / 数组节点和类型、Microdata存在性 |
| 内容与链接 | 字数观察、图片alt及布局线索、懒加载、HTTP(S)内外链 |
| 安全配置 | 安全响应头观察，作为信息项，不当SEO排名缺陷 |
| 页面资源 | head同步外部脚本、样式数量、favicon与资源提示 |

按9类展示每项状态，不只列失败项。默认文本报告，也可用 `--json` 保留原始观察与问题清单。

## 如何转成建议

先读实际输出，再按页面任务选最影响业务的3–5项，分别写：证据、影响、是否需要复核、修复动作与验收方式。只检查一页时，不能把问题扩大为整个产品/分类模板都有问题；要影响模板结论，先追加少量同模板样本。

### 需要保持的判断边界

- **自定义分数**：critical扣15，warning扣3，最低0；它是脚本的核查优先级，不是Google评分、排名潜力或订单预测。不要围绕提高分数推荐无意义改动。
- **初始HTML**：脚本不执行JavaScript。正文、标题或Schema未找到，先用渲染页面/源码或对应官方测试工具复核。抓取失败交付错误和范围，不生成虚构分数。
- **索引**：无noindex不证明已收录；noindex可能符合页面用途。脚本对爬虫专用X-Robots-Tag只给线索，需按目标爬虫确认作用域。domain级规则另用check-crawlability。
- **canonical**：相对链接会解析为绝对链接；缺声明或指向别页需核对重复URL策略，不自动判流量流失。HTTP Link头的canonical另行检查。
- **标题和正文**：title与description长度、H1数量、字数是编辑线索，不是排名硬阈值；按语言和采购任务判断。脚本按空白分词，不适合把中文token数当字数。
- **结构化数据**：解析JSON与识别类型不等于校验完整Schema、当前搜索功能资格或必定展示富结果；Microdata也不能因不是JSON-LD就判错。按当时的官方要求复核适用类型和可见事实。
- **hreflang**：当前只做存在性检查。多语言时另查自指、互返、有效语言/地区/脚本代码、目标页面可达性、canonical和sitemap一致性。x-default是可选回退，不把缺失判为国际化失败。
- **性能**：脚本耗时包含本机网络与下载，不是浏览器TTFB或Core Web Vitals。资源数、同步脚本和图片布局是待测线索，不能代替真实性能测量。
- **图片**：装饰图允许空alt；CSS/fill/aspect-ratio可保留布局空间，静态检测不能验证外部样式。懒加载与尺寸问题需结合首屏、LCP候选和浏览器布局确认。

任务完成后交付报告和具体下一步，不自动修改官网、增加Schema或触发重型审计。

## 查证入口

- [Google 标题链接说明](https://developers.google.com/search/docs/appearance/title-link)
- [Google 多语言页面说明](https://developers.google.com/search/docs/specialty/international/localized-versions)
- [结构化数据基本说明](https://developers.google.com/search/docs/appearance/structured-data/intro-structured-data)
- [Google 规范网址说明](https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls)
