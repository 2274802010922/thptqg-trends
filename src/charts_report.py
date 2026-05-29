"""Sinh phan bao cao chi tiet cho tung bieu do trong README."""
from __future__ import annotations

from pathlib import Path

import pandas as pd

from .config import FIGURES_DIR, TABLES_DIR, YEAR_MAX, YEAR_MIN
from .labels import fmt_float, fmt_int, subject_vi


def _trend_comment(change_pct: float | None) -> str:
    if change_pct is None or pd.isna(change_pct):
        return "Chưa đủ dữ liệu để mô tả xu hướng dài hạn."
    if change_pct > 5:
        return f"Trong 5 năm, điểm trung bình **tăng {change_pct:+.1f}%**, cho thấy môn này có xu hướng cải thiện hoặc thay đổi cơ cấu thí sinh thi."
    if change_pct < -5:
        return f"Trong 5 năm, điểm trung bình **giảm {change_pct:+.1f}%**. Cần đọc kèm cột *Số thí sinh* — giảm TB có thể do thay đổi nhóm thí sinh tham gia thi môn."
    return f"Điểm trung bình **ổn định** qua 5 năm (biến động {change_pct:+.1f}%)."


def _subject_detail(by_ys: pd.DataFrame, mon: str) -> dict:
    sub = by_ys[by_ys["Mon"] == mon].dropna(subset=["mean"]).sort_values("Nam")
    if sub.empty:
        return {}
    first, last = sub.iloc[0], sub.iloc[-1]
    change = None
    if first["mean"] and first["mean"] != 0:
        change = (last["mean"] - first["mean"]) / first["mean"] * 100

    yoy = []
    years = sub["Nam"].tolist()
    means = sub["mean"].tolist()
    for i in range(1, len(years)):
        if means[i - 1]:
            yoy.append((int(years[i]), (means[i] - means[i - 1]) / means[i - 1] * 100))
    steepest_up = max(yoy, key=lambda x: x[1]) if yoy else None
    steepest_down = min(yoy, key=lambda x: x[1]) if yoy else None

    return {
        "mon": mon,
        "name": subject_vi(mon),
        "mean_first": first["mean"],
        "mean_last": last["mean"],
        "change_pct": change,
        "pct_ge_8_last": last.get("pct_ge_8"),
        "count_first": sub.iloc[0].get("count"),
        "count_last": last.get("count"),
        "series": sub[["Nam", "mean", "pct_ge_8", "count"]].to_dict("records"),
        "steepest_up": steepest_up,
        "steepest_down": steepest_down,
        "min_mean": float(sub["mean"].min()),
        "max_mean": float(sub["mean"].max()),
        "min_year": int(sub.loc[sub["mean"].idxmin(), "Nam"]),
        "max_year": int(sub.loc[sub["mean"].idxmax(), "Nam"]),
    }


def _layperson_box(title: str, sentences: list[str]) -> list[str]:
    """Đoạn giải thích ngắn cho người không chuyên."""
    out = [f"**{title}**", ""]
    for s in sentences:
        out.append(f"- {s}")
    out.append("")
    return out


def _analyze_candidates(cand: pd.DataFrame) -> list[str]:
    n2021 = int(cand.iloc[0]["SoThiSinh"]) if len(cand) else 0
    n2025 = int(cand.iloc[-1]["SoThiSinh"]) if len(cand) else 0
    lines = _layperson_box(
        "Điều này có nghĩa là gì?",
        [
            "Hình này trả lời câu hỏi: *Mỗi năm có bao nhiêu học sinh thi?*",
            "Cột cao hơn năm trước = kỳ thi quy mô lớn hơn (nhiều hồ sơ, nhiều dữ liệu hơn).",
            f"Từ {YEAR_MIN} đến {YEAR_MAX}, số thí sinh tăng từ {fmt_int(n2021)} lên {fmt_int(n2025)} — "
            "khi đọc các biểu đồ điểm, hãy nhớ quy mô thí sinh cũng đã thay đổi.",
        ],
    )
    lines += [
        "**Chú thích biểu đồ:**",
        "- **Trục hoành (X):** Năm thi.",
        "- **Trục tung (Y):** Tổng số thí sinh có mặt trong dữ liệu mỗi năm.",
        "- **Ý nghĩa:** Đo quy mô kỳ thi — tăng dần cho thấy áp lực hồ sơ và khối lượng dữ liệu xử lý tăng theo thời gian.",
        "",
        "**Số liệu chi tiết:**",
    ]
    prev = None
    for _, r in cand.iterrows():
        n = int(r["SoThiSinh"])
        y = int(r["Nam"])
        if prev:
            lines.append(f"- **{y}:** {fmt_int(n)} thí sinh (tăng {fmt_int(n - prev)}, ~{(n - prev) / prev * 100:.1f}% so với {y - 1})")
        else:
            lines.append(f"- **{y}:** {fmt_int(n)} thí sinh")
        prev = n
    total = int(cand["SoThiSinh"].sum())
    lines += [
        "",
        "**Phân tích:**",
        f"- Tổng cộng **{fmt_int(total)}** lượt thí sinh trong {len(cand)} năm.",
        f"- Năm **{int(cand.iloc[-1]['Nam'])}** ghi nhận quy mô lớn nhất ({fmt_int(int(cand.iloc[-1]['SoThiSinh']))} thí sinh).",
        "- Xu hướng tăng liên tục gợi ý nhu cầu phân tích theo năm phải chuẩn hoá (tránh so sánh tuyệt đối khi tổng thí sinh đã thay đổi).",
        "",
        "**Kết luận dễ hiểu:** Kỳ thi ngày càng **đông thí sinh**. Điều này không tự nói lên điểm cao hay thấp, nhưng ảnh hưởng cách ta hiểu các biểu đồ điểm phía sau.",
    ]
    return lines


