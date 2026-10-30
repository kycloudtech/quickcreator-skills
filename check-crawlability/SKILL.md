---
name: check-crawlability
description: 检查网站公开抓取信号，包括 HTTP 到 HTTPS 跳转、根目录 robots.txt、按 User-agent 和目标路径匹配的规则、sitemap、X-Robots-Tag 及搜索与 AI 爬虫规则。附可运行脚本，输出 JSON 和请求记录，无需第三方数据 API Key。用于“搜索与 AI 抓取检查”“robots 检查”“网站能否被抓取”。
---

# 搜索与 AI 抓取检查

## 运行

`<SKILL_DIR>` 为本 SKILL.md 所在目录。推荐 Python 3.10+ 与 uv：

```bash
uv run <SKILL_DIR>/scripts/crawl_check.py https://example.com/products/example/
```

也可在虚拟环境安装本目录 `requirements.txt`，然后用 Python 运行同一脚本。仅依赖 requests，无需 Key；首次安装依赖需要网络。

## 检查范围

- HTTP 到 HTTPS 的跳转链与本次请求状态。
- 对应协议、域名和端口**根目录**的 `/robots.txt`。子目录文件不能代替主机根规则。
- 合并同名 User-agent 组，按具体爬虫组优先于 `*`、最长路径规则优先、同等匹配 Allow 优先解释；支持 `*` 和末尾 `$`。
- 针对输入路径分别记录搜索 / AI 爬虫的规则状态。规则检查不通过伪装UA实测真实爬虫网络访问。
- robots 声明的 sitemap 优先，再探输入 URL 父路径下的常见地图名；只认可根元素为 urlset / sitemapindex 的 XML。找到一个地图不代表发现全部地图，索引的 loc 数是子地图数，不是全站URL总数。
- 输入页面（跟随跳转）的 HTTP 状态、X-Robots-Tag 与缓存等响应头。页面源码中的 meta noindex 另用单页检查。
- 可选的 llms.txt 及其同源 Markdown 链接。原脚本保留最多10组配对检查；这些是社区约定的连通性提示，不能当作 AI 搜索必需条件。

## 结果与解释

保留 JSON，重点读取 `robots`、`ai_crawlers.bots`、`sitemap`、`page_headers` 和 `issues_summary`，报告检查时间、输入路径、实际请求与错误。

- `allowed` / `not_declared` 只表示本次取得的 robots 规则对测试路径未禁止，不证明已收录、能过 WAF 或会被推荐。
- `blocked` / `blocked_by_wildcard` 只对应记录的路径与爬虫，不扩大成所有爬虫或全站均被禁止。
- robots 获取失败、429、5xx、网络错误或异常 HTML 返回时标 `unknown`，不能据空文本输出“默认允许”。404/410单独记录为未发现规则。
- GPTBot、ClaudeBot 等训练规则和 OAI-SearchBot 等搜索规则分开报告；训练限制不直接推成搜索不可见。
- noindex 可能是正确配置。先确认页面是否本应进入搜索；robots 禁抓与 noindex 不是同一种控制。
- 缺 sitemap、llms.txt 或 HTML/Markdown 配对不单独构成搜索阻断。没有检测到地图，写“本轮候选位置未发现”。

默认给最多3–5项证据明确的修复建议，附路径、规则或响应头和复测方法。服务错误允许用另一个可用客户端复核；仍失败则交付限制，不无限重试。不因发现问题而修改网站配置。

## 依据

- [Google robots 解释规则](https://developers.google.com/crawling/docs/robots-txt/robots-txt-spec)
- [RFC 9309](https://www.rfc-editor.org/rfc/rfc9309.html)
- [Google AI 功能与网站](https://developers.google.com/search/docs/appearance/ai-features)

具体平台的爬虫名称和用途会变化；涉及配置改动时再核对该平台当前官方文档。脚本结果是公开规则抽样，不是索引诊断或 AI 可见度测试。
