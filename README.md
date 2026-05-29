# THPTQG Trends — Phân tích & dự báo điểm thi THPT quốc gia

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/2274802010922/thptqg-trends/blob/main/colab/THPTQG_Colab.ipynb)

**Repository:** [github.com/2274802010922/thptqg-trends](https://github.com/2274802010922/thptqg-trends)

Đồ án phân tích dữ liệu điểm **Kỳ thi tốt nghiệp THPT quốc gia** trong giai đoạn **2021–2025**, mô tả xu hướng theo thời gian / môn học / tỉnh thành, và dự báo chỉ số tổng hợp cho năm tiếp theo bằng mô hình hồi quy tuyến tính trên chuỗi thời gian.

---

## Mục lục

1. [Tóm tắt](#1-tóm-tắt)
2. [Mục tiêu & phạm vi](#2-mục-tiêu--phạm-vi)
3. [Nguồn dữ liệu](#3-nguồn-dữ-liệu)
4. [Mô tả dữ liệu](#4-mô-tả-dữ-liệu)
5. [Phương pháp & quy trình xử lý](#5-phương-pháp--quy-trình-xử-lý)
6. [Kết quả phân tích](#6-kết-quả-phân-tích)
7. [Dự báo 2026](#7-dự-báo-2026)
8. [Biểu đồ minh họa](#8-biểu-đồ-minh-họa)
9. [Cấu trúc repository](#9-cấu-trúc-repository)
10. [Hướng dẫn chạy](#10-hướng-dẫn-chạy)
11. [Kết quả đầu ra (outputs)](#11-kết-quả-đầu-ra-outputs)
12. [Giới hạn & lưu ý](#12-giới-hạn--lưu-ý)

---

## 1. Tóm tắt

| Hạng mục | Giá trị |
|----------|---------|
| **Phạm vi thời gian** | 2021 – 2025 (5 năm) |
| **Tổng số bản ghi phân tích** | **5.197.946** thí sinh |
| **Số tỉnh/thành** | 63 (mã `Tinh` 1–63) |
| **Số cột dữ liệu gốc** | 31 |
| **Dung lượng file CSV** | ~805 MB |
| **Mô hình dự báo** | Hồi quy tuyến tính `điểm TB ~ năm`, có backtest năm cuối |

**Phát hiện nổi bật (2021 → 2025):**

- Số thí sinh tăng đều từ **987.704** (2021) lên **1.131.136** (2025), tương đương **+14,5%** trong 5 năm.
- **Ngữ văn** duy trì điểm TB cao và ổn định (~6,73 → ~6,95).
- **Toán** và **Ngoại ngữ** có xu hướng giảm mạnh điểm TB tổng hợp trong giai đoạn này (cần đọc kèm giải thích ở [mục 12](#12-giới-hạn--lưu-ý) — liên quan cách tính và tập thí sinh thi môn).
- Chênh lệch điểm Toán giữa tỉnh: cao nhất **Ninh Bình** (~5,64), thấp nhất **Tuyên Quang** (~3,45) năm 2025.

---

## 2. Mục tiêu & phạm vi

### Mục tiêu

| # | Mục tiêu | Mô tả |
|---|----------|--------|
| 1 | **Khám phá dữ liệu (EDA)** | Thống kê mô tả điểm theo năm, môn, tỉnh |
| 2 | **Phân tích xu hướng** | So sánh biến động 2021–2025 (% thay đổi, tỷ lệ điểm ≥ 8) |
| 3 | **Dự báo** | Dự báo điểm TB toàn quốc năm 2026 trên các môn chính |
| 4 | **Trực quan hóa** | Biểu đồ xu hướng, heatmap tỉnh, dự báo |
| 5 | **Tái lập được** | Pipeline một lệnh / một notebook Colab |

### Phạm vi

- ✅ Phân tích **tổng hợp** (toàn quốc, theo tỉnh, theo môn).
- ✅ Dữ liệu đã **làm sạch** (`cleaned_data.csv`).
- ❌ **Không** dự đoán điểm từng cá nhân theo `SBD`.
- ❌ **Không** thu thập/scrape dữ liệu mới từ Bộ GD&ĐT.

---

## 3. Nguồn dữ liệu

File CSV **không** được commit lên GitHub (quá lớn). Tải từ Google Drive:

| | |
|---|---|
| **Link chia sẻ** | [cleaned_data.csv trên Google Drive](https://drive.google.com/file/d/1FIU_8XT4pIC261SwYtmwTDLFP2H_WAUc/view?usp=sharing) |
| **File ID** | `1FIU_8XT4pIC261SwYtmwTDLFP2H_WAUc` |
| **Tên file** | `cleaned_data.csv` |

**Local (Windows):** nếu đã có file trên máy, mặc định trỏ tới:

```text
D:\do an thuc tap\cleaned_data.csv
```

Có thể ghi đè bằng biến môi trường `THPTQG_CSV_PATH` hoặc hàm `configure()` trong Colab.

---

## 4. Mô tả dữ liệu

### Quy mô file gốc (toàn bộ 2020–2025)

| Năm | Số dòng |
|-----|---------|
| 2020 | 870.517 |
| 2021 | 987.704 |
| 2022 | 995.441 |
| 2023 | 1.022.060 |
| 2024 | 1.061.605 |
| 2025 | 1.131.136 |
| **Tổng** | **~6.068.463** |

*Pipeline mặc định lọc **2021–2025** (5 năm gần nhất trong file).*

### Các cột chính (31 cột)

| Nhóm | Cột | Ý nghĩa |
|------|-----|---------|
| Định danh | `SBD`, `SBD_New`, `Nam`, `Tinh` | Số báo danh, năm thi, mã tỉnh |
| Điểm môn | `Toan`, `NguVan`, `VatLy`, `HoaHoc`, `SinhHoc`, `LichSu`, `DiaLy`, `GDCD`, `NgoaiNgu`, … | Điểm từng môn (0.0 = không thi) |
| Tổ hợp / khối | `KhoiA`, `KhoiB`, `KhoiC`, `KhoiD`, `KHTN`, `KHXH`, `TongDiem`, … | Điểm tổ hợp tuyển sinh |
| Ngoại ngữ | `MaMonNgoaiNgu` | Mã môn ngoại ngữ |

### Giả định làm sạch

- Giá trị **`0.0`** trên cột môn được coi là **không tham gia thi môn đó** (loại khỏi mean/median khi thống kê).
- Mã tỉnh `Tinh` (1–63) được map sang tên đầy đủ trong `data/provinces.csv`.

---

## 5. Phương pháp & quy trình xử lý

```text
CSV (805 MB)
    │
    ▼
[1] Validate ── đếm dòng theo năm, kiểm tra schema
    │
    ▼
[2] Aggregate ── groupby (Năm × Môn), (Năm × Tỉnh × Môn)
    │              → mean, median, std, count, % ≥ 8
    ▼
[3] Forecast ── hồi quy tuyến tính trên chuỗi 5 năm
    │            backtest: train 2021–2024 → test 2025
    ▼
[4] Visualize ── biểu đồ xu hướng, heatmap, dự báo
    │
    ▼
[5] Report ── BAO_CAO.md + README (tài liệu này)
```

### Kỹ thuật

| Bước | Công cụ |
|------|---------|
| Đọc file lớn | `pandas` với `chunksize=500_000` |
| Thống kê | `groupby`, hàm `_subject_stats()` |
| Dự báo | `sklearn.linear_model.LinearRegression` |
| Biểu đồ | `matplotlib`, `seaborn` |
| Font tiếng Việt (Colab) | Noto Sans (`src/display.py`) |

### Công thức thống kê môn

Với mỗi (năm, môn):

- **count**: số thí sinh có điểm > 0  
- **mean / median / std**: trên tập điểm > 0  
- **pct_ge_8**: % thí sinh đạt ≥ 8.0  

---

## 6. Kết quả phân tích

### 6.1. Số thí sinh theo năm (2021–2025)

| Năm | Số thí sinh | Tăng so với năm trước |
|-----|-------------|------------------------|
| 2021 | 987.704 | — |
| 2022 | 995.441 | +0,8% |
| 2023 | 1.022.060 | +2,7% |
| 2024 | 1.061.605 | +3,9% |
| 2025 | 1.131.136 | +6,6% |

### 6.2. Xu hướng điểm trung bình (2021 → 2025)

| Môn | TB 2021 | TB 2025 | Thay đổi | Tỷ lệ ≥ 8 (2025) |
|-----|---------|---------|----------|------------------|
| Toán | 7,02 | 4,18 | −40,5% | 1,7% |
| Ngữ văn | 6,73 | 6,95 | +3,3% | 22,5% |
| Ngoại ngữ | 6,69 | 4,92 | −26,4% | 2,7% |
| Vật lý | 6,57 | 6,49 | −1,3% | 19,3% |
| Hóa học | 6,36 | 5,51 | −13,3% | 11,2% |
| Sinh học | 5,24 | 5,45 | +4,0% | 5,2% |
| Lịch sử | 4,92 | 6,46 | +31,3% | 20,6% |
| Địa lý | 6,83 | 6,56 | −3,9% | 24,2% |
| GDCD | 8,23 | 8,02 | −2,6% | 60,9% |
| Tin học | 7,51 | 6,34 | −15,6% | 15,6% |

*Bảng đầy đủ 13 môn: `outputs/tables/trends_summary.csv` và `reports/BAO_CAO.md`.*

### 6.3. Top / Bottom tỉnh — Điểm Toán 2025

**Top 10**

| # | Tỉnh | Điểm TB | Số thí sinh thi Toán |
|---|------|---------|----------------------|
| 1 | Ninh Bình | 5,64 | 23.209 |
| 2 | Hà Nội | 5,56 | 62.373 |
| 3 | Phú Thọ | 5,45 | 16.201 |
| 4 | Lâm Đồng | 5,40 | 16.713 |
| 5 | Nghệ An | 5,26 | 7.686 |
| 6 | Hà Giang | 5,25 | 96.488 |
| 7 | Cao Bằng | 5,20 | 28.752 |
| 8 | Hải Dương | 5,19 | 19.308 |
| 9 | Bắc Kạn | 5,17 | 13.964 |
| 10 | Thanh Hóa | 5,17 | 23.789 |

**Bottom 10**

| # | Tỉnh | Điểm TB | Số thí sinh thi Toán |
|---|------|---------|----------------------|
| 1 | Tuyên Quang | 3,45 | 7.047 |
| 2 | Quảng Ninh | 3,63 | 12.380 |
| 3 | Lào Cai | 3,71 | 4.826 |
| 4 | Hòa Bình | 3,78 | 3.065 |
| 5 | Bạc Liêu | 3,81 | 6.843 |
| 6 | Hà Nam | 3,91 | 10.488 |
| 7 | Yên Bái | 3,94 | 9.517 |
| 8 | Lạng Sơn | 4,00 | 9.048 |
| 9 | Kiên Giang | 4,03 | 10.030 |
| 10 | Điện Biên | 4,07 | 4.178 |

---

## 7. Dự báo 2026

Mô hình: **hồi quy tuyến tính** trên điểm TB toàn quốc theo năm.  
Backtest: huấn luyện 2021–2024, kiểm tra trên 2025 (MAE = sai số tuyệt đối trung bình).

| Môn | Năm dự báo | Điểm TB dự kiến | Thực tế 2025 | MAE backtest |
|-----|------------|-----------------|--------------|--------------|
| Toán | 2026 | **4,922** | 5,564 | 0,794 |
| Ngữ văn | 2026 | **7,485** | 7,833 | 0,336 |
| Ngoại ngữ | 2026 | **5,373** | 6,132 | 0,598 |
| Vật lý | 2026 | **6,956** | 7,400 | 0,720 |
| Hóa học | 2026 | **6,165** | 6,692 | 0,041 |
| Sinh học | 2026 | **6,411** | 6,843 | 0,169 |

**Diễn giải:** Dự báo mang tính **xu hướng học thuật**, giả định cơ chế thi không đổi. MAE thấp (vd. Hóa học ~0,04) không có nghĩa mô hình “chuẩn xác tuyệt đối” — chỉ phản ánh chuỗi 5 điểm khá ổn định.

Chi tiết chuỗi actual/forecast: `outputs/tables/forecast_series.csv`.

---

## 8. Biểu đồ minh họa

Các biểu đồ được tạo tự động trong `outputs/figures/`:

| File | Nội dung |
|------|----------|
| `candidates_by_year.png` | Số thí sinh theo năm |
| `pct_ge_8_by_year.png` | Tỷ lệ điểm ≥ 8 theo môn |
| `mean_by_year_Toan.png` | Xu hướng điểm TB Toán |
| `mean_by_year_NguVan.png` | Xu hướng điểm TB Ngữ văn |
| `mean_by_year_NgoaiNgu.png` | Xu hướng Ngoại ngữ |
| `mean_by_year_VatLy.png` | Xu hướng Vật lý |
| `mean_by_year_HoaHoc.png` | Xu hướng Hóa học |
| `mean_by_year_SinhHoc.png` | Xu hướng Sinh học |
| `heatmap_Toan_2025.png` | Phân bố điểm Toán theo mã tỉnh (2025) |
| `forecast_Toan.png` | Dự báo Toán (actual + forecast) |
| `forecast_NguVan.png` | Dự báo Ngữ văn |
| `forecast_NgoaiNgu.png` | Dự báo Ngoại ngữ |

### Ví dụ

![Số thí sinh theo năm](outputs/figures/candidates_by_year.png)

![Xu hướng điểm TB Toán](outputs/figures/mean_by_year_Toan.png)

![Dự báo Toán](outputs/figures/forecast_Toan.png)

---

## 9. Cấu trúc repository

```text
thptqg-trends/
├── README.md                 ← Tài liệu tổng hợp (file này)
├── requirements.txt          ← Thư viện Python
├── run.ps1 / run.bat         ← Chạy pipeline trên Windows
├── colab/
│   ├── THPTQG_Colab.ipynb    ← Notebook Google Colab (khuyên dùng)
│   └── README.md
├── data/
│   └── provinces.csv         ← Map 63 mã tỉnh → tên có dấu
├── src/
│   ├── config.py             ← Đường dẫn CSV, phạm vi năm
│   ├── load_data.py          ← Đọc CSV theo chunk
│   ├── aggregates.py         ← Tổng hợp thống kê
│   ├── forecast.py           ← Dự báo & backtest
│   ├── plots.py              ← Vẽ biểu đồ
│   ├── report.py             ← Sinh BAO_CAO.md
│   ├── labels.py             ← Tên môn/tỉnh tiếng Việt
│   └── display.py            ← Format số & font Colab
├── scripts/
│   ├── run_all.py            ← Pipeline end-to-end
│   ├── run_validate.py       ← Kiểm tra nhanh
│   └── run_pipeline.py       ← Alias pipeline
├── notebooks/                ← Jupyter notebooks (01–04)
├── outputs/
│   ├── tables/               ← CSV tổng hợp (public-friendly)
│   └── figures/              ← Biểu đồ PNG
└── reports/
    ├── BAO_CAO.md            ← Báo cáo tự động sau mỗi lần chạy
    └── WORKFLOW.md           ← Quy trình ngắn
```

---

## 10. Hướng dẫn chạy

### Cách 1 — Google Colab (khuyên dùng)

1. Mở notebook: [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/2274802010922/thptqg-trends/blob/main/colab/THPTQG_Colab.ipynb)
2. Chạy lần lượt các cell từ trên xuống.
3. Tải dataset từ [Google Drive](https://drive.google.com/file/d/1FIU_8XT4pIC261SwYtmwTDLFP2H_WAUc/view?usp=sharing) hoặc mount Drive / upload file.
4. Cell cuối zip `outputs/` + `reports/` để tải về máy.

**Thời gian ước tính:** 5–15 phút (tùy tải file & RAM Colab).

### Cách 2 — Windows (local)

```powershell
git clone https://github.com/2274802010922/thptqg-trends.git
cd thptqg-trends

# Đặt cleaned_data.csv (hoặc sửa src/config.py)

.\run.ps1
# hoặc double-click run.bat
```

Lần đầu tự tạo `.venv` và cài `requirements.txt`.

### Cách 3 — Thủ công

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python scripts/run_all.py
```

### Tùy chỉnh phạm vi năm

Sửa trong `src/config.py`:

```python
YEAR_MIN = 2021
YEAR_MAX = 2025
```

Hoặc trong Colab:

```python
from src.config import configure
configure(csv_path="/content/cleaned_data.csv", year_min=2021, year_max=2025)
```

---

## 11. Kết quả đầu ra (outputs)

Sau mỗi lần chạy pipeline:

| File | Mô tả |
|------|--------|
| `outputs/tables/by_year_subject.csv` | Thống kê theo (năm × môn) |
| `outputs/tables/by_year_province_subject.csv` | Theo (năm × tỉnh × môn) |
| `outputs/tables/by_year_province_subject_named.csv` | Có thêm tên tỉnh |
| `outputs/tables/candidates_by_year.csv` | Số thí sinh/năm |
| `outputs/tables/trends_summary.csv` | Tóm tắt xu hướng |
| `outputs/tables/forecast_next_year.csv` | Dự báo năm tiếp theo |
| `outputs/tables/forecast_series.csv` | Chuỗi actual + forecast |
| `outputs/tables/data_profile.json` | Metadata lần chạy |
| `reports/BAO_CAO.md` | Báo cáo Markdown tự động |
| `outputs/figures/*.png` | 12 biểu đồ |

---

## 12. Giới hạn & lưu ý

### Giới hạn phương pháp

- **Dự báo đơn giản:** Chỉ dùng hồi quy tuyến tính trên 5 điểm thời gian — phù hợp đồ án, không thay thế mô hình chuyên sâu (ARIMA, Prophet, …).
- **Giả định ổn định:** Cơ chế thi, cách chấm, cấu trúc đề không thay đổi.
- **Điểm 0.0:** Coi là không thi → mean/median chỉ tính trên người thi môn đó; so sánh giữa các môn/năm cần cẩn trọng khi tỷ lệ thi thay đổi.

### Giải thích xu hướng “giảm mạnh” một số môn

Điểm TB Toán/Ngoại ngữ giảm mạnh trong bảng xu hướng có thể phản ánh:

- Thay đổi **cơ cấu thí sinh** thi môn (count thay đổi theo năm).
- Cách xử lý **0.0** và dữ liệu cleaned, không nhất thiết “đề khó hơn” tuyệt đối.
- Cần đối chiếu thêm phân phối điểm và số lượng thí sinh thi môn (`count` trong bảng aggregate).

### Quyền riêng tư & công bố

- Repo công bố **thống kê tổng hợp**; file gốc chứa `SBD` nên không public từng dòng nếu không cần thiết.
- Kết quả dự báo mang tính **minh họa học thuật**, không dùng cho tuyển sinh hay ra quyết định chính thức.

### Yêu cầu hệ thống

| Môi trường | RAM khuyến nghị |
|------------|-----------------|
| Colab free | Có thể cần session RAM cao với file 805 MB |
| Windows local | ≥ 8 GB RAM |

---

## Tham chiếu nhanh

| Tài nguyên | Link |
|------------|------|
| Repository | https://github.com/2274802010922/thptqg-trends |
| Dataset (Drive) | https://drive.google.com/file/d/1FIU_8XT4pIC261SwYtmwTDLFP2H_WAUc/view?usp=sharing |
| Colab notebook | https://colab.research.google.com/github/2274802010922/thptqg-trends/blob/main/colab/THPTQG_Colab.ipynb |

---

*Cập nhật README: báo cáo tổng hợp đồ án THPTQG Trends — pipeline `scripts/run_all.py` / Colab.*
