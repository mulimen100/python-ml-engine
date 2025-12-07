import pandas as pd
import json

def export_csv(df, path):
    df.to_csv(path, index=False)
    return path

def export_json(data, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return path
