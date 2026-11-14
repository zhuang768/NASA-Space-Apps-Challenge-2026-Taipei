/** Artifact Tool authoring for the final current-research worksheets only. */
import fs from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { createRequire } from 'node:module';
import { fileURLToPath } from 'node:url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');
const OUT = path.join(ROOT, 'outputs/consolidated');
const runtime = process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES || path.join(os.homedir(), '.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules');
const workspace = path.join(os.tmpdir(), 'nasa_final_workbook_runtime');
await fs.mkdir(workspace, { recursive: true });
try { await fs.symlink(runtime, path.join(workspace, 'node_modules')); }
catch (error) { if (error.code !== 'EEXIST') throw error; }
const require = createRequire(path.join(workspace, 'package.json'));
const { Workbook, SpreadsheetFile } = require('@oai/artifact-tool');
const data = JSON.parse(await fs.readFile(path.join(OUT, 'support/main_v3_data.json'), 'utf8'));
const wb = Workbook.create();
for (const tab of data.tables) wb.worksheets.add(tab.name);
const previews = path.join(OUT, 'previews/main_v3');
await fs.mkdir(previews, { recursive: true });
const font = { name: 'Arial', size: 11, color: '#000000' };
function colName(index) {
  let result = '';
  for (let value = index + 1; value; value = Math.floor((value - 1) / 26)) result = String.fromCharCode(65 + (value - 1) % 26) + result;
  return result;
}
function literal(value) { return typeof value === 'string' && value.startsWith('=') ? `'${value}` : value; }
for (const [i, tab] of data.tables.entries()) {
  const sheet = wb.worksheets.getItem(tab.name);
  const nr = tab.rows.length + 1, nc = tab.headers.length;
  const area = sheet.getRangeByIndexes(0, 0, nr, nc);
  // Critical: apply literal-text formatting before values to avoid automatic
  // conversion of publisher clocks / ISO strings into Excel date serials.
  area.setNumberFormat('@');
  area.format = { fill: '#FFFFFF', font, wrapText: false, verticalAlignment: 'center', rowHeight: 20 };
  area.values = [tab.headers, ...tab.rows].map(row => row.map(literal));
  for (let ci = 0; ci < nc; ci++) {
    const column = sheet.getRangeByIndexes(0, ci, nr, 1);
    column.format.columnWidth = tab.widths[ci];
    const populated = tab.rows.map(row => row[ci]).filter(v => v !== null);
    if (populated.length && populated.every(v => typeof v === 'number')) {
      const format = populated.every(v => Number.isInteger(v)) ? '0' : '0.000000';
      sheet.getRangeByIndexes(1, ci, nr - 1, 1).setNumberFormat(format);
      sheet.getRangeByIndexes(1, ci, nr - 1, 1).format.horizontalAlignment = 'right';
    } else if (populated.some(v => typeof v === 'number')) {
      // Small vertical research-card and QA summaries have mixed value columns.
      for (let ri = 0; ri < tab.rows.length; ri++) {
        if (typeof tab.rows[ri][ci] === 'number') sheet.getCell(ri + 1, ci).setNumberFormat(Number.isInteger(tab.rows[ri][ci]) ? '0' : '0.000000');
      }
    }
  }
  sheet.getRangeByIndexes(0, 0, 1, nc).format = { fill: '#FFFFFF', font: { ...font, bold: true }, wrapText: true, rowHeight: 48, horizontalAlignment: 'center', verticalAlignment: 'center', borders: { bottom: { style: 'thin', color: '#000000' } } };
  sheet.showGridLines = true;
  sheet.freezePanes.freezeRows(1);
  sheet.freezePanes.freezeColumns(tab.name === 'EH Records' ? 5 : 1);
  if (tab.name !== 'Overview' && tab.name !== 'EH Summary') {
    const native = sheet.tables.add(`A1:${colName(nc-1)}${nr}`, true, `MRv3Table${i+1}`);
    native.style = 'TableStyleLight1';
    native.showBandedColumns = false;
  }
  console.log(`Authored ${tab.name}: ${nr} rows x ${nc} columns`);
}
const overview = wb.worksheets.getItem('Overview');
overview.getRange('B13').setNumberFormat('0');
overview.getRange('B13').formulas = [[`=COUNTA('EH Records'!A2:A${data.tables.find(t=>t.name==='EH Records').rows.length+1})`]];
const summary = wb.worksheets.getItem('EH Summary');
for (const [address, filename] of [['B8', 'summer_temperatures.png'], ['B9', 'summer_temperature_difference.png']]) {
  const file = `outputs/research/elephant_head_final/${filename}`;
  summary.getRange(address).formulas = [[`=HYPERLINK("https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei/blob/main/${file}","${file}")`]];
  summary.getRange(address).format.font = font;
}
wb.recalculate();
const inspections = [];
for (const range of ['Overview!A1:D18', 'Mars Research Cards!A1:E16', 'EH Summary!A1:C12', 'EH Records!A1:O4']) {
  inspections.push((await wb.inspect({ kind: 'table', range, include: 'values,formulas', tableMaxRows: 18, tableMaxCols: 15, tableMaxCellChars: 100, maxChars: 6500 })).ndjson);
}
await fs.writeFile(path.join(OUT, 'review/main_v3/inspections.ndjson'), inspections.join('\n'));
const errors = await wb.inspect({ kind: 'match', searchTerm: '#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A|#NUM!|#NULL!|#SPILL!|#CALC!', options: { useRegex: true, maxResults: 50 }, summary: 'Final new-sheet formula error scan' });
await fs.writeFile(path.join(OUT, 'review/main_v3/formula_scan.ndjson'), errors.ndjson);
for (const tab of data.tables) {
  const maxCols = tab.name === 'EH Records' ? 6 : Math.min(tab.headers.length, 5);
  const range = `A1:${colName(maxCols-1)}${Math.min(tab.rows.length+1, 10)}`;
  const blob = await wb.render({ sheetName: tab.name, range, scale: 1, format: 'png' });
  await fs.writeFile(path.join(previews, `${tab.name}.png`), new Uint8Array(await blob.arrayBuffer()));
  console.log(`Rendered ${tab.name}`);
}
// Additional bounded windows cover the actual temperature/QA fields rather than
// rendering thousands of records or relying only on identifier columns.
for (const [key, sheetName, range] of [['EH measurements','EH Records','M1:X9'], ['EH missing flags','EH Records','Y1:AI9']]) {
  const blob = await wb.render({ sheetName, range, scale: 1, format: 'png' });
  await fs.writeFile(path.join(previews, `${key}.png`), new Uint8Array(await blob.arrayBuffer()));
}
const output = await SpreadsheetFile.exportXlsx(wb);
await output.save(path.join(OUT, 'support/main_v3_new_sheets.xlsx'));
console.log('Exported new native worksheets for capacity-limited merge.');
