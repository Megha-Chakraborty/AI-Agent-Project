import streamlit as st
import pandas as pd
import requests
import openai
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SERP_API_KEY = os.getenv("SERP_API_KEY")

# Function to authenticate Google Sheets
def authenticate_google_sheets(credentials_file):
    credentials = Credentials.from_service_account_file(
        credentials_file, scopes=['https://www.googleapis.com/auth/spreadsheets.readonly']
    )
    service = build('sheets', 'v4', credentials=credentials)
    return service

# Function to load data from Google Sheets
def load_google_sheet(service, spreadsheet_id, range_name):
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()
    values = result.get('values', [])
    if not values:
        return None
    return pd.DataFrame(values[1:], columns=values[0])

# Function to perform a web search
def perform_web_search(query):
    url = f"https://serpapi.com/search.json?q={query}&api_key={SERP_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Web search failed. Please check your API key or query.")
        return {}

# Function to process results using OpenAI GPT
def process_with_llm(query, search_results):
    openai.api_key = OPENAI_API_KEY  # Set your OpenAI API key

    # Construct the prompt for OpenAI
    prompt = f"Extract information based on the query: '{query}'.\n\nSearch results:\n{search_results}"

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",  # Use "gpt-3.5-turbo" if "gpt-4" is not available
            messages=[
                {"role": "system", "content": "You are an assistant that extracts specific information from web search results."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=300
        )

        # Extract and return the LLM's response
        return response['choices'][0]['message']['content'].strip()

    except Exception as e:
        st.error(f"Error with OpenAI API: {e}")
        return None


# Streamlit app
def main():
    st.title("AI Agent Dashboard")
    st.sidebar.header("Navigation")
    page = st.sidebar.radio("Choose a page:", ["File Upload", "Google Sheets", "Results"])

    # Data storage
    if "data" not in st.session_state:
        st.session_state.data = None
    if "results" not in st.session_state:
        st.session_state.results = None

    # File Upload Page
    if page == "File Upload":
        st.header("Upload CSV File")
        uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])
        if uploaded_file:
            st.session_state.data = pd.read_csv(uploaded_file)
            st.write("Preview of uploaded data:")
            st.write(st.session_state.data)

    # Google Sheets Page
    elif page == "Google Sheets":
        st.header("Connect to Google Sheets")
        credentials_file = st.text_input("Enter the path to your credentials.json file:")
        spreadsheet_id = st.text_input("Enter your Google Spreadsheet ID:")
        range_name = st.text_input("Enter the range (e.g., Sheet1!A1:D10):")

        if st.button("Load Google Sheet"):
            if credentials_file and spreadsheet_id and range_name:
                try:
                    service = authenticate_google_sheets(credentials_file)
                    sheet_data = load_google_sheet(service, spreadsheet_id, range_name)
                    if sheet_data is not None:
                        st.session_state.data = sheet_data
                        st.write("Preview of Google Sheet data:")
                        st.write(sheet_data)
                    else:
                        st.error("Failed to load data. Please check your inputs.")
                except Exception as e:
                    st.error(f"Error: {e}")
            else:
                st.warning("Please provide all required inputs.")

    # Results Page
    elif page == "Results":
        st.header("Generate Results")
        if st.session_state.data is not None:
            query_template = st.text_input("Enter your query template (e.g., Get the email of {company}):")

            if st.button("Generate Results"):
                results = []
                for _, row in st.session_state.data.iterrows():
                    entity = row[0]  # Assume the first column contains the entities
                    query = query_template.format(company=entity)
                    search_results = perform_web_search(query)
                    llm_output = process_with_llm(query, search_results)
                    results.append({"Entity": entity, "Result": llm_output})

                st.session_state.results = pd.DataFrame(results)
                st.success("Results generated successfully!")

        if st.session_state.results is not None:
            st.write("Results:")
            st.write(st.session_state.results)
            st.download_button(
                label="Download Results as CSV",
                data=st.session_state.results.to_csv(index=False).encode('utf-8'),
                file_name="results.csv",
                mime="text/csv"
            )
        else:
            st.warning("No results to display. Please upload data and generate results.")

if __name__ == "__main__":
    main()