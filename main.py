from business_analyst import get_business_dd
from technical_analyst import get_technical_dd


def main():
    """
    Main function to execute the due diligence report generation and saving process.
    """
    stock = "GOOG"  # Example stock symbol
    business_dd_report = get_business_dd(stock)
    technical_dd_report = get_technical_dd(stock)
    print(business_dd_report)
    print(technical_dd_report)

if __name__ == "__main__":
    main()
