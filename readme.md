# THPTQG Trends

Phan tich diem THPT quoc gia 2021-2025 va du bao xu huong.

## Google Colab (khuyen dung)

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/2274802010922/thptqg-trends/blob/main/colab/THPTQG_Colab.ipynb)

1. Mo link tren
2. Chay lan luot cac cell tu tren xuong
3. Dat file `cleaned_data.csv` (~805MB) tren **Google Drive** hoac upload trong notebook
4. Cell cuoi zip va tai ket qua ve may

Chi tiet: [`colab/README.md`](colab/README.md)

## Chay tren Windows

```powershell
cd "D:\do an thuc tap\thptqg-trends"
.\run.ps1
```

Hoac double-click **`run.bat`**.

## Ket qua

| Thu muc / file | Noi dung |
|----------------|----------|
| `reports/BAO_CAO.md` | Bao cao tong hop |
| `outputs/tables/` | CSV tong hop |
| `outputs/figures/` | Bieu do PNG |

## Du lieu

File goc khong commit Git. Duong dan mac dinh Windows: `D:\do an thuc tap\cleaned_data.csv`

Colab: set trong notebook hoac bien moi truong `THPTQG_CSV_PATH`.

Doi nam: `src/config.py` hoac `configure()` trong Colab.

## Repo

https://github.com/2274802010922/thptqg-trends
