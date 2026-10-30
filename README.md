# QuickCreator Skills

面向 B2B 外贸企业的建站、SEO 与 GEO 实用技能库。

从一个网址、一个页面或一段正文开始，找出网站在产品表达、采购信任、搜索发现与询盘路径上的具体问题，得到带证据、能执行、可复核的改进建议。适合企业负责人、外贸市场与运营人员、建站团队，也适合培训课堂实操。

这里开放我们在实际工作中使用的部分方法、检查脚本和报告模板。第一批提供一个综合体检入口和三个专项检查，后续逐步扩展。

## 先选一个适合的 Skill

| Skill | 用来解决什么 | 需要准备什么 | 交付与后续改进方向 |
|---|---|---|---|
| [外贸网站获客体检](b2b-website-sales-audit/SKILL.md) `b2b-website-sales-audit` | 看懂产品表达、采购信任、SEO 基础和询盘路径的主要障碍 | 一个网站网址；可补充产品和目标市场 | 网站负责人能看懂的诊断摘要、证据和优先动作；用于询盘流程改造、核心产品页优化及网站升级决策 |
| [搜索与 AI 抓取检查](check-crawlability/SKILL.md) `check-crawlability` | 检查 HTTPS、robots、sitemap、响应头与指定爬虫的公开访问规则 | 一个域名或网址；可运行 Python 的环境 | JSON 检测记录和问题清单；用于 robots、域名跳转、抓取及服务器配置修复 |
| [单页 SEO 检查](page-seo-inspector/SKILL.md) `page-seo-inspector` | 检查标题、描述、canonical、结构化数据、图片和资源等基础信号 | 一个页面网址；可运行 Python 的环境 | 易读报告或 JSON；用于产品与分类模板、多语言 SEO 和前端优化 |
| [单页 GEO 内容检查](geo-content-audit/SKILL.md) `geo-content-audit` | 找出事实、来源、答案表达和段落结构的改进空间 | 粘贴正文即可；也可提供 URL | 定位到原文段落的发现及改写示例；用于产品资料整理、商业页优化、采购指南及内容运营 |

不知道从哪里开始，先用 **外贸网站获客体检**。已经明确问题，再选专项检查。四个 Skill 可以单独使用，无需安装整个私有工具库。

仓库还保留 [QuickCreator Skill Builder](quickcreator-skill-builder/README.md)，用于创建、管理和发布 QuickCreator 平台技能；它有独立的连接设置，不是上述四项检查的必需依赖。

## 安装

把需要的 **整个 Skill 目录**复制到 AI 助手的技能目录，保留其中的 `SKILL.md`、`scripts/`、`references/` 和 `assets/`。只复制说明文件会丢失脚本或模板。

| AI 助手 | 当前项目内安装 |
|---|---|
| Codex | `.agents/skills/<skill-name>/` |
| Claude Code | `.claude/skills/<skill-name>/` |
| Cursor | `.cursor/skills/<skill-name>/` |

其他支持 Skill 的客户端，可按其文档放置目录。实际可用能力取决于客户端提供的网页读取、浏览器和命令执行工具；目录可被识别并不代表所有工具都已配置。

例如，先把仓库下载到本地，在你要检查网站的工作项目中，把四个目录复制到相应技能目录。重新加载客户端后，在对话中点名技能并提供输入。

### 运行环境

- **综合体检**：需要公开网页读取或浏览器能力。搜索、移动端交互与 AI 平台实测按当前可用工具执行，未完成的项目标为“未验证”。
- **抓取 / 单页 SEO 检查**：推荐 Python 3.10+ 和 `uv`。脚本声明了依赖，`uv run` 首次运行会下载所需包；也可在虚拟环境手动安装。
- **GEO 内容检查**：粘贴正文可直接分析；URL 模式需要网页读取。只有正文时，HTML 和 Schema 状态标为“未验证”。

