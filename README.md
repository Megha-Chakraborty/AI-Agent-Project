# AI Agent Project  

## Project Description  
The **AI Agent Dashboard** is a versatile tool designed to simplify and automate data retrieval and processing tasks. It integrates with Google Sheets and allows users to execute custom search queries, retrieve relevant information from the web, and update their datasets dynamically. The dashboard supports CSV uploads, Google Sheets integration, and efficient handling of API-driven tasks.

---

## Setup Instructions  

### 1. Prerequisites  
- Ensure **Python 3.7+** is installed on your system.  
- Install **pip** for package management.

### 2. Download the Project  
Clone or download the project to your local machine.

### 3. Install Dependencies  
Install the necessary libraries by running:  
```bash  
pip install -r requirements.txt  
```
### 4. Configure API Keys and Environment Variables
To run the application successfully, you need to configure API keys and environment variables.
- Create a .env file in the project directory and add the following keys:
  ```bash
  SERPAPI_KEY=your_serpapi_key
  OPENAI_API_KEY=your_openai_key
  GOOGLE_APPLICATION_CREDENTIALS=path_to_google_credentials_file.json
  ```
  ### 5. Start the Application
- To start the application, run the following command:
  ```bash
  streamlit run ai_agent.py
  ```

  ## Usage Guide
  ### 1. Connecting Google Sheets
  - In your Google Sheets document, go to File > Share, and generate a shareable link with "Anyone with the link" access.
  - In the .env file, set the GOOGLE_APPLICATION_CREDENTIALS variable to the path of your Google Sheets credentials file.

  ## 2. Setting Up Search Queries
  - The dashboard allows you to customize and execute search queries.
  - Input your query in the designated field within the dashboard interface, and the AI Agent will process the request and display the relevant results.
 
  ## API Keys and Environment Variables
  - To run the application successfully, you need to enter your API keys and credentials.
  1. SERPAPI_KEY: Obtain your API key from SerpApi.
  2. OPENAI_API_KEY: Create an API key from OpenAI.
  3. GOOGLE_APPLICATION_CREDENTIALS: Download the Google credentials file from your Google Cloud Console.
  - Ensure these credentials are correctly entered in the .env file for smooth operation.

  ## Optional Features
  - CSV Uploads: Upload CSV files directly to the dashboard for automatic processing and updates.
  - Custom Search Queries: Users can define their custom search queries that the AI agent will use to fetch relevant data.
  
