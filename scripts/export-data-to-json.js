const fs = require('fs');
const path = require('path');

const dataDir = path.join(__dirname, '..', 'data');
const outputDir = path.join(__dirname, '..', 'backend', 'data');

if (!fs.existsSync(outputDir)) {
  fs.mkdirSync(outputDir, { recursive: true });
}

const tintos = require(path.join(dataDir, 'tintos.ts').replace('.ts', '.js'));
const blancos = require(path.join(dataDir, 'blancos.ts').replace('.ts', '.js'));
const rosados = require(path.join(dataDir, 'rosados.ts').replace('.ts', '.js'));

const allWines = [
  ...tintos.tintos || [],
  ...blancos.blancos || [],
  ...rosados.rosados || []
];

fs.writeFileSync(
  path.join(outputDir, 'wines.json'),
  JSON.stringify(allWines, null, 2)
);

console.log(`Exported ${allWines.length} wines to backend/data/wines.json`);
