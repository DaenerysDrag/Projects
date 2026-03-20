# Flipkart Scraper — Claude Session Notes

## Project Goal
Build a fully autonomous Flipkart scraper that extracts washing machine product data for Samsung, LG, Whirlpool, and Haier daily and stores it in Excel.

---

## Current Status: WORKING ✅
The scraper is fully functional and extracting real-time data from Flipkart.

Last successful run: **2026-03-17**
- 288 products scraped (72 per brand × 4 brands)
- 24 products per page × 3 pages per brand
- Data saved to `data/Flipkart_WashingMachines.xlsx`

---

## Project Structure
```
flipkart_scraper/
├── data/
│   └── Flipkart_WashingMachines.xlsx   ← scraped output (4 sheets, one per brand)
├── logs/
│   └── YYYY-MM-DD_HH-MM-SS.log
├── src/
│   └── flipkart_scraper/
│       ├── components/
│       │   ├── data_ingestion.py        ← scraping logic
│       │   ├── data_processing.py       ← cleaning + validation
│       │   └── data_storage.py          ← Excel append with dedup
│       ├── utils/
│       │   └── common.py                ← logging setup
│       ├── config.py                    ← all settings live here
│       └── main.py                      ← entry point
├── CLAUDE.md                            ← this file
├── README.md
├── requirements.txt
└── setup.py
```

---

## How to Run
```bash
cd flipkart_scraper
pip3 install -r requirements.txt
PYTHONPATH=src python3 src/flipkart_scraper/main.py
```

Or after installing as a package:
```bash
pip install -e .
flipkart-scraper
```

---

## Key Technical Decisions Made

### 1. Pinned User-Agent (Critical)
Flipkart serves **different HTML structures** depending on the User-Agent:
- `fake_useragent` (random rotation) → sometimes returns React Native Web classes (`css-g5y9jx`) with no stable selectors → **breaks scraping**
- Chrome desktop UA → consistently returns structured HTML with stable class names → **works**

**Fixed in `config.py`:**
```python
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/90.0.4430.212 Safari/537.36"
)
```
`fake_useragent` is no longer used in ingestion.

### 2. Current Working CSS Selectors (as of 2026-03-17)
These are the live Flipkart class names — if scraping breaks in future, these are the first thing to re-inspect:

| Field | Tag | Class |
|---|---|---|
| Product card (container) | `div` | `nZIRY7` |
| Product name | `div` | `RG5Slk` |
| Product link | `a` | `k7wcnx` |
| Selling price | `div` | `DeU9vF` |
| Rating | `span` | `CjyrHS` |
| Reviews | `span` | `PvbNMB` |

If selectors break, run this to re-map them:
```python
import requests
from bs4 import BeautifulSoup, re
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"
resp = requests.get("https://www.flipkart.com/search?q=Samsung+washing+machine", headers={"User-Agent": UA}, timeout=15)
soup = BeautifulSoup(resp.content, "html.parser")
node = soup.find(string=re.compile("Samsung.*kg"))
el = node.parent
for i in range(10):
    print(f"Level {i}: <{el.name} class='{' '.join(el.get('class', []))}'>")
    el = el.parent
```

### 3. Pagination
Scrapes up to `MAX_PAGES = 3` pages per brand. Stops early if a page returns 0 products. Change `MAX_PAGES` in `config.py` to scrape more/fewer pages.

### 4. Duplicate Detection
Before appending to Excel, `data_storage.py` reads all existing URLs in the sheet and skips rows that already exist. Safe to run multiple times per day.

### 5. Data Validation
`data_processing.py` drops any row where `Price` is missing or zero after cleaning.

---

## config.py — All Tuneable Settings
```python
BRANDS = ["Samsung", "LG", "Whirlpool", "Haier"]  # add/remove brands here
EXCEL_FILENAME = 'Flipkart_WashingMachines.xlsx'
RETRIES = 3
BACKOFF_FACTOR = 0.5
MAX_PAGES = 3
REQUEST_TIMEOUT = 15
USER_AGENT = "Mozilla/5.0 ..."
```

---

## Fields Extracted Per Product
| Column | Example |
|---|---|
| Brand | Samsung |
| Product Name | Samsung 7 kg 5 Star, Ecobubble... |
| Model | WW70T4S21VX (if in name) |
| Price | 17490.0 |
| Rating | 4.3 |
| Number of Reviews | 114958.0 |
| URL | https://www.flipkart.com/... |
| Timestamp | 2026-03-17 03:59:20 |

---

## What Was Fixed in This Session
1. **Stale CSS selectors** → updated to current live selectors
2. **Inconsistent UA** → pinned to Chrome desktop UA
3. **No pagination** → added multi-page loop
4. **DataFrame crash on None** → safe `.astype(str)` before all `.str` ops
5. **No duplicate detection** → URL-based dedup in storage
6. **No data validation** → drop rows with invalid price
7. **Missing setup.py** → created with CLI entry point
8. **Incomplete .gitignore** → added logs/, data/, .env, IDE dirs

---

## Potential Next Steps (Not Started Yet)
- Add more product categories beyond washing machines
- Add more brands
- Schedule automation (cron / GitHub Actions / Task Scheduler)
- Switch storage from Excel to a database (PostgreSQL / SQLite)
- Build a dashboard or API on top of the data
- Add price history tracking / price drop alerts
- Scrape additional fields (seller name, delivery date, offers)
