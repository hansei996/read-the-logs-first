# 每日巡检清单（给定时任务的 agent 看）

> 目标：每天用最少的命令回答三个问题——**有没有进展 / 卡在哪 / 下一步做什么**。
> 不要用 `curl`（本机 curl 的 Schannel 坏了，https 一律返 000）。用 `gh`，它在通。

## 1. 执行这几条命令

```powershell
# 两个仓的体量
gh api repos/hansei996/read-the-logs-first --jq '{stars:.stargazers_count,forks:.forks_count,pushed:.pushed_at}'
gh api repos/hansei996/blame-archaeology   --jq '{stars:.stargazers_count,forks:.forks_count,pushed:.pushed_at}'

# 两个外部 PR 的状态（这是最重要的信号）
gh pr view 1010 --repo BehiSecc/awesome-claude-skills --json state,mergeable,comments,reviewDecision
gh pr view 5193 --repo github/awesome-copilot --json state,mergeable,reviewDecision,statusCheckRollup

# CI 最近一次是否还绿
gh run list --repo hansei996/read-the-logs-first --limit 1
gh run list --repo hansei996/blame-archaeology   --limit 1

# 有没有人提 issue / 开 PR 进来
gh issue list --repo hansei996/read-the-logs-first --state all --limit 5
gh issue list --repo hansei996/blame-archaeology   --state all --limit 5
```

## 2. 三段式输出（不要写别的）

```
进展: <只写数字和状态变化。例如 star 0→2；PR #1010 OPEN→MERGED>
卡点: <需要人做的事；没有就写「无」>
下一步: <今天该做的一件事，必须具体到命令或动作>
```

## 3. 升级条件（命中就明写出来，别埋在三段里）

| 条件 | 该做什么 |
|---|---|
| PR #1010 或 #5193 变成 MERGED | 里程碑：在 docs/awesome-lists.md 记下"合并耗时"与"合并后 24h 带星数"，然后按先验顺序批量打剩余清单 |
| 任一 PR 被 CLOSED 或收到 change-request 评论 | **不要重复提**。先读评论，改条目文案/结构，记录到 docs/awesome-lists.md 的"被拒原因"栏 |
| star 达到 20 | heilcheng/awesome-agent-skills 的 20★ 门槛满足，可申报（配合 14 天门槛） |
| 日期 ≥ 2026-11-03 | hesreallyhim/awesome-claude-code（56k★）14 天门槛开闸——注意它**只收网页表单、不收 PR**；heilcheng 同时开闸 |
| CI 变红 | 立即把失败日志前 30 行贴出来，并说明是内容问题还是环境问题；不要自行放宽 tools/skillcheck.py 的校验项 |
| 出现第一个外部 issue | 当天必须回复；这是项目从"demo"变成"有人在用"的分界线 |

## 4. 记录

把当天结果追加到 `docs/status-log.md`（一行日期 + 三段式摘要），然后 push。超过 60 行就只保留最近 30 天。
