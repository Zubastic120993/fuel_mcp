"""
fuel_mcp/core/generate_changelog.py
===================================
Automatic changelog + QA generator for Fuel MCP
Version 2.0 — Adds pytest summary and metadata
"""

import subprocess
import platform
import os
from datetime import datetime, UTC
from pathlib import Path
import getpass
import re

# =====================================================
# ⚙️ Setup paths
# =====================================================
LOGS_DIR = Path("logs")
LOGS_DIR.mkdir(exist_ok=True)
timestamp = datetime.now(UTC).isoformat()

# =====================================================
# 🔍 Detect current version from mcp_api.py
# =====================================================
API_PATH = Path("fuel_mcp/api/mcp_api.py")
version = "unknown"
if API_PATH.exists():
    text = API_PATH.read_text()
    match = re.search(r'version="([\d\.]+)"', text)
    if match:
        version = match.group(1)

# =====================================================
# 🧪 Run pytest and capture output
# =====================================================
print("🧪 Running tests...")
pytest_result = subprocess.run(
    ["pytest", "-q", "--maxfail=1", "--disable-warnings"],
    capture_output=True,
    text=True
)

test_summary = pytest_result.stdout.strip().splitlines()[-1] if pytest_result.stdout else "No test summary."
if pytest_result.returncode == 0:
    test_status = "✅ All tests passed"
else:
    test_status = "❌ Some tests failed"

# =====================================================
# 🧱 Get last 5 git commits
# =====================================================
def get_git_info():
    try:
        commits = subprocess.check_output(
            ["git", "log", "-5", "--pretty=format:%h|%s|%ci"],
            text=True
        ).strip().split("\n")
        parsed = []
        for c in commits:
            parts = c.split("|")
            if len(parts) == 3:
                parsed.append({"hash": parts[0], "message": parts[1], "date": parts[2]})
        return parsed
    except subprocess.CalledProcessError:
        return []

commits = get_git_info()

# =====================================================
# 🧾 Compose changelog content
# =====================================================
changelog_path = LOGS_DIR / f"CHANGELOG_v{version}.md"

system_info = f"{platform.system()} {platform.release()} ({platform.machine()})"
python_info = platform.python_version()
user = getpass.getuser()

content = [
    f"# 🧩 Fuel MCP — CHANGELOG v{version}",
    "",
    f"**Generated:** {timestamp}",
    f"**User:** {user}",
    f"**OS:** {system_info}",
    f"**Python:** {python_info}",
    "",
    f"## 🧪 Test Summary",
    f"{test_status}",
    f"```\n{test_summary}\n```",
    "",
    "## 🧠 Recent Commits",
]

for c in commits:
    content.append(f"- `{c['hash']}` — {c['message']} ({c['date']})")

content.append("")
content.append("---")
content.append("**Generated automatically by Fuel MCP QA Generator v2.0**")

# =====================================================
# 💾 Write changelog file
# =====================================================
changelog_path.write_text("\n".join(content), encoding="utf-8")
print(f"✅ CHANGELOG generated → {changelog_path}")