def _analyze_pct_ge_8(by_ys: pd.DataFrame) -> list[str]:
    last = by_ys[by_ys["Nam"] == YEAR_MAX].dropna(subset=["pct_ge_8"])
    last = last[last["count"] > 0].sort_values("pct_ge_8", ascending=False)
    top3 = last.head(3)
    bot3 = last.tail(3).sort_values("pct_ge_8")

    lines = _layperson_box(
        "Điều này có nghĩa là gì?",
        [
            "Thay vì nhìn điểm trung bình, hình này hỏi: *Bao nhiêu phần trăm học sinh đạt điểm khá (từ 8 trở lên)?*",
            "Một môn có đường cao = nhiều người đạt điểm tốt hơn so với môn có đường thấp.",
            "Đường đi xuống theo năm = tỷ lệ học sinh đạt ≥ 8 đang giảm (có thể do đề khó hơn, hoặc nhiều người hơn thi môn đó).",
        ],
    )
    lines += [
        "**Chú thích biểu đồ:**",
        "- Mỗi đường = một môn thi.",
        "- **Trục Y:** Tỷ lệ (%) thí sinh **có thi môn đó** đạt **≥ 8.0 điểm**.",
        "- Giúp so sánh *độ khó tương đối* và *tỷ lệ học sinh giỏi* giữa các môn qua từng năm.",
        "",
        f"**Năm {YEAR_MAX} — môn có tỷ lệ ≥ 8 cao nhất:**",
    ]
    for _, r in top3.iterrows():
        lines.append(f"- **{subject_vi(r['Mon'])}:** {r['pct_ge_8']:.1f}%")
    lines += [f"", f"**Năm {YEAR_MAX} — tỷ lệ ≥ 8 thấp nhất:**"]
    for _, r in bot3.iterrows():
        lines.append(f"- **{subject_vi(r['Mon'])}:** {r['pct_ge_8']:.1f}%")
    lines += [
        "",
        "**Phân tích:**",
        "- Môn có đường cao và ổn định (vd. GDCD) thường vẫn duy trì tỷ lệ điểm khá.",
        "- Môn có đường sụt mạnh (vd. Toán, Ngoại ngữ) phản ánh cả chất lượng lẫn thay đổi số lượng thí sinh thi môn.",
        "- Nên đọc kết hợp biểu đồ này với biểu đồ điểm TB từng môn (mục 8.2).",
        "",
        "**Kết luận dễ hiểu:** Môn nào **dễ lấy điểm cao** hơn sẽ có đường nằm trên; môn **khó** hoặc **ít người giỏi** sẽ nằm dưới. So sánh giữa các môn hợp lý hơn so sánh điểm tuyệt đối giữa Toán và GDCD.",
    ]
    return lines


