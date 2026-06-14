# Báo Cáo Đồ Án: Phân Tích Và Dự Báo Điểm Thi THPTQG

**Ngày tạo:** 14/06/2026 12:01
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

## 8. Phân Tích DA Nâng Cao

Phần này bổ sung lớp phân tích chẩn đoán để đồ án không chỉ dừng ở thống kê mô tả.

### 8.1. Data quality — dữ liệu có đủ tin cậy để phân tích không?

- Số dòng trong phạm vi 2021-2025: **5.197.946**.
- Số tỉnh/thành xuất hiện: **63**.
- Ô điểm ngoài khoảng 0-10: **0**.
- Ô điểm `0.0`: **39.898.347** — được xem là không thi môn, không đưa vào TB môn.
- Trùng khóa `Nam + SBD`: **0** dòng.

**Môn có tỷ lệ 0.0 cao nhất năm cuối** — thường là môn tự chọn hoặc môn chỉ xuất hiện ở chương trình mới:

| Môn | Tỷ lệ 0.0 | Tỷ lệ thiếu |
| --- | --- | --- |
| GDCD | 100.0% | 0.00% |
| Công nghệ công nghiệp | 99.8% | 0.00% |
| Tin học | 99.3% | 0.00% |
| Công nghệ nông nghiệp | 98.1% | 0.00% |
| Sinh học | 93.8% | 0.00% |
| Hóa học | 78.8% | 0.00% |

**Insight:** kiểm tra `0.0` là bước bắt buộc. Nếu tính cả 0.0 vào trung bình, điểm các môn tự chọn sẽ bị kéo xuống sai bản chất.

### 8.2. Phân phối điểm — không chỉ nhìn điểm trung bình

Phân phối giúp trả lời câu hỏi: điểm trung bình thay đổi vì cả phổ điểm dịch chuyển hay chỉ vì nhóm điểm thấp/cao thay đổi.

| Môn | Median | P10 | P90 | IQR | % < 5 | % >= 8 |
| --- | --- | --- | --- | --- | --- | --- |
| Hóa học | 6,00 | 3,75 | 8,75 | 2,75 | 29.5% | 19.3% |
| Địa lý | 6,75 | 4,25 | 9,00 | 2,65 | 18.7% | 26.7% |
| Lịch sử | 6,60 | 4,25 | 8,75 | 2,50 | 18.6% | 23.0% |
| Công nghệ công nghiệp | 5,60 | 3,95 | 8,00 | 2,45 | 34.1% | 11.2% |
| Vật lý | 7,00 | 5,00 | 9,00 | 2,40 | 9.8% | 30.8% |
| Sinh học | 5,75 | 3,75 | 8,00 | 2,40 | 32.4% | 10.8% |
| Toán | 4,60 | 2,70 | 7,10 | 2,35 | 56.4% | 5.5% |
| Tin học | 6,75 | 4,85 | 8,75 | 2,10 | 11.2% | 24.8% |
| Ngoại ngữ | 5,25 | 3,50 | 7,25 | 2,00 | 37.9% | 6.0% |
| Ngữ văn | 7,25 | 5,25 | 8,50 | 1,75 | 6.2% | 26.7% |

**Insight:** năm 2025, môn có độ phân tán lớn nhất theo IQR là **Hóa học**; môn này cần đọc thêm histogram/boxplot thay vì chỉ kết luận bằng điểm trung bình.

### 8.3. Biến động theo năm — năm nào là điểm gãy?

Các dòng dưới đây là các biến động mạnh nhất theo năm; đây là nơi hội đồng thường hỏi “vì sao năm đó khác?”.

| Nam | Môn | ĐTB | Δ ĐTB | Δ % | Δ % <5 | Δ % >=8 |
| --- | --- | --- | --- | --- | --- | --- |
| 2022 | Lịch sử | 6,34 | +1.37 | +27.6% | -32.7% | +11.1% |
| 2023 | Sinh học | 6,40 | +1.38 | +27.4% | -40.4% | +6.0% |
| 2025 | Toán | 4,78 | -1.66 | -25.8% | +38.9% | -13.5% |
| 2024 | Địa lý | 7,19 | +1.05 | +17.0% | -9.0% | +24.4% |
| 2022 | Ngoại ngữ | 5,16 | -0.69 | -11.8% | +11.2% | -12.1% |
| 2025 | Hóa học | 6,06 | -0.62 | -9.2% | +13.7% | -7.7% |
| 2024 | Lịch sử | 6,57 | +0.54 | +9.0% | -11.9% | +6.5% |
| 2022 | Sinh học | 5,02 | -0.50 | -9.0% | +16.3% | -1.9% |
| 2025 | Sinh học | 5,78 | -0.51 | -8.1% | +19.1% | +0.8% |
| 2023 | Địa lý | 6,15 | -0.53 | -7.9% | +6.0% | -10.1% |

