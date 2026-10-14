# ShopSage AI — AI-Powered Business Decision Assistant

**Turn sales data into actionable business insights.**

ShopSage AI is a Streamlit-based sales analytics application designed to help small shop owners and businesses understand their sales performance. Users can upload sales data, explore key performance indicators, identify product and category trends, check data quality, and receive rule-based business recommendations.

## The Problem

Small businesses may collect sales data without having an easy way to interpret it. ShopSage AI makes common sales metrics and patterns easier to understand through an interactive dashboard.

## Features

- **Sales analytics:** Track revenue, units sold, and unique orders.
- **Interactive filters:** Explore results by product, category, and date.
- **Data quality checks:** Identify duplicate rows, missing required values, and invalid dates.
- **Product performance:** Compare revenue, units sold, and revenue share.
- **Sales trends:** Explore daily revenue and category performance.
- **Revenue goal tracker:** Monitor progress toward a sales target.
- **Business recommendations:** Receive rule-based suggestions based on sales performance.
- **Question-answering assistant:** Ask supported questions about the selected sales data.
- **Downloadable reports:** Export filtered sales data, business summaries, and KPI reports.
## Dashboard Preview
![ShopSage AI Dashboard](https://raw.githubusercontent.com/sunnainatanveerda-debug/ShopSageAI/main/shopsage-dashboard.png)
![ShopSage AI Dashboard](https://raw.githubusercontent.com/sunnainatanveerda-debug/ShopSageAI/main/shopsage-dashboard.png1.png)
![ShopSage AI Dashboard](https://raw.githubusercontent.com/sunnainatanveerda-debug/ShopSageAI/main/shopsage-dashboard.png2.png)

## Technology Stack

- Python
- Pandas
- Streamlit
- Plotly

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/sunnainatanveerda-debug/ShopSageAI.git
cd ShopSageAI
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the application

```bash
python -m streamlit run app.py
```

Open the local URL displayed in your terminal.

## Dataset Format

The CSV file should include these columns:

- `order_id`
- `order_date`
- `product`
- `category`
- `quantity`
- `unit_price`

The application calculates revenue as quantity multiplied by unit price.

## Project Limitations

The current question-answering assistant uses predefined question patterns and calculated sales metrics. Business recommendations are rule-based; the application does not currently claim to use a generative AI model. Results depend on the quality and completeness of the uploaded data.

## Future Improvements

- Add a language-model-powered business assistant.
- Improve data validation and error handling.
- Introduce profit and margin analysis when cost data is available.
- Add more flexible natural-language questions.
- Expand testing with different real-world sales datasets.

## Project Links

- **GitHub:** https://github.com/sunnainatanveerda-debug/ShopSageAI
- **Live Demo:** https://shopsageai-nssbcjh9ji8kpc8wtsutdw.streamlit.app

## Author

Created by **Sunnaina Tanveer**.
