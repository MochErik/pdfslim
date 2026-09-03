"""PDFSlim CLI Main Entrypoint."""

import argparse
import os
import sys
from typing import List

from pdfslim.compressor import inspect_pdf, compress_pdf

RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
GREEN = "\033[32m"
CYAN = "\033[36m"
YELLOW = "\033[33m"


def main(args: List[str] = None):
    parser = argparse.ArgumentParser(
        prog="pdfslim",
        description="📄 PDFSlim - Zero-Bloat PDF Compressor & Metadata Sanitizer CLI",
        epilog="Examples:\n"
               "  pdfslim info document.pdf                  # Inspect file size and page count\n"
               "  pdfslim compress paper.pdf -o paper_slim.pdf # Compress PDF for upload limits\n",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    subparsers = parser.add_subparsers(dest="subcommand")

    # Info
    info_p = subparsers.add_parser("info", help="Inspect PDF file metadata and page count")
    info_p.add_argument("file", help="PDF file path")

    # Compress
    comp_p = subparsers.add_parser("compress", help="Compress PDF file")
    comp_p.add_argument("file", help="Source PDF file")
    comp_p.add_argument("-o", "--output", help="Output PDF file path (default: <name>_slim.pdf)")
    comp_p.add_argument("-q", "--quality", choices=["screen", "ebook", "printer"], default="ebook", help="Quality level")

    parsed = parser.parse_args(args)

    if parsed.subcommand == "info":
        info = inspect_pdf(parsed.file)
        if not info["exists"]:
            print(f"{YELLOW}❌ File '{parsed.file}' does not exist.{RESET}")
            sys.exit(1)
        print(f"\n📄 {BOLD}PDF Inspection:{RESET} {info['filename']}")
        print(f"  • Size : {CYAN}{info['size_mb']} MB{RESET} ({info['size_bytes']:,} bytes)")
        print(f"  • Pages: {GREEN}{info['pages']}{RESET}\n")

    elif parsed.subcommand == "compress":
        output = parsed.output or f"{os.path.splitext(parsed.file)[0]}_slim.pdf"
        print(f"⏳ Compressing '{parsed.file}' -> '{output}' (Quality: {parsed.quality})...")
        ok, msg = compress_pdf(parsed.file, output, quality=parsed.quality)
        if ok:
            print(f"{GREEN}{BOLD}✅ {msg}{RESET}")
            orig_sz = os.path.getsize(parsed.file) / (1024 * 1024)
            new_sz = os.path.getsize(output) / (1024 * 1024)
            print(f"   Original: {orig_sz:.2f} MB  ➜  New: {new_sz:.2f} MB\n")
        else:
            print(f"{YELLOW}❌ Compression failed: {msg}{RESET}")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
