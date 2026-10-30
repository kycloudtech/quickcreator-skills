# 首批公开 Skill：同步与适配记录

日期：2026-10-30。

## 来源

本批四个 Skill 来自内部 seo-operations 工作库的本地安装快照，对应版本 `af8cf9bef70a8757c2451abea42a112722f14f96`。没有同步完整私有工具库，也没有在本次操作中检查远端是否有更新。

保留原目录名，以便与后续维护对应。每个目录复制实际文件，包含所需脚本、参考资料和模板，不使用指向安装缓存的符号链接。

[源文件清单](public-skills-source-manifest.json) 记录完整提交、原始相对路径与 SHA-256；它描述本次输入版本，公开版文件经过以下适配，哈希不应与输入完全一致。后续同步应比较改动，不能整目录覆盖而丢失这些适配。

## 公开版适配

| Skill | 保留 | 调整 |
|---|---|---|
| b2b-website-sales-audit | 买家决策判据、证据模板、客户摘要与可选销售材料 | 默认输出网站负责人报告；先采4–6页，必要时扩样；平台实测可选；移除未发布兄弟Skill的必需依赖和模板中的内部引用 |
| check-crawlability | requests脚本、HTTP/robots/sitemap/响应头与可选llms配对检查 | robots只读主机根路径，按UA和路径判读规则；失败标未知；区分训练与搜索；地图需有效XML；响应头检查实际输入页面 |
| page-seo-inspector | 9类检查、文本/JSON报告与图片布局检测 | 说明自定义分数；标题长度、字数、安全头等降为核查提示；支持JSON-LD数组与@graph，异常节点不崩溃；相对canonical解析；HTTP(S)内链计数；移除过时的富结果保证 |
| geo-content-audit | 段落定位、原文证据、事实/来源/结构审阅和具体改写 | 正文可独立使用；去掉私有凭证与服务；研究关联与客户效果分开；不补造资料；只有正文时技术项未验证 |

新增两个脚本目录的 `requirements.txt`，根README、`.gitignore` 和离线回归样例。沿用本仓库现有MIT许可证；没有改动Skill Builder、站点或发布工作流。

## 验证

离线回归测试覆盖：根robots范围、训练与搜索分离、同名UA组合并、最长规则与Allow同等优先、通配符与末尾锚点、百分号编码、抓取失败未知、HTML伪地图、命名空间地图索引、实际输入路径、JSON-LD异常节点与@graph、相对canonical、none指令、编辑长度提示、内链计数、抓取失败不生成分数及完整JSON输出。

安装两个 `requirements.txt` 中依赖后，从仓库根运行：

```bash
python -m unittest discover -s tests -v
```

另验证四个Skill的frontmatter、相对文档引用、Python语法、符号链接和公开文件中的凭证/本地路径残留。具体执行结果以本次交付说明为准。

本次验证不等于在每个AI客户端完成真实网站端到端实测；网站WAF、JavaScript渲染、真实AI平台回答及表单收件仍需在相应环境核验。
