"""Thuật ngữ và đoạn mở đầu dễ hiểu cho người không chuyên."""
from __future__ import annotations

from .config import YEAR_MAX, YEAR_MIN


def section_glossary() -> str:
    return f"""
---

## Đọc trước — Dành cho người chưa quen phân tích dữ liệu

Báo cáo này dùng **số liệu điểm thi THPT quốc gia** ({YEAR_MIN}–{YEAR_MAX}) để trả lời ba câu hỏi đơn giản:

1. **Có bao nhiêu thí sinh** thi mỗi năm?
2. **Điểm trung bình** các môn đang **tăng hay giảm**?
3. **Năm sau** điểm TB có thể **khoảng bao nhiêu** (ước lượng học thuật)?

### Bảng thuật ngữ (giải thích ngắn)

| Thuật ngữ | Nghĩa dễ hiểu |
|-----------|----------------|
| **Thí sinh** | Học sinh tham gia kỳ thi |
| **Điểm TB (trung bình)** | Cộng tất cả điểm (của người đã thi môn) rồi chia cho số người — giống **điểm trung bình lớp** |
| **Tỷ lệ ≥ 8** | Phần trăm thí sinh **đạt từ 8.0 trở lên** ở môn đó (thường được coi là điểm khá) |
| **Biểu đồ cột** | Mỗi cột = một năm; cột cao hơn = nhiều thí sinh hơn |
| **Biểu đồ đường** | Nối các điểm theo năm; đường **đi lên** = TB tăng, **đi xuống** = TB giảm |
| **Heatmap (bản đồ nhiệt)** | Bảng màu theo tỉnh: **màu đậm** ≈ điểm cao hơn, **màu nhạt** ≈ điểm thấp hơn |
| **Dự báo** | Ước lượng năm tới dựa trên xu hướng 5 năm qua — **không phải** điểm chính thức của Bộ GD&ĐT |
| **MAE (sai số)** | Mô hình dự đoán lệch trung bình bao nhiêu điểm so với thực tế — **càng nhỏ càng tốt** |
| **0.0 điểm** | Trong dữ liệu = **không thi môn đó** (không tính vào TB môn) |

### Cách đọc báo cáo nhanh (5 phút)

- Chỉ muốn **tổng quan** → đọc [Mục 1](#1-tóm-tắt) và [Mục 6](#6-kết-quả-phân-tích--kèm-giải-thích).
- Muốn **hiểu từng hình** → đọc [Mục 8](#8-báo-cáo-chi-tiết-biểu-đồ) (có chú thích từng biểu đồ).
- Muốn **năm sau thế nào** → đọc [Mục 7](#7-dự-báo-2026--giải-thích-cho-người-không-chuyên) (kèm giải thích đơn giản).

> **Lưu ý quan trọng:** Số liệu ở đây là **thống kê tổng hợp toàn quốc**, không phải điểm của một học sinh cụ thể. Khi TB một môn giảm, có thể do nhiều người hơn thi môn đó (kéo TB xuống), không nhất thiết do “học kém hơn toàn dân”.
"""


def section_method_plain() -> str:
    return """
---

## 5. Phương pháp & quy trình (giải thích đơn giản)

Chúng tôi xử lý file điểm thi lớn (~805 MB) theo các bước:

| Bước | Làm gì? | Ví dụ dễ hiểu |
|------|---------|----------------|
| 1. Kiểm tra | Đếm số dòng, số năm | Giống kiểm tra sổ điểm có đủ 5 năm không |
| 2. Tổng hợp | Tính TB, % điểm ≥ 8 theo năm/môn/tỉnh | Giống tính điểm TB môn Toán cả nước mỗi năm |
| 3. Dự báo | Vẽ đường xu hướng và kéo dài 1 năm | Giống nhìn 5 năm mưa nhiều/ít rồi đoán năm sau |
| 4. Vẽ hình | Tạo biểu đồ trong `outputs/figures/` | Để mắt thường nhìn thấy xu hướng |
| 5. Viết README | Gom báo cáo vào file này | Một tài liệu duy nhất, dễ đọc |

**Công cụ kỹ thuật:** Python (pandas, matplotlib). Chi tiết code nằm trong thư mục `src/`.
"""


def section_forecast_plain(forecast_rows: list[str]) -> str:
    body = "\n".join(forecast_rows) if forecast_rows else ""
    return f"""
---

## 7. Dự báo 2026 — Giải thích cho người không chuyên

### Dự báo này là gì?

Hệ thống nhìn **điểm TB 5 năm qua** của mỗi môn, vẽ một **đường thẳng xu hướng**, rồi **ước lượng năm 2026** nằm trên đường đó.

- **Không phải** đề thi hay thang điểm chính thức năm sau.
- **Không dự đoán** điểm của bạn hay của một trường cụ thể.
- Chỉ trả lời: *“Nếu xu hướng 5 năm tiếp tục tương tự, TB toàn quốc có thể quanh X điểm.”*

### Kiểm tra độ tin cậy (backtest)

Trước khi nói về 2026, mô hình thử **đoán năm {YEAR_MAX}** bằng dữ liệu các năm trước, rồi so với điểm thật — cột **MAE** cho biết lệch trung bình bao nhiêu điểm.

| Môn | Dự báo 2026 | Thực tế {YEAR_MAX} | MAE (sai số) |
|-----|-------------|-------------------|--------------|
{body}

**Cách đọc MAE:** MAE = 0,10 nghĩa là dự đoán lệch khoảng **0,1 điểm** so với thực tế; MAE = 1,0 nghĩa là lệch khoảng **1 điểm** — khi đó nên coi dự báo là **định hướng**, không phải con số chính xác.

---
"""


def section_6_intro() -> str:
    return """
---

## 6. Kết quả phân tích — Kèm giải thích

Phần này trả lời bằng **số và bảng**. Nếu bạn thấy khó, hãy đọc đoạn **Giải thích** ngay trước mỗi bảng.
"""


def explain_candidates_table() -> str:
    return """
**Giải thích mục 6.1:** Bảng cho biết **quy mô kỳ thi** mỗi năm. Số càng lớn = càng nhiều học sinh có trong dữ liệu. Con số % trong ngoặc là mức tăng so với năm liền trước.
"""


def explain_trends_table() -> str:
    return f"""
**Giải thích mục 6.2:** Mỗi dòng là **một môn học**.

- **TB đầu / TB cuối:** Điểm trung bình toàn quốc năm {YEAR_MIN} và {YEAR_MAX}.
- **Thay đổi:** TB năm {YEAR_MAX} so với {YEAR_MIN} tăng hay giảm bao nhiêu phần trăm.
- **% ≥ 8 cuối:** Năm {YEAR_MAX}, bao nhiêu phần trăm thí sinh **thi môn đó** đạt từ 8.0 trở lên.
"""


def explain_province_ranking(subject_name: str = "Toán") -> str:
    return f"""
**Giải thích mục 6.3–6.4:** Xếp hạng **63 tỉnh/thành** theo điểm TB môn **{subject_name}** năm {YEAR_MAX}.

- **Top 10:** Nơi có điểm TB cao hơn trung bình cả nước.
- **Bottom 10:** Nơi có điểm TB thấp hơn.
- Số trong ngoặc *(n=…)* = có bao nhiêu thí sinh **đã thi môn đó** ở tỉnh đó — mẫu càng nhỏ thì số liệu càng dễ dao động.
"""
