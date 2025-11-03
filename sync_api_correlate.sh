
#!/bin/bash
set -e

echo "🚀 Starting selective sync of fuel_mcp/api/api_correlate.py to all branches..."

# 1️⃣ Ensure we are on feature/gui-gradio-v1.1.1
git checkout feature/gui-gradio-v1.1.1
echo "✅ On branch feature/gui-gradio-v1.1.1"

# 2️⃣ Commit all local changes first
git add .
git commit -m "🔧 Local updates (keep only api_correlate.py for sync)" || echo "🟡 No new changes to commit."

# 3️⃣ Create temp branch for isolated api_correlate.py sync
git checkout -b temp/api-correlate-sync
echo "🌿 Created branch temp/api-correlate-sync"

# 4️⃣ Restore only api_correlate.py from gradio branch cleanly
git restore --source=feature/gui-gradio-v1.1.1 --staged --worktree fuel_mcp/api/api_correlate.py
git add fuel_mcp/api/api_correlate.py
git commit -m "🧩 Sync: Updated api_correlate.py (for all branches)"
echo "✅ Isolated commit created for api_correlate.py"

# 5️⃣ Define branches to update
branches=("main" "feature/docker-v1.1.0" "feature/gui-flask-v1.1.2" "feature/gui-qt-v1.1.3" "feature/agent-v1.2.0")

# 6️⃣ Merge into each branch
for b in "${branches[@]}"; do
  echo "🔄 Merging into $b ..."
  git checkout "$b"
  git merge temp/api-correlate-sync --no-ff -m "🔄 Sync api_correlate.py from feature/gui-gradio-v1.1.1"
  git push origin "$b"
done

# 7️⃣ Return to original branch
git checkout feature/gui-gradio-v1.1.1

# 8️⃣ Cleanup
git branch -d temp/api-correlate-sync
echo "🧹 Temporary branch removed."

echo "✅ Done! api_correlate.py synced to all target branches."