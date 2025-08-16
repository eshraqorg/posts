import feedparser
import os
from markdownify import markdownify as md
import subprocess

# رابط RSS أو مسار feed.xml محلي
RSS_URL = "https://example.com/rss.xml"  # ضع الرابط الصحيح أو "feed.xml"
OUTPUT_DIR = "posts"

# التأكد من وجود المجلد
os.makedirs(OUTPUT_DIR, exist_ok=True)

# قراءة RSS
feed = feedparser.parse(RSS_URL)

changed_files = []

# إنشاء/تحديث ملفات Markdown
for entry in feed.entries:
    title = entry.title
    content = md(entry.summary)
    # إزالة أي شرطة من اسم الملف لتجنب مشاكل
    filename = os.path.join(OUTPUT_DIR, f"{title}.md".replace("/", "-"))
    
    # تحقق إذا الملف جديد أو تغير محتواه
    if not os.path.exists(filename) or open(filename, "r", encoding="utf-8").read() != f"# {title}\n\n{content}":
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"# {title}\n\n{content}")
        changed_files.append(filename)

# إذا هناك تغييرات، إضافتها إلى Git ودفعها
if changed_files:
    # إعداد بيانات المستخدم الافتراضية
    subprocess.run(["git", "config", "--global", "user.name", "github-actions"], check=True)
    subprocess.run(["git", "config", "--global", "user.email", "actions@github.com"], check=True)
    
    # إضافة الملفات المعدلة
    subprocess.run(["git", "add"] + changed_files, check=True)
    subprocess.run(["git", "commit", "-m", "Sync RSS articles"], check=True)
    
    # سحب آخر التحديثات مع rebase لتجنب رفض الدفع
    subprocess.run(["git", "pull", "--rebase", "origin", "main"], check=True)
    
    # دفع التغييرات
    subprocess.run(["git", "push", "origin", "main"], check=True)
else:
    print("No changes detected.")
