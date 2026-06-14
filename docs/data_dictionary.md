# Data Dictionary

Tài liệu này mô tả các cột chính trong `cleaned_data.csv`.

## Cột Định Danh

| Cột | Ý nghĩa | Ghi chú |
|---|---|---|
| `SBD` | Số báo danh gốc | Không public từng dòng trong báo cáo |
| `SBD_New` | Mã số báo danh đã chuẩn hóa | Dùng nội bộ khi làm sạch |
| `Nam` | Năm thi | Raw có 2020-2025, đồ án dùng 2021-2025 |
| `Tinh` | Mã tỉnh/thành | Tra tên ở `data/provinces.csv`; vùng miền ở `data/province_regions.csv` |

## Cột Điểm Từng Môn

| Cột | Môn |
|---|---|
| `Toan` | Toán |
| `NguVan` | Ngữ văn |
| `VatLy` | Vật lý |
| `HoaHoc` | Hóa học |
| `SinhHoc` | Sinh học |
| `LichSu` | Lịch sử |
| `DiaLy` | Địa lý |
| `GDCD` | Giáo dục công dân |
| `NgoaiNgu` | Ngoại ngữ |
| `KinhTePhapLuat` | Kinh tế & Pháp luật |
| `TinHoc` | Tin học |
| `CongNgheCongNghiep` | Công nghệ công nghiệp |
| `CongNgheNongNghiep` | Công nghệ nông nghiệp |

Quy ước quan trọng: giá trị `0.0` ở cột điểm môn được xem là thí sinh **không thi môn đó**. Khi tính điểm trung bình, độ lệch chuẩn, tỷ lệ điểm cao, pipeline chỉ dùng các điểm `> 0`.

## Cột Tổ Hợp/Xét Tuyển

| Cột | Ý nghĩa |
|---|---|
| `TongDiem` | Tổng điểm đã tính trong dữ liệu nguồn |
| `KhoiA` | Tổng điểm khối A |
| `KhoiA1` | Tổng điểm khối A1 |
| `KhoiB` | Tổng điểm khối B |
| `KhoiC` | Tổng điểm khối C |
| `KhoiD` | Tổng điểm khối D |
| `KHTN` | Chỉ báo/tổng hợp nhóm khoa học tự nhiên trong dữ liệu nguồn |
| `KHXH` | Chỉ báo/tổng hợp nhóm khoa học xã hội trong dữ liệu nguồn |
| `TongDiemKHTN` | Tổng điểm nhóm KHTN |
| `TongDiemKHXH` | Tổng điểm nhóm KHXH |
| `KhoiA02` | Tổng điểm tổ hợp A02 |
| `KhoiC01` | Tổng điểm tổ hợp C01 |
| `KhoiD07` | Tổng điểm tổ hợp D07 |
| `MaMonNgoaiNgu` | Mã môn ngoại ngữ |

Ở phiên bản DA nâng cao, các cột tổ hợp được dùng để phân tích xu hướng điểm theo khối/tổ hợp và tỷ lệ nhóm điểm cao/thấp. Pipeline chỉ dùng giá trị `> 0` khi tính thống kê tổ hợp.

## Bảng Output Nâng Cao

| File | Nội dung |
|---|---|
| `data_quality_summary.csv` | Tóm tắt số dòng, tỉnh, ô thiếu, ô 0.0, điểm ngoài khoảng |
| `missing_by_subject_year.csv` | Missing/zero/invalid/valid theo năm và môn |
| `score_histogram_by_year_subject.csv` | Histogram dạng bảng theo điểm, năm, môn |
| `score_distribution_by_year_subject.csv` | Mean, std, min, P10, P25, median, P75, P90, max, IQR |
| `score_bands_by_year_subject.csv` | Dải điểm `<5`, `5-6.5`, `6.5-8`, `>=8` |
| `yearly_change_by_subject.csv` | Biến động year-over-year của mean, median, nhóm điểm thấp/cao |
| `by_region_subject_year.csv` | Thống kê theo vùng, năm, môn |
| `province_anomalies.csv` | Tỉnh/năm/môn lệch mạnh so với trung bình quốc gia |
| `province_volatility.csv` | Tỉnh có biến động điểm mạnh giữa các năm |
| `subject_correlation_by_year.csv` | Tương quan điểm giữa các cặp môn theo năm |
| `combination_scores_by_year.csv` | Thống kê các tổ hợp/khối điểm |
| `forecast_reliability.csv` | Đánh giá độ tin cậy dự báo dựa trên backtest và độ rộng khoảng dự báo |
