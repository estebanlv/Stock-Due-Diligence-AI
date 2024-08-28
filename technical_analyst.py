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
            {"role": "user","content": f"Conduct a comprehensive technical analysis (3000 words) on the following stock: {symbol}. Use the recent news articles provided below for additional context:\n{data}\n\nPlease structure your report using the following HTML format for pdfkit rendering, and don't add anything outside of the html, and no bullet points:\n\n<!DOCTYPE html>\n<html>\n<head>\n<style>\nbody {{ font-family: Arial, sans-serif; margin: 30px; }}\nh1 {{ font-size: 24px; text-align: center; margin-bottom: 20px; }}\nh2 {{ font-size: 18px; color: #333; margin-top: 20px; }}\np {{ font-size: 12px; line-height: 1.5; }}\n</style>\n</head>\n<body>\n<h1>Technical Analysis Report on {symbol}</h1>\n<h2>1. Executive Summary</h2>\n<p>Provide a high-level overview of the key findings, including potential price trends and trading signals.</p>\n\n<h2>2. Stock Overview</h2>\n<p>Summarize the company’s stock performance, including its historical price movements, trading volume, and volatility.</p>\n\n<h2>3. Price Pattern Analysis</h2>\n<p>Examine recent price patterns using technical indicators such as moving averages, support and resistance levels, and trend lines. Highlight any notable patterns.</p>\n\n<h2>4. Technical Indicators</h2>\n<p>Analyze key technical indicators (e.g., RSI, MACD, Bollinger Bands) and what they suggest about the stock's momentum, strength, and potential reversals.</p>\n\n<h2>5. Market Sentiment</h2>\n<p>Assess the overall market sentiment and its impact on the stock. Consider sentiment analysis from recent news articles and social media trends.</p>\n\n<h2>6. Volume and Liquidity Analysis</h2>\n<p>Evaluate the trading volume and liquidity of the stock to understand the ease of buying and selling, and potential for price manipulation.</p>\n\n<h2>7. Risk and Volatility Assessment</h2>\n<p>Identify the volatility of the stock and potential risks associated with trading it. Use statistical measures such as beta and standard deviation.</p>\n\n<h2>8. Recommendations</h2>\n<p>Provide a clear trading recommendation (e.g., buy, hold, sell) based on your technical analysis, including specific entry and exit points and a rationale for your decision.</p>\n\n</body>\n</html>\n"}
            ],
            max_tokens=15000  # Adjust token limit based on your use case
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"Error generating due diligence report: {e}"
    
def remove_html_tags(input_text):
    """
    Removes specific HTML-related tags from a string.
    
    :param input_text: str, the input string containing HTML tags.
    :return: str, cleaned string without specific HTML tags.
    """
    if input_text.startswith("```html") or input_text.startswith("'''html"):
        input_text = input_text[7:]
    if input_text.endswith("```") or input_text.endswith("'''"):
        input_text = input_text[:-3]
    return input_text.strip()

def save_html_to_file(html_content, file_name='Due_Diligence_Report.html'):
    """
    Saves a given HTML content string to a specified .html file.
    
    :param html_content: str, The HTML content to be saved.
    :param file_name: str, The name of the file to save the content to.
                      Defaults to 'Due_Diligence_Report.html'.
    """
    if not file_name.endswith('.html'):
        file_name += '.html'
    
    try:
        with open(file_name, 'w', encoding='utf-8') as file:
            file.write(html_content)
        print(f"HTML content has been saved to {file_name}.")
    except Exception as e:
        print(f"An error occurred while saving the HTML content: {e}")


def get_technical_dd(symbol):
    due_diligence = generate_due_diligence(symbol)
    cleaned_report = remove_html_tags(due_diligence)
    print(cleaned_report)
    save_html_to_file(cleaned_report)
    return due_diligence

# Example usage:
# dd = get_technical_dd("AAPL")
# print(dd)
