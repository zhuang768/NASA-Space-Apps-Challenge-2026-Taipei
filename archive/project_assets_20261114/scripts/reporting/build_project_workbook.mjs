/** Build one research workbook from the existing source-data bundle. No scientific scoring. */
import fs from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { createRequire } from 'node:module';
import { fileURLToPath } from 'node:url';
import { spawnSync } from 'node:child_process';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');
const OUT = path.join(ROOT, 'outputs/consolidated');
const inputPath = path.join(OUT, 'support/workbook_data.json');
const outputPath = path.join(OUT, 'NASA_Space_Apps_2026_All_Data.xlsx');
const runtimeModules = process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES
  || path.join(os.homedir(), '.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules');
const runtimeWorkspace = path.join(os.tmpdir(), 'nasa_workbook_runtime');
await fs.mkdir(runtimeWorkspace, { recursive: true });
try { await fs.symlink(runtimeModules, path.join(runtimeWorkspace, 'node_modules')); }
catch (error) { if (error.code !== 'EEXIST') throw error; }
const require = createRequire(path.join(runtimeWorkspace, 'package.json'));
const { Workbook, SpreadsheetFile } = require('@oai/artifact-tool');
const previewOnly = process.argv.includes('--overview-preview');
const plainPreview = process.argv.includes('--plain-english-preview');
const data = previewOnly || plainPreview ? null : JSON.parse(await fs.readFile(inputPath, 'utf8'));
const wb = Workbook.create();
const overview = wb.worksheets.add(plainPreview ? 'Overview' : '總覽');
const counts = [];
const navy = '#203864';
const light = '#EAF0F8';
const text = '#1F2937';

function colName(index) {
  let s = '';
  for (let n = index + 1; n; n = Math.floor((n - 1) / 26)) s = String.fromCharCode(65 + (n - 1) % 26) + s;
  return s;
}
function literal(value) {
  if (typeof value === 'string' && value.startsWith('=')) return `'${value}`;
  return value === undefined ? null : value;
}
function quoted(name) { return `'${name.replaceAll("'", "''")}'`; }
function formulaString(s) { return String(s).replaceAll('"', '""'); }
function heading(sheet, range) {
  const r = sheet.getRange(range);
  r.format = {
    fill: navy, font: { name: 'Arial', size: 11, bold: true, color: '#FFFFFF' },
    wrapText: true, verticalAlignment: 'center', horizontalAlignment: 'center',
    rowHeight: 46,
  };
}

if (plainPreview) {
  const samples = JSON.parse(await fs.readFile(path.join(OUT, 'review/plain_english/preview_samples.json'), 'utf8'));
  const previewDir = path.join(OUT, 'previews/plain_english');
  await fs.mkdir(previewDir, { recursive: true });
  for (const sample of samples.sheets) {
    const sheet = sample.name === 'Overview' ? overview : wb.worksheets.add(sample.name);
    const nr = sample.values.length, nc = sample.widths.length;
    sheet.showGridLines = true;
    const area = sheet.getRangeByIndexes(0, 0, nr, nc);
    area.setNumberFormat('@');
    area.values = sample.values.map((row, ri) => row.map((value, ci) =>
      sample.types[ri][ci] === 'date' && value ? new Date(value) : literal(value)));
    area.format = { fill: '#FFFFFF', font: { name: 'Arial', size: 11, color: '#000000' },
      verticalAlignment: 'center', wrapText: false };
    for (let ci = 0; ci < nc; ci++)
      sheet.getRangeByIndexes(0, ci, nr, 1).format.columnWidth = sample.widths[ci];
    for (let ri = 0; ri < nr; ri++) {
      sheet.getRangeByIndexes(ri, 0, 1, nc).format.rowHeight = sample.heights[ri];
      for (let ci = 0; ci < nc; ci++) {
        const cell = sheet.getCell(ri, ci);
        cell.setNumberFormat(sample.formats[ri][ci] || 'General');
        if (sample.bold[ri][ci]) cell.format.font = { name: 'Arial', size: 11, color: '#000000', bold: true };
        if (sample.wrap[ri][ci]) cell.format.wrapText = true;
      }
    }
    wb.recalculate();
    const blob = await wb.render({ sheetName: sample.name, range: `A1:${colName(nc - 1)}${nr}`, scale: 1, format: 'png' });
    await fs.writeFile(path.join(previewDir, `${sample.name}.png`), new Uint8Array(await blob.arrayBuffer()));
    console.log(`Rendered saved workbook sample: ${sample.name}`);
  }
  process.exit(0);
}

