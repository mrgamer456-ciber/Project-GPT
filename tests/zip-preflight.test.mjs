import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import vm from 'node:vm';

// Testa a função real embutida no HTML, sem depender de JSZip ou de rede.
const htmlUrl = new URL('../tools/zip-extractor/index.html', import.meta.url);
const html = readFileSync(htmlUrl, 'utf8');
const match = html.match(/async function preflightZip\\(blob\\)\\s*\\{[\\s\\S]*?\\n\\}\\nasync function unpack/);
assert.ok(match, 'preflightZip deve existir no ZIP Extractor');
const functionSource = match[0].replace(/\\nasync function unpack$/, '');
const context = {
  LIMITS: {
    archive: 128 * 1024 * 1024,
    entries: 5000,
    entry: 128 * 1024 * 1024,
    total: 256 * 1024 * 1024
  },
  Blob, DataView, Uint8Array, Error, Number, Object, Math
};
vm.runInNewContext(`${functionSource}\\nglobalThis.preflightZip = preflightZip;`, context);
const preflightZip = context.preflightZip;

function makeZip({ prefix = Buffer.alloc(0), name = 'sample.bin', data = Buffer.from('PS2'), dataDescriptor = false } = {}) {
  const nameBytes = Buffer.from(name, 'utf8');
  const local = Buffer.alloc(30);
  local.writeUInt32LE(0x04034b50, 0);
  local.writeUInt16LE(20, 4);
  local.writeUInt16LE(dataDescriptor ? 0x08 : 0, 6);
  local.writeUInt16LE(0, 8);
  local.writeUInt32LE(0, 14);
  local.writeUInt32LE(dataDescriptor ? 0 : data.length, 18);
  local.writeUInt32LE(dataDescriptor ? 0 : data.length, 22);
  local.writeUInt16LE(nameBytes.length, 26);
  local.writeUInt16LE(0, 28);

  const descriptor = Buffer.alloc(dataDescriptor ? 16 : 0);
  if (dataDescriptor) {
    descriptor.writeUInt32LE(0x08074b50, 0);
    descriptor.writeUInt32LE(0, 4);
    descriptor.writeUInt32LE(data.length, 8);
    descriptor.writeUInt32LE(data.length, 12);
  }
  const localRecord = Buffer.concat([local, nameBytes, data, descriptor]);

  const central = Buffer.alloc(46);
  central.writeUInt32LE(0x02014b50, 0);
  central.writeUInt16LE(20, 4);
  central.writeUInt16LE(20, 6);
  central.writeUInt16LE(dataDescriptor ? 0x08 : 0, 8);
  central.writeUInt16LE(0, 10);
  central.writeUInt32LE(0, 16);
  central.writeUInt32LE(data.length, 20);
  central.writeUInt32LE(data.length, 24);
  central.writeUInt16LE(nameBytes.length, 28);
  central.writeUInt16LE(0, 30);
  central.writeUInt16LE(0, 32);
  central.writeUInt16LE(0, 34);
  central.writeUInt32LE(0, 42);
  const centralRecord = Buffer.concat([central, nameBytes]);

  const cdOffset = localRecord.length;
  const eocd = Buffer.alloc(22);
  eocd.writeUInt32LE(0x06054b50, 0);
  eocd.writeUInt16LE(1, 8);
  eocd.writeUInt16LE(1, 10);
  eocd.writeUInt32LE(centralRecord.length, 12);
  eocd.writeUInt32LE(cdOffset, 16);

  return {
    bytes: Buffer.concat([prefix, localRecord, centralRecord, eocd]),
    centralOffset: prefix.length + cdOffset
  };
}

async function accepts(label, bytes, expectedEntries = 1) {
  const result = await preflightZip(new Blob([bytes]));
  assert.equal(result.entryCount, expectedEntries, label + ': quantidade de entradas');
  return result;
}
async function rejects(label, bytes) {
  await assert.rejects(() => preflightZip(new Blob([bytes])), undefined, label + ': deveria rejeitar');
}

const ordinary = makeZip();
const ordinaryResult = await accepts('ZIP comum', ordinary.bytes);
assert.equal(ordinaryResult.totalUncompressed, 3);

const selfExtracting = makeZip({ prefix: Buffer.from('MZ-STUB') });
await accepts('ZIP com prefixo autoextraível', selfExtracting.bytes);

const descriptor = makeZip({ dataDescriptor: true });
await accepts('ZIP com data descriptor', descriptor.bytes);

const badOffset = makeZip();
badOffset.bytes.writeUInt32LE(0x7fffffff, badOffset.centralOffset + 42);
await rejects('offset de cabeçalho local fora do arquivo', badOffset.bytes);

const badCompressedSize = makeZip();
badCompressedSize.bytes.writeUInt32LE(0x7fffffff, badCompressedSize.centralOffset + 20);
await rejects('dados compactados além da área de dados', badCompressedSize.bytes);

const badSignature = makeZip();
badSignature.bytes.writeUInt32LE(0x11111111, 0);
await rejects('assinatura de cabeçalho local inválida', badSignature.bytes);

const badHeaderLength = makeZip();
badHeaderLength.bytes.writeUInt16LE(0xffff, 26);
await rejects('nome do cabeçalho local além dos limites', badHeaderLength.bytes);

const empty = Buffer.alloc(22);
empty.writeUInt32LE(0x06054b50, 0);
await accepts('ZIP vazio', empty, 0);

console.log('ZIP preflight: 8 casos passaram (ZIP comum, prefixo SFX, data descriptor, ZIP vazio e quatro entradas malformadas).');
