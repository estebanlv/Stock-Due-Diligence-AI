# Stock Due Diligence AI

## Overview

This project provides an API and a web interface for generating due diligence reports on stocks using AI.

## Prerequisites

- Python 3.7 or higher

## API Setup

1. **Clone the Repository**
   ```bash
   git clone https://github.com/estebanlv/stock-due-diligence-ai.git
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Create a `.env` File**
   - Update the `.env` file with your OpenAI API key and other configurations:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   ```

4. **Run the API**
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000
   ```

## Website Setup

1. **Navigate to the Website Directory**
   ```bash
   cd ../website
   ```

2. **Open the main.html in your prefered browser**
<img width="793" alt="image" src="https://github.com/user-attachments/assets/53858963-12d6-4d7f-9ddb-5688e100d6e3">


## Conclusion

Your API and website should now be running locally. Ensure that the OpenAI API key is correctly set in the `.env` files. Check the console for any errors during the setup process.
