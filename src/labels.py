"""Nhan tieng Viet va dinh dang hien thi."""

SUBJECT_VI = {
    "Toan": "Toán",
    "NguVan": "Ngữ văn",
    "VatLy": "Vật lý",
    "HoaHoc": "Hóa học",
    "SinhHoc": "Sinh học",
    "LichSu": "Lịch sử",
    "DiaLy": "Địa lý",
    "GDCD": "GDCD",
    "NgoaiNgu": "Ngoại ngữ",
    "KinhTePhapLuat": "Kinh tế & Pháp luật",
    "TinHoc": "Tin học",
    "CongNgheCongNghiep": "Công nghệ công nghiệp",
    "CongNgheNongNghiep": "Công nghệ nông nghiệp",
}

PROVINCE_VI = {
    1: "Hà Nội", 2: "Hà Giang", 3: "Cao Bằng", 4: "Bắc Kạn", 5: "Tuyên Quang",
    6: "Lào Cai", 7: "Điện Biên", 8: "Lai Châu", 9: "Sơn La", 10: "Yên Bái",
    11: "Hòa Bình", 12: "Thái Nguyên", 13: "Lạng Sơn", 14: "Quảng Ninh", 15: "Bắc Giang",
    16: "Phú Thọ", 17: "Vĩnh Phúc", 18: "Bắc Ninh", 19: "Hải Dương", 20: "Hải Phòng",
    21: "Hưng Yên", 22: "Thái Bình", 23: "Hà Nam", 24: "Nam Định", 25: "Ninh Bình",
    26: "Thanh Hóa", 27: "Nghệ An", 28: "Hà Tĩnh", 29: "Quảng Bình", 30: "Quảng Trị",
    31: "Thừa Thiên Huế", 32: "Đà Nẵng", 33: "Quảng Nam", 34: "Quảng Ngãi", 35: "Bình Định",
    36: "Phú Yên", 37: "Khánh Hòa", 38: "Ninh Thuận", 39: "Bình Thuận", 40: "Kon Tum",
    41: "Gia Lai", 42: "Đắk Lắk", 43: "Đắk Nông", 44: "Lâm Đồng", 45: "Bình Phước",
    46: "Tây Ninh", 47: "Bình Dương", 48: "Đồng Nai", 49: "Bà Rịa - Vũng Tàu", 50: "TP. Hồ Chí Minh",
    51: "Long An", 52: "Tiền Giang", 53: "Bến Tre", 54: "Trà Vinh", 55: "Vĩnh Long",
    56: "Đồng Tháp", 57: "An Giang", 58: "Kiên Giang", 59: "Cần Thơ", 60: "Hậu Giang",
    61: "Sóc Trăng", 62: "Bạc Liêu", 63: "Cà Mau",
}


def subject_vi(code: str) -> str:
    return SUBJECT_VI.get(code, code)


def province_vi(code) -> str:
    try:
        return PROVINCE_VI.get(int(code), str(code))
    except (TypeError, ValueError):
        return str(code)


def fmt_int(n) -> str:
    if n is None or (isinstance(n, float) and n != n):
        return "—"
    return f"{int(n):,}".replace(",", ".")


def fmt_float(x, digits=2) -> str:
    if x is None or (isinstance(x, float) and x != x):
        return "—"
    s = f"{float(x):,.{digits}f}"
    return s.replace(",", "X").replace(".", ",").replace("X", ".")
