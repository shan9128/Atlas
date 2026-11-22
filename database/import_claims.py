
import csv
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

CSV_PATH = BASE_DIR / "data/kaggle/synthetic_health_claims.csv"
DB_PATH = BASE_DIR / "database/atlas.db"

connection = sqlite3.connect(DB_PATH)
cursor = connection.cursor()

with open(CSV_PATH, newline="", encoding="utf-8-sig") as file:
    reader = csv.DictReader(file)

    records = [
        (
            row["Claim_ID"],
            row["Patient_ID"],
            float(row["Claim_Amount"]),
            row["Service_Date"],
            1 if row["Is_Fraudulent"] == "True" else 0
        )
        for row in reader
    ]

cursor.execute("DELETE FROM raw_claims")

cursor.executemany("""
INSERT INTO raw_claims (
    claim_id,
    patient_id,
    claim_amount,
    service_date,
    is_fraudulent
)
VALUES (?, ?, ?, ?, ?)
""", records)

connection.commit()

cursor.execute("SELECT COUNT(*) FROM raw_claims")
print("Imported records:", cursor.fetchone()[0])

connection.close()
