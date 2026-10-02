# pdf-page-text-extractor

Trích chữ từng trang của một PDF thành mảng JSON (`["chữ trang 1", "chữ trang 2", ...]`),
dùng cho các tính năng đọc giọng nói / tìm kiếm theo trang (vd flipbook, sổ tay điện tử).

## Vì sao công cụ này tồn tại

Nhiều PDF (sách hướng dẫn, sổ tay) đã có sẵn **text layer thật** do phần mềm xuất ra
(Word → PDF, InDesign có xuất text...), không cần OCR. Đọc thẳng layer đó bằng
[`pypdf`](https://pypi.org/project/pypdf/) là **miễn phí, tức thì, chính xác tuyệt đối**
(chữ lấy nguyên từ nguồn, không qua máy đoán).

Nhưng một số trang trong cùng cuốn sách lại là **ảnh thiết kế / đồ hoạ thuần tuý**
(trang bìa, trang chia phần, infographic) — không có text layer, `pypdf` trả về chuỗi rỗng.
Công cụ này **không chạy OCR cho các trang đó** (OCR trộn icon/hoa văn thành chữ rác —
xem ca thật bên dưới), mà **báo rõ số trang cần người đọc bằng mắt và chép tay**.

## Ca thật đã dùng (02/10/2026, dự án TCKN)

Trích 7 cuốn sổ tay thuế điện tử (338 trang gốc PDF), kết quả:

| Cuốn | Số trang | Tự động (pypdf) | Phải chép tay |
|---|---|---|---|
| Hoàn thuế GTGT (thiết kế đồ hoạ nặng) | 38 | 16 | 22 |
| Hộ kinh doanh | 51 | 51 | 0 |
| HKD chuyển khoán→kê khai | 16 | 15 | 1 |
| Chủ doanh nghiệp | 39 | 39 | 0 |
| Kế toán trưởng | 70 | 70 | 0 |
| Công chức thuế | 17 | 16 | 1 |
| Công chức cấp xã | 47 | 47 | 0 |

→ 6/7 cuốn gần như 100% tự động; chỉ cuốn thiết kế đồ hoạ nặng mới cần chép tay nhiều.
**Luôn thử pypdf trước — đừng mặc định phải chép tay cả cuốn.**

## Dùng

```bash
pip install pypdf
python extract.py sach.pdf -o chu-trang.json
# In ra: "Đã ghi chu-trang.json: 38 trang, 16 có chữ, 22 trang CẦN CHÉP TAY: [1,3,5,...]"
```

Trang nào bị báo "CẦN CHÉP TAY": mở ảnh trang đó, đọc bằng mắt, điền thủ công vào đúng
chỉ số trong file JSON. Xem phương pháp chép tay (phân biệt nội dung chính / nhãn trang trí /
slogan, giữ nguyên số điều luật) tại skill `chep-chu-tu-anh-do-hoa` trong
[hoangquan227/doc-to-sang-highlight](https://github.com/hoangquan227/doc-to-sang-highlight)
(dùng chung bộ "đọc giọng nói + tô sáng theo trang").

## Phép thử

```bash
python test_extract.py
```

Kiểm logic ngưỡng "trang thiếu chữ": 1 mẫu biết chắc đúng phải xanh, 1 kiểu phá (đảo dấu
điều kiện `<` thành `>`) phải bị bắt — không chỉ chạy xanh suông.

## Giới hạn

- Không OCR. Trang ảnh thuần sẽ luôn cần chép tay.
- Không tự sắp xếp lại thứ tự cột nếu PDF có bố cục nhiều cột lộn xộn trong text layer
  (hiếm gặp, nhưng có thể làm thứ tự câu trong JSON sai so với mắt đọc).