def _analyze_subject_mean(info: dict) -> list[str]:
    ch = f"{info['change_pct']:+.1f}%" if info["change_pct"] is not None else "—"
    trend_plain = "ổn định"
    if info["change_pct"] is not None:
        if info["change_pct"] > 5:
            trend_plain = "cải thiện dần"
        elif info["change_pct"] < -5:
            trend_plain = "giảm dần"
    lines = _layperson_box(
        "Điều này có nghĩa là gì?",
        [
            f"Biểu đồ cho biết **điểm trung bình cả nước** môn {info['name']} mỗi năm — giống điểm TB chung của cả lớp quốc gia.",
            f"5 năm qua môn này **{trend_plain}** (TB {YEAR_MIN}: {fmt_float(info['mean_first'])} → {YEAR_MAX}: {fmt_float(info['mean_last'])}).",
            "Con số trên đỉnh mỗi cột/điểm trên đường là điểm TB chính xác của năm đó.",
        ],
    )
    lines += [
        "**Chú thích biểu đồ:**",
        "- **Trục X:** Năm.",
        "- **Trục Y:** Điểm trung bình toàn quốc (chỉ tính thí sinh **có điểm > 0**, tức đã thi môn).",
        "- Điểm ghi trên đỉnh mỗi năm (trên hình) là giá trị TB tương ứng.",
        "",
        "**Tóm tắt số liệu:**",
        f"- TB **{YEAR_MIN}:** {fmt_float(info['mean_first'])} → TB **{YEAR_MAX}:** {fmt_float(info['mean_last'])} (**{ch}**).",
        f"- Cao nhất: **{fmt_float(info['max_mean'])}** (năm {info['max_year']}); thấp nhất: **{fmt_float(info['min_mean'])}** (năm {info['min_year']}).",
    ]
    if pd.notna(info.get("pct_ge_8_last")):
        lines.append(f"- Tỷ lệ điểm ≥ 8 năm {YEAR_MAX}: **{info['pct_ge_8_last']:.1f}%**.")
    if pd.notna(info.get("count_first")) and pd.notna(info.get("count_last")):
        cf, cl = int(info["count_first"]), int(info["count_last"])
        cc = (cl - cf) / cf * 100 if cf else 0
        lines.append(f"- Số thí sinh thi môn: {fmt_int(cf)} ({YEAR_MIN}) → {fmt_int(cl)} ({YEAR_MAX}), thay đổi **{cc:+.1f}%**.")

    lines += ["", "**Biến động theo từng năm:**", "", "| Năm | ĐTB | % ≥ 8 | Số TS |", "|-----|-----|-------|-------|"]
    for row in info["series"]:
        p8 = f"{row['pct_ge_8']:.1f}%" if pd.notna(row.get("pct_ge_8")) else "—"
        cnt = fmt_int(int(row["count"])) if pd.notna(row.get("count")) else "—"
        lines.append(f"| {int(row['Nam'])} | {fmt_float(row['mean'])} | {p8} | {cnt} |")

    lines += ["", "**Phân tích:**", f"- {_trend_comment(info['change_pct'])}"]
    if info.get("steepest_up"):
        y, p = info["steepest_up"]
        lines.append(f"- Năm tăng mạnh nhất so với năm trước: **{y}** ({p:+.1f}%).")
    if info.get("steepest_down"):
        y, p = info["steepest_down"]
        lines.append(f"- Năm giảm mạnh nhất so với năm trước: **{y}** ({p:+.1f}%).")

    if info["change_pct"] is not None and info["change_pct"] < -10 and pd.notna(info.get("count_last")):
        lines.append(
            "- *Lưu ý:* Giảm TB mạnh có thể liên quan mở rộng nhóm thí sinh thi môn (xem cột Số TS), "
            "không đồng nghĩa chất lượng giảm tuyệt đối."
        )
    lines += [
        "",
        f"**Kết luận dễ hiểu:** Năm {YEAR_MAX}, học sinh thi {info['name']} trung bình được **{fmt_float(info['mean_last'])}** điểm; "
        f"khoảng **{info['pct_ge_8_last']:.1f}%** đạt từ 8 trở lên."
        if pd.notna(info.get("pct_ge_8_last"))
        else f"**Kết luận dễ hiểu:** Năm {YEAR_MAX}, điểm TB môn {info['name']} là **{fmt_float(info['mean_last'])}**.",
    ]
    return lines


