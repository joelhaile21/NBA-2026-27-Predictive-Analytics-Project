
from pathlib import Path
import pandas as pd

# Locate project folders
PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = PROJECT_DIR / "Data" / "Player Per Game.csv"
OUTPUT_FILE = PROJECT_DIR / "Data" / "player_per_game_clean.csv"

# Load data
df = pd.read_csv(DATA_FILE)

print("Original rows:", len(df))

# Keep NBA records and valid player-season identifiers
df = df[df["lg"] == "NBA"].copy()
df = df.dropna(subset=["player_id", "season"])

# Identify combined-team rows, e.g. 2TM, 3TM
df["is_combined_team"] = df["team"].str.fullmatch(
    r"\d+TM", na=False
)

# Identify player-seasons that have a combined-team row
keys = ["player_id", "season"]

has_combined_row = (
    df.groupby(keys)["is_combined_team"]
      .transform("any")
)

# If a combined row exists, keep it and remove individual team rows.
# Otherwise, retain the available row(s) for that player-season.
df_clean = df.loc[
    ~has_combined_row | df["is_combined_team"]
].copy()

df_clean = df_clean.drop(columns="is_combined_team")

# Check whether any repeated player-seasons remain
duplicates = df_clean.duplicated(subset=keys, keep=False)

print("Rows after cleaning:", len(df_clean))
print(
    "Repeated player-season rows remaining:",
    int(duplicates.sum())
)

if duplicates.any():
    print("\nRemaining duplicate examples:")
    print(
        df_clean.loc[
            duplicates, ["season", "player", "player_id", "team"]
        ]
        .sort_values(["season", "player_id"])
        .head(20)
        .to_string(index=False)
    )

# Save the cleaned dataset
df_clean.to_csv(OUTPUT_FILE, index=False)

print("\nSaved to:", OUTPUT_FILE)
print("Season range:", df_clean["season"].min(), "-", df_clean["season"].max())
