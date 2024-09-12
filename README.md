# Time series forecasting for vegetable price

## Project Overview

This project aims to predict the prices of vegetables for the next 7 days based on historical data scraped from the Katimati Vegetable Market website in Nepal. The project involves data scraping, preprocessing, and time series forecasting using Long Short-Term Memory (LSTM) networks.

## Tools and Technologies

- **Data Scraping:**
  - **Selenium:** Used for automating browser interactions and navigating the Katimati Vegetable Market website.
  - **BeautifulSoup4:** Employed for parsing and extracting the relevant vegetable price data from the website.

- **Data Processing:**
  - **NumPy:** Utilized for numerical operations and data manipulation.
  - **Pandas:** Used for data cleaning, preprocessing, and organizing the dataset.

- **Prediction Model:**
  - **LSTM (Long Short-Term Memory):** Applied to predict the vegetable prices for the next 7 days based on historical data.

## Data Collection

- **Source:** Katimati Vegetable Market website.
- **Frequency:** Daily updates.
- **Data Included:** Prices for various vegetables and fruits.

## Steps

1. **Data Scraping:**
   - Automated browser interactions using Selenium to navigate to the daily vegetable price page.
   - Extracted data with BeautifulSoup4 and collected it into a structured format.

2. **Data Preprocessing:**
   - Combined daily data into a comprehensive dataset.
   - Cleaned and preprocessed data using NumPy and Pandas to handle missing values and normalize prices.

3. **Model Training:**
   - Utilized LSTM to train the model on historical price data.
   - Predicted vegetable prices for the upcoming 7 days.