if (previewOnly) {
  // Values are read back from the completed XLSX, including its full raw-sheet count.
  const displayed = JSON.parse(await fs.readFile(path.join(OUT, 'review/final_overview_values.json'), 'utf8'));
  overview.showGridLines = false;
  overview.getRange('A1:D19').setNumberFormat('@');
  overview.getRange('A1:D19').values = displayed.values;
  overview.getRange('A1:D19').format.font = { name: 'Arial', size: 11, color: text };
  overview.getRange('A2').format.font = { name: 'Arial', size: 16, bold: true, color: navy };
  overview.getRange('A2').format.rowHeight = 28;
  for (const [letter, width] of [['A', 28], ['B', 25], ['C', 39], ['D', 95]])
    overview.getRange(`${letter}1:${letter}19`).format.columnWidth = width;
  heading(overview, 'A6:D6');
  heading(overview, 'A15:D15');
  overview.getRange('A7:D19').format.rowHeight = 29;
  overview.getRange('A6:D19').format.verticalAlignment = 'center';
  overview.getRange('D7:D19').format.wrapText = true;
  overview.getRange('B7:B12').setNumberFormat('#,##0');
  wb.recalculate();
  const blob = await wb.render({ sheetName: '總覽', range: 'A1:D19', scale: 1, format: 'png' });
  await fs.writeFile(path.join(OUT, 'previews/總覽.png'), new Uint8Array(await blob.arrayBuffer()));
  console.log('Rendered final overview from independently read XLSX values');
  process.exit(0);
}

// This is a file inventory, not an extraction of the large gridded products.
const imported = new Map(data.coverage.map(row => [row.path, row]));
const indexRows = [];
const skipDirs = new Set(['web', 'node_modules', '__pycache__', '.git', '.venv', '.wrangler']);
async function walk(directory) {
  for (const entry of await fs.readdir(directory, { withFileTypes: true })) {
    if (entry.name.startsWith('.') || skipDirs.has(entry.name)) continue;
    const full = path.join(directory, entry.name);
    const rel = path.relative(ROOT, full).split(path.sep).join('/');
    if (rel === 'outputs/consolidated') continue;
    if (entry.isDirectory()) { await walk(full); continue; }
    if (!entry.isFile() || /(?:token|secret|credential|password)/i.test(entry.name)) continue;
    const stat = await fs.stat(full);
    const ext = path.extname(entry.name).toLowerCase();
    const category = rel.startsWith('NASA_SpaceApps') ? '地球原始資料'
      : rel.startsWith('data/') ? '原始或處理後格網'
      : rel.startsWith('outputs/research/') ? '研究證據'
      : rel.startsWith('outputs/') ? '分析結果'
      : rel.startsWith('docs/') ? '說明與報告'
      : rel.startsWith('scripts/') || rel.startsWith('analog/') ? '程式'
      : rel.startsWith('tests/') ? '測試' : '專案設定';
    const source = imported.get(rel);
    indexRows.push([
      rel, category, ext, stat.size, stat.mtime.toISOString(),
      source ? `${source.sheet || ''} ${source.method || ''}`.trim() : '原檔索引',
      source?.rows ?? null, source?.sha256 ?? null,
      rel.startsWith('NASA_SpaceApps') ? 'docs/earth_inventory.csv'
        : rel.startsWith('data/raw/mars/') ? 'outputs/mars_profiles/profiles.json；同目錄 PDS 標籤'
        : null,
      '開啟原檔',
    ]);
  }
}
await walk(ROOT);
indexRows.sort((a, b) => a[0].localeCompare(b[0]));
data.tables.push({
  name: '檔案索引', title: '完整檔案索引', kind: 'data',
  note: '影像、網格及壓縮檔保留原檔；雜湊只列本輪實際讀取來源。網站、依賴與憑證排除。',
  columns: [
    { key: 'path', label: '專案相對路徑', type: 'text', width: 90 },
    { key: 'category', label: '分類', type: 'text', width: 20 },
    { key: 'extension', label: '格式', type: 'text', width: 12 },
    { key: 'bytes', label: '檔案大小 (bytes)', type: 'number', width: 22, format: '#,##0' },
    { key: 'modified', label: '檔案修改時間 (UTC)', type: 'date', width: 24 },
    { key: 'import', label: 'Excel 收錄方式', type: 'text', width: 50 },
    { key: 'rows', label: '來源列數', type: 'number', width: 15, format: '#,##0' },
    { key: 'sha256', label: '本輪來源 SHA-256', type: 'text', width: 68 },
    { key: 'metadata', label: '來源中繼資料位置', type: 'text', width: 65 },
    { key: 'open', label: '原始檔案', type: 'text', width: 16 },
  ], rows: indexRows,
});

