1. Clone the Repository
   git clone https://github.dev/ewfx/gaied-next-gen-tech

2.  Install Required Dependencies
    pip install fastapi==0.115.8 google-ai-generativelanguage==0.6.17 greenlet==3.1.1 \
    langchain==0.3.21 langchain-community==0.3.20 langchain-core==0.3.47 \
    langchain-google-genai==2.1.1 langchain-text-splitters==0.3.7 PyMuPDF==1.25.4 \
    streamlit==1.42.2 pytz==2025.1 PyYAML==6.0.2 pyjson5==1.6.8 pyparsing==3.2.1 \
    pypdf==5.4.0
3.  Configure Google Gemini API Key
    Set up your Google Gemini API key inside the configuration file:
    Edit config/setting.py and add your API key.

4.  Start the FastAPI Server
    Open the command prompt, navigate to the project's main directory, and start the server:

    cd D:\NextGenAI-EC
    python -m uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload --workers 1 --loop asyncio

    Once the server is running, you can access the following API endpoints:

    Root Endpoint → GET http://localhost:8000/

    Process Email Endpoint → GET http://localhost:8000/process-emails

5.  Run the UI Application
    Open a new terminal, navigate to the React UI directory, and start the frontend

    cd D:\NextGenAI-EC\react-ui\loan-dashboard
    npm start

This will launch the application in your default web browser, displaying the results in table and chart formats.


