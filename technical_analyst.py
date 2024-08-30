import yfinance as yf
import openai
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

def get_technical_data(symbol):
    # Create the Ticker object
    ticker = yf.Ticker(symbol)
    
    # Extracting various data as specified
    data = {
        "Info": ticker.info,
        "Calendar": ticker.calendar,
        "SEC Filings": ticker.sec_filings,
        "Income Statement": ticker.income_stmt,
        "Quarterly Income Statement": ticker.quarterly_income_stmt,
        "Balance Sheet": ticker.balance_sheet,
        "Quarterly Balance Sheet": ticker.quarterly_balance_sheet,
        "Cash Flow Statement": ticker.cashflow,
        "Quarterly Cash Flow Statement": ticker.quarterly_cashflow,
        "Recommendations": ticker.recommendations,
        "Recommendations Summary": ticker.recommendations_summary,
        "Upgrades and Downgrades": ticker.upgrades_downgrades,
        "Analyst Price Targets": ticker.analyst_price_targets,
        "Earnings Estimate": ticker.earnings_estimate,
        "Revenue Estimate": ticker.revenue_estimate,
        "Earnings History": ticker.earnings_history,
        "EPS Trend": ticker.eps_trend,
        "EPS Revisions": ticker.eps_revisions,
        "Growth Estimates": ticker.growth_estimates,
    }
    
    # Formatting the output
    result = ""
    for section, content in data.items():
        result += f"--- {section} ---\n"
        result += str(content) + "\n\n"
    
    return result


def generate_due_diligence(symbol):
    """
    Generate a due diligence report for the given stock using OpenAI API.
    
    :param stock: str, the stock symbol (e.g., "AAPL").
    :return: str, HTML content of the due diligence report.
    """
    data = get_technical_data(symbol)
    
    # Replace with your actual OpenAI API key
    openai.api_key = os.getenv('OPENAI_API_KEY')
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages = [
            {"role": "system", "content": "You are a seasoned data analyst specializing in financial decision-making. Your role is to utilize data-driven insights to perform thorough and insightful analyses of financial documents, market conditions, and business operations. Your aim is to assess risks, validate data accuracy, and identify potential opportunities. Leverage your expertise in data analysis, financial modeling, valuation techniques, industry trends, and regulatory compliance to support informed decision-making. Be detail-oriented, objective, and proactive in offering recommendations and highlighting key findings. Your advice should be clear, concise, and grounded in best practices of financial analysis and data interpretation."},
            {"role": "user","content": f"""
Conduct a comprehensive technical analysis (3000 words) on the following stock: {symbol}. Use the recent news articles provided below for additional context: {data} Please structure your report using the following format, and its very important that you make no bullet points or lists:

Technical Analysis Report on {symbol}

1. Executive Summary
Provide a high-level overview of the key findings, including potential price trends and trading signals.

2. Stock Overview
Summarize the company’s stock performance, including its historical price movements, trading volume, and volatility.

3. Price Pattern Analysis
Examine recent price patterns using technical indicators such as moving averages, support and resistance levels, and trend lines. Highlight any notable patterns.

4. Market Sentiment
Assess the overall market sentiment and its impact on the stock. Consider sentiment analysis from recent news articles and social media trends.

5. Volume and Liquidity Analysis
Evaluate the trading volume and liquidity of the stock to understand the ease of buying and selling, and potential for price manipulation.

6. Risk and Volatility Assessment
Identify the volatility of the stock and potential risks associated with trading it. Use statistical measures such as beta and standard deviation.

7. Recommendations
Provide a clear trading recommendation (e.g., buy, hold, sell) based on your technical analysis, including specific entry and exit points and a rationale for your decision.
"""}
            ],
            max_tokens=15000  # Adjust token limit based on your use case
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"Error generating due diligence report: {e}"


def get_technical_dd(symbol):
    due_diligence = generate_due_diligence(symbol)
    return due_diligence

# Example usage:
# dd = get_technical_dd("AAPL")
# print(dd)
