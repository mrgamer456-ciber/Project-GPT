#!/usr/bin/env python3
"""Inspect fixed-size binary vertex records without assuming a confirmed layout.

The report shows raw bytes plus independent little-endian u16, i16 and aligned
f32 interpretations. It does not claim that any lane is a position, UV or normal.
"""
import argparse
import hashlib
import math
import struct
import sys
from pathlib import Path


def _empty_ranges(count):
    return [{"min": None, "max": None} for _ in range(count)]


def _add_value(slot, value):
    if slot["min"] is None or value < slot["min"]:
        slot["min"] = value
    if slot["max"] is None or value > slot["max"]:
        slot["max"] = value


def analyze_file(path, stride=16, preview_records=12):
    path = Path(path)
    if stride < 4 or stride % 2:
        raise ValueError("stride precisa ser par e ter pelo menos 4 bytes")
    if stride > 4096:
        raise ValueError("stride não pode exceder 4096 bytes")
    if preview_records < 0:
        raise ValueError("preview_records não pode ser negativo")

    size = path.stat().st_size
    record_count, remainder = divmod(size, stride)
    u16_count = stride // 2
    f32_count = stride // 4

    u16_stats = _empty_ranges(u16_count)
    i16_stats = _empty_ranges(u16_count)
    f32_stats = _empty_ranges(f32_count)
    preview = []
    digest = hashlib.sha256()
    u16_format = "<" + ("H" * u16_count)
    i16_format = "<" + ("h" * u16_count)
    f32_format = "<" + ("f" * f32_count)

    with path.open("rb") as stream:
        for record_index in range(record_count):
            record = stream.read(stride)
            if len(record) != stride:
                raise OSError("arquivo mudou durante a leitura")

            digest.update(record)
            u16_values = struct.unpack(u16_format, record)
            i16_values = struct.unpack(i16_format, record)
            f32_values = struct.unpack(f32_format, record[:f32_count * 4])

            for lane, value in enumerate(u16_values):
                _add_value(u16_stats[lane], value)
            for lane, value in enumerate(i16_values):
                _add_value(i16_stats[lane], value)
            for lane, value in enumerate(f32_values):
                if math.isfinite(value):
                    _add_value(f32_stats[lane], value)

            if record_index < preview_records:
                preview.append({
                    "index": record_index,
                    "hex": record.hex(" "),
                    "u16": u16_values,
                    "i16": i16_values,
                    "f32": f32_values,
                })

        tail = stream.read(remainder)
        digest.update(tail)

    return {
        "path": str(path),
        "size": size,
        "sha256": digest.hexdigest(),
        "stride": stride,
        "records": record_count,
        "remainder": remainder,
        "u16_stats": u16_stats,
        "i16_stats": i16_stats,
        "f32_stats": f32_stats,
        "preview": preview,
    }


def _range_text(slot, floating=False):
    if slot["min"] is None:
        return "n/a"
    if floating:
        return "{:.6g} .. {:.6g}".format(slot["min"], slot["max"])
    return "{} .. {}".format(slot["min"], slot["max"])


def render_report(results):
    lines = [
        "# PS2 geometry — packed vertex record probe",
        "",
        "As leituras u16/i16/f32 são interpretações numéricas independentes. "
        "Nenhuma lane é identificada automaticamente como posição, UV, normal ou cor.",
        "",
    ]
    for result in results:
        lines.extend([
            "## {}".format(result["path"]),
            "",
            "- Tamanho: {} bytes".format(result["size"]),
            "- Stride testado: {} bytes".format(result["stride"]),
            "- Registros completos: {}".format(result["records"]),
            "- Bytes finais fora de um registro: {}".format(result["remainder"]),
            "- SHA-256: {}".format(result["sha256"]),
            "",
        ])
        if not result["records"]:
            lines.extend(["Nenhum registro completo para analisar.", ""])
            continue

        lines.extend([
            "### Primeiros registros",
            "",
            "| Registro | HEX | u16 little-endian | i16 little-endian | f32 alinhado (4 bytes) |",
            "|---:|---|---|---|---|",
        ])
        for record in result["preview"]:
            u16 = ", ".join(str(x) for x in record["u16"])
            i16 = ", ".join(str(x) for x in record["i16"])
            f32 = ", ".join("{:.6g}".format(x) for x in record["f32"])
            lines.append(
                "| {} | {} | {} | {} | {} |".format(
                    record["index"], record["hex"], u16, i16, f32
                )
            )

        lines.extend([
            "",
            "### Faixas por lane",
            "",
            "| Lane u16/i16 (2 bytes) | u16 min..max | i16 min..max |",
            "|---:|---:|---:|",
        ])
        for lane, (u16, i16) in enumerate(zip(result["u16_stats"], result["i16_stats"])):
            lines.append(
                "| {} | {} | {} |".format(
                    lane, _range_text(u16), _range_text(i16)
                )
            )

        lines.extend([
            "",
            "| Lane f32 alinhada (4 bytes) | f32 min..max |",
            "|---:|---:|",
        ])
        for lane, values in enumerate(result["f32_stats"]):
            lines.append("| {} | {} |".format(lane, _range_text(values, True)))
        lines.append("")

    return "\n".join(lines) + "\n"


def collect_files(path):
    path = Path(path)
    if path.is_file():
        return [path]
    if path.is_dir():
        return sorted(path.glob("*_VERT_*.bin"))
    raise FileNotFoundError("caminho não encontrado: {}".format(path))


def validate_output_path(output, input_files):
    """Reject an output path that aliases any input file."""
    target = Path(output)
    target_resolved = target.resolve()
    for source in input_files:
        source = Path(source)
        if target_resolved == source.resolve():
            raise ValueError("arquivo de saída não pode sobrescrever um arquivo de entrada")
        if target.exists() and source.exists() and target.samefile(source):
            raise ValueError("arquivo de saída não pode sobrescrever um arquivo de entrada")
    return target


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Inspeciona registros binários VERT sem presumir o formato."
    )
    parser.add_argument("path", help="arquivo VERT ou pasta contendo *_VERT_*.bin")
    parser.add_argument("--stride", type=int, default=16, help="tamanho do registro em bytes (padrão: 16)")
    parser.add_argument("--output", help="arquivo Markdown de saída; por padrão imprime no terminal")
    args = parser.parse_args(argv)

    try:
        files = collect_files(args.path)
        if not files:
            raise FileNotFoundError("nenhum arquivo *_VERT_*.bin encontrado")
        output_path = validate_output_path(args.output, files) if args.output else None
        results = [analyze_file(path, stride=args.stride) for path in files]
        report = render_report(results)
        if output_path is not None:
            output_path.write_text(report, encoding="utf-8")
        else:
            sys.stdout.write(report)
    except (OSError, ValueError) as error:
        parser.error(str(error))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
