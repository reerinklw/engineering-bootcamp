const esbuild = require('esbuild');
const path = require('path');

const appRoot = path.join(__dirname, '..');
const serverEntry = path.join(appRoot, 'server/index.ts');
const serverOut = path.join(appRoot, 'server/dist/index.js');

esbuild.buildSync({
  entryPoints: [serverEntry],
  outfile: serverOut,
  platform: 'node',
  format: 'cjs',
  packages: 'external',
});
