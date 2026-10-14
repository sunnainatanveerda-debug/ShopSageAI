# ShopSage AI — Your Business Decision Assistant

## About the Project
ShopSage AI is a Python-based sales analytics application that helps small businesses understand their sales data and make better-informed business decisions.

Users can upload a CSV sales dataset, explore key performance indicators, view interactive charts, identify product and category performance, and download business reports.

## Features
- Upload sales data using a CSV file
- Check data quality, including missing values and invalid records
- Filter sales by date, product, and category
- Calculate total revenue, units sold, and unique orders
- Explore product and category performance
- Visualize daily revenue trends
- Generate rule-based business recommendations
- Track progress toward a revenue goal
- Download sales, KPI, and business summary reports

## Technology Stack
- Python
- Pandas
- Streamlit
- Plotly

## Required CSV Columns
The uploaded dataset should contain these columns:

`order_id`, `order_date`, `product`, `category`, `quantity`, `unit_price`

## Run Locally
1. Install Python.
2. Open a terminal in the project folder.
3. Install the dependencies:

   `python -m pip install -r requirements.txt`

4. Start the application:

   `python -m streamlit run app.py`

5. Open the local URL shown in the terminal.

## Project Status
ShopSage AI is a work in progress. Its current recommendations are rule-based and use the uploaded sales data.

## Future Improvements
- Add AI-powered explanations of sales trends
- Improve data-quality diagnostics
- Add more business-focused insights and testing

## Purpose
The goal is to make sales analytics more accessible to small businesses and beginners who want to turn raw data into useful information.
