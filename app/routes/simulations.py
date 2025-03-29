import json
from fastapi import APIRouter # type: ignore
from app.services.simulations.sims import run_ideal_sim, run_real_sim, run_real_sim_range

with open("app/data/rates.json", "r") as f:
    RATES = json.load(f)

router = APIRouter()

@router.get("/sims/{fund}")
def run_simulation(
    fund: str,
    amount: float,
    days: int = 30,
    deposit: float = 0,  # Fixed deposit amount
    deposit_min: float = 0,  # Range min
    deposit_max: float = 0,  # Range max
    freq: str = "none"  # Schedule: daily, weekly, monthly, 2m, 4m, 6m
):
    if fund not in RATES:
        return {"error": "Pick DigiSave, Eurobond, or GlobalTech!"}

    # Validate days
    valid_days = [7, 14, 30, 60, 90, 365]
    if days not in valid_days:
        days = min(valid_days, key=lambda x: abs(x - days))

    # Map frequency to days
    freq_map = {"daily": 1, "weekly": 7, "monthly": 30, "2m": 60, "4m": 120, "6m": 180, "none": 0}
    freq_days = freq_map.get(freq, 0)

    # Run sims
    ideal = run_ideal_sim(amount, RATES[fund]["daily_rate"], days, deposit, freq_days)
    if deposit_min and deposit_max and deposit_min <= deposit_max:
        real = run_real_sim_range(amount, RATES[fund]["daily_rate"], RATES[fund]["volatility"], days, deposit_min, deposit_max, freq_days)
    else:
        real = run_real_sim(amount, RATES[fund]["daily_rate"], RATES[fund]["volatility"], days, deposit, freq_days)
    diff = ideal[-1] - real[-1]

    return {
        "fund": fund,
        "amount": amount,
        "days": days,
        "deposit": deposit if deposit else f"{deposit_min}-{deposit_max}",
        "frequency": freq,
        "ideal": {"values": ideal, "final": round(ideal[-1], 2)},
        "real": {"values": real, "final": round(real[-1], 2)},
        "difference": round(diff, 2),
        "desc": "Ideal vs. Real—watch your savings grow!"
    }