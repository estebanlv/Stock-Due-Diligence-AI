# Stock Due Diligence AI

## Overview

This project provides an API and a web interface for generating due diligence reports on stocks using AI.

## Prerequisites

- Python 3.7 or higher
- Node.js (version X.X.X)
- npm (version X.X.X) or yarn

## API Setup

1. **Clone the Repository**
   ```bash
   git clone https://github.com/estebanlv/stock-due-diligence-ai.git
   cd stock-due-diligence-ai/API
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Create a `.env` File**
   - Copy the example environment file:
   ```bash
   cp .env.example .env
   ```
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

2. **Install Dependencies**
   ```bash
   npm install
   # or
   yarn install
   ```

4. **Run the Website**
   ```bash
   npm start
   # or
   yarn start
   ```

## Conclusion

Your API and website should now be running locally. Ensure that the OpenAI API key is correctly set in the `.env` files. Check the console for any errors during the setup process.