**Insight:** phần này chuyển dự án từ mô tả “môn A tăng/giảm” sang phân tích “năm nào làm xu hướng đổi mạnh, và nhóm điểm nào kéo xu hướng đó”.

### 8.4. Phân tích tỉnh/vùng và bất thường

**So sánh vùng môn Toán năm 2025:**

| Vùng | ĐTB Toán | % >= 8 | Số TS |
| --- | --- | --- | --- |
| Đồng bằng sông Hồng | 5,02 | 7.9% | 283.190 |
| Trung du và miền núi phía Bắc | 4,88 | 5.8% | 248.723 |
| Bắc Trung Bộ và Duyên hải miền Trung | 4,74 | 5.9% | 248.830 |
| Tây Nguyên | 4,73 | 4.3% | 81.546 |
| Đông Nam Bộ | 4,55 | 2.4% | 99.648 |
| Đồng bằng sông Cửu Long | 4,47 | 2.4% | 157.027 |

**Một số tỉnh/năm lệch mạnh so với mặt bằng quốc gia:**

| Nam | Tỉnh | Môn | ĐTB tỉnh | Δ quốc gia | z_score |
| --- | --- | --- | --- | --- | --- |
| 2023 | Tuyên Quang | Toán | 4,32 | -1.94 | -3.4522 |
| 2024 | Tuyên Quang | Toán | 4,58 | -1.86 | -3.4985 |
| 2022 | Tuyên Quang | Toán | 4,70 | -1.77 | -3.3509 |
| 2021 | Tuyên Quang | Toán | 4,92 | -1.70 | -3.2671 |
| 2025 | Tuyên Quang | Sinh học | 4,25 | -1.52 | -3.1287 |
| 2023 | Tuyên Quang | Ngữ văn | 5,27 | -1.59 | -2.9027 |
| 2025 | Bắc Kạn | Ngữ văn | 5,60 | -1.40 | -2.9406 |
| 2024 | Sơn La | Sinh học | 7,32 | +1.04 | 3.2724 |
| 2024 | Tuyên Quang | Ngoại ngữ | 3,92 | -1.61 | -2.6944 |
| 2023 | Tuyên Quang | Ngoại ngữ | 3,83 | -1.63 | -2.6712 |

**Tỉnh có biến động mạnh giữa hai năm liên tiếp:**

| Tỉnh | Môn | Max YoY | latest_count |
| --- | --- | --- | --- |
| Sơn La | Sinh học | 2,12 | 1138 |
| An Giang | Toán | 2,11 | 11473 |
| TP. Hồ Chí Minh | Toán | 2,06 | 17241 |
| Long An | Toán | 2,02 | 20653 |
| Hậu Giang | Toán | 1,96 | 6661 |
| Bến Tre | Toán | 1,91 | 16540 |
| Vĩnh Long | Toán | 1,90 | 13169 |
| Sóc Trăng | Toán | 1,88 | 10852 |
| Đồng Tháp | Toán | 1,87 | 12188 |
| Bà Rịa - Vũng Tàu | Toán | 1,86 | 15662 |

**Insight:** top/bottom tỉnh chỉ cho biết thứ hạng tại một năm; anomaly và volatility cho biết nơi nào cần kiểm tra sâu vì biến động khác thường.

### 8.5. Tương quan môn học và tổ hợp xét tuyển

**Các cặp môn tương quan cao nhất năm 2025:**

