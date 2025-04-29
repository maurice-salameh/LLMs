import pandas as pd

# Load the CSV file
df = pd.read_csv('datasets/india-news-headlines.csv')

#remove headline_category
df = df.drop(columns=['headline_category'])

# Filter for publish_date between 20120101 and 20221231
df = df[(df['publish_date'] >= 20120101) & (df['publish_date'] <= 20221231)]

# add column named "date" with the value of publish_date
df['date'] = df['publish_date'].astype(str).str[:4] + '-' + df['publish_date'].astype(str).str[4:6] + '-' + df['publish_date'].astype(str).str[6:8]
df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')

# add column "location" with the value of "India"
df['location'] = 'India'

# Save filtered data to a new CSV file
df.to_csv('datasets/indian_news_2012_2022.csv', index=False)



