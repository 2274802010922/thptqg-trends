# Báo Cáo Đồ Án: Phân Tích Và Dự Báo Điểm Thi THPTQG

**Ngày tạo:** 12/06/2026 20:05
**Phạm vi nghiên cứu:** 2021-2025
**Đường dẫn dữ liệu khi chạy:** `D:\do an thuc tap\cleaned_data.csv`

## 1. Giới Thiệu

Đề tài phân tích dữ liệu điểm thi tốt nghiệp THPTQG theo năm, môn và tỉnh/thành, sau đó dự báo xu hướng điểm trung bình của một số môn chính trong năm tiếp theo. Sản phẩm chính thức là repository GitHub; raw CSV được lưu ngoài GitHub vì dung lượng lớn.

## 2. Mục Tiêu

- Mô tả quy mô thí sinh giai đoạn 2021-2025.
- Phân tích xu hướng điểm trung bình, tỷ lệ điểm cao và chênh lệch giữa tỉnh/thành.
- Xây dựng pipeline dự báo điểm trung bình năm tiếp theo ở cấp toàn quốc.
- Đánh giá mô hình bằng rolling backtest thay vì chỉ đưa ra con số dự báo.

## 3. Dữ Liệu

- Nguồn raw CSV: https://drive.google.com/file/d/1FIU_8XT4pIC261SwYtmwTDLFP2H_WAUc/view
- SHA256: `E11EC167D7073192F719C5A09B2A91556631CA897E998467C2BAF8CA485E86B0`
- Tổng số dòng raw: **6.068.463**.
- Phạm vi raw: **2020-2025**.
- Phạm vi dùng trong đồ án: **2021-2025**.

| Năm | Số dòng raw |
|-----|-------------|
| 2020 | 870.517 |
| 2021 | 987.704 |
| 2022 | 995.441 |
| 2023 | 1.022.060 |
| 2024 | 1.061.605 |
| 2025 | 1.131.136 |

Quy ước tiền xử lý quan trọng: điểm `0.0` ở một môn được xem là thí sinh không thi môn đó, nên không tính vào điểm trung bình môn.

## 4. Tiền Xử Lý Và Tổng Hợp

Pipeline đọc CSV theo chunk để xử lý file lớn, lọc phạm vi năm, sau đó tổng hợp theo năm, môn và tỉnh. Các bảng tổng hợp nằm trong `outputs/tables/`, còn biểu đồ nằm trong `outputs/figures/`.

## 5. Kết Quả EDA Chính

Tổng số thí sinh trong phạm vi 2021-2025: **5.197.946**.

| Năm | Số thí sinh |
|-----|-------------|
| 2021 | 987.704 |
| 2022 | 995.441 |
| 2023 | 1.022.060 |
| 2024 | 1.061.605 |
| 2025 | 1.131.136 |

### Xu Hướng Theo Môn

| Môn | TB đầu | TB cuối | Thay đổi | % >= 8 cuối |
| --- | --- | --- | --- | --- |
| Công nghệ công nghiệp | 5,79 | 5,79 | +0.00% | 11.2% |
| Công nghệ nông nghiệp | 7,72 | 7,72 | +0.00% | 48.8% |
| GDCD | 8,37 | 8,16 | -2.60% | 65.8% |
| Hóa học | 6,63 | 6,06 | -8.53% | 19.3% |
| Kinh tế & Pháp luật | 7,69 | 7,69 | +0.00% | 49.1% |
| Lịch sử | 4,97 | 6,52 | +31.13% | 23.0% |
| Ngoại ngữ | 5,85 | 5,41 | -7.60% | 6.0% |
| Ngữ văn | 6,47 | 7,00 | +8.22% | 26.7% |
| Sinh học | 5,52 | 5,78 | +4.76% | 10.8% |
| Tin học | 6,78 | 6,78 | +0.00% | 24.8% |
| Toán | 6,61 | 4,78 | -27.68% | 5.5% |
| Vật lý | 6,57 | 6,99 | +6.37% | 30.8% |
| Địa lý | 6,96 | 6,63 | -4.72% | 26.7% |

### Top/Bottom Tỉnh Theo Toán 2025

