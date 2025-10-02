const fs = require('fs');
const path = require('path');
const vm = require('vm');

const ROOT = path.resolve(__dirname, '..');
const DATA_DIR = path.join(ROOT, 'website', 'src', 'data');

function parseTsArray(file) {
  let code = fs.readFileSync(file, 'utf-8');
  // Remove import lines
  code = code.replace(/^\s*import[^\n]*$/gm, '');
  // Strip block comments
  code = code.replace(/\/\*[\s\S]*?\*\//g, '');
  // Replace export const ... = with module.exports =
  code = code.replace(/export\s+const\s+\w+\s*:\s*[^=]+=/, 'module.exports =');
  code = code.replace(/export\s+const\s+\w+\s*=\s*/, 'module.exports = ');

  const sandbox = { module: { exports: null }, exports: {} };
  vm.createContext(sandbox);
  try {
    vm.runInContext(code, sandbox, { timeout: 1000, filename: path.basename(file) });
  } catch (e) {
    throw new Error(`Failed to evaluate ${file}: ${e.message}`);
  }
  if (!Array.isArray(sandbox.module.exports)) {
    throw new Error(`No array exported from ${file}`);
  }
  return sandbox.module.exports;
}

function normalizeItem(item) {
  return {
    id: String(item.id),
    name: item.name || '',
    color: item.color,
    grape: item.grape || '',
    origin: item.origin || null,
    short_description: item.shortDescription || null,
    long_description: item.longDescription || null,
    image: item.image || null,
    characteristics: item.characteristics || null,
    available: item.available !== false,
    prices: item.prices || {},
  };
}

function main() {
  const files = ['tintos.ts', 'blancos.ts', 'rosados.ts'];
  let all = [];
  for (const f of files) {
    const p = path.join(DATA_DIR, f);
    if (!fs.existsSync(p)) continue;
    const arr = parseTsArray(p);
    all = all.concat(arr.map(normalizeItem));
  }
  const outPath = path.join(__dirname, 'wines_from_ts.json');
  fs.writeFileSync(outPath, JSON.stringify(all, null, 2), 'utf-8');
  console.log(`Wrote ${all.length} wines to ${outPath}`);
}

main();
