"""Sinh cac muc insight DA nang cao cho README va docs/report.md."""
from __future__ import annotations

from pathlib import Path

import pandas as pd

from .config import FIGURES_DIR, MAIN_SUBJECTS, TABLES_DIR, YEAR_MAX, YEAR_MIN
from .labels import fmt_float, fmt_int, subject_vi


def _read_table(name: str) -> pd.DataFrame:
    path = Path(TABLES_DIR) / name
    return pd.read_csv(path) if path.exists() else pd.DataFrame()


def _md_table(df: pd.DataFrame, columns: list[str], max_rows: int = 10) -> list[str]:
    if df.empty:
        return ["_Chưa có dữ liệu._"]
    view = df.head(max_rows)
    lines = ["| " + " | ".join(columns) + " |", "| " + " | ".join("---" for _ in columns) + " |"]
    for _, r in view.iterrows():
        lines.append("| " + " | ".join(str(r.get(c, "")) for c in columns) + " |")
    return lines


def _figure(path: str, alt: str) -> list[str]:
    if (Path(FIGURES_DIR) / path).exists():
        return [f"![{alt}](outputs/figures/{path})", ""]
    return []


def _quality_section() -> list[str]:
    summary = _read_table("data_quality_summary.csv")
    missing = _read_table("missing_by_subject_year.csv")
    lines = ["### 6.5. Data quality — dữ liệu có đủ tin cậy để phân tích không?", ""]
    if not summary.empty:
        key = {r["metric"]: r for _, r in summary.iterrows()}
        lines += [
            f"- Số dòng trong phạm vi {YEAR_MIN}-{YEAR_MAX}: **{fmt_int(key.get('filtered_rows', {}).get('value'))}**.",
            f"- Số tỉnh/thành xuất hiện: **{fmt_int(key.get('province_count', {}).get('value'))}**.",
            f"- Ô điểm ngoài khoảng 0-10: **{fmt_int(key.get('invalid_score_cells', {}).get('value'))}**.",
            f"- Ô điểm `0.0`: **{fmt_int(key.get('zero_score_cells', {}).get('value'))}** — được xem là không thi môn, không đưa vào TB môn.",
            f"- Trùng khóa `Nam + SBD`: **{fmt_int(key.get('duplicate_sbd_year_count', {}).get('value'))}** dòng.",
            "",
        ]
    if not missing.empty:
        last = missing[missing["Nam"] == YEAR_MAX].copy()
        last["Môn"] = last["Mon"].map(subject_vi)
        last["Tỷ lệ 0.0"] = last["zero_pct"].map(lambda x: f"{x:.1f}%")
        last["Tỷ lệ thiếu"] = last["missing_pct"].map(lambda x: f"{x:.2f}%")
        lines += [
            "**Môn có tỷ lệ 0.0 cao nhất năm cuối** — thường là môn tự chọn hoặc môn chỉ xuất hiện ở chương trình mới:",
            "",
            *_md_table(last.sort_values("zero_pct", ascending=False), ["Môn", "Tỷ lệ 0.0", "Tỷ lệ thiếu"], 6),
            "",
            "**Insight:** kiểm tra `0.0` là bước bắt buộc. Nếu tính cả 0.0 vào trung bình, điểm các môn tự chọn sẽ bị kéo xuống sai bản chất.",
            "",
        ]
    return lines


