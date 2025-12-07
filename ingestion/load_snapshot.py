import pandas as pd

def load_snapshot(path="../data_snapshot/data_engine_snapshot.xlsx"):
    """
    קורא את כל הלשוניות בקובץ ה-Excel
    מחזיר dict בשם data שבו כל לשונית היא DataFrame
    """

    xls = pd.ExcelFile(path)
    data = {}

    for sheet in xls.sheet_names:
        df = pd.read_excel(xls, sheet_name=sheet)

        # המרת עמודת תאריך אם קיימת
        if "date" in df.columns:
            df["date"] = pd.to_datetime(df["date"], errors="coerce")

        # הסרת כפילויות
        df = df.drop_duplicates()

        data[sheet] = df

    return data


def validate_snapshot(data):
    """
    בדיקות בסיסיות על כל הטאבים
    """

    for name, df in data.items():

        # 1) בדיקת רשומות ריקות
        if df.empty:
            print(f"[אזהרה] הטאב '{name}' ריק.")

        # 2) בדיקת NaN
        nan_count = df.isna().sum().sum()
        if nan_count > 0:
            print(f"[אזהרה] הטאב '{name}' מכיל {nan_count} ערכי NaN.")

        # 3) בדיקת עמודת תאריך תקולה
        if "date" in df.columns:
            if df["date"].isna().any():
                print(f"[אזהרה] הטאב '{name}' מכיל תאריכים שלא הומרו תקין.")

    print("בדיקות ה-SNAPSHOT הושלמו.")


if __name__ == "__main__":
    data = load_snapshot()
    validate_snapshot(data)
    print("✔️ טעינת SNAPSHOT הצליחה.")
