#!/usr/bin/env python3
"""extract_frame — 从报错文本里确定性地找出「用户代码里出错的那一帧」。

为什么需要它：模型看到一坨 stderr 会自己猜哪一行重要，猜错就改错文件。
这个脚本把「哪一帧才是你的代码」变成一条可复现的命令。

规则（差异很重要）：
  * Python traceback 从外到内列帧 → 取【最后一个】用户帧
  * Node / V8 stack 从内到外列帧 → 取【第一个】用户帧
  * 第三方/标准库帧一律跳过（site-packages、node_modules、node:internal、stdlib lib）

用法：pytest 2>&1 | python tools/extract_frame.py     （--json 输出机器可读）
退出码：0 = 找到；2 = 没找到（不猜）。
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

THIRD_PARTY = (
    "site-packages", "dist-packages", "node_modules", "node:internal",
    "<frozen", "/usr/lib/", "/usr/local/lib/", "/lib/", "\\lib\\",
    "/python3.", "\\python3", "/python2.", "\\python2",
)

PY_FRAME = re.compile(r'^\s*File "(?P<file>[^"]+)", line (?P<line>\d+), in (?P<func>\S+)')
JS_FRAME = re.compile(r'^\s*at (?:[^()]*?\()?(?P<file>[^\s():]+):(?P<line>\d+):(?P<col>\d+)\)?\s*$')
ANY_FILE_LINE = re.compile(r'(?P<file>[A-Za-z]:[\\/][^\s:"]+|/[^\s:"]+):(?P<line>\d+)')


def _is_user_code(path: str) -> bool:
    lowered = path.lower()
    return not any(marker in lowered for marker in THIRD_PARTY)


def _read_source(path: str, lineno: int):
    try:
        lines = Path(path).read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return None
    if 1 <= lineno <= len(lines):
        return lines[lineno - 1].strip()
    return None


def extract(text: str):
    is_python = "Traceback (most recent call last)" in text
    candidates = []
    for raw in text.splitlines():
        for pattern, kind in ((PY_FRAME, "python"), (JS_FRAME, "js"), (ANY_FILE_LINE, "generic")):
            match = pattern.search(raw)
            if match:
                file = match.group("file")
                candidates.append({
                    "kind": kind,
                    "file": file,
                    "line": int(match.group("line")),
                    "user_code": _is_user_code(file),
                })
                break
    if not candidates:
        return None
    user = [c for c in candidates if c["user_code"]]
    pool = user if user else candidates
    chosen = pool[-1] if is_python else pool[0]
    chosen["stack"] = "python" if is_python else "js/generic"
    chosen["source"] = _read_source(chosen["file"], chosen["line"])
    chosen["frame_count"] = len(candidates)
    chosen["user_frame_count"] = len(user)
    return chosen


def main(argv) -> int:
    as_json = "--json" in argv
    text = sys.stdin.read()
    if not text.strip():
        print("输入是空的：把 stderr 或日志从 stdin 喂进来", file=sys.stderr)
        return 2
    frame = extract(text)
    if frame is None:
        print("没有找到任何 file:line 形状的帧 —— 不猜。把完整报错贴出来。", file=sys.stderr)
        return 2
    if as_json:
        print(json.dumps(frame, ensure_ascii=False, indent=2))
    else:
        print("%s:%d  (%s, %s)" % (frame["file"], frame["line"], frame["kind"], "user code" if frame["user_code"] else "third-party"))
        if frame["source"]:
            print("  " + frame["source"])
        print("  stack=%s frames=%d user_frames=%d" % (frame["stack"], frame["frame_count"], frame["user_frame_count"]))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
