#!/usr/bin/env python3
"""Trích chữ từng trang PDF thành mảng JSON (1 phần tử = 1 trang).

Dùng pypdf đọc text layer có sẵn trong PDF (miễn phí, tức thì). Trang nào
không có text layer thật (ảnh/thiết kế đồ hoạ) sẽ ra chuỗi rỗng hoặc rất
ngắn — công cụ này CHỈ báo trang nào cần người đọc bằng mắt và chép tay,
KHÔNG tự chạy OCR (OCR trộn icon/hoa văn thành chữ rác, xem README).

Dùng:
    python extract.py sach.pdf -o chu-trang.json
    python extract.py sach.pdf --nguong 10   # trang nào dưới 10 ký tự = "thiếu"
"""
import argparse
import json
import sys

from pypdf import PdfReader


def trich(duong_dan_pdf: str) -> list[str]:
    reader = PdfReader(duong_dan_pdf)
    ket_qua = []
    for trang in reader.pages:
        chu = (trang.extract_text() or "").strip()
        chu = " ".join(chu.split())
        ket_qua.append(chu)
    return ket_qua


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("pdf", help="Đường dẫn file PDF gốc")
    p.add_argument("-o", "--out", default=None, help="Ghi ra file JSON (mặc định in ra stdout)")
    p.add_argument("--nguong", type=int, default=10, help="Số ký tự tối thiểu để tính là 'có chữ' (mặc định 10)")
    args = p.parse_args()

    trang_list = trich(args.pdf)
    thieu = [i + 1 for i, t in enumerate(trang_list) if len(t) < args.nguong]

    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            json.dump(trang_list, f, ensure_ascii=False)
        print(f"Đã ghi {args.out}: {len(trang_list)} trang, {len(trang_list) - len(thieu)} có chữ, "
              f"{len(thieu)} trang CẦN CHÉP TAY: {thieu}", file=sys.stderr)
    else:
        print(json.dumps(trang_list, ensure_ascii=False))
        print(f"# {len(trang_list)} trang, {len(thieu)} trang thiếu: {thieu}", file=sys.stderr)


if __name__ == "__main__":
    main()