const sourceRows = data.coverage.map(c => [c.path, c.rows, c.sheet, c.method, c.sha256]);
data.tables.push({
  name: '匯入對照', title: '來源與收錄位置', kind: 'data',
  note: '同一資料的交接或摘要視圖不算獨立觀測。純量封存與主題表可能重複，不能直接加總。',
  columns: [
    { key: 'path', label: '來源檔', type: 'text', width: 90 },
    { key: 'rows', label: '來源資料列或純量數', type: 'number', width: 22, format: '#,##0' },
    { key: 'sheet', label: 'Excel 工作表', type: 'text', width: 35 },
    { key: 'method', label: '收錄方式', type: 'text', width: 90 },
    { key: 'hash', label: '來源 SHA-256', type: 'text', width: 68 },
  ], rows: sourceRows,
});

for (const [index, table] of data.tables.entries()) {
  if (table.name.length > 31) throw new Error(`Worksheet name too long: ${table.name}`);
  const sheet = wb.worksheets.add(table.name);
  const ncol = table.columns.length;
  // The full raw sheet exceeded the author's 4 GB heap at XLSX serialization.
  // Author its layout and a bounded preview here; stream all raw values into
  // the same final XLSX after this workbook has been exported.
  const rowsToWrite = table.kind === 'raw' ? table.rows.slice(0, 7) : table.rows;
  sheet.showGridLines = false;
  sheet.freezePanes.freezeRows(1);
  sheet.freezePanes.freezeColumns(Math.min(2, ncol));
  sheet.getRangeByIndexes(0, 0, 1, ncol).values = [table.columns.map(c => c.label || c.key)];
  heading(sheet, `A1:${colName(ncol - 1)}1`);
  if (table.kind === 'raw') sheet.getRangeByIndexes(0, 0, 1, ncol).format.rowHeight = 92;
  // Set text storage BEFORE ingress: otherwise ISO strings can be coerced to dates
  // and lose their timezone/microsecond spelling. Formatting afterwards is too late.
  if (rowsToWrite.length) {
    for (const [i, column] of table.columns.entries()) {
      if (column.type === 'text')
        sheet.getRangeByIndexes(1, i, rowsToWrite.length, 1).setNumberFormat('@');
    }
  }

  for (let start = 0; start < rowsToWrite.length; start += 1500) {
    const batch = rowsToWrite.slice(start, start + 1500).map(row => row.map((v, i) =>
      table.columns[i]?.type === 'date' && v ? new Date(v) : literal(v)));
    if (batch.some(row => row.length !== ncol)) throw new Error(`Column count: ${table.name}`);
    sheet.getRangeByIndexes(start + 1, 0, batch.length, ncol).values = batch;
  }
  for (const [i, column] of table.columns.entries()) {
    const range = sheet.getRangeByIndexes(0, i, rowsToWrite.length + 1, 1);
    range.format.columnWidth = Math.min(column.width || 22, 110);
    if (rowsToWrite.length) {
      const body = sheet.getRangeByIndexes(1, i, rowsToWrite.length, 1);
      if (column.type === 'number') {
        if (table.kind !== 'raw') {
          body.format.horizontalAlignment = 'right';
          body.setNumberFormat(column.format || '0.000000');
        }
      } else if (column.type === 'date') body.setNumberFormat('yyyy-mm-dd hh:mm');
      if (table.rows.length < 1000 && /status|novelty|狀態/.test(column.key)) {
        for (const term of ['unchecked', 'unknown', 'not_checked', '待確認', '未查'])
          body.conditionalFormats.add('containsText', { text: term, format: { fill: '#FFF2CC' } });
      }
    }
  }
  if (table.rows.length && table.kind !== 'raw') {
    const area = sheet.getRangeByIndexes(1, 0, table.rows.length, ncol);
    area.format.font = { name: 'Arial', size: 11, color: text };
    area.format.verticalAlignment = 'center';
    area.format.rowHeight = table.kind === 'archive' ? 35 : 24;
    if (table.rows.length <= 1500 || table.kind === 'archive') {
      for (const [i, column] of table.columns.entries()) {
        if (column.type === 'text')
          sheet.getRangeByIndexes(1, i, table.rows.length, 1).format.wrapText = true;
      }
      for (const [i, row] of table.rows.entries()) {
        let lines = 1;
        for (let j = 0; j < row.length; j++) {
          if (typeof row[j] !== 'string') continue;
          const width = Math.min(table.columns[j].width || 22, 110) - 2;
          const count = row[j].split('\n').reduce((n, part) => n + Math.max(1,
            Math.ceil([...part].reduce((sum, ch) => sum + (ch.codePointAt(0) > 255 ? 2 : 1), 0) / width)), 0);
          lines = Math.max(lines, count);
        }
        if (lines > 1) sheet.getRangeByIndexes(i + 1, 0, 1, ncol).format.rowHeight = Math.min(390, lines * 15 + 6);
      }
    }
  }
  // One header row and a single Excel Table make every source filterable.
  if (table.rows.length) {
    const excelTable = sheet.tables.add(`A1:${colName(ncol - 1)}${rowsToWrite.length + 1}`, true, `Data${index + 1}`);
    excelTable.showFilterButton = true;
  }
  if (table.name === '檔案索引') {
    const formulas = table.rows.map(row => [`=HYPERLINK("../../${formulaString(row[0])}","開啟原檔")`]);
    sheet.getRange(`J2:J${formulas.length + 1}`).formulas = formulas;
  }
  counts.push({ name: table.name, rows: table.rows.length, columns: ncol, kind: table.kind,
                title: table.title, note: table.note });
  console.log(`Loaded ${table.name}: ${table.rows.length} rows, ${ncol} columns`
    + (table.kind === 'raw' ? ' (full data queued for streaming export)' : ''));
}