def _distribution_section() -> list[str]:
    dist = _read_table("score_distribution_by_year_subject.csv")
    bands = _read_table("score_bands_by_year_subject.csv")
    lines = ["### 6.6. Phân phối điểm — không chỉ nhìn điểm trung bình", ""]
    if dist.empty:
        return lines + ["_Chưa có bảng phân phối điểm._", ""]
    last = dist[dist["Nam"] == YEAR_MAX].copy()
    last["Môn"] = last["Mon"].map(subject_vi)
    if not bands.empty:
        last = last.merge(bands[bands["Nam"] == YEAR_MAX][["Mon", "pct_lt_5", "pct_ge_8"]], on="Mon", how="left")
    last["Median"] = last["median"].map(lambda x: fmt_float(x))
    last["P10"] = last["p10"].map(lambda x: fmt_float(x))
    last["P90"] = last["p90"].map(lambda x: fmt_float(x))
    last["IQR"] = last["iqr"].map(lambda x: fmt_float(x))
    last["% < 5"] = last.get("pct_lt_5", pd.Series(dtype=float)).map(lambda x: f"{x:.1f}%" if pd.notna(x) else "—")
    last["% >= 8"] = last.get("pct_ge_8", pd.Series(dtype=float)).map(lambda x: f"{x:.1f}%" if pd.notna(x) else "—")
    lines += [
        "Phân phối giúp trả lời câu hỏi: điểm trung bình thay đổi vì cả phổ điểm dịch chuyển hay chỉ vì nhóm điểm thấp/cao thay đổi.",
        "",
        *_md_table(last.sort_values("iqr", ascending=False), ["Môn", "Median", "P10", "P90", "IQR", "% < 5", "% >= 8"], 10),
        "",
    ]
    widest = last.sort_values("iqr", ascending=False).head(1)
    if not widest.empty:
        r = widest.iloc[0]
        lines.append(f"**Insight:** năm {YEAR_MAX}, môn có độ phân tán lớn nhất theo IQR là **{r['Môn']}**; môn này cần đọc thêm histogram/boxplot thay vì chỉ kết luận bằng điểm trung bình.")
        lines.append("")
    return lines


def _yearly_change_section() -> list[str]:
    yearly = _read_table("yearly_change_by_subject.csv")
    lines = ["### 6.7. Biến động theo năm — năm nào là điểm gãy?", ""]
    if yearly.empty:
        return lines + ["_Chưa có bảng biến động theo năm._", ""]
    y = yearly.dropna(subset=["mean_change_pct"]).copy()
    y["Môn"] = y["Mon"].map(subject_vi)
    y["ĐTB"] = y["mean"].map(lambda x: fmt_float(x))
    y["Δ ĐTB"] = y["mean_change"].map(lambda x: f"{x:+.2f}")
    y["Δ %"] = y["mean_change_pct"].map(lambda x: f"{x:+.1f}%")
    y["Δ % <5"] = y["pct_lt_5_change"].map(lambda x: f"{x:+.1f}%" if pd.notna(x) else "—")
    y["Δ % >=8"] = y["pct_ge_8_change"].map(lambda x: f"{x:+.1f}%" if pd.notna(x) else "—")
    lines += [
        "Các dòng dưới đây là các biến động mạnh nhất theo năm; đây là nơi hội đồng thường hỏi “vì sao năm đó khác?”.",
        "",
        *_md_table(y.assign(abs_change=y["mean_change_pct"].abs()).sort_values("abs_change", ascending=False), ["Nam", "Môn", "ĐTB", "Δ ĐTB", "Δ %", "Δ % <5", "Δ % >=8"], 10),
        "",
        "**Insight:** phần này chuyển dự án từ mô tả “môn A tăng/giảm” sang phân tích “năm nào làm xu hướng đổi mạnh, và nhóm điểm nào kéo xu hướng đó”.",
        "",
    ]
    return lines


