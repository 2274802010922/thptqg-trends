# THPTQG Trends — Phân tích & dự báo điểm thi THPT quốc gia

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/2274802010922/thptqg-trends/blob/main/colab/THPTQG_Colab.ipynb)

**Repository:** [github.com/2274802010922/thptqg-trends](https://github.com/2274802010922/thptqg-trends)

Đồ án phân tích dữ liệu điểm **Kỳ thi tốt nghiệp THPT quốc gia** (2021–2025). **Toàn bộ báo cáo nằm trong file README này.**

**Cập nhật lần chạy pipeline gần nhất:** 29/05/2026 

---

## Mục lục

1. [Tóm tắt](#1-tóm-tắt)
2. [Mục tiêu & phạm vi](#2-mục-tiêu--phạm-vi)
3. [Nguồn dữ liệu](#3-nguồn-dữ-liệu)
4. [Mô tả dữ liệu](#4-mô-tả-dữ-liệu)
5. [Phương pháp & quy trình](#5-phương-pháp--quy-trình)
6. [Kết quả phân tích](#6-kết-quả-phân-tích)
7. [Dự báo 2026](#7-dự-báo-2026)
8. [Báo cáo chi tiết biểu đồ](#8-báo-cáo-chi-tiết-biểu-đồ)
9. [Cấu trúc repository](#9-cấu-trúc-repository)
10. [Hướng dẫn chạy](#10-hướng-dẫn-chạy)
11. [Kết quả đầu ra (outputs)](#11-kết-quả-đầu-ra-outputs)
12. [Giới hạn & lưu ý](#12-giới-hạn--lưu-ý)

---

## 1. Tóm tắt

| Hạng mục | Giá trị |
|----------|---------|
| Phạm vi | 2021 – 2025 |
| Tổng thí sinh | **5.197.946** |
| Mô hình dự báo | Hồi quy tuyến tính + backtest |

- Số thí sinh tăng **+14.5%** (987.704 → 1.131.136).
- Môn tăng mạnh nhất: **Lịch sử** (+31.1%). Môn giảm mạnh nhất: **Toán** (-27.7%).

---

## 2. Mục tiêu & phạm vi

| # | Mục tiêu |
|---|----------|
| 1 | Khám phá dữ liệu (EDA) theo năm, môn, tỉnh |
| 2 | Phân tích xu hướng 2021–2025 |
| 3 | Dự báo chỉ số tổng hợp năm tiếp theo |
| 4 | Trực quan hóa & báo cáo trong README |

- ✅ Thống kê tổng hợp, có thể public
- ❌ Không dự đoán điểm từng `SBD`

---

## 3. Nguồn dữ liệu

| | |
|---|---|
| **Google Drive** | [cleaned_data.csv](https://drive.google.com/file/d/1FIU_8XT4pIC261SwYtmwTDLFP2H_WAUc/view?usp=sharing) |
| **File ID** | `1FIU_8XT4pIC261SwYtmwTDLFP2H_WAUc` |
| **Local (Windows)** | `D:\do an thuc tap\cleaned_data.csv` |

CSV ~805 MB **không** commit GitHub.

---

## 4. Mô tả dữ liệu

- **31 cột:** `SBD`, `Nam`, `Tinh`, điểm môn, tổ hợp khối…
- **63 mã tỉnh** (`data/provinces.csv`)
- **0.0** = không thi môn đó

---

## 5. Phương pháp & quy trình

```text
CSV → Validate → Aggregate → Forecast → Charts → README.md
```

| Bước | Công cụ |
|------|---------|
| Đọc file lớn | pandas chunksize 500k |
| Dự báo | LinearRegression |
| Biểu đồ | matplotlib, seaborn |

---

## 6. Kết quả phân tích

### 6.1. Số thí sinh theo năm

| Năm | Số thí sinh |
|-----|-------------|
| 2021 | 987.704 |
| 2022 | 995.441 (+0.8%) |
| 2023 | 1.022.060 (+2.7%) |
| 2024 | 1.061.605 (+3.9%) |
| 2025 | 1.131.136 (+6.5%) |

### 6.2. Xu hướng điểm TB (2021 → 2025)

| Môn | TB đầu | TB cuối | Thay đổi | % ≥ 8 cuối |
|-----|--------|---------|----------|------------|
| Công nghệ công nghiệp | 5,79 | 5,79 | +0.0% | 11.2% |
| Công nghệ nông nghiệp | 7,72 | 7,72 | +0.0% | 48.8% |
| GDCD | 8,37 | 8,16 | -2.6% | 65.8% |
| Hóa học | 6,63 | 6,06 | -8.5% | 19.3% |
| Kinh tế & Pháp luật | 7,69 | 7,69 | +0.0% | 49.1% |
| Lịch sử | 4,97 | 6,52 | +31.1% | 23.0% |
| Ngoại ngữ | 5,85 | 5,41 | -7.6% | 6.0% |
| Ngữ văn | 6,47 | 7,00 | +8.2% | 26.7% |
| Sinh học | 5,52 | 5,78 | +4.8% | 10.8% |
| Tin học | 6,78 | 6,78 | +0.0% | 24.8% |
| Toán | 6,61 | 4,78 | -27.7% | 5.5% |
| Vật lý | 6,57 | 6,99 | +6.4% | 30.8% |
| Địa lý | 6,96 | 6,63 | -4.7% | 26.7% |

### 6.3. Top 10 tỉnh — Toán 2025

1. **Ninh Bình** — 5,64 (23.209 thí sinh)
2. **Phú Thọ** — 5,45 (16.201 thí sinh)
3. **Lâm Đồng** — 5,40 (16.713 thí sinh)
4. **Hà Nội** — 5,28 (120.277 thí sinh)
5. **Hà Giang** — 5,25 (96.488 thí sinh)
6. **Cao Bằng** — 5,20 (28.752 thí sinh)
7. **Hải Dương** — 5,19 (19.308 thí sinh)
8. **Bắc Kạn** — 5,17 (13.964 thí sinh)
9. **Thanh Hóa** — 5,17 (23.789 thí sinh)
10. **Nam Định** — 5,17 (10.172 thí sinh)

### 6.4. Bottom 10 tỉnh — Toán 2025

1. **Tuyên Quang** — 3,45 (7.047 thí sinh)
2. **Quảng Ninh** — 3,63 (12.380 thí sinh)
3. **Lào Cai** — 3,71 (4.826 thí sinh)
4. **Hòa Bình** — 3,78 (3.065 thí sinh)
5. **Bạc Liêu** — 3,81 (6.843 thí sinh)
6. **Hà Nam** — 3,91 (10.488 thí sinh)
7. **Yên Bái** — 3,94 (9.517 thí sinh)
8. **Lạng Sơn** — 4,00 (9.048 thí sinh)
9. **Kiên Giang** — 4,03 (10.030 thí sinh)
10. **Điện Biên** — 4,07 (4.178 thí sinh)
---

## 7. Dự báo 2026

Hồi quy tuyến tính; backtest trên năm 2025.

| Môn | Dự báo 2026 | Thực tế 2025 | MAE |
|-----|-------------|--------------|-----|
| Toán | 5,008 | 4,783 | 1,4826 |
| Ngữ văn | 7,350 | 7,002 | 0,4232 |
| Ngoại ngữ | 5,322 | 5,405 | 0,0773 |
| Vật lý | 6,937 | 6,985 | 0,3144 |
| Hóa học | 6,219 | 6,065 | 0,6732 |
| Sinh học | 6,336 | 5,778 | 0,9461 |
## 8. Báo cáo chi tiết biểu đồ

Phần này trình bày **tất cả biểu đồ** và nhận xét theo từng môn.

### 8.1. Tổng quan

#### Số thí sinh theo năm

![Số thí sinh theo năm](outputs/figures/candidates_by_year.png)

#### Tỷ lệ điểm ≥ 8 — tất cả môn

![Tỷ lệ điểm >= 8](outputs/figures/pct_ge_8_by_year.png)

### 8.2. Xu hướng điểm TB — từng môn

#### Công nghệ công nghiệp

- TB 2021: **5,79** → TB 2025: **5,79** (+0.0%)
- Tỷ lệ ≥ 8 năm 2025: **11.2%**
- Xu hướng **tương đối ổn định** (+0.0% TB 2021→2025).

![Công nghệ công nghiệp](outputs/figures/mean_by_year_CongNgheCongNghiep.png)

#### Công nghệ nông nghiệp

- TB 2021: **7,72** → TB 2025: **7,72** (+0.0%)
- Tỷ lệ ≥ 8 năm 2025: **48.8%**
- Xu hướng **tương đối ổn định** (+0.0% TB 2021→2025).

![Công nghệ nông nghiệp](outputs/figures/mean_by_year_CongNgheNongNghiep.png)

#### GDCD

- TB 2021: **8,37** → TB 2025: **8,16** (-2.6%)
- Tỷ lệ ≥ 8 năm 2025: **65.8%**
- Xu hướng **tương đối ổn định** (-2.6% TB 2021→2025).

![GDCD](outputs/figures/mean_by_year_GDCD.png)

#### Hóa học

- TB 2021: **6,63** → TB 2025: **6,06** (-8.5%)
- Tỷ lệ ≥ 8 năm 2025: **19.3%**
- Xu hướng **giảm** rõ (-8.5% TB 2021→2025).

![Hóa học](outputs/figures/mean_by_year_HoaHoc.png)

#### Kinh tế & Pháp luật

- TB 2021: **7,69** → TB 2025: **7,69** (+0.0%)
- Tỷ lệ ≥ 8 năm 2025: **49.1%**
- Xu hướng **tương đối ổn định** (+0.0% TB 2021→2025).

![Kinh tế & Pháp luật](outputs/figures/mean_by_year_KinhTePhapLuat.png)

#### Lịch sử

- TB 2021: **4,97** → TB 2025: **6,52** (+31.1%)
- Tỷ lệ ≥ 8 năm 2025: **23.0%**
- Xu hướng **tăng** rõ (+31.1% TB 2021→2025).

![Lịch sử](outputs/figures/mean_by_year_LichSu.png)

#### Ngoại ngữ

- TB 2021: **5,85** → TB 2025: **5,41** (-7.6%)
- Tỷ lệ ≥ 8 năm 2025: **6.0%**
- Xu hướng **giảm** rõ (-7.6% TB 2021→2025).

![Ngoại ngữ](outputs/figures/mean_by_year_NgoaiNgu.png)

#### Ngữ văn

- TB 2021: **6,47** → TB 2025: **7,00** (+8.2%)
- Tỷ lệ ≥ 8 năm 2025: **26.7%**
- Xu hướng **tăng** rõ (+8.2% TB 2021→2025).

![Ngữ văn](outputs/figures/mean_by_year_NguVan.png)

#### Sinh học

- TB 2021: **5,52** → TB 2025: **5,78** (+4.8%)
- Tỷ lệ ≥ 8 năm 2025: **10.8%**
- Xu hướng **tương đối ổn định** (+4.8% TB 2021→2025).

![Sinh học](outputs/figures/mean_by_year_SinhHoc.png)

#### Tin học

- TB 2021: **6,78** → TB 2025: **6,78** (+0.0%)
- Tỷ lệ ≥ 8 năm 2025: **24.8%**
- Xu hướng **tương đối ổn định** (+0.0% TB 2021→2025).

![Tin học](outputs/figures/mean_by_year_TinHoc.png)

#### Toán

- TB 2021: **6,61** → TB 2025: **4,78** (-27.7%)
- Tỷ lệ ≥ 8 năm 2025: **5.5%**
- Xu hướng **giảm** rõ (-27.7% TB 2021→2025).

![Toán](outputs/figures/mean_by_year_Toan.png)

#### Vật lý

- TB 2021: **6,57** → TB 2025: **6,99** (+6.4%)
- Tỷ lệ ≥ 8 năm 2025: **30.8%**
- Xu hướng **tăng** rõ (+6.4% TB 2021→2025).

![Vật lý](outputs/figures/mean_by_year_VatLy.png)

#### Địa lý

- TB 2021: **6,96** → TB 2025: **6,63** (-4.7%)
- Tỷ lệ ≥ 8 năm 2025: **26.7%**
- Xu hướng **tương đối ổn định** (-4.7% TB 2021→2025).

![Địa lý](outputs/figures/mean_by_year_DiaLy.png)

### 8.3. Heatmap theo tỉnh (2025)

#### Hóa học — phân bố 63 tỉnh

![Heatmap Hóa học](outputs/figures/heatmap_HoaHoc_2025.png)

#### Ngoại ngữ — phân bố 63 tỉnh

![Heatmap Ngoại ngữ](outputs/figures/heatmap_NgoaiNgu_2025.png)

#### Ngữ văn — phân bố 63 tỉnh

![Heatmap Ngữ văn](outputs/figures/heatmap_NguVan_2025.png)

#### Sinh học — phân bố 63 tỉnh

![Heatmap Sinh học](outputs/figures/heatmap_SinhHoc_2025.png)

#### Toán — phân bố 63 tỉnh

![Heatmap Toán](outputs/figures/heatmap_Toan_2025.png)

#### Vật lý — phân bố 63 tỉnh

![Heatmap Vật lý](outputs/figures/heatmap_VatLy_2025.png)

### 8.4. Dự báo

#### Hóa học

Dự báo 2026: **6,219** điểm. Đường xanh: thực tế; đường đứt đỏ: extrapolation tuyến tính. 

![Dự báo Hóa học](outputs/figures/forecast_HoaHoc.png)

#### Ngoại ngữ

Dự báo 2026: **5,322** điểm. Đường xanh: thực tế; đường đứt đỏ: extrapolation tuyến tính. 

![Dự báo Ngoại ngữ](outputs/figures/forecast_NgoaiNgu.png)

#### Ngữ văn

Dự báo 2026: **7,350** điểm. Đường xanh: thực tế; đường đứt đỏ: extrapolation tuyến tính. 

![Dự báo Ngữ văn](outputs/figures/forecast_NguVan.png)

#### Sinh học

Dự báo 2026: **6,336** điểm. Đường xanh: thực tế; đường đứt đỏ: extrapolation tuyến tính. 

![Dự báo Sinh học](outputs/figures/forecast_SinhHoc.png)

#### Toán

Dự báo 2026: **5,008** điểm. Đường xanh: thực tế; đường đứt đỏ: extrapolation tuyến tính. 

![Dự báo Toán](outputs/figures/forecast_Toan.png)

#### Vật lý

Dự báo 2026: **6,937** điểm. Đường xanh: thực tế; đường đứt đỏ: extrapolation tuyến tính. 

![Dự báo Vật lý](outputs/figures/forecast_VatLy.png)


---

## 9. Cấu trúc repository

```text
thptqg-trends/
├── README.md              ← Báo cáo duy nhất (file này)
├── run.ps1 / run.bat
├── colab/THPTQG_Colab.ipynb
├── data/provinces.csv
├── src/                   ← Pipeline Python
├── scripts/run_all.py
├── outputs/tables/        ← CSV tổng hợp
└── outputs/figures/       ← Biểu đồ PNG
```

---

## 10. Hướng dẫn chạy

### Google Colab

1. Mở [THPTQG_Colab.ipynb](https://colab.research.google.com/github/2274802010922/thptqg-trends/blob/main/colab/THPTQG_Colab.ipynb)
2. Chạy lần lượt các cell
3. Tải dataset từ [Google Drive](https://drive.google.com/file/d/1FIU_8XT4pIC261SwYtmwTDLFP2H_WAUc/view?usp=sharing)
4. Cell cuối: zip `outputs/` + tải về

### Windows

```powershell
git clone https://github.com/2274802010922/thptqg-trends.git
cd thptqg-trends
.\run.ps1
```

Pipeline: `python scripts/run_all.py` → cập nhật **README.md** + outputs.

---

## 11. Kết quả đầu ra (outputs)

| File | Mô tả |
|------|--------|
| `README.md` | Báo cáo đầy đủ (tự cập nhật) |
| `outputs/tables/*.csv` | Bảng thống kê |
| `outputs/figures/*.png` | Biểu đồ |

---

## 12. Giới hạn & lưu ý

- Dự báo mang tính học thuật; giả định cơ chế thi ổn định.
- Điểm 0.0 = không thi môn → so sánh mean giữa các năm cần xem thêm `count`.
- Không public từng dòng `SBD` nếu không cần thiết.

---

*Tái tạo báo cáo: `python scripts/run_all.py`*