上述四项基础检查 **不要求第三方 SEO 数据 API Key**，也不要求 GSC、GA4 或 CRM 后台授权。AI 客户端本身及用户主动启用的外部工具可能收费；实际 AI 平台曝光测试需要另有可用能力，不包含在“无需数据 Key”的承诺中。

## 试一次

把示例域名替换为自己的网址。

**外贸网站获客体检**

```text
使用 b2b-website-sales-audit 检查 https://example.com。
重点看产品是否讲清楚、采购方是否信任、SEO 基础和询盘路径。
给我带页面证据的前三项改进建议；无法验证的地方请标明。
```

**搜索与 AI 抓取检查**

```text
使用 check-crawlability 检查 https://example.com/products/。
解释 Googlebot 和 AI 搜索爬虫在该路径的 robots 规则，以及需要修复的配置。
```

**单页 SEO 检查**

```text
使用 page-seo-inspector 检查 https://example.com/products/example-product/。
区分已确认问题与需要浏览器复核的提示，给出修复顺序。
```

**单页 GEO 内容检查**

```text
使用 geo-content-audit 检查下面的采购指南，目标读者是海外采购人员。
请引用原文定位问题，给出可直接替换的段落，不补造数据或资质。
[在这里粘贴正文]
```

### 直接运行检测脚本

在本仓库根目录运行，也可把路径替换为实际安装目录：

```bash
uv run check-crawlability/scripts/crawl_check.py https://example.com/
uv run page-seo-inspector/scripts/page_seo_inspector.py https://example.com/products/example-product/
uv run page-seo-inspector/scripts/page_seo_inspector.py https://example.com/products/example-product/ --json
```

不使用 `uv` 时，在 Python 3.10+ 虚拟环境中执行：

```bash
python -m pip install -r check-crawlability/requirements.txt
python -m pip install -r page-seo-inspector/requirements.txt
python check-crawlability/scripts/crawl_check.py https://example.com/
python page-seo-inspector/scripts/page_seo_inspector.py https://example.com/ --json
```

## 如何读报告

每个重点发现应说明 **看到了什么 → 对采购或发现有什么影响 → 建议怎么改 → 如何复核**，并列出检查页面、日期和限制。

- 综合体检是公开页面抽样。没有后台或表单提交记录，不能据此判断实际流量、询盘量或收件是否正常。
- 抓取检查反映公开规则和本次请求结果。robots 允许不等于已收录，也不证明真实爬虫能通过 CDN / WAF；训练爬虫和搜索爬虫分别解释。`llms.txt` 是可选补充，不作为通过门槛。
- 单页脚本读取服务器返回的 HTML，不执行 JavaScript。静态结果里没找到，不等于渲染后没有。内置分数是自定义清单分，不是 Google 评分或排名预测。
- GEO 内容检查评估内容准备度。建议改写不代表已证明 AI 不引用的原因，也不承诺引用率提升；实际提及、引用与推荐需要保存真实平台回答再判断。

检查默认在使用者环境运行。两个检测脚本会请求目标网站及其公开链接，不向 QuickCreator 回传报告。AI 助手和所选外部工具如何处理输入，仍取决于使用者的客户端和服务设置。

## 从检查到改进

小问题可按报告自行修复；需要开发或业务资料时，把证据交给网站团队。可以从一条询盘路径、一个产品模板或一份采购指南开始，约定可核验的交付，再决定是否扩大范围。网站升级应建立在实际问题与实施限制之上。

需要了解 QuickCreator 的建站、SEO 与 GEO 能力，可访问 [QuickCreator 官网](https://www.quickcreator.io/)。开源技能可独立使用。

## 反馈与贡献

欢迎在 [Issues](https://github.com/kycloudtech/quickcreator-skills/issues) 提交问题或建议。请附 Skill 名称、运行方式、预期和实际结果；公开前删去凭证、个人信息和未获授权的客户资料。脚本修复请附可复现样例。

本批公开版本的来源与适配记录见 [同步记录](docs/public-skills-sync.md)。

## 许可证

采用 [MIT License](LICENSE)，允许在许可条件下使用、修改和商用。转载或分发时请保留版权和许可声明。
