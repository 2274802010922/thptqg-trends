import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from src.config import CSV_PATH, YEAR_MIN, YEAR_MAX
from src.load_data import count_rows, iter_chunks

def main():
    print("CSV:", CSV_PATH)
    print("Pham vi nam:", YEAR_MIN, "-", YEAR_MAX)
    print("So dong theo nam:", count_rows())
    chunk = next(iter_chunks(usecols=["Nam", "Tinh", "Toan"]))
    print("Mau 3 dong:")
    print(chunk.head(3).to_string(index=False))

if __name__ == "__main__":
    main()
