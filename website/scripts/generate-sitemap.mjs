import { promises as fs } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const routesPath = join(__dirname, '..', 'src', 'router', 'sitemap-routes.json');
const publicPath = join(__dirname, '..', 'public');
const sitemapPath = join(publicPath, 'sitemap.xml');

const baseUrl = (process.env.SITEMAP_BASE_URL || 'https://menu.casavazquez.de').replace(/\/$/, '');
const today = new Date().toISOString().split('T')[0];

async function generate() {
  const raw = await fs.readFile(routesPath, 'utf-8');
  const routes = JSON.parse(raw);

  const urls = routes.map(({ path, changefreq, priority }) => {
    const normalizedPath = path === '/' ? '' : path.replace(/^\//, '');
    const loc = `${baseUrl}/${normalizedPath}`.replace(/\/+$/, '/').replace(/([^:])\/\//g, '$1/');

    return `  <url>\n    <loc>${loc}</loc>\n    <lastmod>${today}</lastmod>\n    <changefreq>${changefreq}</changefreq>\n    <priority>${priority}</priority>\n  </url>`;
  }).join('\n');

  const xml = `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n${urls}\n</urlset>\n`;

  await fs.mkdir(publicPath, { recursive: true });
  await fs.writeFile(sitemapPath, xml, 'utf-8');
  console.log(`Sitemap generated with ${routes.length} entries at ${sitemapPath}`);
}

generate().catch((err) => {
  console.error('Failed to generate sitemap:', err);
  process.exitCode = 1;
});
