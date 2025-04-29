from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import pandas as pd
import time

# 1. Set up Selenium
driver = webdriver.Chrome()  # or your browser driver
driver.get("https://www.aljazeera.com/middle-east/")

# Allow the use of cookies and wait for the page to load
time.sleep(5)

# 2. Keep clicking "Show more"
while True:
    try:
        show_more = driver.find_element(By.CLASS_NAME, "show-more-button")
        show_more.click()
        time.sleep(3)  # Wait for articles to load
    except Exception:
        print("No more articles to load.")
        break

# 3. Parse the page
soup = BeautifulSoup(driver.page_source, 'html.parser')
articles = soup.find_all('article')

data = []

# 4. For each article, collect link and title
for article in articles:
    # Title and URL
    h3_tag = article.find('h3', class_="gc__title")
    a_tag = h3_tag.find('a', class_="u-clickable-card__link") if h3_tag else None
    if a_tag:
        url = "https://www.aljazeera.com" + a_tag['href']
        title = a_tag.get_text(strip=True)
    else:
        continue

    # Date
    date_tag = article.find('div', class_="date-simple")
    date = ""
    if date_tag:
        # Try to get the visible date (aria-hidden="true")
        date_span = date_tag.find('span', attrs={"aria-hidden": "true"})
        date = date_span.get_text(strip=True) if date_span else date_tag.get_text(strip=True)

    # Optional: Excerpt as content (since not all cards have full content)
    excerpt_tag = article.find('div', class_="gc__excerpt")
    content = excerpt_tag.get_text(strip=True) if excerpt_tag else ""

    # Location: not available in card, leave blank or parse from content if possible
    location = ""

    # Only add articles from 2012 onwards
    if any(str(y) in date for y in range(2012, 2026)):
        data.append([title, content, url, date, location])

# 6. Save to CSV
df = pd.DataFrame(data, columns=['Title', 'Content', 'URL', 'Date', 'Location'])
df.to_csv('datasets/middle_east_news.csv', index=False)

driver.quit()