overview.showGridLines = false;
overview.tabColor = navy;
overview.getRange('A1:F45').format.font = { name: 'Arial', size: 11, color: text };
overview.getRange('A2').values = [['NASA Space Apps 2026 資料總表']];
overview.getRange('A2').format.font = { name: 'Arial', size: 16, bold: true, color: navy };
overview.getRange('A3').values = [['Team zasa']];
overview.getRange('A4').values = [[`資料快照：${data.generated_taipei}（Asia/Taipei）`]];
overview.getRange('A6:D6').values = [['資料分類', '數量', '計數單位', '閱讀重點']];
heading(overview, 'A6:D6');
const find = fragment => counts.find(c => c.name.includes(fragment));
const mainRows = [
  ['火星發現候選', find('火星發現'), '點', '原始順序與分數保留，未重新評分'],
  ['火星新穎性查核', find('新穎性'), '點', '已初查不等於已證明全新場址'],
  ['地球視窗', find('視窗') || find('地形'), '個版本視窗', '兩版皆為 100 km 視窗，採樣不同'],
  ['地球候選', find('地球候選'), '筆版本候選', '以 run_id 加 candidate_id 區分'],
  ['原始 MEDA', counts.find(c => c.kind === 'raw'), '筆原始紀錄', '保留所有品質旗標與不確定度'],
  ['JSON 原值', find('JSON'), '個純量或空結構', '完整封存，包含重複交接視圖'],
];
for (const [i, row] of mainRows.entries()) {
  const r = 7 + i;
  overview.getRange(`A${r}:D${r}`).values = [[row[0], null, row[2], row[3]]];
  if (row[1]) overview.getRange(`B${r}`).formulas = [[`=COUNTA(${quoted(row[1].name)}!A2:A${row[1].rows + 1})`]];
  else overview.getRange(`B${r}`).values = [['見分頁']];
}
overview.getRange('B7:B12').setNumberFormat('#,##0');
overview.getRange('A15:D15').values = [['主題', '目前狀態', '用途', '待完成事項']];
heading(overview, 'A15:D15');
overview.getRange('A16:D19').values = [
  ['淺層冰', '2 點條件式保留', '冰資源探查研究', '確切同用途提案、獨立冰證據'],
  ['大氣與塵埃', '2 點背景參照', '塵埃柱量與低起伏地形比較', '局部風、沉降、事件與地球配對'],
  ['地表承載', '用途主張暫停', '熱性質資料仍保留', '缺承載、強度與通行性測量'],
  ['跨天體配對', '既有地形初篩', '四主題資料分開呈現', '新四點地球配對與可比溫度資料'],
];
overview.getRange('A22:D22').values = [['工作表', '資料列數', '內容', '定義或限制']];
heading(overview, 'A22:D22');
for (const [i, c] of counts.entries()) {
  const row = i + 23;
  overview.getRange(`A${row}:D${row}`).values = [[c.name, c.rows, c.title || c.name, c.note || '']];
  overview.getRange(`A${row}`).formulas = [[`=HYPERLINK("#${quoted(c.name)}!A1","${formulaString(c.name)}")`]];
}
const last = counts.length + 22;
overview.getRange(`A6:D${last}`).format.verticalAlignment = 'center';
overview.getRange(`A7:D${last}`).format.rowHeight = 29;
overview.getRange(`D7:D${last}`).format.wrapText = true;
overview.getRange(`A23:D${last}`).format.rowHeight = 62;
overview.getRange(`B23:B${last}`).setNumberFormat('#,##0');
for (const [letter, width] of [['A', 28], ['B', 25], ['C', 39], ['D', 95]])
  overview.getRange(`${letter}1:${letter}${last}`).format.columnWidth = width;
