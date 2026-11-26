import QRCode from 'qrcode';
import catalog from '../mobile/assets/data/knowledge/catalog.json';
import sections from '../mobile/assets/data/knowledge/sections.json';
import { encodeKnowledgePatch, parseKnowledgePatch, qrBytes, QR_LIMIT } from '../mobile/src/core/knowledge/qrPatch';
import './style.css';

const $ = (id) => document.getElementById(id);
const form = $('editor');
const entry = $('entry');
const previous = new Map();
const lines = (value) => value.split(/\r?\n/).map((item) => item.trim()).filter(Boolean);
const read = (name) => form.elements.namedItem(name).value.trim();
const input = (name, value) => { form.elements.namedItem(name).value = value; };

function addOption(select, value, label) {
  const option = new Option(label, value);
  select.append(option);
}

function editable(item) {
  return item.kind !== 'emergency' && item.section !== 'health_safety';
}

for (const section of sections.filter(({ id }) => id !== 'health_safety')) {
  addOption($('section'), section.id, section.title);
}
for (const item of catalog.filter(editable)) {
  previous.set(item.id, item);
  addOption($('catalog'), item.id, item.label);
}

function clearQr() {
  $('output').hidden = true;
  $('placeholder').hidden = false;
  $('error').textContent = '';
}

function mode() {
  const removing = read('operation') === 'remove';
  entry.hidden = removing;
  entry.disabled = removing;
  $('section-field').hidden = removing;
  clearQr();
}

function fillExisting() {
  const item = previous.get($('existing').value.trim());
  if (!item) return;
  input('id', item.id);
  if (read('operation') === 'remove') return;
  input('section', item.section);
  input('title', item.label);
  input('answer', item.short);
  input('steps', item.steps.map((step) => Array.isArray(step) ? step.join(' ') : step).join('\n'));
  input('sources', item.sources.filter((source) => /^https:\/\//.test(source.url ?? '')).slice(0, 3)
    .map((source) => source.label + ' | ' + source.url).join('\n'));
  for (const name of ['questions', 'variants', 'more', 'why', 'related']) input(name, '');
}

form.addEventListener('input', clearQr);
form.addEventListener('change', (event) => {
  if (event.target.name === 'operation') {
    mode();
    fillExisting();
  }
});
$('existing').addEventListener('change', fillExisting);

function suggest() {
  const title = read('title');
  const answer = read('answer');
  if (!title) {
    $('error').textContent = 'Escribe un título para sugerir preguntas.';
    return;
  }
  if (!read('id')) {
    const slug = title.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '')
      .replace(/[^a-z0-9]+/g, '_').replace(/^_|_$/g, '');
    input('id', read('section') + '.' + slug.slice(0, 65));
  }
  if (!read('questions')) input('questions',
    ['¿Qué sabes sobre ' + title + '?', 'Háblame de ' + title, 'Información sobre ' + title].join('\n'));
  if (answer && answer.length <= 345 && !read('variants')) {
    input('variants', 'Sobre ' + title + ', esto es lo que indica la guía. ' + answer);
  }
  clearQr();
}
$('suggest').addEventListener('click', suggest);

let generation = 0;
let lastRevision = 0;
form.addEventListener('input', () => { generation++; });
form.addEventListener('submit', async (event) => {
  event.preventDefault();
  const request = ++generation;
  clearQr();
  try {
    const id = read('id');
    const original = catalog.find((item) => item.id === id);
    if (original && !editable(original)) throw new Error('Esta ficha de seguridad se actualiza con una versión de la app.');
    const revision = lastRevision = Math.max(Date.now(), lastRevision + 1);
    let patch = { op: 'remove', id, revision };
    if (read('operation') === 'put') {
      const sources = lines(read('sources')).map((line) => {
        const split = line.indexOf('|');
        if (split === -1) throw new Error('Escribe cada fuente como Nombre | URL HTTPS.');
        return { label: line.slice(0, split).trim(), url: line.slice(split + 1).trim() };
      });
      patch = { op: 'put', id, revision, entry: {
        section: read('section'), title: read('title'), answer: read('answer'),
        questions: lines(read('questions')), variants: lines(read('variants')),
        steps: lines(read('steps')), more: lines(read('more')), why: lines(read('why')),
        related: lines(read('related')), sources,
      } };
    }
    const payload = encodeKnowledgePatch(patch);
    const verified = parseKnowledgePatch(payload);
    const canvas = document.createElement('canvas');
    await QRCode.toCanvas(canvas, payload, { width: 560, margin: 4, errorCorrectionLevel: 'M' });
    if (request !== generation) return;
    $('qr').replaceWith(canvas);
    canvas.id = 'qr';
    canvas.setAttribute('aria-label', 'Código QR de actualización');
    $('payload').value = payload;
    $('download').href = canvas.toDataURL('image/png');
    $('download').download = id + '-' + verified.op + '.png';
    $('summary').textContent = (verified.op === 'remove' ? 'Retirar ' + id : verified.entry.title) +
      ' · ' + qrBytes(payload) + '/' + QR_LIMIT + ' bytes';
    $('placeholder').hidden = true;
    $('output').hidden = false;
  } catch (error) {
    if (request === generation) $('error').textContent = error.message;
  }
});

$('copy').addEventListener('click', async () => {
  const payload = $('payload');
  try { await navigator.clipboard.writeText(payload.value); }
  catch { payload.focus(); payload.select(); }
});

mode();