def _analyze_heatmap(named: pd.DataFrame, mon: str, year: int = YEAR_MAX) -> list[str]:
    df = named[(named["Nam"] == year) & (named["Mon"] == mon)].dropna(subset=["mean"])
    if df.empty:
        return ["*Không có dữ liệu heatmap cho môn/năm này.*"]
    df = df.sort_values("mean", ascending=False)
    top = df.head(3)
    bot = df.tail(3).sort_values("mean")
    spread = float(df["mean"].max() - df["mean"].min())
    avg = float(df["mean"].mean())

    lines = _layperson_box(
        "Điều này có nghĩa là gì?",
        [
            f"Hình này giống **bản đồ nhiệt**: mỗi hàng là một tỉnh, màu càng đậm = điểm TB môn {subject_vi(mon)} càng cao năm {year}.",
            "Giúp trả lời: *Tỉnh nào điểm cao hơn, tỉnh nào thấp hơn?* — không phải xếp hạng từng học sinh.",
            f"Chênh lệch lớn nhất giữa hai tỉnh trong dữ liệu là khoảng **{fmt_float(spread)}** điểm.",
        ],
    )
    lines += [
        "**Chú thích biểu đồ:**",
        "- **Trục dọc:** Mã tỉnh (1–63, xem `data/provinces.csv`).",
        "- **Màu sắc:** Vàng/nhạt = điểm thấp; cam/đỏ đậm = điểm cao.",
        f"- Thể hiện **chênh lệch vùng** về điểm TB môn **{subject_vi(mon)}** năm **{year}**.",
        "",
        "**Số liệu nổi bật:**",
        f"- Điểm TB trung bình các tỉnh: **{fmt_float(avg)}**.",
        f"- Chênh lệch max–min giữa tỉnh: **{fmt_float(spread)}** điểm.",
        "",
        "**Top 3 tỉnh:**",
    ]
    for _, r in top.iterrows():
        lines.append(f"- **{r['TenTinh']}:** {fmt_float(r['mean'])} ({fmt_int(int(r['count']))} thí sinh)")
    lines += ["", "**Bottom 3 tỉnh:**"]
    for _, r in bot.iterrows():
        lines.append(f"- **{r['TenTinh']}:** {fmt_float(r['mean'])} ({fmt_int(int(r['count']))} thí sinh)")
    lines += [
        "",
        "**Phân tích:**",
        "- Heatmap cho thấy **bất đồng đều không gian**: cùng một môn nhưng điểm TB chênh lệch rõ giữa các tỉnh.",
        "- Cần thận trọng khi so sánh tỉnh có **số thí sinh thi môn rất nhỏ** (mẫu ít → TB dễ biến động).",
        "",
        f"**Kết luận dễ hiểu:** Cùng thi môn {subject_vi(mon)}, điểm TB **không đồng đều** giữa các tỉnh — có nơi nổi bật (top 3) và nơi thấp hơn (bottom 3). Đây là ảnh chụp năm {year}, không phải xếp hạng vĩnh viễn.",
    ]
    return lines


def _analyze_forecast(mon: str, forecast: pd.DataFrame, info: dict | None) -> list[str]:
    name = subject_vi(mon)
    lines = _layperson_box(
        "Điều này có nghĩa là gì?",
        [
            f"Đường xanh = điểm TB thật của môn {name} qua các năm; đường đỏ = **ước lượng** năm tới nếu xu hướng cũ tiếp tục.",
            "Đây là công cụ học thuật (đồ án), **không phải** thông báo điểm chính thức của Bộ.",
            "Hãy coi con số dự báo là *khoảng tham khảo*, không phải lời hứa chính xác.",
        ],
    )
    lines += [
        "**Chú thích biểu đồ:**",
        "- **Đường xanh (tròn):** Điểm TB thực tế 2021–2025.",
        "- **Đường đỏ (đứt, vuông):** Dự báo năm tiếp theo bằng **hồi quy tuyến tính**.",
        "- Mô hình đơn giản — phù hợp mô tả xu hướng, không thay thế dự báo chính thức.",
    ]
    if forecast.empty or mon not in forecast["Mon"].values:
        return lines

    row = forecast[forecast["Mon"] == mon].iloc[0]
    pred = float(row["forecast_mean"])
    actual = float(row.get("backtest_actual") or 0)
    mae = row.get("backtest_mae")
    fy = int(row["forecast_year"])

    lines += [
        "",
        "**Kết quả dự báo:**",
        f"- Dự báo **{fy}:** **{fmt_float(pred, 3)}** điểm.",
        f"- Thực tế **{YEAR_MAX}:** **{fmt_float(actual, 3)}** điểm.",
    ]
    if pd.notna(mae):
        lines.append(f"- **MAE backtest** (dự báo {YEAR_MAX} từ 2021–2024): **{fmt_float(mae, 4)}** — càng nhỏ càng sát lịch sử gần.")
    delta = pred - actual
    lines += [
        "",
        "**Phân tích:**",
        f"- Chênh lệch dự báo {fy} so với thực tế {YEAR_MAX}: **{delta:+.2f}** điểm.",
    ]
    if info and info.get("change_pct") is not None:
        if info["change_pct"] > 0 and delta > 0:
            lines.append("- Dự báo **cùng chiều** xu hướng tăng 5 năm qua.")
        elif info["change_pct"] < 0 and delta < 0:
            lines.append("- Dự báo **cùng chiều** xu hướng giảm 5 năm qua.")
        else:
            lines.append("- Dự báo **không cùng chiều** xu hướng 5 năm — mô hình tuyến tính có thể bị ảnh hưởng bởi năm đột biến.")
    if pd.notna(mae) and float(mae) > 0.5:
        lines.append("- MAE cao → nên trình bày dự báo kèm **khoảng tin cậy / giới hạn mô hình** trong báo cáo đồ án.")
    lines += [
        "",
        f"**Kết luận dễ hiểu:** Nếu xu hướng 5 năm giữ nguyên, TB môn {name} năm tới có thể quanh **{fmt_float(pred, 3)}** điểm — "
        "nhưng thực tế còn phụ thuộc đề thi, quy chế và số người thi.",
    ]
    return lines


