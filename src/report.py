"""Sinh báo cáo học thuật từ các bảng output."""
from __future__ import annotations

from datetime import datetime
from pathlib import Path
import json

import pandas as pd

from .advanced_report import build_report_advanced_sections
from .config import (
    CSV_PATH,
    DOCS_DIR,
    RAW_DATA_DRIVE_URL,
    RAW_DATA_SHA256,
    RAW_DATA_TOTAL_ROWS,
    RAW_DATA_YEAR_COUNTS,
    TABLES_DIR,
    YEAR_MAX,
    YEAR_MIN,
)
from .labels import fmt_float, fmt_int, subject_vi


def _pct_change(first, last):
    if first is None or last is None or first == 0:
        return None
    return round((last - first) / first * 100, 2)


def build_trends_table(by_year_subject: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for mon, g in by_year_subject.groupby("Mon"):
        g = g.dropna(subset=["mean"]).sort_values("Nam")
        if g.empty:
            continue
        first, last = g.iloc[0], g.iloc[-1]
        rows.append(
            {
                "Mon": mon,
                "Môn": subject_vi(mon),
                "mean_first": first["mean"],
                "mean_last": last["mean"],
                "change_pct": _pct_change(first["mean"], last["mean"]),
                "pct_ge_8_last": last.get("pct_ge_8"),
            }
        )
    return pd.DataFrame(rows).sort_values("Môn")


def top_bottom_provinces(named: pd.DataFrame, year: int, subject: str = "Toan", n: int = 10):
    df = named[(named["Nam"] == year) & (named["Mon"] == subject)].dropna(subset=["mean"])
    df = df.sort_values("mean", ascending=False)
    top = df.head(n)[["TenTinh", "mean", "count"]]
    bottom = df.tail(n).sort_values("mean")[["TenTinh", "mean", "count"]]
    return top, bottom


def _markdown_table(df: pd.DataFrame, columns: list[str]) -> list[str]:
    if df.empty:
        return ["_Không có dữ liệu._"]
    rows = ["| " + " | ".join(columns) + " |", "| " + " | ".join("---" for _ in columns) + " |"]
    for _, r in df.iterrows():
        rows.append("| " + " | ".join(str(r.get(c, "")) for c in columns) + " |")
    return rows


def generate_report(out_path: Path | None = None) -> Path:
    docs_dir = Path(DOCS_DIR)
    docs_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_path or docs_dir / "report.md"

    tables = Path(TABLES_DIR)
    by_ys = pd.read_csv(tables / "by_year_subject.csv")
    cand = pd.read_csv(tables / "candidates_by_year.csv")
    named = pd.read_csv(tables / "by_year_province_subject_named.csv")
    forecast = pd.read_csv(tables / "forecast_next_year.csv")
    model_cmp = pd.read_csv(tables / "model_comparison.csv") if (tables / "model_comparison.csv").exists() else pd.DataFrame()

    trends = build_trends_table(by_ys)
    trends.to_csv(tables / "trends_summary.csv", index=False)
    top, bottom = top_bottom_provinces(named, YEAR_MAX, "Toan")

    trend_view = trends.copy()
    trend_view["TB đầu"] = trend_view["mean_first"].map(lambda x: fmt_float(x))
    trend_view["TB cuối"] = trend_view["mean_last"].map(lambda x: fmt_float(x))
    trend_view["Thay đổi"] = trend_view["change_pct"].map(lambda x: f"{x:+.2f}%" if pd.notna(x) else "—")
    trend_view["% >= 8 cuối"] = trend_view["pct_ge_8_last"].map(lambda x: f"{x:.1f}%" if pd.notna(x) else "—")

    forecast_view = forecast.copy()
    forecast_view["Môn"] = forecast_view["Mon"].map(subject_vi)
    forecast_view["Mô hình"] = forecast_view["selected_model_label"]
    forecast_view["Dự báo"] = forecast_view["forecast_mean"].map(lambda x: fmt_float(x, 3))
    forecast_view["Khoảng"] = forecast_view.apply(
        lambda r: f"{fmt_float(r['forecast_lower'], 3)}-{fmt_float(r['forecast_upper'], 3)}"
        if pd.notna(r.get("forecast_lower")) and pd.notna(r.get("forecast_upper"))
        else "—",
        axis=1,
    )
    forecast_view["MAE"] = forecast_view["backtest_mae"].map(lambda x: fmt_float(x, 4) if pd.notna(x) else "—")
    forecast_view["RMSE"] = forecast_view["backtest_rmse"].map(lambda x: fmt_float(x, 4) if pd.notna(x) else "—")

    selected_cmp = pd.DataFrame()
    if not model_cmp.empty:
        selected_cmp = model_cmp[model_cmp["is_selected"] == True].copy()
        selected_cmp["Môn"] = selected_cmp["Mon"].map(subject_vi)
        selected_cmp["Mô hình"] = selected_cmp["model_label"]
        selected_cmp["MAE"] = selected_cmp["mae"].map(lambda x: fmt_float(x, 4))
        selected_cmp["RMSE"] = selected_cmp["rmse"].map(lambda x: fmt_float(x, 4))
        selected_cmp["MAPE"] = selected_cmp["mape"].map(lambda x: f"{x:.2f}%" if pd.notna(x) else "—")

    lines = [
        "# Báo Cáo Đồ Án: Phân Tích Và Dự Báo Điểm Thi THPTQG",
        "",
        f"**Ngày tạo:** {datetime.now():%d/%m/%Y %H:%M}",
        f"**Phạm vi nghiên cứu:** {YEAR_MIN}-{YEAR_MAX}",
        f"**Đường dẫn dữ liệu khi chạy:** `{CSV_PATH}`",
        "",
        "## 1. Giới Thiệu",
        "",
        "Đề tài phân tích dữ liệu điểm thi tốt nghiệp THPTQG theo năm, môn và tỉnh/thành, sau đó dự báo xu hướng điểm trung bình của một số môn chính trong năm tiếp theo. Sản phẩm chính thức là repository GitHub; raw CSV được lưu ngoài GitHub vì dung lượng lớn.",
        "",
        "## 2. Mục Tiêu",
        "",
        "- Mô tả quy mô thí sinh giai đoạn 2021-2025.",
        "- Phân tích xu hướng điểm trung bình, tỷ lệ điểm cao và chênh lệch giữa tỉnh/thành.",
        "- Xây dựng pipeline dự báo điểm trung bình năm tiếp theo ở cấp toàn quốc.",
        "- Đánh giá mô hình bằng rolling backtest thay vì chỉ đưa ra con số dự báo.",
        "",
        "## 3. Dữ Liệu",
        "",
        f"- Nguồn raw CSV: {RAW_DATA_DRIVE_URL}",
        f"- SHA256: `{RAW_DATA_SHA256}`",
        f"- Tổng số dòng raw: **{fmt_int(RAW_DATA_TOTAL_ROWS)}**.",
        f"- Phạm vi raw: **{min(RAW_DATA_YEAR_COUNTS)}-{max(RAW_DATA_YEAR_COUNTS)}**.",
        f"- Phạm vi dùng trong đồ án: **{YEAR_MIN}-{YEAR_MAX}**.",
        "",
        "| Năm | Số dòng raw |",
        "|-----|-------------|",
    ]
    for year, count in RAW_DATA_YEAR_COUNTS.items():
        lines.append(f"| {year} | {fmt_int(count)} |")

    lines += [
        "",
        "Quy ước tiền xử lý quan trọng: điểm `0.0` ở một môn được xem là thí sinh không thi môn đó, nên không tính vào điểm trung bình môn.",
        "",
        "## 4. Tiền Xử Lý Và Tổng Hợp",
        "",
        "Pipeline đọc CSV theo chunk để xử lý file lớn, lọc phạm vi năm, sau đó tổng hợp theo năm, môn và tỉnh. Các bảng tổng hợp nằm trong `outputs/tables/`, còn biểu đồ nằm trong `outputs/figures/`.",
        "",
        "## 5. Kết Quả EDA Chính",
        "",
        f"Tổng số thí sinh trong phạm vi {YEAR_MIN}-{YEAR_MAX}: **{fmt_int(int(cand['SoThiSinh'].sum()))}**.",
        "",
        "| Năm | Số thí sinh |",
        "|-----|-------------|",
    ]
    for _, r in cand.iterrows():
        lines.append(f"| {int(r['Nam'])} | {fmt_int(int(r['SoThiSinh']))} |")

    lines += [
        "",
        "### Xu Hướng Theo Môn",
        "",
        *_markdown_table(trend_view, ["Môn", "TB đầu", "TB cuối", "Thay đổi", "% >= 8 cuối"]),
        "",
        f"### Top/Bottom Tỉnh Theo Toán {YEAR_MAX}",
        "",
        "**Top 10:**",
    ]
    for i, (_, r) in enumerate(top.iterrows(), 1):
        lines.append(f"{i}. {r['TenTinh']}: {fmt_float(r['mean'])} ({fmt_int(int(r['count']))} thí sinh)")
    lines += ["", "**Bottom 10:**"]
    for i, (_, r) in enumerate(bottom.iterrows(), 1):
        lines.append(f"{i}. {r['TenTinh']}: {fmt_float(r['mean'])} ({fmt_int(int(r['count']))} thí sinh)")

    lines += [
        "",
        "## 6. Phương Pháp Dự Báo",
        "",
        "Các mô hình được so sánh gồm naive forecast, trung bình trượt 2 năm, trung bình trượt 3 năm, hồi quy tuyến tính và san bằng mũ đơn. Mỗi môn được chọn mô hình tốt nhất dựa trên MAE/RMSE từ rolling backtest.",
        "",
        "## 7. Thực Nghiệm Và Kết Quả Dự Báo",
        "",
        *_markdown_table(selected_cmp, ["Môn", "Mô hình", "MAE", "RMSE", "MAPE"]),
        "",
        "### Dự Báo Năm Tiếp Theo",
        "",
        *_markdown_table(forecast_view, ["Môn", "Mô hình", "Dự báo", "Khoảng", "MAE", "RMSE"]),
        "",
        build_report_advanced_sections(),
        "",
        "## 10. Hạn Chế",
        "",
        "- Chỉ có 5 điểm thời gian chính trong phạm vi nghiên cứu, nên dự báo phải xem là xu hướng tham khảo.",
        "- Thay đổi cấu trúc đề thi, quy chế thi hoặc nhóm thí sinh có thể làm mô hình sai lệch.",
        "- Một số môn năm 2025 có cấu trúc mới hoặc số lượng thí sinh thay đổi mạnh, cần diễn giải thận trọng.",
        "- Dự báo ở cấp tổng hợp, không dự đoán điểm cá nhân hay điểm của từng trường.",
        "",
        "## 11. Hướng Phát Triển",
        "",
        "- Bổ sung dữ liệu các năm tiếp theo để tăng độ ổn định của mô hình.",
        "- Mở rộng phân tích phân phối điểm sang cấp tỉnh/vùng nếu tài nguyên xử lý cho phép.",
        "- Thử mô hình phân cấp theo tỉnh nếu dữ liệu nhiều năm hơn.",
        "- Xuất report PDF và slide bảo vệ tự động từ pipeline.",
        "",
        "## 12. Kết Luận",
        "",
        "Project đã có pipeline tái lập từ raw CSV đến bảng, biểu đồ, báo cáo và dự báo. Phần dự báo được cải thiện bằng cách so sánh nhiều mô hình và đánh giá bằng rolling backtest, phù hợp hơn với yêu cầu của một đồ án phân tích dữ liệu.",
    ]

    out_path.write_text("\n".join(lines), encoding="utf-8")

    profile = {
        "csv": str(CSV_PATH),
        "year_min": YEAR_MIN,
        "year_max": YEAR_MAX,
        "total_candidates": int(cand["SoThiSinh"].sum()),
        "generated_at": datetime.now().isoformat(),
    }
    (tables / "data_profile.json").write_text(json.dumps(profile, indent=2, ensure_ascii=False), encoding="utf-8")
    return out_path
