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
| 3. Backtest | Giấu năm cuối, cho mô hình đoán lại, rồi đo sai số | Giống thử đề trước khi thi thật |
| 4. So sánh mô hình | Naive, trung bình trượt, hồi quy tuyến tính, san bằng mũ | Chọn cách dự báo có sai số thấp nhất từng môn |
| 5. Vẽ hình | Tạo biểu đồ trong `outputs/figures/` | Để mắt thường nhìn thấy xu hướng |
| 6. Viết báo cáo | Gom README và report học thuật | Một tài liệu GitHub + một tài liệu đồ án |

**Công cụ kỹ thuật:** Python (pandas, matplotlib). Chi tiết code nằm trong thư mục `src/`.
"""


def section_forecast_plain(forecast_rows: list[str]) -> str:
    body = "\n".join(forecast_rows) if forecast_rows else ""
    return f"""
---

## 7. Dự báo 2026 — Có backtest và so sánh mô hình

### Dự báo này là gì?

Hệ thống nhìn **điểm TB 5 năm qua** của mỗi môn, thử nhiều cách dự báo đơn giản, đo sai số bằng backtest, rồi chọn mô hình có sai số thấp nhất cho từng môn.

- **Không phải** đề thi hay thang điểm chính thức năm sau.
- **Không dự đoán** điểm của bạn hay của một trường cụ thể.
- Chỉ trả lời: *“Nếu xu hướng gần đây tiếp tục tương tự, TB toàn quốc có thể quanh X điểm.”*

### Mô hình được so sánh

- **Naive:** lấy điểm trung bình năm gần nhất làm dự báo.
- **Trung bình trượt:** lấy trung bình 2 hoặc 3 năm gần nhất.
- **Hồi quy tuyến tính:** vẽ xu hướng tăng/giảm theo thời gian.
- **San bằng mũ đơn:** ưu tiên dữ liệu gần đây hơn dữ liệu cũ.

### Kiểm tra độ tin cậy (rolling backtest)

Pipeline dùng rolling backtest: ví dụ lấy 2021-2023 để đoán 2024, rồi lấy 2021-2024 để đoán 2025. Cột **MAE** cho biết mô hình lệch trung bình bao nhiêu điểm; **RMSE** phạt nặng hơn khi có lần lệch lớn.

| Môn | Mô hình chọn | Dự báo 2026 | Khoảng dự báo | MAE | RMSE |
|-----|--------------|-------------|---------------|-----|------|
{body}

**Cách đọc:** MAE = 0,10 nghĩa là dự đoán thường lệch khoảng **0,1 điểm**; MAE = 1,0 nghĩa là lệch khoảng **1 điểm**. Khoảng dự báo càng rộng thì kết quả càng nên xem là **định hướng**, không phải con số chắc chắn.

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
