import openai
from dotenv import load_dotenv
import os
import json

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

Structure the report as follows (dont use bullet points, and dont add anything outside this structure) and make sure you send it back in json formatting:

{
  "due_diligence": {
    "Executive Summary": "",
    "Company Overview": "",
    "Financial Analysis": "",
    "Technical Price Analysis": "",
    "Market Sentiment": "",
    "Volume and Liquidity Analysis": "",
    "Risk Assessment": "",
    "Valuation": "",
    "Recommendations": ""
  }
}"""},

                {"role": "user", "content": f"Please create a long and extensive report for the stock {stock}. The business due dilligence is this {business_dd} and the technical due dilligence is this {technical_dd}."}
            ],
            max_tokens=15000  # Adjust token limit based on your use case
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"Error generating due diligence report: {e}"
    

def extract_json(llm_output):
    """
    Extract the JSON content from the LLM output.
    
    :param llm_output: str, the raw output from the LLM
    :return: dict, the extracted JSON content
    """
    # Find the start and end of the JSON content
    start = llm_output.find('{')
    end = llm_output.rfind('}') + 1
    
    if start == -1 or end == 0:
        raise ValueError("No valid JSON found in the LLM output")
    
    # Extract the JSON string
    json_str = llm_output[start:end]
    
    # Parse the JSON string into a Python dictionary
    try:
        json_data = json.loads(json_str)
        return json_data
    except json.JSONDecodeError:
        raise ValueError("Invalid JSON format in the LLM output")

# Update the get_hf_due_diligence function
def get_hf_due_diligence(stock, business_dd, technical_dd):
    raw_due_diligence = generate_due_diligence(stock, business_dd, technical_dd)
    try:
        due_diligence_json = extract_json(raw_due_diligence)
        # Convert the JSON to a formatted string
        due_diligence_str = json.dumps(due_diligence_json, indent=2)
        return due_diligence_str
    except ValueError as e:
        return str(e)