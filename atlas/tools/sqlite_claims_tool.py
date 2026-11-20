
import sqlite3
from pathlib import Path

DB_PATH = (
    Path(__file__).resolve().parents[2]
    / "database"
    / "atlas.db"
)


def lookup_claim_sqlite(claim_id: str) -> dict:
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row

    try:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                claim_id,
                patient_id,
                claim_amount,
                service_date,
                is_fraudulent
            FROM validated_claims
            WHERE claim_id = ?
        """, (claim_id,))

        result = cursor.fetchone()

        if result is None:
            return {
                "found": False,
                "claim_id": claim_id
            }

        return {
            "found": True,
            **dict(result)
        }

    finally:
        connection.close()