| Môn X | Môn Y | Corr | Số cặp |
| --- | --- | --- | --- |
| Lịch sử | Địa lý | 0.76 | 297.399 |
| Vật lý | Hóa học | 0.75 | 162.206 |
| Hóa học | Sinh học | 0.74 | 44.964 |
| Toán | Sinh học | 0.74 | 69.894 |
| Toán | Hóa học | 0.73 | 240.129 |
| Toán | Vật lý | 0.71 | 347.588 |
| Sinh học | Địa lý | 0.64 | 1.442 |
| Hóa học | Địa lý | 0.59 | 1.363 |
| Toán | Địa lý | 0.55 | 472.055 |
| Ngữ văn | Địa lý | 0.53 | 476.426 |

**Tổ hợp/khối thi năm 2025:**

| Tổ hợp | ĐTB | % >=24 | % <15 |
| --- | --- | --- | --- |
| KhoiC | 19,72 | 18.8% | 14.8% |
| KhoiA | 19,37 | 17.6% | 17.1% |
| KhoiA1 | 18,87 | 9.2% | 14.7% |
| KhoiD | 18,61 | 3.8% | 10.3% |
| KhoiB | 18,29 | 13.2% | 25.9% |

**Insight:** tương quan và tổ hợp môn giúp dự án tiến gần bài toán DA thực tế hơn: không chỉ hỏi từng môn riêng lẻ, mà xem cấu trúc điểm giữa các môn có đi cùng nhau không.


## 9. Đánh Giá Độ Tin Cậy Forecast

### 9.1. Độ tin cậy của forecast

Vì chuỗi chỉ có 5 năm, forecast được chấm độ tin cậy riêng để tránh trình bày như dự đoán chắc chắn.

| Môn | Dự báo | Độ tin cậy | Ghi chú |
| --- | --- | --- | --- |
| Toán | 5,827 | Thấp | chỉ có 2 điểm backtest do chuỗi 5 năm; MAE=0.8044; khoảng dự báo rộng 4.449 điểm; MAPE=16.81% |
| Ngữ văn | 7,117 | Trung bình | chỉ có 2 điểm backtest do chuỗi 5 năm; MAE=0.2954; khoảng dự báo rộng 1.524 điểm; MAPE=4.10% |
| Ngoại ngữ | 5,463 | Tương đối | chỉ có 2 điểm backtest do chuỗi 5 năm; MAE=0.0284; khoảng dự báo rộng 0.300 điểm; MAPE=0.52% |
| Vật lý | 6,937 | Trung bình | chỉ có 2 điểm backtest do chuỗi 5 năm; MAE=0.1761; khoảng dự báo rộng 0.878 điểm; MAPE=2.53% |
| Hóa học | 6,497 | Thấp | chỉ có 2 điểm backtest do chuỗi 5 năm; MAE=0.3286; khoảng dự báo rộng 1.788 điểm; MAPE=5.41% |
| Sinh học | 5,778 | Trung bình | chỉ có 2 điểm backtest do chuỗi 5 năm; MAE=0.3085; khoảng dự báo rộng 1.437 điểm; MAPE=5.26% |


## 10. Hạn Chế

- Chỉ có 5 điểm thời gian chính trong phạm vi nghiên cứu, nên dự báo phải xem là xu hướng tham khảo.
- Thay đổi cấu trúc đề thi, quy chế thi hoặc nhóm thí sinh có thể làm mô hình sai lệch.
- Một số môn năm 2025 có cấu trúc mới hoặc số lượng thí sinh thay đổi mạnh, cần diễn giải thận trọng.
- Dự báo ở cấp tổng hợp, không dự đoán điểm cá nhân hay điểm của từng trường.

## 11. Hướng Phát Triển

- Bổ sung dữ liệu các năm tiếp theo để tăng độ ổn định của mô hình.
- Mở rộng phân tích phân phối điểm sang cấp tỉnh/vùng nếu tài nguyên xử lý cho phép.
- Thử mô hình phân cấp theo tỉnh nếu dữ liệu nhiều năm hơn.
- Xuất report PDF và slide bảo vệ tự động từ pipeline.

## 12. Kết Luận

Project đã có pipeline tái lập từ raw CSV đến bảng, biểu đồ, báo cáo và dự báo. Phần dự báo được cải thiện bằng cách so sánh nhiều mô hình và đánh giá bằng rolling backtest, phù hợp hơn với yêu cầu của một đồ án phân tích dữ liệu.