def _region_anomaly_section() -> list[str]:
    region = _read_table("by_region_subject_year.csv")
    anomalies = _read_table("province_anomalies.csv")
    volatility = _read_table("province_volatility.csv")
    lines = ["### 6.8. Phân tích tỉnh/vùng và bất thường", ""]
    if not region.empty:
        focus = region[(region["Nam"] == YEAR_MAX) & (region["Mon"] == "Toan")].copy()
        focus["Vùng"] = focus["Vung"]
        focus["ĐTB Toán"] = focus["mean"].map(lambda x: fmt_float(x))
        focus["% >= 8"] = focus["pct_ge_8"].map(lambda x: f"{x:.1f}%")
        focus["Số TS"] = focus["count"].map(fmt_int)
        lines += [
            f"**So sánh vùng môn Toán năm {YEAR_MAX}:**",
            "",
            *_md_table(focus.sort_values("mean", ascending=False), ["Vùng", "ĐTB Toán", "% >= 8", "Số TS"], 10),
            "",
        ]
    if not anomalies.empty:
        a = anomalies.copy()
        a["Môn"] = a["Mon"].map(subject_vi)
        a["Tỉnh"] = a["TenTinh"]
        a["ĐTB tỉnh"] = a["mean"].map(lambda x: fmt_float(x))
        a["Δ quốc gia"] = a["delta_from_national"].map(lambda x: f"{x:+.2f}")
        lines += [
            "**Một số tỉnh/năm lệch mạnh so với mặt bằng quốc gia:**",
            "",
            *_md_table(a, ["Nam", "Tỉnh", "Môn", "ĐTB tỉnh", "Δ quốc gia", "z_score"], 10),
            "",
        ]
    if not volatility.empty:
        v = volatility.copy()
        v["Môn"] = v["Mon"].map(subject_vi)
        v["Tỉnh"] = v["TenTinh"]
        v["Max YoY"] = v["max_yoy_abs_change"].map(lambda x: fmt_float(x))
        lines += [
            "**Tỉnh có biến động mạnh giữa hai năm liên tiếp:**",
            "",
            *_md_table(v, ["Tỉnh", "Môn", "Max YoY", "latest_count"], 10),
            "",
            "**Insight:** top/bottom tỉnh chỉ cho biết thứ hạng tại một năm; anomaly và volatility cho biết nơi nào cần kiểm tra sâu vì biến động khác thường.",
            "",
        ]
    return lines


def _correlation_combination_section() -> list[str]:
    corr = _read_table("subject_correlation_by_year.csv")
    combo = _read_table("combination_scores_by_year.csv")
    lines = ["### 6.9. Tương quan môn học và tổ hợp xét tuyển", ""]
    if not corr.empty:
        c = corr[corr["Nam"] == YEAR_MAX].copy()
        c = c.dropna(subset=["correlation"]).sort_values("correlation", ascending=False)
        c["Môn X"] = c["MonX"].map(subject_vi)
        c["Môn Y"] = c["MonY"].map(subject_vi)
        c["Corr"] = c["correlation"].map(lambda x: f"{x:.2f}")
        c["Số cặp"] = c["n_pair"].map(fmt_int)
        lines += [
            f"**Các cặp môn tương quan cao nhất năm {YEAR_MAX}:**",
            "",
            *_md_table(c, ["Môn X", "Môn Y", "Corr", "Số cặp"], 10),
            "",
        ]
    if not combo.empty:
        focus = combo[(combo["Nam"] == YEAR_MAX) & (combo["ToHop"].isin(["KhoiA", "KhoiA1", "KhoiB", "KhoiC", "KhoiD", "KHTN", "KHXH"]))].copy()
        focus["Tổ hợp"] = focus["ToHop"]
        focus["ĐTB"] = focus["mean"].map(lambda x: fmt_float(x))
        focus["% >=24"] = focus["pct_ge_24"].map(lambda x: f"{x:.1f}%")
        focus["% <15"] = focus["pct_lt_15"].map(lambda x: f"{x:.1f}%")
        lines += [
            f"**Tổ hợp/khối thi năm {YEAR_MAX}:**",
            "",
            *_md_table(focus.sort_values("mean", ascending=False), ["Tổ hợp", "ĐTB", "% >=24", "% <15"], 10),
            "",
            "**Insight:** tương quan và tổ hợp môn giúp dự án tiến gần bài toán DA thực tế hơn: không chỉ hỏi từng môn riêng lẻ, mà xem cấu trúc điểm giữa các môn có đi cùng nhau không.",
            "",
        ]
    return lines


