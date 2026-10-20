# read-the-logs-first

> **先读日志，再动手。**

给任意 coding agent 用的技能。专治“猜着改”：在它引用出错那一行、打开出错的那一帧、说出根因之前，任何修改都不许发生。

适用于 Claude Code、Codex、Cursor、Gemini CLI、DeepSeek Harness —— 只要能加载 `SKILL.md` / `AGENTS.md`。

## 安装

把下面这句话粘给你的 agent：

```text
从 https://github.com/<you>/read-the-logs-first 安装 read-the-logs-first 技能，按 AGENTS.md 的说明做。
```

## 它做什么

阻止 agent 在读懂错误之前给方案：先逐字引用报错、先打开出错的那一帧、先说出根因，然后只改一处、再跑一遍原命令。

## 前后对比

*（示意对话，非录屏）*

| 之前 | 之后 |
|---|---|
| “这大概是依赖版本问题。先把 `jsonwebtoken` 升一下，顺手把中间件也重构了，你试试还报不报错。” | “`TypeError: Cannot read properties of undefined (reading 'sub')` —— `src/auth.ts:47:22`。第 47 行的 `SECRET` 是 undefined，因为 `src/index.ts` 没有导入 dotenv。改 1 行，然后跑 `npm run dev` 验证。” |

## 十条规则

见 [SKILL.md](./skills/read-the-logs-first/SKILL.md)。第 2、3 条是承重的，删了这技能就废了；第 8、10 条可以按你的口味放宽。

## License

MIT
