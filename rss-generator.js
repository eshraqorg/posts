const fs = require('fs');
const path = require('path');
const matter = require('gray-matter');
const { parseISO, format } = require('date-fns');

const postsDir = path.join(__dirname, 'posts');
const files = fs.readdirSync(postsDir).filter(file => file.endsWith('.md'));

const items = files.map(file => {
  const fullPath = path.join(postsDir, file);
  const content = fs.readFileSync(fullPath, 'utf-8');
  const { data, content: body } = matter(content);
  const url = `https://eshraqorg.github.io/posts/${file.replace(/\.md$/, '')}`;
  const pubDate = data.date ? format(parseISO(data.date), 'EEE, dd MMM yyyy HH:mm:ss xx') : new Date().toUTCString();
  return `
    <item>
      <title>${data.title || file}</title>
      <link>${url}</link>
      <guid>${url}</guid>
      <pubDate>${pubDate}</pubDate>
      <description><![CDATA[${body.substring(0, 300)}...]]></description>
    </item>`;
}).join('\n');

const rss = `<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0">
<channel>
  <title>مدونة إشراق</title>
  <link>https://eshraqorg.github.io/posts</link>
  <description>مقالات الصحة النفسية والتنمية المجتمعية</description>
  <language>ar</language>
  ${items}
</channel>
</rss>`;

fs.writeFileSync(path.join(__dirname, 'feed.xml'), rss);
console.log('✔ تم إنشاء RSS feed بنجاح.');
