# scripts/rss_to_md.py
import os
import feedparser
from markdownify import markdownify as md

# 1) رابط الـ RSS
RSS_URL = "https://eshraq.org/rss.xml"

# 2) مجلّد الإخراج (يتطابق مع posts/)
OUTPUT_DIR = "posts"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 3) جلب وقراءة الخلاصة
feed = feedparser.parse(RSS_URL)

for entry in feed.entries:
    # 4) استخدام تاريخ النشر لاسم الملف yyyy-mm-dd-title.md
    date = entry.published_parsed
    date_prefix = f"{date.tm_year:04d}-{date.tm_mon:02d}-{date.tm_mday:02d}"
    safe_title = "".join(
        c for c in entry.title if c.isalnum() or c in (" ", "-")
    ).rstrip().replace(" ", "-").lower()
    filename = f"{date_prefix}-{safe_title}.md"
    path = os.path.join(OUTPUT_DIR, filename)

    # 5) إذا كان الملف موجودًا نتجاهله
    if os.path.exists(path):
        continue

    # 6) تحويل المحتوى إلى Markdown
    #    بعض الخلاصات تستخدم entry.content، وبعضها entry.summary
    html_content = (
        entry.content[0].value
        if hasattr(entry, "content") and entry.content
        else entry.summary
    )
    content_md = md(html_content)

    # 7) كتابة الملف بصيغة Markdown مع Front Matter
    with open(path, "w", encoding="utf-8") as f:
        f.write("---\n")
        f.write(f"title: \"{entry.title}\"\n")
        f.write(f"date: {date_prefix}\n")
        if hasattr(entry, "tags") and entry.tags:
            f.write("tags:\n")
            for tag in entry.tags:
                f.write(f"  - {tag.term}\n")
        f.write("---\n\n")
        f.write(content_md)

    print(f"Created {path}")
