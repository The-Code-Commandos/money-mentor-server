import random

def run_ideal_sim(amount: float, daily_rate: float, days: int):
    values = [amount]
    for _ in range(days):
        values.append(values[-1] * (1 + daily_rate))
    return [round(v, 2) for v in values]

def run_real_sim(amount: float, daily_rate: float, volatility: float, days: int):
    values = [amount]
    if days <= 30:
        vol = volatility
    elif days <= 90:
        vol = volatility / 2
    else:
        vol = volatility / 4
    for _ in range(days):
        noise = random.uniform(-vol, vol)
        values.append(values[-1] * (1 + daily_rate + noise))
    return [round(v, 2) for v in values]