import asyncio
import os
import pdfplumber

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from pydantic import SecretStr
from browser_use import Agent  

# katjib Api men .env A simo l7mar 
load_dotenv()
api_key = os.getenv("DEEPSEEK_API_KEY", "")
if not api_key:
    raise ValueError("DEEPSEEK_API_KEY is not set")


# Hadi katjib lik PDF al 7mar (love you Bro <3 )
def extract_cv_text(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        return "\n".join(page.extract_text() or "" for page in pdf.pages)


# dirr prompt kifma bghity wla khaliha 
def build_task_prompt(cv_text):
    return (
        "You are acting as a job search assistant. Use the following candidate CV information to identify suitable job opportunities at Google.\n\n"
        "===== CANDIDATE PROFILE =====\n"
        f"{cv_text}\n"
        "=============================\n\n"
        "Your task:\n"
        "1. Go to google.com.\n"
        "2. Search for open positions at Google that align with this candidate’s skills, experience, and goals.\n"
        "3. Find and summarize 3–5 job postings that are a strong match.\n"
        "4. For each job, provide:\n"
        "    - Job title\n"
        "    - Location (if available)\n"
        "    - Short description\n"
        "    - Direct link to the job posting (if possible)\n\n"
        "Only use real results. Be efficient and precise."
    )


# kmel men rassek tssift liya fwhatsapp tgoli makhdemch gha nchdek ghan*****
async def run_search():
    cv_text = extract_cv_text("Cv.pdf")
    task_prompt = build_task_prompt(cv_text)

    agent = Agent(
        task=task_prompt,
        llm=ChatOpenAI(
            base_url="https://api.deepseek.com/v1",
            model="deepseek-chat",
            api_key=SecretStr(api_key),
        ),
        use_vision=False,
    )

    try:
        result = await agent.run()
        print("\n=== JOB OPPORTUNITIES AT GOOGLE ===\n")
        print(result)
    except Exception as e:
        print(f"Agent run failed: {e}")

if __name__ == "__main__":
    asyncio.run(run_search())
