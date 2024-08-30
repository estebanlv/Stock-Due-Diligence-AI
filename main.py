from business_analyst import get_business_dd
from technical_analyst import get_technical_dd
from hf_manager import get_hf_due_diligence

def main():
    """
    Main function to execute the due diligence report generation and saving process.
    """
    stock = "MSFT"  # Example stock symbol
    business_dd_report = get_business_dd(stock)
    technical_dd_report = get_technical_dd(stock)
    #print(business_dd_report)
    #print(technical_dd_report)
    final_dd = get_hf_due_diligence(stock, business_dd_report, technical_dd_report)
    print(final_dd)

if __name__ == "__main__":
    main()
