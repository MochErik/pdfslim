"""Unit tests for PDFSlim."""

import unittest
from pdfslim.compressor import inspect_pdf


class TestPDFSlim(unittest.TestCase):

    def test_inspect_nonexistent(self):
        info = inspect_pdf("nonexistent_file.pdf")
        self.assertFalse(info["exists"])


if __name__ == "__main__":
    unittest.main()
