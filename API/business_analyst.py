import openai
import yfinance as yf
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

def get_recent_news(stock):
    """
    Fetch recent news related to the given stock using yfinance.
    
    :param stock: str, the stock symbol (e.g., "AAPL").
    :return: list of dict, each containing 'title' and 'content' of the news.
    """
    try:
        stock_info = yf.Ticker(stock)
        news_data = stock_info.news

        news_details = []
        for news_item in news_data:
            title = news_item.get('title')
            link = news_item.get('link')
            if title and link:
                news_content = fetch_news_content(link)
                news_details.append({'title': title, 'content': news_content})
        return news_details
    except Exception as e:
        print(f"An error occurred while fetching news: {e}")
        return []

def fetch_news_content(url):
    """
    Fetch the content of a news article from the given URL.
    
    :param url: str, URL of the news article.
    :return: str, the content of the news article.
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            paragraphs = soup.find_all('p')
            content = ' '.join([p.get_text() for p in paragraphs])
            return content
        else:
            return f"Failed to retrieve content. Status code: {response.status_code}"
    except requests.exceptions.RequestException as e:
        return f"Error fetching content: {e}"

def generate_due_diligence(stock):
    """
    Generate a due diligence report for the given stock using OpenAI API.
    
    :param stock: str, the stock symbol (e.g., "AAPL").
    :return: str, HTML content of the due diligence report.
    """
    news_details = get_recent_news(stock)
    
    if not news_details:
        return "No news found for the given stock."
    
    news_content = ""
    for news in news_details:
        news_content += f"Title: {news['title']}\nContent: {news['content']}\n\n"
    
    # Replace with your actual OpenAI API key in a .env file
    openai.api_key = os.getenv('OPENAI_API_KEY')
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a seasoned financial expert specializing in due diligence. Your role is to provide thorough and insightful analysis of financial documents, market conditions, and business operations to assess risks, validate data accuracy, and identify potential opportunities. Use your extensive knowledge in financial modeling, valuation techniques, industry trends, and regulatory compliance to support informed decision-making. Be detail-oriented, objective, and proactive in offering recommendations and highlighting key findings. Your advice should be clear, concise, and grounded in best practices of financial due diligence."},
                {"role": "user", "content": f"""
Conduct a comprehensive due diligence analysis (3000 words) on the following stock: {stock}. Use the recent news articles provided below for additional context:

{news_content}

Please structure your report using the following format, and its very important that you make no bullet points or lists:

Due Diligence Report on {stock}

1. Executive Summary
Provide a high-level overview of the key findings, including potential risks and opportunities.

2. Company Overview
Summarize the company’s business model, industry positioning, and key products or services.

3. Financial Analysis
Analyze recent financial statements and key financial ratios (e.g., P/E ratio, revenue growth, profit margins, etc.). Highlight any trends or concerns.

4. Market and Industry Analysis
Assess the market conditions, industry trends, and competitive landscape. Discuss how these factors might impact the company’s performance.

5. News and Events
Evaluate the recent news articles provided, identifying significant events or announcements that could affect the company’s stock price.

6. Risk Assessment
Identify potential risks, including financial, operational, regulatory, and market risks.

7. Valuation
Offer an estimate of the stock’s intrinsic value using relevant valuation methods (e.g., discounted cash flow analysis, comparable company analysis).

8. Recommendations
Provide a clear recommendation (e.g., buy, hold, sell) based on your analysis, including a rationale for your decision.
"""}
            ],
            max_tokens=15000  # Adjust token limit based on your use case
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"Error generating due diligence report: {e}"

def get_business_dd(stock):
    due_diligence = generate_due_diligence(stock)
    return due_diligence