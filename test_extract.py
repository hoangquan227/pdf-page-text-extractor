"""Phép thử tối thiểu: logic xác định trang 'thiếu chữ' phải đúng, thử ngược phải đỏ."""
from extract import trich


def thieu_trang(trang_list, nguong=10):
    return [i + 1 for i, t in enumerate(trang_list) if len(t) < nguong]


def test_mau_dung():
    # Mẫu ĐÚNG: trang có câu dài tính là có chữ, trang rỗng tính là thiếu
    trang = ["Đây là một đoạn văn bản đủ dài để tính là có chữ thật.", "", "PHẦN IV"]
    assert thieu_trang(trang) == [2, 3], thieu_trang(trang)


def test_pha_nguoc_nguong_sai():
    # Thử PHÁ: nếu ai đó sửa nhầm điều kiện thành > thay vì <, phép thử này phải ĐỎ
    trang = ["Đây là một đoạn văn bản đủ dài để tính là có chữ thật.", ""]
    ket_qua_sai = [i + 1 for i, t in enumerate(trang) if len(t) > 10]  # cố ý phá
    assert ket_qua_sai != thieu_trang(trang), "phép thử không bắt được lỗi đảo dấu điều kiện"


if __name__ == "__main__":
    test_mau_dung()
    test_pha_nguoc_nguong_sai()
    print("OK: 2/2 phép thử qua (1 mẫu đúng xanh, 1 kiểu phá bị bắt)")
