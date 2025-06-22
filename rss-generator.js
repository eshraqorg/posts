const fs = require('fs');
const path = require('path');
const matter = require('gray-matter');
const { format } = require('date-fns');

const postsDir = path.join(__dirname, 'posts');
const feedPath = path.join(__dirname, 'feed.xml');

const siteUrl = 'https://eshraqorg.github.io/posts';

function generateFeed() {
  const files = fs.readdirSync(postsDir).filter(file => file.endsWith('.md'));

  const items = files.map(filename => {
    const filePath = path.join(postsDir, filename);
    const fileContent = fs.readFileSync(filePath, 'utf8');
    const { data, content } = matter(fileContent);

    const title = data.title || filename;
    
    let pubDate;
    try {
      if (typeof data.date === 'string') {
        pubDate = new Date(data.date);
      } else {
        pubDate = fs.statSync(filePath).ctime;
      }
    } catch (e) {
      pubDate = new Date();
    }

    const url = `${siteUrl}/${filename.replace('.md', '')}.html`;

    return `
  <item>
    <title>${title}</title>
    <link>${url}</link>
    <pubDate>${format(pubDate, 'EEE, dd MMM yyyy HH:mm:ss xx')}</pubDate>
    <guid>${url}</guid>
    <description><![CDATA[${content.slice(0, 200)}...]]></description>
  </item>`;
  }).join('\n');

  const xml = `<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
<channel>
  <title>مدونة إشراق</title>
  <link>${siteUrl}</link>
  <description>تحديث تلقائي للمقالات</description>
  <language>ar</language>
  ${items}
</channel>
</rss>`;

  fs.writeFileSync(feedPath, xml, 'utf8');
  console.log('✅ تم إنشاء ملف feed.xml بنجاح');
}

generateFeed();
