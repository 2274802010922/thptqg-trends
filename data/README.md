# Dữ Liệu Đầu Vào

Raw dataset không được lưu trực tiếp trong GitHub vì file CSV lớn hơn giới hạn hợp lý của repository.

## Raw Dataset

- File: `cleaned_data.csv`
- Google Drive: https://drive.google.com/file/d/1FIU_8XT4pIC261SwYtmwTDLFP2H_WAUc/view
- Google Drive file ID: `1FIU_8XT4pIC261SwYtmwTDLFP2H_WAUc`
- Dung lượng: `843,891,415` bytes
- SHA256: `E11EC167D7073192F719C5A09B2A91556631CA897E998467C2BAF8CA485E86B0`
- Tổng số dòng raw: `6,068,463`

## Số Dòng Theo Năm

| Năm | Số dòng |
|---:|---:|
| 2020 | 870,517 |
| 2021 | 987,704 |
| 2022 | 995,441 |
| 2023 | 1,022,060 |
| 2024 | 1,061,605 |
| 2025 | 1,131,136 |

Đồ án dùng phạm vi **2021-2025** để đúng yêu cầu phân tích 5 năm gần nhất. Năm 2020 vẫn có trong raw CSV, nhưng không được đưa vào các bảng/kết luận chính.

## Cách Đặt Đường Dẫn

Windows PowerShell:

```powershell
$env:THPTQG_CSV_PATH="D:\do an thuc tap\cleaned_data.csv"
python scripts/run_all.py
```

Google Colab:

```python
from src.config import configure
configure(csv_path="/content/drive/MyDrive/do an thuc tap/cleaned_data.csv", year_min=2021, year_max=2025)
```

## Quy Ước Tiền Xử Lý

- Mỗi dòng tương ứng một thí sinh trong một năm thi.
- `Nam` là năm thi.
- `Tinh` là mã tỉnh/thành, ánh xạ tên trong `data/provinces.csv`.
- `data/province_regions.csv` ánh xạ tỉnh/thành sang vùng để phân tích vùng miền.
- Điểm `0.0` ở một môn được xem là **không thi môn đó** và không đưa vào mẫu tính trung bình môn.
- Các kết quả public trong `outputs/` là thống kê tổng hợp, không công bố từng dòng `SBD`.

## Output Phân Tích Chính

Pipeline sinh thêm các bảng phục vụ Data Analysis trong `outputs/tables/`:

- `data_quality_summary.csv`, `missing_by_subject_year.csv`: kiểm tra chất lượng dữ liệu.
- `score_distribution_by_year_subject.csv`, `score_bands_by_year_subject.csv`: median, percentile và dải điểm.
- `yearly_change_by_subject.csv`: biến động theo năm.
- `by_region_subject_year.csv`: so sánh theo vùng.
- `province_anomalies.csv`, `province_volatility.csv`: tỉnh/năm lệch bất thường.
- `subject_correlation_by_year.csv`, `combination_scores_by_year.csv`: tương quan môn học và tổ hợp điểm.
- `forecast_reliability.csv`: nhãn độ tin cậy cho dự báo.
