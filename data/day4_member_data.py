
MEMBERS = {
    "M1001": {
        "name": "John Smith",
        "status": "Active",
        "plan": "Gold",
        "effective_date": "2026-01-01",
        "termination_date": None
    },

    "M2002": {
        "name": "Jane Doe",
        "status": "Inactive",
        "plan": "Silver",
        "effective_date": "2025-01-01",
        "termination_date": "2025-12-31"
    },

    "M3003": {
        "name": "Alex Johnson",
        "status": "Active",
        "plan": "Gold",
        "effective_date": "2026-06-01",
        "termination_date": None
    }
}


if __name__ == "__main__":
    print(MEMBERS["M1001"])