def build_readme_charts_section() -> str:
    """Markdown section 8: chu thich + phan tich day du cho moi bieu do."""
    tables = Path(TABLES_DIR)
    figures = Path(FIGURES_DIR)
    by_ys = pd.read_csv(tables / "by_year_subject.csv")
    cand = pd.read_csv(tables / "candidates_by_year.csv")
    named = pd.read_csv(tables / "by_year_province_subject_named.csv")
    forecast = pd.read_csv(tables / "forecast_next_year.csv") if (tables / "forecast_next_year.csv").exists() else pd.DataFrame()

    lines = [
        "## 8. Báo cáo chi tiết biểu đồ",
        "",
        "Phần này dành cho **mọi độc giả** — kể cả người chưa từng học thống kê. Mỗi biểu đồ được trình bày theo thứ tự:",
        "",
        "1. **Điều này có nghĩa là gì?** — giải thích bằng lời đời thường",
        "2. **Chú thích biểu đồ** — trục X, trục Y, màu sắc",
        "3. **Số liệu / bảng** — con số cụ thể",
        "4. **Phân tích** — xu hướng và so sánh",
        "5. **Kết luận dễ hiểu** — một câu tóm tắt",
        "6. **Hình minh hoạ**",
        "",
        "### 8.1. Biểu đồ tổng quan",
        "",
        "#### 8.1.1. Số thí sinh theo năm",
        "",
        *(_analyze_candidates(cand)),
        "",
        "![Số thí sinh theo năm](outputs/figures/candidates_by_year.png)",
        "",
        "#### 8.1.2. Tỷ lệ điểm ≥ 8 — tất cả môn",
        "",
        *(_analyze_pct_ge_8(by_ys)),
        "",
        "![Tỷ lệ điểm >= 8](outputs/figures/pct_ge_8_by_year.png)",
        "",
        "### 8.2. Xu hướng điểm trung bình — từng môn",
        "",
    ]

    subjects = sorted(
        [m for m in by_ys["Mon"].unique() if by_ys.loc[by_ys["Mon"] == m, "count"].sum() > 0],
        key=lambda x: subject_vi(x),
    )
    for idx, mon in enumerate(subjects, 1):
        info = _subject_detail(by_ys, mon)
        if not info:
            continue
        lines += [f"#### 8.2.{idx}. {info['name']}", ""]
        lines += _analyze_subject_mean(info)
        lines += ["", f"![{info['name']}](outputs/figures/mean_by_year_{mon}.png)", ""]

    lines += ["### 8.3. Heatmap phân bố theo tỉnh (2025)", ""]
    heatmaps = sorted(figures.glob(f"heatmap_*_{YEAR_MAX}.png"))
    for idx, hp in enumerate(heatmaps, 1):
        mon = hp.stem.replace("heatmap_", "").replace(f"_{YEAR_MAX}", "")
        lines += [f"#### 8.3.{idx}. {subject_vi(mon)}", ""]
        lines += _analyze_heatmap(named, mon, YEAR_MAX)
        lines += ["", f"![Heatmap {subject_vi(mon)}](outputs/figures/{hp.name})", ""]

    lines += ["### 8.4. Biểu đồ dự báo", ""]
    for idx, fp in enumerate(sorted(figures.glob("forecast_*.png")), 1):
        mon = fp.stem.replace("forecast_", "")
        info = _subject_detail(by_ys, mon) if mon in subjects else None
        lines += [f"#### 8.4.{idx}. {subject_vi(mon)}", ""]
        lines += _analyze_forecast(mon, forecast, info)
        lines += ["", f"![Dự báo {subject_vi(mon)}](outputs/figures/{fp.name})", ""]

    return "\n".join(line for line in lines if line is not None)
