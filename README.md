## Sales Analytics Dashboard (Streamlit)

An end-to-end **Sales Analytics Dashboard** built with **Streamlit**, **Pandas**, and **Plotly**.  
The app provides interactive KPIs, filters, and visualizations to explore sales performance across time, regions, product categories, and sales channels.

### Features

- **Interactive KPIs**
  - **Total Revenue**
  - **Total Profit**
  - **Total Orders**
  - **Average Order Value**
- **Rich Filtering**
  - **Date range** (2022–2024)
  - **Region** (North, South, East, West)
  - **Product Category** (Electronics, Furniture, Clothing, Grocery)
  - **Sales Channel** (Online, Retail)
- **Visualizations (Plotly)**
  - **Monthly Sales Trend** (line chart)
  - **Sales by Region** (bar chart)
  - **Profit by Category** (bar chart)
  - **Sales Channel Distribution** (pie chart)
  - **Top 10 Products by Revenue** (horizontal bar chart)
- **Data Table & Export**
  - Filtered data table
  - Download filtered rows as CSV
- **Performance & UX**
  - Cached data loading with `st.cache_data`
  - Clean layout using Streamlit columns and wide layout

### Tech Stack

- **Python 3.9+**
- **Streamlit**
- **Pandas**
- **NumPy**
- **Plotly Express**

---

### Project Structure

```text
sales-dashboard/
│
├── app.py                  # Main Streamlit app
├── data/
│   └── sales_data.csv      # Generated synthetic sales data
├── utils/
│   └── data_generator.py   # Script to generate realistic sales data
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

### Synthetic Data Generation

The dataset is generated via `utils/data_generator.py` and includes **realistic synthetic sales records**:

- **Columns**
  - `order_id`
  - `order_date` (2022–2024)
  - `region` (North, South, East, West)
  - `country`
  - `product_category` (Electronics, Furniture, Clothing, Grocery)
  - `product_name`
  - `sales_channel` (Online, Retail)
  - `quantity`
  - `unit_price`
  - `total_sales`
  - `profit`
  - `customer_segment` (Consumer, Corporate, Home Office)
- **Realism**
  - Proper date spread from 2022–2024 with bias toward recent dates
  - Product-specific base prices and profit margins
  - Quantities influenced by category and channel (e.g., grocery and retail tend to have higher quantities)
  - Profit calculated using realistic margin percentages with slight per-order variation

To regenerate the dataset:

```bash
cd sales-dashboard
python utils/data_generator.py
```

This will overwrite `data/sales_data.csv` with a fresh dataset (2,000+ rows).

---

### How to Run Locally

1. **Clone the repository**

   ```bash
   git clone <your-repo-url>.git
   cd sales-dashboard
   ```

2. **(Optional) Create and activate a virtual environment**

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Streamlit app**

   ```bash
   streamlit run app.py
   ```

5. **Open the app**

   Streamlit will print a local URL (typically `http://localhost:8501`) that you can open in your browser.

---

### Screenshots (Placeholder)

- **Dashboard Overview** – KPIs + key visualizations.
- **Filters in Action** – different segments, regions, and channels.
- **Top Products View** – ranked products by revenue.

> Add actual screenshots from your running app to this section before publishing on GitHub.

---

### Why This Project Is Useful for Businesses

- **Performance Monitoring**: Quickly track revenue, profit, and order volume trends over time.
- **Regional Insights**: Identify high- and low-performing regions for targeted strategy.
- **Product Strategy**: Understand which product categories and SKUs drive the most revenue and profit.
- **Channel Optimization**: Compare performance between online and retail channels.
- **Segment Analysis**: Explore performance across customer segments (Consumer, Corporate, Home Office).

This type of dashboard can support **sales, marketing, and leadership teams** by turning raw transactional data into actionable insights.

---

### Deployment (Streamlit Cloud)

You can easily deploy this app using **Streamlit Cloud**:

1. Push your project to a **public GitHub repository**.
2. Go to **[Streamlit Community Cloud](https://streamlit.io/cloud)** and sign in.
3. Click **“New app”** and connect your GitHub account.
4. Select your repository, branch, and set **`app.py`** as the entry point.
5. Click **Deploy**.

Streamlit Cloud will:

- Install dependencies from `requirements.txt`
- Run `streamlit run app.py`
- Provide a **public URL** you can share.

---

### Adding This Project to Your CV

You can describe this project on your CV as:

> **Sales Analytics Dashboard | Streamlit, Python, Plotly**  
> Built an end-to-end interactive sales dashboard with KPI tracking, filters, and visual analytics using Streamlit.  
> Generated realistic sales data, implemented business metrics, and deployed via Streamlit Cloud.

Include the **GitHub repository link** and (optionally) the **live Streamlit app URL** so recruiters can explore the dashboard directly.


