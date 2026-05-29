# THPTQG Trends

Phan tich diem THPT quoc gia 2021-2025 va du bao xu huong.

## Chay mot lenh (Windows)

Double-click **`run.bat`** hoac trong PowerShell:

```powershell
cd "D:\do an thuc tap\thptqg-trends"
.\run.ps1
```

Lan dau se tu tao `.venv`, cai thu vien, roi chay pipeline (~5-15 phut tuy may).

## Ket qua

| Thu muc / file | Noi dung |
|----------------|----------|
| `reports/BAO_CAO.md` | Bao cao tong hop |
| `outputs/tables/` | CSV tong hop (public) |
| `outputs/figures/` | Bieu do PNG |

## Du lieu

File goc: `D:\do an thuc tap\cleaned_data.csv` (khong commit Git).

Doi nam: sua `YEAR_MIN`, `YEAR_MAX` trong `src/config.py`.

## Chay thu cong

```powershell
.\.venv\Scripts\Activate.ps1
python scripts/run_all.py
```
