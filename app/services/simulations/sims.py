import random

def run_ideal_sim(amount: float, daily_rate: float, days: int, deposit: float = 0, freq: int = 0):
    values = [amount]
    for day in range(days):
        # Add deposit at frequency intervals
        if freq > 0 and day % freq == 0 and day > 0:
            values.append(values[-1] + deposit)
        else:
            values.append(values[-1] * (1 + daily_rate))
    return [round(v, 2) for v in values]

def run_real_sim(amount: float, daily_rate: float, volatility: float, days: int, deposit: float = 0, freq: int = 0):
    values = [amount]
    vol = volatility if days <= 30 else volatility / 2 if days <= 90 else volatility / 4
    for day in range(days):
        if freq > 0 and day % freq == 0 and day > 0:
            values.append(values[-1] + deposit)
        else:
            noise = random.uniform(-vol, vol)
            values.append(values[-1] * (1 + daily_rate + noise))
    return [round(v, 2) for v in values]

def run_real_sim_range(amount: float, daily_rate: float, volatility: float, days: int, deposit_min: float, deposit_max: float, freq: int):
    values = [amount]
    vol = volatility if days <= 30 else volatility / 2 if days <= 90 else volatility / 4
    for day in range(days):
        if freq > 0 and day % freq == 0 and day > 0:
            deposit = random.uniform(deposit_min, deposit_max)
            values.append(values[-1] + deposit)
        else:
            noise = random.uniform(-vol, vol)
            values.append(values[-1] * (1 + daily_rate + noise))
    return [round(v, 2) for v in values]