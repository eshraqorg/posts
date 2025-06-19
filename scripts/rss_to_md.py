import os
import feedparser
from markdownify import markdownify as md

RSS_URL = "https://eshraq.org/rss.xml"
OUTPUT_DIR = "posts"
os.makedirs(OUTPUT_DIR, exist_ok=True)

feed = feedparser.parse(RSS_URL)
for entry in feed.entries:
    date = entry.published_parsed
    date_prefix = f"{date.tm_year:04d}-{date.tm_mon:02d}-{date.tm_mday:02d}"
    safe_title = "".join(c for c in entry.title if c.isalnum() or c in (' ', '-')).rstrip().replace(' ', '-').lower()
    filename = f"{date_prefix}-{safe_title}.md"
    path = os.path.join(OUTPUT_DIR, filename)
    if os.path.exists(path):
        continue
    content_md = md(entry.content[0].value)
    with open(path, "w", encoding="utf-8") as f:
        f.write("---
")
        f.write(f"title: \"{entry.title}\"\n")
        f.write(f"date: {date_prefix}\n")
        if 'tags' in entry:
            tags = entry.tags
            tag_list = [tag.term for tag in tags]
            f.write("tags:\n")
            for t in tag_list:
                f.write(f"  - {t}\n")
        f.write("---\n\n")
        f.write(content_md)
    print(f"Created {path}")