#!/usr/bin/env python3
"""Inspect little-endian 16-bit index streams without assuming mesh topology.

This probe reports complete u16 values and any trailing byte. It does not claim
that values are triangle indices or that they address a particular VERT block.
"""
import argparse
import hashlib
import struct
import sys
from pathlib import Path


def analyze_file(path, preview_values=48):
    path = Path(path)
    if preview_values < 0:
        raise ValueError("preview_values não pode ser negativo")

    expected_size = path.stat().st_size
    digest = hashlib.sha256()
    count = 0
    minimum = None
    maximum = None
    zero_count = 0
    unique_values = set()
    preview = []
    bytes_read = 0
    pending = b""

    with path.open("rb") as stream:
        while True:
            chunk = stream.read(64 * 1024)
            if not chunk:
                break
            bytes_read += len(chunk)
            digest.update(chunk)
            data = pending + chunk
            if len(data) & 1:
                pending = data[-1:]
                data = data[:-1]
            else:
                pending = b""

            for (value,) in struct.iter_unpack("<H", data):
                count += 1
                minimum = value if minimum is None else min(minimum, value)
                maximum = value if maximum is None else max(maximum, value)
                zero_count += value == 0
                unique_values.add(value)
                if len(preview) < preview_values:
                    preview.append(value)

    if bytes_read != expected_size:
        raise OSError("arquivo mudou durante a leitura")

    return {
        "path": str(path),
        "size": expected_size,
        "bytes_read": bytes_read,
        "sha256": digest.hexdigest(),
        "u16_count": count,
        "remainder": len(pending),
        "min": minimum,
        "max": maximum,
        "unique_count": len(unique_values),
        "zero_count": zero_count,
        "preview": preview,
    }


def collect_files(path):
    path = Path(path)
    if path.is_file():
        return [path]
    if path.is_dir():
        return sorted(path.glob("*_INDX_*.bin"))
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


def render_report(results):
    lines = [
        "# PS2 geometry — INDX 16-bit stream probe",
        "",
        "Valores lidos como u16 little-endian são apenas uma hipótese de interpretação. "
        "Este relatório não determina topologia de triângulos nem offsets por bloco CHNK.",
        "Um byte final restante é reportado e nunca é passado para struct.unpack.",
        "",
    ]
    for result in results:
        lines.extend([
            "## {}".format(result["path"]),
            "",
            "- Tamanho: {} bytes".format(result["size"]),
            "- Bytes lidos: {}".format(result["bytes_read"]),
            "- SHA-256: {}".format(result["sha256"]),
            "- Valores u16 completos: {}".format(result["u16_count"]),
            "- Byte(s) final(is) incompleto(s): {}".format(result["remainder"]),
            "- Mínimo / máximo: {} / {}".format(
                result["min"] if result["min"] is not None else "n/a",
                result["max"] if result["max"] is not None else "n/a",
            ),
            "- Valores distintos: {}".format(result["unique_count"]),
            "- Valores zero: {}".format(result["zero_count"]),
            "- Amostra inicial: {}".format(", ".join(map(str, result["preview"])) or "n/a"),
            "",
        ])
    return "\n".join(lines) + "\n"


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Inspeciona fluxos INDX como u16 little-endian sem presumir topologia."
    )
    parser.add_argument("path", help="arquivo INDX ou pasta contendo *_INDX_*.bin")
    parser.add_argument("--preview", type=int, default=48, help="quantidade de valores na amostra (padrão: 48)")
    parser.add_argument("--output", help="arquivo Markdown de saída; por padrão imprime no terminal")
    args = parser.parse_args(argv)

    try:
        files = collect_files(args.path)
        if not files:
            raise FileNotFoundError("nenhum arquivo *_INDX_*.bin encontrado")
        if args.preview < 0:
            raise ValueError("preview não pode ser negativo")
        output_path = validate_output_path(args.output, files) if args.output else None
        report = render_report([analyze_file(path, preview_values=args.preview) for path in files])
        if output_path is not None:
            output_path.write_text(report, encoding="utf-8")
        else:
            sys.stdout.write(report)
    except (OSError, ValueError) as error:
        parser.error(str(error))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