**Top 10:**
1. Ninh Bình: 5,64 (23.209 thí sinh)
2. Phú Thọ: 5,45 (16.201 thí sinh)
3. Lâm Đồng: 5,40 (16.713 thí sinh)
4. Hà Nội: 5,28 (120.277 thí sinh)
5. Hà Giang: 5,25 (96.488 thí sinh)
6. Cao Bằng: 5,20 (28.752 thí sinh)
7. Hải Dương: 5,19 (19.308 thí sinh)
8. Bắc Kạn: 5,17 (13.964 thí sinh)
9. Thanh Hóa: 5,17 (23.789 thí sinh)
10. Nam Định: 5,17 (10.172 thí sinh)

**Bottom 10:**
1. Tuyên Quang: 3,45 (7.047 thí sinh)
2. Quảng Ninh: 3,63 (12.380 thí sinh)
3. Lào Cai: 3,71 (4.826 thí sinh)
4. Hòa Bình: 3,78 (3.065 thí sinh)
5. Bạc Liêu: 3,81 (6.843 thí sinh)
6. Hà Nam: 3,91 (10.488 thí sinh)
7. Yên Bái: 3,94 (9.517 thí sinh)
8. Lạng Sơn: 4,00 (9.048 thí sinh)
9. Kiên Giang: 4,03 (10.030 thí sinh)
10. Điện Biên: 4,07 (4.178 thí sinh)

## 6. Phương Pháp Dự Báo

Các mô hình được so sánh gồm naive forecast, trung bình trượt 2 năm, trung bình trượt 3 năm, hồi quy tuyến tính và san bằng mũ đơn. Mỗi môn được chọn mô hình tốt nhất dựa trên MAE/RMSE từ rolling backtest.

## 7. Thực Nghiệm Và Kết Quả Dự Báo

| Môn | Mô hình | MAE | RMSE | MAPE |
| --- | --- | --- | --- | --- |
| Toán | Trung bình trượt 3 năm | 0,8044 | 1,1349 | 16.81% |
| Ngữ văn | Trung bình trượt 2 năm | 0,2954 | 0,3887 | 4.10% |
| Ngoại ngữ | Trung bình trượt 3 năm | 0,0284 | 0,0286 | 0.52% |
| Vật lý | Hồi quy tuyến tính | 0,1761 | 0,2239 | 2.53% |
| Hóa học | Trung bình trượt 3 năm | 0,3286 | 0,4562 | 5.41% |
| Sinh học | Naive: lấy năm gần nhất | 0,3085 | 0,3665 | 5.26% |

### Dự Báo Năm Tiếp Theo

| Môn | Mô hình | Dự báo | Khoảng | MAE | RMSE |
| --- | --- | --- | --- | --- | --- |
| Toán | Trung bình trượt 3 năm | 5,827 | 3,603-8,051 | 0,8044 | 1,1349 |
| Ngữ văn | Trung bình trượt 2 năm | 7,117 | 6,355-7,879 | 0,2954 | 0,3887 |
| Ngoại ngữ | Trung bình trượt 3 năm | 5,463 | 5,313-5,613 | 0,0284 | 0,0286 |
| Vật lý | Hồi quy tuyến tính | 6,937 | 6,498-7,376 | 0,1761 | 0,2239 |
| Hóa học | Trung bình trượt 3 năm | 6,497 | 5,603-7,391 | 0,3286 | 0,4562 |
| Sinh học | Naive: lấy năm gần nhất | 5,778 | 5,060-6,497 | 0,3085 | 0,3665 |

## 8. Hạn Chế

- Chỉ có 5 điểm thời gian chính trong phạm vi nghiên cứu, nên dự báo phải xem là xu hướng tham khảo.
- Thay đổi cấu trúc đề thi, quy chế thi hoặc nhóm thí sinh có thể làm mô hình sai lệch.
- Một số môn năm 2025 có cấu trúc mới hoặc số lượng thí sinh thay đổi mạnh, cần diễn giải thận trọng.
- Dự báo ở cấp tổng hợp, không dự đoán điểm cá nhân hay điểm của từng trường.

## 9. Hướng Phát Triển

- Bổ sung dữ liệu các năm tiếp theo để tăng độ ổn định của mô hình.
- Thêm phân tích phân phối điểm bằng histogram/boxplot/percentile.
- Thử mô hình phân cấp theo tỉnh nếu dữ liệu nhiều năm hơn.
- Xuất report PDF và slide bảo vệ tự động từ pipeline.

## 10. Kết Luận

Project đã có pipeline tái lập từ raw CSV đến bảng, biểu đồ, báo cáo và dự báo. Phần dự báo được cải thiện bằng cách so sánh nhiều mô hình và đánh giá bằng rolling backtest, phù hợp hơn với yêu cầu của một đồ án phân tích dữ liệu.