from typing import List, Dict
from collections import defaultdict
from app.services.prompt_utils import get_value_type

SYSTEM_HTML = (
    "You are a reliable and factual financial assistant. "
    "Respond using HTML only — never use Markdown. "
    "Use the exact display names and values from the <CONTEXT> section, where each row represents a fiscal period for a company. "
    "Format values as follows: dollar amounts with commas, a leading '$', and two decimal places; use K/M/B suffixes when large; percentages with '%' symbol. "
    "Highlight all metric names and values using <strong> tags. "
    "Summarize with plain text (in <p>) if the result has 2 or fewer rows/columns; otherwise, use a clean, minimal <table> with <thead> and <tbody>. "
    "Use concise headers with relevant emojis (e.g., 📈, 💸), and indicate trends using 🔼/🔻. "
    "Avoid showing calculation formulas unless explicitly requested. "
    "When multiple companies are involved, return only the top 10 by relevance or metric value (e.g., highest revenue), then suggest: "
    "<em>To explore more, please visit the filter page or request specific tickers.</em>"
)


def build_prompt(user_q: str, tables: List[Dict]) -> str:
    if not tables:
        return f"<p>{SYSTEM_HTML}</p><p><strong>Query:</strong> {user_q}</p><p>No financial data available.</p>"

    period_order = ["Q1", "Q2", "Q3", "Q4", "FY"]
    grouped = defaultdict(lambda: defaultdict(lambda: defaultdict(str)))

    tickers = set()
    years = set()
    periods = set()

    for row in tables:
        metric = row.get("metric")
        raw_metric = row.get("raw_metric", metric)
        value = row.get("value")
        year = row.get("fiscal_year")
        period = row.get("period", "FY")
        ticker = row.get("ticker", "UNKNOWN").upper()
        display_name = row.get("display_name", metric.replace("_", " ").title())
        label = f"{display_name} ({ticker})"

        tickers.add(ticker)
        years.add(year)
        periods.add(period)

        value_type = get_value_type(raw_metric)
        if value is None:
            val_str = "<strong>N/A</strong>"
        else:
            try:
                amount = float(value)
                if value_type == "percent":
                    val_str = f"<strong>{round(amount * 100, 2)}%</strong>"
                elif value_type == "plain":
                    val_str = f"<strong>{round(amount, 2)}</strong>"
                else:
                    if amount >= 1e9:
                        val_str = f"<strong>${round(amount / 1e9, 1)}B</strong>"
                    elif amount >= 1e6:
                        val_str = f"<strong>${round(amount / 1e6, 1)}M</strong>"
                    elif amount >= 1e3:
                        val_str = f"<strong>${round(amount / 1e3, 1)}K</strong>"
                    else:
                        val_str = f"<strong>${round(amount, 2):,}</strong>"
            except:
                val_str = "<strong>Invalid</strong>"

        grouped[label][year][period] = val_str

    multiple = len(tickers) > 1 or len(years) > 1 or len(periods) > 1
    context_parts = []

    for label, year_data in grouped.items():
        year_list = sorted(year_data.keys(), reverse=True)
        period_list = sorted({p for y in year_data for p in year_data[y]}, key=period_order.index)

        if multiple:
            html = f"<h4>{label}</h4><table border='1'><thead><tr><th>Year</th>"
            for p in period_list:
                html += f"<th>{p}</th>"
            html += "</tr></thead><tbody>"
            for y in year_list:
                html += f"<tr><td>{y}</td>"
                for p in period_list:
                    val = year_data[y].get(p, "<strong>N/A</strong>")
                    html += f"<td>{val}</td>"
                html += "</tr>"
            html += "</tbody></table>"
            context_parts.append(html)
        else:
            y = year_list[0]
            p = period_list[0]
            val = year_data[y][p]
            context_parts.append(f"<p><strong>{label}</strong> for {p} {y}: {val}</p>")

    context_html = "".join(context_parts)
    final_html = (
        f"<p>{SYSTEM_HTML}</p><div><h3>User Query</h3><p>{user_q}</p>"
        f"<h3>Context</h3>{context_html}</div>"
    )
    return final_html
