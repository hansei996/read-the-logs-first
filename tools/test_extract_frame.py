"""extract_frame 的回归测试：直接 python tools/test_extract_frame.py 就能跑（无第三方依赖）。"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from extract_frame import extract  # noqa: E402

NODE = """
C:\\proj\\src\\rates.js:16
TypeError: Cannot read properties of null (reading 'USD')
    at convert (C:\\proj\\src\\rates.js:16:21)
    at C:\\proj\\src\\order.js:5:18
    at Module._compile (node:internal/modules/cjs/loader:1830:14)
"""

PY = """
Traceback (most recent call last):
  File "C:\\app\\main.py", line 12, in <module>
    run()
  File "C:\\app\\main.py", line 8, in run
    parse(cfg)
  File "C:\\Python312\\Lib\\json\\__init__.py", line 300, in loads
    raise JSONDecodeError(...)
"""


def test_node_picks_innermost_user_frame():
    frame = extract(NODE)
    assert frame is not None
    assert frame["file"].endswith("rates.js"), frame
    assert frame["line"] == 16


def test_node_skips_node_internal():
    frame = extract(NODE)
    assert "node:internal" not in frame["file"]


def test_python_picks_innermost_user_frame_and_skips_stdlib():
    frame = extract(PY)
    assert frame is not None
    assert frame["file"].endswith("main.py"), frame
    assert frame["line"] == 8


def test_no_frame_returns_none_instead_of_guessing():
    assert extract("everything is fine\n") is None


if __name__ == "__main__":
    failures = 0
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            try:
                fn()
                print("PASS", name)
            except AssertionError as exc:
                failures += 1
                print("FAIL", name, "->", exc)
    print("%d failed" % failures)
    sys.exit(1 if failures else 0)
