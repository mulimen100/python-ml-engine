import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix


# ---------------------------------------------------------
# 1) גרף תנועת דגלים לאורך זמן
# ---------------------------------------------------------
def plot_flags(df, save_path=None):
    plt.figure(figsize=(14, 4))
    plt.plot(df["date"], df["flag_score"], linewidth=1.5)
    plt.title("Flag Movement Over Time")
    plt.grid(True)
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=150)
        plt.close()
    else:
        plt.show()


# ---------------------------------------------------------
# 2) גרף יחס פגיעה (Hit Ratio)
# ---------------------------------------------------------
def plot_hit_ratio(df, save_path=None):
    hit_ratio = (df["prediction"] == df["real"]).rolling(30).mean()

    plt.figure(figsize=(14, 4))
    plt.plot(df["date"], hit_ratio, linewidth=1.5)
    plt.axhline(0.5, color="red", linestyle="--")
    plt.title("Hit Ratio (30D Rolling)")
    plt.grid(True)
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=150)
        plt.close()
    else:
        plt.show()


# ---------------------------------------------------------
# 3) Confusion Matrix
# ---------------------------------------------------------
def plot_confusion_matrix(df, save_path=None):
    y_true = df["real"]
    y_pred = df["prediction"]

    cm = confusion_matrix(y_true, y_pred)

    plt.figure(figsize=(5, 4))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues")
    plt.title("Confusion Matrix")
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=150)
        plt.close()
    else:
        plt.show()


# ---------------------------------------------------------
# 4) גרף תחזיות 1D / 5D לאורך זמן
# ---------------------------------------------------------
def plot_predictions(df, save_path=None):
    plt.figure(figsize=(14, 4))
    plt.plot(df["date"], df["pred_1d"], label="Pred 1D", linewidth=1)
    plt.plot(df["date"], df["pred_5d"], label="Pred 5D", linewidth=1)
    plt.legend()
    plt.title("1D / 5D Predictions Over Time")
    plt.grid(True)
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=150)
        plt.close()
    else:
        plt.show()
