# 📊 InsightThread – Financial Query Engine

InsightThread is a powerful backend service that extracts **ticker**, **financial period**, and **metrics** from user queries, intelligently routes the request to the appropriate database schema and table, and returns results in both tabular and natural language formats.

---

## 🚀 Features

- 🔍 Extracts relevant entities from natural language queries (e.g., ticker symbols, years, metrics)
- 🧠 Targets the correct financial schema and table dynamically
- 📊 Presents data as a structured table and readable summary
- 🔄 Supports real-time API interaction via a local UI
- 💡 Designed to support general query output in HTML (coming soon)

---

## 🛠️ Installation

Clone the repository and set up the environment:

```bash
git clone https://github.com/your-username/insightthread.git
cd insightthread
python -m venv venv
.\venv\Scripts\activate    # On Windows
# source venv/bin/activate # On Mac/Linux
pip install -r requirements.txt
copy .env_example .env  # Windows
# cp .env_example .env  # Mac/Linux

▶️ How to Run
Start the application with:
uvicorn app.main:create_app --factory --reload
Once the server starts, open your browser and go to:


http://127.0.0.1:8000/ui
You can now input queries such as:

"What is the revenue of AAPL in 2023?"

"Show the EBIT margin for MSFT in Q1 2024"

🔮 Future Work
🌐 Generate HTML output for general non financial queries
