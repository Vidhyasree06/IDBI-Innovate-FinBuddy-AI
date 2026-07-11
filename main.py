# FinBuddy AI - Transaction Engine Prototype
# Official Submission for IDBI Innovate 2026
# Submitted By: M.Sreevidhya

import json
from typing import List, Dict

class FinBuddyEngine:
    def __init__(self, user_id: str, monthly_reserve_limit: float = 15000.0):
        self.user_id = user_id
        self.reserve_limit = monthly_reserve_limit

    def scan_stagnant_balances(self, ledger_logs: List[Dict]) -> Dict:
        """
        Analyzes account transactions to isolate idle capital and 
        accumulate fractional micro-savings from digital UPI actions.
        """
        total_income = 0.0
        total_spending = 0.0
        fractional_roundups = 0.0
        
        for item in ledger_logs:
            value = float(item.get("amount", 0.0))
            if item.get("type") == "CREDIT":
                total_income += value
            elif item.get("type") == "DEBIT":
                total_spending += value
                # Micro-roundup logic for UPI payment transactions
                if item.get("mode") == "UPI":
                    change_remainder = value % 10
                    if change_remainder > 0:
                        fractional_roundups += (10 - change_remainder)

        # Formula to evaluate baseline unutilized capital pools
        net_surplus = total_income - total_spending
        detected_idle_cash = max(0.0, net_surplus - self.reserve_limit)

        return {
            "account_id": self.user_id,
            "status": "Analysis Finalized",
            "extracted_metrics": {
                "parsed_income": total_income,
                "parsed_spending": total_spending,
                "identified_idle_surplus": detected_idle_cash,
                "accumulated_roundup_pool": fractional_roundups
            },
            "suggested_idbi_portfolio": {
                "idbi_systematic_deposits_50pct": detected_idle_cash * 0.50,
                "low_risk_liquid_funds_25pct": detected_idle_cash * 0.25,
                "digital_gold_roundups_15pct": fractional_roundups + (detected_idle_cash * 0.15),
                "micro_equity_mutual_funds_10pct": detected_idle_cash * 0.10
            }
        }

if __name__ == "__main__":
    # Simulating a monthly mock transactional statement for verification
    mock_statements = [
        {"id": "TXN_01", "type": "CREDIT", "amount": 50000.0, "mode": "IMPS"},
        {"id": "TXN_02", "type": "DEBIT", "amount": 15000.0, "mode": "NetBanking"},
        {"id": "TXN_03", "type": "DEBIT", "amount": 243.0, "mode": "UPI"},
        {"id": "TXN_04", "type": "DEBIT", "amount": 81.0, "mode": "UPI"},
        {"id": "TXN_05", "type": "DEBIT", "amount": 1200.0, "mode": "DebitCard"}
    ]
    
    analyzer = FinBuddyEngine(user_id="IDBI_RETAIL_USER_4821")
    report = analyzer.scan_stagnant_balances(mock_statements)
    print(json.dumps(report, indent=4))
