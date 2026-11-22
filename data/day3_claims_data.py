
CLAIMS = {
    "123": {
        "status": "Denied",
        "billed_amount": 1000,
        "allowed_amount": 0,
        "paid_amount": 0,
        "denial_reason": "Member not eligible on date of service"
    },

    "CLM456": {
        "status": "Paid",
        "billed_amount": 500,
        "allowed_amount": 350,
        "paid_amount": 280,
        "denial_reason": None
    },

    "5678": {
        "status": "Denied",
        "billed_amount": 800,
        "allowed_amount": 0,
        "paid_amount": 0,
        "denial_reason": "Coordination of Benefits information missing"
    }
}
if __name__ == "__main__":
    print(CLAIMS["123"])