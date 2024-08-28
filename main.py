import openai
import yfinance as yf
import requests
from bs4 import BeautifulSoup
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

def get_recent_news(stock):
    # Fetch stock information using yfinance
    stock_info = yf.Ticker(stock)
    
    # Get news data
    news_data = stock_info.news
    
    news_details = []
    for news_item in news_data:
        title = news_item.get('title')
        link = news_item.get('link')
        if title and link:
            # Fetch the content of the news article
            news_content = fetch_news_content(link)
            news_details.append({'title': title, 'content': news_content})
    
    return news_details

def fetch_news_content(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Example: Scraping the main content of the article
            # This part may need to be adjusted based on the website's structure
            paragraphs = soup.find_all('p')
            content = ' '.join([p.get_text() for p in paragraphs])
            return content
        else:
            return "Failed to retrieve content"
    except Exception as e:
        return f"Error fetching content: {e}"

def generate_due_diligence(stock):
    news_details = get_recent_news(stock)
    
    if not news_details:
        return "No news found for the given stock."
    
    news_content = ""
    for news in news_details:
        news_content += f"Title: {news['title']}\nContent: {news['content']}\n\n"
    
    openai.api_key = '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'  # Replace with actual key
    print("here")
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a seasoned financial expert specializing in due diligence. Your role is to provide thorough and insightful analysis of financial documents, market conditions, and business operations to assess risks, validate data accuracy, and identify potential opportunities. Use your extensive knowledge in financial modeling, valuation techniques, industry trends, and regulatory compliance to support informed decision-making. Be detail-oriented, objective, and proactive in offering recommendations and highlighting key findings. Your advice should be clear, concise, and grounded in best practices of financial due diligence."},
            {"role": "user", "content": f"Conduct a comprehensive due diligence analysis (3000 words) on the following stock: {stock}. Use the recent news articles provided below for additional context:\n{news_content}\n\nPlease structure your report using the following HTML format for pdfkit rendering, and dont add anything outside of the html, and no bulletpoints:\n\n```html\n<!DOCTYPE html>\n<html>\n<head>\n<style>\nbody {{ font-family: Arial, sans-serif; margin: 30px; }}\nh1 {{ font-size: 24px; text-align: center; margin-bottom: 20px; }}\nh2 {{ font-size: 18px; color: #333; margin-top: 20px; }}\np {{ font-size: 12px; line-height: 1.5; }}\n</style>\n</head>\n<body>\n<h1>Due Diligence Report on {stock}</h1>\n<h2>1. Executive Summary</h2>\n<p>Provide a high-level overview of the key findings, including potential risks and opportunities.</p>\n\n<h2>2. Company Overview</h2>\n<p>Summarize the company’s business model, industry positioning, and key products or services.</p>\n\n<h2>3. Financial Analysis</h2>\n<p>Analyze recent financial statements and key financial ratios (e.g., P/E ratio, revenue growth, profit margins, etc.). Highlight any trends or concerns.</p>\n\n<h2>4. Market and Industry Analysis</h2>\n<p>Assess the market conditions, industry trends, and competitive landscape. Discuss how these factors might impact the company’s performance.</p>\n\n<h2>5. News and Events</h2>\n<p>Evaluate the recent news articles provided, identifying significant events or announcements that could affect the company’s stock price.</p>\n\n<h2>6. Risk Assessment</h2>\n<p>Identify potential risks, including financial, operational, regulatory, and market risks.</p>\n\n<h2>7. Valuation</h2>\n<p>Offer an estimate of the stock’s intrinsic value using relevant valuation methods (e.g., discounted cash flow analysis, comparable company analysis).</p>\n\n<h2>8. Recommendations</h2>\n<p>Provide a clear recommendation (e.g., buy, hold, sell) based on your analysis, including a rationale for your decision.</p>\n\n</body>\n</html>\n```\n\nEnsure your analysis is well-supported with data, and provide references or assumptions where applicable."}
],
        max_tokens=10000
    )
    
    return response['choices'][0]['message']['content']

def remove_html_tags(input_text):
    # Remove starting '''html or ```html (both variations)
    if input_text.startswith("```html") or input_text.startswith("'''html"):
        input_text = input_text[7:]  # Remove the first 7 characters (```html or '''html)

    # Remove ending ``` or '''
    if input_text.endswith("```") or input_text.endswith("'''"):
        input_text = input_text[:-3]  # Remove the last 3 characters (``` or ''')

    # Strip any leading/trailing whitespace
    return input_text.strip()


def save_html_to_file(html_content, file_name):
    # Ensure the file name ends with '.html'
    if not file_name.endswith('.html'):
        file_name += '.html'
    try:
        # Open the file in write mode to update its content
        with open(file_name, 'w', encoding='utf-8') as file:
            file.write(html_content)
        print(f"HTML content has been saved to {file_name}.")
    except Exception as e:
        print(f"An error occurred while saving the HTML content: {e}")

def main():
    #stock = input("Enter the stock symbol (e.g., AAPL): ")
    stock = "MSFT"
    due_diligence_report = generate_due_diligence(stock)
    due_diligence_report = remove_html_tags(due_diligence_report)
    print(due_diligence_report)
    save_html_to_file(due_diligence_report, 'Due_Diligence_Report.html')


if __name__ == "__main__":
    main()