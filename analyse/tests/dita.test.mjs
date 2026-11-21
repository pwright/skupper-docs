import test from 'node:test';
import assert from 'node:assert/strict';
import { mkdtemp, mkdir, writeFile, readFile, symlink, rm } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { resolve, join } from 'node:path';
import { spawnSync } from 'node:child_process';
import { analyzeMarkdown, renderReport } from '../dita-analyzer.mjs';

const cli = resolve(import.meta.dirname, '../dita-report.mjs');
test('real procedure: frontmatter, bold labels, nested lists and original line positions', () => {
  const markdown = '---\ntype: module\n---\n# Link sites\n<!--PROCEDURE-->\n\n**Prerequisites**\n\n* Two sites\n\n**Procedure**\n\n1. Create a token.\n   ```sh\n   skupper token issue\n   ```\n   * Keep it safe.\n2. Redeem it.\n\n**Results**\n\nSites are linked.\n';
  const doc = analyzeMarkdown(markdown, 'link.md');
  assert.equal(doc.title, 'Link sites');
  assert.equal(doc.topic.type, 'task');
  assert.equal(doc.hasFrontmatter, true);
  const prereq = doc.sections.find(s => s.classification === 'prerequisites');
  assert.deepEqual(prereq.source, { startLine: 7, endLine: 9 });
  assert.equal(prereq.ditaElements[0].name, 'prereq');
  const steps = doc.sections.find(s => s.title === 'Procedure');
  assert.equal(steps.ditaElements.filter(e => e.name === 'step').length, 2);
  assert.equal(steps.ditaElements.filter(e => e.name === 'cmd').length, 2);
  assert.ok(steps.ditaElements.some(e => e.name === 'codeblock'));
  assert.equal(steps.blocks[1].markdown, markdown.slice(steps.blocks[1].ast.position.start.offset, steps.blocks[1].ast.position.end.offset));
  assert.equal(doc.sections.find(s => s.classification === 'result').ditaElements[0].name, 'result');
});

test('nested procedures stay ambiguous and retain missing-steps warnings', () => {
  for (const label of ['**Procedure**', '## Procedure']) {
    const doc = analyzeMarkdown(`# Install\n<!--PROCEDURE-->\n\nIntroduction.\n\n${label}\n\n1. Run it.\n`);
    const outer = doc.sections.find(s => s.title === 'Install');
    const inner = doc.sections.find(s => s.title === 'Procedure');
    assert.ok(outer.warnings.some(w => w.code === 'NO_ORDERED_STEPS'));
    assert.ok(!outer.ditaElements.some(e => e.name === 'context'));
    const nested = inner.warnings.find(w => w.code === 'NESTED_PROCEDURE');
    assert.ok(nested);
    assert.deepEqual(nested.source, inner.source);
    assert.match(nested.message, /L1/);
    assert.ok(!inner.warnings.some(w => w.code === 'NO_ORDERED_STEPS'));
    assert.match(renderReport({ documents: [doc], summary: { sections: 2, warnings: 2 } }), /NESTED_PROCEDURE/);
  }
  const siblings = analyzeMarkdown('# Guide\n\n## Procedure\n\n1. First.\n\n## Steps\n\n1. Second.\n');
  assert.ok(!siblings.sections.some(s => s.warnings.some(w => w.code === 'NESTED_PROCEDURE')));
});

test('GFM table, examples and opaque raw HTML remain reviewable', () => {
  const doc = analyzeMarkdown('# Site resource\n\n## Examples\n\n```yaml\nkind: Site\n```\n\n## Properties\n\n| Name | Type |\n| --- | --- |\n| name | string |\n\n<div>opaque</div>\n');
  assert.equal(doc.topic.type, 'reference');
  assert.equal(doc.sections.find(s => s.title === 'Examples').classification, 'example');
  const props = doc.sections.find(s => s.title === 'Properties');
  assert.ok(props.ditaElements.some(e => e.name === 'table'));
  assert.ok(props.warnings.some(w => w.code === 'RAW_HTML'));
});

test('unknown prose, unordered lists, and code containing headings do not imply tasks', () => {
  const doc = analyzeMarkdown('# Overview\n\nA network connects sites.\n\n* East\n* West\n\n```md\n## Procedure\n1. Fake step\n```\n');
  assert.equal(doc.topic.type, 'concept');
  assert.equal(doc.sections.length, 1);
  assert.equal(doc.sections[0].classification, 'unknown');
  assert.ok(doc.warnings.some(w => w.code === 'LOW_TOPIC_CONFIDENCE'));
  assert.equal(analyzeMarkdown('').sections.length, 0);
});

test('assemblies and informal tasks are flagged instead of claiming valid DITA', () => {
  const doc = analyzeMarkdown('# Guide\n<!--ASSEMBLY-->\n\n## First\n<!--PROCEDURE-->\n\nRun the tool.\n\n## Second\n<!--PROCEDURE-->\n\nRun another tool.\n\n## Reference\nDetails.\n');
  assert.ok(doc.warnings.some(w => w.code === 'ASSEMBLY'));
  assert.ok(doc.warnings.some(w => w.code === 'MULTIPLE_PROCEDURES'));
  assert.ok(doc.warnings.some(w => w.code === 'MIXED_TOPIC'));
  assert.ok(doc.sections.some(s => s.warnings.some(w => w.code === 'NO_ORDERED_STEPS')));
  assert.match(renderReport({ documents: [doc], summary: { sections: 4, warnings: 5 } }), /steps-informal/);
});

test('CLI scans deterministically, prunes directories and symlinks, and never overwrites sources', async () => {
  const temp = await mkdtemp(join(tmpdir(), 'dita-analysis-'));
  try {
    const root = join(temp, 'docs');
    await mkdir(root);
    await mkdir(join(root, 'archive'));
    await mkdir(join(root, 'refdog'));
    await writeFile(join(root, 'a.md'), '# A\n\n**Procedure**\n\n1. Run it.\n');
    await writeFile(join(root, 'archive/b.md'), '# Old');
    await writeFile(join(root, 'refdog/generated.md'), '# Generated');
    await symlink(join(root, 'a.md'), join(root, 'alias.md'));
    const before = await readFile(join(root, 'a.md'));
    const run = (...args) => spawnSync(process.execPath, [cli, '--scan', root, '--exclude-dir', 'archive', ...args], { encoding: 'utf8' });
    const first = run('--format', 'json');
    assert.ifError(first.error);
    assert.equal(first.status, 0, first.stderr);
    assert.equal(first.stdout, run('--format', 'json').stdout);
    const model = JSON.parse(first.stdout);
    assert.equal(model.summary.files, 1);
    assert.equal(model.documents[0].path, 'a.md');
    assert.equal(run('-o', join(root, 'a.md')).status, 1);
    assert.equal(run('-o', join(root, 'new.json')).status, 1);
    const out = join(temp, 'report.md');
    assert.equal(run('-o', out).status, 0);
    assert.match(await readFile(out, 'utf8'), /DITA classification review/);
    assert.equal(run('-o', out).status, 1);
    assert.equal(run('--format', 'xml').status, 1);
    assert.deepEqual(await readFile(join(root, 'a.md')), before);
  } finally { await rm(temp, { recursive: true, force: true }); }
});