def _forecast_reliability_section() -> list[str]:
    rel = _read_table("forecast_reliability.csv")
    lines = ["### 7.1. Độ tin cậy của forecast", ""]
    if rel.empty:
        return lines + ["_Chưa có bảng độ tin cậy forecast._", ""]
    r = rel.copy()
    r["Môn"] = r["Mon"].map(subject_vi)
    r["Dự báo"] = r["forecast_mean"].map(lambda x: fmt_float(x, 3))
    r["Độ tin cậy"] = r["reliability_label"]
    r["Ghi chú"] = r["reliability_note"]
    lines += [
        "Vì chuỗi chỉ có 5 năm, forecast được chấm độ tin cậy riêng để tránh trình bày như dự đoán chắc chắn.",
        "",
        *_md_table(r, ["Môn", "Dự báo", "Độ tin cậy", "Ghi chú"], 10),
        "",
    ]
    return lines


def build_advanced_results_section() -> str:
    lines = []
    lines += _quality_section()
    lines += _distribution_section()
    lines += _yearly_change_section()
    lines += _region_anomaly_section()
    lines += _correlation_combination_section()
    return "\n".join(lines)


def build_forecast_reliability_section() -> str:
    return "\n".join(_forecast_reliability_section())


def build_advanced_charts_section() -> str:
    lines = [
        "### 8.5. Biểu đồ phân tích nâng cao",
        "",
        "Các hình dưới đây là phần nâng cấp để project không dừng ở thống kê trung bình: kiểm tra chất lượng dữ liệu, phân phối, biến động năm, vùng, tương quan và forecast reliability.",
        "",
    ]
    lines += _figure("data_quality_missingness.png", "Data quality")
    for subject in ["Toan", "NgoaiNgu", "LichSu"]:
        lines += _figure(f"score_bands_{subject}.png", f"Dải điểm {subject_vi(subject)}")
        lines += _figure(f"histogram_{subject}_{YEAR_MAX}.png", f"Histogram {subject_vi(subject)}")
        lines += _figure(f"boxplot_{subject}_by_year.png", f"Boxplot {subject_vi(subject)}")
    lines += _figure("yoy_change_heatmap.png", "YoY heatmap")
    for subject in ["Toan", "NgoaiNgu"]:
        lines += _figure(f"region_comparison_{subject}.png", f"So sánh vùng {subject_vi(subject)}")
        lines += _figure(f"province_volatility_{subject}.png", f"Biến động tỉnh {subject_vi(subject)}")
    lines += _figure(f"correlation_heatmap_{YEAR_MAX}.png", "Correlation heatmap")
    lines += _figure("combination_trends.png", "Combination trends")
    for subject in MAIN_SUBJECTS:
        lines += _figure(f"backtest_actual_vs_predicted_{subject}.png", f"Backtest {subject_vi(subject)}")
    return "\n".join(lines)


def build_report_advanced_sections() -> str:
    advanced = build_advanced_results_section()
    replacements = {
        "### 6.5.": "### 8.1.",
        "### 6.6.": "### 8.2.",
        "### 6.7.": "### 8.3.",
        "### 6.8.": "### 8.4.",
        "### 6.9.": "### 8.5.",
    }
    for old, new in replacements.items():
        advanced = advanced.replace(old, new)
    reliability = build_forecast_reliability_section().replace("### 7.1.", "### 9.1.")
    lines = [
        "## 8. Phân Tích DA Nâng Cao",
        "",
        "Phần này bổ sung lớp phân tích chẩn đoán để đồ án không chỉ dừng ở thống kê mô tả.",
        "",
        advanced,
        "",
        "## 9. Đánh Giá Độ Tin Cậy Forecast",
        "",
        reliability,
    ]
    return "\n".join(lines)
