import fs from 'node:fs/promises';

// Two workers, a pause between requests, and no automatic retry storm.
const base = process.argv[2] || 'https://linkjagd-tools.vercel.app';
const output = process.argv[3] || 'production-audit.json';
const pause = () => new Promise(resolve => setTimeout(resolve, 300));
async function inspect(url) {
  const start = Date.now();
  try {
    const response = await fetch(url, {signal: AbortSignal.timeout(30000)});
    const body = await response.text();
    return {url, status: response.status, finalUrl: response.url, ms: Date.now()-start,
      canonical: body.match(/<link[^>]*rel="canonical"[^>]*href="([^"]+)"/)?.[1],
      body};
  } catch (error) { return {url, status: 0, error: error.message, code: error.cause?.code, ms: Date.now()-start}; }
}
const sitemap = await inspect(`${base}/sitemap.xml`);
const robots = await inspect(`${base}/robots.txt`);
const previous = process.argv[4] ? JSON.parse(await fs.readFile(process.argv[4], 'utf8')) : null;
const urls = previous ? previous.results.filter(r=>r.status!==200).map(r=>r.url) : [...new Set([base+'/', ...['/tools','/blog','/linkjagd','/vergleiche','/tools?q=Zapier','/tools?sort=alphabetisch'].map(p=>base+p),
  ...[...(sitemap.body || '').matchAll(/<loc>(.*?)<\/loc>/g)].map(m=>m[1].replaceAll('&amp;','&'))])];
if(urls.some(url=>new URL(url).origin!==new URL(base).origin)) throw new Error('Sitemap includes another origin; refusing crawl');
const results=[];
let cursor=0;
let transportFailures=0;
await Promise.all(Array.from({length:2},async()=>{
  while(cursor<urls.length && transportFailures<3){const result=await inspect(urls[cursor++]); transportFailures=result.status===0?transportFailures+1:0; delete result.body; results.push(result); if(results.length%100===0) console.log(`Checked ${results.length}/${urls.length}`); await pause();}
}));
const failures = results.filter(r=>r.status!==200);
const retests=[];
if(transportFailures<3) for(const failure of failures){await pause(); const result=await inspect(failure.url); delete result.body; retests.push(result);}
delete sitemap.body;
await fs.writeFile(output,JSON.stringify({at:new Date().toISOString(),base,sitemap,robots,results,retests},null,2));
console.log(JSON.stringify({tested:results.length,failures:failures.length,retestFailures:retests.filter(r=>r.status!==200).length,output}));
