import { unified } from 'unified';
import remarkParse from 'remark-parse';
import remarkGfm from 'remark-gfm';
import remarkFrontmatter from 'remark-frontmatter';

const parser = unified().use(remarkParse).use(remarkGfm).use(remarkFrontmatter);
const rules = [
  ['prerequisites', /^(prerequisites?|requirements?|before you begin)$/i],
  ['procedure', /^(procedure|steps?|instructions?|how to\b.*)$/i],
  ['result', /^(results?|verification|verify\b.*|expected (results?|output))$/i],
  ['example', /^(examples?|sample(s|\b.*)|example output)$/i],
  ['reference', /^(reference|additional resources|related (links|information)|.*\b(properties|parameters|options|attributes|syntax))$/i],
];
const textOf = node => node.value ?? (node.children ?? []).map(textOf).join('');
const labelOf = node => textOf(node).trim().replace(/:$/, '');
const categoryOf = label => rules.find(([, pattern]) => pattern.test(label))?.[0];
const location = node => ({ startLine: node.position.start.line, endLine: node.position.end.line });
const warning = (code, message, source) => ({ code, message, source });
function walk(node, fn) {
  fn(node);
  for (const child of node.children ?? []) walk(child, fn);
}

/** Parse and classify one document. Pure: no filesystem access or source mutations. */
export function analyzeMarkdown(markdown, path = 'document.md') {
  const tree = parser.parse(markdown);
  const sections = [];
  const stack = [];
  const preamble = { id: 's1', parentId: null, title: '(preamble)', level: 0, kind: 'preamble', nodes: [] };
  sections.push(preamble);
  let current = preamble;
  let title;
  let hasFrontmatter = false;
  for (const node of tree.children) {
    if (node.type === 'yaml') { hasFrontmatter = true; continue; }
    const label = labelOf(node);
    const boldLabel = node.type === 'paragraph' && node.children.length === 1 &&
      node.children[0].type === 'strong' && categoryOf(label);
    if (node.type === 'heading' || boldLabel) {
      const level = boldLabel ? (stack.at(-1)?.level ?? 0) + 1 : node.depth;
      if (!boldLabel) {
        while (stack.length && stack.at(-1).level >= level) stack.pop();
      }
      current = {
        id: `s${sections.length + 1}`, parentId: stack.at(-1)?.id ?? null,
        title: label, level, kind: boldLabel ? 'bold-label' : 'heading', nodes: [node],
      };
      sections.push(current);
      if (!boldLabel) stack.push(current);
      if (node.type === 'heading' && node.depth === 1 && !title) title = label;
    } else {
      current.nodes.push(node);
    }
  }

  const classified = sections.filter(section => section.nodes.length).map(section => {
    const { nodes, ...identity } = section;
    const content = nodes.filter(node => node.type !== 'heading' &&
      !(section.kind === 'bold-label' && node === nodes[0]));
    const source = { startLine: nodes[0].position.start.line, endLine: nodes.at(-1).position.end.line };
    const markers = content.filter(node => node.type === 'html').map(node => node.value).join('\n');
    const explicit = categoryOf(section.title);
    const ordered = content.filter(node => node.type === 'list' && node.ordered);
    let classification = 'unknown';
    let confidence = 0.2;
    const evidence = [];
    const warnings = [];
    if (explicit) {
      classification = explicit; confidence = 0.95;
      evidence.push(`Explicit ${section.kind} label: ${section.title}`);
    } else if (/<!--\s*PROCEDURE\s*-->/i.test(markers)) {
      classification = 'procedure'; confidence = 0.9;
      evidence.push('PROCEDURE comment marker');
    } else if (/<!--\s*REFERENCE\s*-->/i.test(markers)) {
      classification = 'reference'; confidence = 0.9;
      evidence.push('REFERENCE comment marker');
    } else if (ordered.length) {
      classification = 'procedure'; confidence = 0.6;
      evidence.push('Top-level ordered list; sequence may not be instructions');
    } else if (content.some(node => node.type === 'table')) {
      classification = 'reference'; confidence = 0.55;
      evidence.push('GFM table; tabular content may have another purpose');
    }
    if (classification === 'unknown') warnings.push(warning('UNKNOWN_SECTION', 'No reliable semantic signal; review manually.', source));
    const html = content.filter(node => node.type === 'html' &&
      !/^\s*(?:<!--[\s\S]*?-->\s*|<a\s+id=[^>]*>\s*<\/a>\s*)+$/.test(node.value));
    for (const node of html) warnings.push(warning('RAW_HTML', 'Raw HTML is preserved but its internal structure is not classified.', location(node)));
    for (const node of content) {
      if (node.type === 'code') continue;
      const raw = markdown.slice(node.position.start.offset, node.position.end.offset);
      if (/\{[{%]|!INCLUDE|^\s*!!!/m.test(raw)) warnings.push(warning('EXTENDED_MARKDOWN', 'Template, include, or admonition syntax needs review.', location(node)));
    }
    if (classification === 'procedure' && !ordered.length) {
      warnings.push(warning('NO_ORDERED_STEPS', 'Procedure has no direct ordered list; consider steps-informal or a separate task.', source));
    }
    return {
      ...identity, source, classification, confidence, evidence, warnings,
      // Full positioned mdast blocks and original slices preserve material for review and a future writer.
      blocks: nodes.map(node => ({ type: node.type, source: location(node),
        markdown: markdown.slice(node.position.start.offset, node.position.end.offset), ast: node })),
    };
  });

  const warnings = [];
  const allHtml = [];
  walk(tree, node => { if (node.type === 'html') allHtml.push(node.value); });
  if (allHtml.some(value => /<!--\s*ASSEMBLY\s*-->/i.test(value))) {
    warnings.push(warning('ASSEMBLY', 'Assembly marker: this file may need multiple DITA topics and a map.', location(tree)));
  }
  const procedures = classified.filter(section => section.classification === 'procedure');
  const references = classified.filter(section => section.classification === 'reference');
  const conceptMarker = allHtml.some(value => /<!--\s*CONCEPT\s*-->/i.test(value));
  const type = procedures.length ? 'task' : references.length ? 'reference' : 'concept';
  const confidence = procedures.length ? Math.max(...procedures.map(s => s.confidence)) :
    references.length ? Math.max(...references.map(s => s.confidence)) : conceptMarker ? 0.9 : 0.4;
  const evidence = procedures.length ? ['Procedure sections found'] : references.length ? ['Reference sections found'] :
    conceptMarker ? ['CONCEPT comment marker'] : ['Fallback: no task or reference evidence'];
  if (confidence < 0.5) warnings.push(warning('LOW_TOPIC_CONFIDENCE', 'Concept is a tentative fallback; review the topic type.', location(tree)));
  if (procedures.length && references.length) warnings.push(warning('MIXED_TOPIC', 'Procedure and reference sections coexist; review topic splitting.', location(tree)));
  const procedureGroups = procedures.filter(section => !procedures.some(other => other.id === section.parentId));
  if (procedureGroups.length > 1) warnings.push(warning('MULTIPLE_PROCEDURES', 'Multiple procedure groups may require separate task topics.', location(tree)));
  for (const section of classified) {
    const parent = procedures.find(parent => parent.id === section.parentId);
    if (section.classification === 'procedure' && parent) {
      section.warnings.push(warning('NESTED_PROCEDURE',
        `Procedure is nested under another procedure at L${parent.source.startLine}; review for an authoring mistake or intentional grouping.`, section.source));
    }
    section.ditaElements = inferElements(section, type);
  }
  return {
    path, title: title ?? path, source: location(tree), hasFrontmatter,
    frontmatter: tree.children.filter(node => node.type === 'yaml').map(node => ({
      source: location(node), markdown: markdown.slice(node.position.start.offset, node.position.end.offset), ast: node,
    })),
    topic: { type, confidence, evidence, elements: [type, 'title', { task: 'taskbody', reference: 'refbody', concept: 'conbody' }[type]] },
    warnings, sections: classified,
  };
}

function inferElements(section, topicType) {
  const category = section.classification;
  const container = category === 'prerequisites' && topicType === 'task' ? 'prereq' :
    category === 'result' && topicType === 'task' ? 'result' : category === 'example' ? 'example' :
      category === 'procedure' ? null : 'section';
  const elements = container ? [{ name: container, source: section.source }] : [];
  for (const block of section.blocks) {
    const node = block.ast;
    if (node.type === 'list') {
      const steps = category === 'procedure' && node.ordered;
      elements.push({ name: steps ? 'steps' : node.ordered ? 'ol' : 'ul', source: block.source });
      if (steps) for (const item of node.children) {
        elements.push({ name: 'step', source: location(item) });
        const first = item.children[0];
        if (first?.type === 'paragraph') elements.push({ name: 'cmd', source: location(first) });
        if (item.children.length > 1) elements.push({ name: 'info', source: {
          startLine: item.children[1].position.start.line, endLine: item.position.end.line,
        } });
      }
    }
    walk(node, child => {
      const name = { code: 'codeblock', table: 'table', blockquote: 'note' }[child.type];
      if (name) elements.push({ name, source: location(child) });
    });
  }
  if (category === 'procedure' && !elements.some(element => element.name === 'steps')) {
    elements.unshift({ name: 'steps-informal', source: section.source });
  }
  return elements;
}

const cell = value => String(value).replace(/\|/g, '\\|').replace(/[\r\n]/g, ' ');
export function renderReport(model) {
  const lines = ['# DITA classification review', '',
    'Read-only heuristic analysis. Confidence is a rule weight, not a calibrated probability. Element names are candidates, not validated DITA.', '',
    `${model.documents.length} files; ${model.summary.sections} sections; ${model.summary.warnings} warnings.`, ''];
  for (const document of model.documents) {
    lines.push(`## ${cell(document.path)}`, '', `Title: ${cell(document.title)}`, '',
      `Inferred topic: **${document.topic.type}** (${document.topic.confidence.toFixed(2)}). ${document.topic.evidence.join('; ')}.`, '',
      `Topic elements: ${document.topic.elements.map(name => `\`${name}\``).join(', ')}.`, '',
      '| Lines | Section | Classification | Confidence | Candidate elements | Evidence / warnings |',
      '| --- | --- | --- | --- | --- | --- |');
    for (const section of document.sections) {
      const elements = [...new Set(section.ditaElements.map(element => element.name))].join(', ');
      const notes = [...section.evidence, ...section.warnings.map(w => `${w.code} (L${w.source.startLine}): ${w.message}`)].join('; ');
      lines.push(`| ${section.source.startLine}–${section.source.endLine} | ${cell(section.title)} | ${section.classification} | ${section.confidence.toFixed(2)} | ${elements} | ${cell(notes)} |`);
    }
    lines.push('');
    for (const item of document.warnings) lines.push(`- ${item.code} (L${item.source.startLine}): ${item.message}`);
    lines.push('');
  }
  return lines.join('\n');
}
