# THPTQG Trends — Phân tích & dự báo điểm thi THPT quốc gia

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/2274802010922/thptqg-trends/blob/main/colab/THPTQG_Colab.ipynb)

**Repository:** [github.com/2274802010922/thptqg-trends](https://github.com/2274802010922/thptqg-trends)

Đồ án phân tích dữ liệu điểm **Kỳ thi tốt nghiệp THPT quốc gia** (2021–2025). **Toàn bộ báo cáo nằm trong file README này** — viết sao cho **giáo viên, phụ huynh, sinh viên ngành khác** cũng đọc được.

**Cập nhật lần chạy pipeline gần nhất:** 12/06/2026 20:06

---

## Mục lục

- [Đọc trước — Thuật ngữ & hướng dẫn nhanh](#đọc-trước--dành-cho-người-chưa-quen-phân-tích-dữ-liệu)
1. [Tóm tắt](#1-tóm-tắt)
2. [Mục tiêu & phạm vi](#2-mục-tiêu--phạm-vi)
3. [Nguồn dữ liệu](#3-nguồn-dữ-liệu)
4. [Mô tả dữ liệu](#4-mô-tả-dữ-liệu)
5. [Phương pháp & quy trình](#5-phương-pháp--quy-trình-giải-thích-đơn-giản)
6. [Kết quả phân tích](#6-kết-quả-phân-tích--kèm-giải-thích)
7. [Dự báo 2026](#7-dự-báo-2026--giải-thích-cho-người-không-chuyên)
8. [Báo cáo chi tiết biểu đồ](#8-báo-cáo-chi-tiết-biểu-đồ)
9. [Cấu trúc repository](#9-cấu-trúc-repository)
10. [Hướng dẫn chạy](#10-hướng-dẫn-chạy)
11. [Kết quả đầu ra (outputs)](#11-kết-quả-đầu-ra-outputs)
12. [Giới hạn & lưu ý](#12-giới-hạn--lưu-ý)


---

## Đọc trước — Dành cho người chưa quen phân tích dữ liệu

Báo cáo này dùng **số liệu điểm thi THPT quốc gia** (2021–2025) để trả lời ba câu hỏi đơn giản:

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

---

## 1. Tóm tắt

*(Đọc mục này trước nếu bạn chỉ có 2 phút.)*

| Hạng mục | Giá trị | Ý nghĩa ngắn |
|----------|---------|--------------|
| Phạm vi | 2021 – 2025 | 5 kỳ thi liên tiếp |
| Tổng thí sinh (cộng 5 năm) | **5.197.946** | Tổng lượt có trong dữ liệu |
| Mô hình dự báo | Chọn theo rolling backtest | So sánh baseline, trung bình trượt, hồi quy tuyến tính, san bằng mũ |

- Số thí sinh mỗi năm **tăng dần**: 987.704 (2021) → 1.131.136 (2025), tức **+14.5%**.
- Môn **tăng** mạnh nhất (TB 2021→2025): **Lịch sử** (+31.1%).
- Môn **giảm** mạnh nhất: **Toán** (-27.7%).

**Điều cần nhớ:** TB giảm không luôn có nghĩa “học kém hơn” — có thể do **nhiều người hơn** thi môn đó. Chi tiết từng môn ở [Mục 8](#8-báo-cáo-chi-tiết-biểu-đồ).

---

## 2. Mục tiêu & phạm vi

**Câu hỏi đồ án muốn trả lời:**

| # | Câu hỏi | Trả lời bằng gì? |
|---|---------|------------------|
| 1 | Mỗi năm có bao nhiêu thí sinh? | Biểu đồ cột, bảng mục 6.1 |
| 2 | Điểm TB từng môn đang tăng hay giảm? | Bảng mục 6.2, biểu đồ mục 8.2 |
| 3 | Tỉnh nào cao/thấp hơn trung bình? | Heatmap mục 8.3 |
| 4 | Năm sau TB có thể quanh bao nhiêu? | Mục 7, biểu đồ mục 8.4 |

**Phạm vi:**

- ✅ Thống kê **tổng hợp** (toàn quốc, theo tỉnh) — an toàn để public
- ❌ **Không** dự đoán điểm của từng số báo danh (`SBD`) cá nhân

---

## 3. Nguồn dữ liệu

| | |
|---|---|
| **Google Drive** | [cleaned_data.csv](https://drive.google.com/file/d/1FIU_8XT4pIC261SwYtmwTDLFP2H_WAUc/view) |
| **File ID** | `1FIU_8XT4pIC261SwYtmwTDLFP2H_WAUc` |
| **Local (Windows)** | `D:\do an thuc tap\cleaned_data.csv` |
| **Dung lượng** | `843,891,415` bytes |
| **SHA256** | `E11EC167D7073192F719C5A09B2A91556631CA897E998467C2BAF8CA485E86B0` |

File CSV khoảng **844 MB** — quá lớn để đưa lên GitHub, nên tải riêng từ Drive hoặc đặt đúng đường dẫn local rồi chạy pipeline.

Raw CSV có **6,068,463 dòng** trong giai đoạn 2020–2025. Đồ án này cố ý chọn **2021–2025** để đúng phạm vi 5 năm gần nhất:

| Năm | Số dòng raw |
|-----|-------------|
| 2020 | 870.517 |
| 2021 | 987.704 |
| 2022 | 995.441 |
| 2023 | 1.022.060 |
| 2024 | 1.061.605 |
| 2025 | 1.131.136 |

Chi tiết schema nằm ở [`docs/data_dictionary.md`](docs/data_dictionary.md); hướng dẫn dữ liệu nằm ở [`data/README.md`](data/README.md).

---

## 4. Mô tả dữ liệu (dễ hiểu)

Mỗi **dòng** trong file ≈ **một thí sinh một năm**, gồm:

- **SBD** — số báo danh (mã định danh, không public chi tiết trong báo cáo này)
- **Nam** — năm thi (2021–2025)
- **Tinh** — mã tỉnh (1–63)
- **Điểm từng môn** — Toán, Văn, Anh, Lý, Hóa, …

**Quy ước quan trọng:** điểm **0.0** = thí sinh **không thi môn đó**. Khi tính điểm TB môn, chỉ lấy người đã thi (điểm > 0).

Danh sách tên tỉnh đầy đủ: `data/provinces.csv`.


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

---

## 6. Kết quả phân tích — Kèm giải thích

Phần này trả lời bằng **số và bảng**. Nếu bạn thấy khó, hãy đọc đoạn **Giải thích** ngay trước mỗi bảng.

### 6.1. Số thí sinh theo năm

**Giải thích mục 6.1:** Bảng cho biết **quy mô kỳ thi** mỗi năm. Số càng lớn = càng nhiều học sinh có trong dữ liệu. Con số % trong ngoặc là mức tăng so với năm liền trước.

| Năm | Số thí sinh |
|-----|-------------|
| 2021 | 987.704 |
| 2022 | 995.441 (+0.8%) |
| 2023 | 1.022.060 (+2.7%) |
| 2024 | 1.061.605 (+3.9%) |
| 2025 | 1.131.136 (+6.5%) |

### 6.2. Xu hướng điểm TB (2021 → 2025)

**Giải thích mục 6.2:** Mỗi dòng là **một môn học**.

- **TB đầu / TB cuối:** Điểm trung bình toàn quốc năm 2021 và 2025.
- **Thay đổi:** TB năm 2025 so với 2021 tăng hay giảm bao nhiêu phần trăm.
- **% ≥ 8 cuối:** Năm 2025, bao nhiêu phần trăm thí sinh **thi môn đó** đạt từ 8.0 trở lên.

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

**Giải thích mục 6.3–6.4:** Xếp hạng **63 tỉnh/thành** theo điểm TB môn **Toán** năm 2025.

- **Top 10:** Nơi có điểm TB cao hơn trung bình cả nước.
- **Bottom 10:** Nơi có điểm TB thấp hơn.
- Số trong ngoặc *(n=…)* = có bao nhiêu thí sinh **đã thi môn đó** ở tỉnh đó — mẫu càng nhỏ thì số liệu càng dễ dao động.

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
| Toán | Trung bình trượt 3 năm | 5,827 | 3,603–8,051 | 0,8044 | 1,1349 |
| Ngữ văn | Trung bình trượt 2 năm | 7,117 | 6,355–7,879 | 0,2954 | 0,3887 |
| Ngoại ngữ | Trung bình trượt 3 năm | 5,463 | 5,313–5,613 | 0,0284 | 0,0286 |
| Vật lý | Hồi quy tuyến tính | 6,937 | 6,498–7,376 | 0,1761 | 0,2239 |
| Hóa học | Trung bình trượt 3 năm | 6,497 | 5,603–7,391 | 0,3286 | 0,4562 |
| Sinh học | Naive: lấy năm gần nhất | 5,778 | 5,060–6,497 | 0,3085 | 0,3665 |

**Cách đọc:** MAE = 0,10 nghĩa là dự đoán thường lệch khoảng **0,1 điểm**; MAE = 1,0 nghĩa là lệch khoảng **1 điểm**. Khoảng dự báo càng rộng thì kết quả càng nên xem là **định hướng**, không phải con số chắc chắn.

---

## 8. Báo cáo chi tiết biểu đồ

Phần này dành cho **mọi độc giả** — kể cả người chưa từng học thống kê. Mỗi biểu đồ được trình bày theo thứ tự:

1. **Điều này có nghĩa là gì?** — giải thích bằng lời đời thường
2. **Chú thích biểu đồ** — trục X, trục Y, màu sắc
3. **Số liệu / bảng** — con số cụ thể
4. **Phân tích** — xu hướng và so sánh
5. **Kết luận dễ hiểu** — một câu tóm tắt
6. **Hình minh hoạ**

### 8.1. Biểu đồ tổng quan

#### 8.1.1. Số thí sinh theo năm

**Điều này có nghĩa là gì?**

- Hình này trả lời câu hỏi: *Mỗi năm có bao nhiêu học sinh thi?*
- Cột cao hơn năm trước = kỳ thi quy mô lớn hơn (nhiều hồ sơ, nhiều dữ liệu hơn).
- Từ 2021 đến 2025, số thí sinh tăng từ 987.704 lên 1.131.136 — khi đọc các biểu đồ điểm, hãy nhớ quy mô thí sinh cũng đã thay đổi.

**Chú thích biểu đồ:**
- **Trục hoành (X):** Năm thi.
- **Trục tung (Y):** Tổng số thí sinh có mặt trong dữ liệu mỗi năm.
- **Ý nghĩa:** Đo quy mô kỳ thi — tăng dần cho thấy áp lực hồ sơ và khối lượng dữ liệu xử lý tăng theo thời gian.

**Số liệu chi tiết:**
- **2021:** 987.704 thí sinh
- **2022:** 995.441 thí sinh (tăng 7.737, ~0.8% so với 2021)
- **2023:** 1.022.060 thí sinh (tăng 26.619, ~2.7% so với 2022)
- **2024:** 1.061.605 thí sinh (tăng 39.545, ~3.9% so với 2023)
- **2025:** 1.131.136 thí sinh (tăng 69.531, ~6.5% so với 2024)

**Phân tích:**
- Tổng cộng **5.197.946** lượt thí sinh trong 5 năm.
- Năm **2025** ghi nhận quy mô lớn nhất (1.131.136 thí sinh).
- Xu hướng tăng liên tục gợi ý nhu cầu phân tích theo năm phải chuẩn hoá (tránh so sánh tuyệt đối khi tổng thí sinh đã thay đổi).

**Kết luận dễ hiểu:** Kỳ thi ngày càng **đông thí sinh**. Điều này không tự nói lên điểm cao hay thấp, nhưng ảnh hưởng cách ta hiểu các biểu đồ điểm phía sau.

![Số thí sinh theo năm](outputs/figures/candidates_by_year.png)

#### 8.1.2. Tỷ lệ điểm ≥ 8 — tất cả môn

**Điều này có nghĩa là gì?**

- Thay vì nhìn điểm trung bình, hình này hỏi: *Bao nhiêu phần trăm học sinh đạt điểm khá (từ 8 trở lên)?*
- Một môn có đường cao = nhiều người đạt điểm tốt hơn so với môn có đường thấp.
- Đường đi xuống theo năm = tỷ lệ học sinh đạt ≥ 8 đang giảm (có thể do đề khó hơn, hoặc nhiều người hơn thi môn đó).

**Chú thích biểu đồ:**
- Mỗi đường = một môn thi.
- **Trục Y:** Tỷ lệ (%) thí sinh **có thi môn đó** đạt **≥ 8.0 điểm**.
- Giúp so sánh *độ khó tương đối* và *tỷ lệ học sinh giỏi* giữa các môn qua từng năm.

**Năm 2025 — môn có tỷ lệ ≥ 8 cao nhất:**
- **Kinh tế & Pháp luật:** 49.1%
- **Công nghệ nông nghiệp:** 48.8%
- **Vật lý:** 30.8%

**Năm 2025 — tỷ lệ ≥ 8 thấp nhất:**
- **Toán:** 5.5%
- **Ngoại ngữ:** 6.0%
- **Sinh học:** 10.8%

**Phân tích:**
- Môn có đường cao và ổn định (vd. GDCD) thường vẫn duy trì tỷ lệ điểm khá.
- Môn có đường sụt mạnh (vd. Toán, Ngoại ngữ) phản ánh cả chất lượng lẫn thay đổi số lượng thí sinh thi môn.
- Nên đọc kết hợp biểu đồ này với biểu đồ điểm TB từng môn (mục 8.2).

**Kết luận dễ hiểu:** Môn nào **dễ lấy điểm cao** hơn sẽ có đường nằm trên; môn **khó** hoặc **ít người giỏi** sẽ nằm dưới. So sánh giữa các môn hợp lý hơn so sánh điểm tuyệt đối giữa Toán và GDCD.

![Tỷ lệ điểm >= 8](outputs/figures/pct_ge_8_by_year.png)

### 8.2. Xu hướng điểm trung bình — từng môn

#### 8.2.1. Công nghệ công nghiệp

**Điều này có nghĩa là gì?**

- Biểu đồ cho biết **điểm trung bình cả nước** môn Công nghệ công nghiệp mỗi năm — giống điểm TB chung của cả lớp quốc gia.
- 5 năm qua môn này **ổn định** (TB 2021: 5,79 → 2025: 5,79).
- Con số trên đỉnh mỗi cột/điểm trên đường là điểm TB chính xác của năm đó.

**Chú thích biểu đồ:**
- **Trục X:** Năm.
- **Trục Y:** Điểm trung bình toàn quốc (chỉ tính thí sinh **có điểm > 0**, tức đã thi môn).
- Điểm ghi trên đỉnh mỗi năm (trên hình) là giá trị TB tương ứng.

**Tóm tắt số liệu:**
- TB **2021:** 5,79 → TB **2025:** 5,79 (**+0.0%**).
- Cao nhất: **5,79** (năm 2025); thấp nhất: **5,79** (năm 2025).
- Tỷ lệ điểm ≥ 8 năm 2025: **11.2%**.
- Số thí sinh thi môn: 2.290 (2021) → 2.290 (2025), thay đổi **+0.0%**.

**Biến động theo từng năm:**

| Năm | ĐTB | % ≥ 8 | Số TS |
|-----|-----|-------|-------|
| 2025 | 5,79 | 11.2% | 2.290 |

**Phân tích:**
- Điểm trung bình **ổn định** qua 5 năm (biến động +0.0%).

**Kết luận dễ hiểu:** Năm 2025, học sinh thi Công nghệ công nghiệp trung bình được **5,79** điểm; khoảng **11.2%** đạt từ 8 trở lên.

![Công nghệ công nghiệp](outputs/figures/mean_by_year_CongNgheCongNghiep.png)

#### 8.2.2. Công nghệ nông nghiệp

**Điều này có nghĩa là gì?**

- Biểu đồ cho biết **điểm trung bình cả nước** môn Công nghệ nông nghiệp mỗi năm — giống điểm TB chung của cả lớp quốc gia.
- 5 năm qua môn này **ổn định** (TB 2021: 7,72 → 2025: 7,72).
- Con số trên đỉnh mỗi cột/điểm trên đường là điểm TB chính xác của năm đó.

**Chú thích biểu đồ:**
- **Trục X:** Năm.
- **Trục Y:** Điểm trung bình toàn quốc (chỉ tính thí sinh **có điểm > 0**, tức đã thi môn).
- Điểm ghi trên đỉnh mỗi năm (trên hình) là giá trị TB tương ứng.

**Tóm tắt số liệu:**
- TB **2021:** 7,72 → TB **2025:** 7,72 (**+0.0%**).
- Cao nhất: **7,72** (năm 2025); thấp nhất: **7,72** (năm 2025).
- Tỷ lệ điểm ≥ 8 năm 2025: **48.8%**.
- Số thí sinh thi môn: 22.048 (2021) → 22.048 (2025), thay đổi **+0.0%**.

**Biến động theo từng năm:**

| Năm | ĐTB | % ≥ 8 | Số TS |
|-----|-----|-------|-------|
| 2025 | 7,72 | 48.8% | 22.048 |

**Phân tích:**
- Điểm trung bình **ổn định** qua 5 năm (biến động +0.0%).

**Kết luận dễ hiểu:** Năm 2025, học sinh thi Công nghệ nông nghiệp trung bình được **7,72** điểm; khoảng **48.8%** đạt từ 8 trở lên.

![Công nghệ nông nghiệp](outputs/figures/mean_by_year_CongNgheNongNghiep.png)

#### 8.2.3. GDCD

**Điều này có nghĩa là gì?**

- Biểu đồ cho biết **điểm trung bình cả nước** môn GDCD mỗi năm — giống điểm TB chung của cả lớp quốc gia.
- 5 năm qua môn này **ổn định** (TB 2021: 8,37 → 2025: 8,16).
- Con số trên đỉnh mỗi cột/điểm trên đường là điểm TB chính xác của năm đó.

**Chú thích biểu đồ:**
- **Trục X:** Năm.
- **Trục Y:** Điểm trung bình toàn quốc (chỉ tính thí sinh **có điểm > 0**, tức đã thi môn).
- Điểm ghi trên đỉnh mỗi năm (trên hình) là giá trị TB tương ứng.

**Tóm tắt số liệu:**
- TB **2021:** 8,37 → TB **2025:** 8,16 (**-2.6%**).
- Cao nhất: **8,37** (năm 2021); thấp nhất: **8,03** (năm 2022).
- Tỷ lệ điểm ≥ 8 năm 2025: **65.8%**.
- Số thí sinh thi môn: 532.213 (2021) → 583.586 (2025), thay đổi **+9.7%**.

**Biến động theo từng năm:**

| Năm | ĐTB | % ≥ 8 | Số TS |
|-----|-----|-------|-------|
| 2021 | 8,37 | 71.5% | 532.213 |
| 2022 | 8,03 | 61.9% | 554.318 |
| 2023 | 8,29 | 69.0% | 565.430 |
| 2024 | 8,16 | 65.8% | 583.586 |

**Phân tích:**
- Điểm trung bình **ổn định** qua 5 năm (biến động -2.6%).
- Năm tăng mạnh nhất so với năm trước: **2023** (+3.1%).
- Năm giảm mạnh nhất so với năm trước: **2022** (-4.1%).

**Kết luận dễ hiểu:** Năm 2025, học sinh thi GDCD trung bình được **8,16** điểm; khoảng **65.8%** đạt từ 8 trở lên.

![GDCD](outputs/figures/mean_by_year_GDCD.png)

#### 8.2.4. Hóa học

**Điều này có nghĩa là gì?**

- Biểu đồ cho biết **điểm trung bình cả nước** môn Hóa học mỗi năm — giống điểm TB chung của cả lớp quốc gia.
- 5 năm qua môn này **giảm dần** (TB 2021: 6,63 → 2025: 6,06).
- Con số trên đỉnh mỗi cột/điểm trên đường là điểm TB chính xác của năm đó.

**Chú thích biểu đồ:**
- **Trục X:** Năm.
- **Trục Y:** Điểm trung bình toàn quốc (chỉ tính thí sinh **có điểm > 0**, tức đã thi môn).
- Điểm ghi trên đỉnh mỗi năm (trên hình) là giá trị TB tương ứng.

**Tóm tắt số liệu:**
- TB **2021:** 6,63 → TB **2025:** 6,06 (**-8.5%**).
- Cao nhất: **6,74** (năm 2023); thấp nhất: **6,06** (năm 2025).
- Tỷ lệ điểm ≥ 8 năm 2025: **19.3%**.
- Số thí sinh thi môn: 346.709 (2021) → 240.135 (2025), thay đổi **-30.7%**.

**Biến động theo từng năm:**

| Năm | ĐTB | % ≥ 8 | Số TS |
|-----|-----|-------|-------|
| 2021 | 6,63 | 24.9% | 346.709 |
| 2022 | 6,70 | 27.9% | 327.358 |
| 2023 | 6,74 | 22.7% | 328.115 |
| 2024 | 6,68 | 26.9% | 346.507 |
| 2025 | 6,06 | 19.3% | 240.135 |

**Phân tích:**
- Trong 5 năm, điểm trung bình **giảm -8.5%**. Cần đọc kèm cột *Số thí sinh* — giảm TB có thể do thay đổi nhóm thí sinh tham gia thi môn.
- Năm tăng mạnh nhất so với năm trước: **2022** (+1.1%).
- Năm giảm mạnh nhất so với năm trước: **2025** (-9.2%).

**Kết luận dễ hiểu:** Năm 2025, học sinh thi Hóa học trung bình được **6,06** điểm; khoảng **19.3%** đạt từ 8 trở lên.

![Hóa học](outputs/figures/mean_by_year_HoaHoc.png)

#### 8.2.5. Kinh tế & Pháp luật

**Điều này có nghĩa là gì?**

- Biểu đồ cho biết **điểm trung bình cả nước** môn Kinh tế & Pháp luật mỗi năm — giống điểm TB chung của cả lớp quốc gia.
- 5 năm qua môn này **ổn định** (TB 2021: 7,69 → 2025: 7,69).
- Con số trên đỉnh mỗi cột/điểm trên đường là điểm TB chính xác của năm đó.

**Chú thích biểu đồ:**
- **Trục X:** Năm.
- **Trục Y:** Điểm trung bình toàn quốc (chỉ tính thí sinh **có điểm > 0**, tức đã thi môn).
- Điểm ghi trên đỉnh mỗi năm (trên hình) là giá trị TB tương ứng.

**Tóm tắt số liệu:**
- TB **2021:** 7,69 → TB **2025:** 7,69 (**+0.0%**).
- Cao nhất: **7,69** (năm 2025); thấp nhất: **7,69** (năm 2025).
- Tỷ lệ điểm ≥ 8 năm 2025: **49.1%**.
- Số thí sinh thi môn: 246.401 (2021) → 246.401 (2025), thay đổi **+0.0%**.

**Biến động theo từng năm:**

| Năm | ĐTB | % ≥ 8 | Số TS |
|-----|-----|-------|-------|
| 2025 | 7,69 | 49.1% | 246.401 |

**Phân tích:**
- Điểm trung bình **ổn định** qua 5 năm (biến động +0.0%).

**Kết luận dễ hiểu:** Năm 2025, học sinh thi Kinh tế & Pháp luật trung bình được **7,69** điểm; khoảng **49.1%** đạt từ 8 trở lên.

![Kinh tế & Pháp luật](outputs/figures/mean_by_year_KinhTePhapLuat.png)

#### 8.2.6. Lịch sử

**Điều này có nghĩa là gì?**

- Biểu đồ cho biết **điểm trung bình cả nước** môn Lịch sử mỗi năm — giống điểm TB chung của cả lớp quốc gia.
- 5 năm qua môn này **cải thiện dần** (TB 2021: 4,97 → 2025: 6,52).
- Con số trên đỉnh mỗi cột/điểm trên đường là điểm TB chính xác của năm đó.

**Chú thích biểu đồ:**
- **Trục X:** Năm.
- **Trục Y:** Điểm trung bình toàn quốc (chỉ tính thí sinh **có điểm > 0**, tức đã thi môn).
- Điểm ghi trên đỉnh mỗi năm (trên hình) là giá trị TB tương ứng.

**Tóm tắt số liệu:**
- TB **2021:** 4,97 → TB **2025:** 6,52 (**+31.1%**).
- Cao nhất: **6,57** (năm 2024); thấp nhất: **4,97** (năm 2021).
- Tỷ lệ điểm ≥ 8 năm 2025: **23.0%**.
- Số thí sinh thi môn: 634.722 (2021) → 481.291 (2025), thay đổi **-24.2%**.

**Biến động theo từng năm:**

| Năm | ĐTB | % ≥ 8 | Số TS |
|-----|-----|-------|-------|
| 2021 | 4,97 | 7.0% | 634.722 |
| 2022 | 6,34 | 18.1% | 659.660 |
| 2023 | 6,03 | 13.1% | 683.442 |
| 2024 | 6,57 | 19.6% | 706.208 |
| 2025 | 6,52 | 23.0% | 481.291 |

**Phân tích:**
- Trong 5 năm, điểm trung bình **tăng +31.1%**, cho thấy môn này có xu hướng cải thiện hoặc thay đổi cơ cấu thí sinh thi.
- Năm tăng mạnh nhất so với năm trước: **2022** (+27.6%).
- Năm giảm mạnh nhất so với năm trước: **2023** (-5.0%).

**Kết luận dễ hiểu:** Năm 2025, học sinh thi Lịch sử trung bình được **6,52** điểm; khoảng **23.0%** đạt từ 8 trở lên.

![Lịch sử](outputs/figures/mean_by_year_LichSu.png)

#### 8.2.7. Ngoại ngữ

**Điều này có nghĩa là gì?**

- Biểu đồ cho biết **điểm trung bình cả nước** môn Ngoại ngữ mỗi năm — giống điểm TB chung của cả lớp quốc gia.
- 5 năm qua môn này **giảm dần** (TB 2021: 5,85 → 2025: 5,41).
- Con số trên đỉnh mỗi cột/điểm trên đường là điểm TB chính xác của năm đó.

**Chú thích biểu đồ:**
- **Trục X:** Năm.
- **Trục Y:** Điểm trung bình toàn quốc (chỉ tính thí sinh **có điểm > 0**, tức đã thi môn).
- Điểm ghi trên đỉnh mỗi năm (trên hình) là giá trị TB tương ứng.

**Tóm tắt số liệu:**
- TB **2021:** 5,85 → TB **2025:** 5,41 (**-7.6%**).
- Cao nhất: **5,85** (năm 2021); thấp nhất: **5,16** (năm 2022).
- Tỷ lệ điểm ≥ 8 năm 2025: **6.0%**.
- Số thí sinh thi môn: 868.287 (2021) → 357.721 (2025), thay đổi **-58.8%**.

**Biến động theo từng năm:**

| Năm | ĐTB | % ≥ 8 | Số TS |
|-----|-----|-------|-------|
| 2021 | 5,85 | 24.2% | 868.287 |
| 2022 | 5,16 | 12.1% | 870.601 |
| 2023 | 5,46 | 15.2% | 880.991 |
| 2024 | 5,52 | 14.6% | 912.702 |
| 2025 | 5,41 | 6.0% | 357.721 |

**Phân tích:**
- Trong 5 năm, điểm trung bình **giảm -7.6%**. Cần đọc kèm cột *Số thí sinh* — giảm TB có thể do thay đổi nhóm thí sinh tham gia thi môn.
- Năm tăng mạnh nhất so với năm trước: **2023** (+5.9%).
- Năm giảm mạnh nhất so với năm trước: **2022** (-11.8%).

**Kết luận dễ hiểu:** Năm 2025, học sinh thi Ngoại ngữ trung bình được **5,41** điểm; khoảng **6.0%** đạt từ 8 trở lên.

![Ngoại ngữ](outputs/figures/mean_by_year_NgoaiNgu.png)

#### 8.2.8. Ngữ văn

**Điều này có nghĩa là gì?**

- Biểu đồ cho biết **điểm trung bình cả nước** môn Ngữ văn mỗi năm — giống điểm TB chung của cả lớp quốc gia.
- 5 năm qua môn này **cải thiện dần** (TB 2021: 6,47 → 2025: 7,00).
- Con số trên đỉnh mỗi cột/điểm trên đường là điểm TB chính xác của năm đó.

**Chú thích biểu đồ:**
- **Trục X:** Năm.
- **Trục Y:** Điểm trung bình toàn quốc (chỉ tính thí sinh **có điểm > 0**, tức đã thi môn).
- Điểm ghi trên đỉnh mỗi năm (trên hình) là giá trị TB tương ứng.

**Tóm tắt số liệu:**
- TB **2021:** 6,47 → TB **2025:** 7,00 (**+8.2%**).
- Cao nhất: **7,23** (năm 2024); thấp nhất: **6,47** (năm 2021).
- Tỷ lệ điểm ≥ 8 năm 2025: **26.7%**.
- Số thí sinh thi môn: 974.415 (2021) → 1.126.719 (2025), thay đổi **+15.6%**.

**Biến động theo từng năm:**

| Năm | ĐTB | % ≥ 8 | Số TS |
|-----|-----|-------|-------|
| 2021 | 6,47 | 14.9% | 974.415 |
| 2022 | 6,51 | 17.0% | 981.369 |
| 2023 | 6,86 | 24.4% | 1.008.215 |
| 2024 | 7,23 | 36.0% | 1.050.081 |
| 2025 | 7,00 | 26.7% | 1.126.719 |

**Phân tích:**
- Trong 5 năm, điểm trung bình **tăng +8.2%**, cho thấy môn này có xu hướng cải thiện hoặc thay đổi cơ cấu thí sinh thi.
- Năm tăng mạnh nhất so với năm trước: **2024** (+5.4%).
- Năm giảm mạnh nhất so với năm trước: **2025** (-3.2%).

**Kết luận dễ hiểu:** Năm 2025, học sinh thi Ngữ văn trung bình được **7,00** điểm; khoảng **26.7%** đạt từ 8 trở lên.

![Ngữ văn](outputs/figures/mean_by_year_NguVan.png)

#### 8.2.9. Sinh học

**Điều này có nghĩa là gì?**

- Biểu đồ cho biết **điểm trung bình cả nước** môn Sinh học mỗi năm — giống điểm TB chung của cả lớp quốc gia.
- 5 năm qua môn này **ổn định** (TB 2021: 5,52 → 2025: 5,78).
- Con số trên đỉnh mỗi cột/điểm trên đường là điểm TB chính xác của năm đó.

**Chú thích biểu đồ:**
- **Trục X:** Năm.
- **Trục Y:** Điểm trung bình toàn quốc (chỉ tính thí sinh **có điểm > 0**, tức đã thi môn).
- Điểm ghi trên đỉnh mỗi năm (trên hình) là giá trị TB tương ứng.

**Tóm tắt số liệu:**
- TB **2021:** 5,52 → TB **2025:** 5,78 (**+4.8%**).
- Cao nhất: **6,40** (năm 2023); thấp nhất: **5,02** (năm 2022).
- Tỷ lệ điểm ≥ 8 năm 2025: **10.8%**.
- Số thí sinh thi môn: 341.264 (2021) → 69.895 (2025), thay đổi **-79.5%**.

**Biến động theo từng năm:**

| Năm | ĐTB | % ≥ 8 | Số TS |
|-----|-----|-------|-------|
| 2021 | 5,52 | 6.5% | 341.264 |
| 2022 | 5,02 | 4.6% | 322.162 |
| 2023 | 6,40 | 10.6% | 324.606 |
| 2024 | 6,28 | 10.1% | 342.343 |
| 2025 | 5,78 | 10.8% | 69.895 |

**Phân tích:**
- Điểm trung bình **ổn định** qua 5 năm (biến động +4.8%).
- Năm tăng mạnh nhất so với năm trước: **2023** (+27.4%).
- Năm giảm mạnh nhất so với năm trước: **2022** (-9.0%).

**Kết luận dễ hiểu:** Năm 2025, học sinh thi Sinh học trung bình được **5,78** điểm; khoảng **10.8%** đạt từ 8 trở lên.

![Sinh học](outputs/figures/mean_by_year_SinhHoc.png)

#### 8.2.10. Tin học

**Điều này có nghĩa là gì?**

- Biểu đồ cho biết **điểm trung bình cả nước** môn Tin học mỗi năm — giống điểm TB chung của cả lớp quốc gia.
- 5 năm qua môn này **ổn định** (TB 2021: 6,78 → 2025: 6,78).
- Con số trên đỉnh mỗi cột/điểm trên đường là điểm TB chính xác của năm đó.

**Chú thích biểu đồ:**
- **Trục X:** Năm.
- **Trục Y:** Điểm trung bình toàn quốc (chỉ tính thí sinh **có điểm > 0**, tức đã thi môn).
- Điểm ghi trên đỉnh mỗi năm (trên hình) là giá trị TB tương ứng.

**Tóm tắt số liệu:**
- TB **2021:** 6,78 → TB **2025:** 6,78 (**+0.0%**).
- Cao nhất: **6,78** (năm 2025); thấp nhất: **6,78** (năm 2025).
- Tỷ lệ điểm ≥ 8 năm 2025: **24.8%**.
- Số thí sinh thi môn: 7.602 (2021) → 7.602 (2025), thay đổi **+0.0%**.

**Biến động theo từng năm:**

| Năm | ĐTB | % ≥ 8 | Số TS |
|-----|-----|-------|-------|
| 2025 | 6,78 | 24.8% | 7.602 |

**Phân tích:**
- Điểm trung bình **ổn định** qua 5 năm (biến động +0.0%).

**Kết luận dễ hiểu:** Năm 2025, học sinh thi Tin học trung bình được **6,78** điểm; khoảng **24.8%** đạt từ 8 trở lên.

![Tin học](outputs/figures/mean_by_year_TinHoc.png)

#### 8.2.11. Toán

**Điều này có nghĩa là gì?**

- Biểu đồ cho biết **điểm trung bình cả nước** môn Toán mỗi năm — giống điểm TB chung của cả lớp quốc gia.
- 5 năm qua môn này **giảm dần** (TB 2021: 6,61 → 2025: 4,78).
- Con số trên đỉnh mỗi cột/điểm trên đường là điểm TB chính xác của năm đó.

**Chú thích biểu đồ:**
- **Trục X:** Năm.
- **Trục Y:** Điểm trung bình toàn quốc (chỉ tính thí sinh **có điểm > 0**, tức đã thi môn).
- Điểm ghi trên đỉnh mỗi năm (trên hình) là giá trị TB tương ứng.

**Tóm tắt số liệu:**
- TB **2021:** 6,61 → TB **2025:** 4,78 (**-27.7%**).
- Cao nhất: **6,61** (năm 2021); thấp nhất: **4,78** (năm 2025).
- Tỷ lệ điểm ≥ 8 năm 2025: **5.5%**.
- Số thí sinh thi môn: 977.363 (2021) → 1.126.166 (2025), thay đổi **+15.2%**.

**Biến động theo từng năm:**

| Năm | ĐTB | % ≥ 8 | Số TS |
|-----|-----|-------|-------|
| 2021 | 6,61 | 25.9% | 977.363 |
| 2022 | 6,47 | 21.9% | 982.723 |
| 2023 | 6,25 | 15.2% | 1.003.371 |
| 2024 | 6,45 | 19.0% | 1.045.612 |
| 2025 | 4,78 | 5.5% | 1.126.166 |

**Phân tích:**
- Trong 5 năm, điểm trung bình **giảm -27.7%**. Cần đọc kèm cột *Số thí sinh* — giảm TB có thể do thay đổi nhóm thí sinh tham gia thi môn.
- Năm tăng mạnh nhất so với năm trước: **2024** (+3.1%).
- Năm giảm mạnh nhất so với năm trước: **2025** (-25.8%).
- *Lưu ý:* Giảm TB mạnh có thể liên quan mở rộng nhóm thí sinh thi môn (xem cột Số TS), không đồng nghĩa chất lượng giảm tuyệt đối.

**Kết luận dễ hiểu:** Năm 2025, học sinh thi Toán trung bình được **4,78** điểm; khoảng **5.5%** đạt từ 8 trở lên.

![Toán](outputs/figures/mean_by_year_Toan.png)

#### 8.2.12. Vật lý

**Điều này có nghĩa là gì?**

- Biểu đồ cho biết **điểm trung bình cả nước** môn Vật lý mỗi năm — giống điểm TB chung của cả lớp quốc gia.
- 5 năm qua môn này **cải thiện dần** (TB 2021: 6,57 → 2025: 6,99).
- Con số trên đỉnh mỗi cột/điểm trên đường là điểm TB chính xác của năm đó.

**Chú thích biểu đồ:**
- **Trục X:** Năm.
- **Trục Y:** Điểm trung bình toàn quốc (chỉ tính thí sinh **có điểm > 0**, tức đã thi môn).
- Điểm ghi trên đỉnh mỗi năm (trên hình) là giá trị TB tương ứng.

**Tóm tắt số liệu:**
- TB **2021:** 6,57 → TB **2025:** 6,99 (**+6.4%**).
- Cao nhất: **6,99** (năm 2025); thấp nhất: **6,57** (năm 2021).
- Tỷ lệ điểm ≥ 8 năm 2025: **30.8%**.
- Số thí sinh thi môn: 345.079 (2021) → 347.598 (2025), thay đổi **+0.7%**.

**Biến động theo từng năm:**

| Năm | ĐTB | % ≥ 8 | Số TS |
|-----|-----|-------|-------|
| 2021 | 6,57 | 18.3% | 345.079 |
| 2022 | 6,72 | 22.8% | 325.513 |
| 2023 | 6,57 | 21.3% | 327.179 |
| 2024 | 6,67 | 27.2% | 345.611 |
| 2025 | 6,99 | 30.8% | 347.598 |

**Phân tích:**
- Trong 5 năm, điểm trung bình **tăng +6.4%**, cho thấy môn này có xu hướng cải thiện hoặc thay đổi cơ cấu thí sinh thi.
- Năm tăng mạnh nhất so với năm trước: **2025** (+4.8%).
- Năm giảm mạnh nhất so với năm trước: **2023** (-2.2%).

**Kết luận dễ hiểu:** Năm 2025, học sinh thi Vật lý trung bình được **6,99** điểm; khoảng **30.8%** đạt từ 8 trở lên.

![Vật lý](outputs/figures/mean_by_year_VatLy.png)

#### 8.2.13. Địa lý

**Điều này có nghĩa là gì?**

- Biểu đồ cho biết **điểm trung bình cả nước** môn Địa lý mỗi năm — giống điểm TB chung của cả lớp quốc gia.
- 5 năm qua môn này **ổn định** (TB 2021: 6,96 → 2025: 6,63).
- Con số trên đỉnh mỗi cột/điểm trên đường là điểm TB chính xác của năm đó.

**Chú thích biểu đồ:**
- **Trục X:** Năm.
- **Trục Y:** Điểm trung bình toàn quốc (chỉ tính thí sinh **có điểm > 0**, tức đã thi môn).
- Điểm ghi trên đỉnh mỗi năm (trên hình) là giá trị TB tương ứng.

**Tóm tắt số liệu:**
- TB **2021:** 6,96 → TB **2025:** 6,63 (**-4.7%**).
- Cao nhất: **7,19** (năm 2024); thấp nhất: **6,15** (năm 2023).
- Tỷ lệ điểm ≥ 8 năm 2025: **26.7%**.
- Số thí sinh thi môn: 628.784 (2021) → 476.469 (2025), thay đổi **-24.2%**.

**Biến động theo từng năm:**

| Năm | ĐTB | % ≥ 8 | Số TS |
|-----|-----|-------|-------|
| 2021 | 6,96 | 22.1% | 628.784 |
| 2022 | 6,68 | 16.7% | 657.400 |
| 2023 | 6,15 | 6.6% | 682.054 |
| 2024 | 7,19 | 31.0% | 704.623 |
| 2025 | 6,63 | 26.7% | 476.469 |

**Phân tích:**
- Điểm trung bình **ổn định** qua 5 năm (biến động -4.7%).
- Năm tăng mạnh nhất so với năm trước: **2024** (+17.0%).
- Năm giảm mạnh nhất so với năm trước: **2023** (-7.9%).

**Kết luận dễ hiểu:** Năm 2025, học sinh thi Địa lý trung bình được **6,63** điểm; khoảng **26.7%** đạt từ 8 trở lên.

![Địa lý](outputs/figures/mean_by_year_DiaLy.png)

### 8.3. Heatmap phân bố theo tỉnh (2025)

#### 8.3.1. Hóa học

**Điều này có nghĩa là gì?**

- Hình này giống **bản đồ nhiệt**: mỗi hàng là một tỉnh, màu càng đậm = điểm TB môn Hóa học càng cao năm 2025.
- Giúp trả lời: *Tỉnh nào điểm cao hơn, tỉnh nào thấp hơn?* — không phải xếp hạng từng học sinh.
- Chênh lệch lớn nhất giữa hai tỉnh trong dữ liệu là khoảng **1,65** điểm.

**Chú thích biểu đồ:**
- **Trục dọc:** Mã tỉnh (1–63, xem `data/provinces.csv`).
- **Màu sắc:** Vàng/nhạt = điểm thấp; cam/đỏ đậm = điểm cao.
- Thể hiện **chênh lệch vùng** về điểm TB môn **Hóa học** năm **2025**.

**Số liệu nổi bật:**
- Điểm TB trung bình các tỉnh: **5,98**.
- Chênh lệch max–min giữa tỉnh: **1,65** điểm.

**Top 3 tỉnh:**
- **Quảng Trị:** 6,74 (3.150 thí sinh)
- **Phú Thọ:** 6,71 (3.150 thí sinh)
- **Quảng Nam:** 6,57 (3.006 thí sinh)

**Bottom 3 tỉnh:**
- **Điện Biên:** 5,09 (844 thí sinh)
- **Tuyên Quang:** 5,23 (603 thí sinh)
- **Sóc Trăng:** 5,24 (2.816 thí sinh)

**Phân tích:**
- Heatmap cho thấy **bất đồng đều không gian**: cùng một môn nhưng điểm TB chênh lệch rõ giữa các tỉnh.
- Cần thận trọng khi so sánh tỉnh có **số thí sinh thi môn rất nhỏ** (mẫu ít → TB dễ biến động).

**Kết luận dễ hiểu:** Cùng thi môn Hóa học, điểm TB **không đồng đều** giữa các tỉnh — có nơi nổi bật (top 3) và nơi thấp hơn (bottom 3). Đây là ảnh chụp năm 2025, không phải xếp hạng vĩnh viễn.

![Heatmap Hóa học](outputs/figures/heatmap_HoaHoc_2025.png)

#### 8.3.2. Ngoại ngữ

**Điều này có nghĩa là gì?**

- Hình này giống **bản đồ nhiệt**: mỗi hàng là một tỉnh, màu càng đậm = điểm TB môn Ngoại ngữ càng cao năm 2025.
- Giúp trả lời: *Tỉnh nào điểm cao hơn, tỉnh nào thấp hơn?* — không phải xếp hạng từng học sinh.
- Chênh lệch lớn nhất giữa hai tỉnh trong dữ liệu là khoảng **1,06** điểm.

**Chú thích biểu đồ:**
- **Trục dọc:** Mã tỉnh (1–63, xem `data/provinces.csv`).
- **Màu sắc:** Vàng/nhạt = điểm thấp; cam/đỏ đậm = điểm cao.
- Thể hiện **chênh lệch vùng** về điểm TB môn **Ngoại ngữ** năm **2025**.

**Số liệu nổi bật:**
- Điểm TB trung bình các tỉnh: **5,22**.
- Chênh lệch max–min giữa tỉnh: **1,06** điểm.

**Top 3 tỉnh:**
- **Hà Nội:** 5,82 (60.962 thí sinh)
- **Lâm Đồng:** 5,72 (6.479 thí sinh)
- **Hà Giang:** 5,70 (49.066 thí sinh)

**Bottom 3 tỉnh:**
- **Cần Thơ:** 4,76 (2.137 thí sinh)
- **nan:** 4,83 (1.106 thí sinh)
- **Kiên Giang:** 4,84 (1.530 thí sinh)

**Phân tích:**
- Heatmap cho thấy **bất đồng đều không gian**: cùng một môn nhưng điểm TB chênh lệch rõ giữa các tỉnh.
- Cần thận trọng khi so sánh tỉnh có **số thí sinh thi môn rất nhỏ** (mẫu ít → TB dễ biến động).

**Kết luận dễ hiểu:** Cùng thi môn Ngoại ngữ, điểm TB **không đồng đều** giữa các tỉnh — có nơi nổi bật (top 3) và nơi thấp hơn (bottom 3). Đây là ảnh chụp năm 2025, không phải xếp hạng vĩnh viễn.

![Heatmap Ngoại ngữ](outputs/figures/heatmap_NgoaiNgu_2025.png)

#### 8.3.3. Ngữ văn

**Điều này có nghĩa là gì?**

- Hình này giống **bản đồ nhiệt**: mỗi hàng là một tỉnh, màu càng đậm = điểm TB môn Ngữ văn càng cao năm 2025.
- Giúp trả lời: *Tỉnh nào điểm cao hơn, tỉnh nào thấp hơn?* — không phải xếp hạng từng học sinh.
- Chênh lệch lớn nhất giữa hai tỉnh trong dữ liệu là khoảng **2,44** điểm.

**Chú thích biểu đồ:**
- **Trục dọc:** Mã tỉnh (1–63, xem `data/provinces.csv`).
- **Màu sắc:** Vàng/nhạt = điểm thấp; cam/đỏ đậm = điểm cao.
- Thể hiện **chênh lệch vùng** về điểm TB môn **Ngữ văn** năm **2025**.

**Số liệu nổi bật:**
- Điểm TB trung bình các tỉnh: **6,83**.
- Chênh lệch max–min giữa tỉnh: **2,44** điểm.

**Top 3 tỉnh:**
- **Quảng Bình:** 8,04 (39.062 thí sinh)
- **Quảng Trị:** 7,91 (16.894 thí sinh)
- **Phú Thọ:** 7,77 (16.202 thí sinh)

**Bottom 3 tỉnh:**
- **Bắc Kạn:** 5,60 (13.923 thí sinh)
- **Quảng Ninh:** 5,79 (12.560 thí sinh)
- **Tuyên Quang:** 5,96 (7.108 thí sinh)

**Phân tích:**
- Heatmap cho thấy **bất đồng đều không gian**: cùng một môn nhưng điểm TB chênh lệch rõ giữa các tỉnh.
- Cần thận trọng khi so sánh tỉnh có **số thí sinh thi môn rất nhỏ** (mẫu ít → TB dễ biến động).

**Kết luận dễ hiểu:** Cùng thi môn Ngữ văn, điểm TB **không đồng đều** giữa các tỉnh — có nơi nổi bật (top 3) và nơi thấp hơn (bottom 3). Đây là ảnh chụp năm 2025, không phải xếp hạng vĩnh viễn.

![Heatmap Ngữ văn](outputs/figures/heatmap_NguVan_2025.png)

#### 8.3.4. Sinh học

**Điều này có nghĩa là gì?**

- Hình này giống **bản đồ nhiệt**: mỗi hàng là một tỉnh, màu càng đậm = điểm TB môn Sinh học càng cao năm 2025.
- Giúp trả lời: *Tỉnh nào điểm cao hơn, tỉnh nào thấp hơn?* — không phải xếp hạng từng học sinh.
- Chênh lệch lớn nhất giữa hai tỉnh trong dữ liệu là khoảng **2,45** điểm.

**Chú thích biểu đồ:**
- **Trục dọc:** Mã tỉnh (1–63, xem `data/provinces.csv`).
- **Màu sắc:** Vàng/nhạt = điểm thấp; cam/đỏ đậm = điểm cao.
- Thể hiện **chênh lệch vùng** về điểm TB môn **Sinh học** năm **2025**.

**Số liệu nổi bật:**
- Điểm TB trung bình các tỉnh: **5,73**.
- Chênh lệch max–min giữa tỉnh: **2,45** điểm.

**Top 3 tỉnh:**
- **Hải Dương:** 6,70 (450 thí sinh)
- **Lâm Đồng:** 6,66 (906 thí sinh)
- **Phú Thọ:** 6,61 (540 thí sinh)

**Bottom 3 tỉnh:**
- **Tuyên Quang:** 4,25 (1.097 thí sinh)
- **Điện Biên:** 4,71 (637 thí sinh)
- **Lào Cai:** 4,78 (359 thí sinh)

**Phân tích:**
- Heatmap cho thấy **bất đồng đều không gian**: cùng một môn nhưng điểm TB chênh lệch rõ giữa các tỉnh.
- Cần thận trọng khi so sánh tỉnh có **số thí sinh thi môn rất nhỏ** (mẫu ít → TB dễ biến động).

**Kết luận dễ hiểu:** Cùng thi môn Sinh học, điểm TB **không đồng đều** giữa các tỉnh — có nơi nổi bật (top 3) và nơi thấp hơn (bottom 3). Đây là ảnh chụp năm 2025, không phải xếp hạng vĩnh viễn.

![Heatmap Sinh học](outputs/figures/heatmap_SinhHoc_2025.png)

#### 8.3.5. Toán

**Điều này có nghĩa là gì?**

- Hình này giống **bản đồ nhiệt**: mỗi hàng là một tỉnh, màu càng đậm = điểm TB môn Toán càng cao năm 2025.
- Giúp trả lời: *Tỉnh nào điểm cao hơn, tỉnh nào thấp hơn?* — không phải xếp hạng từng học sinh.
- Chênh lệch lớn nhất giữa hai tỉnh trong dữ liệu là khoảng **2,19** điểm.

**Chú thích biểu đồ:**
- **Trục dọc:** Mã tỉnh (1–63, xem `data/provinces.csv`).
- **Màu sắc:** Vàng/nhạt = điểm thấp; cam/đỏ đậm = điểm cao.
- Thể hiện **chênh lệch vùng** về điểm TB môn **Toán** năm **2025**.

**Số liệu nổi bật:**
- Điểm TB trung bình các tỉnh: **4,57**.
- Chênh lệch max–min giữa tỉnh: **2,19** điểm.

**Top 3 tỉnh:**
- **Ninh Bình:** 5,64 (23.209 thí sinh)
- **Phú Thọ:** 5,45 (16.201 thí sinh)
- **Lâm Đồng:** 5,40 (16.713 thí sinh)

**Bottom 3 tỉnh:**
- **Tuyên Quang:** 3,45 (7.047 thí sinh)
- **Quảng Ninh:** 3,63 (12.380 thí sinh)
- **Lào Cai:** 3,71 (4.826 thí sinh)

**Phân tích:**
- Heatmap cho thấy **bất đồng đều không gian**: cùng một môn nhưng điểm TB chênh lệch rõ giữa các tỉnh.
- Cần thận trọng khi so sánh tỉnh có **số thí sinh thi môn rất nhỏ** (mẫu ít → TB dễ biến động).

**Kết luận dễ hiểu:** Cùng thi môn Toán, điểm TB **không đồng đều** giữa các tỉnh — có nơi nổi bật (top 3) và nơi thấp hơn (bottom 3). Đây là ảnh chụp năm 2025, không phải xếp hạng vĩnh viễn.

![Heatmap Toán](outputs/figures/heatmap_Toan_2025.png)

#### 8.3.6. Vật lý

**Điều này có nghĩa là gì?**

- Hình này giống **bản đồ nhiệt**: mỗi hàng là một tỉnh, màu càng đậm = điểm TB môn Vật lý càng cao năm 2025.
- Giúp trả lời: *Tỉnh nào điểm cao hơn, tỉnh nào thấp hơn?* — không phải xếp hạng từng học sinh.
- Chênh lệch lớn nhất giữa hai tỉnh trong dữ liệu là khoảng **1,25** điểm.

**Chú thích biểu đồ:**
- **Trục dọc:** Mã tỉnh (1–63, xem `data/provinces.csv`).
- **Màu sắc:** Vàng/nhạt = điểm thấp; cam/đỏ đậm = điểm cao.
- Thể hiện **chênh lệch vùng** về điểm TB môn **Vật lý** năm **2025**.

**Số liệu nổi bật:**
- Điểm TB trung bình các tỉnh: **6,88**.
- Chênh lệch max–min giữa tỉnh: **1,25** điểm.

**Top 3 tỉnh:**
- **Phú Thọ:** 7,50 (4.770 thí sinh)
- **Hải Dương:** 7,41 (6.857 thí sinh)
- **Nam Định:** 7,39 (3.310 thí sinh)

**Bottom 3 tỉnh:**
- **Tuyên Quang:** 6,25 (808 thí sinh)
- **Lào Cai:** 6,28 (848 thí sinh)
- **Sóc Trăng:** 6,34 (3.016 thí sinh)

**Phân tích:**
- Heatmap cho thấy **bất đồng đều không gian**: cùng một môn nhưng điểm TB chênh lệch rõ giữa các tỉnh.
- Cần thận trọng khi so sánh tỉnh có **số thí sinh thi môn rất nhỏ** (mẫu ít → TB dễ biến động).

**Kết luận dễ hiểu:** Cùng thi môn Vật lý, điểm TB **không đồng đều** giữa các tỉnh — có nơi nổi bật (top 3) và nơi thấp hơn (bottom 3). Đây là ảnh chụp năm 2025, không phải xếp hạng vĩnh viễn.

![Heatmap Vật lý](outputs/figures/heatmap_VatLy_2025.png)

### 8.4. Biểu đồ dự báo

#### 8.4.1. Hóa học

**Điều này có nghĩa là gì?**

- Đường xanh = điểm TB thật của môn Hóa học qua các năm; đường đỏ = **ước lượng** năm tới bằng Trung bình trượt 3 năm.
- Đây là công cụ học thuật (đồ án), **không phải** thông báo điểm chính thức của Bộ.
- Hãy coi con số dự báo và khoảng dự báo là *tham khảo*, không phải lời hứa chính xác.

**Chú thích biểu đồ:**
- **Đường xanh (tròn):** Điểm TB thực tế 2021–2025.
- **Đường đỏ (đứt, vuông):** Dự báo năm tiếp theo bằng **Trung bình trượt 3 năm**.
- **Vùng đỏ nhạt:** Khoảng dự báo ước lượng từ sai số backtest.
- Mô hình được chọn theo MAE/RMSE rolling backtest, không thay thế dự báo chính thức.

**Kết quả dự báo:**
- Dự báo **2026:** **6,497** điểm.
- Khoảng dự báo: **5,603–7,391** điểm.
- Thực tế **2025:** **6,065** điểm.
- **MAE backtest:** **0,3286** — càng nhỏ càng sát lịch sử gần.
- **RMSE backtest:** **0,4562** — phạt nặng hơn khi có lần dự báo lệch lớn.

**Phân tích:**
- Chênh lệch dự báo 2026 so với thực tế 2025: **+0.43** điểm.
- Dự báo **không cùng chiều** xu hướng 5 năm — mô hình tuyến tính có thể bị ảnh hưởng bởi năm đột biến.

**Kết luận dễ hiểu:** Nếu xu hướng 5 năm giữ nguyên, TB môn Hóa học năm tới có thể quanh **6,497** điểm — nhưng thực tế còn phụ thuộc đề thi, quy chế và số người thi.

![Dự báo Hóa học](outputs/figures/forecast_HoaHoc.png)

#### 8.4.2. Ngoại ngữ

**Điều này có nghĩa là gì?**

- Đường xanh = điểm TB thật của môn Ngoại ngữ qua các năm; đường đỏ = **ước lượng** năm tới bằng Trung bình trượt 3 năm.
- Đây là công cụ học thuật (đồ án), **không phải** thông báo điểm chính thức của Bộ.
- Hãy coi con số dự báo và khoảng dự báo là *tham khảo*, không phải lời hứa chính xác.

**Chú thích biểu đồ:**
- **Đường xanh (tròn):** Điểm TB thực tế 2021–2025.
- **Đường đỏ (đứt, vuông):** Dự báo năm tiếp theo bằng **Trung bình trượt 3 năm**.
- **Vùng đỏ nhạt:** Khoảng dự báo ước lượng từ sai số backtest.
- Mô hình được chọn theo MAE/RMSE rolling backtest, không thay thế dự báo chính thức.

**Kết quả dự báo:**
- Dự báo **2026:** **5,463** điểm.
- Khoảng dự báo: **5,313–5,613** điểm.
- Thực tế **2025:** **5,405** điểm.
- **MAE backtest:** **0,0284** — càng nhỏ càng sát lịch sử gần.
- **RMSE backtest:** **0,0286** — phạt nặng hơn khi có lần dự báo lệch lớn.

**Phân tích:**
- Chênh lệch dự báo 2026 so với thực tế 2025: **+0.06** điểm.
- Dự báo **không cùng chiều** xu hướng 5 năm — mô hình tuyến tính có thể bị ảnh hưởng bởi năm đột biến.

**Kết luận dễ hiểu:** Nếu xu hướng 5 năm giữ nguyên, TB môn Ngoại ngữ năm tới có thể quanh **5,463** điểm — nhưng thực tế còn phụ thuộc đề thi, quy chế và số người thi.

![Dự báo Ngoại ngữ](outputs/figures/forecast_NgoaiNgu.png)

#### 8.4.3. Ngữ văn

**Điều này có nghĩa là gì?**

- Đường xanh = điểm TB thật của môn Ngữ văn qua các năm; đường đỏ = **ước lượng** năm tới bằng Trung bình trượt 2 năm.
- Đây là công cụ học thuật (đồ án), **không phải** thông báo điểm chính thức của Bộ.
- Hãy coi con số dự báo và khoảng dự báo là *tham khảo*, không phải lời hứa chính xác.

**Chú thích biểu đồ:**
- **Đường xanh (tròn):** Điểm TB thực tế 2021–2025.
- **Đường đỏ (đứt, vuông):** Dự báo năm tiếp theo bằng **Trung bình trượt 2 năm**.
- **Vùng đỏ nhạt:** Khoảng dự báo ước lượng từ sai số backtest.
- Mô hình được chọn theo MAE/RMSE rolling backtest, không thay thế dự báo chính thức.

**Kết quả dự báo:**
- Dự báo **2026:** **7,117** điểm.
- Khoảng dự báo: **6,355–7,879** điểm.
- Thực tế **2025:** **7,002** điểm.
- **MAE backtest:** **0,2954** — càng nhỏ càng sát lịch sử gần.
- **RMSE backtest:** **0,3887** — phạt nặng hơn khi có lần dự báo lệch lớn.

**Phân tích:**
- Chênh lệch dự báo 2026 so với thực tế 2025: **+0.11** điểm.
- Dự báo **cùng chiều** xu hướng tăng 5 năm qua.

**Kết luận dễ hiểu:** Nếu xu hướng 5 năm giữ nguyên, TB môn Ngữ văn năm tới có thể quanh **7,117** điểm — nhưng thực tế còn phụ thuộc đề thi, quy chế và số người thi.

![Dự báo Ngữ văn](outputs/figures/forecast_NguVan.png)

#### 8.4.4. Sinh học

**Điều này có nghĩa là gì?**

- Đường xanh = điểm TB thật của môn Sinh học qua các năm; đường đỏ = **ước lượng** năm tới bằng Naive: lấy năm gần nhất.
- Đây là công cụ học thuật (đồ án), **không phải** thông báo điểm chính thức của Bộ.
- Hãy coi con số dự báo và khoảng dự báo là *tham khảo*, không phải lời hứa chính xác.

**Chú thích biểu đồ:**
- **Đường xanh (tròn):** Điểm TB thực tế 2021–2025.
- **Đường đỏ (đứt, vuông):** Dự báo năm tiếp theo bằng **Naive: lấy năm gần nhất**.
- **Vùng đỏ nhạt:** Khoảng dự báo ước lượng từ sai số backtest.
- Mô hình được chọn theo MAE/RMSE rolling backtest, không thay thế dự báo chính thức.

**Kết quả dự báo:**
- Dự báo **2026:** **5,778** điểm.
- Khoảng dự báo: **5,060–6,497** điểm.
- Thực tế **2025:** **5,778** điểm.
- **MAE backtest:** **0,3085** — càng nhỏ càng sát lịch sử gần.
- **RMSE backtest:** **0,3665** — phạt nặng hơn khi có lần dự báo lệch lớn.

**Phân tích:**
- Chênh lệch dự báo 2026 so với thực tế 2025: **+0.00** điểm.
- Dự báo **không cùng chiều** xu hướng 5 năm — mô hình tuyến tính có thể bị ảnh hưởng bởi năm đột biến.

**Kết luận dễ hiểu:** Nếu xu hướng 5 năm giữ nguyên, TB môn Sinh học năm tới có thể quanh **5,778** điểm — nhưng thực tế còn phụ thuộc đề thi, quy chế và số người thi.

![Dự báo Sinh học](outputs/figures/forecast_SinhHoc.png)

#### 8.4.5. Toán

**Điều này có nghĩa là gì?**

- Đường xanh = điểm TB thật của môn Toán qua các năm; đường đỏ = **ước lượng** năm tới bằng Trung bình trượt 3 năm.
- Đây là công cụ học thuật (đồ án), **không phải** thông báo điểm chính thức của Bộ.
- Hãy coi con số dự báo và khoảng dự báo là *tham khảo*, không phải lời hứa chính xác.

**Chú thích biểu đồ:**
- **Đường xanh (tròn):** Điểm TB thực tế 2021–2025.
- **Đường đỏ (đứt, vuông):** Dự báo năm tiếp theo bằng **Trung bình trượt 3 năm**.
- **Vùng đỏ nhạt:** Khoảng dự báo ước lượng từ sai số backtest.
- Mô hình được chọn theo MAE/RMSE rolling backtest, không thay thế dự báo chính thức.

**Kết quả dự báo:**
- Dự báo **2026:** **5,827** điểm.
- Khoảng dự báo: **3,603–8,051** điểm.
- Thực tế **2025:** **4,783** điểm.
- **MAE backtest:** **0,8044** — càng nhỏ càng sát lịch sử gần.
- **RMSE backtest:** **1,1349** — phạt nặng hơn khi có lần dự báo lệch lớn.

**Phân tích:**
- Chênh lệch dự báo 2026 so với thực tế 2025: **+1.04** điểm.
- Dự báo **không cùng chiều** xu hướng 5 năm — mô hình tuyến tính có thể bị ảnh hưởng bởi năm đột biến.
- MAE cao → nên trình bày dự báo kèm **khoảng tin cậy / giới hạn mô hình** trong báo cáo đồ án.

**Kết luận dễ hiểu:** Nếu xu hướng 5 năm giữ nguyên, TB môn Toán năm tới có thể quanh **5,827** điểm — nhưng thực tế còn phụ thuộc đề thi, quy chế và số người thi.

![Dự báo Toán](outputs/figures/forecast_Toan.png)

#### 8.4.6. Vật lý

**Điều này có nghĩa là gì?**

- Đường xanh = điểm TB thật của môn Vật lý qua các năm; đường đỏ = **ước lượng** năm tới bằng Hồi quy tuyến tính.
- Đây là công cụ học thuật (đồ án), **không phải** thông báo điểm chính thức của Bộ.
- Hãy coi con số dự báo và khoảng dự báo là *tham khảo*, không phải lời hứa chính xác.

**Chú thích biểu đồ:**
- **Đường xanh (tròn):** Điểm TB thực tế 2021–2025.
- **Đường đỏ (đứt, vuông):** Dự báo năm tiếp theo bằng **Hồi quy tuyến tính**.
- **Vùng đỏ nhạt:** Khoảng dự báo ước lượng từ sai số backtest.
- Mô hình được chọn theo MAE/RMSE rolling backtest, không thay thế dự báo chính thức.

**Kết quả dự báo:**
- Dự báo **2026:** **6,937** điểm.
- Khoảng dự báo: **6,498–7,376** điểm.
- Thực tế **2025:** **6,985** điểm.
- **MAE backtest:** **0,1761** — càng nhỏ càng sát lịch sử gần.
- **RMSE backtest:** **0,2239** — phạt nặng hơn khi có lần dự báo lệch lớn.

**Phân tích:**
- Chênh lệch dự báo 2026 so với thực tế 2025: **-0.05** điểm.
- Dự báo **không cùng chiều** xu hướng 5 năm — mô hình tuyến tính có thể bị ảnh hưởng bởi năm đột biến.

**Kết luận dễ hiểu:** Nếu xu hướng 5 năm giữ nguyên, TB môn Vật lý năm tới có thể quanh **6,937** điểm — nhưng thực tế còn phụ thuộc đề thi, quy chế và số người thi.

![Dự báo Vật lý](outputs/figures/forecast_VatLy.png)


---

## 9. Cấu trúc repository

```text
thptqg-trends/
├── .github/workflows/ci.yml
├── README.md              ← Báo cáo duy nhất (file này)
├── .env.example           ← Mẫu cấu hình đường dẫn raw CSV
├── run.ps1 / run.bat
├── colab/THPTQG_Colab.ipynb
├── data/provinces.csv
├── data/README.md
├── docs/data_dictionary.md
├── docs/report.md
├── src/                   ← Pipeline Python
├── scripts/run_all.py
├── tests/                 ← Unit tests tối thiểu
├── outputs/tables/        ← CSV tổng hợp
└── outputs/figures/       ← Biểu đồ PNG
```

---

## 10. Hướng dẫn chạy

### Google Colab (khuyên dùng nếu không có máy mạnh)

1. Mở [THPTQG_Colab.ipynb](https://colab.research.google.com/github/2274802010922/thptqg-trends/blob/main/colab/THPTQG_Colab.ipynb)
2. Chạy lần lượt các cell từ trên xuống
3. Tải dataset từ [Google Drive](https://drive.google.com/file/d/1FIU_8XT4pIC261SwYtmwTDLFP2H_WAUc/view) hoặc mount Drive
4. Chạy pipeline để sinh lại `outputs/`, `README.md`, `docs/report.md`
5. Cell cuối: zip kết quả và tải về

### Windows (máy local)

```powershell
git clone https://github.com/2274802010922/thptqg-trends.git
cd thptqg-trends
$env:THPTQG_CSV_PATH="D:\do an thuc tap\cleaned_data.csv"
.\run.ps1
```

Lệnh trên chạy `python scripts/run_all.py` → cập nhật **README.md**, `docs/report.md` và thư mục `outputs/`.

---

## 11. Kết quả đầu ra (outputs)

| File | Mô tả | Ai cần đọc? |
|------|--------|-------------|
| `README.md` | Báo cáo đầy đủ (tự cập nhật) | Mọi người |
| `docs/report.md` | Báo cáo học thuật theo cấu trúc đồ án | Hội đồng / giảng viên |
| `data/README.md` | Thông tin raw data và cách cấu hình | Người muốn chạy lại |
| `docs/data_dictionary.md` | Giải thích schema dữ liệu | Người kiểm chứng dữ liệu |
| `tests/` | Kiểm tra logic xử lý và dự báo bằng dữ liệu mẫu | Người review code |
| `outputs/tables/*.csv` | Bảng số liệu thô đã tổng hợp | Người muốn tự vẽ biểu đồ / kiểm chứng |
| `outputs/figures/*.png` | Biểu đồ tổng quan, heatmap, dự báo | Slide, báo cáo miệng |

---

## 12. Giới hạn & lưu ý

| Giới hạn | Giải thích đơn giản |
|----------|---------------------|
| Dự báo 2026 | Chỉ là **ước lượng học thuật**, không thay thế thông tin Bộ GD&ĐT |
| Raw data | Không push lên GitHub vì quá lớn; tải qua Google Drive hoặc đặt local path |
| Điểm 0.0 | = không thi môn → khi TB giảm, xem thêm **số người thi** |
| So sánh tỉnh | Tỉnh ít thí sinh thi môn → số liệu dễ **lệch** |
| Quyền riêng tư | Không public từng dòng `SBD` nếu không cần thiết |

---

*Tái tạo báo cáo: `python scripts/run_all.py` hoặc `.\run.ps1`*