overview.getRange('A2').format.rowHeight = 28;

await fs.mkdir(path.join(OUT, 'review'), { recursive: true });
await fs.mkdir(path.join(OUT, 'previews'), { recursive: true });
wb.recalculate();
const inspection = await wb.inspect({ kind: 'table', range: '總覽!A6:D12', include: 'values,formulas',
  tableMaxRows: 8, tableMaxCols: 4, maxChars: 5000 });
await fs.writeFile(path.join(OUT, 'review/overview_base_inspection.ndjson'), inspection.ndjson);
console.log(inspection.ndjson);
const errors = await wb.inspect({ kind: 'match', range: '總覽!A1:D80',
  searchTerm: '#REF!|#DIV/0!|#VALUE!|#NAME\\?|#NUM!|#NULL!|#SPILL!|#CALC!',
  options: { useRegex: true, maxResults: 30 }, summary: 'Summary formula errors' });
await fs.writeFile(path.join(OUT, 'review/formula_scan.ndjson'), errors.ndjson);

// Each created sheet gets a bounded, readable preview. No whole-raw-table rendering.
for (const item of [{ name: '總覽', columns: 4 }, ...counts]) {
  const end = colName(Math.min(item.columns, 8) - 1);
  const endRow = item.name === '總覽' ? 19 : Math.min(item.rows + 1, item.kind === 'archive' ? 5 : 8);
  const blob = await wb.render({ sheetName: item.name, range: `A1:${end}${endRow}`, scale: 1, format: 'png' });
  await fs.writeFile(path.join(OUT, 'previews', `${item.name}.png`), new Uint8Array(await blob.arrayBuffer()));
  console.log(`Rendered ${item.name}`);
}
const output = await SpreadsheetFile.exportXlsx(wb);
const basePath = path.join(OUT, 'support/workbook_base.xlsx');
await output.save(basePath);
await fs.writeFile(path.join(OUT, 'review/layout_manifest.json'), JSON.stringify({
  generated_taipei: data.generated_taipei, sheets: [{ name: '總覽', rows: last }, ...counts],
  source_file_count: new Set(data.coverage.map(c => c.path)).size,
  coverage_entry_count: data.coverage.length,
  raw_preview_only_in_base: true, final_output_requires_streaming: true,
}, null, 2) + '\n');
console.log(`BASE_READY ${basePath}`);
const primaryPython = process.env.CODEX_PRIMARY_RUNTIME_PYTHON
  || path.join(os.homedir(), '.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3');
const streamed = spawnSync(primaryPython, [
  path.join(ROOT, 'scripts/reporting/stream_raw_sheet.py'), '--base', basePath,
  '--bundle', inputPath, '--output', outputPath,
], { cwd: ROOT, encoding: 'utf8', maxBuffer: 1024 * 1024 });
if (streamed.stdout) console.log(streamed.stdout);
if (streamed.status !== 0) throw new Error(streamed.stderr || `Streaming export failed: ${streamed.status}`);
const st = await fs.stat(outputPath);
await fs.writeFile(path.join(OUT, 'review/workbook_manifest.json'), JSON.stringify({
  generated_taipei: data.generated_taipei, output_path: path.relative(ROOT, outputPath),
  file_bytes: st.size, sheets: [{ name: '總覽', rows: last }, ...counts],
  source_file_count: new Set(data.coverage.map(c => c.path)).size,
  coverage_entry_count: data.coverage.length, original_scientific_scores_changed: false,
  original_raw_data_moved: false,
}, null, 2) + '\n');
console.log(`SAVED ${outputPath} (${st.size} bytes)`);
