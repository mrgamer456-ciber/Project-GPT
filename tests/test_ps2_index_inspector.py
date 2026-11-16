import hashlib
import importlib.util
import os
import struct
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "tools" / "ps2-geometry" / "inspect_index_records.py"
SPEC = importlib.util.spec_from_file_location("inspect_index_records", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class IndexRecordInspectorTests(unittest.TestCase):
    def test_reads_little_endian_u16_values_and_statistics(self):
        payload = struct.pack("<5H", 2, 0, 5, 5, 1)
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "COMMON_INDX_04.bin"
            path.write_bytes(payload)
            result = MODULE.analyze_file(path)

        self.assertEqual(result["u16_count"], 5)
        self.assertEqual(result["remainder"], 0)
        self.assertEqual((result["min"], result["max"]), (0, 5))
        self.assertEqual(result["unique_count"], 4)
        self.assertEqual(result["zero_count"], 1)
        self.assertEqual(result["preview"], [2, 0, 5, 5, 1])
        self.assertEqual(result["sha256"], hashlib.sha256(payload).hexdigest())

    def test_odd_trailing_byte_is_reported_without_unpack_error(self):
        payload = b"\\x01\\x00\\x02"
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "sample_INDX.bin"
            path.write_bytes(payload)
            result = MODULE.analyze_file(path)

        self.assertEqual(result["u16_count"], 1)
        self.assertEqual(result["remainder"], 1)
        self.assertIn("Byte(s) final(is) incompleto(s): 1", MODULE.render_report([result]))

    def test_empty_file_is_reported(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "empty_INDX.bin"
            path.write_bytes(b"")
            result = MODULE.analyze_file(path)
        self.assertEqual(result["u16_count"], 0)
        self.assertIsNone(result["min"])
        self.assertIsNone(result["max"])

    def test_preview_zero_is_allowed_and_negative_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "sample_INDX.bin"
            path.write_bytes(struct.pack("<2H", 4, 9))
            self.assertEqual(MODULE.analyze_file(path, preview_values=0)["preview"], [])
            with self.assertRaises(ValueError):
                MODULE.analyze_file(path, preview_values=-1)

    def test_streams_multiple_chunks_and_preserves_odd_tail(self):
        payload = bytes(range(256)) * 256 + b"\\xaa"
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "COMMON_INDX_04.bin"
            path.write_bytes(payload)
            result = MODULE.analyze_file(path)

        self.assertEqual(result["bytes_read"], 65537)
        self.assertEqual(result["u16_count"], 32768)
        self.assertEqual(result["remainder"], 1)
        self.assertEqual((result["min"], result["max"]), (0x0100, 0xFFFE))
        self.assertEqual(result["unique_count"], 128)
        self.assertEqual(result["zero_count"], 0)
        self.assertEqual(result["sha256"], hashlib.sha256(payload).hexdigest())

    def test_directory_only_selects_index_sections(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            index = root / "COMMON_INDX_04.bin"
            other = root / "COMMON_VERT_04.bin"
            index.write_bytes(b"\\x00\\x00")
            other.write_bytes(bytes(16))
            self.assertEqual(MODULE.collect_files(root), [index])

    def test_output_cannot_overwrite_input(self):
        with tempfile.TemporaryDirectory() as temp:
            source = Path(temp) / "COMMON_INDX_04.bin"
            source.write_bytes(b"\\x00\\x00")
            with self.assertRaisesRegex(ValueError, "sobrescrever"):
                MODULE.validate_output_path(source, [source])

    def test_output_symlink_cannot_overwrite_input(self):
        with tempfile.TemporaryDirectory() as temp:
            source = Path(temp) / "COMMON_INDX_04.bin"
            alias = Path(temp) / "report.md"
            source.write_bytes(b"\\x00\\x00")
            alias.symlink_to(source)
            with self.assertRaisesRegex(ValueError, "sobrescrever"):
                MODULE.validate_output_path(alias, [source])

    def test_output_hardlink_cannot_overwrite_input(self):
        with tempfile.TemporaryDirectory() as temp:
            source = Path(temp) / "COMMON_INDX_04.bin"
            alias = Path(temp) / "report.md"
            source.write_bytes(b"\\x00\\x00")
            try:
                os.link(source, alias)
            except (OSError, NotImplementedError) as error:
                self.skipTest("hard links indisponíveis: {}".format(error))
            with self.assertRaisesRegex(ValueError, "sobrescrever"):
                MODULE.validate_output_path(alias, [source])

    def test_directory_only_selects_index_sections(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            index = root / "COMMON_INDX_04.bin"
            other = root / "COMMON_VERT_04.bin"
            index.write_bytes(b"\\x00\\x00")
            other.write_bytes(bytes(16))
            self.assertEqual(MODULE.collect_files(root), [index])


if __name__ == "__main__":
    unittest.main()
