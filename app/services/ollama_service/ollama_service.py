import ollama
from app.schema.schema import ChallengeCreate

SYSTEM_PROMPT = """You are a specialized AI that exclusively generates gamified financial challenges. Your sole purpose is to create structured, engaging, and motivational savings and investment challenges based on user-provided inputs. You do not provide financial advice, answer unrelated questions, or engage in general conversation. You only generate financial challenges. If asked anything outside this scope, you must respond with: "I only generate financial challenges."""

def generate_challenge(data: ChallengeCreate):
    user_prompt = f"""
    The user is a {data.employment_type} with a financial goal of {data.financial_goal}.
    They prefer {data.investment_preference} investments.
    Their monthly income is ${data.Monthly_income}, with a savings rate of {data.savings_rate}%.
    They have {data.spending_behavior} spending habits and {data.debt_situation} debt.
    The challenge duration is {data.challenge_duration} days.
    They chose a {data.challenge_type} challenge with a {data.commitment_level} commitment level.
    Their biggest financial fear is {data.financial_fear}.

    Generate a structured, engaging financial challenge using the following format:
    
    **Challenge Title:** [Catchy name]  
    **Duration:** {data.challenge_duration} Days  
    **Type:** {data.challenge_type}  
    **Daily/Weekly Task:** [Specific, actionable steps based on user input]  
    **Progress Tracking:** [How the user can measure success]  
    **Motivational Hook:** [Encouraging message to keep the user engaged]  

    Do not provide financial advice or respond to any unrelated topics. Do not be asking the users if they are ready to start the challenge or any kind of similar questions. Just follow the instructions above. If any required input is missing, respond with: "Please provide all required inputs for challenge generation."
"""

    
    response = ollama.chat(model="llama3.2", messages=[{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": user_prompt}])
    return response["message"]["content"]