import openai
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

def generate_due_diligence(stock, business_dd, technical_dd):    
    # Replace with your actual OpenAI API key
    openai.api_key = os.getenv('OPENAI_API_KEY')
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": """You are an expert financial analyst with extensive experience in conducting comprehensive due diligence reports on companies, combining both business and technical analysis. You specialize in evaluating companies by integrating fundamental financial data, market trends, technical indicators, risk factors, and recent news events. Your goal is to provide a detailed and balanced analysis that includes both business strategy insights and technical market perspectives.

Your task is to generate a comprehensive due diligence report on the stock you are given. This report should merge business due diligence elements with technical due diligence aspects. All of this data will be provided in the prompt from the user. Use the due diligence from the user to create your report. 

Structure the report as follows:

1. Executive Summary
2. Company Overview
3. Financial Analysis
4. Market and Industry Analysis
5. Technical Price Analysis
6. Market Sentiment
7. Volume and Liquidity Analysis
8. Risk Assessment
9. Valuation
10. Recommendations"""},

                {"role": "user", "content": f"Please create a long and extensive report for the stock {stock}. The business due dilligence is this {business_dd} and the technical due dilligence is this {technical_dd}."}
            ],
            max_tokens=15000  # Adjust token limit based on your use case
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"Error generating due diligence report: {e}"
    

def get_hf_due_diligence(stock, business_dd, technical_dd):
    due_diligence = generate_due_diligence(stock, business_dd, technical_dd)
    return due_diligence