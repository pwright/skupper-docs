#!/usr/bin/env node
import { readdir, readFile, realpath, lstat, open } from 'node:fs/promises';
import { resolve, relative, dirname, extname, sep } from 'node:path';
import { parseArgs } from 'node:util';
import { analyzeMarkdown, renderReport } from './dita-analyzer.mjs';

const help = `Usage: node analyse/dita-report.mjs [options]
  --scan DIR          Markdown tree (default: input)
  --exclude-dir NAME  Extra directory name to prune, repeatable (refdog always excluded)
  --format FORMAT     markdown (default) or json
  --output, -o FILE    New report file outside the scanned tree (default: stdout)
  --help, -h          Show help
Hidden entries, node_modules, and symlinks are skipped. Source files are never written.
Existing output files are refused to avoid overwriting sources or earlier review results.
`;
const inside = (root, path) => {
  const rel = relative(root, path);
  return rel === '' || (rel !== '..' && !rel.startsWith(`..${sep}`) && !rel.startsWith(sep));
};

async function main() {
  const { values } = parseArgs({ options: {
    scan: { type: 'string', default: 'input' },
    'exclude-dir': { type: 'string', multiple: true, default: [] },
    format: { type: 'string', default: 'markdown' },
    output: { type: 'string', short: 'o', default: '-' },
    help: { type: 'boolean', short: 'h' },
  } });
  if (values.help) { process.stdout.write(help); return; }
  if (!['markdown', 'json'].includes(values.format)) throw new Error('--format must be markdown or json');
  const root = await realpath(resolve(values.scan));
  if (!(await lstat(root)).isDirectory()) throw new Error('--scan must be a directory');
  const files = [];
  const excluded = new Set(['node_modules', 'refdog', ...values['exclude-dir']]);
  async function discover(directory) {
    const entries = await readdir(directory, { withFileTypes: true });
    entries.sort((a, b) => a.name < b.name ? -1 : a.name > b.name ? 1 : 0);
    for (const entry of entries) {
      if (entry.name.startsWith('.') || entry.isSymbolicLink()) continue;
      const path = resolve(directory, entry.name);
      if (entry.isDirectory() && !excluded.has(entry.name)) await discover(path);
      else if (entry.isFile() && extname(entry.name).toLowerCase() === '.md') files.push(path);
    }
  }
  await discover(root);
  const documents = [];
  for (const file of files) {
    documents.push(analyzeMarkdown(await readFile(file, 'utf8'), relative(root, file).split(sep).join('/')));
  }
  const sections = documents.flatMap(doc => doc.sections);
  const model = {
    schemaVersion: '1.0', analyzer: 'remark-dita-heuristics-v1', root,
    summary: {
      files: documents.length, sections: sections.length,
      warnings: documents.reduce((count, doc) => count + doc.warnings.length, 0) +
        sections.reduce((count, section) => count + section.warnings.length, 0),
      topicTypes: Object.fromEntries(['task', 'reference', 'concept'].map(type => [type, documents.filter(doc => doc.topic.type === type).length])),
      classifications: Object.fromEntries(['prerequisites', 'procedure', 'result', 'example', 'reference', 'unknown']
        .map(type => [type, sections.filter(section => section.classification === type).length])),
    },
    documents,
  };
  const report = values.format === 'json' ? `${JSON.stringify(model, null, 2)}\n` : renderReport(model);
  if (values.output === '-') { process.stdout.write(report); return; }
  const output = resolve(values.output);
  const destination = resolve(await realpath(dirname(output)), output.split(sep).at(-1));
  if (inside(root, destination)) throw new Error('Output must be outside the scanned tree; source files are read-only');
  // Exclusive creation also refuses symlinks and hard links to existing source files.
  const stream = await open(destination, 'wx');
  try { await stream.writeFile(report); } finally { await stream.close(); }
}
main().catch(error => { process.stderr.write(`dita-report: ${error.message}\n`); process.exitCode = 1; });
