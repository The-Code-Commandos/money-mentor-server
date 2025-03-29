import json
from fastapi import FastAPI, APIRouter # type: ignore
from app.services.simulations.sims import run_ideal_sim, run_real_sim

with open("app/data/rates.json", "r") as f:
    RATES = json.load(f)

router = APIRouter()

@router.get("/sims/{fund}")
def run_simulation(fund: str, amount: float, days: int = 30):
    if fund not in RATES:
        return {
            "error": "Pick DigiSave, Eurobond, or GlobalTech!"
        }
    
    # Validate days
    valid_days = [7, 14, 30, 60, 90, 365]
    if days not in valid_days:
        days = min(valid_days, key=lambda x: abs(x - days))  # Closest match
    
    # Run sims
    ideal = run_ideal_sim(amount, RATES[fund]["daily_rate"], days)
    real = run_real_sim(amount, RATES[fund]["daily_rate"], RATES[fund]["volatility"], days)
    diff = ideal[-1] - real[-1]
    
    return {
        "fund": fund,
        "amount": amount,
        "days": days,
        "ideal": {"values": ideal, "final": round(ideal[-1], 2)},
        "real": {"values": real, "final": round(real[-1], 2)},
        "difference": round(diff, 2),
        "desc": "Ideal vs. Real—see how markets wiggle!"
    }
    ...
