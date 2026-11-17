import importlib.util
import io
import struct
import os
import tempfile
import unittest
from unittest import mock
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "tools" / "ps2-geometry" / "inspect_vertex_records.py"
SPEC = importlib.util.spec_from_file_location("inspect_vertex_records", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class VertexRecordInspectorTests(unittest.TestCase):
    def test_16_byte_records_have_four_safe_float_lanes(self):
        first = struct.pack("<8H", 1, 2, 3, 4, 5, 6, 7, 8)
        second = struct.pack("<8H", 101, 102, 103, 104, 105, 106, 107, 108)
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "COMMON_VERT_04.bin"
            path.write_bytes(first + second)
            result = MODULE.analyze_file(path)

        self.assertEqual(result["records"], 2)
        self.assertEqual(result["remainder"], 0)
        self.assertEqual(len(result["u16_stats"]), 8)
        self.assertEqual(len(result["f32_stats"]), 4)
        self.assertEqual(result["u16_stats"][7], {"min": 8, "max": 108})

    def test_trailing_bytes_are_reported_not_unpacked(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "sample_VERT.bin"
            path.write_bytes(bytes(range(18)))
            result = MODULE.analyze_file(path)

        self.assertEqual(result["records"], 1)
        self.assertEqual(result["remainder"], 2)

    def test_empty_file_is_reported_without_crashing(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "empty_VERT.bin"
            path.write_bytes(b"")
            result = MODULE.analyze_file(path)
        self.assertEqual(result["records"], 0)
        self.assertIn("Nenhum registro completo", MODULE.render_report([result]))

    def test_invalid_stride_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "sample.bin"
            path.write_bytes(bytes(32))
            with self.assertRaises(ValueError):
                MODULE.analyze_file(path, stride=3)

    def test_even_strides_with_partial_f32_lane_are_supported(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "sample_VERT.bin"
            for stride in (6, 18):
                data = bytes(range(stride * 2))
                path.write_bytes(data)
                result = MODULE.analyze_file(path, stride=stride)

                self.assertEqual(result["records"], 2)
                self.assertEqual(result["remainder"], 0)
                self.assertEqual(len(result["f32_stats"]), stride // 4)
                f32_size = (stride // 4) * 4
                for record_index in range(2):
                    start = record_index * stride
                    expected = struct.unpack(
                        "<" + ("f" * (stride // 4)),
                        data[start:start + f32_size],
                    )
                    self.assertEqual(
                        result["preview"][record_index]["f32"],
                        expected,
                    )

    def test_non_finite_f32_values_are_excluded_from_statistics(self):
        payload = struct.pack("<4f", float("nan"), float("inf"), float("-inf"), -2.5)
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "sample_VERT.bin"
            path.write_bytes(payload)
            result = MODULE.analyze_file(path, stride=16)

        for lane in range(3):
            self.assertEqual(result["f32_stats"][lane], {"min": None, "max": None})
        self.assertEqual(result["f32_stats"][3], {"min": -2.5, "max": -2.5})
        self.assertEqual(result["f32_finite_counts"], [0, 0, 0, 1])
        self.assertEqual(result["f32_non_finite_counts"], [1, 1, 1, 0])
        report = MODULE.render_report([result])
        self.assertIn("| 0 | n/a | 0 | 1 |", report)
        self.assertIn("| 3 | -2.5 .. -2.5 | 1 | 0 |", report)

    def test_output_path_cannot_overwrite_input_file(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "COMMON_VERT_04.bin"
            original = bytes(range(16))
            path.write_bytes(original)

            with self.assertRaisesRegex(ValueError, "sobrescrever"):
                MODULE.validate_output_path(path, [path])

            self.assertEqual(path.read_bytes(), original)

    def test_output_symlink_cannot_overwrite_input_file(self):
        with tempfile.TemporaryDirectory() as temp:
            source = Path(temp) / "COMMON_VERT_04.bin"
            alias = Path(temp) / "report.md"
            source.write_bytes(bytes(range(16)))
            alias.symlink_to(source)

            with self.assertRaisesRegex(ValueError, "sobrescrever"):
                MODULE.validate_output_path(alias, [source])

            self.assertEqual(source.read_bytes(), bytes(range(16)))

    def test_output_hardlink_cannot_overwrite_input_file(self):
        with tempfile.TemporaryDirectory() as temp:
            source = Path(temp) / "COMMON_VERT_04.bin"
            alias = Path(temp) / "report.md"
            original = bytes(range(16))
            source.write_bytes(original)
            try:
                os.link(source, alias)
            except (OSError, NotImplementedError) as error:
                self.skipTest("hard links não estão disponíveis neste ambiente: {}".format(error))

            with self.assertRaisesRegex(ValueError, "sobrescrever"):
                MODULE.validate_output_path(alias, [source])

            self.assertEqual(source.read_bytes(), original)

    def test_file_growth_during_read_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "sample_VERT.bin"
            path.write_bytes(bytes(16))

            # Keep the initial stat size at 16 bytes while presenting a stream
            # with appended data, simulating a file that grows during analysis.
            with mock.patch.object(
                MODULE.Path,
                "open",
                lambda self, *args, **kwargs: io.BytesIO(bytes(32)),
            ):
                with self.assertRaisesRegex(OSError, "arquivo mudou durante a leitura"):
                    MODULE.analyze_file(path, stride=16)

    def test_directory_only_selects_vertex_sections(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            vertex = root / "COMMON_VERT_04.bin"
            other = root / "COMMON_INDX_05.bin"
            vertex.write_bytes(bytes(16))
            other.write_bytes(bytes(16))
            self.assertEqual(MODULE.collect_files(root), [vertex])


if __name__ == "__main__":
    unittest.main()
