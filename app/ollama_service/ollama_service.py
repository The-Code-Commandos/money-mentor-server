import ollama
from schema import ChallengeCreate

SYSTEM_PROMPT = """You are an AI financial coach. Generate engaging, gamified savings and investment challenges based on user input. Keep it simple, actionable, and jargon-free. Do not include any disclaimers or legal information. Focus on the user's financial goals, preferences, and behaviors and queries given to you below. Anything out of the scope of the query should be ignored. The user is looking for a unique and engaging challenge that will help them achieve their financial goals."""

def generate_challenge(data: ChallengeCreate):
    user_prompt = f"""
    The user is {data.employment_type} with a financial goal of {data.financial_goal}.
    They prefer {data.investment_preference} investments.
    Their savings rate is {data.savings_rate}% of their income.
    They have {data.spending_behavior} spending habits and {data.debt_situation} debt.
    The challenge duration is {data.challenge_duration} days.
    They chose a {data.challenge_type} challenge with {data.commitment_level} commitment level.
    Their biggest financial fear is {data.financial_fear}.
    Generate a unique and engaging savings/investment challenge.
    """
    
    response = ollama.chat(model="llama3.2", messages=[{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": user_prompt}])
    return response["message"]["content"]
