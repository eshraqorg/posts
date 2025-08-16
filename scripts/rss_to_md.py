import feedparser
import os
from markdownify import markdownify as md
import subprocess

# رابط RSS أو ملف feed.xml
RSS_URL = "https://example.com/rss.xml"  # أو مسار محلي: "feed.xml"
OUTPUT_DIR = "posts"

os.makedirs(OUTPUT_DIR, exist_ok=True)

feed = feedparser.parse(RSS_URL)

changed_files = []

for entry in feed.entries:
    title = entry.title
    content = md(entry.summary)
    filename = os.path.join(OUTPUT_DIR, f"{title}.md".replace("/", "-"))
    
    # تحقق إذا الملف جديد أو تغيّر
    if not os.path.exists(filename) or open(filename, "r", encoding="utf-8").read() != f"# {title}\n\n{content}":
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"# {title}\n\n{content}")
        changed_files.append(filename)

# إضافة الملفات الجديدة أو المعدلة إلى Git ودفعها
if changed_files:
    subprocess.run(["git", "config", "--global", "user.name", "github-actions"], check=True)
    subprocess.run(["git", "config", "--global", "user.email", "actions@github.com"], check=True)
    subprocess.run(["git", "add"] + changed_files, check=True)
    subprocess.run(["git", "commit", "-m", "Sync RSS articles"], check=True)
    subprocess.run(["git", "push"], check=True)
else:
    print("No changes detected.")
