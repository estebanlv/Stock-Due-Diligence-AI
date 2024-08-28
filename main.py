import openai
import yfinance as yf
import requests
from bs4 import BeautifulSoup
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
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
    
    # Replace with your actual OpenAI API key
    openai.api_key = os.getenv('OPENAI_API_KEY')
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a seasoned financial expert specializing in due diligence. Your role is to provide thorough and insightful analysis of financial documents, market conditions, and business operations to assess risks, validate data accuracy, and identify potential opportunities. Use your extensive knowledge in financial modeling, valuation techniques, industry trends, and regulatory compliance to support informed decision-making. Be detail-oriented, objective, and proactive in offering recommendations and highlighting key findings. Your advice should be clear, concise, and grounded in best practices of financial due diligence."},
                {"role": "user", "content": f"Conduct a comprehensive due diligence analysis (3000 words) on the following stock: {stock}. Use the recent news articles provided below for additional context:\n{news_content}\n\nPlease structure your report using the following HTML format for pdfkit rendering, and don't add anything outside of the html, and no bullet points:\n\n<!DOCTYPE html>\n<html>\n<head>\n<style>\nbody {{ font-family: Arial, sans-serif; margin: 30px; }}\nh1 {{ font-size: 24px; text-align: center; margin-bottom: 20px; }}\nh2 {{ font-size: 18px; color: #333; margin-top: 20px; }}\np {{ font-size: 12px; line-height: 1.5; }}\n</style>\n</head>\n<body>\n<h1>Due Diligence Report on {stock}</h1>\n<h2>1. Executive Summary</h2>\n<p>Provide a high-level overview of the key findings, including potential risks and opportunities.</p>\n\n<h2>2. Company Overview</h2>\n<p>Summarize the company’s business model, industry positioning, and key products or services.</p>\n\n<h2>3. Financial Analysis</h2>\n<p>Analyze recent financial statements and key financial ratios (e.g., P/E ratio, revenue growth, profit margins, etc.). Highlight any trends or concerns.</p>\n\n<h2>4. Market and Industry Analysis</h2>\n<p>Assess the market conditions, industry trends, and competitive landscape. Discuss how these factors might impact the company’s performance.</p>\n\n<h2>5. News and Events</h2>\n<p>Evaluate the recent news articles provided, identifying significant events or announcements that could affect the company’s stock price.</p>\n\n<h2>6. Risk Assessment</h2>\n<p>Identify potential risks, including financial, operational, regulatory, and market risks.</p>\n\n<h2>7. Valuation</h2>\n<p>Offer an estimate of the stock’s intrinsic value using relevant valuation methods (e.g., discounted cash flow analysis, comparable company analysis).</p>\n\n<h2>8. Recommendations</h2>\n<p>Provide a clear recommendation (e.g., buy, hold, sell) based on your analysis, including a rationale for your decision.</p>\n\n</body>\n</html>\n"}
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

def main():
    """
    Main function to execute the due diligence report generation and saving process.
    """
    stock = "GOOG"  # Example stock symbol
    due_diligence_report = generate_due_diligence(stock)
    cleaned_report = remove_html_tags(due_diligence_report)
    print(cleaned_report)
    save_html_to_file(cleaned_report)

if __name__ == "__main__":
    main()
