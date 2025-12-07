from visuals.charts import plot_flags
import pandas as pd

# יצירת DataFrame קטן לדוגמה
df = pd.DataFrame({
    "date": ["2024-01-01", "2024-01-02", "2024-01-03"],
    "flag_score": [10, 45, 80]
})

# שמירת גרף ראשון כ-PNG
plot_flags(df, save_path="flags.png")
