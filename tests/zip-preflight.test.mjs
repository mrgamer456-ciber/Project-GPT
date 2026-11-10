import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import vm from 'node:vm';

// Testa a função real embutida no HTML, sem depender de JSZip ou de rede.
const htmlUrl = new URL('../tools/zip-extractor/index.html', import.meta.url);
const html = readFileSync(htmlUrl, 'utf8');
const match = html.match(/async function preflightZip\(blob\)\s*\{[\s\S]*?\n\}\nasync function unpack/);
assert.ok(match, 'preflightZip deve existir no ZIP Extractor');
const functionSource = match[0].replace(/\nasync function unpack$/, '');
const context = {
  LIMITS: { archive: 128 * 1024 * 1024, entries: 5000, entry: 128 * 1024 * 1024, total: 256 * 1024 * 1024 },
  Blob, DataView, Uint8Array, Error, Number, Object, Math
};
vm.runInNewContext(functionSource + "\nglobalThis.preflightZip = preflightZip;", context);
const preflightZip = context.preflightZip;

function makeZip({ prefix = Buffer.alloc(0), name = 'sample.bin', data = Buffer.from('PS2'), dataDescriptor = false, descriptorSignature = true } = {}) {
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

  const descriptor = Buffer.alloc(dataDescriptor ? (descriptorSignature ? 16 : 12) : 0);
  if (dataDescriptor) {
    const shift = descriptorSignature ? 4 : 0;
    if (descriptorSignature) descriptor.writeUInt32LE(0x08074b50, 0);
    descriptor.writeUInt32LE(0, shift);
    descriptor.writeUInt32LE(data.length, shift + 4);
    descriptor.writeUInt32LE(data.length, shift + 8);
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
  return { bytes: Buffer.concat([prefix, localRecord, centralRecord, eocd]), centralOffset: prefix.length + cdOffset };
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
await accepts('ZIP com prefixo autoextraível', makeZip({ prefix: Buffer.from('MZ-STUB') }).bytes);
await accepts('ZIP com data descriptor', makeZip({ dataDescriptor: true }).bytes);
await accepts('ZIP com data descriptor sem assinatura', makeZip({ dataDescriptor: true, descriptorSignature: false }).bytes);

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
const localMethodMismatch = makeZip();
localMethodMismatch.bytes.writeUInt16LE(8, 8);
await rejects('método local diferente do central', localMethodMismatch.bytes);
const localFlagsMismatch = makeZip();
localFlagsMismatch.bytes.writeUInt16LE(1, 6);
await rejects('flags locais diferentes das centrais', localFlagsMismatch.bytes);
const localNameMismatch = makeZip();
localNameMismatch.bytes[30] ^= 1;
await rejects('nome local diferente do central', localNameMismatch.bytes);
const localCrcMismatch = makeZip();
localCrcMismatch.bytes.writeUInt32LE(0x12345678, 14);
await rejects('CRC local diferente do central', localCrcMismatch.bytes);
const localSizeMismatch = makeZip();
localSizeMismatch.bytes.writeUInt32LE(99, 18);
await rejects('tamanho local diferente do central', localSizeMismatch.bytes);
const unsupportedMethod = makeZip();
unsupportedMethod.bytes.writeUInt16LE(99, unsupportedMethod.centralOffset + 10);
await rejects('método de compactação não suportado', unsupportedMethod.bytes);
const badDescriptor = makeZip({ dataDescriptor: true });
const descriptorOffset = 30 + Buffer.byteLength('sample.bin') + 3;
badDescriptor.bytes.writeUInt32LE(0x12345678, descriptorOffset + 4);
await rejects('descritor de dados inconsistente', badDescriptor.bytes);

const empty = Buffer.alloc(22);
empty.writeUInt32LE(0x06054b50, 0);
await accepts('ZIP vazio', empty, 0);
console.log('ZIP preflight: 16 casos passaram (ZIP comum, prefixo SFX, descritores com/sem assinatura, ZIP vazio e entradas malformadas/inconsistentes).');
