# Flipkart Washing Machine Scraper

This is a fully autonomous Python-based agent that extracts washing machine data for Samsung, LG, Whirlpool, and Haier from Flipkart every morning at 8:00 AM, stores the results in an Excel file, logs each run, prevents blocking, and maintains a long-term daily dataset.

## Features

- Scrapes product data for Samsung, LG, Whirlpool, and Haier washing machines.
- Cleans, validates, and normalizes the scraped data.
- Stores the data in an Excel file with a separate sheet for each brand.
- Appends new data daily without overwriting existing data.
- Logs each run, including any errors.
- Rotates user agents and uses random delays to avoid being blocked.
- Includes retry logic and error recovery.
- Modular and scalable architecture.

## Architecture

The agent is designed with a modular architecture, separating the concerns of data ingestion, processing, and storage.

- **Data Ingestion (`data_ingestion.py`):** This module is responsible for scraping the data from Flipkart. It uses the `requests` and `BeautifulSoup` libraries to fetch and parse the HTML, and `fake_useragent` to rotate user agents.
- **Data Processing (`data_processing.py`):** This module cleans and normalizes the raw data scraped from Flipkart. It uses the `pandas` library to perform data manipulation and cleaning.
- **Data Storage (`data_storage.py`):** This module stores the processed data in an Excel file. It uses the `pandas` and `openpyxl` libraries to handle Excel operations.
- **Logging (`common.py`):** The agent uses Python's built-in `logging` module to log its activities and any errors that occur.
- **Main (`main.py`):** This is the entry point of the application. It orchestrates the entire process, from scraping to storing the data.

## Project Structure
```
flipkart_scraper/
├── data/
│   └── Flipkart_WashingMachines.xlsx
├── logs/
│   └── YYYY-MM-DD_HH-MM-SS.log
├── src/
│   └── flipkart_scraper/
│       ├── components/
│       │   ├── __init__.py
│       │   ├── data_ingestion.py
│       │   ├── data_processing.py
│       │   └── data_storage.py
│       ├── utils/
│       │   ├── __init__.py
│       │   └── common.py
│       ├── __init__.py
│       ├── config.py
│       └── main.py
├── .gitignore
├── README.md
├── requirements.txt
└── setup.py
```

## Setup and Installation

1. **Clone the repository:**
   ```bash
   git clone <repository_url>
   cd flipkart_scraper
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. **Install the required packages:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

To run the scraper manually, execute the `main.py` script:
```bash
python src/flipkart_scraper/main.py
```

## Scheduling

You can schedule the agent to run automatically at 8:00 AM daily using one of the following methods:

### Windows Task Scheduler

1. **Open Task Scheduler:** Search for "Task Scheduler" in the Start Menu and open it.
2. **Create a new task:** In the "Actions" pane on the right, click "Create Basic Task...".
3. **Name the task:** Give the task a name (e.g., "Flipkart Scraper") and a description, then click "Next".
4. **Set the trigger:** Choose "Daily" and click "Next". Set the start time to "8:00:00 AM" and click "Next".
5. **Set the action:** Choose "Start a program" and click "Next".
6. **Configure the action:**
   - In the "Program/script" field, browse to the location of your Python executable within your virtual environment (e.g., `C:\path\to\flipkart_scraper\venv\Scripts\python.exe`).
   - In the "Add arguments (optional)" field, enter the path to the `main.py` script (e.g., `src\flipkart_scraper\main.py`).
   - In the "Start in (optional)" field, enter the path to the `flipkart_scraper` directory.
7. **Finish:** Review the settings and click "Finish".

### PythonAnywhere

1. **Upload your project:** Upload your `flipkart_scraper` project to your PythonAnywhere account.
2. **Open the "Tasks" tab:** Navigate to the "Tasks" tab in your PythonAnywhere dashboard.
3. **Create a new task:**
   - Set the time to "08:00".
   - In the "Command" field, enter the command to run your script, making sure to use the full path to your virtual environment's Python interpreter and the `main.py` script:
     ```bash
     /home/your_username/path/to/flipkart_scraper/venv/bin/python /home/your_username/path/to/flipkart_scraper/src/flipkart_scraper/main.py
     ```
   - Click "Create".

### GitHub Actions

1. **Create a workflow file:** In your repository, create a new directory called `.github/workflows`. Inside this directory, create a new file called `schedule.yml`.
2. **Add the workflow configuration:** Paste the following code into the `schedule.yml` file:
   ```yaml
   name: Run Flipkart Scraper

   on:
     schedule:
       - cron: '0 8 * * *'  # Runs at 8:00 AM UTC every day

   jobs:
     build:
       runs-on: ubuntu-latest

       steps:
         - name: Checkout repository
           uses: actions/checkout@v2

         - name: Set up Python
           uses: actions/setup-python@v2
           with:
             python-version: '3.x'

         - name: Install dependencies
           run: |
             python -m pip install --upgrade pip
             pip install -r requirements.txt

         - name: Run scraper
           run: python src/flipkart_scraper/main.py

         - name: Commit and push changes
           uses: stefanzweifel/git-auto-commit-action@v4
           with:
             commit_message: "Update data"
             branch: main
             file_pattern: data/Flipkart_WashingMachines.xlsx logs/*.log
   ```
3. **Commit the file:** Commit and push the `schedule.yml` file to your repository. The scraper will now run automatically at 8:00 AM UTC every day.

## Scalability and Future Extensibility

The agent is designed to be scalable and extensible.

- **Adding new brands:** To scrape data for a new brand, simply add the brand's name to the `brands` list in the `main.py` file.
- **Adding new data points:** To scrape additional data points, you will need to update the `scrape` method in the `data_ingestion.py` file to extract the new data, and the `DataProcessor` class in the `data_processing.py` file to clean and process it.
- **API integration:** The modular design makes it easy to add an API to the agent. You could create a new module that uses a web framework like Flask or FastAPI to expose the scraped data through an API endpoint. This would allow you to build a dashboard or other applications that consume the data.
- **Database storage:** While the agent currently stores data in an Excel file, it could be easily modified to store the data in a database like PostgreSQL or MongoDB. This would be a more robust and scalable solution for storing large amounts of data.
