
from pathlib import Path
import pandas as pd

project_folder = Path(__file__).resolve().parent.parent
data_file = project_folder / "Data" / "Player Per Game.csv"

df = pd.read_csv(data_file)

print("\n--- FIRST 5 ROWS ---")
print(df.head().to_string())

print("\n--- DATASET SIZE ---")
print(f"Rows: {df.shape[0]:,}")
print(f"Columns: {df.shape[1]}")

print("\n--- COLUMN NAMES ---")
print(df.columns.tolist())

print("\n--- DATA TYPES ---")
df.info()

print("\n--- MOST RECENT SEASONS ---")
season_col = next(
    (col for col in df.columns if col.lower() == "season"),
    None
)

if season_col:
    print(sorted(df[season_col].dropna().unique())[-10:])
else:
    print("Season column not found.")
