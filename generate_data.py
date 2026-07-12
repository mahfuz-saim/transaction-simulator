import json
import random
import uuid
from datetime import datetime, timedelta

# Constants based on Prisma Schema
PROVIDER_CODES = ["BKASH", "NAGAD", "ROCKET"]
TXN_TYPES = ["CASH_IN", "CASH_OUT", "SEND_MONEY", "PAYMENT", "BALANCE_INQUIRY", "TRANSFER"]
TXN_STATUSES = ["SUCCESS", "FAILED", "PENDING", "REVERSED"]
TXN_DIRECTIONS = ["INBOUND", "OUTBOUND"]
TXN_CHANNELS = ["USSD", "APP", "AGENT_ASSISTED", "API"]
ACCOUNT_TYPES = ["PERSONAL", "MERCHANT", "AGENT", "CORPORATE"]

def generate_ipn_data(count=1000):
    data = []
    start_date = datetime(2026, 1, 1)
    
    for i in range(count):
        provider = random.choice(PROVIDER_CODES)
        # Use a small set of agent codes to simulate some overlap/duplicates
        agent_code = f"AGNT-{random.randint(100, 120)}" 
        
        amount = round(random.uniform(10.0, 50000.0), 2)
        prev_balance = round(random.uniform(1000.0, 1000000.0), 2)
        
        # Calculate new balance based on direction
        if random.choice(TXN_DIRECTIONS) == "INBOUND":
            new_balance = prev_balance + amount
        else:
            new_balance = prev_balance - amount

        timestamp = start_date + timedelta(
            days=random.randint(0, 200), 
            hours=random.randint(0, 23), 
            minutes=random.randint(0, 59)
        )

        payload = {
            "providerTxnId": str(uuid.uuid4()).upper(),
            "providerAgentCode": agent_code,
            "accountIdentifier": f"ACC-{random.randint(100000, 999999)}",
            "accountType": random.choice(ACCOUNT_TYPES),
            "txnType": random.choice(TXN_TYPES),
            "direction": random.choice(TXN_DIRECTIONS),
            "amount": amount,
            "status": random.choice(TXN_STATUSES),
            "channel": random.choice(TXN_CHANNELS),
            "previousBalance": prev_balance,
            "newBalance": new_balance,
            "deviceFingerprint": f"fp-{uuid.uuid4().hex[:12]}",
            "sessionId": str(uuid.uuid4()),
            "txnTimestamp": timestamp.isoformat() + "Z",
            "eventFlags": {
                "is_high_value": amount > 10000,
                "is_off_hours": timestamp.hour < 6 or timestamp.hour > 22
            }
        }
        
        data.append({
            "providerCode": provider,
            "payload": payload
        })
    
    return data

if __name__ == "__main__":
    dummy_data = generate_ipn_data(1000)
    with open("data.json", "w") as f:
        json.dump(dummy_data, f, indent=2)
    print("Successfully generated data.json with 1000 rows.")
