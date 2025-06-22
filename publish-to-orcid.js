const fs = require('fs');
const path = require('path');
const xml2js = require('xml2js');
const axios = require('axios');

const FEED_PATH = path.join(__dirname, 'feed.xml');
const PUBLISHED_LOG = path.join(__dirname, 'published.txt');

const ORCID_ID = process.env.ORCID_ID;
const ACCESS_TOKEN = process.env.ORCID_TOKEN;
const ORCID_API = 'https://api.orcid.org/v3.0';

function loadPublished() {
  return fs.existsSync(PUBLISHED_LOG)
    ? fs.readFileSync(PUBLISHED_LOG, 'utf-8').split('\n').filter(Boolean)
    : [];
}

function savePublished(guid) {
  fs.appendFileSync(PUBLISHED_LOG, guid + '\n');
}

async function publishItem(item) {
  const pubDate = new Date(item.pubDate[0]);
  const xml = `
<work:work xmlns:work="http://www.orcid.org/ns/work" xmlns:common="http://www.orcid.org/ns/common">
  <work:title>
    <common:title>${item.title[0]}</common:title>
  </work:title>
  <work:type>website</work:type>
  <work:publication-date>
    <common:year>${pubDate.getFullYear()}</common:year>
    <common:month>${String(pubDate.getMonth() + 1).padStart(2, '0')}</common:month>
    <common:day>${String(pubDate.getDate()).padStart(2, '0')}</common:day>
  </work:publication-date>
  <work:external-ids>
    <common:external-id>
      <common:external-id-type>uri</common:external-id-type>
      <common:external-id-value>${item.link[0]}</common:external-id-value>
      <common:external-id-relationship>self</common:external-id-relationship>
    </common:external-id>
  </work:external-ids>
  <work:url>${item.link[0]}</work:url>
  <work:short-description>${item.description[0].slice(0, 500)}</work:short-description>
</work:work>`;

  const url = `${ORCID_API}/${ORCID_ID}/work`;
  const headers = {
    Authorization: `Bearer ${ACCESS_TOKEN}`,
    'Content-Type': 'application/vnd.orcid+xml',
    Accept: 'application/vnd.orcid+xml'
  };

  const res = await axios.post(url, xml, { headers });
  console.log(`✅ نُشر: ${item.title[0]}`);
}

async function main() {
  const xml = fs.readFileSync(FEED_PATH, 'utf-8');
  const parsed = await xml2js.parseStringPromise(xml);
  const items = parsed.rss.channel[0].item;

  const published = loadPublished();

  for (const item of items) {
    const guid = item.guid[0];
    if (!published.includes(guid)) {
      try {
        await publishItem(item);
        savePublished(guid);
      } catch (e) {
        console.error(`❌ خطأ أثناء نشر "${item.title[0]}"`, e.message);
      }
    }
  }
}

main();
