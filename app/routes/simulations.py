from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class SimulationRequest(BaseModel):
    starting_amount: float
    portfolio: str  # Options: digisave, eurobond

class SimulationResponse(BaseModel):
    one_year_savings: float
    three_year_savings: float

def calculate_simulation(starting_amount: float, portfolio: str):
    if portfolio == "digisave":
        rate = 0.08  # 8% per year
    elif portfolio == "eurobond":
        rate = 0.12  # 12% per year
    else:
        rate = 0.05  # Default rate

    one_year = starting_amount * (1 + rate)
    three_year = starting_amount * ((1 + rate) ** 3)
    return one_year, three_year

@router.post("/", response_model=SimulationResponse)
def run_simulation(data: SimulationRequest):
    one_year, three_year = calculate_simulation(data.starting_amount, data.portfolio)
    return {"one_year_savings": one_year, "three_year_savings": three_year}
